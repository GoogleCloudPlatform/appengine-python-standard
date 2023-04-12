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


"""Tests for google.appengine.api.search.tokens."""





from google.appengine.api.search.stub import tokens
from absl.testing import absltest


class TokenTest(absltest.TestCase):

  def testEquals(self):
    token = tokens.Token(chars='abc', position=9)
    token2 = tokens.Token(chars='abc', position=5)
    self.assertEqual(token, token2)
    token2 = tokens.Token(chars='xyz', position=9)
    self.assertNotEqual(token, token2)

  def testHash(self):
    token = tokens.Token(chars='abc', position=9)
    token2 = tokens.Token(chars='abc', position=5)
    self.assertEqual(hash(token), hash(token2))
    token2 = tokens.Token(chars='xyz', position=9)
    self.assertNotEqual(hash(token), hash(token2))

  def testRestrictField(self):
    token = tokens.Token(chars='abc', position=9)
    restrict = token.RestrictField('field')
    self.assertNotEqual(token, restrict)
    self.assertEqual('field:abc', restrict.chars)

  def testUnicodeContent(self):
    token = tokens.Token(chars=u'abc', position=1)
    self.assertEqual(u'abc', token.chars)
    token = tokens.Token(chars='abc', position=1)
    self.assertEqual('abc', token.chars)
    token = tokens.Token(chars=u'abc', field_name='f', position=1)
    self.assertEqual(u'f:abc', token.chars)
    token = tokens.Token(chars='abc', field_name='f', position=1)
    self.assertEqual('f:abc', token.chars)


if __name__ == '__main__':
  absltest.main()
