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
"""Tests for google.appengine.api.search.expression_evaluator."""

import datetime

from google.appengine.api.search import geo_util
from google.appengine.api.search import search
from google.appengine.api.search import search_service_pb2
from google.appengine.api.search import search_util
from google.appengine.api.search import simple_search_stub
from google.appengine.api.search.stub import expression_evaluator
from google.appengine.api.search.stub import simple_tokenizer
from google.appengine.datastore import document_pb2
from absl.testing import absltest


class ExpressionEvaluatorTest(absltest.TestCase):

  def _SetExpressionOnDocument(self,
                               expr,
                               doc,
                               score=1.0,
                               name='test',
                               order_id=None):
    """Assert that an expression evaluates to a result."""

    index = simple_search_stub.RamInvertedIndex(
        simple_tokenizer.SimpleTokenizer())

    if doc is None:
      doc = simple_search_stub._ScoredDocument(document_pb2.Document(), score)
    elif isinstance(doc, document_pb2.Document):
      doc = simple_search_stub._ScoredDocument(doc, score)
    elif not isinstance(doc, simple_search_stub._ScoredDocument):
      raise Exception('Cannot parse expressions for document of type %s' %
                      type(doc))

    doc.document.id = 'id'
    index.AddDocument('id', doc.document)

    if order_id is not None:
      doc.document.order_id = order_id

    expression = search_service_pb2.FieldSpec.Expression()
    expression.name = name
    expression.expression = expr

    evaluator = expression_evaluator.ExpressionEvaluator(doc, index)
    evaluator.Evaluate(expression)

    return doc

  def _AssertAllEvaluateTo(self, doc, score, *pairs, **kwargs):
    score = float(score)
    for expr, result in pairs:
      doc = self._SetExpressionOnDocument(expr, doc, score, **kwargs)
      self.assertEqual(
          result,
          doc.expressions.get('test', None),
          msg='Expected %s to evaluate to %s, but got %s' %
          (expr, result, doc.expressions.get('test', None)))
      if 'test' in doc.expressions:
        del doc.expressions['test']

  def testArithmeticEvaluation(self):
    self._AssertAllEvaluateTo(
        None, 1.0,
        ('1 + 2', 3),
        ('1 - 2', -1),
        ('3 * 2', 6),
        ('3 / 2', 1.5),
        ('-2', -2),
        ('1 + (2 / 3) * 6', 5),
        ('-(2 + 7) / 9', -1),
        ('"this is a test"', 'this is a test'),
        )

  def testDocumentFields(self):
    doc = document_pb2.Document()
    fields = [
        ('name', 'test', document_pb2.FieldValue.TEXT),
        ('value', '4', document_pb2.FieldValue.NUMBER),
        ('rank', '2', document_pb2.FieldValue.NUMBER),
    ]
    search_util.AddFieldsToDocumentPb('test_doc', fields, doc)
    self._AssertAllEvaluateTo(
        doc, 1.2,
        ('name', 'test'),
        ('value', 4),
        ('value - 2', 2),
        ('value + rank', 6),
        ('_score', 1.2),
        ('max(_score, value)', 4),
        ('nonexistent_field', None),
        ('_rank', 1000),
        order_id=1000
        )

  def testFunctions(self):
    doc = document_pb2.Document()
    fields = [
        ('name', 'testing one two three', document_pb2.FieldValue.TEXT),
        ('value', '4', document_pb2.FieldValue.NUMBER),
        ('value', '7', document_pb2.FieldValue.NUMBER),
        ('rank', '2', document_pb2.FieldValue.NUMBER),
        ('price', '20', document_pb2.FieldValue.NUMBER),
    ]
    search_util.AddFieldsToDocumentPb('test_doc', fields, doc)
    self._AssertAllEvaluateTo(
        doc, 1.0,
        ('count(name)', 1),
        ('count(value)', 2),
        ('max(value, rank, price)', 20),
        ('min(value, rank, price)', 2),
        ('snippet("one", name)', '...testing <b>one</b> two three...'),
        )

  def testDistance(self):
    doc = document_pb2.Document()
    fields = [('name', 'testing one two three', document_pb2.FieldValue.TEXT),
              ('location', search.GeoPoint(latitude=-35.28, longitude=149.12),
               document_pb2.FieldValue.GEO)]
    search_util.AddFieldsToDocumentPb('test_doc', fields, doc)
    self._AssertAllEvaluateTo(
        doc, 1.0,
        ('max(distance(location, geopoint(-34.42, 150.89)), 187698)', 187698),
        ('min(distance(location, geopoint(-34.42, 150.89)), 187697)', 187697),
        )

  def testSnippets(self):
    doc = document_pb2.Document()
    fields = [
        ('content',
         '''Remember, a Jedi's strength flows from the Force. But beware. Anger,
         fear, aggression. The dark side are they. Once you start down the dark
         path, forever will it dominate your destiny. Luke... Luke... do not...
         do not underestimate the powers of the Emperor or suffer your father's
         fate you will. Luke, when gone am I... the last of the Jedi will you
         be.''', document_pb2.FieldValue.TEXT),
        ('short', 'This is a short field.', document_pb2.FieldValue.TEXT),
        ('shorter', 'word', document_pb2.FieldValue.TEXT),
        ('empty', '', document_pb2.FieldValue.TEXT),
    ]
    search_util.AddFieldsToDocumentPb('test_doc', fields, doc)

    doc = self._SetExpressionOnDocument(
        'snippet("forever", content)', doc, name='good')
    doc = self._SetExpressionOnDocument(
        'snippet("Yoda", content)', doc, name='bad')
    doc = self._SetExpressionOnDocument(
        'snippet("short", short)', doc, name='short')
    doc = self._SetExpressionOnDocument(
        'snippet("word", shorter)', doc, name='shorter')
    doc = self._SetExpressionOnDocument(
        'snippet("", empty)', doc, name='empty')

    doc = self._SetExpressionOnDocument(
        'snippet("what what", nonexistent)', doc, name='nonexistent')

    def CheckSnippet(snippet, expect):
      self.assertIn('<b>%s</b>' % expect, snippet)
      self.assertTrue(snippet.startswith('...') and snippet.endswith('...'))
      self.assertLessEqual(
          len(snippet), search_util.DEFAULT_MAX_SNIPPET_LENGTH + 6)

    self.assertIn('good', doc.expressions)
    self.assertIn('bad', doc.expressions)
    self.assertIn('short', doc.expressions)
    self.assertIn('shorter', doc.expressions)

    CheckSnippet(doc.expressions['good'], 'forever')
    CheckSnippet(doc.expressions['short'], 'short')
    CheckSnippet(doc.expressions['shorter'], 'word')

    bad_val = doc.expressions['bad']
    self.assertNotIn('<b>', bad_val)
    self.assertTrue(bad_val.endswith('...'))

  def _AssertFieldValue(self, expected, field_pb):
    actual = expression_evaluator.ExpressionEvaluator._GetFieldValue(field_pb)
    self.assertEqual(expected, actual)

  def testGetFieldValue(self):
    nums = (7, -7, 1e-5, -1e-5, int(1e40), int(-1e40))
    for num in nums:
      field = document_pb2.Field()
      field.name = 'test'
      field_value = field.value
      field_value.type = document_pb2.FieldValue.NUMBER
      field_value.string_value = str(num)
      self._AssertFieldValue(num, field)

    field = document_pb2.Field()
    field.name = 'test'
    field_value = field.value
    field_value.type = document_pb2.FieldValue.TEXT
    field_value.string_value = 'test'
    self._AssertFieldValue('test', field)
    field_value.string_value = u'test'
    self._AssertFieldValue(u'test', field)
    field_value.type = document_pb2.FieldValue.DATE
    d = datetime.date(year=2012, month=5, day=18)
    field_value.string_value = search_util.SerializeDate(d)
    self._AssertFieldValue(datetime.datetime(year=2012, month=5, day=18), field)

    field = document_pb2.Field()
    field.name = 'test'
    field_value = field.value
    field_value.type = document_pb2.FieldValue.GEO
    field_value.geo.lat = 10
    field_value.geo.lng = -50
    expected = geo_util.LatLng(10, -50)
    actual = expression_evaluator.ExpressionEvaluator._GetFieldValue(field)
    self.assertEqual(expected.latitude, actual.latitude)
    self.assertEqual(expected.longitude, actual.longitude)

if __name__ == '__main__':
  absltest.main()
