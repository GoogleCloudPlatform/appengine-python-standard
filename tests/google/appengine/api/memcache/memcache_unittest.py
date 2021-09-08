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

"""Unit-test for google.appengine.api.memcache module.

This tests that google.appengine.api.memcache sets up request protos
correctly, and returns the correct results assuming faked response protos.
"""

import collections
import hashlib
import os

import google

import mock
import six
from six.moves import range
import six.moves.cPickle

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import memcache
from google.appengine.api import namespace_manager
from google.appengine.api.memcache import memcache_service_pb2
from google.appengine.runtime import apiproxy_errors
from google.protobuf import text_format
from absl.testing import absltest




if six.PY3:
  long = int


MemcacheSetResponse = memcache_service_pb2.MemcacheSetResponse
MemcacheSetRequest = memcache_service_pb2.MemcacheSetRequest

MemcacheGetResponse = memcache_service_pb2.MemcacheGetResponse
MemcacheGetRequest = memcache_service_pb2.MemcacheGetRequest

MemcacheIncrementResponse = memcache_service_pb2.MemcacheIncrementResponse
MemcacheIncrementRequest = memcache_service_pb2.MemcacheIncrementRequest

MemcacheBatchIncrementResponse = memcache_service_pb2.MemcacheBatchIncrementResponse
MemcacheBatchIncrementRequest = memcache_service_pb2.MemcacheBatchIncrementRequest

MemcacheDeleteResponse = memcache_service_pb2.MemcacheDeleteResponse
MemcacheDeleteRequest = memcache_service_pb2.MemcacheDeleteRequest

MemcacheFlushResponse = memcache_service_pb2.MemcacheFlushResponse
MemcacheFlushRequest = memcache_service_pb2.MemcacheFlushRequest

MemcacheStatsRequest = memcache_service_pb2.MemcacheStatsRequest
MergedNamespaceStats = memcache_service_pb2.MergedNamespaceStats
MemcacheStatsResponse = memcache_service_pb2.MemcacheStatsResponse

INITIAL_ENVIRON = dict(os.environ)
ONE_MEGABYTE = 1024 * 1024


def MakeArbitraryGetRequest():
  """Makes an arbitrary MemcacheGetRequest.

  The request is arbitrary in that every field is set to a valid value, but the
  caller should not depened on anything other than the presence. Instead,
  callers should set/clear what's important to their test case.

  Returns:
    An arbitrary MemcacheGetRequest.
  """
  request = MemcacheGetRequest()
  body = """
    key: "test-key"
    name_space: "unused-namespace"
    for_cas: false
    override <
      app_id: "override-app"
    >
    """
  return text_format.Parse(body, request)


class MemcacheNamespaceTest(absltest.TestCase):

  def tearDown(self):
    """Restore environment."""
    os.environ = dict(INITIAL_ENVIRON)

  def testAddNamespacePart(self):
    """Test _add_namespace_part and related methods."""
    request = MakeArbitraryGetRequest()
    expected = MemcacheGetRequest()
    expected.CopyFrom(request)

    os.environ['HTTP_X_APPENGINE_DEFAULT_NAMESPACE'] = 'namespace_from_http'
    namespace_manager.enable_request_namespace()
    memcache._add_name_space(request)
    expected.name_space = 'namespace_from_http'
    self.assertEqual(expected, request)

    namespace_manager.set_namespace('a_namespace')
    self.assertEqual('a_namespace', namespace_manager.get_namespace())
    memcache._add_name_space(request)
    expected.name_space = 'a_namespace'
    self.assertEqual(expected, request)

    namespace_manager.set_namespace('')
    memcache._add_name_space(request)
    expected.ClearField('name_space')
    self.assertEqual(expected, request)

    namespace_manager.set_namespace(None)
    memcache._add_name_space(request)
    self.assertEqual(expected, request)

    namespace_manager.enable_request_namespace()
    memcache._add_name_space(request)
    expected.name_space = 'namespace_from_http'
    self.assertEqual(expected, request)

  def testAddNamespacePartEmptyString(self):
    """Tests that namespace field is cleared when empty requested."""
    request = MakeArbitraryGetRequest()
    expected = MemcacheGetRequest()
    expected.CopyFrom(request)

    namespace_manager.set_namespace('not-this-one')
    memcache._add_name_space(request, '')
    expected.ClearField('name_space')
    self.assertEqual(expected, request)


class MockUserRPC(object):
  """Minimally functional mock for UserRPC."""

  _error = None
  _hook = None

  def __init__(self, *args):
    pass

  def check_success(self):
    if self._error is not None:
      raise self._error

  def get_result(self):
    if self._hook is None:
      self.check_success()
      return None
    else:
      return self._hook(self)


class MemcacheAppIdTest(absltest.TestCase):
  """Test that specifying app_ids and num_memcacheg_backends works correctly."""

  def setUp(self):
    self.app_id = 'app1'

  def testAppIdSet(self):
    """Test undocumented fields are set when specified in the constructor."""
    request = MakeArbitraryGetRequest()
    request.ClearField('override')
    expected = MemcacheGetRequest()
    expected.CopyFrom(request)

    client = memcache.Client(_app_id=self.app_id)
    client._add_app_id(request)
    expected.override.app_id = self.app_id
    self.assertEqual(expected, request)

  def testAppIdNotSetWhenNotSpecified(self):
    """Test that app_id not set in request."""
    request = MakeArbitraryGetRequest()


    request.ClearField('override')
    expected = MemcacheGetRequest()
    expected.CopyFrom(request)

    client = memcache.Client()
    client._add_app_id(request)
    self.assertEqual(expected, request)

  def testAddAppIdCalled(self):
    """Test that _add_app_id is called for every type of request."""
    self.last_recorded_request = None

    def RecordSetAppIdRequest(message):
      """We record the message passed in to Client._set_app_id.
      The same message should then be sent to _make_async_call.
      """
      self.last_recorded_request = message

    def MockedAsyncCall(rpc, method, request, response, hook, user_data):
      self.assertEqual(request, self.last_recorded_request)


      if method == 'Delete':
        response.delete_status.append(MemcacheDeleteResponse.DELETED)
      if method == 'Set':
        response.set_status.append(MemcacheSetResponse.STORED)
      if method == 'BatchIncrement':
        response.item.add()
      rpc = MockUserRPC()
      rpc.method = method
      rpc.request = request
      rpc.response = response
      rpc._hook = hook
      rpc.user_data = user_data
      return rpc

    client = memcache.Client(_app_id=self.app_id)



    methods = [
      (memcache.Client.get_stats, [client]),
      (memcache.Client.flush_all, [client]),
      (memcache.Client.get, [client, 'key']),
      (memcache.Client.gets, [client, 'key']),
      (memcache.Client.get_multi, [client, ['key']]),
      (memcache.Client.delete, [client, 'key']),
      (memcache.Client.delete_multi, [client, ['key']]),
      (memcache.Client.set, [client, 'key', 'value']),
      (memcache.Client.add, [client, 'key', 'value']),
      (memcache.Client.replace, [client, 'key', 'value']),
      (memcache.Client.cas, [client, 'key', 'value']),
      (memcache.Client.set_multi, [client, {'key': 'value'}]),
      (memcache.Client.add_multi, [client, {'key': 'value'}]),
      (memcache.Client.replace_multi, [client, {'key': 'value'}]),
      (memcache.Client.cas_multi, [client, {'key': 'value'}]),
      (memcache.Client.incr, [client, 'key']),
      (memcache.Client.decr, [client, 'key']),
      (memcache.Client.offset_multi, [client, {'key': 1}])
    ]


    for method, args in methods:
      with mock.patch.object(client, '_add_app_id', RecordSetAppIdRequest):
        with mock.patch.object(client, '_make_async_call', MockedAsyncCall):
          method(*args)


