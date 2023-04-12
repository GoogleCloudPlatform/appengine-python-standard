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


"""Tests for google.appengine.api.search.expression_parser."""



import google

from absl import app
from absl import flags
from google.appengine.api.search import expression_parser
from absl.testing import absltest

FLAGS = flags.FLAGS


class ExpressionParserTest(absltest.TestCase):

  def toStringTree(self, node):
    """Modified version of tree.toStringTree() handles node.toString()=None."""
    if not node.children:
      return node.toString()

    ret = ''
    if not node.isNil():
      ret += '(%s ' % (node.toString())

    ret += ' '.join([self.toStringTree(child) for child in node.children if
                     self.toStringTree(child) is not None])

    if not node.isNil():
      ret += ')'

    return ret

  def Parse(self, expected, expression):
    self.assertEqual(
        expected, self.toStringTree(expression_parser.Parse(expression).tree))

  def testParse(self):
    self.Parse('price', 'price')
    self.Parse('(+ price tax)', 'price + tax')
    self.Parse('(< (+ price tax) 100)', 'price + tax < 100')
    self.Parse('(snippet "this query" content)',
               'snippet("this query", content)')
    self.Parse('(snippet "\\\"this query\\\"" content)',
               'snippet("\\\"this query\\\"", content)')
    self.Parse('(snippet "\\\"foo bar\\\" baz" content)',
               'snippet("\\\"foo bar\\\" baz", content)')
    self.assertRaises(expression_parser.ExpressionException,
                      expression_parser.Parse, 'unknown(')
    self.assertRaises(expression_parser.ExpressionException,
                      expression_parser.Parse, 'price > ')

  def testUnicode(self):

    expression_parser.Parse(u'snippet("\u0909", content)')
    expression_parser.Parse(u'snippet("\u7fff", content)')


    expression_parser.Parse(u'snippet("\u8000", content)')
    expression_parser.Parse(u'snippet("\uffee", content)')


    expression_parser.Parse(u'snippet("\fffc", content)')


    expression_parser.Parse(u'snippet("\U00020c78", content)')


def main(unused_argv):
  absltest.main()


if __name__ == '__main__':
  absltest.main(main)
