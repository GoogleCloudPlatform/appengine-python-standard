#!/usr/bin/env python
#
# Copyright 2007 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#














"""A tasklet decorator.

Tasklets are a way to write concurrently running functions without
threads; tasklets are executed by an event loop and can suspend
themselves blocking for I/O or some other operation using a yield
statement.  The notion of a blocking operation is abstracted into the
Future class, but a tasklet may also yield an RPC in order to wait for
that RPC to complete.

The @tasklet decorator wraps generator function so that when it is
called, a Future is returned while the generator is executed by the
event loop.  Within the tasklet, any yield of a Future waits for and
returns the Future's result.  For example::

  @tasklet
  def foo():
    a = yield <some Future>
    b = yield <another Future>
    raise Return(a + b)

  def main():
    f = foo()
    x = f.get_result()
    print x

Note that blocking until the Future's result is available using
get_result() is somewhat inefficient (though not vastly -- it is not
busy-waiting).  In most cases such code should be rewritten as a tasklet
instead::

  @tasklet
  def main_tasklet():
    f = foo()
    x = yield f
    print x

Calling a tasklet automatically schedules it with the event loop::

  def main():
    f = main_tasklet()
    eventloop.run()  # Run until no tasklets left to do
    f.done()  # Returns True

As a special feature, if the wrapped function is not a generator
function, its return value is returned via the Future.  This makes the
following two equivalent::

  @tasklet
  def foo():
    return 42

  @tasklet
  def foo():
    if False: yield  # The presence of 'yield' makes foo a generator
    raise Return(42)  # Or, after PEP 380, return 42

This feature (inspired by Monocle) is handy in case you are
implementing an interface that expects tasklets but you have no need to
suspend -- there's no need to insert a dummy yield in order to make
the tasklet into a generator.
"""

import collections
import functools
import logging
import os
import sys
import threading
import types
import weakref

from google.appengine.api import apiproxy_rpc
from google.appengine.api import apiproxy_stub
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import full_app_id
from google.appengine.api import namespace_manager
from google.appengine.datastore import datastore_pbs
from google.appengine.datastore import datastore_rpc
from google.appengine.ext.ndb import eventloop
from google.appengine.ext.ndb import utils
from google.appengine.runtime import apiproxy
import six
from six.moves import map

__all__ = ['Return', 'tasklet', 'synctasklet', 'toplevel', 'sleep',
           'add_flow_exception', 'get_return_value',
           'get_context', 'set_context',
           'make_default_context', 'make_context',
           'Future', 'MultiFuture', 'QueueFuture', 'SerialQueueFuture',
           'ReducingFuture',
          ]

_logging_debug = utils.logging_debug

_CALLBACK_KEY = '__CALLBACK__'


def _is_generator(obj):
  """Helper to test for a generator object.

  NOTE: This tests for the (iterable) object returned by calling a
  generator function, not for a generator function.
  """
  return isinstance(obj, types.GeneratorType)


class _State(threading.local):
  """Hold thread-local state."""

  def __init__(self):
    super(_State, self).__init__()
    self.current_context = None
    self.all_generators = weakref.WeakSet()
    self.all_pending = set()

  def set_context(self, ctx):
    self.current_context = ctx

  def add_generator(self, gen):
    if _CALLBACK_KEY not in os.environ:
      apiproxy.SetRequestEndCallback(self.reset)
      os.environ[_CALLBACK_KEY] = '1'

    _logging_debug('all_generators: add %s', gen)
    self.all_generators.add(gen)

  def add_pending(self, fut):
    if _CALLBACK_KEY not in os.environ:
      apiproxy.SetRequestEndCallback(self.reset)
      os.environ[_CALLBACK_KEY] = '1'

    _logging_debug('all_pending: add %s', fut)
    self.all_pending.add(fut)

  def remove_pending(self, fut, status='success'):
    if fut in self.all_pending:
      _logging_debug('all_pending: %s: remove %s', status, fut)
      self.all_pending.remove(fut)
    else:
      _logging_debug('all_pending: %s: not found %s', status, fut)

  def clear_all_generators(self):
    if self.all_generators:
      _logging_debug('all_generators: clear %s', self.all_generators)
      for gen in self.all_generators:
        gen.close()
      self.all_generators.clear()
    else:
      _logging_debug('all_generators: clear no-op')

  def clear_all_pending(self):
    if self.all_pending:
      _logging_debug('all_pending: clear %s', self.all_pending)
      self.all_pending.clear()
    else:
      _logging_debug('all_pending: clear no-op')

  def dump_all_pending(self, verbose=False):
    pending = []
    for fut in self.all_pending:
      if verbose:
        line = fut.dump() + ('\n' + '-' * 40)
      else:
        line = fut.dump_stack()
      pending.append(line)
    return '\n'.join(pending)

  def reset(self, unused_req_id):
    self.current_context = None
    ev = eventloop.get_event_loop()
    ev.clear()
    self.clear_all_pending()
    self.clear_all_generators()


