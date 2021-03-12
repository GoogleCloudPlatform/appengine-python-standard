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


"""Unittest for the memcache_stub module"""




import hashlib
import pickle
import time

import six
import six.moves.cPickle

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import memcache
from google.appengine.api import namespace_manager
from google.appengine.api.memcache import memcache_service_pb2
from google.appengine.api.memcache import memcache_stub
from google.appengine.api.memcache import memcache_stub_service_pb2
from absl import logging
from absl.testing import absltest




if six.PY3:
  long = int


class MyClass(object):
  """Dummy class used for pickling tests."""

  def __init__(self):
    """Initializer."""
    self.x = 10


class MemcacheServiceStubTest(absltest.TestCase):
  """Tests memcache service stub."""

  def setUp(self):
    """Set up test fixture."""
    self.when = time.time()
    self.gettime = lambda: self.when

    self.stub = memcache_stub.MemcacheServiceStub(gettime=self.gettime)
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub('memcache', self.stub)

    self.key1 = b'key1'
    self.value1 = b'value1'

    self.key2 = b'key2 is very very long' + b' pad' * 100
    self.value2 = b'value2'



    key2_bytes = self.key2
    if isinstance(key2_bytes, six.text_type):
      key2_bytes = key2_bytes.encode('utf-8')

    self.key2_hash = hashlib.sha1(key2_bytes).hexdigest()
    if isinstance(self.key2_hash, six.text_type):
      self.key2_hash = self.key2_hash.encode('utf-8')

    self.key3 = 'key3'
    self.value3 = 'value3'

  def _StepClock(self, timedelta):
    """Steps the fake clock forward.

    Args:
      timedelta: How far forward to step the fake clock.
    """
    assert timedelta > 0
    self.when += timedelta

  def testSet(self):
    """Tests set with a good key."""
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertTrue(memcache.set(self.key2, self.value2))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(self.value2, memcache.get(self.key2))

  def testSetExpiration(self):
    """Tests that set expires properly with relative and absolute times."""
    for expiration in (self.gettime() + 5, 5):
      self.assertTrue(memcache.set(self.key1, self.value1, time=expiration))
      self.assertEqual(self.value1, memcache.get(self.key1))
      self.assertLen(self.stub._lru, 1)

      self._StepClock(4)
      self.assertEqual(self.value1, memcache.get(self.key1))
      self.assertLen(self.stub._lru, 1)

      self._StepClock(2)
      self.assertEqual(None, memcache.get(self.key1))
      self.assertEmpty(self.stub._lru)

      self.assertTrue(memcache.set(self.key1, self.value1))
      self.assertEqual(self.value1, memcache.get(self.key1))

  def testSetTwice(self):
    """Tests setting the same key twice."""
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertTrue(memcache.set(self.key1, self.value2))
    self.assertEqual(self.value2, memcache.get(self.key1))

  def testSetMulti(self):
    """Tests setting multiple keys."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([], memcache.set_multi(mapping))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(self.value2, memcache.get(self.key2))
    self.assertEqual(self.value3, memcache.get(self.key3))

  def testSetMultiExpiration(self):
    """Tests setting multiple keys with expiration."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    for expiration in (self.gettime() + 5, 5):
      logging.info('Testing with expiration %s', expiration)
      self.assertEqual([], memcache.set_multi(mapping, time=5))

      self._StepClock(4)
      self.assertEqual(self.value1, memcache.get(self.key1))
      self.assertEqual(self.value2, memcache.get(self.key2))
      self.assertEqual(self.value3, memcache.get(self.key3))

      self._StepClock(2)
      self.assertEqual(None, memcache.get(self.key1))
      self.assertEqual(None, memcache.get(self.key2))
      self.assertEqual(None, memcache.get(self.key3))

  def testSetInNamespaces(self):
    """Tests that keys in different namespaces don't clobber each other."""
    self.assertTrue(memcache.set(self.key1, self.value1, namespace='ns1'))
    self.assertTrue(memcache.set(self.key1, self.value2, namespace='ns2'))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(self.value1, memcache.get(self.key1, namespace='ns1'))
    self.assertEqual(self.value2, memcache.get(self.key1, namespace='ns2'))

  def testAddSucceed(self):
    """Tests setting a key that does not exist when policy is ADD."""
    self.assertTrue(memcache.add(self.key1, self.value1))
    self.assertEqual(self.value1, memcache.get(self.key1))

  def testAddFail(self):
    """Tests setting a key that already exists when policy is ADD."""
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertFalse(memcache.add(self.key1, self.value2))
    self.assertEqual(self.value1, memcache.get(self.key1))

  def testAddMulti(self):
    """Tests setting multiple keys when policy is ADD."""
    mapping1 = {
        self.key1: self.value1,
        self.key2: self.value2,
    }
    self.assertEqual([], memcache.add_multi(mapping1))


    mapping2 = {
        self.key2: self.value3,
        self.key3: self.value3,
    }

    self.assertEqual([self.key2], memcache.add_multi(mapping2))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(self.value2, memcache.get(self.key2))
    self.assertEqual(self.value3, memcache.get(self.key3))

  def testAddInNamespace(self):
    """Tests adding keys in two namespaces."""
    self.assertTrue(memcache.add(self.key1, self.value1, namespace='ns1'))
    self.assertTrue(memcache.add(self.key1, self.value2, namespace='ns2'))
    self.assertEqual(self.value1, memcache.get(self.key1, namespace='ns1'))
    self.assertEqual(self.value2, memcache.get(self.key1, namespace='ns2'))

  def testReplaceSucceed(self):
    """Tests setting a key that exists when policy is REPLACE."""
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertTrue(memcache.replace(self.key1, self.value2))
    self.assertEqual(self.value2, memcache.get(self.key1))

  def testReplaceFail(self):
    """Tests setting a key that does not exist when policy is REPLACE."""
    self.assertFalse(memcache.replace(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))

  def testReplaceMulti(self):
    """Tests setting multiple keys when policy is REPLACE."""
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertEqual(memcache.get(self.key1), self.value1)

    mapping = {
        self.key1: self.value2,
        self.key2: self.value2,
    }
    self.assertEqual([self.key2], memcache.replace_multi(mapping))
    self.assertEqual(self.value2, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))

  def testReplaceInNamespace(self):
    """Tests replacing doesn't replace from the wrong namespace."""
    self.assertTrue(memcache.set(self.key1, self.value1, namespace='ns1'))
    self.assertTrue(memcache.replace(self.key1, self.value2, namespace='ns1'))
    self.assertFalse(memcache.replace(self.key1, self.value3, namespace='ns2'))
    self.assertEqual(self.value2, memcache.get(self.key1, namespace='ns1'))

  def testGetMulti(self):
    """Tests getting multiple keys."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([], memcache.set_multi(mapping))
    result = memcache.get_multi(list(mapping.keys()))
    self.assertEqual(len(mapping), len(result))
    for key in result:
      self.assertEqual(mapping[key], result[key])

  def testDelete(self):
    """Tests delete when the item is present."""
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertLen(self.stub._lru, 1)
    self.assertEqual(memcache.DELETE_SUCCESSFUL, memcache.delete(self.key1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEmpty(self.stub._lru)

  def testDeleteMissing(self):
    """Tests delete when the item is missing."""
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(memcache.DELETE_ITEM_MISSING, memcache.delete(self.key1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEmpty(self.stub._lru)

  def testDeleteTimeout_RelativeTimeout(self):
    """Tests delete with a relative timeout."""
    self._TestDeleteTimeout(self.gettime() + 5)

  def testDeleteTimeout_AbsoluteTimeout(self):
    """Tests delete with an absolute timeout."""
    self._TestDeleteTimeout(5)

  def _TestDeleteTimeout(self, timeout):
    """Executes test of deletion with timeout for testDeleteTimeout_* tests."""

    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertLen(self.stub._lru, 1)



    self.assertEqual(memcache.DELETE_SUCCESSFUL,
                     memcache.delete(self.key1, seconds=timeout))
    self.assertFalse(memcache.add(self.key1, self.value1))
    self.assertFalse(memcache.replace(self.key1, self.value1))
    self.assertEqual(0, memcache.get_stats().get('items'))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEmpty(self.stub._lru)



    self._StepClock(4)
    self.assertFalse(memcache.add(self.key1, self.value1))
    self.assertFalse(memcache.replace(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEmpty(self.stub._lru)



    self._StepClock(2)
    self.assertTrue(memcache.add(self.key1, self.value1))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertTrue(memcache.replace(self.key1, self.value2))
    self.assertEqual(self.value2, memcache.get(self.key1))
    self.assertLen(self.stub._lru, 1)

  def testDeleteMulti(self):
    """Tests delete_multi."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([], memcache.set_multi(mapping))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(self.value2, memcache.get(self.key2))
    self.assertEqual(self.value3, memcache.get(self.key3))
    self.assertLen(self.stub._lru, 3)

    self.assertTrue(memcache.delete_multi(list(mapping.keys())))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))
    self.assertEqual(None, memcache.get(self.key3))
    self.assertEmpty(self.stub._lru)

  def testDeleteMultiTimeout(self):
    """Tests delete_multi with relative and absolute timeouts."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    for timeout in (self.gettime() + 5, 5):
      logging.info('Testing with timeout %s', timeout)
      self.assertEqual([], memcache.set_multi(mapping))
      self.assertEqual(self.value1, memcache.get(self.key1))
      self.assertEqual(self.value2, memcache.get(self.key2))
      self.assertEqual(self.value3, memcache.get(self.key3))

      self.assertTrue(
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
        self.assertTrue(memcache.add(key, 'random value'))
        self.assertEqual('random value', memcache.get(key))
        self.assertTrue(memcache.replace(key, 'random value2'))
        self.assertEqual('random value2', memcache.get(key))

  def testSetAfterDeleteWithTimeout(self):
    """Tests that set after a delete with timeout will work."""
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(memcache.DELETE_SUCCESSFUL,
                     memcache.delete(self.key1, seconds=5))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertFalse(memcache.add(self.key1, self.value1))
    self.assertFalse(memcache.replace(self.key1, self.value1))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertEqual(self.value1, memcache.get(self.key1))

  def testIncrementAfterDeleteWithTimeout(self):
    """Tests that increment after a delete with timeout will work properly."""
    self.assertTrue(memcache.set(self.key1, 10))
    self.assertEqual(10, memcache.get(self.key1))
    self.assertEqual(memcache.DELETE_SUCCESSFUL,
                     memcache.delete(self.key1, seconds=5))
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(1, memcache.incr(self.key1, delta=1, initial_value=0))

  def testDeleteRepeatedly(self):
    """Tests deleting an item repeatedly. The last timeout wins."""
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(memcache.DELETE_SUCCESSFUL,
                     memcache.delete(self.key1, seconds=5))
    self.assertEqual(memcache.DELETE_SUCCESSFUL,
                     memcache.delete(self.key1, seconds=1))
    self.assertEqual(memcache.DELETE_SUCCESSFUL,
                     memcache.delete(self.key1, seconds=3))
    self._StepClock(4)
    self.assertEqual(memcache.DELETE_ITEM_MISSING, memcache.delete(self.key1))

  def testDeleteInNamespace(self):
    self.assertTrue(memcache.set(self.key1, self.value1, namespace='ns1'))
    self.assertTrue(memcache.set(self.key1, self.value2, namespace='ns2'))
    self.assertEqual(memcache.DELETE_SUCCESSFUL,
                     memcache.delete(self.key1, namespace='ns1'))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns1'))
    self.assertEqual(self.value2, memcache.get(self.key1, namespace='ns2'))

  def testDeleteLockNamespace(self):
    self.assertTrue(memcache.add(self.key1, self.value1, namespace='ns1'))
    self.assertTrue(memcache.add(self.key1, self.value2, namespace='ns2'))
    self.assertEqual(memcache.DELETE_SUCCESSFUL,
                     memcache.delete(self.key1, namespace='ns1', seconds=5))
    self.assertFalse(memcache.add(self.key1, self.value1, namespace='ns1'))
    self.assertTrue(memcache.add(self.key1, self.value1))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key1, namespace='ns1'))
    self.assertEqual(self.value2, memcache.get(self.key1, namespace='ns2'))

  def testDeleteMultiRepeatedly(self):
    """Tests deleting a set of items repeatedly. The last timeout wins."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([], memcache.set_multi(mapping))
    self.assertTrue(memcache.delete_multi(list(mapping.keys()), seconds=5))
    self.assertTrue(memcache.delete_multi(list(mapping.keys()), seconds=1))
    self.assertTrue(memcache.delete_multi(list(mapping.keys()), seconds=3))
    self._StepClock(4)



    self.assertTrue(memcache.delete_multi(list(mapping.keys())))

  def testIncrementByOne(self):
    """Tests incrementing a key by one."""
    self.assertTrue(memcache.set(self.key1, '0'))
    self.assertEqual(1, memcache.incr(self.key1))
    self.assertEqual('1', memcache.get(self.key1))

  def testIncrementByDelta(self):
    """Tests incrementing a key by a delta."""
    self.assertTrue(memcache.set(self.key1, '0'))
    self.assertEqual(10, memcache.incr(self.key1, delta=10))
    self.assertEqual('10', memcache.get(self.key1))

  def testIncrementOverflow(self):
    """Tests incrementing until overflow."""
    self.assertTrue(memcache.set(self.key1, str(2**64 - 1)))
    self.assertEqual(0, memcache.incr(self.key1))
    self.assertEqual('0', memcache.get(self.key1))

  def testIncrementWrapAround(self):
    self.assertTrue(memcache.set(self.key1, '2'))
    self.assertEqual(1, memcache.incr(self.key1, delta=2**64 - 1))
    self.assertEqual('1', memcache.get(self.key1))
    self.assertTrue(memcache.set(self.key1, 2))
    self.assertEqual(1, memcache.incr(self.key1, delta=2**64 - 1))
    self.assertEqual(1, memcache.get(self.key1))

  def testIncrementUnknownKey(self):
    """Tests increment for a key that does not exist."""
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testIncrementUnknownKeyButVivify(self):
    """Tests increment for a key that does not exist, but with initial_value."""
    self.assertEqual(6, memcache.incr(self.key1, initial_value=5))
    self.assertEqual(6, memcache.get(self.key1))

  def testIncrementBadValue(self):
    """Tests incrementing a value that can't be interpreted as an integer."""
    self.assertTrue(memcache.set(self.key1, 'some data'))
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual('some data', memcache.get(self.key1))

  def testIncrementAnInteger(self):
    """Tests that incrementing an integer works, not a str."""
    self.assertTrue(memcache.set(self.key1, 99))
    self.assertEqual(100, memcache.incr(self.key1))
    self.assertEqual(100, memcache.get(self.key1))

  def testIncrementALong(self):
    """Tests that incrementing a long works."""
    self.assertTrue(memcache.set(self.key1, long(99)))
    self.assertEqual(long(100), memcache.incr(self.key1))
    self.assertEqual(long(100), memcache.get(self.key1))

  def testIncrementAnIntegerPromotedToLong(self):
    """Tests that incrementing a int into a long works."""
    self.assertTrue(memcache.set(self.key1, 2147483647))
    self.assertEqual(2147483647, memcache.get(self.key1))
    self.assertEqual(long(2147483648), memcache.incr(self.key1))
    self.assertEqual(long(2147483648), memcache.get(self.key1))

  def testIncrementANegativeInteger(self):
    """Tests that incrementing a negative value fails."""
    self.assertTrue(memcache.set(self.key1, -5))
    self.assertEqual(None, memcache.incr(self.key1))
    self.assertEqual(-5, memcache.get(self.key1))

  def testDecrementByOne(self):
    """Tests decrementing a key by one."""
    self.assertTrue(memcache.set(self.key1, '10'))
    self.assertEqual(9, memcache.decr(self.key1))
    self.assertEqual('9', memcache.get(self.key1))

  def testDecrementByDelta(self):
    """Tests decrementing a key by a delta."""
    self.assertTrue(memcache.set(self.key1, '11'))
    self.assertEqual(1, memcache.decr(self.key1, delta=10))
    self.assertEqual('1', memcache.get(self.key1))

  def testDecrementCap(self):
    """Tests that decrements are capped at 0."""
    self.assertTrue(memcache.set(self.key1, '5'))
    self.assertEqual(0, memcache.decr(self.key1, delta=10))
    self.assertEqual('0', memcache.get(self.key1))

  def testDecrementUnknownKey(self):
    """Tests decrement for a key that does not exist."""
    self.assertEqual(None, memcache.decr(self.key1))
    self.assertEqual(None, memcache.get(self.key1))

  def testDecrementBadValue(self):
    """Tests decrementing a value that can't be interpreted as an integer."""
    self.assertTrue(memcache.set(self.key1, 'some data'))
    self.assertEqual(None, memcache.decr(self.key1))
    self.assertEqual('some data', memcache.get(self.key1))

  def testDecrementANegativeInteger(self):
    """Tests that decrementing a negative value fails."""
    self.assertTrue(memcache.set(self.key1, -5))
    self.assertEqual(None, memcache.decr(self.key1))
    self.assertEqual(-5, memcache.get(self.key1))

  def testOffsetMulti(self):
    """Tests incrementing a batch of keys all at the same time."""
    self.assertTrue(memcache.set(self.key1, 5))
    self.assertTrue(memcache.set(self.key2, 'blue'))
    offsets = {self.key1: 4, self.key2: 10, self.key3: -2}
    result = memcache.offset_multi(offsets, initial_value=0)
    self.assertEqual({
        self.key1: 9,
        self.key2: None,
        self.key3: 0,
    }, result)
    self.assertEqual(0, memcache.get(self.key3))

  def testFlushAll(self):
    """Tests flushing all data from the cache."""
    mapping = {
        self.key1: self.value1,
        self.key2: self.value2,
        self.key3: self.value3,
    }
    self.assertEqual([], memcache.set_multi(mapping))
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(self.value2, memcache.get(self.key2))
    self.assertEqual(self.value3, memcache.get(self.key3))

    self.assertTrue(memcache.flush_all())
    self.assertEqual(None, memcache.get(self.key1))
    self.assertEqual(None, memcache.get(self.key2))
    self.assertEqual(None, memcache.get(self.key3))

  def testStatsAfterFlush(self):
    """Asserts that the stats are reset after a flush."""


    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertTrue(memcache.set(self.key2, self.value2))


    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(self.value2, memcache.get(self.key2))
    self.assertLen(memcache.get_multi([self.key1, self.key2]), 2)


    self.assertEqual(None, memcache.get(self.key3))
    self.assertEqual(None, memcache.get('unknown'))
    self.assertEqual(None, memcache.get('another not known'))
    self.assertEmpty(memcache.get_multi(['what', 'who']))

    self._StepClock(7)

    result = memcache.get_stats()

    expected = {
        memcache.STAT_HITS: 4,
        memcache.STAT_MISSES: 5,
        memcache.STAT_BYTE_HITS: (2 * (len(self.key1) + len(self.value1) +
                                       len(self.key2_hash) + len(self.value2))),
        memcache.STAT_ITEMS: 2,
        memcache.STAT_BYTES: (len(self.key1) + len(self.value1) +
                              len(self.key2_hash) + len(self.value2)),
        memcache.STAT_OLDEST_ITEM_AGES: 7,
    }

    self.assertEqual(expected, result)


    self.assertTrue(memcache.flush_all())
    result = memcache.get_stats()
    expected = {
        memcache.STAT_HITS: 0,
        memcache.STAT_MISSES: 0,
        memcache.STAT_BYTE_HITS: 0,
        memcache.STAT_ITEMS: 0,
        memcache.STAT_BYTES: 0,
        memcache.STAT_OLDEST_ITEM_AGES: 0,
    }
    self.assertEqual(expected, result)

  def testGetStats(self):
    """Tests get_stats."""
    self.assertTrue(memcache.set(self.key1, self.value1))
    self.assertTrue(memcache.set(self.key2, self.value2))


    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(self.value2, memcache.get(self.key2))
    self.assertLen(memcache.get_multi([self.key1, self.key2]), 2)


    self.assertEqual(None, memcache.get(self.key3))
    self.assertEqual(None, memcache.get('unknown'))
    self.assertEqual(None, memcache.get('another not known'))
    self.assertEmpty(memcache.get_multi(['what', 'who']))

    self._StepClock(7)

    result = memcache.get_stats()

    expected = {
        memcache.STAT_HITS: 4,
        memcache.STAT_MISSES: 5,
        memcache.STAT_BYTE_HITS: (2 * (len(self.key1) + len(self.value1) +
                                       len(self.key2_hash) + len(self.value2))),
        memcache.STAT_ITEMS: 2,
        memcache.STAT_BYTES: (len(self.key1) + len(self.value1) +
                              len(self.key2_hash) + len(self.value2)),
        memcache.STAT_OLDEST_ITEM_AGES: 7,
    }

    self.assertEqual(expected, result)

  def testGetStatsOldestItemAge(self):
    """Tests the oldest_item_age returned by a get_stats call."""
    stats = memcache.get_stats()
    self.assertEqual(0, stats[memcache.STAT_OLDEST_ITEM_AGES])


    memcache.set(self.key1, self.value1)
    self._StepClock(1)
    stats = memcache.get_stats()
    self.assertEqual(1, stats[memcache.STAT_OLDEST_ITEM_AGES])



    memcache.set(self.key2, self.value2)
    self._StepClock(1)
    stats = memcache.get_stats()
    self.assertEqual(2, stats[memcache.STAT_OLDEST_ITEM_AGES])


    memcache.delete(self.key1)
    stats = memcache.get_stats()
    self.assertEqual(1, stats[memcache.STAT_OLDEST_ITEM_AGES])



    self._StepClock(1)
    stats = memcache.get_stats()
    self.assertEqual(2, stats[memcache.STAT_OLDEST_ITEM_AGES])



    memcache.delete(self.key2, 10)
    stats = memcache.get_stats()
    self.assertEqual(0, stats[memcache.STAT_OLDEST_ITEM_AGES])

  def testGetStatsEmptyCache(self):
    """Tests get_stats on empty cache."""
    result = memcache.get_stats()
    expected = {
        memcache.STAT_HITS: 0,
        memcache.STAT_MISSES: 0,
        memcache.STAT_BYTE_HITS: 0,
        memcache.STAT_ITEMS: 0,
        memcache.STAT_BYTES: 0,
        memcache.STAT_OLDEST_ITEM_AGES: 0,
    }
    self.assertEqual(expected, result)

  def testUnicodeKey(self):
    """Tests that unicode keys can be accessed properly."""
    the_value = 'foobar'

    self.assertTrue(memcache.set('asdf', the_value))
    self.assertEqual(the_value, memcache.get('asdf'))
    self.assertEqual(the_value, memcache.get(u'asdf'))

    self.assertTrue(memcache.set(u'asdf', the_value))
    self.assertEqual(the_value, memcache.get('asdf'))
    self.assertEqual(the_value, memcache.get(u'asdf'))


    self.assertTrue(memcache.set(b'\xc3\xa9', the_value))
    self.assertEqual(the_value, memcache.get(b'\xc3\xa9'))
    self.assertEqual(the_value, memcache.get(u'\xe9'))

  def testUnicodeKeyPrefix(self):
    """Tests when a key_prefix is a unicode string."""
    mapping = {
        'one': 'value1',
        'two': 'value2',
        'three': 'value3',
        'four': 'value4'
    }
    key_prefix = u'\xe9:'

    self.assertEqual([], memcache.set_multi(mapping, key_prefix=key_prefix))
    self.assertEqual('value1', memcache.get(u'\xe9:one'))
    self.assertEqual('value1', memcache.get(b'\xc3\xa9:one'))
    self.assertEqual('value2', memcache.get(u'\xe9:two'))
    self.assertEqual('value2', memcache.get(b'\xc3\xa9:two'))
    self.assertEqual('value3', memcache.get(u'\xe9:three'))
    self.assertEqual('value3', memcache.get(b'\xc3\xa9:three'))
    self.assertEqual('value4', memcache.get(u'\xe9:four'))
    self.assertEqual('value4', memcache.get(b'\xc3\xa9:four'))

    output = memcache.get_multi(list(mapping.keys()), key_prefix=key_prefix)
    self.assertEqual(mapping, output)

  def testMultiComplexValues(self):
    """Tests set_multi() and get_multi() with multiple value types."""
    mapping = {'one': u'value1', 'two': 2.0, 'three': 3, 'four': 'value4'}
    self.assertEqual([], memcache.set_multi(mapping))
    self.assertEqual(u'value1', memcache.get('one'))
    self.assertEqual(2.0, memcache.get('two'))
    self.assertEqual(3, memcache.get('three'))
    self.assertEqual('value4', memcache.get('four'))

    output = memcache.get_multi(list(mapping.keys()))
    self.assertEqual(mapping, output)

  def testUnicodeValue(self):
    """Tests when a value is a unicode string with set() and get()."""
    self.assertTrue(memcache.set(self.key1, u'the valu\xe9'))
    self.assertEqual(u'the valu\xe9', memcache.get(self.key1))

  def testPickledValue(self):
    """Tests when a value is a pickled object with set() and get()."""
    self.assertTrue(memcache.set(self.key1, 1234))
    self.assertEqual(1234, memcache.get(self.key1))

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


    self.assertTrue(client.set(self.key1, self.value1))
    self.assertEqual(self.value1, client.get(self.key1))


    self.assertTrue(client.set(self.key2, 1234))
    self.assertEqual(1234, client.get(self.key2))


    self.assertTrue(client.set(self.key3, the_object))
    self.assertIs(the_object, client.get(self.key3))

    client = memcache.Client(pickler=pickle.Pickler, unpickler=pickle.Unpickler)


    self.assertRaises((AttributeError, six.moves.cPickle.UnpicklingError),
                      client.get, self.key3)

  def testMemoClearing(self):


    shared = {'memo-bait': 'yum'}
    one = {'shared': shared}
    two = {'shared': shared}
    client = memcache.Client()
    client.set('one', one)
    client.set('two', two)

    self.assertEqual(client.get('two'), two)

  def testCompareAndSwap(self):


    ns = 'casns'
    client = memcache.Client()


    namespace_manager.set_namespace(None)
    self.assertTrue(client.set(self.key1, self.value1))
    self.assertEqual(client.gets(self.key1), self.value1)
    self.assertTrue(client.cas(self.key1, self.value2))
    self.assertEqual(client.gets(self.key1), self.value2)


    self.assertTrue(client.set(self.key1, self.value1, namespace=ns))
    self.assertEqual(client.gets(self.key1, namespace=ns), self.value1)
    self.assertTrue(client.cas(self.key1, self.value2, namespace=ns))
    self.assertEqual(client.gets(self.key1, namespace=ns), self.value2)


    namespace_manager.set_namespace(ns)
    self.assertTrue(client.set(self.key1, self.value1))
    self.assertEqual(client.gets(self.key1), self.value1)
    self.assertTrue(client.cas(self.key1, self.value2))
    self.assertEqual(client.gets(self.key1), self.value2)
    self.assertTrue(client.cas(self.key1, self.value3, namespace=ns))
    self.assertEqual(client.gets(self.key1), self.value3)



    stub = memcache_stub.MemcacheServiceStub(gettime=self.gettime)


    request = memcache_service_pb2.MemcacheSetRequest()
    item = request.item.add()
    item.key = self.key1
    item.value = b'aaa'
    item.set_policy = memcache_service_pb2.MemcacheSetRequest.SET
    item.expiration_time = 10
    response = memcache_service_pb2.MemcacheSetResponse()
    stub._Dynamic_Set(request, response)
    self.assertEqual(memcache_service_pb2.MemcacheSetResponse.STORED,
                     response.set_status[0])


    request = memcache_service_pb2.MemcacheGetRequest()
    request.key.append(self.key1)
    request.for_cas = True
    response = memcache_service_pb2.MemcacheGetResponse()
    stub._Dynamic_Get(request, response)
    self.assertEqual(b'aaa', response.item[0].value)


    cas_id = response.item[0].cas_id
    self.assertNotEqual(0, cas_id)



    request = memcache_service_pb2.MemcacheSetRequest()
    item = request.item.add()
    item.key = self.key1
    item.value = b'bbb'
    item.set_policy = memcache_service_pb2.MemcacheSetRequest.CAS
    item.expiration_time = 10
    item.for_cas = True
    item.cas_id = cas_id
    response = memcache_service_pb2.MemcacheSetResponse()
    stub._Dynamic_Set(request, response)
    self.assertEqual(memcache_service_pb2.MemcacheSetResponse.STORED,
                     response.set_status[0])



    request = memcache_service_pb2.MemcacheSetRequest()
    item = request.item.add()
    item.key = self.key1
    item.value = b'ccc'
    item.set_policy = memcache_service_pb2.MemcacheSetRequest.CAS
    item.expiration_time = 10
    item.for_cas = True
    item.cas_id = cas_id
    response = memcache_service_pb2.MemcacheSetResponse()
    stub._Dynamic_Set(request, response)
    self.assertEqual(memcache_service_pb2.MemcacheSetResponse.EXISTS,
                     response.set_status[0])



    request = memcache_service_pb2.MemcacheGetRequest()
    request.key.append(self.key1)
    request.for_cas = True
    response = memcache_service_pb2.MemcacheGetResponse()
    stub._Dynamic_Get(request, response)
    self.assertEqual(b'bbb', response.item[0].value)

    cas_id = response.item[0].cas_id
    self.assertNotEqual(0, cas_id)


    request = memcache_service_pb2.MemcacheSetRequest()
    item = request.item.add()
    item.key = self.key1
    item.value = b'ccc'
    item.set_policy = memcache_service_pb2.MemcacheSetRequest.CAS
    item.expiration_time = 10
    item.cas_id = cas_id
    response = memcache_service_pb2.MemcacheSetResponse()
    stub._Dynamic_Set(request, response)
    self.assertEqual(memcache_service_pb2.MemcacheSetResponse.STORED,
                     response.set_status[0])

  def testLeastRecentlyUsedEviction(self):

    max_cache_size = len(self.key1 + self.value1 + self.key2_hash +
                         self.value2) + 1
    apiproxy_stub_map.apiproxy.ReplaceStub('memcache',
                                           memcache_stub.MemcacheServiceStub(
                                               gettime=self.gettime,
                                               max_size_bytes=max_cache_size))


    memcache.set(self.key1, self.value1)
    self._StepClock(1000)
    memcache.set(self.key2, self.value2)
    self._StepClock(1000)
    self.assertEqual(self.value1, memcache.get(self.key1))
    self.assertEqual(self.value2, memcache.get(self.key2))


    memcache.set(self.key3, self.value3)
    self.assertEqual(self.value3, memcache.get(self.key3))
    self.assertEqual(self.value2, memcache.get(self.key2))
    self.assertIsNone(memcache.get(self.key1))

  def testSetClock(self):
    """Tests that the clock time is frozen when setting the clock."""
    request = memcache_stub_service_pb2.SetClockRequest
    request.clock_time_milliseconds = 12345
    self.stub._Dynamic_SetClock(request, None)

    self.assertEqual(12.345, self.stub._gettime())
    time.sleep(2)
    self.assertEqual(12.345, self.stub._gettime())

  def testAdvanceClock(self):
    """Tests advancing a frozen clock."""

    self.stub._static_clock_time = 200
    self.stub._gettime = lambda: self.stub._static_clock_time
    self.assertEqual(200, self.stub._gettime())


    request = memcache_stub_service_pb2.AdvanceClockRequest
    request.milliseconds = 1000
    response = memcache_stub_service_pb2.AdvanceClockResponse
    self.stub._Dynamic_AdvanceClock(request, response)
    self.assertEqual(201000, response.clock_time_milliseconds)
    self.assertEqual(201, self.stub._gettime())

  def testGetLruChainLength(self):
    """Tests that verify a call to get the LRU chain length."""
    response = memcache_stub_service_pb2.GetLruChainLengthResponse
    self.stub._Dynamic_GetLruChainLength(None, response)
    self.assertEqual(0, response.chain_length)

    memcache.set(self.key1, self.value1)
    self.stub._Dynamic_GetLruChainLength(None, response)
    self.assertEqual(1, response.chain_length)

    memcache.set(self.key2, self.value2)
    self.stub._Dynamic_GetLruChainLength(None, response)
    self.assertEqual(2, response.chain_length)

    memcache.set(self.key3, self.value3)
    self.stub._Dynamic_GetLruChainLength(None, response)
    self.assertEqual(3, response.chain_length)

    memcache.delete(self.key1)
    self.stub._Dynamic_GetLruChainLength(None, response)
    self.assertEqual(2, response.chain_length)

    memcache.delete(self.key2)
    self.stub._Dynamic_GetLruChainLength(None, response)
    self.assertEqual(1, response.chain_length)

    memcache.delete(self.key3)
    self.stub._Dynamic_GetLruChainLength(None, response)
    self.assertEqual(0, response.chain_length)

  def testSetMaxSize(self):
    request = memcache_stub_service_pb2.SetMaxSizeRequest
    request.max_size_bytes = 1000
    self.stub._Dynamic_SetMaxSize(request, None)
    self.assertEqual(1000, self.stub._max_size_bytes)


