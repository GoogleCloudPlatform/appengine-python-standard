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



"""Container of APIProxy stubs for more convenient unittesting.

Classes/variables/functions defined here:

-  `APIProxyStubMap`: Container of APIProxy stubs.
-  `apiproxy`: Global instance of an APIProxyStubMap.
-  `MakeSyncCall`: APIProxy entry point.
-  `UserRPC`: User-visible class wrapping asynchronous RPCs.
"""








from concurrent import futures
import inspect
import threading
import six

from google.appengine.api import apiproxy_rpc
from google.appengine.runtime import apiproxy_errors




def CreateRPC(service, stubmap=None):
  """Creates a RPC instance for the given service.

  The instance is suitable for talking to remote services.
  Each RPC instance can be used only once, and should not be reused.

  Args:
    service: `string`. Represents which service to call.
    stubmap: Optional `APIProxyStubMap` instance, for dependency injection.

  Returns:
    The rpc object.

  Raises:
    `AssertionError` or `RuntimeError` if the stub for service doesn't supply a
    `CreateRPC` method.
  """
  if stubmap is None:
    stubmap = apiproxy
  stub = stubmap.GetStub(service)

  assert stub, 'No api proxy found for service "%s"' % service
  assert hasattr(stub, 'CreateRPC'), (('The service "%s" doesn\'t have ' +
                                       'a CreateRPC method.') % service)
  return stub.CreateRPC()


def MakeSyncCall(service, call, request, response, stubmap=None):
  """The APIProxy entry point for a synchronous API call.

  Args:
    service: `string`. Represents which service to call.
    call: `string`. Represents which function to call.
    request: Protocol buffer for the request.
    response: Protocol buffer for the response.
    stubmap: Optional `APIProxyStubMap` instance, for dependency injection.

  Returns:
    Response protocol buffer or `None`. Some implementations may return
    a response protocol buffer instead of modifying `response`.
    Caller must use returned value in such cases. If `response` is modified
    then returns `None`.

  Raises:
    `apiproxy_errors.Error` or a subclass.
  """
  if stubmap is None:
    stubmap = apiproxy
  return stubmap.MakeSyncCall(service, call, request, response)


class ListOfHooks(object):
  """An ordered collection of hooks for a particular API call.

  A hook is a function that has exactly the same signature as
  a service stub. It will be called before or after an API hook is
  executed, depending on whether this list is for precall of postcall hooks.
  Hooks can be used for debugging purposes (check certain
  pre- or postconditions on api calls) or to apply patches to protocol
  buffers before/after a call gets submitted.
  """

  def __init__(self):
    """Constructor."""


    self.__content = []


    self.__unique_keys = set()

  def __len__(self):
    """Returns the amount of elements in the collection."""
    return self.__content.__len__()

  def __Insert(self, index, key, function, service=None):
    """Appends a hook at a certain position in the list.

    Args:
      index: the index of where to insert the function
      key: a unique key (within the module) for this particular function.
        If something from the same module with the same key is already
        registered, nothing will be added.
      function: the hook to be added.
      service: optional argument that restricts the hook to a particular api

    Returns:
      True if the collection was modified.
    """
    unique_key = (key, inspect.getmodule(function))
    if unique_key in self.__unique_keys:
      return False
    argsspec_func = inspect.getfullargspec if six.PY3 else inspect.getargspec
    num_args = len(argsspec_func(function)[0])
    if (inspect.ismethod(function)):
      num_args -= 1
    self.__content.insert(index, (key, function, service, num_args))
    self.__unique_keys.add(unique_key)
    return True

  def Append(self, key, function, service=None):
    """Appends a hook at the end of the list.

    Args:
      key: A unique key (within the module) for this particular function.
        If something from the same module with the same key is already
        registered, nothing will be added.
      function: The hook to be added.
      service: Optional argument that restricts the hook to a particular API.

    Returns:
      `True` if the collection was modified.
    """
    return self.__Insert(len(self), key, function, service)

  def Push(self, key, function, service=None):
    """Inserts a hook at the beginning of the list.

    Args:
      key: A unique key (within the module) for this particular function.
        If something from the same module with the same key is already
        registered, nothing will be added.
      function: The hook to be added.
      service: Optional argument that restricts the hook to a particular API.

    Returns:
      `True` if the collection was modified.
    """
    return self.__Insert(0, key, function, service)

  def Clear(self):
    """Removes all hooks from the list (useful for unit tests)."""
    self.__content = []
    self.__unique_keys = set()

  def Call(self, service, call, request, response, rpc=None, error=None):
    """Invokes all hooks in this collection.

    NOTE: For backwards compatibility, if error is not `None`, hooks
    with 4 or 5 arguments are *not* called. This situation
    (`error=None`) only occurs when the RPC request raised an exception;
    in the past no hooks would be called at all in that case.

    Args:
      service: `string`. Represents which service to call.
      call: `string`. Representswhich function to call.
      request: Protocol buffer for the request.
      response: Protocol buffer for the response.
      rpc: Optional RPC used to make this call.
      error: Optional `Exception` instance to be passed as sixth argument.
    """
    for key, function, srv, num_args in self.__content:
      if srv is None or srv == service:
        if num_args == 6:
          function(service, call, request, response, rpc, error)
        elif error is not None:


          pass
        elif num_args == 5:
          function(service, call, request, response, rpc)
        else:
          function(service, call, request, response)