_state = _State()



_flow_exceptions = ()


def add_flow_exception(exc):
  """Add an exception that should not be logged.

  The argument must be a subclass of Exception.
  """
  global _flow_exceptions
  if not isinstance(exc, type) or not issubclass(exc, Exception):
    raise TypeError('Expected an Exception subclass, got %r' % (exc,))
  as_set = set(_flow_exceptions)
  as_set.add(exc)
  _flow_exceptions = tuple(as_set)


def _init_flow_exceptions():
  """Internal helper to initialize _flow_exceptions.

  This automatically adds webob.exc.HTTPException, if it can be imported.
  """
  global _flow_exceptions
  _flow_exceptions = ()
  add_flow_exception(datastore_errors.Rollback)
  try:
    from webob import exc
  except ImportError:
    pass
  else:
    add_flow_exception(exc.HTTPException)


_init_flow_exceptions()


class Future(object):
  """A Future has 0 or more callbacks.

  The callbacks will be called when the result is ready.

  NOTE: This is somewhat inspired but not conformant to the Future interface
  defined by PEP 3148.  It is also inspired (and tries to be somewhat
  compatible with) the App Engine specific UserRPC and MultiRpc classes.
  """




  IDLE = apiproxy_rpc.RPC.IDLE
  RUNNING = apiproxy_rpc.RPC.RUNNING
  FINISHING = apiproxy_rpc.RPC.FINISHING



  _geninfo = None

  def __init__(self, info=None):


    __ndb_debug__ = 'SKIP'
    self._info = info
    self._where = utils.get_stack()
    self._context = None
    self._reset()

  def _reset(self):
    self._done = False
    self._result = None
    self._exception = None
    self._traceback = None
    self._callbacks = []
    self._immediate_callbacks = []
    _state.add_pending(self)
    self._next = None




  def __repr__(self):
    if self._done:
      if self._exception is not None:
        state = 'exception %s: %s' % (self._exception.__class__.__name__,
                                      self._exception)
      else:
        state = 'result %r' % (self._result,)
    else:
      state = 'pending'
    line = '?'
    for line in self._where:
      if 'tasklets.py' not in line:
        break
    if self._info:
      line += ' for %s' % self._info
    if self._geninfo:
      line += ' %s' % self._geninfo
    return '<%s %x created by %s; %s>' % (
        self.__class__.__name__, id(self), line, state)

  def dump(self):
    return '%s\nCreated by %s' % (self.dump_stack(),
                                  '\n called by '.join(self._where))

  def dump_stack(self):
    lines = []
    fut = self
    while fut is not None:
      lines.append(str(fut))
      fut = fut._next
    return '\n waiting for '.join(lines)

  def add_callback(self, callback, *args, **kwds):
    if self._done:
      eventloop.queue_call(None, callback, *args, **kwds)
    else:
      self._callbacks.append((callback, args, kwds))

  def add_immediate_callback(self, callback, *args, **kwds):
    if self._done:
      callback(*args, **kwds)
    else:
      self._immediate_callbacks.append((callback, args, kwds))

  def set_result(self, result):
    if self._done:
      raise RuntimeError('Result cannot be set twice.')
    self._result = result
    self._done = True
    _state.remove_pending(self)
    for callback, args, kwds in self._immediate_callbacks:
      callback(*args, **kwds)
    for callback, args, kwds in self._callbacks:
      eventloop.queue_call(None, callback, *args, **kwds)

  def set_exception(self, exc, tb=None):
    if not isinstance(exc, BaseException):
      raise TypeError('exc must be an Exception; received %r' % exc)
    if self._done:
      raise RuntimeError('Exception cannot be set twice.')
    self._exception = exc
    self._traceback = tb
    self._done = True
    _state.remove_pending(self, status='fail')
    for callback, args, kwds in self._immediate_callbacks:
      callback(*args, **kwds)
    for callback, args, kwds in self._callbacks:
      eventloop.queue_call(None, callback, *args, **kwds)

  def done(self):
    return self._done

  @property
  def state(self):


    if self._done:
      return self.FINISHING
    else:
      return self.RUNNING

  def wait(self):
    if self._done:
      return
    ev = eventloop.get_event_loop()
    while not self._done:
      if not ev.run1():
        logging.info('Deadlock in %s', self)
        logging.info('All pending Futures:\n%s', _state.dump_all_pending())
        _logging_debug('All pending Futures (verbose):\n%s',
                       _state.dump_all_pending(verbose=True))
        self.set_exception(RuntimeError('Deadlock waiting for %s' % self))

  def get_exception(self):
    self.wait()
    return self._exception

  def get_traceback(self):
    self.wait()
    return self._traceback

  def check_success(self):
    self.wait()
    if self._exception is not None:
      six.reraise(self._exception.__class__, self._exception, self._traceback)

  def get_result(self):
    self.check_success()
    return self._result


  @classmethod
  def wait_any(cls, futures):

    waiting_on = set(futures)
    ev = eventloop.get_event_loop()
    while waiting_on:
      for f in waiting_on:
        if f.state == cls.FINISHING:
          return f
      ev.run1()
    return None


  @classmethod
  def wait_all(cls, futures):

    waiting_on = set(futures)
    ev = eventloop.get_event_loop()
    while waiting_on:
      waiting_on = set(f for f in waiting_on if f.state == cls.RUNNING)
      ev.run1()

  def _help_tasklet_along(self, ns, ds_conn, gen, val=None, exc=None, tb=None):

    info = utils.gen_info(gen)

    __ndb_debug__ = info
    try:
      save_context = get_context()
      save_namespace = namespace_manager.get_namespace()
      save_ds_connection = datastore._GetConnection()
      try:
        set_context(self._context)
        if ns != save_namespace:
          namespace_manager.set_namespace(ns)
        if ds_conn is not save_ds_connection:
          datastore._SetConnection(ds_conn)
        if exc is not None:
          _logging_debug('Throwing %s(%s) into %s',
                         exc.__class__.__name__, exc, info)
          value = gen.throw(exc.__class__, exc, tb)
        else:
          _logging_debug('Sending %r to %s', val, info)
          value = gen.send(val)
          self._context = get_context()
      finally:
        ns = namespace_manager.get_namespace()
        ds_conn = datastore._GetConnection()
        set_context(save_context)
        if save_namespace != ns:
          namespace_manager.set_namespace(save_namespace)
        if save_ds_connection is not ds_conn:
          datastore._SetConnection(save_ds_connection)

    except (StopIteration, Return) as err:
      result = get_return_value(err)
      _logging_debug('%s returned %r', info, result)
      self.set_result(result)
      return

    except GeneratorExit:




      raise

    except Exception as err:
      _, _, tb = sys.exc_info()
      if isinstance(err, _flow_exceptions):


        _logging_debug('%s raised %s(%s)',
                       info, err.__class__.__name__, err)
      elif utils.DEBUG and logging.getLogger().level < logging.DEBUG:


        logging.warning('%s raised %s(%s)',
                        info, err.__class__.__name__, err, exc_info=True)
      else:

        logging.warning('%s raised %s(%s)', info, err.__class__.__name__, err)
      self.set_exception(err, tb)
      return

    else:
      _logging_debug('%s yielded %r', info, value)
      if isinstance(value, (apiproxy_stub_map.UserRPC,
                            datastore_rpc.MultiRpc)):

        eventloop.queue_rpc(value, self._on_rpc_completion,
                            value, ns, ds_conn, gen)
        return
      if isinstance(value, Future):

        if self._next:
          raise RuntimeError('Future has already completed yet next is %r' %
                             self._next)
        self._next = value
        self._geninfo = utils.gen_info(gen)
        _logging_debug('%s is now blocked waiting for %s', self, value)
        value.add_callback(self._on_future_completion, value, ns, ds_conn, gen)
        return
      if isinstance(value, (tuple, list)):

        info = 'multi-yield from %s' % utils.gen_info(gen)
        mfut = MultiFuture(info)
        try:
          for subfuture in value:
            mfut.add_dependent(subfuture)
          mfut.complete()
        except GeneratorExit:
          raise
        except Exception as err:
          _, _, tb = sys.exc_info()
          mfut.set_exception(err, tb)
        mfut.add_callback(self._on_future_completion, mfut, ns, ds_conn, gen)
        return
      if _is_generator(value):

        raise NotImplementedError('Cannot defer to another generator.')
      raise RuntimeError('A tasklet should not yield a plain value: '
                         '%.200s yielded %.200r' % (info, value))

  def _on_rpc_completion(self, rpc, ns, ds_conn, gen):
    try:
      result = rpc.get_result()
    except GeneratorExit:
      raise
    except Exception as err:
      _, _, tb = sys.exc_info()
      self._help_tasklet_along(ns, ds_conn, gen, exc=err, tb=tb)
    else:
      self._help_tasklet_along(ns, ds_conn, gen, result)

  def _on_future_completion(self, future, ns, ds_conn, gen):
    if self._next is future:
      self._next = None
      self._geninfo = None
      _logging_debug('%s is no longer blocked waiting for %s', self, future)
    exc = future.get_exception()
    if exc is not None:
      self._help_tasklet_along(ns, ds_conn, gen,
                               exc=exc, tb=future.get_traceback())
    else:
      val = future.get_result()
      self._help_tasklet_along(ns, ds_conn, gen, val)


