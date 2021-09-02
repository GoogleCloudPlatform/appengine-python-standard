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


"""Tests for the 'taskqueue' module."""


import datetime
import functools
import os
import time

import google


from google.appengine.tools import os_compat

from absl import app
from google.appengine.api import apiproxy_rpc
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import full_app_id
from google.appengine.api import module_testutil
from google.appengine.api import modules
from google.appengine.api.modules import modules_service_pb2
from google.appengine.api.taskqueue import taskqueue
from google.appengine.api.taskqueue import taskqueue_service_bytes_pb2 as taskqueue_service_pb2
from google.appengine.runtime import apiproxy_errors
from google.appengine.runtime.context import ctx_test_util
import mox
import six
from six.moves import range
from six.moves import zip

from absl.testing import absltest










InvalidEtaError = taskqueue.InvalidEtaError
InvalidTaskError = taskqueue.InvalidTaskError
TaskRetryOptions = taskqueue.TaskRetryOptions
Task = taskqueue.Task
Queue = taskqueue.Queue
QueueStatistics = taskqueue.QueueStatistics
TaskQueueServiceError = taskqueue_service_pb2.TaskQueueServiceError
parse_relative_url = taskqueue._parse_relative_url
determine_eta_posix = taskqueue.Task._Task__determine_eta_posix
flatten_params = taskqueue._flatten_params
convert_payload = taskqueue.Task._Task__convert_payload
_RelativeUrlError = taskqueue._RelativeUrlError
DEFAULT_HOSTNAME = 'app-id.appsplot.com'
_base_headers = {'X-AppEngine-Current-Namespace': '',
                 'Host': DEFAULT_HOSTNAME}



class _AustraliaBrisbaneTimeZone(datetime.tzinfo):
  """Australia/Brisbane timezone."""

  TEN_HOURS = datetime.timedelta(hours=10)

  def utcoffset(self, dt):
    return self.TEN_HOURS

  def dst(self, dt):
    return self.TEN_HOURS

  def tzname(self, dt):
    return 'Australia/Brisbane'


_AustraliaBrisbane = _AustraliaBrisbaneTimeZone()


def SecToUsec(sec):
  seconds_in_usec = 1000000
  return int(sec * seconds_in_usec)


def _InitAddRequest(bulk_add_request):
  """Adds a new add_request and initializes standard headers."""
  add_request = bulk_add_request.add_request.add()
  for key, value in _base_headers.items():
    header = add_request.header.add()
    header.key = key.encode('utf8')
    header.value = value.encode('utf8')
  return add_request


class EqualsProto(mox.Comparator):
  """Mox comparator that compares protos.

  This comparator will output the ascii version of the proto when repr-ed.
  """

  def __init__(self, expected):
    self._expected = expected

  def equals(self, rhs):
    return self._expected.Equals(rhs)

  def __repr__(self):
    return 'EqualsProto<%s>' % (self._expected.ToShortASCII())


class MockRPC(object):
  """Mock for system RPC."""

  def __init__(self,
               service,
               stubs,
               expected_request=None,
               populate_response=None):
    """Constructor for the MockRPC object.

    Args:
      service: The name of the service for the RPC.
      stubs: An APIProxyStubMap.
      expected_request: The anticipated request protobuf (or a Comparator).
      populate_response: Function populating the RPC response.
    """
    assert isinstance(stubs, apiproxy_stub_map.APIProxyStubMap)
    self.service = service
    self._expected_request = expected_request
    self._populate_response = populate_response
    self.state = apiproxy_rpc.RPC.IDLE

  def MakeCall(self, service, method, request, response):
    """Check the actual RPC request against the expected request."""
    assert self.service == service
    if self._expected_request is not None:
      assert self._expected_request == request

    self.method = method
    self.request = request
    self.response = response
    self.state = apiproxy_rpc.RPC.RUNNING

  def Wait(self):
    """Complete immediately."""
    self.state = apiproxy_rpc.RPC.FINISHING

  def CheckSuccess(self):
    """Populate the RPC response."""
    if self._populate_response is not None:
      self._populate_response(self.service,
                              self.method,
                              self.request,
                              self.response)


class TaskQueueBulkAddRequestComparator(mox.Comparator):
  """Mox comparator for TaskQueueBulkAddRequest that ignores header order."""

  def __init__(self, expected):
    self._expected = expected

  def SameTask(self, x, y):

    headers_x = {}
    for header in x.header:
      headers_x[header.key] = header.value
    headers_y = {}
    for header in y.header:
      headers_y[header.key] = header.value
    if headers_x != headers_y:
      return False


    z = taskqueue_service_pb2.TaskQueueAddRequest()
    z.MergeFrom(y)
    z.ClearField('header')
    for header in x.header:
      z.header.add().MergeFrom(header)


    return x == z

  def equals(self, rhs):
    return ((len(self._expected.add_request) == len(rhs.add_request)) and all(
        self.SameTask(x, y)
        for x, y in zip(self._expected.add_request, rhs.add_request)))

  def __repr__(self):
    return 'TaskQueueBulkAddRequestComparator<%s>' % (str(self._expected))


class HttpEnvironTest(absltest.TestCase):

  def setUp(self):
    os.environ['DEFAULT_VERSION_HOSTNAME'] = DEFAULT_HOSTNAME
    os.environ['HTTP_HOST'] = DEFAULT_HOSTNAME


class HelpersTest(absltest.TestCase):
  """Tests for the taskqueue module's helper methods."""

  def testCreateRpc(self):
    """Tests create_rpc() function."""
    mocker = mox.Mox()
    mocker.StubOutWithMock(apiproxy_stub_map, 'CreateRPC')
    apiproxy_stub_map.CreateRPC('taskqueue',
                                mox.IgnoreArg()).WithSideEffects(MockRPC)
    try:
      mocker.ReplayAll()
      rpc = taskqueue.create_rpc()
      mocker.VerifyAll()
    finally:
      mocker.UnsetStubs()
      mocker.ResetAll()

    self.assertIsInstance(rpc, apiproxy_stub_map.UserRPC)
    self.assertEqual(rpc.deadline, None)
    self.assertEqual(rpc.callback, None)

  def testParseRelativeUrl(self):
    """Tests the __parse_relative_url method."""
    path, query = parse_relative_url('/foo/baz?one=two&three=four')
    self.assertEqual('/foo/baz', path)
    self.assertEqual('one=two&three=four', query)

    self.assertRaises(_RelativeUrlError, parse_relative_url, '')
    self.assertRaises(
        _RelativeUrlError, parse_relative_url, 'http://example.com/blah')
    self.assertRaises(
        _RelativeUrlError, parse_relative_url, '//example.com/blah')
    self.assertRaises(
        _RelativeUrlError, parse_relative_url,
        '/foo/baz?one=two&three=four#fragment')
    self.assertRaises(
        _RelativeUrlError, parse_relative_url,
        'foo/baz?one=two&three=four')

  def testDetermineEtaPosix(self):
    """Tests the __determine_eta_posix method."""
    now_timestamp = time.time()

    if six.PY3:
      now_timestamp = round(now_timestamp, 6)
    now_time = datetime.datetime.fromtimestamp(now_timestamp)
    now_brisbanetime = now_time.replace(tzinfo=_AustraliaBrisbane)
    current_time = lambda: now_timestamp
    countdown = 30.4
    future_time = now_timestamp + countdown
    future_time2 = now_timestamp + int(countdown)

    self.assertEqual(
        now_timestamp,
        determine_eta_posix(countdown=0, current_time=current_time))
    self.assertEqual(now_timestamp, determine_eta_posix(eta=now_time))
    self.assertEqual(now_timestamp - 10 * 3600,
                     determine_eta_posix(eta=now_brisbanetime))
    self.assertEqual(now_timestamp,
                     determine_eta_posix(current_time=current_time))

    self.assertEqual(
        future_time,
        determine_eta_posix(countdown=countdown, current_time=current_time))
    self.assertEqual(
        future_time,
        determine_eta_posix(
            countdown=str(countdown), current_time=current_time))
    self.assertEqual(
        future_time2,
        determine_eta_posix(
            countdown=int(countdown), current_time=current_time))
    self.assertEqual(
        future_time2,
        determine_eta_posix(
            countdown=int(countdown), current_time=current_time))

    self.assertRaises(
        InvalidTaskError, determine_eta_posix,
        datetime.datetime.now(), 30)
    self.assertRaises(
        InvalidTaskError, determine_eta_posix,
        datetime.date.today(), None)
    self.assertRaises(
        InvalidTaskError, determine_eta_posix,
        None, 'asdf')
    self.assertRaises(
        InvalidTaskError, determine_eta_posix,
        None, 10**1000)

  def testFlattenParams(self):
    """Tests the __flatten_params method."""
    params = {
        'one': 'two',
        'three': ('four', 'five'),
        u'\xfcmlaut': 'six',
        'seven': [8, 9.0, 10],
        'eleven': 11,
        'twelve': 12,
        'thirteen': 13.123,
    }
    expected = [
        (b'one', b'two'),
        (b'three', b'four'),
        (b'three', b'five'),
        (b'\xc3\xbcmlaut', b'six'),
        (b'seven', b'8'),
        (b'seven', b'9.0'),
        (b'seven', b'10'),
        (b'eleven', b'11'),
        (b'twelve', b'12'),
        (b'thirteen', b'13.123'),
    ]
    self.assertCountEqual(expected, flatten_params(params))
    self.assertEqual([], flatten_params({}))
    self.assertEqual([], flatten_params({'stuff': []}))

  def testConvertPayload(self):
    """Tests the __convert_payload method."""
    headers = {}
    self.assertEqual(b'\xc3\xbcmlaut', convert_payload(u'\xfcmlaut', headers))
    self.assertEqual({'content-type': 'text/plain; charset=utf-8'}, headers)

    headers.clear()
    self.assertEqual(b'stuff', convert_payload(b'stuff', headers))
    self.assertEqual({}, headers)

    self.assertRaises(
        InvalidTaskError, convert_payload,
        object(), headers)
    self.assertRaises(
        InvalidTaskError, convert_payload,
        1, headers)


class TaskRetryOptionsTest(absltest.TestCase):
  """Tests for the TaskRetryOptionsTest class."""

  def testNoFieldsSet(self):
    options = TaskRetryOptions()
    self.assertEqual(None, options.min_backoff_seconds)
    self.assertEqual(None, options.max_backoff_seconds)
    self.assertEqual(None, options.max_doublings)
    self.assertEqual(None, options.task_retry_limit)
    self.assertEqual(None, options.task_age_limit)

  def testSetAllFields(self):
    options = TaskRetryOptions(min_backoff_seconds=3,
                               max_backoff_seconds=5,
                               max_doublings=8,
                               task_retry_limit=10,
                               task_age_limit=600)
    self.assertEqual(3, options.min_backoff_seconds)
    self.assertEqual(5, options.max_backoff_seconds)
    self.assertEqual(8, options.max_doublings)
    self.assertEqual(10, options.task_retry_limit)
    self.assertEqual(600, options.task_age_limit)

  def testIllegalConstructorArgument(self):
    self.assertRaises(TypeError,
                      TaskRetryOptions,
                      min_backoff_seconds=1,
                      max_backoff_seconds=5,
                      foo=23)

  def testNegativeMinBackoffSeconds(self):
    self.assertRaises(taskqueue.InvalidTaskRetryOptionsError,
                      TaskRetryOptions,
                      min_backoff_seconds=-1)

  def testNegativeMaxBackoffSeconds(self):
    self.assertRaises(taskqueue.InvalidTaskRetryOptionsError,
                      TaskRetryOptions,
                      max_backoff_seconds=-5)

  def testMinBackoffLessThanMaxBackoffSeconds(self):
    self.assertRaises(taskqueue.InvalidTaskRetryOptionsError,
                      TaskRetryOptions,
                      min_backoff_seconds=5,
                      max_backoff_seconds=3)

  def testNegativeMaxDoublings(self):
    self.assertRaises(taskqueue.InvalidTaskRetryOptionsError,
                      TaskRetryOptions,
                      max_doublings=-1)

  def testNegativeTaskRetryLimit(self):
    self.assertRaises(taskqueue.InvalidTaskRetryOptionsError,
                      TaskRetryOptions,
                      task_retry_limit=-1)

  def testNegativeTaskAgeLimit(self):
    self.assertRaises(taskqueue.InvalidTaskRetryOptionsError,
                      TaskRetryOptions,
                      task_age_limit=-1)


