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




"""An APIProxy stub that communicates with VMEngine service bridges."""

from concurrent import futures
import imp
import logging
import os
import sys
import threading
from google.appengine.api import apiproxy_rpc
from google.appengine.api import apiproxy_stub_map
from google.appengine.ext.remote_api import remote_api_bytes_pb2 as remote_api_pb2
from google.appengine.runtime import apiproxy_errors
import six.moves.urllib.parse
import urllib3









logging.getLogger('requests_nologs').setLevel(logging.ERROR)

TICKET_HEADER = 'HTTP_X_APPENGINE_API_TICKET'
DEV_TICKET_HEADER = 'HTTP_X_APPENGINE_DEV_REQUEST_ID'
DAPPER_ENV_KEY = 'HTTP_X_GOOGLE_DAPPERTRACEINFO'
SERVICE_BRIDGE_HOST = 'appengine.googleapis.internal'
API_PORT = 10001
SERVICE_ENDPOINT_NAME = 'app-engine-apis'
APIHOST_METHOD = '/VMRemoteAPI.CallRemoteAPI'
PROXY_PATH = '/rpc_http'
DAPPER_HEADER = 'X-Google-DapperTraceInfo'
SERVICE_DEADLINE_HEADER = 'X-Google-RPC-Service-Deadline'
SERVICE_ENDPOINT_HEADER = 'X-Google-RPC-Service-Endpoint'
SERVICE_METHOD_HEADER = 'X-Google-RPC-Service-Method'
RPC_CONTENT_TYPE = 'application/octet-stream'
DEFAULT_TIMEOUT = 60

DEADLINE_DELTA_SECONDS = 1





MAX_CONCURRENT_API_CALLS = 100

URLLIB3_POOL_COUNT = 10

URLLIB3_POOL_SIZE = 10



_EXCEPTIONS_MAP = {
    remote_api_pb2.RpcError.UNKNOWN:
        (apiproxy_errors.RPCFailedError,
         'The remote RPC to the application server failed for call %s.%s().'),
    remote_api_pb2.RpcError.CALL_NOT_FOUND:
        (apiproxy_errors.CallNotFoundError,
         'The API package \'%s\' or call \'%s()\' was not found.'),
    remote_api_pb2.RpcError.PARSE_ERROR:
        (apiproxy_errors.ArgumentError,
         'There was an error parsing arguments for API call %s.%s().'),
    remote_api_pb2.RpcError.OVER_QUOTA:
        (apiproxy_errors.OverQuotaError,
         'The API call %s.%s() required more quota than is available.'),
    remote_api_pb2.RpcError.REQUEST_TOO_LARGE:
        (apiproxy_errors.RequestTooLargeError,
         'The request to API call %s.%s() was too large.'),
    remote_api_pb2.RpcError.CAPABILITY_DISABLED:
        (apiproxy_errors.CapabilityDisabledError,
         'The API call %s.%s() is temporarily disabled.'),
    remote_api_pb2.RpcError.FEATURE_DISABLED:
        (apiproxy_errors.FeatureNotEnabledError,
         'The API call %s.%s() is currently not enabled.'),
    remote_api_pb2.RpcError.RESPONSE_TOO_LARGE:
        (apiproxy_errors.ResponseTooLargeError,
         'The response from API call %s.%s() was too large.'),
    remote_api_pb2.RpcError.CANCELLED:
        (apiproxy_errors.CancelledError,
         'The API call %s.%s() was explicitly cancelled.'),
    remote_api_pb2.RpcError.DEADLINE_EXCEEDED:
        (apiproxy_errors.DeadlineExceededError,
         'The API call %s.%s() took too long to respond and was cancelled.')
}

_DEFAULT_EXCEPTION = _EXCEPTIONS_MAP[remote_api_pb2.RpcError.UNKNOWN]

_DEADLINE_EXCEEDED_EXCEPTION = _EXCEPTIONS_MAP[
    remote_api_pb2.RpcError.DEADLINE_EXCEEDED]