def sleep(dt):
  """Public function to sleep some time.

  Example:
    yield tasklets.sleep(0.5)  # Sleep for half a sec.
  """
  fut = Future('sleep(%.3f)' % dt)
  eventloop.queue_call(dt, fut.set_result, None)
  return fut


class MultiFuture(Future):
  """A Future that depends on multiple other Futures.

  This is used internally by 'v1, v2, ... = yield f1, f2, ...'; the
  semantics (e.g. error handling) are constrained by that use case.

  The protocol from the caller's POV is::

    mf = MultiFuture()
    mf.add_dependent(<some other Future>)  -OR- mf.putq(<some value>)
    mf.add_dependent(<some other Future>)  -OR- mf.putq(<some value>)
      .
      . (More mf.add_dependent() and/or mf.putq() calls)
      .
    mf.complete()  # No more dependents will be added.
      .
      . (Time passes)
      .
    results = mf.get_result()

  Now, results is a list of results from all dependent Futures in
  the order in which they were added.

  It is legal to add the same dependent multiple times.

  Callbacks can be added at any point.

  From a dependent Future POV, there's nothing to be done: a callback
  is automatically added to each dependent Future which will signal
  its completion to the MultiFuture.

  Error handling: if any dependent future raises an error, it is
  propagated to mf.  To force an early error, you can call
  mf.set_exception() instead of mf.complete().  After this you can't
  call mf.add_dependent() or mf.putq() any more.
  """

  def __init__(self, info=None):

    __ndb_debug__ = 'SKIP'
    self._full = False
    self._dependents = set()
    self._results = []
    super(MultiFuture, self).__init__(info=info)

  def __repr__(self):


    line = super(MultiFuture, self).__repr__()
    lines = [line]
    for fut in self._results:
      lines.append(fut.dump_stack().replace('\n', '\n  '))
    return '\n waiting for '.join(lines)



  def complete(self):
    if self._full:
      raise RuntimeError('MultiFuture cannot complete twice.')
    self._full = True
    if not self._dependents:
      self._finish()


  def set_exception(self, exc, tb=None):
    self._full = True
    super(MultiFuture, self).set_exception(exc, tb)

  def _finish(self):
    if not self._full:
      raise RuntimeError('MultiFuture cannot finish until completed.')
    if self._dependents:
      raise RuntimeError('MultiFuture cannot finish whilst waiting for '
                         'dependents %r' % self._dependents)
    if self._done:
      raise RuntimeError('MultiFuture done before finishing.')
    try:
      result = [r.get_result() for r in self._results]
    except GeneratorExit:
      raise
    except Exception as err:
      _, _, tb = sys.exc_info()
      self.set_exception(err, tb)
    else:
      self.set_result(result)

  def putq(self, value):
    if isinstance(value, Future):
      fut = value
    else:
      fut = Future()
      fut.set_result(value)
    self.add_dependent(fut)

  def add_dependent(self, fut):
    if isinstance(fut, list):
      mfut = MultiFuture()
      list(map(mfut.add_dependent, fut))
      mfut.complete()
      fut = mfut
    elif not isinstance(fut, Future):
      raise TypeError('Expected Future, received %s: %r' % (type(fut), fut))
    if self._full:
      raise RuntimeError('MultiFuture cannot add a dependent once complete.')
    self._results.append(fut)
    if fut not in self._dependents:
      self._dependents.add(fut)
      fut.add_callback(self._signal_dependent_done, fut)

  def _signal_dependent_done(self, fut):
    self._dependents.remove(fut)
    if self._full and not self._dependents and not self._done:
      self._finish()