class _CancelFuture(futures.Future):
  pass


class WaitCanceller(object):
  """A helper object that can be used to cancel a `UserRPC.wait_any()` call.

  An instance of this class can be passed in the RPCs list to
  `UserRPC.wait_any()` to cancel the wait.
  """

  def __init__(self):
    self.future = _CancelFuture()
    self.future._canceller = self

  def cancel(self):
    """Indicates that the wait should be cancelled."""
    if not self.future.cancelled():
      self.future.cancel()
      self.future.set_running_or_notify_cancel()


class APIProxyStubMap(object):
  """Container of APIProxy stubs for more convenient unittesting.

  Stubs may be either trivial implementations of APIProxy services (e.g.
  DatastoreFileStub, UserServiceStub) or "real" implementations.

  For unittests, we may want to mix and match real and trivial implementations
  of services in order to better focus testing on individual service
  implementations. To achieve this, we allow the client to attach stubs to
  service names, as well as define a default stub to be used if no specific
  matching stub is identified.
  """




  def __init__(self, default_stub=None):
    """Constructor.

    Args:
      default_stub: optional stub. `default_stub` will be used whenever no
        specific matching stub is found.
    """
    self.__stub_map = {}
    self.__default_stub = default_stub
    self.__precall_hooks = ListOfHooks()
    self.__postcall_hooks = ListOfHooks()

  def SetDefaultStub(self, stub):
    self.__default_stub = stub

  def GetPreCallHooks(self):
    """Gets a collection for all precall hooks."""
    return self.__precall_hooks

  def GetPostCallHooks(self):
    """Gets a collection for all precall hooks."""
    return self.__postcall_hooks

  def ReplaceStub(self, service, stub):
    """Replace the existing stub for the specified service with a new one.

    NOTE: This is a risky operation; external callers should use this with
    caution.

    Args:
      service: string
      stub: stub
    """
    self.__stub_map[service] = stub







    if service == 'datastore':
      self.RegisterStub('datastore_v3', stub)

  def RegisterStub(self, service, stub):
    """Register the provided stub for the specified service.

    Args:
      service: string
      stub: stub
    """
    assert service not in self.__stub_map, repr(service)
    self.ReplaceStub(service, stub)

  def GetStub(self, service):
    """Retrieve the stub registered for the specified service.

    Args:
      service: string

    Returns:
      stub

    Returns the stub registered for 'service', and returns the default stub
    if no such stub is found.
    """
    return self.__stub_map.get(service, self.__default_stub)

  def _CopyStubMap(self):
    """Get a copy of the stub map. For testing only.

    Returns:
      Get a shallow copy of the stub map.
    """
    return dict(self.__stub_map)

  def MakeSyncCall(self, service, call, request, response):
    """The APIProxy entry point.

    Args:
      service: string representing which service to call
      call: string representing which function to call
      request: protocol buffer for the request
      response: protocol buffer for the response

    Returns:
      Response protocol buffer or `None`. Some implementations may return
      a response protocol buffer instead of modifying `response`.
      Caller must use returned value in such cases. If `response` is modified
      then returns `None`.

    Raises:
      `apiproxy_errors.Error` or a subclass.
    """


    stub = self.GetStub(service)
    assert stub, 'No api proxy found for service "%s"' % service
    if hasattr(stub, 'CreateRPC'):
      rpc = stub.CreateRPC()
      self.__precall_hooks.Call(service, call, request, response, rpc)
      try:
        rpc.MakeCall(service, call, request, response)
        rpc.Wait()
        rpc.CheckSuccess()
      except Exception as err:
        self.__postcall_hooks.Call(service, call, request, response, rpc, err)
        raise
      else:
        self.__postcall_hooks.Call(service, call, request, response, rpc)
    else:
      self.__precall_hooks.Call(service, call, request, response)
      try:
        returned_response = stub.MakeSyncCall(service, call, request, response)
      except Exception as err:
        self.__postcall_hooks.Call(service, call, request, response, None, err)
        raise
      else:
        self.__postcall_hooks.Call(service, call, request,
                                   returned_response or response)
        return returned_response

  def CancelApiCalls(self):
    if self.__default_stub:
      self.__default_stub.CancelApiCalls()