class DefaultApiRPC(apiproxy_rpc.RPC):
  """A class representing an RPC to a remote server."""

  def _ErrorException(self, exception_class, error_details):
    return exception_class(error_details % (self.package, self.call))

  def _TranslateToError(self, response):
    """Translates a failed APIResponse into an exception."""


    if response.HasField('rpc_error'):
      code = response.rpc_error.code
      detail = response.rpc_error.detail
      exception_type, msg = _EXCEPTIONS_MAP.get(code, _DEFAULT_EXCEPTION)
      if detail:
        msg = '%s -- Additional details from server: %s' % (msg, detail)
      raise self._ErrorException(exception_type, msg)


    raise apiproxy_errors.ApplicationError(response.application_error.code,
                                           response.application_error.detail)

  def _MakeCallImpl(self):
    """Makes an asynchronous API call over the service bridge.

    For this to work the following must be set:
      self.package: the API package name;
      self.call: the name of the API call/method to invoke;
      self.request: the API request body as a serialized protocol buffer.

    The actual API call is made by urllib3.request via a thread pool
    (multiprocessing.dummy.Pool). The thread pool restricts the number of
    concurrent requests to MAX_CONCURRENT_API_CALLS, so this method will
    block if that limit is exceeded, until other asynchronous calls resolve.

    If the main thread holds the import lock, waiting on thread work can cause
    a deadlock:
    https://docs.python.org/2/library/threading.html#importing-in-threaded-code

    Therefore, we try to detect this error case and fall back to sync calls.
    """
    assert self._state == apiproxy_rpc.RPC.IDLE, self._state






    ticket = None
    if DefaultApiStub.ShouldUseRequestSecurityTicketForThread():


      ticket = os.environ.get(TICKET_HEADER, os.environ.get(DEV_TICKET_HEADER))

    if not ticket:
      raise apiproxy_errors.RPCFailedError(
          'Attempted RPC call without active security ticket')

    request = remote_api_pb2.Request(
        service_name=self.package,
        method=self.call,
        request_id=ticket,
        request=self.request.SerializeToString())

    deadline = self.deadline or DEFAULT_TIMEOUT

    body_data = request.SerializeToString()
    headers = {
        SERVICE_DEADLINE_HEADER: str(deadline),
        SERVICE_ENDPOINT_HEADER: SERVICE_ENDPOINT_NAME,
        SERVICE_METHOD_HEADER: APIHOST_METHOD,
        'Content-type': RPC_CONTENT_TYPE,
    }


    dapper_header_value = os.environ.get(DAPPER_ENV_KEY)
    if dapper_header_value:
      headers[DAPPER_HEADER] = dapper_header_value





    api_host = os.environ.get('API_HOST', SERVICE_BRIDGE_HOST)
    api_port = os.environ.get('API_PORT', API_PORT)

    if ':' in api_host:
      api_host = '[{}]'.format(api_host)
    endpoint_url = six.moves.urllib.parse.urlunparse(
        ('http', '%s:%s' % (api_host, api_port), PROXY_PATH, '', '', ''))

    self._state = apiproxy_rpc.RPC.RUNNING

    request_kwargs = dict(
        url=endpoint_url,
        method='POST',
        timeout=DEADLINE_DELTA_SECONDS + deadline,
        headers=headers,
        body=body_data)






    if six.PY2 and imp.lock_held():
      self.future = futures.Future()
      self.future.set_result(self._SendRequestAndFinish(**request_kwargs))

    else:


      self.future = self.stub.thread_pool.submit(self._SendRequestAndFinish,
                                                 **request_kwargs)

  def _WaitImpl(self):

    assert self.future is not None
    futures.wait([self.future])
    return True

  def _SendRequest(self, **kwargs):
    try:
      response = self.stub.http.request(**kwargs)

      if response.status != 200:
        raise apiproxy_errors.RPCFailedError(
            'Proxy returned HTTP status %s %s' %
            (response.status, response.reason))
    except urllib3.exceptions.TimeoutError:
      raise self._ErrorException(*_DEADLINE_EXCEEDED_EXCEPTION)
    except (urllib3.exceptions.RequestError,
            urllib3.exceptions.ConnectionError):

      raise self._ErrorException(*_DEFAULT_EXCEPTION)


    parsed_response = remote_api_pb2.Response.FromString(response.data)


    if (parsed_response.HasField('application_error') or
        parsed_response.HasField('rpc_error')):
      raise self._TranslateToError(parsed_response)


    self.response.ParseFromString(parsed_response.response)

  def _CaptureTrace(self, f, **kwargs):
    try:
      f(**kwargs)
    except Exception:


      _, exc, tb = sys.exc_info()
      self._exception = exc
      self._traceback = tb

  def _SendRequestAndFinish(self, **kwargs):
    try:
      self._CaptureTrace(self._SendRequest, **kwargs)
    finally:
      if self.callback:
        self._CaptureTrace(self.callback)
      self._state = apiproxy_rpc.RPC.FINISHING


class _UseRequestSecurityTicketLocal(threading.local):
  """Thread local holding if the default ticket should always be used."""

  def __init__(self):
    super(_UseRequestSecurityTicketLocal, self).__init__()
    self.use_ticket_header_value = False


class DefaultApiStub(object):
  """A stub for calling services through a VM service bridge.

  You can use this to stub out any service that the remote server supports.
  """


  _USE_REQUEST_SECURITY_TICKET_LOCAL = _UseRequestSecurityTicketLocal()

  @classmethod
  def SetUseRequestSecurityTicketForThread(cls, value):
    """Sets if the in environment security ticket should be used.

    Security tickets are set in the os.environ, which gets inherited by a
    child thread.  Child threads should not use the security ticket of their
    parent by default, because once the parent thread returns and the request
    is complete, the security ticket is no longer valid.

    Args:
      value: Boolean value describing if we should use the security ticket.
    """
    cls._USE_REQUEST_SECURITY_TICKET_LOCAL.use_ticket_header_value = value

  @classmethod
  def ShouldUseRequestSecurityTicketForThread(cls):
    """Gets if thie security ticket should be used for this thread."""
    return cls._USE_REQUEST_SECURITY_TICKET_LOCAL.use_ticket_header_value


  def __init__(self):
    self.thread_pool = futures.ThreadPoolExecutor(MAX_CONCURRENT_API_CALLS)
    self.http = urllib3.PoolManager(
        num_pools=URLLIB3_POOL_COUNT, maxsize=URLLIB3_POOL_SIZE)

  def MakeSyncCall(self, service, call, request, response):
    """Make a synchronous API call.

    Args:
      service: The name of the service you are trying to use.
      call: The name of the method.
      request: The request protocol buffer
      response: The response protocol buffer to be filled.
    """
    rpc = self.CreateRPC()
    rpc.MakeCall(service, call, request, response)
    rpc.Wait()
    rpc.CheckSuccess()

  def CreateRPC(self):
    """Create a new RPC object."""
    return DefaultApiRPC(stub=self)


def Register(stub):
  """Insert stubs so App Engine services are accessed via the service bridge."""
  apiproxy_stub_map.apiproxy.SetDefaultStub(stub)
