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


"""Base class for implementing RPC of API proxy stubs."""








from concurrent import futures
import sys
import contextvars








_MAX_CONCURRENT_API_CALLS = 100

_THREAD_POOL = futures.ThreadPoolExecutor(_MAX_CONCURRENT_API_CALLS)


class RPC(object):
  """Base class for implementing RPC of API proxy stubs.

  Constructor for the RPC object.

  All arguments are optional, and simply set members on the class.
  These data members will be overriden by values passed to `MakeCall`.
  """

  IDLE = 0
  RUNNING = 1
  FINISHING = 2

  def __init__(self, package=None, call=None, request=None, response=None,
               callback=None, deadline=None, stub=None):
    """Constructor.

    Args:
      package: `string`. The package for the call.
      call: `string`. The call within the package.
      request: `ProtocolMessage` instance. Appropriate for the arguments.
      response: `ProtocolMessage` instance. Appropriate for the response.
      callback: `callable`. Called when call is complete.
      deadline: `double`. Specifies the deadline for this call as the number
        of seconds from the current time. Ignored if non-positive.
      stub: `APIProxyStub` instance. Used in default `_WaitImpl` to do real
        call.
    """
    self._exception = None
    self._state = RPC.IDLE

    self.package = package
    self.call = call
    self.request = request
    self.future = None
    self.response = response
    self.callback = callback
    self.deadline = deadline
    self.stub = stub
    self.cpu_usage_mcycles = 0

  def Clone(self):
    """Make a shallow copy of this instances attributes, excluding methods.

    This is usually used when an RPC has been specified with some configuration
    options and is being used as a template for multiple RPCs outside of a
    developer's easy control.

    Returns:
      A clone of this RPC.
    """
    if self.state != RPC.IDLE:
      raise AssertionError('Cannot clone a call already in progress')

    clone = self.__class__()
    for k, v in self.__dict__.items():
      setattr(clone, k, v)
    return clone

  def MakeCall(self, package=None, call=None, request=None, response=None,
               callback=None, deadline=None):
    """Makes an asynchronous (i.e., non-blocking) API call within the specified package for the specified call method.

    It will call the `_MakeRealCall` to do the real job.

    Args:
      package: `string`. The package for the call.
      call: `string`. The call within the package.
      request: `ProtocolMessage` instance. Appropriate for the arguments.
      response: `ProtocolMessage` instance. Appropriate for the response.
      callback: `callable`. Called when call is complete.
      deadline: `double`. Specifies the deadline for this call as the number
        of seconds from the current time. Ignored if non-positive.

    Raises:
      `TypeError` or `AssertionError` if an argument is of an invalid type.
      `AssertionError` or `RuntimeError` is an RPC is already in use.
    """
    self.callback = callback or self.callback
    self.package = package or self.package
    self.call = call or self.call
    self.request = request or self.request
    self.response = response or self.response
    self.deadline = deadline or self.deadline
    self.future = None

    assert self._state == RPC.IDLE, ('RPC for %s.%s has already been started' %
                                     (self.package, self.call))
    assert self.callback is None or callable(self.callback)
    self._MakeCallImpl()

  def Wait(self):
    """Waits on the API call associated with this RPC."""
    rpc_completed = self._WaitImpl()

    assert rpc_completed, ('RPC for %s.%s was not completed, and no other '
                           'exception was raised ' % (self.package, self.call))

  def CheckSuccess(self):
    """If there was an exception, raise it now.

    Raises:
      Exception of the API call or the `callback`, if any.
    """
    if self.exception:
      raise self.exception

  @property
  def exception(self):
    return self._exception

  @property
  def state(self):
    return self._state

  def _MakeCallImpl(self):
    """Makes an asynchronous API call.

    For this to work the following must be set:
      `self.package`: the API package name;
      `self.call`: the name of the API call/method to invoke;
      `self.request`: the API request body as a serialized protocol buffer.

    The actual API call is made via a thread pool. The thread pool restricts the
    number of concurrent requests to `MAX_CONCURRENT_API_CALLS`, so this method
    will block if that limit is exceeded, until other asynchronous calls
    resolve.

    If the main thread holds the import lock, waiting on thread work can cause
    a deadlock:
    https://docs.python.org/2/library/threading.html#importing-in-threaded-code

    Therefore, we try to detect this error case and fall back to sync calls.
    """
    assert self._state == RPC.IDLE, self._state

    self._state = RPC.RUNNING


    run_async = getattr(self.stub.__class__, 'THREADSAFE', False)

    ctx = contextvars.copy_context()

    def ExecInContext():
      ctx.run(self._SendRequestAndFinish)

    if run_async:
      self.future = _THREAD_POOL.submit(ExecInContext)
    else:
      self.future = None

  def _WaitImpl(self):
    """Waits for this and only this RPC to complete."""

    if self.future:
      futures.wait([self.future])
      return True


    self._SendRequestAndFinish(reraise_callback_exception=True)
    return True

  def _SendRequest(self):
    self.stub.MakeSyncCall(self.package, self.call, self.request, self.response)

  def _CaptureTrace(self, f):
    """Runs `f()` and captures exception information if raised."""
    try:
      f()
    except Exception as exc:


      self._exception = exc

  def _CaptureTraceAndReraise(self, f):
    """A variant of `_CaptureTrace()` used in the synchronous fallback path."""
    try:
      f()
    except:
      _, exc, _ = sys.exc_info()
      self._exception = exc


      self._exception._appengine_apiproxy_rpc = self
      raise

  def _SendRequestAndFinish(self, reraise_callback_exception=False):
    try:
      self._CaptureTrace(self._SendRequest)
    finally:
      self._state = RPC.FINISHING
      if self.callback:
        if reraise_callback_exception:
          self._CaptureTraceAndReraise(self.callback)
        else:
          self._CaptureTrace(self.callback)