class TaskTest(HttpEnvironTest):
  """Tests for the Task class."""

  def setUp(self):
    """Sets up the test harness."""
    HttpEnvironTest.setUp(self)
    self.payload = b'this is the example payload'
    self.unicode_payload = u'\xfcmlauts are fun'
    self.encoded_payload = b'\xc3\xbcmlauts are fun'
    self.params = {
        'one$funny&': 'fish',
        'red': 'blue with spaces',
        'fish': ['guppy', 'flounder'],
    }
    self.params_query = ('one%24funny%26=fish&fish=guppy&fish=flounder'
                         '&red=blue+with+spaces')


    self.now_timestamp = time.time()
    self.now_time = datetime.datetime.fromtimestamp(self.now_timestamp)
    self.now_utctime = self.now_time.replace(tzinfo=taskqueue._UTC)
    self.old_determine_eta_posix = staticmethod(
        getattr(Task, '_Task__determine_eta_posix'))

    @staticmethod
    def new_determine_eta_posix(eta, countdown):
      return determine_eta_posix(eta, countdown,
                                 current_time=lambda: self.now_timestamp)
    setattr(Task, '_Task__determine_eta_posix', new_determine_eta_posix)

  def tearDown(self):
    """Tears down the test harness."""
    setattr(Task, '_Task__determine_eta_posix', self.old_determine_eta_posix)
    HttpEnvironTest.tearDown(self)

  def assertParamsEqual(self, expected, actual):
    self.assertSetEqual(set(expected.split('&')), set(actual.split('&')))

  def testNotEnqueued(self):
    """Tests that the enqueued attribute is False after initialization."""
    t = Task()
    self.assertFalse(t.was_enqueued)

  def testPayloadData(self):
    """Tests a Task with a method that has a body."""
    t = Task(self.payload)
    self.assertEqual('POST', t.method)
    self.assertEqual(self.payload, t.payload)
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual('', t.url)
    self.assertEqual(None, t.name)

  def testEmptyPayload(self):
    """Tests a Task with a body-allowed method but an empty payload."""
    t = Task('')
    self.assertEqual('POST', t.method)
    self.assertEqual(b'', t.payload)
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual('', t.url)
    self.assertEqual(None, t.name)

  def testNoPayload(self):
    """Tests creating a task without any payload at all."""
    t = Task()
    self.assertEqual('POST', t.method)
    self.assertEqual(None, t.payload)
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual('', t.url)
    self.assertEqual(None, t.name)

  def testPostParameters(self):
    """Tests a Task with a POST method and form parameters."""
    t = Task(params=self.params)
    self.assertEqual('POST', t.method)
    self.assertParamsEqual(self.params_query, t.payload)
    expected_headers = _base_headers.copy()
    expected_headers['content-type'] = 'application/x-www-form-urlencoded'
    self.assertEqual(expected_headers, t.headers)
    self.assertEqual('', t.url)
    self.assertEqual(None, t.name)

  def testPullParameters(self):
    """Tests a Task with a POST method and form parameters."""
    t = Task(params=self.params, method='PULL')
    self.assertEqual('PULL', t.method)
    self.assertParamsEqual(self.params_query, t.payload.decode('utf8'))
    self.assertEqual(None, t.name)

  def testUnicodePayload(self):
    """Tests that unicode text is properly encoded in Task bodies."""
    t = Task(self.unicode_payload)
    self.assertEqual('POST', t.method)
    self.assertEqual(self.encoded_payload, t.payload)
    expected_headers = _base_headers.copy()
    expected_headers['content-type'] = 'text/plain; charset=utf-8'
    self.assertEqual(expected_headers, t.headers)

    self.assertEqual('', t.url)
    self.assertEqual(None, t.name)

  def testNonStringPayload(self):
    """Tests that non-string payloads will cause an error."""
    self.assertRaises(
        InvalidTaskError, Task,
        object())
    self.assertRaises(
        InvalidTaskError, Task,
        1)
    self.assertRaises(
        InvalidTaskError, Task,
        ['list', 'of', 'strings'])

  def testPostParamsAndBodyError(self):
    """Tests when a POST Task has parameters and a body payload."""
    self.assertRaises(
        InvalidTaskError, Task,
        self.payload, params=self.params)

  def testPostQueryStringInUrlError(self):
    """Tests that a query string showing up for a POST request will error."""
    self.assertRaises(
        InvalidTaskError, Task,
        url='/path/to/my/stuff?foo=bar')

  def testParamsAndBodyOkay(self):
    """Tests when a Task with parameters and a body is okay."""
    t = Task(self.payload, params=self.params, method='PUT')
    self.assertEqual('PUT', t.method)
    self.assertEqual('?', t.url[0])
    self.assertParamsEqual(self.params_query, t.url[1:])
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual(self.payload, t.payload)
    self.assertEqual(None, t.name)

  def testGetUrlHasQuery(self):
    """Tests a Task with a specified path that has a query string."""
    url = '/path/with?' + self.params_query
    t = Task(url=url, method='GET')
    self.assertEqual('GET', t.method)
    self.assertEqual(url, t.url)
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual(None, t.payload)
    self.assertEqual(None, t.name)

  def testGetUrlWithParams(self):
    """Tests a Task for getting a path with additional parameters."""
    t = Task(url='/path/with', params=self.params, method='GET')
    self.assertEqual('GET', t.method)
    self.assertEqual('/path/with?', t.url[0:11])
    self.assertParamsEqual(self.params_query, t.url[11:])
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual(None, t.payload)
    self.assertEqual(None, t.name)

  def testGetHasQueryAndParamsError(self):
    """Tests when a GET Task has a query string and parameters specified."""
    self.assertRaises(
        InvalidTaskError, Task,
        url='/path/with?' + self.params_query, method='GET', params=self.params)

  def testNonPayloadMethods(self):
    """Tests when a non-payload methods have a request body."""
    for method in ('DELETE', 'HEAD', 'GET'):
      self.assertRaises(
          InvalidTaskError, Task,
          'my payload', method=method)

  def testDefaultUrl(self):
    """Tests that a default URL will be empty if only the name is specified."""
    t = Task(name='mycooltask')
    self.assertEqual('POST', t.method)
    self.assertEqual(None, t.payload)
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual('', t.url)
    self.assertEqual('mycooltask', t.name)

  def testDefaultUrlWithGetParams(self):
    """Tests assigning a default URL with GET params."""
    t = Task(name='mycooltask', params=self.params, method='GET')
    self.assertEqual('GET', t.method)
    self.assertEqual(None, t.payload)
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual('?', t.url[0])
    self.assertParamsEqual(self.params_query, t.url[1:])
    self.assertEqual('mycooltask', t.name)

  def testDefaultUrlWithoutGetParams(self):
    """Tests assigning a default URL without GET params."""
    t = Task(name='mycooltask', method='GET')
    self.assertEqual('GET', t.method)
    self.assertEqual(None, t.payload)
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual('', t.url)
    self.assertEqual('mycooltask', t.name)

  def testUrlAndNameError(self):
    """Tests when a Task has a name and a URL assigned."""
    t = Task(name='mycooltask', url='/my_fun_url')
    self.assertEqual('POST', t.method)
    self.assertEqual(None, t.payload)
    self.assertEqual(_base_headers, t.headers)
    self.assertEqual('/my_fun_url', t.url)
    self.assertEqual('mycooltask', t.name)

  def testHeaders(self):
    """Tests a Task's request headers and that they will override defaults."""
    expected = self.params.copy()
    expected.update(_base_headers)
    expected['content-type'] = 'text/plain; charset=utf-8'
    t = Task(self.unicode_payload, headers=self.params)
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)

    expected = self.params.copy()
    expected.update(_base_headers)
    expected['content-type'] = 'do not override'
    t = Task(self.unicode_payload, headers=expected)
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)

  def testHeaderCapitalization(self):
    """Tests that any header capitalization is allowed."""
    expected = self.params.copy()
    expected.update(_base_headers)
    expected['CoNtEnT-TyPe'] = 'do not override'
    t = Task(self.unicode_payload, headers=expected)
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)

  def testTargetParameter(self):
    """Tests that the target parameter creates a 'Host' header."""
    expected = self.params.copy()
    expected.update(_base_headers)
    expected['content-type'] = 'text/plain; charset=utf-8'
    expected['Host'] = '%s.%s' % ('2', DEFAULT_HOSTNAME)
    t = Task(self.unicode_payload, headers=self.params, target='2')
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)
    self.assertEqual('2', t.target)

  def testTargetParameterDevAppserver(self):
    """Tests that the target parameter creates a 'Host' header."""
    local_module_hostname = 'localhost:8081'

    def SetHostnameResponse(service, method, request, response):
      response.hostname = local_module_hostname

    os.environ['SERVER_SOFTWARE'] = 'Development/2.0'
    mocker = mox.Mox()
    mocker.StubOutWithMock(apiproxy_stub_map, 'CreateRPC')
    apiproxy_stub_map.CreateRPC('modules', mox.IgnoreArg()).WithSideEffects(
        functools.partial(
            MockRPC,
            populate_response=SetHostnameResponse))
    try:
      mocker.ReplayAll()
      t = Task(self.unicode_payload, headers=self.params, target='2')
      mocker.VerifyAll()
    finally:
      mocker.UnsetStubs()
      mocker.ResetAll()

    expected = self.params.copy()
    expected.update(_base_headers)
    expected['content-type'] = 'text/plain; charset=utf-8'
    expected['Host'] = local_module_hostname
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)
    self.assertEqual('2', t.target)

  def testTargetParameterDevAppserver_VersionOnly(self):
    local_module_hostname = 'localhost:8081'

    os.environ['SERVER_SOFTWARE'] = 'Development/2.0'
    mocker = mox.Mox()
    mocker.StubOutWithMock(apiproxy_stub_map, 'CreateRPC')

    def SetHostnameResponse(service, method, request, response):
      if request.version and request.module:
        response.hostname = local_module_hostname
      else:
        raise apiproxy_errors.ApplicationError(
            modules_service_pb2.ModulesServiceError.INVALID_MODULE)


    apiproxy_stub_map.CreateRPC('modules', mox.IgnoreArg()).WithSideEffects(
        functools.partial(
            MockRPC,
            populate_response=SetHostnameResponse))


    apiproxy_stub_map.CreateRPC('modules', mox.IgnoreArg()).WithSideEffects(
        functools.partial(
            MockRPC,
            populate_response=SetHostnameResponse))

    try:
      mocker.ReplayAll()
      t = Task(self.unicode_payload, headers=self.params, target='2')
      mocker.VerifyAll()
    finally:
      mocker.UnsetStubs()
      mocker.ResetAll()

    expected = self.params.copy()
    expected.update(_base_headers)
    expected['content-type'] = 'text/plain; charset=utf-8'
    expected['Host'] = local_module_hostname
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)
    self.assertEqual('2', t.target)

  def testTargetParameterDevAppserver_InvalidModule(self):
    os.environ['SERVER_SOFTWARE'] = 'Development/2.0'
    mocker = mox.Mox()
    mocker.StubOutWithMock(apiproxy_stub_map, 'CreateRPC')

    def RaiseInvalidModule(service, method, request, response):
      raise apiproxy_errors.ApplicationError(
          modules_service_pb2.ModulesServiceError.INVALID_MODULE)


    apiproxy_stub_map.CreateRPC('modules', mox.IgnoreArg()).WithSideEffects(
        functools.partial(
            MockRPC,
            populate_response=RaiseInvalidModule))

    try:
      mocker.ReplayAll()
      self.assertRaises(modules.InvalidModuleError, Task, self.unicode_payload,
                        headers=self.params, target='2.mymodule')
      mocker.VerifyAll()
    finally:
      mocker.UnsetStubs()
      mocker.ResetAll()

  def testTargetFromHostHeader(self):
    """Tests that a 'Host' header sets the target parameter."""
    host_header = '%s.%s' % ('2', DEFAULT_HOSTNAME)
    expected = _base_headers.copy()
    expected['content-type'] = 'text/plain; charset=utf-8'
    expected['Host'] = host_header
    t = Task(self.unicode_payload,
             headers={'Host': host_header})
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)
    self.assertEqual('2', t.target)

  def testTargetFromDefaultHostHeader(self):
    """Tests that the default app version sets the target parameter."""
    expected = _base_headers.copy()
    expected['content-type'] = 'text/plain; charset=utf-8'
    expected['Host'] = DEFAULT_HOSTNAME
    t = Task(self.unicode_payload,
             headers={'Host': DEFAULT_HOSTNAME})
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)
    self.assertEqual(taskqueue.DEFAULT_APP_VERSION, t.target)

  def testTargetFromCurrentHostname(self):
    """."""
    expected = _base_headers.copy()
    expected['content-type'] = 'text/plain; charset=utf-8'
    expected['Host'] = DEFAULT_HOSTNAME
    t = Task(self.unicode_payload)
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)
    self.assertEqual(taskqueue.DEFAULT_APP_VERSION, t.target)

  def testTargetFromCurrentHostnameNonDefaultVersion(self):
    """."""
    host_header = '%s.%s' % ('2', DEFAULT_HOSTNAME)
    os.environ['HTTP_HOST'] = host_header
    expected = _base_headers.copy()
    expected['content-type'] = 'text/plain; charset=utf-8'
    expected['Host'] = host_header
    t = Task(self.unicode_payload)
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)
    self.assertEqual('2', t.target)

  def testTargetParameterAndHostHeader(self):
    """Tests that the target parameter can not be used with a 'Host' header."""
    self.assertRaises(
        InvalidTaskError,
        Task, target='2', headers={'host': 'ignored'})

  def testTargetParameterWithDefault(self):
    """Tests that the target parameter creates a 'Host' header."""
    expected = self.params.copy()
    expected.update(_base_headers)
    expected['content-type'] = 'text/plain; charset=utf-8'
    expected['Host'] = DEFAULT_HOSTNAME
    t = Task(self.unicode_payload, headers=self.params,
             target=taskqueue.DEFAULT_APP_VERSION)
    self.assertEqual('POST', t.method)
    self.assertEqual(expected, t.headers)
    self.assertEqual(taskqueue.DEFAULT_APP_VERSION, t.target)

  def testMethodCapitalization(self):
    """Tests that any method capitalization is allowed."""
    t = Task(method='GeT')
    self.assertEqual('GET', t.method)

  def testBadMethod(self):
    """Tests when an invalid method is specified."""
    self.assertRaises(
        InvalidTaskError, Task,
        method='stuff')

  def testTag(self):
    """Tests with a Task with a tag."""
    tags = [None, '', 'My test Tag', u'\u30cb\u30e3\u30f3', '\x00\x01\x02\x03']
    for tag in tags:
      t = Task(method='PULL', payload='data', tag=tag)
      self.assertEqual(tag, t.tag)

  def testTagwithNonPullQueue(self):
    """Tests with a Task with a tag."""
    for method in ['GET', 'POST', 'HEAD', 'PUT', 'DELETE']:
      self.assertRaises(
          InvalidTaskError,
          Task, method=method, params={'test': 'data'}, tag='a tag')
      Task(method=method, params={'test': 'data'})

  def testCountdown(self):
    """Tests specifying a countdown for a Task."""
    t = Task(countdown=15)
    self.assertEqual(self.now_utctime + datetime.timedelta(seconds=15), t.eta)

  def testEta(self):
    """Tests specifying an explicit ETA for a Task."""
    self.now_timestamp += 15
    self.now_time += datetime.timedelta(seconds=15)
    t = Task(eta=self.now_time)
    self.assertEqual(self.now_utctime + datetime.timedelta(seconds=15), t.eta)

  def testDefaultEta(self):
    """Test that the default ETA is the current time."""
    t = Task()
    self.assertEqual(self.now_utctime, t.eta)

  def testRetryOptions(self):
    """Tests specifying TaskRetryOptions for a Task."""
    retry_options = TaskRetryOptions(min_backoff_seconds=1,
                                     max_backoff_seconds=2)
    t = Task(retry_options=retry_options)
    self.assertEqual(retry_options, t.retry_options)

  def testMaxTaskSize(self):
    """Tests the max allowed size of a Task."""
    self.assertRaises(
        taskqueue.TaskTooLargeError, Task,
        'a' * (taskqueue.MAX_TASK_SIZE_BYTES + 1))
    self.assertRaises(
        taskqueue.TaskTooLargeError, Task,
        'a' * (taskqueue.MAX_PULL_TASK_SIZE_BYTES + 1), method='PULL')
    self.assertRaises(
        taskqueue.TaskTooLargeError, Task,
        'a' * (taskqueue.MAX_PUSH_TASK_SIZE_BYTES + 1))

  def testMaxNameLength(self):
    """Tests the max allowed length of a Task name."""
    self.assertRaises(
        taskqueue.InvalidTaskNameError, Task,
        name=('a' * (taskqueue.MAX_TASK_NAME_LENGTH + 1)))

  def testDefaultDispatchDeadline(self):
    """Tests the default dispatch deadline is None."""
    t = Task()
    self.assertIsNone(t.dispatch_deadline_usec)

  def testDispatchDeadlineType(self):
    """Tests dispatch deadline type must be a number."""
    self.assertRaises(TypeError, Task, dispatch_deadline_usec='a')

  def testMaxDispatchDeadline(self):
    """Tests the maximum allowed dispatch deadline for a Task."""
    self.assertRaises(
        taskqueue.InvalidDispatchDeadlineError,
        Task,

        dispatch_deadline_usec=int(
            datetime.timedelta(hours=24, seconds=1).total_seconds() * 1000000))

  def testMinDispatchDeadline(self):
    """Tests the minimum allowed dispatch deadline for a Task."""
    self.assertRaises(
        taskqueue.InvalidDispatchDeadlineError,
        Task,

        dispatch_deadline_usec=14999999)

  def testNamePattern(self):
    """Tests the task name must match a pattern."""
    self.assertRaises(taskqueue.InvalidTaskNameError, Task, name='ba.d')
    self.assertRaises(taskqueue.InvalidTaskNameError, Task, name='ba/d')
    self.assertRaises(taskqueue.InvalidTaskNameError, Task, name='ba$d.')
    Task(name='good')
    Task(name='GooD')
    Task(name='Go-oD')
    Task(name='Go_oD')
    Task(name='-GooD')
    Task(name='GooD-')
    Task(name='1234')
    Task(name='1234-foo')

  def testMaxRelativeUrlLength(self):
    """Tests the max allowed length of the Task URL."""
    self.assertRaises(
        taskqueue.InvalidUrlError, Task,
        url='/' + ('a' * (taskqueue.MAX_URL_LENGTH)))

  def testInvalidCountdown(self):
    """Tests when the task countdown is invalid."""
    self.assertRaises(
        taskqueue.InvalidEtaError, Task,
        countdown=(3600 * 24 * 30 + 300))
    Task(countdown=(3600 * 24 * 30))

  def testInvalidUrl(self):
    """Tests when the task URL is invalid."""
    self.assertRaises(
        taskqueue.InvalidUrlError, Task,
        url='asdf')

  def testBadKeywordArgument(self):
    """Tests that unknown keyword arguments will raise an error.

    This prevents bozo typos like 'parmas' from breaking user code.
    """
    self.assertRaises(
        TypeError, Task, parmas=self.params)

  def testSize(self):
    """Tests the size method."""
    t = Task(b'mypayload',
             headers={'one': 'two', 'three': 'four'},
             url='/foo/bar/baz',
             params={'seven': 'eleven', 'must be': 'esca&ped'},
             method='PUT')
    all_data = (
        'mypayload' + 'one: two\r\n' + 'three: four\r\n' +
        'X-AppEngine-Current-Namespace: \r\n' +
        'Host: app-id.appsplot.com\r\n' +
        '/foo/bar/baz?seven=eleven&must+be=escap%26ed' + 'PUT'
    )
    self.assertLen(all_data, t.size)

  def testExtractParamsGet(self):
    """Tests extract_params with a GET method."""
    params = {'names': [b'brian', b'nick'], 'must be': b'esca&ped'}
    t = Task(url='/foo/bar/baz',
             params=params,
             method='GET')
    self.assertEqual(params, t.extract_params())

  def testExtractParamsGetNoQuery(self):
    """Tests extract_params with a GET method and no query present."""
    t = Task(url='/foo/bar/baz',
             method='GET')
    self.assertEqual({}, t.extract_params())

  def testExtractParamsGetEmptyQuery(self):
    """Tests extract_params with a GET method whose URL ends with ?."""
    t = Task(url='/foo/bar/baz?',
             method='GET')
    self.assertEqual({}, t.extract_params())

  def testExtractParamsGetBadQuery(self):
    """Tests extract_params with a GET method and an invalid query present."""
    t = Task(url='/foo/bar/baz?foo',
             method='GET')
    self.assertRaises(ValueError, t.extract_params)

  def testExtractParamsPost(self):
    """Tests extract_params with a POST method."""
    params = {'names': [b'brian', b'nick'], 'must be': b'esca&ped'}
    t = Task(url='/foo/bar/baz',
             params=params,
             method='POST')
    self.assertEqual(params, t.extract_params())

  def testExtractParamsPostNoQuery(self):
    """Tests extract_params with a POST method and no query present."""
    t = Task(url='/foo/bar/baz',
             method='POST')
    self.assertEqual({}, t.extract_params())

  def testExtractParamsPostBadQuery(self):
    """Tests extract_params with a POST method and an invalid query present."""
    t = Task('foo',
             url='/foo/bar/baz',
             method='POST')
    self.assertRaises(ValueError, t.extract_params)

  def testExtractParamsUnicodeQuery(self):
    """Tests extract_params returns encoded strings and not Unicode."""
    t = Task(url='/foo/bar/baz',
             params={'money': u'\N{EURO SIGN}'},
             method='GET')
    self.assertEqual({'money': u'\N{EURO SIGN}'.encode('utf-8')},
                     t.extract_params())

  def testExtractParamsValueCached(self):
    """Tests extract_params returns encoded strings and not Unicode."""
    t = Task(url='/foo/bar/baz',
             params={'money': u'\N{EURO SIGN}'},
             method='GET')
    self.assertEqual({'money': u'\N{EURO SIGN}'.encode('utf-8')},
                     t.extract_params())

  def testQueueNameNone(self):
    """Tests that the queue name is None if the task has not been added/read
       from a queue."""
    t = Task(url='/foo/bar')
    self.assertIsNone(t.queue_name)