class LRUChainableElementTest(absltest.TestCase):

  def testLength(self):
    self.assertEqual(1, memcache_stub._LRUChainableElement('a').byte_size)
    self.assertEqual(2, memcache_stub._LRUChainableElement('ab').byte_size)
    self.assertEqual(4, memcache_stub._LRUChainableElement('abcd').byte_size)
    self.assertEqual(0, memcache_stub._LRUChainableElement().byte_size)


class LRUTest(absltest.TestCase):
  """Tests for the LRU cache.

  Heavily inspired by //jt/c/g/appengine/api/memcache/dev/LRUTest.java.
  """

  def setUp(self):
    self.element1 = memcache_stub._LRUChainableElement('a')
    self.element2 = memcache_stub._LRUChainableElement('ab')
    self.element3 = memcache_stub._LRUChainableElement('abcd')
    self.lru = memcache_stub.LRU()

  def _VerifyChain(self, lru, *chain):
    self.assertEqual(len(lru), len(chain))
    if chain:
      self.assertEqual(lru.newest, chain[0])
      self.assertEqual(lru.oldest, chain[-1])
    else:
      self.assertIsNone(lru.newest)
      self.assertIsNone(lru.oldest)

    total_size = 0
    for idx, elem in enumerate(chain):
      total_size += elem.byte_size
      if idx != 0:
        self.assertEqual(elem.newer, chain[idx - 1])
      else:
        self.assertIsNone(elem.newer)
      if idx != len(chain) - 1:
        self.assertEqual(elem.older, chain[idx + 1])
      else:
        self.assertIsNone(elem.older)
    self.assertEqual(lru.total_byte_size, total_size)

  def _VerifyOrphan(self, item):
    self.assertIsNone(item.newer)
    self.assertIsNone(item.older)

  def _UpdateAndVerifyLengthAndSize(self, item, expected_length, expected_size):
    self.lru.Update(item)
    self.assertLen(self.lru, expected_length)
    self.assertEqual(expected_size, self.lru.total_byte_size)

  def _RemoveAndVerifyLengthAndSize(self, item, expected_length, expected_size):
    self.lru.Remove(item)
    self.assertLen(self.lru, expected_length)
    self.assertEqual(expected_size, self.lru.total_byte_size)

  def _RemoveOldestAndVerifyLengthAndSize(self, expected_length, expected_size):
    self.lru.RemoveOldest()
    self.assertLen(self.lru, expected_length)
    self.assertEqual(expected_size, self.lru.total_byte_size)

  def testAddThree(self):
    self._UpdateAndVerifyLengthAndSize(self.element3, 1, 4)
    self._UpdateAndVerifyLengthAndSize(self.element2, 2, 6)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._VerifyChain(self.lru, self.element1, self.element2, self.element3)

  def testUpdate(self):
    self._UpdateAndVerifyLengthAndSize(self.element3, 1, 4)
    self._UpdateAndVerifyLengthAndSize(self.element2, 2, 6)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._UpdateAndVerifyLengthAndSize(self.element2, 3, 7)
    self._VerifyChain(self.lru, self.element2, self.element1, self.element3)

  def testUpdateFirst(self):
    self._UpdateAndVerifyLengthAndSize(self.element3, 1, 4)
    self._UpdateAndVerifyLengthAndSize(self.element2, 2, 6)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._VerifyChain(self.lru, self.element1, self.element2, self.element3)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._VerifyChain(self.lru, self.element1, self.element2, self.element3)

  def testUpdateLast(self):
    self._UpdateAndVerifyLengthAndSize(self.element3, 1, 4)
    self._UpdateAndVerifyLengthAndSize(self.element2, 2, 6)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._VerifyChain(self.lru, self.element1, self.element2, self.element3)
    self._UpdateAndVerifyLengthAndSize(self.element3, 3, 7)
    self._VerifyChain(self.lru, self.element3, self.element1, self.element2)

  def testRemove(self):
    self._UpdateAndVerifyLengthAndSize(self.element3, 1, 4)
    self._UpdateAndVerifyLengthAndSize(self.element2, 2, 6)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._RemoveAndVerifyLengthAndSize(self.element2, 2, 5)
    self._VerifyChain(self.lru, self.element1, self.element3)
    self._VerifyOrphan(self.element2)

  def testRemoveFirst(self):
    self._UpdateAndVerifyLengthAndSize(self.element3, 1, 4)
    self._UpdateAndVerifyLengthAndSize(self.element2, 2, 6)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._RemoveAndVerifyLengthAndSize(self.element1, 2, 6)
    self._VerifyChain(self.lru, self.element2, self.element3)
    self._VerifyOrphan(self.element1)

  def testRemoveLast(self):
    self._UpdateAndVerifyLengthAndSize(self.element3, 1, 4)
    self._UpdateAndVerifyLengthAndSize(self.element2, 2, 6)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._RemoveAndVerifyLengthAndSize(self.element3, 2, 3)
    self._VerifyChain(self.lru, self.element1, self.element2)
    self._VerifyOrphan(self.element3)

  def testRemoveOldest(self):
    self._UpdateAndVerifyLengthAndSize(self.element3, 1, 4)
    self._UpdateAndVerifyLengthAndSize(self.element2, 2, 6)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._RemoveOldestAndVerifyLengthAndSize(2, 3)
    self._VerifyChain(self.lru, self.element1, self.element2)
    self._VerifyOrphan(self.element3)

  def testRemoveAll(self):
    self._UpdateAndVerifyLengthAndSize(self.element3, 1, 4)
    self._UpdateAndVerifyLengthAndSize(self.element2, 2, 6)
    self._UpdateAndVerifyLengthAndSize(self.element1, 3, 7)
    self._RemoveOldestAndVerifyLengthAndSize(2, 3)
    self._RemoveOldestAndVerifyLengthAndSize(1, 1)
    self._RemoveOldestAndVerifyLengthAndSize(0, 0)
    self._VerifyChain(self.lru)
    self._VerifyOrphan(self.element1)
    self._VerifyOrphan(self.element2)
    self._VerifyOrphan(self.element3)




if __name__ == '__main__':
  absltest.main()