class MemcacheTest(absltest.TestCase):
  """Unit test for getting keys from memcache."""

  def CallMethod(self,
                 method,
                 args=None,
                 error=None,
                 proto_response=None,
                 client=None,
                 **kwargs):
    """Calls named method with provided args on new client object.

    Args:
      method: Method to call on memcache client object.
      args: List of arguments to pass to method.
      error: Error to raise in sync call, if true.
      proto_response: The fake proto response to give to the sync call.
      client: Optional pre-initialized Client instance.
      **kwargs: Keyword arguments passed to the method.

    Returns:
      Tuple (service_method, proto_request, result) where:
        service_method: The service method that was sync called.
        proto_request: The request proto that was generated.
        result: The result of the memcached method call, after it
          assumes the result of proto_response came from
          the backend.
    """
    result_list = [None, None, None]
    if args is None:
      args = []

    def FakeAsyncCall(rpc, method, request, response, hook=None,
                      user_data=None):
      """Does fake asynchronous API call."""
      result_list[0] = method
      result_list[1] = request
      rpc = MockUserRPC()
      rpc.method = method
      rpc.request = request
      if error is not None:
        rpc._error = error
      else:
        response.CopyFrom(proto_response)
      rpc.response = response
      rpc._hook = hook
      rpc.user_data = user_data
      return rpc

    if client is None:
      client = memcache.Client()
    self.client = client
    client._make_async_call = FakeAsyncCall
    memcache.setup_client(client)
    if method in ('gets', 'cas', 'cas_multi') or method.endswith('_async'):
      method = getattr(client, method)
    else:
      method = getattr(memcache, method)
    result_list[2] = method(*args, **kwargs)
    return tuple(result_list)

  def testKeyStringHelper(self):
    """Tests the _key_string() helper function."""
    self.assertEqual(b'foo', memcache._key_string(b'foo'))
    self.assertEqual(b'pfx:foo', memcache._key_string(b'foo', b'pfx:'))
    server_to_user_map = {}
    self.assertEqual(
        b'pfx:foo2',
        memcache._key_string((1234, b'foo2'), b'pfx:', server_to_user_map))
    self.assertEqual(
        b'pfx:foo3', memcache._key_string(b'foo3', b'pfx:', server_to_user_map))
    self.assertEqual({
        b'pfx:foo3': b'foo3',
        b'pfx:foo2': b'foo2'
    }, server_to_user_map)

  def testKeyStringHelperValidation(self):
    """Tests that the _key_string() helper validates keys."""
    self.assertRaises(TypeError, memcache._key_string, 1234)
    self.assertRaises(TypeError, memcache._key_string, 1234, key_prefix='stuff')
    self.assertRaises(TypeError, memcache._key_string, 'key', key_prefix=1234)

  def testKeyStringHelperUnicodeKey(self):
    """Tests that unicode keys will be encoded strings as server keys."""
    server_to_user_dict = {}
    memcache._key_string(b'\xc3\xa9', server_to_user_dict=server_to_user_dict)
    self.assertEqual(b'\xc3\xa9', server_to_user_dict[b'\xc3\xa9'])

    server_to_user_dict.clear()
    memcache._key_string(u'\xe9', server_to_user_dict=server_to_user_dict)
    self.assertEqual(u'\xe9', server_to_user_dict[b'\xc3\xa9'])

  def testKeyStringHelperUnicodeKeyPrefix(self):
    """Tests when a key_prefix is a unicode string."""
    server_to_user_dict = {}
    memcache._key_string(
        'asdf', key_prefix=u'\xe9:', server_to_user_dict=server_to_user_dict)
    self.assertEqual('asdf', server_to_user_dict[b'\xc3\xa9:asdf'])

  def testLargeKeyString(self):
    """Tests that keys > memcache.MAX_KEY_SIZE are allowed."""
    server_to_user_dict = {}
    large_key = b'a' * 500
    self.assertGreater(len(large_key), memcache.MAX_KEY_SIZE)
    memcache._key_string(large_key, server_to_user_dict=server_to_user_dict)
    large_key_sha = hashlib.sha1(large_key).hexdigest()

    if isinstance(large_key_sha, six.text_type):
      large_key_sha = large_key_sha.encode('utf-8')

    self.assertEqual(large_key, server_to_user_dict[large_key_sha])

  def testEncodeValueHelperStringValue(self):
    """Tests that string values are passed through without modification."""
    stored_value, flags = memcache._validate_encode_value(b'foobar', None)
    self.assertEqual(b'foobar', stored_value)
    self.assertEqual(0, flags)

  def testEncodeValueHelperUnicodeValue(self):
    """Tests encoding for the server when the value is a unicode string."""
    stored_value, flags = memcache._validate_encode_value(u'foobar\xe9', None)
    self.assertEqual(b'foobar\xc3\xa9', stored_value)
    self.assertEqual(memcache.TYPE_UNICODE, flags)

  def testEncodeValueHelperIntValue(self):
    """Tests encoding for the server when the value is an int."""
    stored_value, flags = memcache._validate_encode_value(42, None)
    self.assertEqual(b'42', stored_value)
    self.assertEqual(memcache.TYPE_INT, flags)

  def testEncodeValueHelperLongValue(self):
    """Tests encoding for the server when the value is an int."""
    type_long = memcache.TYPE_LONG
    if six.PY3:
      type_long = memcache.TYPE_INT

    stored_value, flags = memcache._validate_encode_value(long(42), None)
    self.assertEqual(b'42', stored_value)
    self.assertEqual(type_long, flags)

  def testEncodeValueHelperBoolValue(self):
    """Tests encoding for the server when the value is an bool."""
    stored_value, flags = memcache._validate_encode_value(True, None)
    self.assertEqual(b'1', stored_value)
    self.assertEqual(memcache.TYPE_BOOL, flags)
    stored_value, flags = memcache._validate_encode_value(False, None)
    self.assertEqual(b'0', stored_value)
    self.assertEqual(memcache.TYPE_BOOL, flags)

  def testEncodeValueHelperPickledValue(self):
    """Tests encoding for the server when the value is a pickled object."""
    my_value = {
        'asdf': 1,
        'foo': long(2),
        'bar': 1.0,
    }
    stored_value, flags = memcache._validate_encode_value(
        my_value, six.moves.cPickle.dumps)
    self.assertEqual(my_value, six.moves.cPickle.loads(stored_value))
    self.assertEqual(memcache.TYPE_PICKLED, flags)

  def testDecodeValueHelperUnicodeValue(self):
    """Tests decoding the server value when it's a unicode string."""
    value = memcache._decode_value(b'foobar\xc3\xa9', memcache.TYPE_UNICODE,
                                   six.moves.cPickle.loads)
    self.assertEqual(u'foobar\xe9', value)

  def testDecodeValueHelperPickledValue(self):
    """Tests encoding the server value when it's a pickled object."""
    my_value = {
        'asdf': 1,
        'foo': 2,
        'bar': 1.0,
    }
    value = memcache._decode_value(
        six.moves.cPickle.dumps(my_value), memcache.TYPE_PICKLED,
        six.moves.cPickle.loads)
    self.assertEqual(my_value, value)

  def testDecodeValueHelperIntValue(self):
    """Tests encoding the server value when it's an int."""
    my_value = 42
    value = memcache._decode_value(b'42', memcache.TYPE_INT,
                                   six.moves.cPickle.loads)
    self.assertEqual(my_value, value)
    self.assertIs(type(value), int)

  def testDecodeValueHelperLongValue(self):
    """Tests encoding the server value when it's a long."""
    my_value = long(42)
    value = memcache._decode_value(b'42', memcache.TYPE_LONG,
                                   six.moves.cPickle.loads)
    self.assertEqual(my_value, value)
    self.assertIs(type(value), long)

  def testDecodeValueHelperBoolValue(self):
    """Tests encoding the server value when it's a bool."""
    value = memcache._decode_value(b'1', memcache.TYPE_BOOL,
                                   six.moves.cPickle.loads)
    self.assertEqual(True, value)
    self.assertIs(type(value), bool)

    value = memcache._decode_value(b'0', memcache.TYPE_BOOL,
                                   six.moves.cPickle.loads)
    self.assertEqual(False, value)
    self.assertIs(type(value), bool)

  def testCreateRpc(self):
    """Tests create_rpc() function."""
    with mock.patch.object(apiproxy_stub_map, 'CreateRPC'):
      rpc = memcache.create_rpc()
      self.assertIsInstance(rpc, apiproxy_stub_map.UserRPC)
      self.assertEqual(rpc.deadline, None)
      self.assertEqual(rpc.callback, None)
      apiproxy_stub_map.CreateRPC.assert_called_once_with('memcache', mock.ANY)

  def testCreateRpcArgs(self):
    """Tests create_rpc() function."""
    with mock.patch.object(apiproxy_stub_map, 'CreateRPC'):
      callback = lambda: None
      rpc = memcache.create_rpc(deadline=2, callback=callback)
      self.assertIsInstance(rpc, apiproxy_stub_map.UserRPC)
      self.assertEqual(rpc.deadline, 2)
      self.assertEqual(rpc.callback, callback)
      apiproxy_stub_map.CreateRPC.assert_called_once_with('memcache', mock.ANY)

  def testSetServers(self):
    """Tests no-op set_servers call."""
    service_method, proto_request, return_value = self.CallMethod(
        'set_servers', args=[['10.0.0.1:11211', '10.0.0.2:11212']])
    self.assertEqual(None, proto_request)
    self.assertEqual(None, return_value)
    self.assertEqual(None, service_method)

  def testDisconnectAll(self):
    """Tests no-op disconnect_all call."""
    service_method, proto_request, return_value = self.CallMethod(
        'disconnect_all')
    self.assertEqual(None, proto_request)
    self.assertEqual(None, return_value)
    self.assertEqual(None, service_method)

  def testForgetDeadHosts(self):
    """Tests no-op forget_dead_hosts call."""
    service_method, proto_request, return_value = self.CallMethod(
        'forget_dead_hosts')
    self.assertEqual(None, proto_request)
    self.assertEqual(None, return_value)
    self.assertEqual(None, service_method)

  def testDebugLog(self):
    """Tests no-op debuglog call."""
    service_method, proto_request, return_value = self.CallMethod('debuglog')
    self.assertEqual(None, proto_request)
    self.assertEqual(None, return_value)
    self.assertEqual(None, service_method)

  def testFlushAllPass(self):
    """Tests that a Flush RPC gets setup correctly, and succeeds."""
    service_method, proto_request, return_value = self.CallMethod(
        'flush_all', proto_response=MemcacheFlushResponse())
    self.assertEqual('FlushAll', service_method)

    self.assertEqual(MemcacheFlushRequest(), proto_request)
    self.assertEqual(True, return_value)

  def testFlushAllFail(self):
    """Tests that a Flush RPC handles application errors correctly."""
    service_method, proto_request, return_value = self.CallMethod(
        'flush_all',
        error=apiproxy_errors.ApplicationError('fake error'),
        proto_response=MemcacheFlushResponse())
    self.assertEqual('FlushAll', service_method)

    self.assertEqual(MemcacheFlushRequest(), proto_request)
    self.assertEqual(False, return_value)

  def testFlushAllTimeout(self):
    """Tests that a Flush RPC handles timeouts correctly."""
    service_method, proto_request, return_value = self.CallMethod(
        'flush_all',
        error=apiproxy_errors.DeadlineExceededError('fake error'),
        proto_response=MemcacheFlushResponse())
    self.assertEqual('FlushAll', service_method)

    self.assertEqual(MemcacheFlushRequest(), proto_request)
    self.assertEqual(False, return_value)

  def testGetEmpty(self):
    """Tests that get() returns None on a cache miss."""
    service_method, proto_request, return_value = self.CallMethod(
        'get', args=[b'foo'], proto_response=MemcacheGetResponse())
    self.assertEqual('Get', service_method)
    self.assertEqual(None, return_value)
    self.assertEqual(1, len(proto_request.key))
    self.assertEqual(b'foo', proto_request.key[0])

  def testGetWithValue(self):
    """Tests that get() returns a value on a cache hit."""
    response = MemcacheGetResponse()
    request_item = response.item.add()
    request_item.key = b'foo'
    request_item.value = b'foo_value'

    service_method, proto_request, return_value = self.CallMethod(
        'get', args=[b'foo'], proto_response=response)
    self.assertEqual('Get', service_method)
    self.assertEqual(b'foo_value', return_value)
    self.assertEqual(1, len(proto_request.key))
    self.assertEqual(b'foo', proto_request.key[0])

  def testGetForCas(self):
    """Tests that get(..., for_cas=True) stores the cas_id on the client."""
    response = MemcacheGetResponse()
    request_item = response.item.add()
    request_item.key = b'foo'
    request_item.value = b'foo_value'
    request_item.cas_id = 42

    service_method, proto_request, return_value = self.CallMethod(
        'get', args=[b'foo'], proto_response=response, for_cas=True)
    self.assertEqual('Get', service_method)
    self.assertEqual(b'foo_value', return_value)
    self.assertEqual(42, self.client._cas_ids[('', b'foo')])
    self.assertEqual(1, len(proto_request.key))
    self.assertEqual(b'foo', proto_request.key[0])

  def testGets(self):
    """Tests that gets() has the same effect as get(for_cas=True)."""
    response = MemcacheGetResponse()
    request_item = response.item.add()
    request_item.key = b'foo'
    request_item.value = b'foo_value'
    request_item.cas_id = 42

    service_method, proto_request, return_value = self.CallMethod(
        'gets', args=[b'foo'], proto_response=response)
    self.assertEqual('Get', service_method)
    self.assertEqual(b'foo_value', return_value)
    self.assertEqual(42, self.client._cas_ids[('', b'foo')])
    self.assertEqual(1, len(proto_request.key))
    self.assertEqual(b'foo', proto_request.key[0])

  def testGetWithPickledValue(self):
    """Tests that get() returns a value on a cache hit."""
    response = MemcacheGetResponse()
    request_item = response.item.add()
    request_item.key = b'foo'
    request_item.value = six.moves.cPickle.dumps(['foo_value'])
    request_item.flags = memcache.TYPE_PICKLED

    service_method, proto_request, return_value = self.CallMethod(
        'get', args=[b'foo'], proto_response=response)
    self.assertEqual('Get', service_method)
    self.assertEqual(['foo_value'], return_value)
    self.assertEqual(1, len(proto_request.key))
    self.assertEqual(b'foo', proto_request.key[0])

  def testGetWithTuple(self):
    """Tests that get() when given a tuple ignores the hash value component."""
    response = MemcacheGetResponse()
    request_item = response.item.add()
    request_item.key = b'key_part'
    request_item.value = b'foo_value'
    service_method, proto_request, return_value = self.CallMethod(
        'get', proto_response=response, args=[(123, b'key_part')])
    self.assertEqual(1, len(proto_request.key))
    self.assertEqual(b'key_part', proto_request.key[0])
    self.assertEqual('Get', service_method)
    self.assertEqual(b'foo_value', return_value)

  def testGetWithException(self):
    """Tests that get() returns None on RPC exception."""
    service_method, proto_request, return_value = self.CallMethod(
        'get',
        error=apiproxy_errors.ApplicationError('fake error'),
        args=[b'key'])
    self.assertEqual(1, len(proto_request.key))
    self.assertEqual(b'key', proto_request.key[0])
    self.assertEqual('Get', service_method)
    self.assertEqual(None, return_value)

  def testGetWithTimeout(self):
    """Tests that get() returns None on RPC timeout."""
    service_method, proto_request, return_value = self.CallMethod(
        'get',
        error=apiproxy_errors.DeadlineExceededError('fake error'),
        args=[b'key'])
    self.assertEqual(1, len(proto_request.key))
    self.assertEqual(b'key', proto_request.key[0])
    self.assertEqual('Get', service_method)
    self.assertEqual(None, return_value)

  def testGetMulti(self):
    """Tests that get_multi() returns multiple values on a cache hit."""
    response = MemcacheGetResponse()
    request_item = response.item.add()
    request_item.key = b'abc:foo'
    request_item.value = b'foo_value'
    request_item = response.item.add()
    request_item.key = b'abc:bar'
    request_item.value = b'bar_value'

    service_method, proto_request, return_value = self.CallMethod(
        'get_multi',
        args=[[b'foo', (123, b'bar'), 'missing']],
        proto_response=response,
        key_prefix=b'abc:')
    self.assertEqual(3, len(proto_request.key))
    self.assertEqual(b'abc:foo', proto_request.key[0])
    self.assertEqual(b'abc:bar', proto_request.key[1])
    self.assertEqual(b'abc:missing', proto_request.key[2])
    self.assertEqual('Get', service_method)
    self.assertEqual({
        b'foo': b'foo_value',
        b'bar': b'bar_value'
    }, return_value)

  def testGetMultiForCas(self):
    """Tests that get_multi(..., for_cas) returns (value, cas_id) tuples."""
    response = MemcacheGetResponse()
    request_item = response.item.add()
    request_item.key = b'abc:foo'
    request_item.value = b'foo_value'
    request_item.cas_id = 42
    request_item = response.item.add()
    request_item.key = b'abc:bar'
    request_item.value = b'bar_value'
    request_item.cas_id = 43

    service_method, proto_request, return_value = self.CallMethod(
        'get_multi',
        args=[[b'foo', (123, b'bar'), b'missing']],
        proto_response=response,
        key_prefix=b'abc:',
        for_cas=True)
    self.assertEqual(3, len(proto_request.key))
    self.assertEqual(b'abc:foo', proto_request.key[0])
    self.assertEqual(b'abc:bar', proto_request.key[1])
    self.assertEqual(b'abc:missing', proto_request.key[2])
    self.assertEqual('Get', service_method)
    self.assertEqual({
        b'foo': b'foo_value',
        b'bar': b'bar_value'
    }, return_value)
    self.assertEqual(42, self.client._cas_ids[('', b'abc:foo')])
    self.assertEqual(43, self.client._cas_ids[('', b'abc:bar')])

  def testGetMultiRpcError(self):
    """Tests that get_multi() returns empty dictionary on RPC error."""
    service_method, proto_request, return_value = self.CallMethod(
        'get_multi',
        args=[['foo', 'bar', 'missing']],
        error=apiproxy_errors.ApplicationError('fake error'))
    self.assertEqual({}, return_value)

  def testGetMultiTimeout(self):
    """Tests that get_multi() returns empty dictionary on RPC timeout."""
    service_method, proto_request, return_value = self.CallMethod(
        'get_multi',
        args=[['foo', 'bar', 'missing']],
        error=apiproxy_errors.DeadlineExceededError('fake error'))
    self.assertEqual({}, return_value)

  def testSetSuccessful(self):
    """Tests set() successfully working with and without an expiration."""
    for expiration in (None, 0.5, 1, 1.0, long(1)):
      response = MemcacheSetResponse()
      response.set_status.append(MemcacheSetResponse.STORED)

      kw_args = {}
      expected_expiration = 0
      if expiration is not None:
        kw_args = {'time': expiration}
        expected_expiration = 1

      service_method, proto_request, return_value = self.CallMethod(
          'set',
          args=[b'foo', b'foo_value'],
          error=None,
          proto_response=response,
          **kw_args)

      self.assertEqual(1, len(proto_request.item))
      self.assertEqual(b'foo', proto_request.item[0].key)
      self.assertEqual(b'foo_value', proto_request.item[0].value)
      self.assertEqual(expected_expiration,
                        proto_request.item[0].expiration_time)
      self.assertEqual(MemcacheSetRequest.SET,
                        proto_request.item[0].set_policy)
      self.assertEqual('Set', service_method)
      self.assertEqual(True, return_value)

  def testSetPickledSuccessful(self):
    """Tests set() successfully working where the value needs to be pickled."""
    for expiration in (None, 0.5, 1, 1.0, long(1)):
      response = MemcacheSetResponse()
      response.set_status.append(MemcacheSetResponse.STORED)

      kw_args = {}
      expected_expiration = 0
      if expiration is not None:
        kw_args = {'time': expiration}
        expected_expiration = 1

      service_method, proto_request, return_value = self.CallMethod(
          'set',
          args=[b'foo', ['foo_value']],
          error=None,
          proto_response=response,
          **kw_args)

      self.assertEqual(1, len(proto_request.item))
      self.assertEqual(b'foo', proto_request.item[0].key)
      self.assertEqual(['foo_value'],
                        six.moves.cPickle.loads(proto_request.item[0].value))
      self.assertEqual(memcache.TYPE_PICKLED, proto_request.item[0].flags)
      self.assertEqual(expected_expiration,
                        proto_request.item[0].expiration_time)
      self.assertEqual(MemcacheSetRequest.SET,
                        proto_request.item[0].set_policy)
      self.assertEqual('Set', service_method)
      self.assertEqual(True, return_value)

  def testSetFail(self):
    """Tests set() making valid request, but returning False on failure."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.NOT_STORED)
    service_method, proto_request, return_value = self.CallMethod(
        'set', args=[b'foo', b'foo_value'], error=None, proto_response=response)
    self.assertEqual(1, len(proto_request.item))
    self.assertEqual(b'foo', proto_request.item[0].key)
    self.assertEqual(b'foo_value', proto_request.item[0].value)
    self.assertEqual(MemcacheSetRequest.SET,
                      proto_request.item[0].set_policy)
    self.assertEqual('Set', service_method)
    self.assertEqual(False, return_value)

  def testSetTimeout(self):
    """Tests set() making valid request, but returning False on failure."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.NOT_STORED)
    service_method, proto_request, return_value = self.CallMethod(
        'set',
        args=[b'foo', b'foo_value'],
        error=apiproxy_errors.DeadlineExceededError('fake error'),
        proto_response=response)
    self.assertEqual(1, len(proto_request.item))
    self.assertEqual(b'foo', proto_request.item[0].key)
    self.assertEqual(b'foo_value', proto_request.item[0].value)
    self.assertEqual(MemcacheSetRequest.SET,
                      proto_request.item[0].set_policy)
    self.assertEqual('Set', service_method)
    self.assertEqual(False, return_value)

  def testSetApplicationError(self):
    """Tests set() making valid request, but returning False on failure."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.NOT_STORED)
    service_method, proto_request, return_value = self.CallMethod(
        'set',
        args=[b'foo', b'foo_value'],
        error=apiproxy_errors.ApplicationError(666, 'about the error'),
        proto_response=response)
    self.assertEqual(1, len(proto_request.item))
    self.assertEqual(b'foo', proto_request.item[0].key)
    self.assertEqual(b'foo_value', proto_request.item[0].value)
    self.assertEqual(MemcacheSetRequest.SET,
                      proto_request.item[0].set_policy)
    self.assertEqual('Set', service_method)
    self.assertEqual(False, return_value)

  def testSetNewRpcError(self):
    """Tests set() returning only ERROR code for compatibility."""
    for status in (MemcacheSetResponse.DEADLINE_EXCEEDED,
                   MemcacheSetResponse.UNREACHABLE,
                   MemcacheSetResponse.OTHER_ERROR):
      response = MemcacheSetResponse()
      response.set_status.append(status)
      service_method, proto_request, return_value = self.CallMethod(
          'set',
          args=[b'foo', b'foo_value'],
          error=None,
          proto_response=response)
      self.assertEqual(1, len(proto_request.item))
      self.assertEqual(b'foo', proto_request.item[0].key)
      self.assertEqual(b'foo_value', proto_request.item[0].value)
      self.assertEqual(MemcacheSetRequest.SET,
                        proto_request.item[0].set_policy)
      self.assertEqual('Set', service_method)
      self.assertEqual(False, return_value)

  def testAdd(self):
    """Tests that add() sets the right SetPolicy."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    service_method, proto_request, return_value = self.CallMethod(
        'add', args=['foo', 'foo_value'], error=None, proto_response=response)
    self.assertEqual(1, len(proto_request.item))
    self.assertEqual(MemcacheSetRequest.ADD,
                      proto_request.item[0].set_policy)
    self.assertEqual('Set', service_method)
    self.assertEqual(True, return_value)

  def testReplace(self):
    """Tests that replace() sets the right SetPolicy."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    service_method, proto_request, return_value = self.CallMethod(
        'replace',
        args=['foo', 'foo_value'],
        error=None,
        proto_response=response)
    self.assertEqual(1, len(proto_request.item))
    self.assertEqual(MemcacheSetRequest.REPLACE,
                      proto_request.item[0].set_policy)
    self.assertEqual('Set', service_method)
    self.assertEqual(True, return_value)

  def testCas(self):
    """Tests that cas() sets the right SetPolicy and cas_id."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    client = memcache.Client()
    client._cas_ids[('', b'foo')] = 42
    service_method, proto_request, return_value = self.CallMethod(
        'cas',
        args=[b'foo', 'foo_value'],
        error=None,
        proto_response=response,
        client=client)
    self.assertEqual(1, len(proto_request.item))
    self.assertEqual(MemcacheSetRequest.CAS,
                      proto_request.item[0].set_policy)
    self.assertEqual(42, proto_request.item[0].cas_id)
    self.assertEqual('Set', service_method)
    self.assertEqual(True, return_value)

  def testCasWithNamespace(self):
    """Tests that cas() sets the right SetPolicy and cas_id."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    client = memcache.Client()
    client._cas_ids[('', b'foo')] = 42
    service_method, proto_request, return_value = self.CallMethod(
        'cas',
        args=[b'foo', 'foo_value'],
        error=None,
        proto_response=response,
        client=client)
    self.assertEqual(1, len(proto_request.item))
    self.assertEqual(MemcacheSetRequest.CAS,
                      proto_request.item[0].set_policy)
    self.assertEqual(42, proto_request.item[0].cas_id)
    self.assertEqual('Set', service_method)
    self.assertEqual(True, return_value)

    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    client = memcache.Client()
    client._cas_ids[('ns1', b'foo')] = 84
    service_method, proto_request, return_value = self.CallMethod(
        'cas',
        args=[b'foo', 'foo_value2'],
        error=None,
        proto_response=response,
        namespace='ns1',
        client=client)
    self.assertEqual(1, len(proto_request.item))
    self.assertEqual(MemcacheSetRequest.CAS,
                      proto_request.item[0].set_policy)
    self.assertEqual(84, proto_request.item[0].cas_id)
    self.assertEqual('Set', service_method)
    self.assertEqual(True, return_value)

  def testCasTypeError(self):
    """Tets that cas() raises TypeError for malformed old_value."""
    client = memcache.Client()
    self.assertRaises(
        TypeError, client.cas, 'key', None, 'value', time=0, namespace=None)
    self.assertRaises(TypeError, client.cas, 'key', 'old', 'value', time=0)
    self.assertRaises(TypeError, client.cas, 'key', ('old', 1, 2), 'value')

  def testSetMulti(self):
    """Tests set_multi() with and without an expiration time."""
    for expiration in (None, 0.5, 1, 1.0, long(1)):
      mapping = {b'a': b'val1', b'b': b'val2', b'c': b'val3'}



      expected_responses = {
          b'pfx:a': MemcacheSetResponse.STORED,
          b'pfx:b': MemcacheSetResponse.NOT_STORED,
          b'pfx:c': MemcacheSetResponse.STORED,
      }
      response = MemcacheSetResponse()
      for key, value in six.iteritems(expected_responses):
        response.set_status.append(value)

      kw_args = {}
      expected_expiration = 0
      if expiration is not None:
        kw_args = {'time': expiration}
        expected_expiration = 1

      service_method, proto_request, return_value = self.CallMethod(
          'set_multi',
          args=[mapping],
          proto_response=response,
          key_prefix=b'pfx:',
          **kw_args)

      expected_values = {
          b'pfx:a': b'val1',
          b'pfx:b': b'val2',
          b'pfx:c': b'val3',
      }
      self.assertEqual(3, len(proto_request.item))
      self.assertEqual('Set', service_method)
      self.assertEqual([b'b'], return_value)

      for index, key in enumerate(six.iterkeys(expected_values)):
        self.assertEqual(key, proto_request.item[index].key)
        self.assertEqual(expected_values[key],
                          proto_request.item[index].value)
        self.assertEqual(MemcacheSetRequest.SET,
                          proto_request.item[index].set_policy)
        self.assertEqual(expected_expiration,
                          proto_request.item[index].expiration_time)

  def testSetMultiError(self):
    """Tests set_multi() with an RPC error."""
    response = MemcacheSetResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'set_multi',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=apiproxy_errors.ApplicationError('fake error'),
        proto_response=response,
        key_prefix='prefix')
    self.assertEqual(set(['foo', 'bar']), set(return_value))

  def testSetMultiTimeout(self):
    """Tests set_multi() with an RPC timeout."""
    response = MemcacheSetResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'set_multi',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=apiproxy_errors.DeadlineExceededError('fake error'),
        proto_response=response,
        key_prefix='prefix')
    self.assertEqual(set(['foo', 'bar']), set(return_value))

  def testSetMultiApplicationError(self):
    """Tests set_multi() making valid request, but failing."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    response.set_status.append(MemcacheSetResponse.ERROR)
    response.set_status.append(MemcacheSetResponse.DEADLINE_EXCEEDED)
    response.set_status.append(MemcacheSetResponse.UNREACHABLE)
    response.set_status.append(MemcacheSetResponse.OTHER_ERROR)

    service_method, proto_request, return_value = self.CallMethod(
        'set_multi',
        args=[
            collections.OrderedDict([('k1', 'value1'), ('k2', 'value2'),
                                     ('k3', 'value3'), ('k4', 'value4'),
                                     ('k5', 'value5')])
        ],
        proto_response=response,
        key_prefix='prefix')
    self.assertEqual('Set', service_method)
    self.assertEqual(5, len(proto_request.item))
    self.assertEqual(set(['k2', 'k3', 'k4', 'k5']), set(return_value))

  def testSetMultiAsync(self):
    """Tests set_multi_async()."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    response.set_status.append(MemcacheSetResponse.ERROR)
    response.set_status.append(MemcacheSetResponse.DEADLINE_EXCEEDED)
    response.set_status.append(MemcacheSetResponse.UNREACHABLE)
    response.set_status.append(MemcacheSetResponse.OTHER_ERROR)

    service_method, proto_request, return_value = self.CallMethod(
        'set_multi_async',
        args=[
            collections.OrderedDict([
                ('k1', 'value1'),
                ('k2', 'value2'),
                ('k3', 'value3'),
                ('k4', 'value4'),
                ('k5', 'value5')
            ])
        ],
        error=None,
        proto_response=response)
    self.assertEqual(5, len(proto_request.item))
    for i in range(0, 5):
      self.assertEqual(MemcacheSetRequest.SET,
                        proto_request.item[i].set_policy)
    self.assertEqual('Set', service_method)
    result = return_value.get_result()
    self.assertEqual(result, {
        'k1': MemcacheSetResponse.STORED,
        'k2': MemcacheSetResponse.ERROR,
        'k3': MemcacheSetResponse.ERROR,
        'k4': MemcacheSetResponse.ERROR,
        'k5': MemcacheSetResponse.ERROR
    })

  def testAddMulti(self):
    """Tests that add_multi() sets the right SetPolicy."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    response.set_status.append(MemcacheSetResponse.STORED)

    service_method, proto_request, return_value = self.CallMethod(
        'add_multi',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=None,
        proto_response=response)
    self.assertEqual(2, len(proto_request.item))
    self.assertEqual(MemcacheSetRequest.ADD,
                      proto_request.item[0].set_policy)
    self.assertEqual(MemcacheSetRequest.ADD,
                      proto_request.item[1].set_policy)
    self.assertEqual('Set', service_method)
    self.assertEqual([], return_value)

  def testAddMultiError(self):
    """Tests add_multi() with an RPC error."""
    response = MemcacheSetResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'add_multi',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=apiproxy_errors.ApplicationError('fake error'),
        proto_response=response,
        key_prefix='prefix')
    self.assertEqual(set(['foo', 'bar']), set(return_value))

  def testAddMultiTimeout(self):
    """Tests add_multi() with an RPC timeout."""
    response = MemcacheSetResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'add_multi',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=apiproxy_errors.DeadlineExceededError('fake error'),
        proto_response=response,
        key_prefix='prefix')
    self.assertEqual(set(['foo', 'bar']), set(return_value))

  def testAddMultiAsync(self):
    """Tests add_multi_async()."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    response.set_status.append(MemcacheSetResponse.STORED)

    service_method, proto_request, return_value = self.CallMethod(
        'add_multi_async',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=None,
        proto_response=response)
    self.assertEqual(2, len(proto_request.item))
    self.assertEqual(MemcacheSetRequest.ADD,
                      proto_request.item[0].set_policy)
    self.assertEqual(MemcacheSetRequest.ADD,
                      proto_request.item[1].set_policy)
    self.assertEqual('Set', service_method)
    result = return_value.get_result()
    self.assertEqual(result, {
        'foo': MemcacheSetResponse.STORED,
        'bar': MemcacheSetResponse.STORED
    })

  def testReplaceMulti(self):
    """Tests that replace_multi() sets the right SetPolicy."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    response.set_status.append(MemcacheSetResponse.STORED)

    service_method, proto_request, return_value = self.CallMethod(
        'replace_multi',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=None,
        proto_response=response)
    self.assertEqual(2, len(proto_request.item))
    self.assertEqual(MemcacheSetRequest.REPLACE,
                      proto_request.item[0].set_policy)
    self.assertEqual(MemcacheSetRequest.REPLACE,
                      proto_request.item[1].set_policy)
    self.assertEqual('Set', service_method)
    self.assertEqual([], return_value)

  def testReplaceMultiError(self):
    """Tests replace_multi() with an RPC error."""
    response = MemcacheSetResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'replace_multi',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=apiproxy_errors.ApplicationError('fake error'),
        proto_response=response,
        key_prefix='prefix')
    self.assertEqual(set(['foo', 'bar']), set(return_value))

  def testReplaceMultiTimeout(self):
    """Tests replace_multi() with an RPC timeout."""
    response = MemcacheSetResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'replace_multi',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=apiproxy_errors.DeadlineExceededError('fake error'),
        proto_response=response,
        key_prefix='prefix')
    self.assertEqual(set(['foo', 'bar']), set(return_value))

  def testReplaceMultiAsync(self):
    """Tests replace_multi_async()."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    response.set_status.append(MemcacheSetResponse.STORED)

    service_method, proto_request, return_value = self.CallMethod(
        'replace_multi_async',
        args=[{
            'foo': 'foo_value',
            'bar': 'bar_value'
        }],
        error=None,
        proto_response=response)
    self.assertEqual(2, len(proto_request.item))
    self.assertEqual(MemcacheSetRequest.REPLACE,
                      proto_request.item[0].set_policy)
    self.assertEqual(MemcacheSetRequest.REPLACE,
                      proto_request.item[1].set_policy)
    self.assertEqual('Set', service_method)
    result = return_value.get_result()
    self.assertEqual(result, {
        'foo': MemcacheSetResponse.STORED,
        'bar': MemcacheSetResponse.STORED
    })

  def testCasMulti(self):
    """Tests that cas_multi() sets the right SetPolicy and cas_id."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    response.set_status.append(MemcacheSetResponse.STORED)
    client = memcache.Client()
    client._cas_ids[('', b'x:foo')] = 42
    client._cas_ids[('', b'x:bar')] = 43

    service_method, proto_request, return_value = self.CallMethod(
        'cas_multi',
        args=[{
            b'foo': 'foo_value',
            b'bar': 'foo_value'
        }],
        error=None,
        proto_response=response,
        client=client,
        key_prefix=b'x:')
    self.assertEqual(2, len(proto_request.item))


    cas_ids = [proto_request.item[i].cas_id for i in range(2)]
    self.assertEqual(set(cas_ids), set([42, 43]))

    self.assertEqual(MemcacheSetRequest.CAS,
                      proto_request.item[0].set_policy)
    self.assertEqual(MemcacheSetRequest.CAS,
                      proto_request.item[1].set_policy)
    self.assertEqual('Set', service_method)
    self.assertEqual([], return_value)

  def testCasMultiAsync(self):
    """Tests cas_multi_async()."""
    response = MemcacheSetResponse()
    response.set_status.append(MemcacheSetResponse.STORED)
    response.set_status.append(MemcacheSetResponse.STORED)
    client = memcache.Client()
    client._cas_ids[('', b'abc:foo')] = 42
    client._cas_ids[('', b'abc:bar')] = 43

    service_method, proto_request, return_value = self.CallMethod(
        'cas_multi_async',
        args=[{
            b'foo': 'foo_value',
            b'bar': 'foo_value'
        }],
        key_prefix=b'abc:',
        error=None,
        proto_response=response,
        client=client)
    self.assertEqual(2, len(proto_request.item))


    cas_ids = [proto_request.item[i].cas_id for i in range(2)]
    self.assertEqual(set(cas_ids), set([42, 43]))

    self.assertEqual(MemcacheSetRequest.CAS,
                      proto_request.item[0].set_policy)
    self.assertEqual(MemcacheSetRequest.CAS,
                      proto_request.item[1].set_policy)
    self.assertEqual('Set', service_method)
    result = return_value.get_result()
    self.assertEqual(result, {
        b'foo': MemcacheSetResponse.STORED,
        b'bar': MemcacheSetResponse.STORED
    })

  def testDeleteHit(self):
    """Tests the delete() method with and without a timeout."""
    for timeout in (None, 0.5, 1, 1.0, long(1)):
      response = MemcacheDeleteResponse()
      response.delete_status.append(MemcacheDeleteResponse.DELETED)

      kw_args = {}
      expected_timeout = 0
      if timeout is not None:
        kw_args = {'seconds': timeout}
        expected_timeout = 1

      service_method, proto_request, return_value = self.CallMethod(
          'delete', args=[b'key_to_die'], proto_response=response, **kw_args)
      self.assertEqual(1, len(proto_request.item))
      self.assertEqual(b'key_to_die', proto_request.item[0].key)
      self.assertEqual(expected_timeout, proto_request.item[0].delete_time)
      self.assertEqual(2, return_value)

  def testDeleteMiss(self):
    """Tests the delete() RPC succeeding, but not deleting."""
    response = MemcacheDeleteResponse()
    response.delete_status.append(MemcacheDeleteResponse.NOT_FOUND)
    service_method, proto_request, return_value = self.CallMethod(
        'delete', args=['key_to_die'], proto_response=response)
    self.assertEqual(1, return_value)

  def testDeleteFail(self):
    """Tests the delete() RPC failing."""
    service_method, proto_request, return_value = self.CallMethod(
        'delete',
        args=['key_to_die'],
        error=apiproxy_errors.ApplicationError('fake error'))
    self.assertEqual(0, return_value)

  def testDeleteServerError(self):
    """Tests the delete() RPC succeeding with error status code."""


    for status in (MemcacheDeleteResponse.DEADLINE_EXCEEDED,
                   MemcacheDeleteResponse.UNREACHABLE,
                   MemcacheDeleteResponse.OTHER_ERROR):
      response = MemcacheDeleteResponse()
      response.delete_status.append(status)
      service_method, proto_request, return_value = self.CallMethod(
          'delete', args=['key_to_die'], proto_response=response)
      self.assertEqual('Delete', service_method)
      self.assertEqual(1, len(proto_request.item))
      self.assertEqual(0, return_value)

  def testDeleteTimeout(self):
    """Tests the delete() RPC timeout."""
    service_method, proto_request, return_value = self.CallMethod(
        'delete',
        args=['key_to_die'],
        error=apiproxy_errors.DeadlineExceededError('fake error'))
    self.assertEqual(0, return_value)

  def testDeleteMulti(self):
    """Tests the delete_multi() method with and without a timeout."""
    for timeout in (None, 0.5, 1, 1.0, long(1)):
      response = MemcacheDeleteResponse()
      response.delete_status.append(MemcacheDeleteResponse.DELETED)
      response.delete_status.append(MemcacheDeleteResponse.NOT_FOUND)

      kw_args = {}
      expected_timeout = 0
      if timeout is not None:
        kw_args = {'seconds': timeout}
        expected_timeout = 1

      service_method, proto_request, return_value = self.CallMethod(
          'delete_multi',
          args=[[b'key_to_die', b'and_another']],
          proto_response=response,
          key_prefix=b'pfx:',
          **kw_args)
      self.assertEqual(2, len(proto_request.item))
      self.assertEqual(b'pfx:key_to_die', proto_request.item[0].key)
      self.assertEqual(expected_timeout, proto_request.item[0].delete_time)
      self.assertEqual(b'pfx:and_another', proto_request.item[1].key)
      self.assertEqual(expected_timeout, proto_request.item[1].delete_time)
      self.assertEqual('Delete', service_method)
      self.assertEqual(True, return_value)

  def testDeleteMultiServerError(self):
    """Tests backwards compatibility for delete_multi() with server error."""

    response = MemcacheDeleteResponse()
    response.delete_status.append(MemcacheDeleteResponse.DELETED)
    response.delete_status.append(MemcacheDeleteResponse.DEADLINE_EXCEEDED)

    service_method, proto_request, return_value = self.CallMethod(
        'delete_multi',
        args=[['key_to_die', 'and_another']],
        proto_response=response,
        key_prefix='pfx:')
    self.assertEqual('Delete', service_method)
    self.assertEqual(2, len(proto_request.item))
    self.assertEqual(False, return_value)

  def testDeleteMultiAsync(self):
    """Tests the delete_multi_async() method."""
    response = MemcacheDeleteResponse()
    response.delete_status.append(MemcacheDeleteResponse.DELETED)
    response.delete_status.append(MemcacheDeleteResponse.NOT_FOUND)

    service_method, proto_request, return_value = self.CallMethod(
        'delete_multi_async',
        args=[[b'key_to_die', b'and_another']],
        proto_response=response,
        key_prefix=b'pfx:',
    )
    self.assertEqual(2, len(proto_request.item))
    self.assertEqual(b'pfx:key_to_die', proto_request.item[0].key)
    self.assertEqual(b'pfx:and_another', proto_request.item[1].key)
    self.assertEqual('Delete', service_method)
    result = return_value.get_result()
    self.assertEqual(
        [memcache.DELETE_SUCCESSFUL, memcache.DELETE_ITEM_MISSING], result)

  def testDeleteMultiAsyncServerError(self):

    response = MemcacheDeleteResponse()
    response.delete_status.append(MemcacheDeleteResponse.DELETED)
    response.delete_status.append(MemcacheDeleteResponse.DEADLINE_EXCEEDED)

    service_method, proto_request, return_value = self.CallMethod(
        'delete_multi_async',
        args=[['key_to_die', 'and_another']],
        proto_response=response,
        key_prefix='pfx:')
    result = return_value.get_result()
    self.assertEqual('Delete', service_method)
    self.assertEqual(2, len(proto_request.item))
    self.assertEqual(None, result)

  def testIncrHit(self):
    """Tests incr(), with implicit delta, returns new value on cache hit."""
    response = MemcacheIncrementResponse()
    response.new_value = 17
    service_method, proto_request, return_value = self.CallMethod(
        'incr', args=[b'my_key'], error=None, proto_response=response)
    self.assertEqual('Increment', service_method)
    self.assertEqual(17, return_value)
    self.assertEqual(MemcacheIncrementRequest.INCREMENT,
                      proto_request.direction)
    self.assertEqual(1, proto_request.delta)
    self.assertEqual(b'my_key', proto_request.key)

  def testIncrAsync(self):
    """Tests incr_async()."""
    response = MemcacheIncrementResponse()
    response.new_value = 17
    service_method, proto_request, return_value = self.CallMethod(
        'incr_async', args=[b'my_key'], error=None, proto_response=response)
    self.assertEqual('Increment', service_method)
    self.assertEqual(MemcacheIncrementRequest.INCREMENT,
                      proto_request.direction)
    self.assertEqual(1, proto_request.delta)
    self.assertEqual(b'my_key', proto_request.key)
    self.assertEqual(17, return_value.get_result())

  def testDecrMiss(self):
    """Tests decr(), with explicit delta, returns None on cache miss."""
    response = MemcacheIncrementResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'decr', args=[b'my_key'], error=None, proto_response=response, delta=7)
    self.assertEqual('Increment', service_method)
    self.assertEqual(None, return_value)
    self.assertEqual(MemcacheIncrementRequest.DECREMENT,
                      proto_request.direction)
    self.assertEqual(7, proto_request.delta)
    self.assertEqual(b'my_key', proto_request.key)

  def testDecrTimeout(self):
    """Tests decr(), with explicit delta, returns None on RPC error."""
    response = MemcacheIncrementResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'decr',
        args=[b'my_key'],
        error=apiproxy_errors.DeadlineExceededError('fake error'),
        proto_response=response,
        delta=7)
    self.assertEqual('Increment', service_method)
    self.assertEqual(None, return_value)
    self.assertEqual(MemcacheIncrementRequest.DECREMENT,
                      proto_request.direction)
    self.assertEqual(7, proto_request.delta)
    self.assertEqual(b'my_key', proto_request.key)

  def testDecrAsync(self):
    """Tests decr_async()."""
    response = MemcacheIncrementResponse()
    response.new_value = 17
    service_method, proto_request, return_value = self.CallMethod(
        'decr_async', args=[b'my_key'], error=None, proto_response=response)
    self.assertEqual('Increment', service_method)
    self.assertEqual(MemcacheIncrementRequest.DECREMENT,
                      proto_request.direction)
    self.assertEqual(1, proto_request.delta)
    self.assertEqual(b'my_key', proto_request.key)
    self.assertEqual(17, return_value.get_result())

  def testIncrVivify(self):
    """Tests incr(), vivifying a non-existant key."""
    response = MemcacheIncrementResponse()
    response.new_value = 2
    service_method, proto_request, return_value = self.CallMethod(
        'incr',
        args=[b'my_key'],
        initial_value=500,
        error=None,
        proto_response=response)
    self.assertEqual('Increment', service_method)
    self.assertEqual(2, return_value)
    self.assertEqual(MemcacheIncrementRequest.INCREMENT,
                      proto_request.direction)
    self.assertEqual(500, proto_request.initial_value)
    self.assertEqual(memcache.TYPE_INT, proto_request.initial_flags)
    self.assertEqual(b'my_key', proto_request.key)

  def testGetStats(self):
    """Tests get_stats()."""
    response = MemcacheStatsResponse()
    stats = response.stats
    stats.hits = 5
    stats.misses = 10
    stats.byte_hits = 15
    stats.items = 20
    stats.bytes = 25
    stats.oldest_item_age = 30
    service_method, proto_request, return_value = self.CallMethod(
        'get_stats', args=[], error=None, proto_response=response)
    expected = {
        memcache.STAT_HITS: 5,
        memcache.STAT_MISSES: 10,
        memcache.STAT_BYTE_HITS: 15,
        memcache.STAT_ITEMS: 20,
        memcache.STAT_BYTES: 25,
        memcache.STAT_OLDEST_ITEM_AGES: 30,
    }
    self.assertEqual(expected, return_value)

  def testOffsetMulti(self):
    """Tests the offset_multi() method."""
    response = MemcacheBatchIncrementResponse()
    item = response.item.add()
    item.increment_status = MemcacheIncrementResponse.OK
    item.new_value = 55
    item = response.item.add()
    item.increment_status = MemcacheIncrementResponse.NOT_CHANGED
    item = response.item.add()
    item.increment_status = MemcacheIncrementResponse.ERROR
    offsets = {b'one': 12, b'two': long(-5), b'three': 0}
    service_method, proto_request, return_value = self.CallMethod(
        'offset_multi',
        args=[offsets],
        key_prefix=b'woot',
        initial_value=14,
        namespace='stuff',
        proto_response=response)

    self.assertEqual(3, len(proto_request.item))
    self.assertEqual('stuff', proto_request.name_space)



    wrk = [proto_request.item[i].key for i in range(3)]
    self.assertTrue(all(w[:4] == b'woot' for w in wrk))
    rk = [w[4:] for w in wrk]
    self.assertEqual(set(rk), set(offsets))

    ione = rk.index(b'one')
    itwo = rk.index(b'two')
    ithree = rk.index(b'three')

    self.assertEqual(0, proto_request.item[ithree].delta)
    self.assertEqual(MemcacheIncrementRequest.INCREMENT,
                      proto_request.item[ithree].direction)
    self.assertEqual(14, proto_request.item[ithree].initial_value)
    self.assertEqual(memcache.TYPE_INT, proto_request.item[0].initial_flags)

    self.assertEqual(5, proto_request.item[itwo].delta)
    self.assertEqual(MemcacheIncrementRequest.DECREMENT,
                      proto_request.item[itwo].direction)
    self.assertEqual(14, proto_request.item[itwo].initial_value)
    self.assertEqual(memcache.TYPE_INT, proto_request.item[1].initial_flags)

    self.assertEqual(12, proto_request.item[ione].delta)
    self.assertEqual(MemcacheIncrementRequest.INCREMENT,
                      proto_request.item[ione].direction)
    self.assertEqual(14, proto_request.item[ione].initial_value)
    self.assertEqual(memcache.TYPE_INT, proto_request.item[2].initial_flags)

    self.assertEqual({rk[0]: 55, rk[1]: None, rk[2]: None}, return_value)

  def testIncrMulti(self):
    """Tests the incr() method with multiple keys."""
    response = MemcacheBatchIncrementResponse()
    item = response.item.add()
    item.increment_status = MemcacheIncrementResponse.OK
    item.new_value = 55
    item = response.item.add()
    item.increment_status = MemcacheIncrementResponse.NOT_CHANGED
    item = response.item.add()
    item.increment_status = MemcacheIncrementResponse.ERROR
    keys = (b'one', b'two', b'three')
    service_method, proto_request, return_value = self.CallMethod(
        'incr',
        args=[keys, 33],
        initial_value=14,
        namespace='stuff',
        proto_response=response)

    self.assertEqual(3, len(proto_request.item))
    self.assertEqual('stuff', proto_request.name_space)



    rk = [proto_request.item[i].key for i in range(3)]
    self.assertEqual(set(rk), set(keys))

    self.assertEqual(33, proto_request.item[0].delta)
    self.assertEqual(MemcacheIncrementRequest.INCREMENT,
                      proto_request.item[0].direction)
    self.assertEqual(14, proto_request.item[0].initial_value)
    self.assertEqual(memcache.TYPE_INT, proto_request.item[0].initial_flags)

    self.assertEqual(33, proto_request.item[1].delta)
    self.assertEqual(MemcacheIncrementRequest.INCREMENT,
                      proto_request.item[1].direction)
    self.assertEqual(14, proto_request.item[1].initial_value)
    self.assertEqual(memcache.TYPE_INT, proto_request.item[1].initial_flags)

    self.assertEqual(33, proto_request.item[2].delta)
    self.assertEqual(MemcacheIncrementRequest.INCREMENT,
                      proto_request.item[2].direction)
    self.assertEqual(14, proto_request.item[2].initial_value)
    self.assertEqual(memcache.TYPE_INT, proto_request.item[2].initial_flags)

    self.assertEqual({rk[0]: 55, rk[1]: None, rk[2]: None}, return_value)

  def testDecrMulti(self):
    """Tests the decr() method with multiple keys."""
    response = MemcacheBatchIncrementResponse()
    item = response.item.add()
    item.increment_status = MemcacheIncrementResponse.OK
    item.new_value = 55
    item = response.item.add()
    item.increment_status = MemcacheIncrementResponse.NOT_CHANGED
    item = response.item.add()
    item.increment_status = MemcacheIncrementResponse.ERROR
    keys = (b'one', b'two', b'three')
    service_method, proto_request, return_value = self.CallMethod(
        'decr',
        args=[keys, 33],
        initial_value=long(14),
        namespace='stuff',
        proto_response=response)
    type_long = memcache.TYPE_LONG
    if six.PY3:
      type_long = memcache.TYPE_INT

    self.assertEqual(3, len(proto_request.item))
    self.assertEqual('stuff', proto_request.name_space)



    rk = [proto_request.item[i].key for i in range(3)]
    self.assertEqual(set(rk), set(keys))

    self.assertEqual(33, proto_request.item[0].delta)
    self.assertEqual(MemcacheIncrementRequest.DECREMENT,
                      proto_request.item[0].direction)
    self.assertEqual(14, proto_request.item[0].initial_value)
    self.assertEqual(type_long, proto_request.item[0].initial_flags)

    self.assertEqual(33, proto_request.item[1].delta)
    self.assertEqual(MemcacheIncrementRequest.DECREMENT,
                      proto_request.item[1].direction)
    self.assertEqual(14, proto_request.item[1].initial_value)
    self.assertEqual(type_long, proto_request.item[1].initial_flags)

    self.assertEqual(33, proto_request.item[2].delta)
    self.assertEqual(MemcacheIncrementRequest.DECREMENT,
                      proto_request.item[2].direction)
    self.assertEqual(14, proto_request.item[2].initial_value)
    self.assertEqual(type_long, proto_request.item[2].initial_flags)

    self.assertEqual({rk[0]: 55, rk[1]: None, rk[2]: None}, return_value)

  def testOffsetMultiBadInitialValue(self):
    """Tests the offset_multi() method with a bad initial value."""
    self.assertRaises(
        TypeError, memcache.offset_multi, {'my_key': 1}, initial_value=1.0)
    self.assertRaises(
        ValueError, memcache.offset_multi, {'my_key': 1}, initial_value=-1)

  def testOffsetMultiBadDelta(self):
    """Tests the offset_multi() method with a bad delta."""
    self.assertRaises(TypeError, memcache.offset_multi, {'my_key': 1.0})

  def testGetStatsTimeout(self):
    """Tests get_stats() with RPC timeout."""
    response = MemcacheStatsResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'get_stats',
        args=[],
        error=apiproxy_errors.DeadlineExceededError('fake error'),
        proto_response=response)
    self.assertEqual(None, return_value)

  def testGetStatsEmptyCache(self):
    """Tests get_stats() on empty cache."""
    response = MemcacheStatsResponse()
    service_method, proto_request, return_value = self.CallMethod(
        'get_stats', args=[], error=None, proto_response=response)
    expected = {
        memcache.STAT_HITS: 0,
        memcache.STAT_MISSES: 0,
        memcache.STAT_BYTE_HITS: 0,
        memcache.STAT_ITEMS: 0,
        memcache.STAT_BYTES: 0,
        memcache.STAT_OLDEST_ITEM_AGES: 0,
    }
    self.assertEqual(expected, return_value)

  def testIncrValidation(self):
    """Tests incr() with a bad delta."""
    self.assertRaises(TypeError, memcache.incr, 'my_key', delta=1.0)
    self.assertRaises(ValueError, memcache.incr, 'my_key', delta=-4)

  def testSetValueValidation(self):
    """Tests set() with bad values."""
    self.assertRaises(ValueError, memcache.set, 'my_key', 'a' * ONE_MEGABYTE)

  def testSetMultiValueValidation(self):
    """Tests set_multi() with bad values."""
    self.assertRaises(ValueError, memcache.set_multi,
                      {'my_key': 'a' * ONE_MEGABYTE})

  def testSetBadExpiration(self):
    """Tests set() with a bad expiration time."""
    self.assertRaises(
        TypeError, memcache.set, 'my_key', 'my_value', time='stuff')
    self.assertRaises(ValueError, memcache.set, 'my_key', 'my_value', time=-1)
    self.assertRaises(ValueError, memcache.set, 'my_key', 'my_value', time=-0.5)

  def testSetMultiBadExpiration(self):
    """Tests set_multi() with a bad expiration time."""
    self.assertRaises(
        TypeError, memcache.set_multi, {'my_key': 'my_value'}, time='stuff')
    self.assertRaises(
        ValueError, memcache.set_multi, {'my_key': 'my_value'}, time=-1)
    self.assertRaises(
        ValueError, memcache.set_multi, {'my_key': 'my_value'}, time=-0.5)

  def testDeleteBadTimeout(self):
    """Tests delete() with a bad timeout."""
    self.assertRaises(TypeError, memcache.delete, 'my_key', seconds='stuff')
    self.assertRaises(ValueError, memcache.delete, 'my_key', seconds=-1)
    self.assertRaises(ValueError, memcache.delete, 'my_key', seconds=-0.5)

  def testDeleteMultiBadTimeout(self):
    """Tests delete_multi() with a bad timeout."""
    self.assertRaises(
        TypeError,
        memcache.delete_multi, ['my_key', 'other_key'],
        seconds='stuff')
    self.assertRaises(
        ValueError, memcache.delete_multi, ['my_key', 'other_key'], seconds=-1)
    self.assertRaises(
        ValueError,
        memcache.delete_multi, ['my_key', 'other_key'],
        seconds=-0.5)

  def testDoPickle(self):
    """Tests _do_pickle."""
    my_value = {
        'asdf': 1,
        'foo': long(2),
        'bar': 1.0,
    }
    client = memcache.Client(pickler=six.moves.cPickle.Pickler)
    stored_value = client._do_pickle(my_value)
    expected_value = six.moves.cPickle.dumps(
        my_value, protocol=six.moves.cPickle.HIGHEST_PROTOCOL)

    self.assertEqual(expected_value, stored_value)

  def testDoPickleWithPersistentId(self):
    """Tests _do_pickle with persistent_id set."""
    my_value = {
        'asdf': 1,
        'foo': long(2),
        'bar': 1.0,
    }
    client = memcache.Client(
        pickler=six.moves.cPickle.Pickler, pid=self.PersistentId)
    stored_value = client._do_pickle(my_value)
    pickle_value = six.BytesIO()
    pickler = six.moves.cPickle.Pickler(
        pickle_value, protocol=six.moves.cPickle.HIGHEST_PROTOCOL)
    pickler.persistent_id = self.PersistentId
    pickler.dump(my_value)
    expected_value = pickle_value.getvalue()

    self.assertEqual(expected_value, stored_value)

  def testDoUnpickle(self):
    """Tests _do_unpickle."""
    expected_value = {
        'asdf': 1,
        'foo': long(2),
        'bar': 1.0,
    }
    my_value = six.moves.cPickle.dumps(
        expected_value, protocol=six.moves.cPickle.HIGHEST_PROTOCOL)
    client = memcache.Client()
    retrieved_value = client._do_unpickle(my_value)

    self.assertEqual(expected_value, retrieved_value)

  def testDoUnpickleWithPersistentLoad(self):
    """Tests _do_unpickle with persistent_load set."""
    my_value = {
        'asdf': 1,
        'foo': long(2),
        'bar': 1.0,
    }
    expected_value = {str(my_value): 2}
    pickle_value = six.BytesIO()
    pickler = six.moves.cPickle.Pickler(
        pickle_value, protocol=six.moves.cPickle.HIGHEST_PROTOCOL)
    pickler.persistent_id = self.PersistentId
    pickler.dump(my_value)
    pickled_value = pickle_value.getvalue()
    client = memcache.Client(pload=lambda x: {x: 2})

    value = client._do_unpickle(pickled_value)
    self.assertEqual(expected_value, value)

  @staticmethod
  def PersistentId(value):
    if isinstance(value, str):
      return None
    else:
      return str(value)


if __name__ == '__main__':
  absltest.main()