class DeleteTasksTest(absltest.TestCase):
  """Tests for Queue.delete_tasks method."""

  def setUp(self):
    """Sets up the test harness."""
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.mox = mox.Mox()
    self.mox.StubOutWithMock(apiproxy_stub_map.apiproxy,
                             'MakeSyncCall')
    self.mox.StubOutWithMock(apiproxy_stub_map, 'UserRPC')

  def tearDown(self):
    """Tears down the test harness."""
    self.mox.ResetAll()
    self.mox.UnsetStubs()

  def DeleteTasks(self, queue, tasks):
    """Exercise the synchronous method delete_tasks."""
    return queue.delete_tasks(tasks)

  def MockSuccessfulRPC(self, expected_request, populate_response):
    """Mock an asynchronous Delete call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC result available to the caller."""
      populate_response('taskqueue', method, request, response)

      rpc.response = response
      rpc.get_result = lambda: get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('Delete',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success()

  def testDeleteSingleTask(self):
    """Tests deleting one task."""

    def SetResponse(service, method, request, response):
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)

    task_name = 'task1'
    expected_request = taskqueue_service_pb2.TaskQueueDeleteRequest()
    expected_request.queue_name = b'default'
    expected_request.task_name.append(task_name.encode('utf8'))

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    task = Task(name=task_name)
    task = self.DeleteTasks(Queue('default'), task)
    self.mox.VerifyAll()

    self.assertTrue(task.was_deleted)

  def testDeleteListOfTasks(self):
    """Tests deleting a list of tasks."""

    def SetResponse(service, method, request, response):
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)

    task_name_one = 'task1'
    task_name_two = 'task2'
    task_name_three = 'task3'
    expected_request = taskqueue_service_pb2.TaskQueueDeleteRequest()
    expected_request.queue_name = b'default'
    expected_request.task_name.append(task_name_one.encode('utf8'))
    expected_request.task_name.append(task_name_two.encode('utf8'))
    expected_request.task_name.append(task_name_three.encode('utf8'))

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    task1 = Task(name=task_name_one)
    task2 = Task(name=task_name_two)
    task3 = Task(name=task_name_three)
    tasks = [task1, task2, task3]
    tasks = self.DeleteTasks(Queue('default'), tasks)
    self.mox.VerifyAll()

    self.assertLen(tasks, 3)
    self.assertTrue(tasks[0].was_deleted)
    self.assertTrue(tasks[1].was_deleted)
    self.assertTrue(tasks[2].was_deleted)

  def testDeleteTombstonedTaskError(self):
    """Tests TombstonedTaskError returned from MakeSyncCall."""

    def SetResponse(service, method, request, response):
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)
      response.result.append(
          taskqueue_service_pb2.TaskQueueServiceError.TOMBSTONED_TASK)
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)

    task_name_one = 'task1'
    task_name_two = 'isTombstoned'
    task_name_three = 'task3'
    expected_request = taskqueue_service_pb2.TaskQueueDeleteRequest()
    expected_request.queue_name = b'default'
    expected_request.task_name.append(task_name_one.encode('utf8'))
    expected_request.task_name.append(task_name_two.encode('utf8'))
    expected_request.task_name.append(task_name_three.encode('utf8'))

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    task1 = Task(name=task_name_one)
    task2 = Task(name=task_name_two)
    task3 = Task(name=task_name_three)
    tasks = [task1, task2, task3]
    tasks = self.DeleteTasks(Queue('default'), tasks)
    self.mox.VerifyAll()

    self.assertTrue(tasks[0].was_deleted)
    self.assertFalse(tasks[1].was_deleted)
    self.assertTrue(tasks[2].was_deleted)

  def testDeleteTwice(self):
    """Tests deleting a list of tasks twice."""

    def SetResponse(service, method, request, response):
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)

    task_name_one = 'task1'
    task_name_two = 'T2'
    task_name_three = 't-three'
    expected_request = taskqueue_service_pb2.TaskQueueDeleteRequest()
    expected_request.queue_name = b'default'
    expected_request.task_name.append(task_name_one.encode('utf8'))
    expected_request.task_name.append(task_name_two.encode('utf8'))
    expected_request.task_name.append(task_name_three.encode('utf8'))

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    task1 = Task(name=task_name_one)
    task2 = Task(name=task_name_two)
    task3 = Task(name=task_name_three)
    tasks = [task1, task2, task3]
    tasks = self.DeleteTasks(Queue('default'), tasks)
    self.mox.VerifyAll()

    self.assertRaises(taskqueue.BadTaskStateError,
                      self.DeleteTasks,
                      Queue('default'),
                      tasks)

  def testDeleteNoTaskName(self):
    """Tests deleting tasks that have no name specified."""
    task1 = Task()
    tasks = [task1]

    self.assertRaises(taskqueue.BadTaskStateError,
                      self.DeleteTasks,
                      Queue('default'),
                      tasks)

  def testDeleteDuplicateTaskNames(self):
    """Tests deleting list of duplicate task names."""

    task1 = Task(name='T1')
    task2 = Task(name='T2')
    task3 = Task(name='T1')
    tasks = [task1, task2, task3]

    self.assertRaises(taskqueue.DuplicateTaskNameError,
                      self.DeleteTasks,
                      Queue('default'),
                      tasks)

  def testDeleteNonExistingTask(self):
    """Tests deleting a task that does not exist."""

    def SetResponse(service, method, request, response):
      response.result.append(TaskQueueServiceError.OK)
      response.result.append(TaskQueueServiceError.UNKNOWN_TASK)

    task_name_one = 'task1'
    task_name_two = 'task2'
    expected_request = taskqueue_service_pb2.TaskQueueDeleteRequest()
    expected_request.queue_name = b'default'
    expected_request.task_name.append(task_name_one.encode('utf8'))
    expected_request.task_name.append(task_name_two.encode('utf8'))

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    task1 = Task(name=task_name_one)
    task2 = Task(name=task_name_two)
    tasks = [task1, task2]
    tasks = self.DeleteTasks(Queue('default'), tasks)
    self.mox.VerifyAll()

    self.assertTrue(tasks[0].was_deleted)
    self.assertFalse(tasks[1].was_deleted)

  def testDeleteCallsAsync(self):
    """Test delete_tasks calls delete_tasks_async."""
    dummy_task = object()
    dummy_result = object()

    rpc = self.mox.CreateMockAnything()
    rpc.get_result().AndReturn(dummy_result)

    def DeleteTasksAsync(task):
      self.assertIs(task, dummy_task)
      return rpc

    queue = Queue('backlog')
    queue.delete_tasks_async = DeleteTasksAsync

    self.mox.ReplayAll()
    result = queue.delete_tasks(dummy_task)
    self.mox.VerifyAll()

    self.assertIs(result, dummy_result)


class AsyncDeleteTasksTest(DeleteTasksTest):
  """Tests for Queue.delete_tasks_async method.

  This will run all the tests in the superclass.
  """

  def DeleteTasks(self, queue, tasks):
    """Exercise the asynchronous method delete_tasks_async."""
    return queue.delete_tasks_async(tasks).get_result()

  def testDeleteAsyncUsesRpc(self):
    """Test delete_tasks_async returns supplied rpc."""

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    rpc.make_call('Delete',
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None)

    queue = Queue('jobs')
    task = Task(name='run')
    self.mox.ReplayAll()
    returned_rpc = queue.delete_tasks_async(task, rpc)
    self.mox.VerifyAll()

    self.assertIs(returned_rpc, rpc)


class DeleteTasksByNameTest(absltest.TestCase):
  """Tests for Queue.delete_tasks_by_name method."""

  def setUp(self):
    """Sets up the test harness."""
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.mox = mox.Mox()
    self.mox.StubOutWithMock(apiproxy_stub_map.apiproxy,
                             'MakeSyncCall')
    self.mox.StubOutWithMock(apiproxy_stub_map, 'UserRPC')

  def tearDown(self):
    """Tears down the test harness."""
    self.mox.ResetAll()
    self.mox.UnsetStubs()

  def DeleteTasksByName(self, queue, task_name):
    """Exercise the synchronous method delete_tasks_by_name."""
    return queue.delete_tasks_by_name(task_name)

  def MockSuccessfulRPC(self, expected_request, populate_response):
    """Mock an asynchronous Delete call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC result available to the caller."""
      populate_response('taskqueue', method, request, response)

      rpc.response = response
      rpc.get_result = lambda: get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('Delete',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success()

  def testDeleteSingleTask(self):
    """Tests deleting one task."""

    def SetResponse(service, method, request, response):
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)

    task_name = 'task1'
    expected_request = taskqueue_service_pb2.TaskQueueDeleteRequest()
    expected_request.queue_name = b'default'
    expected_request.task_name.append(task_name.encode('utf8'))

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    task = self.DeleteTasksByName(Queue('default'), task_name)
    self.mox.VerifyAll()

    self.assertTrue(task.was_deleted)

  def testDeleteListOfTasks(self):
    """Tests deleting a list of tasks."""

    def SetResponse(service, method, request, response):
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)
      response.result.append(taskqueue_service_pb2.TaskQueueServiceError.OK)

    task_name_one = 'task1'
    task_name_two = 'task2'
    task_name_three = 'task3'
    expected_request = taskqueue_service_pb2.TaskQueueDeleteRequest()
    expected_request.queue_name = b'default'
    expected_request.task_name.append(task_name_one.encode('utf8'))
    expected_request.task_name.append(task_name_two.encode('utf8'))
    expected_request.task_name.append(task_name_three.encode('utf8'))

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    task_names = [task_name_one, task_name_two, task_name_three]
    tasks = self.DeleteTasksByName(Queue('default'), task_names)
    self.mox.VerifyAll()

    self.assertLen(tasks, 3)
    self.assertTrue(tasks[0].was_deleted)
    self.assertTrue(tasks[1].was_deleted)
    self.assertTrue(tasks[2].was_deleted)

  def testDeleteDuplicateTaskNames(self):
    """Tests deleting list of duplicate task names."""

    task_names = ['T1', 'T2', 'T1']

    self.assertRaises(taskqueue.DuplicateTaskNameError,
                      self.DeleteTasksByName,
                      Queue('default'),
                      task_names)

  def testDeleteTasksByNameCallsAsync(self):
    """Test delete_tasks_by_name calls delete_tasks_by_name_async."""
    dummy_result = object()

    rpc = self.mox.CreateMockAnything()
    rpc.get_result().AndReturn(dummy_result)

    def DeleteTasksByNameAsync(task_name):
      self.assertEqual(task_name, 'foo')
      return rpc

    queue = Queue('backlog')
    queue.delete_tasks_by_name_async = DeleteTasksByNameAsync

    self.mox.ReplayAll()
    result = queue.delete_tasks_by_name('foo')
    self.mox.VerifyAll()

    self.assertIs(result, dummy_result)


class AsyncDeleteTasksByNameTest(DeleteTasksByNameTest):
  """Tests for Queue.delete_tasks_by_name_async method.

  This will run all the tests in the superclass.
  """

  def DeleteTasksByName(self, queue, task_name):
    """Exercise the asynchronous method delete_tasks_by_name_async."""
    return queue.delete_tasks_by_name_async(task_name).get_result()

  def testDeleteByNameAsyncUsesRpc(self):
    """Test delete_tasks_by_name_async returns supplied rpc."""

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    rpc.make_call('Delete',
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None)

    queue = Queue('jobs')
    self.mox.ReplayAll()
    returned_rpc = queue.delete_tasks_by_name_async('run', rpc)
    self.mox.VerifyAll()

    self.assertIs(returned_rpc, rpc)


