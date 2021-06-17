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

"""Unittest for the memcache_stub module when memcache is unavailable."""



import time

from absl import logging
import six

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import memcache
from google.appengine.api.memcache import memcache_stub
from google.appengine.runtime import apiproxy_errors
from absl.testing import absltest


if six.PY3:
  long = int


class _MemcacheServiceUnavailableStub(memcache_stub.MemcacheServiceStub):
  """Service stub for unavailable memcache always gives application error."""

  def __init__(self, gettime=time.time):
    super(_MemcacheServiceUnavailableStub, self).__init__(gettime=gettime)

  def _Dynamic_Get(self, request, response):
    self._Unavailable()

  def _Dynamic_Set(self, request, response):
    self._Unavailable()

  def _Dynamic_Delete(self, request, response):
    self._Unavailable()

  def _internal_increment(self, namespace, request):
    self._Unavailable()

  def _Dynamic_Increment(self, request, response):
    self._Unavailable()

  def _Dynamic_BatchIncrement(self, request, response):
    self._Unavailable()

  def _Dynamic_FlushAll(self, request, response):
    self._Unavailable()

  def _Dynamic_Stats(self, request, response):
    self._Unavailable()

  def _Unavailable(self):
    raise apiproxy_errors.CapabilityDisabledError('some error')