class QueueFuture(Future):
  """A Queue following the same protocol as MultiFuture.

  However, instead of returning results as a list, it lets you
  retrieve results as soon as they are ready, one at a time, using
  getq().  The Future itself finishes with a result of None when the
  last result is ready (regardless of whether it was retrieved).

  The getq() method returns a Future which blocks until the next
  result is ready, and then returns that result.  Each getq() call
  retrieves one unique result.  Extra getq() calls after the last
  result is already returned return EOFError as their Future's
  exception.  (I.e., q.getq() returns a Future as always, but yieding
  that Future raises EOFError.)

  NOTE: Values can also be pushed directly via .putq(value).  However
  there is no flow control -- if the producer is faster than the
  consumer, the queue will grow unbounded.
  """


  def __init__(self, info=None):
    self._full = False
    self._dependents = set()
    self._completed = collections.deque()
    self._waiting = collections.deque()


    super(QueueFuture, self).__init__(info=info)



  def complete(self):
    if self._full:
      raise RuntimeError('MultiFuture cannot complete twice.')
    self._full = True
    if not self._dependents:
      self.set_result(None)
      self._mark_finished()

  def set_exception(self, exc, tb=None):
    self._full = True
    super(QueueFuture, self).set_exception(exc, tb)
    if not self._dependents:
      self._mark_finished()

  def putq(self, value):
    if isinstance(value, Future):
      fut = value
    else:
      fut = Future()
      fut.set_result(value)
    self.add_dependent(fut)

  def add_dependent(self, fut):
    if not isinstance(fut, Future):
      raise TypeError('fut must be a Future instance; received %r' % fut)
    if self._full:
      raise RuntimeError('QueueFuture add dependent once complete.')
    if fut not in self._dependents:
      self._dependents.add(fut)
      fut.add_callback(self._signal_dependent_done, fut)

  def _signal_dependent_done(self, fut):
    if not fut.done():
      raise RuntimeError('Future not done before signalling dependant done.')
    self._dependents.remove(fut)
    exc = fut.get_exception()
    tb = fut.get_traceback()
    val = None
    if exc is None:
      val = fut.get_result()
    if self._waiting:
      waiter = self._waiting.popleft()
      self._pass_result(waiter, exc, tb, val)
    else:
      self._completed.append((exc, tb, val))
    if self._full and not self._dependents and not self._done:
      self.set_result(None)
      self._mark_finished()

  def _mark_finished(self):
    if not self.done():
      raise RuntimeError('Future not done before marking as finished.')
    while self._waiting:
      waiter = self._waiting.popleft()
      self._pass_eof(waiter)

  def getq(self):
    fut = Future()
    if self._completed:
      exc, tb, val = self._completed.popleft()
      self._pass_result(fut, exc, tb, val)
    elif self._full and not self._dependents:
      self._pass_eof(fut)
    else:
      self._waiting.append(fut)
    return fut

  def _pass_eof(self, fut):
    if not self._done:
      raise RuntimeError('QueueFuture cannot pass EOF until done.')
    exc = self.get_exception()
    if exc is not None:
      tb = self.get_traceback()
    else:
      exc = EOFError('Queue is empty')
      tb = None
    self._pass_result(fut, exc, tb, None)

  def _pass_result(self, fut, exc, tb, val):
    if exc is not None:
      fut.set_exception(exc, tb)
    else:
      fut.set_result(val)


