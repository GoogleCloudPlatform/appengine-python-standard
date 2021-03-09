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



"""Tests for google.appengine.ext.key_range."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import random
import string

import mox
import six
from six.moves import range
from six.moves import zip

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.ext import db
from google.appengine.ext import key_range as key_range_module
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from absl.testing import absltest




KIND = 'test_kind'
APP_ID = 'test_app'


def MakeKey(id_or_name, kind=KIND, parent_path=None, namespace=None):
  if not parent_path:
    parent_path = []
  path = parent_path + [kind, id_or_name]
  return MakePathKey(*path, **dict(namespace=namespace))


def MakePathKey(*path, **kwargs):
  return db.Key.from_path(*path, **dict(namespace=kwargs.get('namespace')))


def MakeRange(key1, key2, direction=key_range_module.KeyRange.ASC,
              include_start=True, include_end=True, namespace=None, _app=None):
  return key_range_module.KeyRange(key_start=key1,
                                   key_end=key2,
                                   direction=direction,
                                   include_start=include_start,
                                   include_end=include_end,
                                   namespace=namespace,
                                   _app=_app)


def setUpModule():
  os.environ['APPLICATION_ID'] = APP_ID


class KeyRangeRepresentationHelper(object):

  if six.PY3:

    def VarRepr(self, var):
      return repr(var)
  else:

    def VarRepr(self, var):
      if isinstance(var, six.integer_types):
        return '{}L'.format(var)
      if isinstance(var, six.string_types):
        return "u'{}'".format(var.decode('utf-8'))
      return repr(var)

  def KeyFromPathRepr(self, *args, **kwargs):
    out = ['datastore_types.Key.from_path(']
    for v in args:
      out += [self.VarRepr(v), ', ']
    for k, v in kwargs.items():
      out += [str(k), '=', self.VarRepr(v), ', ']
    if args or kwargs:
      out.pop(-1)
    out.append(')')
    return ''.join(out)


class KeyRangeTest(absltest.TestCase):

  dbmod = db
  repr_helper = KeyRangeRepresentationHelper()

  def new_db_key(self):
    return db.Key()

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_all_stubs()
    ndb.get_context().clear_cache()
    self.batch_size = 2

  def PerformSplitRange(self, key_range, split_key=None, expected_ranges=None):
    if split_key:
      assert not expected_ranges
      expected_ranges = [
          MakeRange(key_range.key_start, split_key,
                    direction=key_range_module.KeyRange.DESC),
          MakeRange(split_key, key_range.key_end, include_start=False)]

    ranges = key_range.split_range(batch_size=self.batch_size)

    self.assertEqual(expected_ranges, ranges)

  def testSplitNoneOnLeft(self):
    """A key range with None on the left should be unsplit and ASC."""
    key1 = None
    key2 = MakeKey('named-key')
    key_range = MakeRange(key1, key2, direction=key_range_module.KeyRange.DESC)
    expected_range = MakeRange(key1,
                               key2,
                               direction=key_range_module.KeyRange.ASC)
    self.PerformSplitRange(key_range, expected_ranges=[expected_range])

  def testSplitNoneOnRight(self):
    """A key range with None on the right should be unsplit and DESC."""
    key1 = MakeKey('named-key')
    key2 = None
    key_range = MakeRange(key1, key2, direction=key_range_module.KeyRange.ASC)
    expected_range = MakeRange(key1,
                               key2,
                               direction=key_range_module.KeyRange.DESC)
    self.PerformSplitRange(key_range, expected_ranges=[expected_range])

  def testSplitNoneOnLeftOtherApp(self):
    """A key range with None on the left should be unsplit and ASC."""
    key1 = None
    key2 = MakeKey('named-key')
    key_range = MakeRange(key1, key2, direction=key_range_module.KeyRange.DESC,
                          _app='other')
    expected_range = MakeRange(key1,
                               key2,
                               direction=key_range_module.KeyRange.ASC,
                               _app='other')
    self.PerformSplitRange(key_range, expected_ranges=[expected_range])

  def testSplitNoneOnRightOtherApp(self):
    """A key range with None on the left should be unsplit and DESC."""
    key1 = MakeKey('named-key')
    key2 = None
    key_range = MakeRange(key1, key2, direction=key_range_module.KeyRange.ASC,
                          _app='other')
    expected_range = MakeRange(key1,
                               key2,
                               direction=key_range_module.KeyRange.DESC,
                               _app='other')
    self.PerformSplitRange(key_range, expected_ranges=[expected_range])

  def testSplitNoneOfLeftWithNamespace(self):
    """A key range with None on the left and a KeyRange with a namespace."""
    key1 = None
    key2 = MakeKey('named-key', namespace='google')
    key_range = MakeRange(key1, key2, direction=key_range_module.KeyRange.DESC,
                          namespace='google')
    expected_range = MakeRange(key1,
                               key2,
                               direction=key_range_module.KeyRange.ASC,
                               namespace='google')
    self.PerformSplitRange(key_range, expected_ranges=[expected_range])

  def testSplitNoneOnRightWithNamespace(self):
    """A key range with None on the right and a KeyRange with a namespace."""
    key1 = MakeKey('named-key', namespace='google')
    key2 = None
    key_range = MakeRange(key1, key2, direction=key_range_module.KeyRange.ASC,
                          namespace='google')
    expected_range = MakeRange(key1,
                               key2,
                               direction=key_range_module.KeyRange.DESC,
                               namespace='google')
    self.PerformSplitRange(key_range, expected_ranges=[expected_range])

  def testSplitRanges(self):
    key_splits = (
        (MakeKey(1), MakeKey(9999), MakeKey(5000)),
        (MakeKey(1, parent_path=['Kind1', 'name1', 'Kind2', 1]),
         MakeKey(9999, parent_path=['Kind1', 'name1', 'Kind2', 1]),
         MakeKey(5000, parent_path=['Kind1', 'name1', 'Kind2', 1])),
        (MakeKey(1, parent_path=['Kind1', 'name1', 'Kind2', 1]),
         MakeKey(2, parent_path=['Kind1', 'name1', 'Kind2', 1]),
         MakeKey(1, parent_path=['Kind1', 'name1', 'Kind2', 1])),
        (MakeKey('named-key1'), MakeKey('named-key7'), MakeKey('named-key4')),
        (MakeKey(1000), MakeKey('named-key'), MakeKey(six.unichr(0))),
        (MakeKey(1, kind='Kind1'), MakeKey(1, kind='Kind3'),
         MakeKey(six.unichr(0), kind='Kind2')),
        (MakePathKey('kind1', 'stuff1', 'kind2', 'things'),
         MakePathKey('kind1', 'stuff3'),
         MakePathKey('kind1', 'stuff2')))
    for key1, key2, split_key in key_splits:
      key_range = MakeRange(key1, key2)
      self.PerformSplitRange(key_range, split_key=split_key)

  def testSplitIdAndName(self):
    key1 = MakeKey(4345)
    key2 = MakeKey('named-key')
    zero_key = MakeKey(six.unichr(0))

    key_range = MakeRange(key1, key2, direction=key_range_module.KeyRange.ASC)
    expected_ranges = [
        MakeRange(key1, zero_key, direction=key_range_module.KeyRange.DESC),
        MakeRange(zero_key, key2, direction=key_range_module.KeyRange.ASC,
                  include_start=False)]
    self.PerformSplitRange(key_range, expected_ranges=expected_ranges)

    key_range = MakeRange(key1, zero_key,
                          direction=key_range_module.KeyRange.ASC)
    expected_ranges = [
        MakeRange(
            key1,
            MakeKey(4611686018427390076),
            direction=key_range_module.KeyRange.DESC),
        MakeRange(
            MakeKey(4611686018427390076),
            zero_key,
            direction=key_range_module.KeyRange.ASC,
            include_start=False)
    ]
    self.PerformSplitRange(key_range, expected_ranges=expected_ranges)

    key_range = MakeRange(zero_key, key2,
                          direction=key_range_module.KeyRange.ASC)
    expected_ranges = [
        MakeRange(zero_key, MakeKey(u'7'),
                  direction=key_range_module.KeyRange.DESC),
        MakeRange(MakeKey(u'7'), key2, direction=key_range_module.KeyRange.ASC,
                  include_start=False)]
    self.PerformSplitRange(key_range, expected_ranges=expected_ranges)

  def testStr(self):
    kr = MakeRange(db.Key.from_path('Blah', 1), None)





    expected_key_str = self.repr_helper.KeyFromPathRepr(
        'Blah', 1, _app='test_app')
    self.assertEqual(
        str(kr), 'ASC[{} to None]'.format(expected_key_str))
    kr = MakeRange(db.Key.from_path('Blah', 1), None,
                   include_start=False, include_end=False)
    self.assertEqual(
        str(kr), 'ASC({} to None)'.format(expected_key_str))

  def testRepr(self):
    kr = MakeRange(db.Key.from_path('Blah', 1), None)
    expected_key_str = self.repr_helper.KeyFromPathRepr(
        'Blah', 1, _app='test_app')
    self.assertEqual(
        repr(kr),
        "key_range.KeyRange(key_start={},key_end=None,direction='ASC',"
        "include_start=True,"
        "include_end=True, namespace='')".format(expected_key_str))

  def testHash(self):
    kr = MakeRange(db.Key.from_path('Blah', 1), None)
    self.assertRaises(TypeError, hash, kr)

  def testAdvance(self):
    kr = MakeRange(db.Key.from_path('Blah', 1), None)
    kr.advance(db.Key.from_path('Blah', 2))
    self.assertEqual(
        kr, MakeRange(db.Key.from_path('Blah', 2), None, include_start=False))

  def testFilterQuery(self, key_start=None, key_end=None):
    mocker = mox.Mox()
    query = mocker.CreateMock(self.dbmod.Query)
    key_range = MakeRange(key_start,
                          key_end,
                          include_start=False,
                          include_end=False,
                          direction=key_range_module.KeyRange.ASC)
    if self.dbmod is ndb:
      if key_start:
        query.filter(ndb.FilterNode('__key__', '>', key_start)).AndReturn(query)
      if key_end:
        query.filter(ndb.FilterNode('__key__', '<', key_end)).AndReturn(query)
    else:
      if key_start and key_end:
        query.filter('__key__ >', key_start)
        query.filter('__key__ <', key_end)
      elif key_start:
        query.filter('__key__ >', key_start)
      elif key_end:
        query.filter('__key__ <', key_end)
    mocker.ReplayAll()
    key_range.filter_query(query)
    mocker.VerifyAll()

  def testFilterQueryEmpty(self):
    key = self.new_db_key()
    self.testFilterQuery(key_start=key, key_end=key)

  def testFilterQueryStart(self):
    self.testFilterQuery(key_start=self.new_db_key())

  def testFilterQueryEnd(self):
    self.testFilterQuery(key_end=self.new_db_key())

  def testFilterQueryStartEnd(self):
    self.testFilterQuery(key_start=self.new_db_key(), key_end=self.new_db_key())

  def testFilterDatastoreQuery(self, key_start=None, key_end=None, _app=None):
    mocker = mox.Mox()
    query = mocker.CreateMock(datastore.Query)
    key_range = MakeRange(key_start,
                          key_end,
                          include_start=False,
                          include_end=False,
                          direction=key_range_module.KeyRange.ASC,
                          _app=_app)
    if key_start:
      query.update({'__key__ >': key_start})
    if key_end:
      query.update({'__key__ <': key_end})
    mocker.ReplayAll()
    key_range.filter_datastore_query(query)
    mocker.VerifyAll()

  def testFilterDatastoreQueryEmpty(self):
    key = object()
    self.testFilterDatastoreQuery(key_start=key, key_end=key)

  def testFilterDatastoreQueryStart(self):
    self.testFilterDatastoreQuery(key_start=object())

  def testFilterDatastoreQueryEnd(self):
    self.testFilterDatastoreQuery(key_end=object())

  def testFilterDatastoreQueryStartEnd(self):
    self.testFilterDatastoreQuery(key_start=object(), key_end=object())

  def testFilterDatastoreQueryEmptyOtherApp(self):
    key = object()
    self.testFilterDatastoreQuery(key_start=key, key_end=key, _app='other')

  def testFilterDatastoreQueryStartOtherApp(self):
    self.testFilterDatastoreQuery(key_start=object(), _app='other')

  def testFilterDatastoreQueryEndOtherApp(self):
    self.testFilterDatastoreQuery(key_end=object(), _app='other')

  def testFilterDatastoreQueryStartEndOtherApp(self):
    self.testFilterDatastoreQuery(key_start=object(), key_end=object(),
                                  _app='other')

  def RandomString(self, max_len):
    strlen = random.randrange(0, max_len)
    if not strlen:
      return u''
    valid = False
    high_surrogate_range = [0xD800, 0xDBFF]
    low_surrogate_range = [0xDC00, 0xDFFF]

    def GenerateValidUnicodeSequence(target_len):
      """Generate unicode string with valid pairs of surrogates."""
      current_len = 0
      while current_len < target_len:
        char_code = random.randrange(0, 0xFFFF)
        if high_surrogate_range[0] <= char_code <= high_surrogate_range[1]:
          if target_len - current_len < 1:

            continue
          yield six.unichr(char_code)
          yield six.unichr(random.randrange(*low_surrogate_range))
          current_len += 2
        elif low_surrogate_range[0] <= char_code <= low_surrogate_range[1]:
          if target_len - current_len < 1:

            continue
          yield six.unichr(random.randrange(*high_surrogate_range))
          yield six.unichr(char_code)
          current_len += 2
        else:
          yield six.unichr(char_code)
          current_len += 1

    while not valid:
      try:
        random_str = ''.join(GenerateValidUnicodeSequence(strlen))
        datastore_types.ValidateString(random_str, '')
        if random_str and random_str[0] in string.digits:
          continue
        valid = True
      except datastore_errors.BadValueError:

        pass
    return random_str

  def UnicodeLeq(self, str1, str2):
    for x, y in zip(str1, str2):
      if ord(x) < ord(y):
        return True
      if ord(x) > ord(y):
        return False
    return len(str2) >= len(str1)

  def assertUnicodeLeq(self, str1, str2):
    self.assertTrue(self.UnicodeLeq(str1, str2),
                    '%s </= %s' % (repr(str1), repr(str2)))

  def testBisectStringRange(self):
    corner_cases = [
        (u'a\u8000', u'a\ubfff', 'b'),
        ('', '', ''),
        ('', '0?', 'a string'),
        ('a', 'a?', 'b'),
        (u'a\u7fff', u'a\ubfff', 'b'),
        (u'a\u7ffe', u'a\ubffe', 'b'),
        (u'a\uffff', u'a\uffff', 'b'),
        ('another string', 'j', 'some string'),
        ('stringswithcommonprefix1', 'stringswithcommonprefix1?',
         'stringswithcommonprefix2'),
        ('a', 'a', 'a'),
        ('a', 'a\0', 'a\0'),
        ]
    max_len = 5
    num_tests = 10000
    self.key_range = MakeRange(None, None)
    for key_str1, expected_mid, key_str2 in corner_cases:
      mid = self.BisectStringsTest(key_str1, key_str2)
      self.assertEqual(expected_mid, mid)
    for unused_idx in range(num_tests):
      key_str1 = self.RandomString(max_len)
      key_str2 = self.RandomString(max_len)
      self.BisectStringsTest(key_str1, key_str2)

  def BisectStringsTest(self, key_str1, key_str2):
    if self.UnicodeLeq(key_str2, key_str1):
      tmp = key_str1
      key_str1 = key_str2
      key_str2 = tmp
    mid = key_range_module.KeyRange.bisect_string_range(key_str1, key_str2)
    self.assertUnicodeLeq(key_str1, mid)
    self.assertUnicodeLeq(mid, key_str2)
    return mid

  def testSplitIdOrName(self):
    """Test splitting the range [0, 10] with _split_id_or_name."""

    self.assertEqual(
        5, key_range_module.KeyRange._split_id_or_name(0, 10, 10, False))


    self.assertEqual(
        0, key_range_module.KeyRange._split_id_or_name(0, 10, 10, True))


    self.assertEqual(
        5, key_range_module.KeyRange._split_id_or_name(0, 10, 9, True))

  def testDefaultAsc(self):
    self.assertEqual(key_range_module.KeyRange.ASC,
                     key_range_module.KeyRange().direction)

  def testCorrectEdgesSplit(self):
    """Making sure that no key belongs to more than range at once."""

    key_range = MakeRange(MakeKey(1), MakeKey(2))
    split_ranges = key_range.split_range(1)
    self.assertSequenceEqual(
        [
            MakeRange(MakeKey(1), MakeKey(1), 'DESC', True, True),
            MakeRange(MakeKey(1), MakeKey(2), 'ASC', False, True),
        ],
        split_ranges)


    key_range = MakeRange(MakeKey(1), MakeKey(1))
    split_ranges = key_range.split_range(1)
    self.assertSequenceEqual(
        [
            MakeRange(MakeKey(1), MakeKey(1), 'DESC', True, True),
            MakeRange(MakeKey(1), MakeKey(1), 'ASC', False, False),
        ],
        split_ranges)


    key_range = MakeRange(MakeKey(1), MakeKey(1), 'ASC', False, False)
    split_ranges = key_range.split_range(1)
    self.assertSequenceEqual(
        [
            MakeRange(MakeKey(1), MakeKey(1), 'DESC', False, False),
            MakeRange(MakeKey(1), MakeKey(1), 'ASC', False, False),
        ],
        split_ranges)


    key_range = MakeRange(MakeKey(1), MakeKey(2), 'ASC', False, True)
    split_ranges = key_range.split_range(1)
    self.assertSequenceEqual(
        [
            MakeRange(MakeKey(1), MakeKey(1), 'DESC', False, False),
            MakeRange(MakeKey(1), MakeKey(2), 'ASC', False, True),
        ],
        split_ranges)

  def testGuessEndKeyIntegerIds(self):
    """Tests the guess_end_key static function with integer IDs."""
    datastore.Put(datastore.Entity(KIND, id=8192))
    datastore.Put(datastore.Entity(KIND, id=12288))
    datastore.Put(datastore.Entity(KIND, id=13312))
    key_end = key_range_module.KeyRange.guess_end_key(
        KIND,
        datastore.Key.from_path(KIND, 0),
        probe_count=20,
        split_rate=5)
    self.assertEqual(datastore.Key.from_path(KIND, 13535), key_end)

  def testGuessEndKeyIntegerIdsOtherApp(self):
    """Tests the guess_end_key static function with integer IDs."""
    apiproxy_stub_map.apiproxy.GetStub("datastore_v3").SetTrusted(True)
    datastore.Put(datastore.Entity(KIND, id=8192, _app='other'))
    datastore.Put(datastore.Entity(KIND, id=12288, _app='other'))
    datastore.Put(datastore.Entity(KIND, id=13312, _app='other'))
    key_end = key_range_module.KeyRange.guess_end_key(
        KIND,
        datastore.Key.from_path(KIND, 0, _app='other'),
        probe_count=20,
        split_rate=5)
    self.assertEqual(
        datastore.Key.from_path(KIND, 13535, _app='other'), key_end)

  def testGuessEndKeyIntegerIdsWithNamespace(self):
    """Tests guess_end_key with a key containing an namespace."""
    datastore.Put(datastore.Entity(KIND, id=8192, namespace='google'))
    datastore.Put(datastore.Entity(KIND, id=12288, namespace='google'))
    datastore.Put(datastore.Entity(KIND, id=13312, namespace='google'))
    datastore.Put(datastore.Entity(KIND, id=18322))
    key_end = key_range_module.KeyRange.guess_end_key(
        KIND,
        datastore.Key.from_path(KIND, 0, namespace='google'),
        probe_count=20,
        split_rate=5)
    self.assertEqual(
        datastore.Key.from_path(KIND, 13535, namespace='google'), key_end)

  def testGuessEndKeySmallRange(self):
    """Tests the guess_end_key function when the key range is small."""
    datastore.Put(datastore.Entity(KIND, id=int(2**30)))
    datastore.Put(datastore.Entity(KIND, id=int(2**30 - 1)))
    datastore.Put(datastore.Entity(KIND, id=int(2**30 - 2)))
    key_end = key_range_module.KeyRange.guess_end_key(
        KIND,
        datastore.Key.from_path(KIND, 0),
        probe_count=20,
        split_rate=5)
    self.assertEqual(datastore.Key.from_path(KIND, 1074659326), key_end)

  def testGuessEndKeyStrings(self):
    """Tests the guess_end_key function with string keys."""
    datastore.Put(datastore.Entity(KIND, name='peanut'))
    datastore.Put(datastore.Entity(KIND, name=u'\x7fblah'))
    datastore.Put(datastore.Entity(KIND, name=u'\x80meep'))
    key_end = key_range_module.KeyRange.guess_end_key(
        KIND,
        datastore.Key.from_path(KIND, u'\x00'),
        probe_count=10,
        split_rate=5)
    self.assertEqual(datastore.Key.from_path(KIND, u'\x80n'), key_end)

  def testGuessEndKeyMultiLevelPath(self):
    """Tests guessing the end key when the path has multiple components."""
    parent1 = datastore.Entity('chocolate', name='begin')
    parent2 = datastore.Entity('chocolate', name='stuff')
    datastore.Put(datastore.Entity(KIND, name='peanut', parent=parent1))
    datastore.Put(datastore.Entity(KIND, name=u'\x7fblah', parent=parent2))
    datastore.Put(datastore.Entity(KIND, id=1234, parent=parent2))
    datastore.Put(datastore.Entity(KIND, name=u'\x80meep', parent=parent1))

    key_end = key_range_module.KeyRange.guess_end_key(
        KIND,
        datastore.Key.from_path('chocolate', 'begin', KIND, u'\x00'),
        probe_count=10,
        split_rate=5)
    self.assertEqual(datastore.Key.from_path('chocolate', u'svz'), key_end)

  def testGuessEndKeyIntegerVeryLargeId(self):
    """Tests the guess_end_key static function with integer IDs."""
    entity_id = 2**60
    datastore.Put(datastore.Entity(KIND, id=entity_id))
    key_end = key_range_module.KeyRange.guess_end_key(
        KIND,
        datastore.Key.from_path(KIND, 0),
        probe_count=50,
        split_rate=5)
    guess = 1152921504606861311
    self.assertEqual(datastore.Key.from_path(KIND, guess), key_end)
    self.assertEqual(14335, guess - entity_id)

  def testGuessEndKeyMixedIdsAndNames(self):
    """Tests the guess_end_key function with string keys."""
    datastore.Put(datastore.Entity(KIND, id=20000))
    datastore.Put(datastore.Entity(KIND, id=80000))
    datastore.Put(datastore.Entity(KIND, name=u'foo'))
    datastore.Put(datastore.Entity(KIND, name=u'bar'))
    key_end = key_range_module.KeyRange.guess_end_key(
        KIND,
        datastore.Key.from_path(KIND, 0),
        probe_count=10,
        split_rate=5)
    self.assertEqual(datastore.Key.from_path(KIND, u'foo\x0f?'), key_end)

  def testComputeSplitPoints_Empty(self):
    """Tests compute_split_points when there are no entities."""
    result = key_range_module.KeyRange.compute_split_points(KIND, 10)
    self.assertEqual([MakeRange(None, None, 'ASC', True, True)], result)

  def testComputeSplitPoints_Many(self):
    """Tests compute_split_points when there are many split points."""
    expected_keys = []
    for i in range(11):
      expected_keys.append(MakePathKey(KIND, i+1))
      datastore.Put(datastore.Entity(KIND, id=i+1))




    result = key_range_module.KeyRange.compute_split_points(KIND, 3)
    self.assertLen(result, 4)

    found_keys = []
    for key_range in result:
      found_keys.extend(
          key_range.make_ascending_datastore_query(KIND, keys_only=True).Run())



    self.assertEqual(sorted(expected_keys), sorted(found_keys))

  def testBothKeysAreNotNoneToJson(self):
    """Test serialization when both start and end keys are not None."""
    key_range = MakeRange(MakeKey(324), MakeKey(993), "DESC", False, True)
    self.assertEqual(
        '{'
        '"direction": "DESC", '
        '"include_end": true, '
        '"include_start": false, '
        '"key_end": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGOEHDA", '
        '"key_start": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGMQCDA", '
        '"namespace": ""'
        '}', key_range.to_json())

  def testNoneKeyToJson(self):
    """Test serialization when some keys are None."""
    key_range = MakeRange(MakeKey(324), None, "ASC", True, False)
    self.assertEqual(
        '{'
        '"direction": "ASC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": null, '
        '"key_start": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGMQCDA", '
        '"namespace": ""'
        '}', key_range.to_json())

  def testBothKeysAreNotNoneToJsonOtherApp(self):
    """Test serialization when both start and end keys are not None."""
    key_range = MakeRange(MakeKey(324), MakeKey(993), "DESC", False, True,
                          _app='other')
    self.assertEqual(
        '{'
        '"_app": "other", '
        '"direction": "DESC", '
        '"include_end": true, '
        '"include_start": false, '
        '"key_end": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGOEHDA", '
        '"key_start": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGMQCDA", '
        '"namespace": ""'
        '}', key_range.to_json())

  def testNoneKeyToJsonOtherApp(self):
    """Test serialization when some keys are None."""
    key_range = MakeRange(MakeKey(324), None, "ASC", True, False, _app='other')
    self.assertEqual(
        '{'
        '"_app": "other", '
        '"direction": "ASC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": null, '
        '"key_start": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGMQCDA", '
        '"namespace": ""'
        '}', key_range.to_json())

  def testBothKeysAreNotNoneFromJson(self):
    """Test deserialization when both start and end keys are not None."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "DESC", '
        '"include_end": true, '
        '"include_start": false, '
        '"key_end": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGOEHDA", '
        '"key_start": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGMQCDA", '
        '"namespace": ""'
        '}')

    self.assertEqual('DESC', key_range.direction)
    self.assertEqual(True, key_range.include_end)
    self.assertEqual(False, key_range.include_start)
    self.assertEqual(MakeKey(324), key_range.key_start)
    self.assertEqual(MakeKey(993), key_range.key_end)

  def testSomeKeysAreNoneFromJson(self):
    """Test deserialization when some keys are None."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "ASC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGOEHDA", '
        '"key_start": null'
        '}')

    self.assertEqual('ASC', key_range.direction)
    self.assertEqual(False, key_range.include_end)
    self.assertEqual(True, key_range.include_start)
    self.assertEqual(None, key_range.key_start)
    self.assertEqual(MakeKey(993), key_range.key_end)

  def testBothKeysAreNotNoneFromJsonOtherApp(self):
    """Test deserialization when both start and end keys are not None."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "DESC", '
        '"include_end": true, '
        '"include_start": false, '
        '"key_end": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGOEHDA", '
        '"key_start": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGMQCDA", '
        '"_app": "other"'
        '}')

    self.assertEqual('DESC', key_range.direction)
    self.assertEqual(True, key_range.include_end)
    self.assertEqual(False, key_range.include_start)
    self.assertEqual(MakeKey(324), key_range.key_start)
    self.assertEqual(MakeKey(993), key_range.key_end)
    self.assertEqual('other', key_range._app)

  def testSomeKeysAreNoneFromJsonOtherApp(self):
    """Test deserialization when some keys are None."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "ASC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGOEHDA", '
        '"key_start": null, '
        '"_app": "other"'
        '}')

    self.assertEqual('ASC', key_range.direction)
    self.assertEqual(False, key_range.include_end)
    self.assertEqual(True, key_range.include_start)
    self.assertEqual(None, key_range.key_start)
    self.assertEqual(MakeKey(993), key_range.key_end)
    self.assertEqual('other', key_range._app)

  def testNamespaceNull(self):
    """Tests deserialization when namespace is explicitly specified as null."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "ASC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGOEHDA", '
        '"key_start": null, '
        '"namespace": ""'
        '}')

    self.assertEqual('ASC', key_range.direction)
    self.assertEqual(False, key_range.include_end)
    self.assertEqual(True, key_range.include_start)
    self.assertEqual(None, key_range.key_start)
    self.assertEqual(MakeKey(993), key_range.key_end)
    self.assertEqual('', key_range.namespace)

  def testNamespaceNotNone(self):
    """Tests deserialization when a non-null namespace is specified."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "ASC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": "agh0ZXN0X2FwcHIQCxIJdGVzdF9raW5kGOEHDA", '
        '"key_start": null, '
        '"namespace": "google"'
        '}')

    self.assertEqual('ASC', key_range.direction)
    self.assertEqual(False, key_range.include_end)
    self.assertEqual(True, key_range.include_start)
    self.assertEqual(None, key_range.key_start)
    self.assertEqual(MakeKey(993), key_range.key_end)
    self.assertEqual('google', key_range.namespace)

  def testMakeDirectedQuery(self):
    """Test conversion to [n]db.Query."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "DESC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": null, '
        '"key_start": null, '
        '"_app": null'
        '}')

    class Blah(self.dbmod.Model):
      pass
    if self.dbmod is ndb:
      qry = Blah.query(namespace='').order(-Blah._key)
    else:
      qry = Blah.all()
      qry.order('-__key__')

    actual = key_range.make_directed_query(Blah)

    if self.dbmod is ndb:

      q = qry._get_query(None)
      a = actual._get_query(None)
      self.assertEqual(q, a)
    else:

      q = qry._get_query()
      a = actual._get_query()
      self.assertEqual(q, a)
      self.assertEqual(q.GetOrder(), a.GetOrder())

  def testMakeAscendingQuery(self):
    """Test conversion to [n]db.Query."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "ASC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": null, '
        '"key_start": null, '
        '"_app": null'
        '}')

    class Blah(self.dbmod.Model):
      pass
    if self.dbmod is ndb:
      qry = Blah.query().order(Blah._key)
    else:
      qry = Blah.all()
      qry.order('__key__')

    actual = key_range.make_ascending_query(Blah)

    if self.dbmod is ndb:

      q = qry._get_query(None)
      a = actual._get_query(None)
      self.assertEqual(q, a)
    else:

      q = qry._get_query()
      a = actual._get_query()
      self.assertEqual(q, a)
      self.assertEqual(q.GetOrder(), a.GetOrder())

  def testMakeAscendingQueryWithFilters(self):
    """Test conversion to [n]db.Query."""
    key_range = MakeRange(MakeKey(1), MakeKey(100), 'DESC', True, True)

    class Blah(self.dbmod.Model):
      pass

    if self.dbmod is ndb:
      qry = Blah.query().order(Blah._key).filter(
          ndb.FilterNode('a', '=', 1)).filter(
          ndb.FilterNode('b', '=', 2)).filter(
          ndb.FilterNode('__key__', '>=', MakeKey(1))).filter(
          ndb.FilterNode('__key__', '<=', MakeKey(100)))
    else:
      qry = Blah.all()
      qry.order('__key__')
      qry.filter('a =', 1)
      qry.filter('b =', 2)
      qry.filter('__key__ >=', MakeKey(1))
      qry.filter('__key__ <=', MakeKey(100))

    actual = key_range.make_ascending_query(
        Blah, filters=[('a', '=', 1), ('b', '=', 2)])

    if self.dbmod is ndb:

      q = qry._get_query(None)
      a = actual._get_query(None)
      self.assertEqual(q, a)
    else:

      q = qry._get_query()
      a = actual._get_query()
      self.assertEqual(q, a)
      self.assertEqual(q.GetOrder(), a.GetOrder())

  def testMakeDirectedDatastoreQuery(self):
    """Test conversion to datastore.Query."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "ASC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": null, '
        '"key_start": null, '
        '"_app": "other"'
        '}')

    self.assertEqual(
        datastore.Query('Blah', _app='other'),
        key_range.make_directed_datastore_query("Blah"))

  def testMakeAscendingDatastoreQuery(self):
    """Test conversion to datastore.Query."""
    key_range = key_range_module.KeyRange.from_json(
        '{'
        '"direction": "ASC", '
        '"include_end": false, '
        '"include_start": true, '
        '"key_end": null, '
        '"key_start": null, '
        '"_app": "other"'
        '}')

    self.assertEqual(
        datastore.Query('Blah', _app='other'),
        key_range.make_ascending_datastore_query("Blah"))

    self.assertEqual(
        datastore.Query("Blah", {
            'a =': 1,
            'b =': 2
        }, _app="other"),
        key_range.make_ascending_datastore_query(
            "Blah", filters=[('a', '=', 1), ('b', '=', 2)]))


if ndb is not None:
  class NdbKeyRangeTest(KeyRangeTest):
    dbmod = ndb

    def new_db_key(self):
      return ndb.Key('Blah', 1)


if __name__ == '__main__':
  absltest.main()
