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


"""Tests for google.appengine.api.search.query_parser."""



import google

from absl import app
from absl import flags
from google.appengine.api.search import query_parser
from absl.testing import absltest

FLAGS = flags.FLAGS


def _Sequence(*args):
  return '(SEQUENCE %s)' % ' '.join(args)


def _Conjunction(*args):
  return '(CONJUNCTION %s)' % ' '.join(args)


def _Disjunction(*args):
  return '(DISJUNCTION %s)' % ' '.join(args)


def _Negation(arg):
  return '(NEGATION %s)' % arg


def _FieldEq(field, val, op=':'):
  return '(%s (VALUE TEXT %s) (VALUE TEXT %s))' % (op, field, val)


def _Global(val, value_type='TEXT'):
  return '(HAS GLOBAL (VALUE %s %s))' % (value_type, val)


class QueryParserTest(absltest.TestCase):

  def assertParsesToSame(self, expected, query):
    result = query_parser.ParseAndSimplify(query).toStringTree()
    self.assertEqual(expected, result,
                     'expected %s but got %s' % (expected, result))

  def testParse(self):
    self.assertParsesToSame(_Global('hello'), 'hello')
    self.assertParsesToSame(_Global('12402102-AAA5-480D-B26E-6B955D97685A'),
                            '12402102-AAA5-480D-B26E-6B955D97685A')
    self.assertParsesToSame(_Conjunction(_Global('hello'), _Global('world')),
                            'hello AND world')
    self.assertParsesToSame(_Disjunction(_Global('hello'), _Global('world')),
                            'hello OR world')
    self.assertParsesToSame(_Negation(_Global('world')), 'NOT world')
    self.assertParsesToSame(_FieldEq('title', 'hello'), 'title:hello')
    self.assertParsesToSame(_FieldEq('foo', 'bar', op='!='), 'foo != bar')
    self.assertParsesToSame(_FieldEq('foo', 'bar', op='!='), 'foo!= bar')
    self.assertParsesToSame(_FieldEq('foo', 'bar', op='!='), 'foo !=bar')
    self.assertParsesToSame(_FieldEq('foo', 'bar', op='!='), 'foo!=bar')


    self.assertParsesToSame(
        _Global('" hello   world "', value_type='STRING'), '"hello world"')

    self.assertParsesToSame(
        _Sequence(
            _FieldEq('field', '99', op='>'), _FieldEq('field', '199', op='<')),
        'field > 99 field < 199')

    self.assertParsesToSame(
        _Conjunction(
            _Disjunction(_Global('hello'), _Global('hola')),
            _Sequence(
                _Disjunction(_Global('world'), _Global('mundo')),
                _Negation(_Global('today')))),
        '(hello OR hola) AND (world OR mundo) NOT today')

    self.assertRaises(query_parser.QueryException, query_parser.Parse,
                      'OR AND NOT !!!')

  def testUnicode(self):

    query_parser.ParseAndSimplify(u'\u0909')
    query_parser.ParseAndSimplify(u'\u7fff')


    query_parser.ParseAndSimplify(u'\u8000')
    query_parser.ParseAndSimplify(u'\uffee')


    query_parser.ParseAndSimplify(u'\fffc')


    query_parser.ParseAndSimplify(u'\U00020c78')

  def testUnicodeTokenization(self):

    self.assertParsesToSame(
        _FieldEq(u'p\ud801\udc37q', u'r\ud801\udc37s', op='!='),
        u'p\U00010437q!=r\U00010437s')


def main(unused_argv):
  absltest.main()


if __name__ == '__main__':
  absltest.main(main)