class SerialQueueFuture(Future):
  """Like QueueFuture but maintains the order of insertion.

  This class is used by Query operations.

  Invariants:

  - At least one of _queue and _waiting is empty.
  - The Futures in _waiting are always pending.

  (The Futures in _queue may be pending or completed.)

  In the discussion below, add_dependent() is treated the same way as
  putq().

  If putq() is ahead of getq(), the situation is like this:

                         putq()
                         v
    _queue: [f1, f2, ...]; _waiting: []
    ^
    getq()

  Here, putq() appends a Future to the right of _queue, and getq()
  removes one from the left.

  If getq() is ahead of putq(), it's like this:

              putq()
              v
    _queue: []; _waiting: [f1, f2, ...]
                                       ^
                                       getq()

  Here, putq() removes a Future from the left of _waiting, and getq()
  appends one to the right.

  When both are empty, putq() appends a Future to the right of _queue,
  while getq() appends one to the right of _waiting.

  The _full flag means that no more calls to putq() will be made; it
  is set by calling either complete() or set_exception().

  Calling complete() signals that no more putq() calls will be made.
  If getq() is behind, subsequent getq() calls will eat up _queue
  until it is empty, and after that will return a Future that passes
  EOFError (note that getq() itself never raises EOFError).  If getq()
  is ahead when complete() is called, the Futures in _waiting are all
  passed an EOFError exception (thereby eating up _waiting).

  If, instead of complete(), set_exception() is called, the exception
  and traceback set there will be used instead of EOFError.
  """

  def __init__(self, info=None):
    self._queue = collections.deque()
    self._waiting = collections.deque()
    super(SerialQueueFuture, self).__init__(info=info)



  def complete(self):
    while self._waiting:
      waiter = self._waiting.popleft()
      waiter.set_exception(EOFError('Queue is empty'))



    self.set_result(None)

  def set_exception(self, exc, tb=None):
    super(SerialQueueFuture, self).set_exception(exc, tb)
    while self._waiting:
      waiter = self._waiting.popleft()
      waiter.set_exception(exc, tb)

  def putq(self, value):
    if isinstance(value, Future):
      fut = value
    else:
      if self._waiting:
        waiter = self._waiting.popleft()
        waiter.set_result(value)
        return
      fut = Future()
      fut.set_result(value)
    self.add_dependent(fut)

  def add_dependent(self, fut):
    if not isinstance(fut, Future):
      raise TypeError('fut must be a Future instance; received %r' % fut)
    if self._done:
      raise RuntimeError('SerialQueueFuture cannot add dependent '
                         'once complete.')
    if self._waiting:
      waiter = self._waiting.popleft()
      fut.add_callback(_transfer_result, fut, waiter)
    else:
      self._queue.append(fut)

  def getq(self):
    if self._queue:
      fut = self._queue.popleft()
    else:
      fut = Future()
      if self._done:
        err = self.get_exception()
        if err is not None:
          tb = self.get_traceback()
        else:
          err = EOFError('Queue is empty')
          tb = None
        fut.set_exception(err, tb)
      else:
        self._waiting.append(fut)
    return fut


