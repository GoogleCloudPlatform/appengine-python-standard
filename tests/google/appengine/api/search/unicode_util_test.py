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
"""Tests for google.appengine.api.search.unicode_util."""


from google.appengine.api.search import unicode_util
from absl.testing import absltest


class UnicodeUtilTest(absltest.TestCase):

  def testLimitUnicode(self):
    self.assertEqual('abc', unicode_util.LimitUnicode('abc'))
    self.assertEqual(u'a\u7fffc', unicode_util.LimitUnicode(u'a\u7fffc'))


    self.assertEqual(u'a\ud801\udc37c',
                     unicode_util.LimitUnicode(u'a\U00010437c'))
    self.assertEqual(u'a\ud801\udc37cd\ud801\udc37f',
                     unicode_util.LimitUnicode(u'a\U00010437cd\U00010437f'))


if __name__ == '__main__':
  absltest.main()

