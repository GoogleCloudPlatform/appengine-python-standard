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

"""Tests for google.appengine.api.search.search_util."""



import datetime

from google.appengine.api.search import search_util
from absl.testing import absltest


class SimpleSearchStubUtilTest(absltest.TestCase):

  def testEpochTime(self):
    ms_offset = 8675309
    test_date = (
        search_util.BASE_DATE + datetime.timedelta(milliseconds=ms_offset))
    self.assertEqual(ms_offset, search_util.EpochTime(test_date))


    test_date = search_util.BASE_DATE + datetime.timedelta(microseconds=140)
    self.assertEqual(0, search_util.EpochTime(test_date))

    day_offset = 18
    ms_offset = int(1.5552e9)
    test_date = search_util.BASE_DATE + datetime.timedelta(days=day_offset)
    self.assertEqual(ms_offset, search_util.EpochTime(test_date))


    test_date = datetime.date(year=2012, month=5, day=18)
    self.assertEqual(1337299200000, search_util.EpochTime(test_date))

  def testSerializeDate(self):
    test_date = search_util.BASE_DATE + datetime.timedelta(milliseconds=8675309)
    self.assertEqual('8675309', search_util.SerializeDate(test_date))


    test_date = search_util.BASE_DATE + datetime.timedelta(microseconds=140)
    self.assertEqual('0', search_util.SerializeDate(test_date))

    test_date = search_util.BASE_DATE + datetime.timedelta(days=18)
    self.assertEqual('1555200000', search_util.SerializeDate(test_date))


    test_date = datetime.date(year=2012, month=5, day=18)
    self.assertEqual('1337299200000', search_util.SerializeDate(test_date))

  def testDeserializeDate(self):
    test_date = datetime.datetime(
        year=1934, month=7, day=4, hour=5, minute=7, microsecond=213000)
    self.assertEqual(
        test_date,
        search_util.DeserializeDate(search_util.SerializeDate(test_date)))

    test_date = datetime.date(year=2034, month=2, day=11)
    self.assertEqual(
        test_date,
        search_util.DeserializeDate(
            search_util.SerializeDate(test_date)).date())

  def testRemoveAccentsNfkd(self):

    self.assertEqual(u'Ruben', search_util.RemoveAccentsNfkd(u'Rub\xe9n'))

    self.assertEqual(u'Ruben', search_util.RemoveAccentsNfkd(u'Rube\u0301n'))

    self.assertEqual(u'Ruben', search_util.RemoveAccentsNfkd(b'Rub\xc3\xa9n'))

    self.assertEqual(u'difficult',
                     search_util.RemoveAccentsNfkd(u'di\ufb00icult'))


if __name__ == '__main__':
  absltest.main()

