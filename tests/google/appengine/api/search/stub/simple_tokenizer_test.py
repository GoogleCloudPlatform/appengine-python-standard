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


"""Tests for google.appengine.api.search.simple_tokenizer."""

from six.moves import range
from six.moves import zip

from google.appengine.api.search.stub import simple_tokenizer
from google.appengine.api.search.stub import tokens
from google.appengine.datastore import document_pb2
from absl.testing import absltest




class SimpleTokenizerTest(absltest.TestCase):

  def TokenSequence(self, words):
    return [
        tokens.Token(chars=word, position=i)
        for word, i in zip(words, range(len(words)))
    ]

  def testTokenizeValueSimple(self):
    field_value = document_pb2.FieldValue()
    field_value.string_value = 'A simple story about A'
    self.assertEqual(
        self.TokenSequence('a simple story about a'.split()),
        simple_tokenizer.SimpleTokenizer().TokenizeValue(field_value))

  def testTokenizeTextSimple(self):
    self.assertEqual(
        self.TokenSequence('a simple story about a'.split()),
        simple_tokenizer.SimpleTokenizer().TokenizeText(
            'A simple story about A'))

  def testTokenizePrefixValue(self):
    field_value = document_pb2.FieldValue()
    field_value.string_value = 'A simple story about A'
    field_value.type = document_pb2.FieldValue.UNTOKENIZED_PREFIX
    self.assertEqual(
        self.TokenSequence(['a simple story about a']),
        simple_tokenizer.SimpleTokenizer().TokenizeValue(field_value))
    field_value.type = document_pb2.FieldValue.TOKENIZED_PREFIX
    self.assertEqual(
        self.TokenSequence('a simple story about a'.split()),
        simple_tokenizer.SimpleTokenizer().TokenizeValue(field_value))

  def testTokenizeTextColon(self):
    self.assertEqual(
        self.TokenSequence('a b c'.split()),
        simple_tokenizer.SimpleTokenizer().TokenizeText('a:b:c'))

  def testTokenizeTextPhraseQuery(self):
    self.assertEqual(
        self.TokenSequence('a:b c'.split()),
        simple_tokenizer.SimpleTokenizer(split_restricts=False).TokenizeText(
            'a:b c'))

  def testTokenizeCjk(self):
    test_str = u'\u308f\u305f\u3057 \u306f \u3046\u3043\u308b \u3067\u3059'
    split_test_str = [u'\u308f\u305f\u3057', u'\u306f', u'\u3046\u3043\u308b',
                      u'\u3067\u3059']
    tokenizer = simple_tokenizer.SimpleTokenizer()
    normalized = [
        tokenizer.Normalize(word, document_pb2.FieldValue.TEXT)
        for word in split_test_str
    ]
    self.assertEqual(
        self.TokenSequence(normalized),
        simple_tokenizer.SimpleTokenizer().TokenizeText(test_str))

  def testNewMembers(self):
    """Test to ensure old versions of SimpleTokenizer will still work.

    This test removes members added to SimpleTokenizer since we started
    persisting search indexes to ensure that, even without these members, the
    tokenizer will still work as intended.
    """
    tokenizer = simple_tokenizer.SimpleTokenizer()
    del tokenizer._preserve_case

    field_value = document_pb2.FieldValue()
    field_value.string_value = 'A simple story about A'
    self.assertEqual(
        self.TokenSequence('a simple story about a'.split()),
        tokenizer.TokenizeValue(field_value))

  def testTokenizeWithPunctuation(self):
    self.assertEqual(
        self.TokenSequence('this is a story all about how'.split()),
        simple_tokenizer.SimpleTokenizer().TokenizeText(
            'This is a story, all about how.'))

  def testTokenizeWithMultipleSpaces(self):
    self.assertEqual(
        self.TokenSequence('my life got twist-turned upside-down'.split()),
        simple_tokenizer.SimpleTokenizer().TokenizeText(
            'my  life  got    twist-turned     upside-down.'))

  def testTokenizerRemovesSingleQuotes(self):

    self.assertEqual(
        self.TokenSequence('this is a story all about how'.split()),
        simple_tokenizer.SimpleTokenizer().TokenizeText(
            'This is a \'\'story\', all about how.'))

    self.assertEqual(
        self.TokenSequence('this is a story\'s arc'.split()),
        simple_tokenizer.SimpleTokenizer().TokenizeText(
            'This is a story\'s arc'))

  def testTokenizeAtomWithMultiline(self):
    self.assertEqual(
        self.TokenSequence(['This is a story, all\nabout how.']),
        simple_tokenizer.SimpleTokenizer().TokenizeText(
            'This is a story, all\nabout how.',
            input_field_type=document_pb2.FieldValue.ATOM))


if __name__ == '__main__':
  absltest.main()
