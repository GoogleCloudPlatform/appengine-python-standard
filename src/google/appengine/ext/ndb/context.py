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














"""Context class."""

import logging
import sys

from google.appengine.ext.ndb import eventloop
from google.appengine.ext.ndb import key as key_module
from google.appengine.ext.ndb import model
from google.appengine.ext.ndb import tasklets
from google.appengine.ext.ndb import utils
import six
from six.moves import range
from six.moves import zip

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import memcache
from google.appengine.api import namespace_manager
from google.appengine.api import urlfetch
from google.appengine.datastore import datastore_rpc
from google.protobuf import message
from google.appengine.datastore import entity_bytes_pb2 as entity_pb2

__all__ = ['Context', 'ContextOptions', 'TransactionOptions', 'AutoBatcher',
           'EVENTUAL_CONSISTENCY',
          ]

_LOCK_TIME = 32
_LOCKED = 0



EVENTUAL_CONSISTENCY = datastore_rpc.Configuration.EVENTUAL_CONSISTENCY


class ContextOptions(datastore_rpc.Configuration):
  """Configuration options that may be passed along with get/put/delete."""

  @datastore_rpc.ConfigOption
  def use_cache(value):
    if not isinstance(value, bool):
      raise datastore_errors.BadArgumentError(
          'use_cache should be a bool (%r)' % (value,))
    return value

  @datastore_rpc.ConfigOption
  def use_memcache(value):
    if not isinstance(value, bool):
      raise datastore_errors.BadArgumentError(
          'use_memcache should be a bool (%r)' % (value,))
    return value

  @datastore_rpc.ConfigOption
  def use_datastore(value):
    if not isinstance(value, bool):
      raise datastore_errors.BadArgumentError(
          'use_datastore should be a bool (%r)' % (value,))
    return value

  @datastore_rpc.ConfigOption
  def memcache_timeout(value):
    if not isinstance(value, six.integer_types):
      raise datastore_errors.BadArgumentError(
          'memcache_timeout should be an integer (%r)' % (value,))
    return value

  @datastore_rpc.ConfigOption
  def max_memcache_items(value):
    if not isinstance(value, six.integer_types):
      raise datastore_errors.BadArgumentError(
          'max_memcache_items should be an integer (%r)' % (value,))
    return value

  @datastore_rpc.ConfigOption
  def memcache_deadline(value):
    if not isinstance(value, six.integer_types):
      raise datastore_errors.BadArgumentError(
          'memcache_deadline should be an integer (%r)' % (value,))
    return value


class TransactionOptions(ContextOptions, datastore_rpc.TransactionOptions):
  """Support both context options and transaction options."""



_OPTION_TRANSLATIONS = {
    'options': 'config',
}


def _make_ctx_options(ctx_options, config_cls=ContextOptions):
  """Helper to construct a ContextOptions object from keyword arguments.

  Args:
    ctx_options: A dict of keyword arguments.
    config_cls: Optional Configuration class to use, default ContextOptions.

  Note that either 'options' or 'config' can be used to pass another
  Configuration object, but not both.  If another Configuration
  object is given it provides default values.

  Returns:
    A Configuration object, or None if ctx_options is empty.
  """
  if not ctx_options:
    return None
  for key in list(ctx_options):
    translation = _OPTION_TRANSLATIONS.get(key)
    if translation:
      if translation in ctx_options:
        raise ValueError('Cannot specify %s and %s at the same time' %
                         (key, translation))
      ctx_options[translation] = ctx_options.pop(key)
  return config_cls(**ctx_options)