class UserRPC(object):
  """Wrapper class for asynchronous RPC.

  Simplest low-level usage pattern:

    ```python
    rpc = UserRPC('service', [deadline], [callback])
    rpc.make_call('method', request, response)
    .
    .
    .
    rpc.wait()
    rpc.check_success()
    ```

  However, a service module normally provides a wrapper so that the
  typical usage pattern becomes more like this:

    ```python
    from google.appengine.api import service
    rpc = service.create_rpc([deadline], [callback])
    service.make_method_call(rpc, [service-specific-args])
    .
    .
    .
    rpc.wait()
    result = rpc.get_result()
    ```

  The `service.make_method_call()` function sets a service- and method-
  specific hook function that is called by `rpc.get_result()` with the
  rpc object as its first argument, and service-specific value as its
  second argument.  The hook function should call `rpc.check_success()`
  and then extract the user-level result from the `rpc.result`
  protobuffer.  Additional arguments may be passed from
  `make_method_call()` to the `get_result` hook via the second argument.

  Also note `wait_any()` and `wait_all()`, which wait for multiple RPCs.
  """

  __method = None
  __get_result_hook = None
  __user_data = None
  __postcall_hooks_called = False
  __must_call_user_callback = False

  class MyLocal(threading.local):
    """Class to hold per-thread class level attributes."""

    may_interrupt_wait = False

  __local = MyLocal()

  def __init__(self, service, deadline=None, callback=None, stubmap=None):
    """Constructor.

    Args:
      service: The service name.
      deadline: Optional deadline.  Default depends on the implementation.
      callback: Optional argument-less callback function.
      stubmap: optional APIProxyStubMap instance, for dependency injection.
    """
    if stubmap is None:
      stubmap = apiproxy
    self.__stubmap = stubmap
    self.__service = service
    self.__rpc = CreateRPC(service, stubmap)
    self.__rpc.deadline = deadline
    self.__rpc.callback = self.__internal_callback
    self.callback = callback













    self.__class__.__local.may_interrupt_wait = False

  def __internal_callback(self):
    """This is the callback set on the low-level RPC object.

    It sets a flag on the current object indicating that the high-level
    callback should now be called.  If interrupts are enabled, it also
    interrupts the current wait_any() call by raising an exception.
    """
    self.__must_call_user_callback = True
    self.__rpc.callback = None
    if self.__class__.__local.may_interrupt_wait and not self.__rpc.exception:








      raise apiproxy_errors.InterruptedError(None, self.__rpc)

  @property
  def service(self):
    """Return the service name."""
    return self.__service

  @property
  def method(self):
    """Return the method name."""
    return self.__method

  @property
  def deadline(self):
    """Return the deadline, if set explicitly (otherwise `None`)."""
    return self.__rpc.deadline

  @property
  def request(self):
    """Return the request protocol buffer object."""
    return self.__rpc.request

  @property
  def response(self):
    """Return the response protocol buffer object."""
    return self.__rpc.response

  @property
  def state(self):
    """Return the RPC state.

    Possible values are attributes of apiproxy_rpc.RPC: IDLE, RUNNING,
    FINISHING.
    """
    return self.__rpc.state

  @property
  def get_result_hook(self):
    """Return the get-result hook function."""
    return self.__get_result_hook

  @property
  def user_data(self):
    """Return the user data for the hook function."""
    return self.__user_data

  @property
  def future(self):
    """Return the underlying RPC's future, if present."""
    return getattr(self.__rpc, 'future', None)

  def make_call(self, method, request, response,
                get_result_hook=None, user_data=None):
    """Initiate a call.

    Args:
      method: The method name.
      request: The request protocol buffer.
      response: The response protocol buffer.
      get_result_hook: Optional get-result hook function.  If not `None`,
        this must be a function with exactly one argument, the RPC
        object (`self`).  Its return value is returned from `get_result()`.
      user_data: Optional additional arbitrary data for the get-result
        hook function.  This can be accessed as `rpc.user_data`.  The
        type of this value is up to the service module.

    This function may only be called once per RPC object.  It sends
    the request to the remote server, but does not wait for a
    response.  This allows concurrent execution of the remote call and
    further local processing (e.g., making additional remote calls).

    Before the call is initiated, the precall hooks are called.
    """

    assert self.__rpc.state == apiproxy_rpc.RPC.IDLE, repr(self.state)

    self.__method = method

    self.__get_result_hook = get_result_hook
    self.__user_data = user_data

    self.__stubmap.GetPreCallHooks().Call(
        self.__service, method, request, response, self.__rpc)

    self.__rpc.MakeCall(self.__service, method, request, response)

  def wait(self):
    """Wait for the call to complete, and call callback if needed.

    This and `wait_any()`/`wait_all()` are the only time callback
    functions may be called.  (However, note that `check_success()` and
    `get_result()` call `wait()`.)  Waiting for one RPC will not cause
    callbacks for other RPCs to be called.  Callback functions may
    call `check_success()` and `get_result()`.

    Callbacks are called without arguments; if a callback needs access
    to the RPC object a Python nested function (a.k.a. closure) or a
    bound may be used.  To facilitate this, the callback may be
    assigned after the RPC object is created (but before `make_call()`
    is called).

    Note: Don't confuse callbacks with get-result hooks or precall
    and postcall hooks.
    """

    assert self.__rpc.state != apiproxy_rpc.RPC.IDLE, repr(self.state)

    if self.__rpc.state == apiproxy_rpc.RPC.RUNNING:
      self.__rpc.Wait()

    assert self.__rpc.state == apiproxy_rpc.RPC.FINISHING, repr(self.state)
    self.__call_user_callback()

  def __call_user_callback(self):
    """Call the high-level callback, if requested."""
    if self.__must_call_user_callback:
      self.__must_call_user_callback = False
      if self.callback is not None:
        self.callback()

  def check_success(self):
    """Check for success of the RPC, possibly raising an exception.

    This function should be called at least once per RPC.  If `wait()`
    hasn't been called yet, it is called first.  If the RPC caused
    an exceptional condition, an exception will be raised here.
    The first time `check_success()` is called, the postcall hooks
    are called.
    """


    self.wait()
    try:
      self.__rpc.CheckSuccess()
    except Exception as err:

      if not self.__postcall_hooks_called:
        self.__postcall_hooks_called = True
        self.__stubmap.GetPostCallHooks().Call(self.__service, self.__method,
                                               self.request, self.response,
                                               self.__rpc, err)
      raise
    else:

      if not self.__postcall_hooks_called:
        self.__postcall_hooks_called = True
        self.__stubmap.GetPostCallHooks().Call(self.__service, self.__method,
                                               self.request, self.response,
                                               self.__rpc)

  def get_result(self):
    """Get the result of the RPC, or possibly raise an exception.

    This implies a call to `check_success()`.  If a get-result hook was
    passed to `make_call()`, that hook is responsible for calling
    `check_success()`, and the return value of the hook is returned.
    Otherwise, `check_success()` is called directly and `None` is
    returned.
    """




    if self.__get_result_hook is None:
      self.check_success()
      return None
    else:
      return self.__get_result_hook(self)



  @classmethod
  def __is_finished(cls, rpc):
    """Check if the given RPC is finished or is running.

    Args:
      rpc: `UserRPC` instance.

    Returns:
      `True` if the RPC is finished.
      `False` if the RPC is running.
    """
    assert isinstance(rpc, cls), repr(rpc)
    state = rpc.__rpc.state
    if state == apiproxy_rpc.RPC.FINISHING:
      rpc.__call_user_callback()
      return True

    assert state != apiproxy_rpc.RPC.IDLE, repr(rpc)
    return False



  @classmethod
  def __get_first_finished_or_last_running(cls, rpcs):
    """Check the list of RPCs for first one finished, the last one running, or `None`.

    Args:
      rpcs: Iterable collection of `UserRPC` instances.

    Returns:
      A pair `(finished, running)`, as follows:
      `(UserRPC, None)` indicating the first RPC found that is finished;
      `(None, UserRPC)` indicating the last RPC found that is running;
      `(None, None)` indicating no RPCs are finished or running.
    """
    rpc = None
    for rpc in rpcs:
      if cls.__is_finished(rpc):
        return rpc, None
    return None, rpc

  @classmethod
  def wait_any(cls, rpcs):
    """Wait until an RPC is finished.

    A `WaitCanceller` can also be included in the list of RPCs as a mechanism to
    cancel the wait.

    Args:
      rpcs: Iterable collection of `UserRPC` or `WaitCanceller` instances.

    Returns:
      A `UserRPC` instance, indicating the first RPC among the given
      RPCs that finished; or `None`, indicating that either an RPC not
      among the given RPCs finished in the mean time, or the iterable
      is empty.

    NOTES:

      - Repeatedly calling `wait_any()` with the same arguments will not wait;
        it will immediately return, meaning it will return the same RPC until
        one earlier in the
        collection finishes.  The callback, however, will only be called the
        first time the RPC finishes (which may be here or in the `wait()`
        method).
    """
    assert iter(rpcs) is not rpcs, 'rpcs must be a collection, not an iterator'
    rpc_futures = [rpc.future for rpc in rpcs if rpc.future]
    done, _ = futures.wait(rpc_futures, return_when=futures.FIRST_COMPLETED)
    if done and done == set(f for f in done if isinstance(f, _CancelFuture)):

      return next(iter(done))._canceller

    rpcs = [rpc for rpc in rpcs if not isinstance(rpc, WaitCanceller)]
    finished, running = cls.__get_first_finished_or_last_running(rpcs)
    if finished:

      return finished

    if running is None:
      return None

    try:
      cls.__local.may_interrupt_wait = True
      try:
        running.__rpc.Wait()
      except apiproxy_errors.InterruptedError as err:





        err.rpc._exception = None
        err.rpc._traceback = None
    finally:
      cls.__local.may_interrupt_wait = False
    finished, running = cls.__get_first_finished_or_last_running(rpcs)
    return finished

  @classmethod
  def wait_all(cls, rpcs):
    """Wait until all given RPCs are finished.

    This is a thin wrapper around `wait_any()` that loops until all
    given RPCs have finished.

    Args:
      rpcs: Iterable collection of `UserRPC` instances.

    Returns:
      None.
    """
    rpcs = set(rpcs)
    while rpcs:
      finished = cls.wait_any(rpcs)
      if finished is not None:
        rpcs.remove(finished)



def GetDefaultAPIProxy():
  return APIProxyStubMap()




apiproxy = GetDefaultAPIProxy()