def _transfer_result(fut1, fut2):
  """Helper to transfer result or errors from one Future to another."""
  exc = fut1.get_exception()
  if exc is not None:
    tb = fut1.get_traceback()
    fut2.set_exception(exc, tb)
  else:
    val = fut1.get_result()
    fut2.set_result(val)


class ReducingFuture(Future):
  """A Queue following the same protocol as MultiFuture.

  However the result, instead of being a list of results of dependent
  Futures, is computed by calling a 'reducer' tasklet.  The reducer tasklet
  takes a list of values and returns a single value.  It may be called
  multiple times on sublists of values and should behave like
  e.g. sum().

  NOTE: The reducer input values may be reordered compared to the
  order in which they were added to the queue.
  """


  def __init__(self, reducer, info=None, batch_size=20):
    self._reducer = reducer
    self._batch_size = batch_size
    self._full = False
    self._dependents = set()
    self._completed = collections.deque()
    self._queue = collections.deque()
    super(ReducingFuture, self).__init__(info=info)



  def complete(self):
    if self._full:
      raise RuntimeError('ReducingFuture cannot complete twice.')
    self._full = True
    if not self._dependents:
      self._mark_finished()

  def set_exception(self, exc, tb=None):
    self._full = True
    self._queue.clear()
    super(ReducingFuture, self).set_exception(exc, tb)

  def putq(self, value):
    if isinstance(value, Future):
      fut = value
    else:
      fut = Future()
      fut.set_result(value)
    self.add_dependent(fut)

  def add_dependent(self, fut):
    if self._full:
      raise RuntimeError('ReducingFuture cannot add dependent once complete.')
    self._internal_add_dependent(fut)

  def _internal_add_dependent(self, fut):
    if not isinstance(fut, Future):
      raise TypeError('fut must be a Future; received %r' % fut)
    if fut not in self._dependents:
      self._dependents.add(fut)
      fut.add_callback(self._signal_dependent_done, fut)

  def _signal_dependent_done(self, fut):
    if not fut.done():
      raise RuntimeError('Future not done before signalling dependant done.')
    self._dependents.remove(fut)
    if self._done:
      return
    try:
      val = fut.get_result()
    except GeneratorExit:
      raise
    except Exception as err:
      _, _, tb = sys.exc_info()
      self.set_exception(err, tb)
      return
    self._queue.append(val)
    if len(self._queue) >= self._batch_size:
      todo = list(self._queue)
      self._queue.clear()
      try:
        nval = self._reducer(todo)
      except GeneratorExit:
        raise
      except Exception as err:
        _, _, tb = sys.exc_info()
        self.set_exception(err, tb)
        return
      if isinstance(nval, Future):
        self._internal_add_dependent(nval)
      else:
        self._queue.append(nval)
    if self._full and not self._dependents:
      self._mark_finished()

  def _mark_finished(self):
    if not self._queue:
      self.set_result(None)
    elif len(self._queue) == 1:
      self.set_result(self._queue.pop())
    else:
      todo = list(self._queue)
      self._queue.clear()
      try:
        nval = self._reducer(todo)
      except GeneratorExit:
        raise
      except Exception as err:
        _, _, tb = sys.exc_info()
        self.set_exception(err, tb)
        return
      if isinstance(nval, Future):
        self._internal_add_dependent(nval)
      else:
        self.set_result(nval)