class AutoBatcher(object):
  """Batches multiple async calls if they share the same rpc options.

  Here is an example to explain what this class does.

  Life of a key.get_async(options) API call:
  *) Key gets the singleton Context instance and invokes Context.get.
  *) Context.get calls Context._get_batcher.add(key, options). This
     returns a future "fut" as the return value of key.get_async.
     At this moment, key.get_async returns.

  *) When more than "limit" number of _get_batcher.add() was called,
     _get_batcher invokes its self._todo_tasklet, Context._get_tasklet,
     with the list of keys seen so far.
  *) Context._get_tasklet fires a MultiRPC and waits on it.
  *) Upon MultiRPC completion, Context._get_tasklet passes on the results
     to the respective "fut" from key.get_async.

  *) If user calls "fut".get_result() before "limit" number of add() was called,
     "fut".get_result() will repeatedly call eventloop.run1().
  *) After processing immediate callbacks, eventloop will run idlers.
     AutoBatcher._on_idle is an idler.
  *) _on_idle will run the "todo_tasklet" before the batch is full.

  So the engine is todo_tasklet, which is a proxy tasklet that can combine
  arguments into batches and passes along results back to respective futures.
  This class is mainly a helper that invokes todo_tasklet with the right
  arguments at the right time.
  """

  def __init__(self, todo_tasklet, limit):
    """Init.

    Args:
      todo_tasklet: the tasklet that actually fires RPC and waits on a MultiRPC.
        It should take a list of (future, arg) pairs and an "options" as
        arguments. "options" are rpc options.
      limit: max number of items to batch for each distinct value of "options".
    """
    self._todo_tasklet = todo_tasklet
    self._limit = limit


    self._queues = {}
    self._running = []
    self._cache = {}

  def __repr__(self):
    return '%s(%s)' % (self.__class__.__name__, self._todo_tasklet.__name__)

  def run_queue(self, options, todo):
    """Actually run the _todo_tasklet."""
    utils.logging_debug('AutoBatcher(%s): %d items',
                        self._todo_tasklet.__name__, len(todo))
    batch_fut = self._todo_tasklet(todo, options)
    self._running.append(batch_fut)

    batch_fut.add_callback(self._finished_callback, batch_fut, todo)

  def _on_idle(self):
    """An idler eventloop can run.

    Eventloop calls this when it has finished processing all immediate
    callbacks. This method runs _todo_tasklet even before the batch is full.
    """
    if not self.action():
      return None
    return True

  def add(self, arg, options=None):
    """Adds an arg and gets back a future.

    Args:
      arg: one argument for _todo_tasklet.
      options: rpc options.

    Return:
      An instance of future, representing the result of running
        _todo_tasklet without batching.
    """
    fut = tasklets.Future('%s.add(%s, %s)' % (self, arg, options))
    todo = self._queues.get(options)
    if todo is None:
      utils.logging_debug('AutoBatcher(%s): creating new queue for %r',
                          self._todo_tasklet.__name__, options)
      if not self._queues:
        eventloop.add_idle(self._on_idle)
      todo = self._queues[options] = []
    todo.append((fut, arg))
    if len(todo) >= self._limit:
      del self._queues[options]
      self.run_queue(options, todo)
    return fut

  def add_once(self, arg, options=None):
    cache_key = (arg, options)
    fut = self._cache.get(cache_key)
    if fut is None:
      fut = self.add(arg, options)
      self._cache[cache_key] = fut
      fut.add_immediate_callback(self._cache.__delitem__, cache_key)
    return fut

  def action(self):
    queues = self._queues
    if not queues:
      return False
    options, todo = queues.popitem()
    self.run_queue(options, todo)
    return True

  def _finished_callback(self, batch_fut, todo):
    """Passes exception along.

    Args:
      batch_fut: the batch future returned by running todo_tasklet.
      todo: (fut, option) pair. fut is the future return by each add() call.

    If the batch fut was successful, it has already called fut.set_result()
    on other individual futs. This method only handles when the batch fut
    encountered an exception.
    """
    self._running.remove(batch_fut)
    err = batch_fut.get_exception()
    if err is not None:
      tb = batch_fut.get_traceback()
      for (fut, _) in todo:
        if not fut.done():
          fut.set_exception(err, tb)

  @tasklets.tasklet
  def flush(self):
    while self._running or self.action():
      if self._running:
        yield self._running


