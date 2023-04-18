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
"""Tests for google.appengine.api.search.stub.document_matcher.

These are basic sanity checks for document_matcher. More thorough tests are
included in simple_search_stub_test.
"""

from google.appengine.api.search import query_parser
from google.appengine.api.search import simple_search_stub
from google.appengine.api.search.stub import document_matcher
from google.appengine.api.search.stub import simple_tokenizer
from google.appengine.datastore import document_pb2
from absl.testing import absltest


class DocumentMatcherTest(absltest.TestCase):

  def testFieldMatch(self):
    index, docs = self._GetIndexWithSampleDocs()
    self.assertQueryReturns('field:test', index, docs, docs)
    self.assertQueryReturns('field:hello', index, docs, docs[:1])
    self.assertQueryReturns('field:adsf', index, docs, [])
    self.assertQueryReturns('nonexistent:test', index, docs, [])
    self.assertQueryReturns('nonexistent:adsf', index, docs, [])

  def testBooleanMatch(self):
    index, docs = self._GetIndexWithSampleDocs()
    self.assertQueryReturns('field:(hello OR okay)', index, docs, docs)
    self.assertQueryReturns('field:(hello AND okay)', index, docs, [])
    self.assertQueryReturns('field:test AND field:hello', index, docs, docs[:1])
    self.assertQueryReturns('field:test OR field:hello', index, docs, docs)

  def testGlobalMatch(self):
    index, docs = self._GetIndexWithSampleDocs()
    self.assertQueryReturns('test', index, docs, docs)
    self.assertQueryReturns('hello', index, docs, docs[:1])
    self.assertQueryReturns('adsf', index, docs, [])

  def testNumberMatch(self):
    index, docs = self._GetIndexWithSampleDocs()
    self.assertQueryReturns('num = 7', index, docs, docs[1:])
    self.assertRaises(document_matcher.ExpressionTreeException,
                      self._DoQuery, 'num != 7', index, docs)
    self.assertQueryReturns('num <= 7', index, docs, docs[1:])
    self.assertQueryReturns('num < 7', index, docs, [])
    self.assertQueryReturns('num >= 7', index, docs, docs[1:])
    self.assertQueryReturns('num > 7', index, docs, [])

  def testPhraseMatch(self):
    index, docs = self._GetIndexWithSampleDocs()
    self.assertQueryReturns('"hello i am"', index, docs, docs[:1])
    self.assertQueryReturns('"hello am i"', index, docs, [])
    self.assertQueryReturns('"test"', index, docs, docs)
    self.assertQueryReturns('"hello i am" test', index, docs, docs[:1])

  def testAtomMatch(self):
    index, docs = self._GetIndexWithSampleDocs()
    self.assertQueryReturns('exact', index, docs, [])
    self.assertQueryReturns('atom:exact', index, docs, [])
    self.assertQueryReturns('atom:"exact match"', index, docs, docs[:1])

  def testGeoMatch(self):
    index, docs = self._GetIndexWithSampleDocs()

    self.assertQueryReturns('distance(geo, geopoint(-33.857, 151.215)) < 50',
                            index, docs, docs[:1])

    self.assertQueryReturns('distance(geopoint(-33.857, 151.215), geo) < 50',
                            index, docs, docs[:1])


    self.assertQueryReturns('distance(geopoint(-33.857, 151.215), geo) <= 50',
                            index, docs, docs[:1])


    self.assertQueryReturns('distance(geopoint(-33.857, 151.215), geo) > 50',
                            index, docs, docs[1:])


    self.assertQueryReturns('distance(geopoint(-33.857, 151.215), geo) >= 50',
                            index, docs, docs[1:])

  def assertQueryReturns(self, query, index, docs, expected_docs):
    result = self._DoQuery(query, index, docs)
    self.assertEqual(expected_docs, result)

  def _DoQuery(self, query, index, docs):
    tree = query_parser.ParseAndSimplify(query)
    matcher = document_matcher.DocumentMatcher(tree, index)
    return list(matcher.FilterDocuments(docs))

  def _GetIndex(self):
    return simple_search_stub.RamInvertedIndex(
        simple_tokenizer.SimpleTokenizer())

  def _GetIndexWithSampleDocs(self):
    doc1 = document_pb2.Document()
    doc1.id = 'doc1'
    field = doc1.field.add()
    field.name = 'field'
    value = field.value
    value.string_value = 'hello i am a test'
    field = doc1.field.add()
    field.name = 'atom'
    value = field.value
    value.string_value = 'exact match'
    value.type = document_pb2.FieldValue.ATOM
    field = doc1.field.add()
    field.name = 'geo'
    value = field.value
    value.geo.lat = -33.857
    value.geo.lng = 151.215
    value.type = document_pb2.FieldValue.GEO

    doc2 = document_pb2.Document()
    doc2.id = 'doc2'
    field = doc2.field.add()
    field.name = 'field'
    value = field.value
    value.string_value = 'different test okay'
    field = doc2.field.add()
    field.name = 'num'
    value = field.value
    value.string_value = '7'
    value.type = document_pb2.FieldValue.NUMBER
    field = doc2.field.add()
    field.name = 'geo'
    value = field.value
    value.geo.lat = -23.7
    value.geo.lng = 133.87
    value.type = document_pb2.FieldValue.GEO

    index = self._GetIndex()
    index.AddDocument('doc1', doc1)
    index.AddDocument('doc2', doc2)
    return index, [doc1, doc2]

if __name__ == '__main__':
  absltest.main()