class Return(Exception):
  """Return from a tasklet in Python 2.

  In Python 2, generators may not return a value. In order to return a value
  from a tasklet, then, it is necessary to raise an instance of this
  exception with the return value:

      @ndb.tasklet
      def get_some_stuff():
        future1 = get_something_async()
        future2 = get_something_else_async()
        thing1, thing2 = yield future1, future2
        result = compute_result(thing1, thing2)
        raise ndb.Return(result)

  In Python 3, you can simply return the result:

      @ndb.tasklet
      def get_some_stuff():
        future1 = get_something_async()
        future2 = get_something_else_async()
        thing1, thing2 = yield future1, future2
        result = compute_result(thing1, thing2)
        return result
  """


def get_return_value(err):

  if not err.args:
    result = None
  elif len(err.args) == 1:
    result = err.args[0]
  else:
    result = err.args
  return result


def tasklet(func):


  @functools.wraps(func)
  def tasklet_wrapper(*args, **kwds):






    __ndb_debug__ = utils.func_info(func)
    fut = Future('tasklet %s' % utils.func_info(func))
    fut._context = get_context()
    try:
      result = func(*args, **kwds)
    except (StopIteration, Return) as err:


      result = get_return_value(err)
    if _is_generator(result):
      ns = namespace_manager.get_namespace()
      ds_conn = datastore._GetConnection()
      _state.add_generator(result)
      eventloop.queue_call(None, fut._help_tasklet_along, ns, ds_conn, result)
    else:
      fut.set_result(result)
    return fut

  return tasklet_wrapper


def synctasklet(func):
  """Decorator to run a function as a tasklet when called.

  Use this to wrap a request handler function that will be called by
  some web application framework (e.g. a Django view function or a
  webapp.RequestHandler.get method).
  """
  taskletfunc = tasklet(func)

  @functools.wraps(func)
  def synctasklet_wrapper(*args, **kwds):

    __ndb_debug__ = utils.func_info(func)
    return taskletfunc(*args, **kwds).get_result()
  return synctasklet_wrapper


def toplevel(func):
  """A sync tasklet that sets a fresh default Context.

  Use this for toplevel view functions such as
  webapp.RequestHandler.get() or Django view functions.
  """
  synctaskletfunc = synctasklet(func)

  @functools.wraps(func)
  def add_context_wrapper(*args, **kwds):

    __ndb_debug__ = utils.func_info(func)
    _state.clear_all_pending()

    ctx = make_default_context()
    try:
      set_context(ctx)
      return synctaskletfunc(*args, **kwds)
    finally:
      set_context(None)
      ctx.flush().check_success()
      eventloop.run()
  return add_context_wrapper


_CONTEXT_KEY = '__CONTEXT__'

_DATASTORE_APP_ID_ENV = 'DATASTORE_APP_ID'
_DATASTORE_PROJECT_ID_ENV = 'DATASTORE_PROJECT_ID'
_DATASTORE_ADDITIONAL_APP_IDS_ENV = 'DATASTORE_ADDITIONAL_APP_IDS'
_DATASTORE_USE_PROJECT_ID_AS_APP_ID_ENV = 'DATASTORE_USE_PROJECT_ID_AS_APP_ID'


def get_context():

  ctx = None
  if os.getenv(_CONTEXT_KEY):
    ctx = _state.current_context
  if ctx is None:
    ctx = make_default_context()
    set_context(ctx)
  return ctx