class Context(object):

  def __init__(self, conn=None, auto_batcher_class=AutoBatcher, config=None,
               parent_context=None):


    if conn is None:
      conn = model.make_connection(config)
    self._conn = conn
    self._auto_batcher_class = auto_batcher_class
    self._parent_context = parent_context



    max_get = (datastore_rpc.Configuration.max_get_keys(config, conn.config) or
               datastore_rpc.Connection.MAX_GET_KEYS)
    max_put = (datastore_rpc.Configuration.max_put_entities(config,
                                                            conn.config) or
               datastore_rpc.Connection.MAX_PUT_ENTITIES)
    max_delete = (datastore_rpc.Configuration.max_delete_keys(config,
                                                              conn.config) or
                  datastore_rpc.Connection.MAX_DELETE_KEYS)

    self._get_batcher = auto_batcher_class(self._get_tasklet, max_get)
    self._put_batcher = auto_batcher_class(self._put_tasklet, max_put)
    self._delete_batcher = auto_batcher_class(self._delete_tasklet, max_delete)

    max_memcache = (ContextOptions.max_memcache_items(config, conn.config) or
                    datastore_rpc.Connection.MAX_GET_KEYS)

    self._memcache_get_batcher = auto_batcher_class(self._memcache_get_tasklet,
                                                    max_memcache)
    self._memcache_set_batcher = auto_batcher_class(self._memcache_set_tasklet,
                                                    max_memcache)
    self._memcache_del_batcher = auto_batcher_class(self._memcache_del_tasklet,
                                                    max_memcache)
    self._memcache_off_batcher = auto_batcher_class(self._memcache_off_tasklet,
                                                    max_memcache)

    self._batchers = [self._get_batcher,
                      self._put_batcher,
                      self._delete_batcher,
                      self._memcache_get_batcher,
                      self._memcache_set_batcher,
                      self._memcache_del_batcher,
                      self._memcache_off_batcher,
                     ]
    self._cache = {}
    self._memcache = memcache.Client()
    self._on_commit_queue = []



  _memcache_prefix = b'NDB9:'

  @tasklets.tasklet
  def flush(self):

    more = True
    while more:
      yield [batcher.flush() for batcher in self._batchers]
      more = False
      for batcher in self._batchers:
        if batcher._running or batcher._queues:
          more = True
          break

  @tasklets.tasklet
  def _get_tasklet(self, todo, options):
    if not todo:
      raise RuntimeError('Nothing to do.')

    datastore_keys = []
    for unused_fut, key in todo:
      datastore_keys.append(key)

    entities = yield self._conn.async_get(options, datastore_keys)
    for ent, (fut, unused_key) in zip(entities, todo):
      fut.set_result(ent)

  @tasklets.tasklet
  def _put_tasklet(self, todo, options):
    if not todo:
      raise RuntimeError('Nothing to do.')


    datastore_entities = []
    for unused_fut, ent in todo:
      datastore_entities.append(ent)

    keys = yield self._conn.async_put(options, datastore_entities)
    for key, (fut, ent) in zip(keys, todo):
      if key != ent._key:
        if ent._has_complete_key():
          ent_key = ent._key
          raise datastore_errors.BadKeyError(
              'Entity Key differs from the one returned by Datastore. '
              'Returned Key: %r, Entity Key: %r' % (key, ent_key))
        ent._key = key
      fut.set_result(key)

  @tasklets.tasklet
  def _delete_tasklet(self, todo, options):
    if not todo:
      raise RuntimeError('Nothing to do.')
    futures = []
    datastore_keys = []
    for fut, key in todo:
      futures.append(fut)
      datastore_keys.append(key)

    yield self._conn.async_delete(options, datastore_keys)

    for fut in futures:
      fut.set_result(None)












  @staticmethod
  def default_cache_policy(key):
    """Default cache policy.

    This defers to _use_cache on the Model class.

    Args:
      key: Key instance.

    Returns:
      A bool or None.
    """
    flag = None
    if key is not None:
      modelclass = model.Model._kind_map.get(key.kind())
      if modelclass is not None:
        policy = getattr(modelclass, '_use_cache', None)
        if policy is not None:
          if isinstance(policy, bool):
            flag = policy
          else:
            flag = policy(key)
    return flag

  _cache_policy = default_cache_policy

  def get_cache_policy(self):
    """Return the current context cache policy function.

    Returns:
      A function that accepts a Key instance as argument and returns
      a bool indicating if it should be cached.  May be None.
    """
    return self._cache_policy

  def set_cache_policy(self, func):
    """Set the context cache policy function.

    Args:
      func: A function that accepts a Key instance as argument and returns
        a bool indicating if it should be cached.  May be None.
    """
    if func is None:
      func = self.default_cache_policy
    elif isinstance(func, bool):
      func = lambda unused_key, flag=func: flag
    self._cache_policy = func

  def _use_cache(self, key, options=None):
    """Return whether to use the context cache for this key.

    Args:
      key: Key instance.
      options: ContextOptions instance, or None.

    Returns:
      True if the key should be cached, False otherwise.
    """
    flag = ContextOptions.use_cache(options)
    if flag is None:
      flag = self._cache_policy(key)
    if flag is None:
      flag = ContextOptions.use_cache(self._conn.config)
    if flag is None:
      flag = True
    return flag

  @staticmethod
  def default_memcache_policy(key):
    """Default memcache policy.

    This defers to _use_memcache on the Model class.

    Args:
      key: Key instance.

    Returns:
      A bool or None.
    """
    flag = None
    if key is not None:
      modelclass = model.Model._kind_map.get(key.kind())
      if modelclass is not None:
        policy = getattr(modelclass, '_use_memcache', None)
        if policy is not None:
          if isinstance(policy, bool):
            flag = policy
          else:
            flag = policy(key)
    return flag

  _memcache_policy = default_memcache_policy

  def get_memcache_policy(self):
    """Return the current memcache policy function.

    Returns:
      A function that accepts a Key instance as argument and returns
      a bool indicating if it should be cached.  May be None.
    """
    return self._memcache_policy

  def set_memcache_policy(self, func):
    """Set the memcache policy function.

    Args:
      func: A function that accepts a Key instance as argument and returns
        a bool indicating if it should be cached.  May be None.
    """
    if func is None:
      func = self.default_memcache_policy
    elif isinstance(func, bool):
      func = lambda unused_key, flag=func: flag
    self._memcache_policy = func

  def _use_memcache(self, key, options=None):
    """Return whether to use memcache for this key.

    Args:
      key: Key instance.
      options: ContextOptions instance, or None.

    Returns:
      True if the key should be cached in memcache, False otherwise.
    """
    flag = ContextOptions.use_memcache(options)
    if flag is None:
      flag = self._memcache_policy(key)
    if flag is None:
      flag = ContextOptions.use_memcache(self._conn.config)
    if flag is None:
      flag = True
    return flag

  @staticmethod
  def default_datastore_policy(key):
    """Default datastore policy.

    This defers to _use_datastore on the Model class.

    Args:
      key: Key instance.

    Returns:
      A bool or None.
    """
    flag = None
    if key is not None:
      modelclass = model.Model._kind_map.get(key.kind())
      if modelclass is not None:
        policy = getattr(modelclass, '_use_datastore', None)
        if policy is not None:
          if isinstance(policy, bool):
            flag = policy
          else:
            flag = policy(key)
    return flag

  _datastore_policy = default_datastore_policy

  def get_datastore_policy(self):
    """Return the current context datastore policy function.

    Returns:
      A function that accepts a Key instance as argument and returns
      a bool indicating if it should use the datastore.  May be None.
    """
    return self._datastore_policy

  def set_datastore_policy(self, func):
    """Set the context datastore policy function.

    Args:
      func: A function that accepts a Key instance as argument and returns
        a bool indicating if it should use the datastore.  May be None.
    """
    if func is None:
      func = self.default_datastore_policy
    elif isinstance(func, bool):
      func = lambda unused_key, flag=func: flag
    self._datastore_policy = func

  def _use_datastore(self, key, options=None):
    """Return whether to use the datastore for this key.

    Args:
      key: Key instance.
      options: ContextOptions instance, or None.

    Returns:
      True if the datastore should be used, False otherwise.
    """
    flag = ContextOptions.use_datastore(options)
    if flag is None:
      flag = self._datastore_policy(key)
    if flag is None:
      flag = ContextOptions.use_datastore(self._conn.config)
    if flag is None:
      flag = True
    return flag

  @staticmethod
  def default_memcache_timeout_policy(key):
    """Default memcache timeout policy.

    This defers to _memcache_timeout on the Model class.

    Args:
      key: Key instance.

    Returns:
      Memcache timeout to use (integer), or None.
    """
    timeout = None
    if key is not None and isinstance(key, model.Key):
      modelclass = model.Model._kind_map.get(key.kind())
      if modelclass is not None:
        policy = getattr(modelclass, '_memcache_timeout', None)
        if policy is not None:
          if isinstance(policy, six.integer_types):
            timeout = policy
          else:
            timeout = policy(key)
    return timeout

  _memcache_timeout_policy = default_memcache_timeout_policy

  def set_memcache_timeout_policy(self, func):
    """Set the policy function for memcache timeout (expiration).

    Args:
      func: A function that accepts a key instance as argument and returns
        an integer indicating the desired memcache timeout.  May be None.

    If the function returns 0 it implies the default timeout.
    """
    if func is None:
      func = self.default_memcache_timeout_policy
    elif isinstance(func, six.integer_types):
      func = lambda unused_key, flag=func: flag
    self._memcache_timeout_policy = func

  def get_memcache_timeout_policy(self):
    """Return the current policy function for memcache timeout (expiration)."""
    return self._memcache_timeout_policy

  def _get_memcache_timeout(self, key, options=None):
    """Return the memcache timeout (expiration) for this key."""
    timeout = ContextOptions.memcache_timeout(options)
    if timeout is None:
      timeout = self._memcache_timeout_policy(key)
    if timeout is None:
      timeout = ContextOptions.memcache_timeout(self._conn.config)
    if timeout is None:
      timeout = 0
    return timeout

  def _get_memcache_deadline(self, options=None):
    """Return the memcache RPC deadline.

    Not to be confused with the memcache timeout, or expiration.

    This is only used by datastore operations when using memcache
    as a cache; it is ignored by the direct memcache calls.

    There is no way to vary this per key or per entity; you must either
    set it on a specific call (e.g. key.get(memcache_deadline=1) or
    in the configuration options of the context's connection.
    """

    return ContextOptions.memcache_deadline(options, self._conn.config)

  def _load_from_cache_if_available(self, key):
    """Returns a cached Model instance given the entity key if available.

    Args:
      key: Key instance.

    Returns:
      A Model instance if the key exists in the cache.
    """
    if key in self._cache:
      entity = self._cache[key]
      if entity is None or entity._key == key:


        raise tasklets.Return(entity)








  @tasklets.tasklet
  def get(self, key, **ctx_options):
    """Return a Model instance given the entity key.

    It will use the context cache if the cache policy for the given
    key is enabled.

    Args:
      key: Key instance.
      **ctx_options: Context options.

    Returns:
      A Model instance if the key exists in the datastore; None otherwise.
    """
    options = _make_ctx_options(ctx_options)
    use_cache = self._use_cache(key, options)
    if use_cache:
      self._load_from_cache_if_available(key)

    use_datastore = self._use_datastore(key, options)
    if (use_datastore and
        isinstance(self._conn, datastore_rpc.TransactionalConnection)):
      use_memcache = False
    else:
      use_memcache = self._use_memcache(key, options)
    ns = key.namespace()
    memcache_deadline = None

    if use_memcache:
      mkey = self._memcache_prefix + key.urlsafe()
      memcache_deadline = self._get_memcache_deadline(options)
      mvalue = yield self.memcache_get(mkey, for_cas=use_datastore,
                                       namespace=ns, use_cache=True,
                                       deadline=memcache_deadline)

      if use_cache:
        self._load_from_cache_if_available(key)
      if mvalue not in (_LOCKED, None):
        cls = model.Model._lookup_model(key.kind(),
                                        self._conn.adapter.default_model)
        pb = entity_pb2.EntityProto()

        try:
          pb.MergeFromString(mvalue)
        except message.DecodeError:
          logging.warning('Corrupt memcache entry found '
                          'with key %s and namespace %s', mkey, ns)
          mvalue = None
        else:
          entity = cls._from_pb(pb)

          entity._key = key
          if use_cache:

            self._cache[key] = entity
          raise tasklets.Return(entity)

      if mvalue is None and use_datastore:
        yield self.memcache_set(mkey, _LOCKED, time=_LOCK_TIME, namespace=ns,
                                use_cache=True, deadline=memcache_deadline)
        yield self.memcache_gets(mkey, namespace=ns, use_cache=True,
                                 deadline=memcache_deadline)

    if not use_datastore:


      raise tasklets.Return(None)

    if use_cache:
      entity = yield self._get_batcher.add_once(key, options)
    else:
      entity = yield self._get_batcher.add(key, options)

    if entity is not None:
      if use_memcache and mvalue != _LOCKED:

        pbs = entity._to_pb(set_key=False).SerializePartialToString()





        if len(pbs) <= memcache.MAX_VALUE_SIZE:
          timeout = self._get_memcache_timeout(key, options)




          yield self.memcache_cas(mkey, pbs, time=timeout, namespace=ns,
                                  deadline=memcache_deadline)

    if use_cache:


      self._cache[key] = entity

    raise tasklets.Return(entity)

  @tasklets.tasklet
  def put(self, entity, **ctx_options):
    options = _make_ctx_options(ctx_options)


    key = entity._key
    if key is None:

      key = model.Key(entity.__class__, None)
    use_datastore = self._use_datastore(key, options)
    use_memcache = None
    memcache_deadline = None

    if entity._has_complete_key():
      use_memcache = self._use_memcache(key, options)
      if use_memcache:

        memcache_deadline = self._get_memcache_deadline(options)
        mkey = self._memcache_prefix + key.urlsafe()
        ns = key.namespace()
        if use_datastore:
          yield self.memcache_set(mkey, _LOCKED, time=_LOCK_TIME,
                                  namespace=ns, use_cache=True,
                                  deadline=memcache_deadline)
        else:
          pbs = entity._to_pb(set_key=False).SerializePartialToString()


          if len(pbs) > memcache.MAX_VALUE_SIZE:
            raise ValueError('Values may not be more than %d bytes in length; '
                             'received %d bytes' % (memcache.MAX_VALUE_SIZE,
                                                    len(pbs)))
          timeout = self._get_memcache_timeout(key, options)
          yield self.memcache_set(mkey, pbs, time=timeout, namespace=ns,
                                  deadline=memcache_deadline)

    if use_datastore:
      key = yield self._put_batcher.add(entity, options)
      if not isinstance(self._conn, datastore_rpc.TransactionalConnection):
        if use_memcache is None:
          use_memcache = self._use_memcache(key, options)
        if use_memcache:
          mkey = self._memcache_prefix + key.urlsafe()
          ns = key.namespace()

          yield self.memcache_delete(mkey, namespace=ns,
                                     deadline=memcache_deadline)

    if key is not None:
      if entity._key != key:
        logging.info('replacing key %s with %s', entity._key, key)
        entity._key = key

      if self._use_cache(key, options):

        self._cache[key] = entity

    raise tasklets.Return(key)

  @tasklets.tasklet
  def delete(self, key, **ctx_options):
    options = _make_ctx_options(ctx_options)
    if self._use_memcache(key, options):
      memcache_deadline = self._get_memcache_deadline(options)
      mkey = self._memcache_prefix + key.urlsafe()
      ns = key.namespace()

      yield self.memcache_set(mkey, _LOCKED, time=_LOCK_TIME, namespace=ns,
                              use_cache=True, deadline=memcache_deadline)

    if self._use_datastore(key, options):
      yield self._delete_batcher.add(key, options)


    if self._use_cache(key, options):
      self._cache[key] = None

  @tasklets.tasklet
  def allocate_ids(self, key, size=None, max=None, **ctx_options):
    options = _make_ctx_options(ctx_options)
    lo_hi = yield self._conn.async_allocate_ids(options, key, size, max)
    raise tasklets.Return(lo_hi)

  @tasklets.tasklet
  def get_indexes(self, **ctx_options):
    options = _make_ctx_options(ctx_options)
    index_list = yield self._conn.async_get_indexes(options)
    raise tasklets.Return(index_list)

  @utils.positional(3)
  def map_query(self, query, callback, pass_batch_into_callback=None,
                options=None, merge_future=None):
    mfut = merge_future
    if mfut is None:
      mfut = tasklets.MultiFuture('map_query')

    @tasklets.tasklet
    def helper():
      try:
        inq = tasklets.SerialQueueFuture()
        query.run_to_queue(inq, self._conn, options)
        while True:
          try:
            batch, i, ent = yield inq.getq()
          except EOFError:
            break
          ent = self._update_cache_from_query_result(ent, options)
          if ent is None:
            continue
          if callback is None:
            val = ent
          else:

            if pass_batch_into_callback:
              val = callback(batch, i, ent)
            else:
              val = callback(ent)
          mfut.putq(val)
      except GeneratorExit:
        raise
      except Exception as err:
        _, _, tb = sys.exc_info()
        mfut.set_exception(err, tb)
        raise
      else:
        mfut.complete()

    helper()
    return mfut

  def _update_cache_from_query_result(self, ent, options):
    if isinstance(ent, model.Key):
      return ent
    if ent._projection:
      return ent
    key = ent._key
    if not self._use_cache(key, options):
      return ent



    if key in self._cache:
      cached_ent = self._cache[key]
      if (cached_ent is None or
          cached_ent.key == key and cached_ent.__class__ is ent.__class__):
        return cached_ent


    self._cache[key] = ent
    return ent

  @utils.positional(2)
  def iter_query(self, query, callback=None, pass_batch_into_callback=None,
                 options=None):
    return self.map_query(query, callback=callback, options=options,
                          pass_batch_into_callback=pass_batch_into_callback,
                          merge_future=tasklets.SerialQueueFuture())

  @tasklets.tasklet
  def transaction(self, callback, **ctx_options):



    options = _make_ctx_options(ctx_options, TransactionOptions)
    propagation = TransactionOptions.propagation(options)
    if propagation is None:
      propagation = TransactionOptions.NESTED

    mode = datastore_rpc.TransactionMode.READ_WRITE
    if ctx_options.get('read_only', False):
      mode = datastore_rpc.TransactionMode.READ_ONLY

    parent = self
    if propagation == TransactionOptions.NESTED:
      if self.in_transaction():
        raise datastore_errors.BadRequestError(
            'Nested transactions are not supported.')
    elif propagation == TransactionOptions.MANDATORY:
      if not self.in_transaction():
        raise datastore_errors.BadRequestError(
            'Requires an existing transaction.')
      result = callback()
      if isinstance(result, tasklets.Future):
        result = yield result
      raise tasklets.Return(result)
    elif propagation == TransactionOptions.ALLOWED:
      if self.in_transaction():
        result = callback()
        if isinstance(result, tasklets.Future):
          result = yield result
        raise tasklets.Return(result)
    elif propagation == TransactionOptions.INDEPENDENT:
      while parent.in_transaction():
        parent = parent._parent_context
        if parent is None:
          raise datastore_errors.BadRequestError(
              'Context without non-transactional ancestor')
    else:
      raise datastore_errors.BadArgumentError(
          'Invalid propagation value (%s).' % (propagation,))

    app = TransactionOptions.app(options) or key_module._DefaultAppId()

    retries = TransactionOptions.retries(options)
    if retries is None:
      retries = 3
    yield parent.flush()

    transaction = None
    tconn = None
    for _ in range(1 + max(0, retries)):
      previous_transaction = (
          transaction
          if mode == datastore_rpc.TransactionMode.READ_WRITE else None)
      transaction = yield (parent._conn.async_begin_transaction(
          options, app,
          previous_transaction,
          mode))
      tconn = datastore_rpc.TransactionalConnection(
          adapter=parent._conn.adapter,
          config=parent._conn.config,
          transaction=transaction,
          _api_version=parent._conn._api_version)
      tctx = parent.__class__(conn=tconn,
                              auto_batcher_class=parent._auto_batcher_class,
                              parent_context=parent)
      tctx._old_ds_conn = datastore._GetConnection()
      ok = False
      try:





        tctx.set_memcache_policy(parent.get_memcache_policy())
        tctx.set_memcache_timeout_policy(parent.get_memcache_timeout_policy())
        tasklets.set_context(tctx)
        datastore._SetConnection(tconn)
        try:
          try:
            result = callback()
            if isinstance(result, tasklets.Future):
              result = yield result
          finally:
            yield tctx.flush()
        except GeneratorExit:
          raise
        except Exception:
          t, e, tb = sys.exc_info()
          tconn.async_rollback(options)
          if issubclass(t, datastore_errors.Rollback):

            return
          else:
            six.reraise(t, e, tb)
        else:
          ok = yield tconn.async_commit(options)
          if ok:
            parent._cache.update(tctx._cache)
            yield parent._clear_memcache(tctx._cache)
            raise tasklets.Return(result)

      finally:
        datastore._SetConnection(tctx._old_ds_conn)
        del tctx._old_ds_conn
        if ok:





          for on_commit_callback in tctx._on_commit_queue:
            on_commit_callback()


    tconn.async_rollback(options)
    raise datastore_errors.TransactionFailedError(
        'The transaction could not be committed. Please try again.')

  def in_transaction(self):
    """Return whether a transaction is currently active."""
    return isinstance(self._conn, datastore_rpc.TransactionalConnection)

  def call_on_commit(self, callback):
    """Call a callback upon successful commit of a transaction.

    If not in a transaction, the callback is called immediately.

    In a transaction, multiple callbacks may be registered and will be
    called once the transaction commits, in the order in which they
    were registered.  If the transaction fails, the callbacks will not
    be called.

    If the callback raises an exception, it bubbles up normally.  This
    means: If the callback is called immediately, any exception it
    raises will bubble up immediately.  If the call is postponed until
    commit, remaining callbacks will be skipped and the exception will
    bubble up through the transaction() call.  (However, the
    transaction is already committed at that point.)
    """
    if not self.in_transaction():
      callback()
    else:
      self._on_commit_queue.append(callback)

  def clear_cache(self):
    """Clears the in-memory cache.

    NOTE: This does not affect memcache.
    """
    self._cache.clear()

  @tasklets.tasklet
  def _clear_memcache(self, keys):
    keys = set(key for key in keys if self._use_memcache(key))
    futures = []
    for key in keys:
      mkey = self._memcache_prefix + key.urlsafe()
      ns = key.namespace()
      fut = self.memcache_delete(mkey, namespace=ns)
      futures.append(fut)
    yield futures

  @tasklets.tasklet
  def _memcache_get_tasklet(self, todo, options):
    if not todo:
      raise RuntimeError('Nothing to do.')
    for_cas, namespace, deadline = options
    keys = set()
    for unused_fut, key in todo:
      keys.add(key)
    rpc = memcache.create_rpc(deadline=deadline)
    results = yield self._memcache.get_multi_async(keys, for_cas=for_cas,
                                                   namespace=namespace,
                                                   rpc=rpc)
    for fut, key in todo:
      fut.set_result(results.get(key))

  @tasklets.tasklet
  def _memcache_set_tasklet(self, todo, options):
    if not todo:
      raise RuntimeError('Nothing to do.')
    opname, time, namespace, deadline = options
    methodname = opname + '_multi_async'
    method = getattr(self._memcache, methodname)
    mapping = {}
    for unused_fut, (key, value) in todo:
      mapping[key] = value
    rpc = memcache.create_rpc(deadline=deadline)
    results = yield method(mapping, time=time, namespace=namespace, rpc=rpc)
    for fut, (key, unused_value) in todo:
      if results is None:
        status = memcache.MemcacheSetResponse.ERROR
      else:
        status = results.get(key)
      fut.set_result(status == memcache.MemcacheSetResponse.STORED)

  @tasklets.tasklet
  def _memcache_del_tasklet(self, todo, options):
    if not todo:
      raise RuntimeError('Nothing to do.')
    seconds, namespace, deadline = options
    keys = set()
    for unused_fut, key in todo:
      keys.add(key)
    rpc = memcache.create_rpc(deadline=deadline)
    statuses = yield self._memcache.delete_multi_async(keys, seconds=seconds,
                                                       namespace=namespace,
                                                       rpc=rpc)
    status_key_mapping = {}
    if statuses:
      for key, status in zip(keys, statuses):
        status_key_mapping[key] = status
    for fut, key in todo:
      status = status_key_mapping.get(key, memcache.DELETE_NETWORK_FAILURE)
      fut.set_result(status)

  @tasklets.tasklet
  def _memcache_off_tasklet(self, todo, options):
    if not todo:
      raise RuntimeError('Nothing to do.')
    initial_value, namespace, deadline = options
    mapping = {}
    for unused_fut, (key, delta) in todo:
      mapping[key] = delta
    rpc = memcache.create_rpc(deadline=deadline)
    results = yield self._memcache.offset_multi_async(
        mapping, initial_value=initial_value, namespace=namespace, rpc=rpc)
    for fut, (key, unused_delta) in todo:
      fut.set_result(results.get(key))

  def memcache_get(self, key, for_cas=False, namespace=None, use_cache=False,
                   deadline=None):
    """An auto-batching wrapper for memcache.get() or .get_multi().

    Args:
      key: Key to set.  This must be a string; no prefix is applied.
      for_cas: If True, request and store CAS ids on the Context.
      namespace: Optional namespace.
      deadline: Optional deadline for the RPC.

    Returns:
      A Future (!) whose return value is the value retrieved from
      memcache, or None.
    """
    if not isinstance(key, (six.text_type, six.binary_type)):
      raise TypeError('key must be a string; received %r' % key)
    if not isinstance(for_cas, bool):
      raise TypeError('for_cas must be a bool; received %r' % for_cas)
    if namespace is None:
      namespace = namespace_manager.get_namespace()
    options = (for_cas, namespace, deadline)
    batcher = self._memcache_get_batcher
    if use_cache:
      return batcher.add_once(key, options)
    else:
      return batcher.add(key, options)



  def memcache_gets(self, key, namespace=None, use_cache=False, deadline=None):
    return self.memcache_get(key, for_cas=True, namespace=namespace,
                             use_cache=use_cache, deadline=deadline)

  def memcache_set(self, key, value, time=0, namespace=None, use_cache=False,
                   deadline=None):
    if not isinstance(key, (six.text_type, six.binary_type)):
      raise TypeError('key must be a string; received %r' % key)
    if not isinstance(time, six.integer_types):
      raise TypeError('time must be a number; received %r' % time)
    if namespace is None:
      namespace = namespace_manager.get_namespace()
    options = ('set', time, namespace, deadline)
    batcher = self._memcache_set_batcher
    if use_cache:
      return batcher.add_once((key, value), options)
    else:
      return batcher.add((key, value), options)

  def memcache_add(self, key, value, time=0, namespace=None, deadline=None):
    if not isinstance(key, (six.text_type, six.binary_type)):
      raise TypeError('key must be a string; received %r' % key)
    if not isinstance(time, six.integer_types):
      raise TypeError('time must be a number; received %r' % time)
    if namespace is None:
      namespace = namespace_manager.get_namespace()
    return self._memcache_set_batcher.add((key, value),
                                          ('add', time, namespace, deadline))

  def memcache_replace(self, key, value, time=0, namespace=None, deadline=None):
    if not isinstance(key, (six.text_type, six.binary_type)):
      raise TypeError('key must be a string; received %r' % key)
    if not isinstance(time, six.integer_types):
      raise TypeError('time must be a number; received %r' % time)
    if namespace is None:
      namespace = namespace_manager.get_namespace()
    options = ('replace', time, namespace, deadline)
    return self._memcache_set_batcher.add((key, value), options)

  def memcache_cas(self, key, value, time=0, namespace=None, deadline=None):
    if not isinstance(key, (six.text_type, six.binary_type)):
      raise TypeError('key must be a string; received %r' % key)
    if not isinstance(time, six.integer_types):
      raise TypeError('time must be a number; received %r' % time)
    if namespace is None:
      namespace = namespace_manager.get_namespace()
    return self._memcache_set_batcher.add((key, value),
                                          ('cas', time, namespace, deadline))

  def memcache_delete(self, key, seconds=0, namespace=None, deadline=None):
    if not isinstance(key, (six.text_type, six.binary_type)):
      raise TypeError('key must be a string; received %r' % key)
    if not isinstance(seconds, six.integer_types):
      raise TypeError('seconds must be a number; received %r' % seconds)
    if namespace is None:
      namespace = namespace_manager.get_namespace()
    return self._memcache_del_batcher.add(key, (seconds, namespace, deadline))

  def memcache_incr(self, key, delta=1, initial_value=None, namespace=None,
                    deadline=None):
    if not isinstance(key, (six.text_type, six.binary_type)):
      raise TypeError('key must be a string; received %r' % key)
    if not isinstance(delta, six.integer_types):
      raise TypeError('delta must be a number; received %r' % delta)
    if initial_value is not None and not isinstance(initial_value,
                                                    six.integer_types):
      raise TypeError('initial_value must be a number or None; received %r' %
                      initial_value)
    if namespace is None:
      namespace = namespace_manager.get_namespace()
    return self._memcache_off_batcher.add((key, delta),
                                          (initial_value, namespace, deadline))

  def memcache_decr(self, key, delta=1, initial_value=None, namespace=None,
                    deadline=None):
    if not isinstance(key, (six.text_type, six.binary_type)):
      raise TypeError('key must be a string; received %r' % key)
    if not isinstance(delta, six.integer_types):
      raise TypeError('delta must be a number; received %r' % delta)
    if initial_value is not None and not isinstance(initial_value,
                                                    six.integer_types):
      raise TypeError('initial_value must be a number or None; received %r' %
                      initial_value)
    if namespace is None:
      namespace = namespace_manager.get_namespace()
    return self._memcache_off_batcher.add((key, -delta),
                                          (initial_value, namespace, deadline))

  @tasklets.tasklet
  def urlfetch(self, url, payload=None, method='GET', headers={},
               allow_truncated=False, follow_redirects=True,
               validate_certificate=None, deadline=None, callback=None):
    rpc = urlfetch.create_rpc(deadline=deadline, callback=callback)
    urlfetch.make_fetch_call(rpc, url,
                             payload=payload,
                             method=method,
                             headers=headers,
                             allow_truncated=allow_truncated,
                             follow_redirects=follow_redirects,
                             validate_certificate=validate_certificate)
    result = yield rpc
    raise tasklets.Return(result)