class LeaseTasksTest(absltest.TestCase):
  """Tests for Queue.lease_tasks method."""

  def setUp(self):
    """Sets up the test harness."""
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.mox = mox.Mox()
    self.mox.StubOutWithMock(apiproxy_stub_map.apiproxy, 'MakeSyncCall')
    self.mox.StubOutWithMock(apiproxy_stub_map, 'UserRPC')
    self.now_timestamp = time.time()

  def tearDown(self):
    """Tears down the test harness."""
    self.mox.ResetAll()
    self.mox.UnsetStubs()

  def LeaseTasks(self, queue, *args, **kwargs):
    """Exercise the synchronous method lease_tasks."""
    return queue.lease_tasks(*args, **kwargs)

  def MockSuccessfulRPC(self, expected_request, populate_response):
    """Mock an asynchronous QueryAndOwnTasks call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC result available to the caller."""
      populate_response(method, request, response)

      rpc.response = response
      rpc.get_result = lambda: get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('QueryAndOwnTasks',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success()

  def MockUnsuccessfulRPC(self, expected_request, error_code):
    """Mock a failing asynchronous QueryAndOwnTasks call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC failure result available to the caller."""
      rpc.response = response
      get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('QueryAndOwnTasks',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success().AndRaise(apiproxy_errors.ApplicationError(
        error_code, ''))

  def testLeaseTasks(self):
    """Tests successfully leased tasks from Queue."""

    lease_seconds = 10.24

    def SetResponse(method, request, response):
      task_response1 = response.task.add()
      task_response2 = response.task.add()

      task_response1.task_name = b'T1'
      task_response1.eta_usec = SecToUsec(self.now_timestamp + lease_seconds)
      task_response1.retry_count = 0
      task_response1.body = b'somebody'

      task_response2.task_name = b't-2'
      task_response2.eta_usec = SecToUsec(self.now_timestamp + lease_seconds)
      task_response2.retry_count = 3
      task_response2.body = b'everybody'

    expected_request = taskqueue_service_pb2.TaskQueueQueryAndOwnTasksRequest()
    expected_request.queue_name = b'default'
    expected_request.lease_seconds = lease_seconds
    expected_request.max_tasks = 10

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    tasks = self.LeaseTasks(Queue('default'), lease_seconds, 10)
    self.mox.VerifyAll()

    self.assertLen(tasks, 2)

    task_result1 = tasks[0]
    self.assertEqual('T1', task_result1.name)
    self.assertEqual('default', task_result1.queue_name)
    self.assertEqual('PULL', task_result1.method)


    self.assertAlmostEqual(task_result1.eta_posix,
                           self.now_timestamp + lease_seconds, 4)
    self.assertEqual(0, task_result1.retry_count)
    self.assertEqual(b'somebody', task_result1.payload)
    self.assertEqual('', task_result1.url)

    task_result2 = tasks[1]
    self.assertEqual('t-2', task_result2.name)
    self.assertEqual('default', task_result2.queue_name)
    self.assertEqual('PULL', task_result2.method)
    self.assertAlmostEqual(task_result2.eta_posix,
                           self.now_timestamp + lease_seconds, 4)
    self.assertEqual(3, task_result2.retry_count)
    self.assertEqual(b'everybody', task_result2.payload)
    self.assertEqual('', task_result2.url)

  def testLeaseTasksWithDeadline(self):
    """Tests successfully leased tasks with deadline from Queue."""

    lease_seconds = 10.24
    deadline = 600.0

    def SetResponse(method, request, response):
      task_response1 = response.task.add()

      task_response1.task_name = b'T1'
      task_response1.eta_usec = SecToUsec(self.now_timestamp + lease_seconds)
      task_response1.retry_count = 0
      task_response1.body = b'somebody'

    expected_request = taskqueue_service_pb2.TaskQueueQueryAndOwnTasksRequest()
    expected_request.queue_name = b'default'
    expected_request.lease_seconds = lease_seconds
    expected_request.max_tasks = 10

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    tasks = self.LeaseTasks(Queue('default'),
                            lease_seconds,
                            10,
                            deadline=deadline)
    self.mox.VerifyAll()

    self.assertLen(tasks, 1)

    task_result1 = tasks[0]
    self.assertEqual('T1', task_result1.name)
    self.assertEqual('default', task_result1.queue_name)
    self.assertEqual('PULL', task_result1.method)


    self.assertAlmostEqual(task_result1.eta_posix,
                           self.now_timestamp + lease_seconds, 4)
    self.assertEqual(0, task_result1.retry_count)
    self.assertEqual(b'somebody', task_result1.payload)
    self.assertEqual('', task_result1.url)

  def testLeaseOversizedTasks(self):
    """Tests successfully leasing oversized tasks from Queue."""

    lease_seconds = 10.24

    def SetResponse(method, request, response):
      task_response1 = response.task.add()

      task_response1.task_name = b'T1'
      task_response1.eta_usec = SecToUsec(self.now_timestamp + lease_seconds)
      task_response1.retry_count = 0
      oversized_size = (taskqueue.MAX_PULL_TASK_SIZE_BYTES
                        + taskqueue.MAX_PUSH_TASK_SIZE_BYTES)
      task_response1.body = b'x' * oversized_size

    expected_request = taskqueue_service_pb2.TaskQueueQueryAndOwnTasksRequest()
    expected_request.queue_name = b'default'
    expected_request.lease_seconds = lease_seconds
    expected_request.max_tasks = 10

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    tasks = self.LeaseTasks(Queue('default'), lease_seconds, 10)
    self.mox.VerifyAll()

    self.assertLen(tasks, 1)

  def testLeaseTasksOnPushQueue(self):
    """Tests leasing tasks from a push queue."""

    expected_request = taskqueue_service_pb2.TaskQueueQueryAndOwnTasksRequest()
    expected_request.queue_name = b'push-queue'
    expected_request.lease_seconds = 100.0
    expected_request.max_tasks = 10

    self.MockUnsuccessfulRPC(expected_request,
                             TaskQueueServiceError.INVALID_QUEUE_MODE)

    q = Queue('push-queue')
    self.mox.ReplayAll()
    self.assertRaises(taskqueue.InvalidQueueModeError,
                      self.LeaseTasks,
                      q,
                      100.0,
                      10)
    self.mox.VerifyAll()

  def testLeaseTasksNegativeLeaseTime(self):
    """Tests lease_tasks with negative lease time value."""
    self.assertRaises(taskqueue.InvalidLeaseTimeError,
                      self.LeaseTasks,
                      Queue('default'),
                      -1.0,
                      10)

  def testLeaseTasksTooLongLeaseTime(self):
    """Tests lease_tasks with too large lease time value."""
    self.assertRaises(taskqueue.InvalidLeaseTimeError,
                      self.LeaseTasks,
                      Queue('default'),
                      86400 * 30.0,
                      10)

  def testLeaseTasksNegativeNumberOfTasks(self):
    """Tests lease_tasks with negative number of max tasks."""
    self.assertRaises(taskqueue.InvalidMaxTasksError,
                      self.LeaseTasks,
                      Queue('default'),
                      100.0,
                      -1)

  def testLeaseTooLargeMaxNumberOfTasks(self):
    """Tests lease_tasks with too large max number."""
    self.assertRaises(taskqueue.InvalidMaxTasksError,
                      self.LeaseTasks,
                      Queue('default'),
                      100.0,
                      1024)

  def testLeaseTasksParameterWrongType(self):
    """Tests lease_tasks with wrong type of parameters."""
    self.assertRaises(TypeError,
                      self.LeaseTasks,
                      Queue('default'),
                      '100.0',
                      12)

  def testLeaseTasksParameterWrongValue(self):
    """Tests lease_tasks with invalid value."""
    self.assertRaises(TypeError,
                      self.LeaseTasks,
                      Queue('default'),
                      100.0,
                      5.8)

  def testLeaseTasksNullDeadline(self):
    """Tests lease_tasks with null deadline value."""

    self.assertRaises(TypeError,
                      Queue('default').lease_tasks,
                      123.0,
                      45,
                      deadline=None)

  def testLeaseTasksNegativeDeadline(self):
    """Tests lease_tasks with negative deadline value."""
    self.assertRaises(taskqueue.InvalidDeadlineError,
                      Queue('default').lease_tasks,
                      1.0,
                      10,
                      deadline=-600.0)

  def testLeaseCallsAsync(self):
    """Test lease_tasks calls lease_tasks_async."""
    dummy_result = object()

    rpc = self.mox.CreateMockAnything()
    rpc.get_result().AndReturn(dummy_result)
    apiproxy_stub_map.UserRPC('taskqueue', 10, None).AndReturn(rpc)

    def LeaseTasksAsync(lease_seconds, max_tasks, optional_rpc):
      self.assertEqual(lease_seconds, 750)
      self.assertEqual(max_tasks, 800)
      self.assertIs(optional_rpc, rpc)
      return rpc

    queue = Queue('backlog')
    queue.lease_tasks_async = LeaseTasksAsync

    self.mox.ReplayAll()
    result = queue.lease_tasks(750, 800)
    self.mox.VerifyAll()

    self.assertIs(result, dummy_result)


class AsyncLeaseTasksTest(LeaseTasksTest):
  """Tests for Queue.lease_tasks_async method.

  This will run all the tests in the superclass.
  """

  def LeaseTasks(self, queue, lease_seconds, max_tasks, deadline=None):
    """Exercise the asynchronous method lease_tasks_async."""
    if deadline is None:
      return queue.lease_tasks_async(lease_seconds, max_tasks).get_result()
    else:
      rpc = taskqueue.create_rpc(deadline=deadline)
      returned_rpc = queue.lease_tasks_async(lease_seconds, max_tasks, rpc)
      self.assertIs(returned_rpc, rpc)
      return rpc.get_result()

  def testLeaseAsyncUsesRpc(self):
    """Test lease_tasks_async returns supplied rpc."""

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    rpc.make_call('QueryAndOwnTasks',
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None)

    queue = Queue('jobs')
    self.mox.ReplayAll()
    returned_rpc = queue.lease_tasks_async(20.0, 500, rpc)
    self.mox.VerifyAll()

    self.assertIs(returned_rpc, rpc)


class LeaseTasksByTagTest(absltest.TestCase):
  """Tests for Queue.lease_tasks_by_tag method."""

  def setUp(self):
    """Sets up the test harness."""
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.mox = mox.Mox()
    self.mox.StubOutWithMock(apiproxy_stub_map.apiproxy, 'MakeSyncCall')
    self.mox.StubOutWithMock(apiproxy_stub_map, 'UserRPC')

  def tearDown(self):
    """Tears down the test harness."""
    self.mox.ResetAll()
    self.mox.UnsetStubs()

  def LeaseTasksByTag(self, queue, *args, **kwargs):
    """Exercise the synchronous method lease_tasks_by_tag."""
    return queue.lease_tasks_by_tag(*args, **kwargs)

  def MockSuccessfulRPC(self, expected_request, populate_response):
    """Mock an asynchronous QueryAndOwnTasks call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC result available to the caller."""
      populate_response(method, request, response)

      rpc.response = response
      rpc.get_result = lambda: get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('QueryAndOwnTasks',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success()

  def MockUnsuccessfulRPC(self, expected_request, error_code):
    """Mock a failing asynchronous QueryAndOwnTasks call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC failure result available to the caller."""
      rpc.response = response
      get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('QueryAndOwnTasks',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success().AndRaise(apiproxy_errors.ApplicationError(
        error_code, ''))

  def SetResponse(self, real_response):
    def _Inner(unused_service, unused_method, unused_request, response):
      response.CopyFrom(real_response)
    return _Inner

  def testLeaseTasksWithoutSpecifiedTag(self):
    """Tests successfully leased tasks from Queue."""

    lease_seconds = 1.234
    lease_timestamp_sec = 12345678
    lease_timestamp_usec = SecToUsec(lease_timestamp_sec)

    expected_request = taskqueue_service_pb2.TaskQueueQueryAndOwnTasksRequest()
    expected_request.queue_name = b'default'
    expected_request.lease_seconds = lease_seconds
    expected_request.max_tasks = 10
    expected_request.group_by_tag = True

    def SetResponse(method, request, response):
      task_response1 = response.task.add()
      task_response2 = response.task.add()

      task_response1.task_name = b'T1'
      task_response1.eta_usec = lease_timestamp_usec
      task_response1.retry_count = 0
      task_response1.body = b'somebody'

      task_response2.task_name = b't-2'
      task_response2.eta_usec = lease_timestamp_usec
      task_response2.retry_count = 3
      task_response2.body = b'everybody'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    tasks = self.LeaseTasksByTag(Queue('default'), lease_seconds, 10)
    self.mox.VerifyAll()

    self.assertLen(tasks, 2)

    task_result1 = tasks[0]
    self.assertEqual('T1', task_result1.name)
    self.assertEqual('default', task_result1.queue_name)
    self.assertEqual('PULL', task_result1.method)
    self.assertEqual(task_result1.eta_posix, lease_timestamp_sec)
    self.assertEqual(0, task_result1.retry_count)
    self.assertEqual(b'somebody', task_result1.payload)
    self.assertEqual('', task_result1.url)
    self.assertEqual(None, task_result1.tag)

    task_result2 = tasks[1]
    self.assertEqual('t-2', task_result2.name)
    self.assertEqual('default', task_result2.queue_name)
    self.assertEqual('PULL', task_result2.method)
    self.assertEqual(task_result2.eta_posix, lease_timestamp_sec)
    self.assertEqual(3, task_result2.retry_count)
    self.assertEqual(b'everybody', task_result2.payload)
    self.assertEqual('', task_result2.url)
    self.assertEqual(None, task_result2.tag)

  def testLeaseTasksWithoutSpecifiedTag2(self):
    """Tests successfully leased tasks from Queue.

    This test requests for tasks to be grouped by the first available tag.
    """

    lease_seconds = 1.234
    lease_timestamp_sec = 12345678
    lease_timestamp_usec = SecToUsec(lease_timestamp_sec)
    tag = 'my-tag'

    expected_request = taskqueue_service_pb2.TaskQueueQueryAndOwnTasksRequest()
    expected_request.queue_name = b'default'
    expected_request.lease_seconds = lease_seconds
    expected_request.max_tasks = 10
    expected_request.group_by_tag = True

    def SetResponse(method, request, response):
      task_response1 = response.task.add()
      task_response2 = response.task.add()

      task_response1.task_name = b'T1'
      task_response1.eta_usec = lease_timestamp_usec
      task_response1.retry_count = 0
      task_response1.body = b'somebody'
      task_response1.tag = tag.encode('utf8')

      task_response2.task_name = b't-2'
      task_response2.eta_usec = lease_timestamp_usec
      task_response2.retry_count = 3
      task_response2.body = b'everybody'
      task_response2.tag = tag.encode('utf8')

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    tasks = self.LeaseTasksByTag(Queue('default'), lease_seconds, 10)
    self.mox.VerifyAll()

    self.assertLen(tasks, 2)

    task_result1 = tasks[0]
    self.assertEqual('T1', task_result1.name)
    self.assertEqual('default', task_result1.queue_name)
    self.assertEqual('PULL', task_result1.method)
    self.assertEqual(task_result1.eta_posix, lease_timestamp_sec)
    self.assertEqual(0, task_result1.retry_count)
    self.assertEqual(b'somebody', task_result1.payload)
    self.assertEqual('', task_result1.url)
    self.assertEqual(tag, task_result1.tag)

    task_result2 = tasks[1]
    self.assertEqual('t-2', task_result2.name)
    self.assertEqual('default', task_result2.queue_name)
    self.assertEqual('PULL', task_result2.method)
    self.assertEqual(task_result2.eta_posix, lease_timestamp_sec)
    self.assertEqual(3, task_result2.retry_count)
    self.assertEqual(b'everybody', task_result2.payload)
    self.assertEqual('', task_result2.url)
    self.assertEqual(tag, task_result2.tag)

  def testLeaseTasksWithSpecifiedTag(self):
    """Tests successfully leased tasks from Queue."""

    lease_seconds = 1.234
    lease_timestamp_sec = 12345678
    lease_timestamp_usec = SecToUsec(lease_timestamp_sec)
    tag = 'my-tag'

    expected_request = taskqueue_service_pb2.TaskQueueQueryAndOwnTasksRequest()
    expected_request.queue_name = b'default'
    expected_request.lease_seconds = lease_seconds
    expected_request.max_tasks = 10
    expected_request.group_by_tag = True
    expected_request.tag = tag.encode('utf8')

    def SetResponse(method, request, response):
      task_response1 = response.task.add()
      task_response2 = response.task.add()

      task_response1.task_name = b'T1'
      task_response1.eta_usec = lease_timestamp_usec
      task_response1.retry_count = 0
      task_response1.body = b'somebody'
      task_response1.tag = tag.encode('utf8')

      task_response2.task_name = b't-2'
      task_response2.eta_usec = lease_timestamp_usec
      task_response2.retry_count = 3
      task_response2.body = b'everybody'
      task_response2.tag = tag.encode('utf8')

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    tasks = self.LeaseTasksByTag(Queue('default'), lease_seconds, 10, tag=tag)
    self.mox.VerifyAll()

    self.assertLen(tasks, 2)

    task_result1 = tasks[0]
    self.assertEqual('T1', task_result1.name)
    self.assertEqual('default', task_result1.queue_name)
    self.assertEqual('PULL', task_result1.method)
    self.assertEqual(task_result1.eta_posix, lease_timestamp_sec)
    self.assertEqual(0, task_result1.retry_count)
    self.assertEqual(b'somebody', task_result1.payload)
    self.assertEqual('', task_result1.url)
    self.assertEqual(tag, task_result1.tag)

    task_result2 = tasks[1]
    self.assertEqual('t-2', task_result2.name)
    self.assertEqual('default', task_result2.queue_name)
    self.assertEqual('PULL', task_result2.method)
    self.assertEqual(task_result2.eta_posix, lease_timestamp_sec)
    self.assertEqual(3, task_result2.retry_count)
    self.assertEqual(b'everybody', task_result2.payload)
    self.assertEqual('', task_result2.url)
    self.assertEqual(tag, task_result2.tag)

  def testLeaseTasksOnPushQueue(self):
    """Tests leasing tasks from a push queue."""

    expected_request = taskqueue_service_pb2.TaskQueueQueryAndOwnTasksRequest()
    expected_request.queue_name = b'default'
    expected_request.lease_seconds = 100.0
    expected_request.max_tasks = 10
    expected_request.group_by_tag = True

    self.MockUnsuccessfulRPC(expected_request,
                             TaskQueueServiceError.INVALID_QUEUE_MODE)

    q = Queue('default')
    self.mox.ReplayAll()
    self.assertRaises(taskqueue.InvalidQueueModeError,
                      self.LeaseTasksByTag,
                      q,
                      100.0,
                      10)
    self.mox.VerifyAll()

  def testLeaseTasksNegativeLeaseTime(self):
    """Tests lease_tasks with negative lease time value."""
    self.assertRaises(taskqueue.InvalidLeaseTimeError,
                      self.LeaseTasksByTag,
                      Queue('default'),
                      -1.0,
                      10)

  def testLeaseTasksTooLongLeaseTime(self):
    """Tests lease_tasks with too large lease time value."""
    self.assertRaises(taskqueue.InvalidLeaseTimeError,
                      self.LeaseTasksByTag,
                      Queue('default'),
                      86400 * 30.0,
                      10)

  def testLeaseTasksNegativeNumberOfTasks(self):
    """Tests lease_tasks with negative number of max tasks."""
    self.assertRaises(taskqueue.InvalidMaxTasksError,
                      self.LeaseTasksByTag,
                      Queue('default'),
                      100.0,
                      -1)

  def testLeaseTooLargeMaxNumberOfTasks(self):
    """Tests lease_tasks with too large max number."""
    self.assertRaises(taskqueue.InvalidMaxTasksError,
                      self.LeaseTasksByTag,
                      Queue('default'),
                      100.0,
                      1024)

  def testLeaseTasksParameterWrongType(self):
    """Tests lease_tasks with wrong type of parameters."""
    self.assertRaises(TypeError,
                      self.LeaseTasksByTag,
                      Queue('default'),
                      '100.0',
                      12)

  def testLeaseTasksParameterWrongValue(self):
    """Tests lease_tasks with invalid value."""
    self.assertRaises(TypeError,
                      self.LeaseTasksByTag,
                      Queue('default'),
                      100.0,
                      5.8)

  def testLeaseTasksParameterWrongType2(self):
    """Tests lease_tasks with wrong type of parameters.

    This test uses the wrong deadline type.
    """

    self.assertRaises(TypeError,
                      Queue('default').lease_tasks_by_tag,
                      100.0,
                      12,
                      tag='my-tag',
                      deadline=3J)

  def testLeaseByTagCallsAsync(self):
    """Test lease_tasks_by_tag calls lease_tasks_by_tag_async."""
    dummy_result = object()

    rpc = self.mox.CreateMockAnything()
    rpc.get_result().AndReturn(dummy_result)
    apiproxy_stub_map.UserRPC('taskqueue', 10, None).AndReturn(rpc)

    def LeaseTasksByTagAsync(lease_seconds, max_tasks, tag, optional_rpc):
      self.assertEqual(lease_seconds, 750)
      self.assertEqual(max_tasks, 800)
      self.assertEqual(tag, 'priority')
      self.assertIs(optional_rpc, rpc)
      return rpc

    queue = Queue('backlog')
    queue.lease_tasks_by_tag_async = LeaseTasksByTagAsync

    self.mox.ReplayAll()
    result = queue.lease_tasks_by_tag(750, 800, 'priority')
    self.mox.VerifyAll()

    self.assertIs(result, dummy_result)


class AsyncLeaseTasksByTagTest(LeaseTasksByTagTest):
  """Tests for Queue.lease_tasks_by_tag_async method.

  This will run all the tests in the superclass.
  """

  def LeaseTasksByTag(self,
                      queue,
                      lease_seconds,
                      max_tasks,
                      tag=None,
                      deadline=None):
    """Exercise the asynchronous method lease_tasks_by_tag_async."""
    if deadline is None:
      if tag is None:
        return queue.lease_tasks_by_tag_async(
            lease_seconds, max_tasks).get_result()
      else:
        return queue.lease_tasks_by_tag_async(
            lease_seconds, max_tasks, tag).get_result()
    else:
      rpc = taskqueue.create_rpc(deadline=deadline)
      returned_rpc = queue.lease_tasks_by_tag_async(
          lease_seconds, max_tasks, tag, rpc)
      self.assertIs(returned_rpc, rpc)
      return rpc.get_result()

  def testLeaseByTagAsyncUsesRpc(self):
    """Test lease_tasks_by_tag_async returns supplied rpc."""

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    rpc.make_call('QueryAndOwnTasks',
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None)

    queue = Queue('jobs')
    self.mox.ReplayAll()
    returned_rpc = queue.lease_tasks_by_tag_async(20.0, 500, rpc=rpc)
    self.mox.VerifyAll()

    self.assertIs(returned_rpc, rpc)


class QueuePurgeTest(absltest.TestCase):
  """Tests for Queue.purge method."""

  def setUp(self):
    """Sets up the test harness."""
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.mox = mox.Mox()
    self.mox.StubOutWithMock(apiproxy_stub_map.apiproxy,
                             'MakeSyncCall')

  def tearDown(self):
    """Tears down the test harness."""
    self.mox.ResetAll()
    self.mox.UnsetStubs()

  def testPurge(self):
    """Tests purging a Queue."""
    expected_request = taskqueue_service_pb2.TaskQueuePurgeQueueRequest()
    expected_request.queue_name = b'default'

    apiproxy_stub_map.apiproxy.MakeSyncCall(
        'taskqueue',
        'PurgeQueue',
        expected_request,
        mox.IgnoreArg())

    self.mox.ReplayAll()
    Queue('default').purge()
    self.mox.VerifyAll()

  def testPurgeApplicationError(self):
    """Tests ApplicationError returned from MakeSyncCall."""

    def RaiseUnknownQueueApplicationError(service, method, request, response):
      raise apiproxy_errors.ApplicationError(
          taskqueue_service_pb2.TaskQueueServiceError.UNKNOWN_QUEUE)

    expected_request = taskqueue_service_pb2.TaskQueuePurgeQueueRequest()
    expected_request.queue_name = b'WrongName'

    apiproxy_stub_map.apiproxy.MakeSyncCall(
        'taskqueue',
        'PurgeQueue',
        expected_request,
        mox.IgnoreArg()).WithSideEffects(RaiseUnknownQueueApplicationError)

    self.mox.ReplayAll()
    self.assertRaises(taskqueue.UnknownQueueError,
                      Queue('WrongName').purge)
    self.mox.VerifyAll()


class QueueAddTest(HttpEnvironTest):
  """Tests for the Queue class and anything that puts Tasks in a queue."""

  def setUp(self):
    """Sets up the test harness."""
    HttpEnvironTest.setUp(self)
    self.now = datetime.datetime(2009, 5, 5, 21, 50, 28, 517317)
    self.now_timestamp_usec = 1241560228517317
    self.params = {'one': 'two'}
    self.headers = {'red': 'blue', 'five': 'six'}
    self.payload = b'some-data'

    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()

    self.mox = mox.Mox()
    self.mox.StubOutWithMock(apiproxy_stub_map.apiproxy,
                             'MakeSyncCall')
    self.mox.StubOutWithMock(apiproxy_stub_map, 'UserRPC')

  def tearDown(self):
    """Tears down the test harness."""
    self.mox.ResetAll()
    self.mox.UnsetStubs()
    HttpEnvironTest.tearDown(self)

  def Add(self, queue, *args, **kwargs):
    """Exercise Queue's synchronous method add."""
    self.assertIsInstance(queue, Queue)
    return queue.add(*args, **kwargs)

  def TaskAdd(self, task, *args, **kwargs):
    """Exercise Task's synchronous method add."""
    self.assertIsInstance(task, Task)
    return task.add(*args, **kwargs)

  def MockSuccessfulRPC(self, expected_request, populate_response):
    """Mock an asynchronous BulkAdd call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC result available to the caller."""
      populate_response('taskqueue', method, request, response)

      rpc.response = response
      rpc.get_result = lambda: get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('BulkAdd',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success()

  def MockUnsuccessfulRPC(self, expected_request, error_code):
    """Mock a failing asynchronous BulkAdd call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC failure result available to the caller."""
      rpc.response = response
      get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('BulkAdd',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success().AndRaise(apiproxy_errors.ApplicationError(
        error_code, ''))

  def testWithNameAndUrl(self):
    """Tests adding a Task, which has a name and URL specified, to a Queue."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b'mytask'
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.GET
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    url = '/my/custom/url?foo=bar'
    add_request.url = url.encode('utf8')

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    t = self.TaskAdd(Task(name='mytask', url=url, eta=self.now, method='GET'))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('mytask', t.name)
    self.assertEqual('default', t.queue_name)

  def testWithRelativeUrl(self):
    """Tests adding a Task, which only has a URL specified, to a Queue."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result.chosen_task_name = b'AUTO-ASSIGNED'

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b''
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.GET
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    url = '/my/custom/url?foo=bar'
    add_request.url = url.encode('utf8')

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    t = self.TaskAdd(Task(url=url, eta=self.now, method='GET'))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('AUTO-ASSIGNED', t.name)
    self.assertEqual('default', t.queue_name)

  def testWithName(self):
    """Tests adding a Task to a queue that only specifies a name."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b'mytask'
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    t = self.TaskAdd(Task(name='mytask', eta=self.now))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('mytask', t.name)
    self.assertEqual('default', t.queue_name)

  def testWithDispatchDeadline(self):
    """Tests adding a Task to a queue that specifies a dispatch deadline."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b'deadline'
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default'
    add_request.dispatch_deadline_usec = 15000000

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    t = self.TaskAdd(
        Task(name='deadline', eta=self.now, dispatch_deadline_usec=15000000))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)

  def testWithNameAndParams(self):
    """Tests adding a Task, which has a name and GET arguments, to a Queue."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b'mytask'
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.GET
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default?one=two'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    t = self.TaskAdd(Task(name='mytask',
                          eta=self.now,
                          params=self.params,
                          method='GET'))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('mytask', t.name)
    self.assertEqual('default', t.queue_name)

  def testNoNameAndNoUrl(self):
    """Tests adding a Task that has no assigned name or URL."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result.chosen_task_name = b'AUTO-ASSIGNED'

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b''
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    t = self.TaskAdd(Task(eta=self.now))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('AUTO-ASSIGNED', t.name)
    self.assertEqual('default', t.queue_name)

  def testNoNameAndNoUrlAndParams(self):
    """Tests adding a Task that has no assigned name or URL."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result.chosen_task_name = b'AUTO-ASSIGNED'

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b''
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.GET
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default?one=two'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    t = self.TaskAdd(Task(eta=self.now, params=self.params, method='GET'))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('AUTO-ASSIGNED', t.name)
    self.assertEqual('default', t.queue_name)

  def testBackoffOnlyTaskRetryOptions(self):
    """Tests adding a Task with only the backoff times set on RetryOptions."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result.chosen_task_name = b'AUTO-ASSIGNED'

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b''
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default'
    retry_parameters = add_request.retry_parameters
    retry_parameters.min_backoff_sec = 1.1
    retry_parameters.max_backoff_sec = 2.6

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    task_retry_options = TaskRetryOptions(min_backoff_seconds=1.1,
                                          max_backoff_seconds=2.6)
    t = self.TaskAdd(Task(eta=self.now,
                          retry_options=task_retry_options))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('default', t.queue_name)

  def testMinimalTaskRetryOptions(self):
    """Tests adding a Task with no optional parameters set on RetryOptions."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result.chosen_task_name = b'AUTO-ASSIGNED'

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b''
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default'
    add_request.retry_parameters

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    t = self.TaskAdd(Task(eta=self.now, retry_options=TaskRetryOptions()))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('default', t.queue_name)

  def testFullAssignment(self):
    """Tests all fields of the Task together."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.app_id = b'admin-console'
    add_request.task_name = b'mytask'
    add_request.queue_name = b'override'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/override/path'
    add_request.body = b'this is my body'
    header = add_request.header.add()
    header.key = b'five'
    header.value = b'six'
    header = add_request.header.add()
    header.key = b'red'
    header.value = b'blue'
    retry_parameters = add_request.retry_parameters
    retry_parameters.retry_limit = 10
    retry_parameters.age_limit_sec = 60
    retry_parameters.min_backoff_sec = 1.1
    retry_parameters.max_backoff_sec = 2.6
    retry_parameters.max_doublings = 100

    self.MockSuccessfulRPC(
        TaskQueueBulkAddRequestComparator(expected_request),
        SetResponse)

    self.mox.ReplayAll()
    q = Queue('override')
    q._app = 'admin-console'
    t = Task(b'this is my body', name='mytask', eta=self.now,
             headers=self.headers, url='/override/path',
             retry_options=TaskRetryOptions(min_backoff_seconds=1.1,
                                            max_backoff_seconds=2.6,
                                            task_age_limit=59.8,
                                            max_doublings=100,
                                            task_retry_limit=10))
    self.Add(q, t)
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('mytask', t.name)
    self.assertEqual('override', t.queue_name)

  def testFullAssignmentWithAdd(self):
    """Tests all fields of the Task together."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b'mytask'
    add_request.queue_name = b'override'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/override/path'
    add_request.body = b'this is my body'
    header = add_request.header.add()
    header.key = b'five'
    header.value = b'six'
    header = add_request.header.add()
    header.key = b'red'
    header.value = b'blue'
    retry_parameters = add_request.retry_parameters
    retry_parameters.retry_limit = 10
    retry_parameters.age_limit_sec = 60
    retry_parameters.min_backoff_sec = 1.1
    retry_parameters.max_backoff_sec = 2.6
    retry_parameters.max_doublings = 100

    self.MockSuccessfulRPC(
        TaskQueueBulkAddRequestComparator(expected_request),
        SetResponse)

    self.mox.ReplayAll()

    t = taskqueue.add(b'this is my body',
                      name='mytask',
                      eta=self.now,
                      queue_name='override',
                      headers=self.headers,
                      url='/override/path',
                      retry_options=TaskRetryOptions(min_backoff_seconds=1.1,
                                                     max_backoff_seconds=2.6,
                                                     task_age_limit=59.8,
                                                     max_doublings=100,
                                                     task_retry_limit=10))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('mytask', t.name)
    self.assertEqual('override', t.queue_name)

  def testTransactionalAddOutsideOfTransaction(self):
    """Tests adding a Task with transactional set outside of a transaction."""

    self.assertRaises(taskqueue.BadTransactionStateError,
                      self.TaskAdd,
                      Task(eta=self.now, params=self.params, method='GET'),
                      transactional=True)
    self.assertRaises(taskqueue.BadTransactionStateError,
                      taskqueue.add,
                      method='PULL',
                      payload='payload',
                      transactional=True)

  def testConvenienceMethod(self):
    """Tests the module-level 'add' convenience method."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b'mytask'
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()

    t = taskqueue.add(name='mytask', eta=self.now)
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('mytask', t.name)
    self.assertEqual('default', t.queue_name)

  def testAddTaskInstanceTwice(self):
    """Tests that enqueueing a Task instance twice will error."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b'mytask5'
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    t = Task(name='mytask5', eta=self.now)
    self.mox.ReplayAll()
    self.TaskAdd(t)
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('mytask5', t.name)

    self.assertRaises(taskqueue.BadTaskStateError,
                      self.TaskAdd,
                      t)
    self.assertTrue(t.was_enqueued)
    self.assertEqual('mytask5', t.name)

  def testMultipleResults(self):
    """Tests that the a results is returned with many Task arguments."""

    def SetResponse(service, method, request, response):
      task_result1 = response.taskresult.add()
      task_result1.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result2 = response.taskresult.add()
      task_result2.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result3 = response.taskresult.add()
      task_result3.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request1 = _InitAddRequest(expected_request)
    add_request1.task_name = b'mytask1'
    add_request1.queue_name = b'default'
    add_request1.eta_usec = self.now_timestamp_usec
    add_request1.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request1.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request1.url = b'/_ah/queue/default'
    add_request2 = _InitAddRequest(expected_request)
    add_request2.task_name = b'mytask2'
    add_request2.queue_name = b'default'
    add_request2.eta_usec = self.now_timestamp_usec
    add_request2.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request2.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request2.url = b'/_ah/queue/default'
    add_request3 = _InitAddRequest(expected_request)
    add_request3.task_name = b'mytask3'
    add_request3.queue_name = b'default'
    add_request3.eta_usec = self.now_timestamp_usec
    add_request3.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request3.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request3.url = b'/_ah/queue/default'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    t1 = Task(name='mytask1', eta=self.now)
    t2 = Task(name='mytask2', eta=self.now)
    t3 = Task(name='mytask3', eta=self.now)

    self.mox.ReplayAll()
    self.assertEqual([t1, t2, t3], self.Add(Queue(), [t1, t2, t3], False))
    self.mox.VerifyAll()

  def testAddExistingTask(self):
    """Tests partial success (some tasks added, others not)."""

    def SetResponse(service, method, request, response):
      task_result1 = response.taskresult.add()
      task_result1.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result1.chosen_task_name = b'AUTO-ASSIGNED2'
      task_result2 = response.taskresult.add()
      task_result2.result = taskqueue_service_pb2.TaskQueueServiceError.TASK_ALREADY_EXISTS
      task_result3 = response.taskresult.add()
      task_result3.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request1 = _InitAddRequest(expected_request)
    add_request1.task_name = b''
    add_request1.queue_name = b'default'
    add_request1.eta_usec = self.now_timestamp_usec
    add_request1.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request1.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request1.url = b'/_ah/queue/default'
    add_request2 = _InitAddRequest(expected_request)
    add_request2.task_name = b'mytask2'
    add_request2.queue_name = b'default'
    add_request2.eta_usec = self.now_timestamp_usec
    add_request2.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request2.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request2.url = b'/_ah/queue/default'
    add_request3 = _InitAddRequest(expected_request)
    add_request3.task_name = b'mytask3'
    add_request3.queue_name = b'default'
    add_request3.eta_usec = self.now_timestamp_usec
    add_request3.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request3.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request3.url = b'/_ah/queue/default'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    t1 = Task(name='', eta=self.now)
    t2 = Task(name='mytask2', eta=self.now)
    t3 = Task(name='mytask3', eta=self.now)

    self.mox.ReplayAll()
    self.assertRaises(taskqueue.TaskAlreadyExistsError,
                      self.Add,
                      Queue(),
                      [t1, t2, t3])
    self.mox.VerifyAll()
    self.assertTrue(t1.was_enqueued)
    self.assertEqual('AUTO-ASSIGNED2', t1.name)
    self.assertFalse(t2.was_enqueued)
    self.assertEqual('mytask2', t2.name)
    self.assertTrue(t3.was_enqueued)
    self.assertEqual('mytask3', t3.name)

  def testAddMixedErrors(self):
    """Tests TaskAlreadyExists and TombstonedTask never hide other errors."""

    def SetResponse(service, method, request, response):
      task_result1 = response.taskresult.add()
      task_result1.result = taskqueue_service_pb2.TaskQueueServiceError.TASK_ALREADY_EXISTS
      task_result2 = response.taskresult.add()
      task_result2.result = taskqueue_service_pb2.TaskQueueServiceError.TOMBSTONED_TASK
      task_result3 = response.taskresult.add()
      task_result3.result = taskqueue_service_pb2.TaskQueueServiceError.TRANSIENT_ERROR
      task_result4 = response.taskresult.add()
      task_result4.result = taskqueue_service_pb2.TaskQueueServiceError.DATASTORE_ERROR

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    task_names = ['first', 'second', 'third', 'fourth']
    for task_name in task_names:
      add_request = _InitAddRequest(expected_request)
      add_request.task_name = task_name.encode('utf8')
      add_request.queue_name = b'default'
      add_request.eta_usec = self.now_timestamp_usec
      add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
      add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
      add_request.url = b'/_ah/queue/default'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    tasks = [Task(name=task_name, eta=self.now)
             for task_name in task_names]

    self.mox.ReplayAll()
    self.assertRaises(taskqueue.TransientError,
                      self.Add,
                      Queue(),
                      tasks)
    self.mox.VerifyAll()
    for task in tasks:
      self.assertFalse(task.was_enqueued)

  def testNoTasks(self):
    """Tests adding an empty list of tasks to a Queue."""

    self.assertEqual([], Queue().add([]))

  def testTooManyTasks(self):
    """Tests adding a list containing too many tasks to a Queue."""
    tasks = [Task() for _ in range(taskqueue.MAX_TASKS_PER_ADD + 1)]
    self.assertRaises(taskqueue.TooManyTasksError, self.Add, Queue(), tasks)

  def testDuplicateTaskNames(self):
    """Tests adding Tasks with duplicate names to a Queue."""
    self.assertRaises(taskqueue.DuplicateTaskNameError,
                      self.Add,
                      Queue(),
                      [Task(name='A'), Task(name='B'), Task(name='B')])

  def RunBulkAddApplicationError(self, error_code, error_class):
    """Tests BulkAdd() raising an ApplicationError error with the given code."""
    self.mox.ResetAll()

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request1 = _InitAddRequest(expected_request)
    add_request1.task_name = b'mytask'
    add_request1.queue_name = b'default'
    add_request1.eta_usec = self.now_timestamp_usec
    add_request1.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request1.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request1.url = b'/_ah/queue/default'

    self.MockUnsuccessfulRPC(expected_request, error_code)

    t = Task(name='mytask', eta=self.now)
    self.mox.ReplayAll()
    self.assertRaises(error_class, self.TaskAdd, t)
    self.mox.VerifyAll()
    self.assertFalse(t.was_enqueued)
    self.assertEqual('mytask', t.name)

  def testBulkAddApplicationErrors(self):
    """Tests that BulkAdd() ApplicationErrors are mapped to exceptions."""
    self.RunBulkAddApplicationError(TaskQueueServiceError.UNKNOWN_QUEUE,
                                    taskqueue.UnknownQueueError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.TRANSIENT_ERROR,
                                    taskqueue.TransientError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.INTERNAL_ERROR,
                                    taskqueue.InternalError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.TASK_TOO_LARGE,
                                    taskqueue.TaskTooLargeError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.INVALID_TASK_NAME,
                                    taskqueue.InvalidTaskNameError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.INVALID_QUEUE_NAME,
                                    taskqueue.InvalidQueueNameError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.INVALID_URL,
                                    taskqueue.InvalidUrlError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.INVALID_QUEUE_RATE,
                                    taskqueue.InvalidQueueError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.PERMISSION_DENIED,
                                    taskqueue.PermissionDeniedError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.TASK_ALREADY_EXISTS,
                                    taskqueue.TaskAlreadyExistsError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.TOMBSTONED_TASK,
                                    taskqueue.TombstonedTaskError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.INVALID_ETA,
                                    taskqueue.InvalidEtaError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.INVALID_REQUEST,
                                    taskqueue.Error)
    self.RunBulkAddApplicationError(TaskQueueServiceError.UNKNOWN_TASK,
                                    taskqueue.Error)
    self.RunBulkAddApplicationError(TaskQueueServiceError.TOMBSTONED_QUEUE,
                                    taskqueue.Error)
    self.RunBulkAddApplicationError(TaskQueueServiceError.DUPLICATE_TASK_NAME,
                                    taskqueue.DuplicateTaskNameError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.TOO_MANY_TASKS,
                                    taskqueue.TooManyTasksError)

    self.RunBulkAddApplicationError(object(), taskqueue.Error)



    self.RunBulkAddApplicationError(TaskQueueServiceError.DATASTORE_ERROR,
                                    taskqueue.DatastoreError)
    self.RunBulkAddApplicationError(TaskQueueServiceError.DATASTORE_ERROR,
                                    datastore_errors.Error)

  def RunBulkAddTaskResultError(self, error_code, error_class):
    """Tests BulkAdd() returning error_code in a TaskResult."""
    self.mox.ResetAll()

    def SetResponse(service, method, request, response):
      response.taskresult.add().result = taskqueue_service_pb2.TaskQueueServiceError.SKIPPED
      response.taskresult.add().result = error_code
      response.taskresult.add().result = taskqueue_service_pb2.TaskQueueServiceError.SKIPPED

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request1 = _InitAddRequest(expected_request)
    add_request1.task_name = b'mytask1'
    add_request1.queue_name = b'default'
    add_request1.eta_usec = self.now_timestamp_usec
    add_request1.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request1.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request1.url = b'/_ah/queue/default'
    add_request2 = _InitAddRequest(expected_request)
    add_request2.task_name = b'mytask2'
    add_request2.queue_name = b'default'
    add_request2.eta_usec = self.now_timestamp_usec
    add_request2.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request2.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request2.url = b'/_ah/queue/default'
    add_request3 = _InitAddRequest(expected_request)
    add_request3.task_name = b'mytask3'
    add_request3.queue_name = b'default'
    add_request3.eta_usec = self.now_timestamp_usec
    add_request3.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request3.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request3.url = b'/_ah/queue/default'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    t1 = Task(name='mytask1', eta=self.now)
    t2 = Task(name='mytask2', eta=self.now)
    t3 = Task(name='mytask3', eta=self.now)

    self.mox.ReplayAll()
    self.assertRaises(error_class, self.Add, Queue(), [t1, t2, t3])
    self.mox.VerifyAll()

    self.assertFalse(t1.was_enqueued)
    self.assertEqual('mytask1', t1.name)
    self.assertFalse(t2.was_enqueued)
    self.assertEqual('mytask2', t2.name)
    self.assertFalse(t3.was_enqueued)
    self.assertEqual('mytask3', t3.name)

  def testBulkAddTaskResultErrors(self):
    """Tests that BulkAdd() TaskResult errors are mapped to exceptions."""
    self.RunBulkAddTaskResultError(TaskQueueServiceError.UNKNOWN_QUEUE,
                                   taskqueue.UnknownQueueError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.TRANSIENT_ERROR,
                                   taskqueue.TransientError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.INTERNAL_ERROR,
                                   taskqueue.InternalError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.TASK_TOO_LARGE,
                                   taskqueue.TaskTooLargeError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.INVALID_TASK_NAME,
                                   taskqueue.InvalidTaskNameError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.INVALID_QUEUE_NAME,
                                   taskqueue.InvalidQueueNameError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.INVALID_URL,
                                   taskqueue.InvalidUrlError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.INVALID_QUEUE_RATE,
                                   taskqueue.InvalidQueueError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.PERMISSION_DENIED,
                                   taskqueue.PermissionDeniedError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.TASK_ALREADY_EXISTS,
                                   taskqueue.TaskAlreadyExistsError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.TOMBSTONED_TASK,
                                   taskqueue.TombstonedTaskError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.INVALID_ETA,
                                   taskqueue.InvalidEtaError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.INVALID_REQUEST,
                                   taskqueue.Error)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.UNKNOWN_TASK,
                                   taskqueue.Error)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.TOMBSTONED_QUEUE,
                                   taskqueue.Error)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.DUPLICATE_TASK_NAME,
                                   taskqueue.DuplicateTaskNameError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.TOO_MANY_TASKS,
                                   taskqueue.TooManyTasksError)






    self.RunBulkAddTaskResultError(TaskQueueServiceError.DATASTORE_ERROR,
                                   taskqueue.DatastoreError)
    self.RunBulkAddTaskResultError(TaskQueueServiceError.DATASTORE_ERROR,
                                   datastore_errors.Error)

  def testAddPullTasksMultipleResults(self):
    """Tests adding multiple tasks in a call."""

    def SetResponse(service, method, request, response):
      task_result1 = response.taskresult.add()
      task_result1.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result2 = response.taskresult.add()
      task_result2.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result3 = response.taskresult.add()
      task_result3.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request1 = expected_request.add_request.add()
    add_request1.queue_name = b'Aqueue'
    add_request1.task_name = b'A'
    add_request1.eta_usec = self.now_timestamp_usec
    add_request1.mode = taskqueue_service_pb2.TaskQueueMode.PULL
    add_request1.body = b'123'

    add_request2 = expected_request.add_request.add()
    add_request2.queue_name = b'Aqueue'
    add_request2.task_name = b'B'
    add_request2.eta_usec = self.now_timestamp_usec
    add_request2.mode = taskqueue_service_pb2.TaskQueueMode.PULL
    add_request2.body = b'456'

    add_request3 = expected_request.add_request.add()
    add_request3.queue_name = b'Aqueue'
    add_request3.task_name = b'C'
    add_request3.eta_usec = self.now_timestamp_usec
    add_request3.mode = taskqueue_service_pb2.TaskQueueMode.PULL
    add_request3.body = b'789'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    task1 = Task(name='A', eta=self.now, payload='123', method='PULL')
    task2 = Task(name='B', eta=self.now, payload='456', method='PULL')
    task3 = Task(name='C', eta=self.now, payload='789', method='PULL')
    tasks = [task1, task2, task3]
    queue = Queue('Aqueue')
    self.mox.ReplayAll()
    t = self.Add(queue, tasks)
    self.mox.VerifyAll()

    self.assertTrue(t[0].was_enqueued)
    self.assertTrue(t[1].was_enqueued)
    self.assertTrue(t[2].was_enqueued)

  def testPullTaskSingleTaskWithPayload(self):
    """Tests adding a pull task with payload data."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = expected_request.add_request.add()
    add_request.queue_name = b'default'
    add_request.task_name = b'T'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PULL
    add_request.body = self.payload

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    task = Task(name='T', payload=self.payload, eta=self.now, method='PULL')
    queue = Queue()
    t = self.Add(queue, task)
    self.mox.VerifyAll()

    self.assertTrue(t.was_enqueued)

  def testPullTaskWithoutPayload(self):
    """Tests adding a pull task that without payload data."""

    self.assertRaises(InvalidTaskError,
                      Task,
                      eta=self.now,
                      method='PULL')

  def testPullTaskWithUrl(self):
    """Tests adding pull task with url."""
    self.assertRaises(InvalidTaskError, Task,
                      payload=self.payload,
                      eta=self.now,
                      url='/useless_url',
                      method='PULL')

  def testPullTaskWithPayloadAndParams(self):
    """Tests adding pull task with both payload and params."""
    self.assertRaises(InvalidTaskError, Task,
                      payload=self.payload,
                      eta=self.now,
                      params={'A': 'b',
                              'B': 'a'},
                      method='PULL')

  def testPullTaskWithHeaders(self):
    """Tests adding pull task with headers."""
    self.assertRaises(InvalidTaskError, Task,
                      payload=self.payload,
                      eta=self.now,
                      headers={'A': 'b',
                               'B': 'a'},
                      method='PULL')

  def testPullTaskNoName(self):
    """Tests adding task that doesn't have task name."""

    def SetResponse(service, method, request, response):
      task_result1 = response.taskresult.add()
      task_result1.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result1.chosen_task_name = b'GENERATED-NAME'
      task_result2 = response.taskresult.add()
      task_result2.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request1 = expected_request.add_request.add()
    add_request1.queue_name = b'default'
    add_request1.task_name = b''
    add_request1.eta_usec = self.now_timestamp_usec
    add_request1.mode = taskqueue_service_pb2.TaskQueueMode.PULL
    add_request1.body = b'55555'
    add_request2 = expected_request.add_request.add()
    add_request2.queue_name = b'default'
    add_request2.eta_usec = self.now_timestamp_usec
    add_request2.task_name = b'NAME'
    add_request2.mode = taskqueue_service_pb2.TaskQueueMode.PULL
    add_request2.body = b'4444'

    self.MockSuccessfulRPC(expected_request, SetResponse)

    queue = Queue()
    task1 = Task(eta=self.now, payload='55555', method='PULL')
    task2 = Task(eta=self.now, name='NAME', payload='4444', method='PULL')
    tasks = [task1, task2]
    self.mox.ReplayAll()
    t = self.Add(queue, tasks)
    self.mox.VerifyAll()

    self.assertTrue(t[0].was_enqueued)
    self.assertEqual(t[0].name, 'GENERATED-NAME')
    self.assertTrue(t[1].was_enqueued)
    self.assertEqual(t[1].name, 'NAME')

  def testPullTasksWithTag(self):
    tags = [
        None, '', 'My test Tag', u'\u30cb\u30e3\u30f3', '\x00\x01\x02\x03']

    def SetResponse(service, method, request, response):
      for _ in request.add_request:
        task_result = response.taskresult.add()
        task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    for i, tag in enumerate(tags):
      add_request = expected_request.add_request.add()
      add_request.queue_name = b'default'
      add_request.task_name = b'task-%d' % i
      add_request.eta_usec = self.now_timestamp_usec
      add_request.mode = taskqueue_service_pb2.TaskQueueMode.PULL
      add_request.body = self.payload
      if tag:
        if isinstance(tag, six.text_type):
          add_request.tag = tag.encode('utf-8')
        else:
          add_request.tag = tag


    expected_request.ByteSize()

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()

    tasks = []
    for i, tag in enumerate(tags):
      tasks.append(Task(name='task-%d' % i,
                        payload=self.payload,
                        eta=self.now,
                        method='PULL',
                        tag=tag))

    self.Add(Queue(), tasks)
    self.mox.VerifyAll()

    for task in tasks:
      self.assertTrue(task.was_enqueued)

  def testPullTasksWithOversizedTag(self):
    self.assertRaises(
        taskqueue.InvalidTagError,
        Task, payload=self.payload, method='PULL', tag='a'*501)

  def testTaskAddCallsAsync(self):
    """Test Task's add method calls add_async."""
    dummy_result = object()

    rpc = self.mox.CreateMockAnything()
    rpc.get_result().AndReturn(dummy_result)

    def AddAsync(queue_name, transactional):
      self.assertEqual(queue_name, 'jobs')
      self.assertTrue(transactional)
      return rpc

    task = Task()
    task.add_async = AddAsync

    self.mox.ReplayAll()
    result = task.add('jobs', True)
    self.mox.VerifyAll()

    self.assertIs(result, dummy_result)

  def testAddCallsAsync(self):
    """Test Queue's add method calls add_async."""
    dummy_task = object()
    dummy_result = object()

    rpc = self.mox.CreateMockAnything()
    rpc.get_result().AndReturn(dummy_result)

    def AddAsync(task, transactional):
      self.assertIs(task, dummy_task)
      self.assertTrue(transactional)
      return rpc

    queue = Queue('backlog')
    queue.add_async = AddAsync

    self.mox.ReplayAll()
    result = queue.add(dummy_task, True)
    self.mox.VerifyAll()

    self.assertIs(result, dummy_result)


class AsyncQueueAddTest(QueueAddTest):
  """Tests for Queue.add_async method.

  This will run all the tests in the superclass.
  """

  def Add(self, queue, *args, **kwargs):
    """Exercise Queue's asynchronous method add_async."""
    self.assertIsInstance(queue, Queue)
    return queue.add_async(*args, **kwargs).get_result()

  def TaskAdd(self, task, *args, **kwargs):
    """Exercise Task's asynchronous method add_async."""
    self.assertIsInstance(task, Task)
    return task.add_async(*args, **kwargs).get_result()

  def testAddAsyncUsesRpc(self):
    """Test add_async returns supplied rpc."""

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    rpc.make_call('BulkAdd',
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None)

    queue = Queue('jobs')
    task = Task(name='run')
    self.mox.ReplayAll()
    returned_rpc = queue.add_async(task, rpc=rpc)
    self.mox.VerifyAll()

    self.assertIs(returned_rpc, rpc)

  def testTaskAddAsyncUsesRpc(self):
    """Test Task add_async returns supplied rpc."""

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    rpc.make_call('BulkAdd',
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None)

    task = Task(name='my-task')
    self.mox.ReplayAll()
    returned_rpc = task.add_async('my-queue', rpc=rpc)
    self.mox.VerifyAll()

    self.assertIs(returned_rpc, rpc)


class QueueTransactionalAddTest(HttpEnvironTest):
  """Tests for the Queue class and anything that puts Tasks in a queue."""
  APP_ID = 'app'

  def setUp(self):
    """Sets up the test harness."""
    HttpEnvironTest.setUp(self)
    self.now = datetime.datetime(2009, 5, 5, 21, 50, 28, 517317)
    self.now_timestamp_usec = 1241560228517317
    self.params = {'one': 'two'}
    self.headers = {'red': 'blue', 'five': 'six'}
    self.tx_handle = 42
    self.payload = 'some-data'

    full_app_id.put(self.APP_ID)
    self.mox = mox.Mox()
    self.mox.StubOutWithMock(apiproxy_stub_map, 'CreateRPC')

  def tearDown(self):
    """Tears down the test harness."""
    self.mox.ResetAll()
    self.mox.UnsetStubs()
    HttpEnvironTest.tearDown(self)

  def Add(self, queue, *args, **kwargs):
    """Exercise the synchronous method add."""
    return queue.add(*args, **kwargs)

  def TaskAdd(self, task, *args, **kwargs):
    """Exercise Task's synchronous method add."""
    self.assertIsInstance(task, Task)
    return task.add(*args, **kwargs)

  def testInTransaction(self):
    """Tests adding a Task in a transaction."""

    def SetDatastoreResponse(service, method, request, response):
      response.app = 'app'
      response.handle = self.tx_handle

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK
      task_result.chosen_task_name = b'AUTO-ASSIGNED'

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b''
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default'
    add_request.transaction.app = self.APP_ID
    add_request.transaction.handle = self.tx_handle

    apiproxy_stub_map.CreateRPC('datastore_v3',
                                mox.IgnoreArg()).WithSideEffects(
                                    functools.partial(
                                        MockRPC,
                                        populate_response=SetDatastoreResponse))
    apiproxy_stub_map.CreateRPC('taskqueue',
                                mox.IgnoreArg()).WithSideEffects(
                                    functools.partial(
                                        MockRPC,
                                        expected_request=expected_request,
                                        populate_response=SetResponse))
    apiproxy_stub_map.CreateRPC('datastore_v3',
                                mox.IgnoreArg()).WithSideEffects(MockRPC)

    self.mox.ReplayAll()

    t = datastore.RunInTransaction(
        lambda: self.TaskAdd(Task(eta=self.now), transactional=True))
    self.mox.VerifyAll()
    self.assertTrue(t.was_enqueued)
    self.assertEqual('AUTO-ASSIGNED', t.name)
    self.assertEqual('default', t.queue_name)

  def testInTransactionWithTaskName(self):
    """Tests adding a named Task in a transaction."""

    def transaction():
      q = Queue()
      self.Add(q,
               task=[Task(eta=self.now), Task(name='hello')],
               transactional=True)

    apiproxy_stub_map.CreateRPC('datastore_v3',
                                mox.IgnoreArg()).WithSideEffects(MockRPC)
    apiproxy_stub_map.CreateRPC('datastore_v3',
                                mox.IgnoreArg()).WithSideEffects(MockRPC)

    self.mox.ReplayAll()
    self.assertRaises(taskqueue.InvalidTaskNameError,
                      datastore.RunInTransaction, transaction)
    self.mox.VerifyAll()

  def testInTransactionWithNonTransactionalAdd(self):
    """Tests adding a Task in a transaction with transactional set to False."""

    def SetResponse(service, method, request, response):
      task_result = response.taskresult.add()
      task_result.result = taskqueue_service_pb2.TaskQueueServiceError.OK

    expected_request = taskqueue_service_pb2.TaskQueueBulkAddRequest()
    add_request = _InitAddRequest(expected_request)
    add_request.task_name = b'mytask'
    add_request.queue_name = b'default'
    add_request.eta_usec = self.now_timestamp_usec
    add_request.method = taskqueue_service_pb2.TaskQueueAddRequest.POST
    add_request.mode = taskqueue_service_pb2.TaskQueueMode.PUSH
    add_request.url = b'/_ah/queue/default'

    apiproxy_stub_map.CreateRPC('datastore_v3',
                                mox.IgnoreArg()).WithSideEffects(MockRPC)
    apiproxy_stub_map.CreateRPC('taskqueue',
                                mox.IgnoreArg()).WithSideEffects(
                                    functools.partial(
                                        MockRPC,
                                        expected_request=expected_request,
                                        populate_response=SetResponse))
    apiproxy_stub_map.CreateRPC('datastore_v3',
                                mox.IgnoreArg()).WithSideEffects(MockRPC)

    self.mox.ReplayAll()
    task = Task(eta=self.now, name='mytask')
    result_task = datastore.RunInTransaction(
        lambda: self.TaskAdd(task, transactional=False))
    self.mox.VerifyAll()
    self.assertIs(result_task, task)
    self.assertTrue(task.was_enqueued)
    self.assertEqual('mytask', task.name)
    self.assertEqual('default', task.queue_name)

  def testInTransactionRequestTooLarge(self):
    """Tests adding too many large Tasks in a transaction."""
    longstring = 'a' * (taskqueue.MAX_PULL_TASK_SIZE_BYTES - 1024)

    def transaction():
      q = Queue()
      self.Add(
          q, [Task(method='PULL', payload=longstring) for _ in range(3)],
          transactional=True)

    apiproxy_stub_map.CreateRPC('datastore_v3',
                                mox.IgnoreArg()).WithSideEffects(MockRPC)
    apiproxy_stub_map.CreateRPC('datastore_v3',
                                mox.IgnoreArg()).WithSideEffects(MockRPC)

    self.mox.ReplayAll()
    self.assertRaises(taskqueue.TransactionalRequestTooLargeError,
                      datastore.RunInTransaction, transaction)
    self.mox.VerifyAll()


class AsyncQueueTransactionalAddTest(QueueTransactionalAddTest):
  """Tests for Queue.add_async method with transactions.

  This will run all the tests in the superclass.
  """

  def Add(self, queue, *args, **kwargs):
    """Exercise the asynchronous method add_async."""
    self.assertIsInstance(queue, Queue)
    return queue.add_async(*args, **kwargs).get_result()

  def TaskAdd(self, task, *args, **kwargs):
    """Exercise Task's asynchronous method add_async."""
    self.assertIsInstance(task, Task)
    return task.add_async(*args, **kwargs).get_result()


class QueueTest(absltest.TestCase):
  """Tests non-adding methods of the Queue class."""

  def testAccessors(self):
    """Tests getting a Queue's name."""
    queue = Queue('meepa')
    self.assertEqual('meepa', queue.name)

  def testQueueNameTooLong(self):
    """Tests when the queue name is too long."""
    self.assertRaises(
        taskqueue.InvalidQueueNameError, Queue, 'a' *
        (taskqueue.MAX_QUEUE_NAME_LENGTH + 1))

  def testQueueNamePattern(self):
    """Tests that the queue name is validated."""
    self.assertRaises(
        taskqueue.InvalidQueueNameError, Queue, 'bad.')
    self.assertRaises(
        taskqueue.InvalidQueueNameError, Queue, 'ba/d')
    self.assertRaises(
        taskqueue.InvalidQueueNameError, Queue, 'ba_d')
    self.assertRaises(
        taskqueue.InvalidQueueNameError, Queue, 'ba$d')
    Queue(name='good')
    Queue(name='GooD')
    Queue(name='Go-oD')
    Queue(name='-GooD')
    Queue(name='GooD-')
    Queue(name='1234')
    Queue(name='1234-foo')

  def testDefaultName(self):
    queue = Queue()
    self.assertEqual(queue.name, 'default')

  def testEqMethod(self):
    queue_names = ('default', 'queue-0', 'good', 'GooD')
    for queue_name in queue_names:
      q1 = Queue(queue_name)
      q2 = Queue(queue_name)
      self.assertEqual(q1, q2)

    for name1, name2 in zip(queue_names, queue_names[1:]):
      q1 = Queue(name1)
      q2 = Queue(name2)
      self.assertNotEqual(q1, q2)


class QueueStatisticsTest(absltest.TestCase):
  """Tests the FetchQueueStats calls."""

  def setUp(self):
    self.mox = mox.Mox()
    self.mox.StubOutWithMock(apiproxy_stub_map, 'UserRPC')

  def tearDown(self):
    self.mox.ResetAll()
    self.mox.UnsetStubs()

  def Fetch(self, *args, **kwargs):
    """Exercise the synchronous method QueueStatistics.fetch."""
    return QueueStatistics.fetch(*args, **kwargs)

  def FetchStatistics(self, queue, *args, **kwargs):
    """Exercise the synchronous method fetch_statistics."""
    return queue.fetch_statistics(*args, **kwargs)

  def MockSuccessfulRPC(self, expected_request, populate_response):
    """Mock an asynchronous FetchQueueStats call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC result available to the caller."""
      populate_response(method, request, response)

      rpc.response = response
      rpc.get_result = lambda: get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('FetchQueueStats',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success()

  def MockUnsuccessfulRPC(self, expected_request, error_code):
    """Mock a failing asynchronous FetchQueueStats call, made synchronous."""

    def SetResponse(method, request, response, get_result_hook, user_data):
      """Make the RPC failure result available to the caller."""
      rpc.response = response
      get_result_hook(rpc)

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    apiproxy_stub_map.UserRPC('taskqueue', mox.IgnoreArg(), None).AndReturn(rpc)
    rpc.make_call('FetchQueueStats',
                  expected_request,
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None).WithSideEffects(SetResponse)
    rpc.check_success().AndRaise(apiproxy_errors.ApplicationError(
        error_code, ''))

  def testEq(self):
    queue = Queue()
    stat1 = QueueStatistics(queue, 10, 20)
    stat2 = QueueStatistics(queue, 10, 20)
    self.assertEqual(stat1, stat2)

  def testNoQueues(self):

    self.assertEqual([], QueueStatistics.fetch([]))

  def testSingleQueueNoList(self):
    queue = Queue('default')

    def SetResponse(method, request, response):
      queue_stat = response.queuestats.add()
      queue_stat.num_tasks = 10
      queue_stat.oldest_eta_usec = 20

    expected_request = taskqueue_service_pb2.TaskQueueFetchQueueStatsRequest()
    expected_request.queue_name.append(queue.name.encode('utf8'))

    expected_result = QueueStatistics(
        queue=queue,
        tasks=10,
        oldest_eta_usec=20)

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    result = self.Fetch(queue)

    self.assertEqual(result, expected_result)

  def testSingleStringNoList(self):
    queue = Queue('default')

    def SetResponse(method, request, response):
      queue_stat = response.queuestats.add()
      queue_stat.num_tasks = 10
      queue_stat.oldest_eta_usec = -1

    expected_request = taskqueue_service_pb2.TaskQueueFetchQueueStatsRequest()
    expected_request.queue_name.append(queue.name.encode('utf8'))

    expected_result = QueueStatistics(
        queue=queue,
        tasks=10,
        oldest_eta_usec=None)

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    result = self.Fetch(queue.name)

    self.assertEqual(result, expected_result)

  def testQueueShortcutMethod(self):
    queue = Queue('default')

    def SetResponse(method, request, response):
      queue_stat = response.queuestats.add()
      queue_stat.num_tasks = 10
      queue_stat.oldest_eta_usec = 20

    expected_request = taskqueue_service_pb2.TaskQueueFetchQueueStatsRequest()
    expected_request.queue_name.append(queue.name.encode('utf8'))

    expected_result = QueueStatistics(
        queue=queue,
        tasks=10,
        oldest_eta_usec=20)

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    result = self.FetchStatistics(queue)

    self.assertEqual(result, expected_result)

  def testMultipleQueues(self):
    self.PerformTestWithMultipleQueues(3, use_strings=False)

  def testSingleQueue(self):
    self.PerformTestWithMultipleQueues(1, use_strings=False)

  def testMultipleQueuesWithStrings(self):
    self.PerformTestWithMultipleQueues(3, use_strings=True)

  def testSingleQueueWithStrings(self):
    self.PerformTestWithMultipleQueues(1, use_strings=True)

  def PerformTestWithMultipleQueues(self, number_of_queues, use_strings):
    queues = [Queue('queue-%d' % i) for i in range(number_of_queues)]

    def SetResponse(method, request, response):
      for i in range(number_of_queues):
        queue_stat = response.queuestats.add()
        queue_stat.num_tasks = 11 + i
        queue_stat.oldest_eta_usec = 22 + i

    expected_request = taskqueue_service_pb2.TaskQueueFetchQueueStatsRequest()
    for queue in queues:
      expected_request.queue_name.append(queue.name.encode('utf8'))

    expected_result = []
    for i, queue in enumerate(queues):
      expected_result.append(QueueStatistics(
          queue=queue,
          tasks=11+i,
          oldest_eta_usec=22+i))

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    if use_strings:
      result = self.Fetch(queues)
    else:
      result = self.Fetch([queue.name for queue in queues])
    self.assertEqual(result, expected_result)

  def testQueueWithScannerInfo(self):
    queue = Queue('default')

    def SetResponse(method, request, response):
      queue_stat = response.queuestats.add()
      queue_stat.num_tasks = 10
      queue_stat.oldest_eta_usec = 87654321
      scanner_info = queue_stat.scanner_info
      scanner_info.executed_last_minute = 1234
      scanner_info.executed_last_hour = 123456789
      scanner_info.requests_in_flight = int(101.23)

    expected_request = taskqueue_service_pb2.TaskQueueFetchQueueStatsRequest()
    expected_request.queue_name.append(queue.name.encode('utf8'))

    expected_result = QueueStatistics(
        queue=queue,
        tasks=10,
        oldest_eta_usec=87654321,
        executed_last_minute=1234,
        in_flight=int(101.23))

    self.MockSuccessfulRPC(expected_request, SetResponse)

    self.mox.ReplayAll()
    result = self.FetchStatistics(queue)

    self.assertEqual(result, expected_result)

  def testPermissionError(self):
    queue = Queue('forbidden')
    expected_request = taskqueue_service_pb2.TaskQueueFetchQueueStatsRequest()
    expected_request.queue_name.append(queue.name.encode('utf8'))

    self.MockUnsuccessfulRPC(expected_request,
                             TaskQueueServiceError.PERMISSION_DENIED)

    self.mox.ReplayAll()
    self.assertRaises(
        taskqueue.PermissionDeniedError, self.Fetch, queue)
    self.mox.VerifyAll()

  def testFetchBadDeadline(self):
    """Tests fetch with a null deadline."""

    self.assertRaises(TypeError,
                      QueueStatistics.fetch,
                      Queue('default'),
                      deadline=None)

  def testFetchStatisticsBadDeadline(self):
    """Tests fetch_statistics with a null deadline."""

    self.assertRaises(TypeError,
                      Queue('default').fetch_statistics,
                      deadline=None)

  def testFetchStatisticsCallsAsync(self):
    """Test fetch_statistics calls fetch_statistics_async."""
    dummy_result = object()

    rpc = self.mox.CreateMockAnything()
    rpc.get_result().AndReturn(dummy_result)
    apiproxy_stub_map.UserRPC('taskqueue', 8, None).AndReturn(rpc)

    def FetchStatisticsAsync(optional_rpc):
      self.assertIs(optional_rpc, rpc)
      return rpc

    queue = Queue('backlog')
    queue.fetch_statistics_async = FetchStatisticsAsync

    self.mox.ReplayAll()
    result = self.FetchStatistics(queue, deadline=8)
    self.mox.VerifyAll()

    self.assertIs(result, dummy_result)


class AsyncQueueStatisticsTest(QueueStatisticsTest):
  """Tests the asynchronous FetchQueueStats calls.

  This will run all the tests in the superclass.
  """

  def Fetch(self, queue_or_queues, deadline=None):
    """Exercise the asynchronous method QueueStatistics.fetch_async."""
    if deadline is None:
      return QueueStatistics.fetch_async(queue_or_queues).get_result()
    else:
      rpc = taskqueue.create_rpc(deadline=deadline)
      returned_rpc = QueueStatistics.fetch_async(queue_or_queues, rpc)
      self.assertIs(returned_rpc, rpc)
      return rpc.get_result()

  def FetchStatistics(self, queue, deadline=None):
    """Exercise the asynchronous method fetch_statistics_async."""
    if deadline is None:
      return queue.fetch_statistics_async().get_result()
    else:
      rpc = taskqueue.create_rpc(deadline=deadline)
      returned_rpc = queue.fetch_statistics_async(rpc)
      self.assertIs(returned_rpc, rpc)
      return rpc.get_result()

  def testFetchAsyncUsesRpc(self):
    """Test fetch_async returns supplied rpc."""

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    rpc.make_call('FetchQueueStats',
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None)

    queue = Queue('jobs')
    self.mox.ReplayAll()
    returned_rpc = QueueStatistics.fetch_async(queue, rpc)
    self.mox.VerifyAll()

    self.assertIs(returned_rpc, rpc)

  def testFetchStatisticsAsyncUsesRpc(self):
    """Test fetch_statistics_async returns supplied rpc."""

    rpc = self.mox.CreateMockAnything()
    rpc.service = 'taskqueue'
    rpc.make_call('FetchQueueStats',
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  mox.IgnoreArg(),
                  None)

    queue = Queue('jobs')
    self.mox.ReplayAll()
    returned_rpc = queue.fetch_statistics_async(rpc)
    self.mox.VerifyAll()

    self.assertIs(returned_rpc, rpc)


@ctx_test_util.isolated_context()
class TestNamespace(absltest.TestCase):
  """Taskqueue namespace tests."""

  def setUp(self):
    """Sets up the test harness."""
    HttpEnvironTest.setUp(self)

  def assertExpectedTaskHeaders(self, header_overrides, task_headers):
    expected_headers = _base_headers.copy()
    expected_headers.update(header_overrides)
    self.assertEqual(expected_headers, task_headers)

  def testNoNamespaceManagerState(self):
    """Context is empty."""
    t = Task()
    self.assertExpectedTaskHeaders({}, t.headers)

  def testHasDefaultNamespace(self):
    """Context has default namespace."""
    os.environ['HTTP_X_APPENGINE_DEFAULT_NAMESPACE'] = 'request-namespace'
    t = Task()
    self.assertExpectedTaskHeaders(
        {'X-AppEngine-Current-Namespace': '',
         'X-AppEngine-Default-Namespace': 'request-namespace'},
        t.headers)

  def testHasCurrentNamespace(self):
    """Context has a current default namespace."""
    os.environ['HTTP_X_APPENGINE_CURRENT_NAMESPACE'] = 'current-namespace'
    t = Task()
    self.assertExpectedTaskHeaders(
        {'X-AppEngine-Current-Namespace': 'current-namespace'},
        t.headers)

  def testHasCurrentAndDefaultNamespace(self):
    """Context has a current and a request namespace."""
    os.environ['HTTP_X_APPENGINE_DEFAULT_NAMESPACE'] = 'request-namespace'
    os.environ['HTTP_X_APPENGINE_CURRENT_NAMESPACE'] = 'current-namespace'
    t = Task()
    self.assertExpectedTaskHeaders(
        {'X-AppEngine-Current-Namespace': 'current-namespace',
         'X-AppEngine-Default-Namespace': 'request-namespace'},
        t.headers)

  def testDoesNotOverrideHeaders(self):
    """Do not override headers in specified Task headers."""
    os.environ['HTTP_X_APPENGINE_DEFAULT_NAMESPACE'] = 'request-namespace'
    os.environ['HTTP_X_APPENGINE_CURRENT_NAMESPACE'] = 'current-namespace'
    testheaders = {'X-AppEngine-Current-Namespace': '',
                   'AontherHeader': 'another-value'}
    t = Task(headers=testheaders)
    testheaders['X-AppEngine-Default-Namespace'] = 'request-namespace'
    self.assertExpectedTaskHeaders(testheaders, t.headers)

  def testDoesNotOverrideAnyHeaders(self):
    """Do not override any headers in specified Task headers."""
    os.environ['HTTP_X_APPENGINE_DEFAULT_NAMESPACE'] = 'request-namespace'
    os.environ['HTTP_X_APPENGINE_CURRENT_NAMESPACE'] = 'current-namespace'
    testheaders = {'X-AppEngine-Current-Namespace': '',
                   'X-AppEngine-Default-Namespace': 'abc-def',
                   'AontherHeader': 'another-value'}
    t = Task(headers=testheaders)
    self.assertExpectedTaskHeaders(testheaders, t.headers)


class ModifyTaskLeaseTest(absltest.TestCase):
  """Tests for Queue.modify_task_lease method."""

  def setUp(self):
    """Sets up the test harness."""
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.mox = mox.Mox()
    self.mox.StubOutWithMock(apiproxy_stub_map.apiproxy, 'MakeSyncCall')
    self.now_timestamp = time.time()

  def tearDown(self):
    """Tears down the test harness."""
    self.mox.ResetAll()
    self.mox.UnsetStubs()

  def testEtaAccuracy(self):
    """Tests that a task's eta_usec can be recovered exactly from eta_posix."""
    task = Task(payload='bar', method='PULL', name='foo')


    for i in range(1000000):
      eta_usec = 1023456789000000 + i
      task._Task__eta_posix = eta_usec * 1e-6
      self.assertEqual(task._eta_usec, eta_usec)

  def testModifyLease(self):
    """Tests successfully modifying the lease on a task."""

    current_eta_seconds = 1
    lease_seconds = 10

    def SetResponse(service, method, request, response):
      response.updated_eta_usec = SecToUsec(lease_seconds)

    expected_request = taskqueue_service_pb2.TaskQueueModifyTaskLeaseRequest()
    expected_request.queue_name = b'default'
    expected_request.task_name = b'foo'
    expected_request.lease_seconds = lease_seconds
    expected_request.eta_usec = SecToUsec(current_eta_seconds)

    apiproxy_stub_map.apiproxy.MakeSyncCall(
        'taskqueue',
        'ModifyTaskLease',
        expected_request,
        mox.IgnoreArg()).WithSideEffects(SetResponse)

    self.mox.ReplayAll()
    task = Task(payload='bar', method='PULL', name='foo')
    task._Task__queue_name = 'default'
    task._Task__eta_posix = current_eta_seconds
    Queue('default').modify_task_lease(task, lease_seconds)
    self.mox.VerifyAll()

    self.assertEqual(lease_seconds, task._Task__eta_posix)

  def testModifyTaskLeaseOnPushQueue(self):
    """Tests modifying a task from a push queue."""

    expected_request = taskqueue_service_pb2.TaskQueueModifyTaskLeaseRequest()
    expected_request.queue_name = b'default'
    expected_request.eta_usec = SecToUsec(1)
    expected_request.task_name = b'foo'
    expected_request.lease_seconds = 10

    apiproxy_stub_map.MakeSyncCall(
        'taskqueue',
        'ModifyTaskLease',
        expected_request,
        mox.IgnoreArg()).AndRaise(
            apiproxy_errors.ApplicationError(
                TaskQueueServiceError.INVALID_QUEUE_MODE, ''))

    q = Queue('default')
    task = Task(payload='bar', method='PULL', name='foo')
    task._Task__queue_name = 'default'
    task._Task__eta_posix = 1
    self.mox.ReplayAll()
    self.assertRaises(taskqueue.InvalidQueueModeError,
                      q.modify_task_lease, task, 10)
    self.mox.VerifyAll()

  def testModifyTaskLeaseExpiredLease(self):
    """Tests modifying the lease of the task with an expired lease."""

    expected_request = taskqueue_service_pb2.TaskQueueModifyTaskLeaseRequest()
    expected_request.queue_name = b'default'
    expected_request.eta_usec = SecToUsec(1)
    expected_request.task_name = b'foo'
    expected_request.lease_seconds = 10

    apiproxy_stub_map.MakeSyncCall(
        'taskqueue',
        'ModifyTaskLease',
        expected_request,
        mox.IgnoreArg()).AndRaise(
            apiproxy_errors.ApplicationError(
                TaskQueueServiceError.TASK_LEASE_EXPIRED, ''))

    q = Queue('default')
    task = Task(payload='bar', method='PULL', name='foo')
    task._Task__queue_name = 'default'
    task._Task__eta_posix = 1
    self.mox.ReplayAll()
    self.assertRaises(taskqueue.TaskLeaseExpiredError,
                      q.modify_task_lease, task, 10)
    self.mox.VerifyAll()

  def testModifyTaskLeaseQueuePaused(self):
    """Tests modifing task lease from a paused queue."""

    expected_request = taskqueue_service_pb2.TaskQueueModifyTaskLeaseRequest()
    expected_request.queue_name = b'default'
    expected_request.eta_usec = SecToUsec(1)
    expected_request.task_name = b'foo'
    expected_request.lease_seconds = 10

    apiproxy_stub_map.MakeSyncCall(
        'taskqueue',
        'ModifyTaskLease',
        expected_request,
        mox.IgnoreArg()).AndRaise(
            apiproxy_errors.ApplicationError(
                TaskQueueServiceError.QUEUE_PAUSED, ''))

    q = Queue('default')
    task = Task(payload='bar', method='PULL', name='foo')
    task._Task__queue_name = 'default'
    task._Task__eta_posix = 1
    self.mox.ReplayAll()
    self.assertRaises(taskqueue.QueuePausedError,
                      q.modify_task_lease, task, 10)
    self.mox.VerifyAll()

  def testModifyTaskLeaseNegativeLeaseTime(self):
    """Tests modify_task_lease with a negative lease time value."""
    q = Queue('default')
    task = Task(payload='bar', method='PULL', name='foo')
    task._Task__queue_name = 'default'
    task._Task__eta_posix = 1
    self.assertRaises(taskqueue.InvalidLeaseTimeError,
                      q.modify_task_lease, task, -1)

  def testModifyTaskLeaseTooLargeLeaseTime(self):
    """Tests modify_task_lease with too large lease time value."""
    q = Queue('default')
    task = Task(payload='bar', method='PULL', name='foo')
    task._Task__queue_name = 'default'
    task._Task__eta_posix = 1
    self.assertRaises(taskqueue.InvalidLeaseTimeError,
                      q.modify_task_lease, task, 86400 * 30.0)

  def testModifyTaskLeaseInvalidLeaseTime(self):
    """Tests modify_task_lease with lease_seconds of incorrect type."""
    q = Queue('default')
    task = Task(payload='bar', method='PULL', name='foo')
    task._Task__queue_name = 'default'
    task._Task__eta_posix = 1
    self.assertRaises(TypeError,
                      q.modify_task_lease, task, '100')


class ModuleInterfaceTest(module_testutil.ModuleInterfaceTest,
                          absltest.TestCase):
  """Verify the module interface is correctly exported.

  This validates that all attributes in __all__ are present in the module, and
  that no private atributes are accidently exported.

  Note: All tests are inherited from module_testutil.ModuleInterfaceTest.
  """

  MODULE = taskqueue





def main(argv):
  absltest.main()


if __name__ == '__main__':
  absltest.main(main)