def make_default_context():

  datastore_app_id = os.environ.get(_DATASTORE_APP_ID_ENV, None)
  datastore_project_id = os.environ.get(_DATASTORE_PROJECT_ID_ENV, None)
  if datastore_app_id or datastore_project_id:

    app_id_override = bool(os.environ.get(
        _DATASTORE_USE_PROJECT_ID_AS_APP_ID_ENV, False))
    if not datastore_app_id and not app_id_override:
      raise ValueError('Could not determine app id. To use project id (%s) '
                       'instead, set %s=true. This will affect the '
                       'serialized form of entities and should not be used '
                       'if serialized entities will be shared between '
                       'code running on App Engine and code running off '
                       'App Engine. Alternatively, set %s=<app id>.'
                       % (datastore_project_id,
                          _DATASTORE_USE_PROJECT_ID_AS_APP_ID_ENV,
                          _DATASTORE_APP_ID_ENV))
    elif datastore_app_id:
      if app_id_override:
        raise ValueError('App id was provided (%s) but %s was set to true. '
                         'Please unset either %s or %s.' %
                         (datastore_app_id,
                          _DATASTORE_USE_PROJECT_ID_AS_APP_ID_ENV,
                          _DATASTORE_APP_ID_ENV,
                          _DATASTORE_USE_PROJECT_ID_AS_APP_ID_ENV))
      elif datastore_project_id:

        id_resolver = datastore_pbs.IdResolver([datastore_app_id])
        if (datastore_project_id !=
            id_resolver.resolve_project_id(datastore_app_id)):
          raise ValueError('App id "%s" does not match project id "%s".'
                           % (datastore_app_id, datastore_project_id))

    datastore_app_id = datastore_project_id or datastore_app_id
    additional_app_str = os.environ.get(_DATASTORE_ADDITIONAL_APP_IDS_ENV, '')
    additional_apps = (app.strip() for app in additional_app_str.split(','))
    return _make_cloud_datastore_context(datastore_app_id, additional_apps)
  return make_context()


@utils.positional(0)
def make_context(conn=None, config=None):

  from google.appengine.ext.ndb import context
  return context.Context(conn=conn, config=config)


def _make_cloud_datastore_context(app_id, external_app_ids=()):
  """Creates a new context to connect to a remote Cloud Datastore instance.

  This should only be used outside of Google App Engine.

  Args:
    app_id: The application id to connect to. This differs from the project
      id as it may have an additional prefix, e.g. "s~" or "e~".
    external_app_ids: A list of apps that may be referenced by data in your
      application. For example, if you are connected to s~my-app and store keys
      for s~my-other-app, you should include s~my-other-app in the external_apps
      list.
  Returns:
    An ndb.Context that can connect to a Remote Cloud Datastore. You can use
    this context by passing it to ndb.set_context.
  """
  from google.appengine.ext.ndb import model

  if not datastore_pbs._CLOUD_DATASTORE_ENABLED:
    raise datastore_errors.BadArgumentError(
        datastore_pbs.MISSING_CLOUD_DATASTORE_MESSAGE)
  import googledatastore
  from google.appengine.datastore import cloud_datastore_v1_remote_stub

  current_app_id = full_app_id.get()
  if current_app_id and current_app_id != app_id:


    raise ValueError('Cannot create a Cloud Datastore context that connects '
                     'to an application (%s) that differs from the application '
                     'already connected to (%s).' % (app_id, current_app_id))
  full_app_id.put(app_id)

  id_resolver = datastore_pbs.IdResolver((app_id,) + tuple(external_app_ids))
  project_id = id_resolver.resolve_project_id(app_id)
  endpoint = googledatastore.helper.get_project_endpoint_from_env(project_id)
  datastore = googledatastore.Datastore(
      project_endpoint=endpoint,
      credentials=googledatastore.helper.get_credentials_from_env())

  conn = model.make_connection(_api_version=datastore_rpc._CLOUD_DATASTORE_V1,
                               _id_resolver=id_resolver)


  try:
    stub = cloud_datastore_v1_remote_stub.CloudDatastoreV1RemoteStub(datastore)
    apiproxy_stub_map.apiproxy.RegisterStub(datastore_rpc._CLOUD_DATASTORE_V1,
                                            stub)
  except:
    pass



  try:
    apiproxy_stub_map.apiproxy.RegisterStub('memcache', _ThrowingStub())
  except:
    pass
  try:
    apiproxy_stub_map.apiproxy.RegisterStub('taskqueue', _ThrowingStub())
  except:
    pass


  return make_context(conn=conn)


def set_context(new_context):

  os.environ[_CONTEXT_KEY] = '1'
  _state.set_context(new_context)


class _ThrowingStub(apiproxy_stub.APIProxyStub):
  """A Stub implementation which always throws a NotImplementedError."""

  def __init__(self):
    pass


  def MakeSyncCall(self, service, call, request, response):
    raise NotImplementedError('In order to use %s.%s you must '
                              'install the Remote API.' % (service, call))


  def CreateRPC(self):
    return apiproxy_rpc.RPC(stub=self)






























