class MemcacheServiceUnavailableTest(absltest.TestCase):
  """Tests memcache unavailable."""

  def setUp(self):
    """Set up test fixture."""
    self.when = time.time()
    self.gettime = lambda: self.when

    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub(
        'memcache', _MemcacheServiceUnavailableStub(gettime=self.gettime))

    self.key1 = 'key1'
    self.value1 = 'value1'

    self.key2 = 'key2 is very very long' + ' pad' * 100
    self.value2 = 'value2'

    self.key3 = 'key3'
    self.value3 = 'value3'

  def _StepClock(self, timedelta):
    """Steps the fake clock forward.

    Args:
      timedelta: How far forward to step the fake clock.
    """
    assert timedelta > 0
    self.when += timedelta

  def testCasMultiAsync(self):
    """Tests setting multiple keys."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    client = memcache.Client()
    rpc = client.cas_multi_async(mapping)
    self.assertEqual(None, rpc.get_result())
    self.assertRaises(apiproxy_errors.CapabilityDisabledError,
                      rpc.check_success)

  def testSetMultiAsync(self):
    """Tests CAS multiple keys."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    client = memcache.Client()
    rpc = client.set_multi_async(mapping)
    self.assertEqual(None, rpc.get_result())
    self.assertRaises(apiproxy_errors.CapabilityDisabledError,
                      rpc.check_success)

  def testGetMultiAsync(self):
    """Tests getting multiple keys."""
    keys = [self.key1, self.key2, self.key3]
    client = memcache.Client()
    rpc = client.get_multi_async(keys)
    self.assertEqual({}, rpc.get_result())
    self.assertRaises(apiproxy_errors.CapabilityDisabledError,
                      rpc.check_success)

  def testGetStatsAsync(self):
    """Tests getting stats."""
    client = memcache.Client()
    rpc = client.get_stats_async()
    self.assertEqual(None, rpc.get_result())
    self.assertRaises(apiproxy_errors.CapabilityDisabledError,
                      rpc.check_success)

  def testFlushAllAsync(self):
    """Tests getting stats."""
    client = memcache.Client()
    rpc = client.flush_all_async()
    self.assertFalse(rpc.get_result())
    self.assertRaises(apiproxy_errors.CapabilityDisabledError,
                      rpc.check_success)

  def testDeleteMultiAsync(self):
    """Tests delete_multi."""
    keys = [self.key1, self.key2, self.key3]
    client = memcache.Client()
    rpc = client.delete_multi_async(keys)
    self.assertEqual(None, rpc.get_result())
    self.assertRaises(apiproxy_errors.CapabilityDisabledError,
                      rpc.check_success)

  def testAddMultiAsync(self):
    """Tests add_multi."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    client = memcache.Client()
    rpc = client.add_multi_async(mapping)
    self.assertEqual(None, rpc.get_result())
    self.assertRaises(apiproxy_errors.CapabilityDisabledError,
                      rpc.check_success)

  def testSet(self):
    """Tests set with a good key."""
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertFalse(memcache.set(self.key2, self.value2))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))

  def testSetExpiration(self):
    """Tests that set expires properly with relative and absolute times."""
    for expiration in (self.gettime() + 5, 5):
      self.assertFalse(memcache.set(self.key1, self.value1, time=expiration))
      self.assertEqual(None, memcache.get(self.key1))

      self._StepClock(4)
      self.assertEqual(None, memcache.get(self.key1))

      self._StepClock(2)
      self.assertEqual(None, memcache.get(self.key1))

      self.assertFalse(memcache.set(self.key1, self.value1))
      self.assertEqual(None, memcache.get(self.key1))

  def testSetTwice(self):
    """Tests setting the same key twice."""
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertFalse(memcache.set(self.key1, self.value2))
    self.assertEqual(None, memcache.get(self.key1))

  def testSetMulti(self):
    """Tests setting multiple keys."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([self.key1, self.key2, self.key3],
                     sorted(memcache.set_multi(mapping)))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))
    self.assertEqual(None, memcache.get(self.key3))

  def testSetMultiExpiration(self):
    """Tests setting multiple keys with expiration."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    for expiration in (self.gettime() + 5, 5):
      logging.info('Testing with expiration %s', expiration)
      self.assertEqual([self.key1, self.key2, self.key3],
                       sorted(memcache.set_multi(mapping, time=5)))

      self._StepClock(4)
      self.assertEqual(None, memcache.get(self.key1))
      self.assertEqual(None, memcache.get(self.key2))
      self.assertEqual(None, memcache.get(self.key3))

      self._StepClock(2)
      self.assertEqual(None, memcache.get(self.key1))
      self.assertEqual(None, memcache.get(self.key2))
      self.assertEqual(None, memcache.get(self.key3))

  def testSetInNamespaces(self):
    """Tests that keys in different namespaces don't clobber each other."""
    self.assertFalse(memcache.set(self.key1, self.value1, namespace='ns1'))
    self.assertFalse(memcache.set(self.key1, self.value2, namespace='ns2'))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns1'))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns2'))

  def testAddSucceed(self):
    """Tests setting a key that does not exist when policy is ADD."""
    self.assertFalse(memcache.add(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))

  def testAddFail(self):
    """Tests setting a key that already exists when policy is ADD."""
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertFalse(memcache.add(self.key1, self.value2))
    self.assertEqual(None, memcache.get(self.key1))

  def testAddMulti(self):
    """Tests setting multiple keys when policy is ADD."""
    mapping1 = {
        self.key1: self.value1,
        self.key2: self.value2,
    }
    self.assertEqual([self.key1, self.key2],
                     sorted(memcache.add_multi(mapping1)))


    mapping2 = {
        self.key2: self.value3,
        self.key3: self.value3,
    }

    self.assertEqual([self.key2, self.key3],
                     sorted(memcache.add_multi(mapping2)))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))
    self.assertEqual(None, memcache.get(self.key3))

  def testAddInNamespace(self):
    """Tests adding keys in two namespaces."""
    self.assertFalse(memcache.add(self.key1, self.value1, namespace='ns1'))
    self.assertFalse(memcache.add(self.key1, self.value2, namespace='ns2'))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns1'))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns2'))

  def testReplaceSucceed(self):
    """Tests setting a key that exists when policy is REPLACE."""
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertFalse(memcache.replace(self.key1, self.value2))
    self.assertEqual(None, memcache.get(self.key1))

  def testReplaceFail(self):
    """Tests setting a key that does not exist when policy is REPLACE."""
    self.assertFalse(memcache.replace(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))

  def testReplaceMulti(self):
    """Tests setting multiple keys when policy is REPLACE."""
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertEqual(memcache.get(self.key1), None)

    mapping = {
        self.key1: self.value2,
        self.key2: self.value2,
    }
    self.assertEqual([self.key1, self.key2],
                     sorted(memcache.replace_multi(mapping)))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))

  def testReplaceInNamespace(self):
    """Tests replacing doesn't replace from the wrong namespace."""
    self.assertFalse(memcache.set(self.key1, self.value1, namespace='ns1'))
    self.assertFalse(memcache.replace(self.key1, self.value2, namespace='ns1'))
    self.assertFalse(memcache.replace(self.key1, self.value3, namespace='ns2'))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns1'))

  def testGetMulti(self):
    """Tests getting multiple keys."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([self.key1, self.key2, self.key3],
                     sorted(memcache.set_multi(mapping)))
    result = memcache.get_multi(list(mapping.keys()))
    self.assertEmpty(result)

  def testDelete(self):
    """Tests delete when the item is present."""
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testDeleteMissing(self):
    """Tests delete when the item is missing."""
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testDeleteTimeout(self):
    """Tests delete with relative and absolute timeouts."""
    for timeout in (self.gettime() + 5, 5):
      logging.info('Testing with timeout %s', timeout)
      self.assertFalse(memcache.set(self.key1, self.value1))
      self.assertEqual(None, memcache.get(self.key1))

      self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                       memcache.delete(self.key1, seconds=timeout))
      self.assertFalse(memcache.add(self.key1, self.value1))
      self.assertFalse(memcache.replace(self.key1, self.value1))
      self.assertEqual(None, memcache.get(self.key1))

      self._StepClock(4)
      self.assertFalse(memcache.add(self.key1, self.value1))
      self.assertFalse(memcache.replace(self.key1, self.value1))
      self.assertEqual(None, memcache.get(self.key1))

      self._StepClock(2)
      self.assertFalse(memcache.add(self.key1, self.value1))
      self.assertEqual(None, memcache.get(self.key1))
      self.assertFalse(memcache.replace(self.key1, self.value2))
      self.assertEqual(None, memcache.get(self.key1))

  def testDeleteMulti(self):
    """Tests delete_multi."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([self.key1, self.key2, self.key3],
                     sorted(memcache.set_multi(mapping)))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))
    self.assertEqual(None, memcache.get(self.key3))

    self.assertFalse(memcache.delete_multi(list(mapping.keys())))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))
    self.assertEqual(None, memcache.get(self.key3))

  def testDeleteMultiTimeout(self):
    """Tests delete_multi with relative and absolute timeouts."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    for timeout in (self.gettime() + 5, 5):
      logging.info('Testing with timeout %s', timeout)
      self.assertEqual([self.key1, self.key2, self.key3],
                       sorted(memcache.set_multi(mapping)))
      self.assertEqual(None, memcache.get(self.key1))
      self.assertEqual(None, memcache.get(self.key2))
      self.assertEqual(None, memcache.get(self.key3))

      self.assertFalse(
          memcache.delete_multi(list(mapping.keys()), seconds=timeout))
      for key in mapping:
        self.assertEqual(None, memcache.get(key))
        self.assertFalse(memcache.add(key, 'random value'))
        self.assertFalse(memcache.replace(key, 'random value'))

      self._StepClock(4)
      for key in mapping:
        self.assertFalse(memcache.add(key, 'random value'))
        self.assertFalse(memcache.replace(key, 'random value'))
        self.assertEqual(None, memcache.get(self.key1))

      self._StepClock(2)
      for key in mapping:
        self.assertFalse(memcache.add(key, 'random value'))
        self.assertEqual(None, memcache.get(key))
        self.assertFalse(memcache.replace(key, 'random value2'))
        self.assertEqual(None, memcache.get(key))

  def testSetAfterDeleteWithTimeout(self):
    """Tests that set after a delete with timeout will work."""
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1, seconds=5))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertFalse(memcache.add(self.key1, self.value1))
    self.assertFalse(memcache.replace(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementAfterDeleteWithTimeout(self):
    """Tests that increment after a delete with timeout will work properly."""
    self.assertFalse(memcache.set(self.key1, 10))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1, seconds=5))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.incr(self.key1, delta=1, initial_value=0))

  def testDeleteRepeatedly(self):
    """Tests deleting an item repeatedly. The last timeout wins."""
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1, seconds=5))
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1, seconds=1))
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1, seconds=3))
    self._StepClock(4)
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1))

  def testDeleteInNamespace(self):
    self.assertFalse(memcache.set(self.key1, self.value1, namespace='ns1'))
    self.assertFalse(memcache.set(self.key1, self.value2, namespace='ns2'))
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1, namespace='ns1'))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns1'))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns2'))

  def testDeleteLockNamespace(self):
    self.assertFalse(memcache.add(self.key1, self.value1, namespace='ns1'))
    self.assertFalse(memcache.add(self.key1, self.value2, namespace='ns2'))
    self.assertEqual(memcache.DELETE_NETWORK_FAILURE,
                     memcache.delete(self.key1, namespace='ns1', seconds=5))
    self.assertFalse(memcache.add(self.key1, self.value1, namespace='ns1'))
    self.assertFalse(memcache.add(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns1'))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns2'))

  def testDeleteMultiRepeatedly(self):
    """Tests deleting a set of items repeatedly. The last timeout wins."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([self.key1, self.key2, self.key3],
                     sorted(memcache.set_multi(mapping)))
    self.assertFalse(memcache.delete_multi(list(mapping.keys()), seconds=5))
    self.assertFalse(memcache.delete_multi(list(mapping.keys()), seconds=1))
    self.assertFalse(memcache.delete_multi(list(mapping.keys()), seconds=3))
    self._StepClock(4)

    self.assertFalse(memcache.delete_multi(list(mapping.keys())))

  def testIncrementByOne(self):
    """Tests incrementing a key by one."""
    self.assertFalse(memcache.set(self.key1, '0'))
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementByDelta(self):
    """Tests incrementing a key by a delta."""
    self.assertFalse(memcache.set(self.key1, '0'))
    self.assertEqual(None, memcache.incr(self.key1, delta=10))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementOverflow(self):
    """Tests incrementing until overflow."""
    self.assertFalse(memcache.set(self.key1, str(2**64 - 1)))
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementWrapAround(self):
    self.assertFalse(memcache.set(self.key1, '2'))
    self.assertEqual(None, memcache.incr(self.key1, delta=2**64 - 1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertFalse(memcache.set(self.key1, 2))
    self.assertEqual(None, memcache.incr(self.key1, delta=2**64 - 1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementUnknownKey(self):
    """Tests increment for a key that does not exist."""
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementUnknownKeyButVivify(self):
    """Tests increment for a key that does not exist, but with initial_value."""
    self.assertEqual(None, memcache.incr(self.key1, initial_value=5))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementBadValue(self):
    """Tests incrementing a value that can't be interpreted as an integer."""
    self.assertFalse(memcache.set(self.key1, 'some data'))
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementAnInteger(self):
    """Tests that incrementing an integer works, not a str."""
    self.assertFalse(memcache.set(self.key1, 99))
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementALong(self):
    """Tests that incrementing a long works."""
    self.assertFalse(memcache.set(self.key1, long(99)))
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementAnIntegerPromotedToLong(self):
    """Tests that incrementing a int into a long works."""
    self.assertFalse(memcache.set(self.key1, 2147483647))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementANegativeInteger(self):
    """Tests that incrementing a negative value fails."""
    self.assertFalse(memcache.set(self.key1, -5))
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testDecrementByOne(self):
    """Tests decrementing a key by one."""
    self.assertFalse(memcache.set(self.key1, '10'))
    self.assertEqual(None, memcache.decr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testDecrementByDelta(self):
    """Tests decrementing a key by a delta."""
    self.assertFalse(memcache.set(self.key1, '11'))
    self.assertEqual(None, memcache.decr(self.key1, delta=10))
    self.assertEqual(None, memcache.get(self.key1))

  def testDecrementCap(self):
    """Tests that decrements are capped at 0."""
    self.assertFalse(memcache.set(self.key1, '5'))
    self.assertEqual(None, memcache.decr(self.key1, delta=10))
    self.assertEqual(None, memcache.get(self.key1))

  def testDecrementUnknownKey(self):
    """Tests decrement for a key that does not exist."""
    self.assertEqual(None, memcache.decr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testDecrementBadValue(self):
    """Tests decrementing a value that can't be interpreted as an integer."""
    self.assertFalse(memcache.set(self.key1, 'some data'))
    self.assertEqual(None, memcache.decr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testDecrementANegativeInteger(self):
    """Tests that decrementing a negative value fails."""
    self.assertFalse(memcache.set(self.key1, -5))
    self.assertEqual(None, memcache.decr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testOffsetMulti(self):
    """Tests incrementing a batch of keys all at the same time."""
    self.assertFalse(memcache.set(self.key1, 5))
    self.assertFalse(memcache.set(self.key2, 'blue'))
    offsets = {self.key1: 4, self.key2: 10, self.key3: -2}
    result = memcache.offset_multi(offsets, initial_value=0)
    self.assertEqual({
        self.key1: None,
        self.key2: None,
        self.key3: None
    }, result)
    self.assertEqual(None, memcache.get(self.key3))

  def testFlushAll(self):
    """Tests flushing all data from the cache."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([self.key1, self.key2, self.key3],
                     sorted(memcache.set_multi(mapping)))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))
    self.assertEqual(None, memcache.get(self.key3))

    self.assertFalse(memcache.flush_all())
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))
    self.assertEqual(None, memcache.get(self.key3))

  def testGetStats(self):
    """Tests get_stats."""
    self.assertFalse(memcache.set(self.key1, self.value1))
    self.assertFalse(memcache.set(self.key2, self.value2))


    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))
    self.assertEmpty(memcache.get_multi([self.key1, self.key2]))


    self.assertEqual(None, memcache.get(self.key3))
    self.assertEqual(None, memcache.get('unknown'))
    self.assertEqual(None, memcache.get('another not known'))
    self.assertEmpty(memcache.get_multi(['what', 'who']))

    self._StepClock(7)

    result = memcache.get_stats()


    expected = None
    self.assertEqual(expected, result)

  def testGetStatsEmptyCache(self):
    """Tests get_stats on empty cache."""
    result = memcache.get_stats()

    expected = None
    self.assertEqual(expected, result)

  def testUnicodeKey(self):
    """Tests that unicode keys can be accessed properly."""
    the_value = 'foobar'

    self.assertFalse(memcache.set('asdf', the_value))
    self.assertEqual(None, memcache.get('asdf'))
    self.assertEqual(None, memcache.get(u'asdf'))

    self.assertFalse(memcache.set(u'asdf', the_value))
    self.assertEqual(None, memcache.get('asdf'))
    self.assertEqual(None, memcache.get(u'asdf'))


    self.assertFalse(memcache.set('\xc3\xa9', the_value))
    self.assertEqual(None, memcache.get('\xc3\xa9'))
    self.assertEqual(None, memcache.get(u'\xe9'))

  def testUnicodeKeyPrefix(self):
    """Tests when a key_prefix is a unicode string."""
    mapping = {
        'one': 'value1',
        'two': 'value2',
        'three': 'value3',
        'four': 'value4'
    }
    key_prefix = u'\xe9:'

    self.assertEqual(['four', 'one', 'three', 'two'],
                     sorted(memcache.set_multi(mapping, key_prefix=key_prefix)))
    self.assertEqual(None, memcache.get(u'\xe9:one'))
    self.assertEqual(None, memcache.get('\xc3\xa9:one'))
    self.assertEqual(None, memcache.get(u'\xe9:two'))
    self.assertEqual(None, memcache.get('\xc3\xa9:two'))
    self.assertEqual(None, memcache.get(u'\xe9:three'))
    self.assertEqual(None, memcache.get('\xc3\xa9:three'))
    self.assertEqual(None, memcache.get(u'\xe9:four'))
    self.assertEqual(None, memcache.get('\xc3\xa9:four'))

    output = memcache.get_multi(list(mapping.keys()), key_prefix=key_prefix)
    self.assertEqual({}, output)

  def testMultiComplexValues(self):
    """Tests set_multi() and get_multi() with multiple value types."""
    mapping = {'one': u'value1', 'two': 2.0, 'three': 3, 'four': 'value4'}
    self.assertEqual(['four', 'one', 'three', 'two'],
                     sorted(memcache.set_multi(mapping)))
    self.assertEqual(None, memcache.get('one'))
    self.assertEqual(None, memcache.get('two'))
    self.assertEqual(None, memcache.get('three'))
    self.assertEqual(None, memcache.get('four'))

    output = memcache.get_multi(list(mapping.keys()))
    self.assertEqual({}, output)

  def testUnicodeValue(self):
    """Tests when a value is a unicode string with set() and get()."""
    self.assertFalse(memcache.set(self.key1, u'the valu\xe9'))
    self.assertEqual(None, memcache.get(self.key1))

  def testPickledValue(self):
    """Tests when a value is a pickled object with set() and get()."""
    self.assertFalse(memcache.set(self.key1, 1234))
    self.assertEqual(None, memcache.get(self.key1))

  def testPersistentId(self):
    """Tests using pickle persistent ids."""
    the_object = object()

    def _PersistentId(value):
      if value is the_object:
        return 'one'
      return None

    def _PersistentLoad(value):
      if value == 'one':
        return the_object
      return None

    client = memcache.Client(pid=_PersistentId, pload=_PersistentLoad)


    self.assertFalse(client.set(self.key1, self.value1))
    self.assertEqual(None, client.get(self.key1))


    self.assertFalse(client.set(self.key2, 1234))
    self.assertEqual(None, client.get(self.key2))


    self.assertFalse(client.set(self.key3, the_object))
    self.assertIsNot(the_object, client.get(self.key3))

  def testMemoClearing(self):


    shared = {'memo-bait': 'yum'}
    one = {'shared': shared}
    two = {'shared': shared}
    client = memcache.Client()
    client.set('one', one)
    client.set('two', two)

    self.assertEqual(client.get('two'), None)




if __name__ == '__main__':
  absltest.main()
