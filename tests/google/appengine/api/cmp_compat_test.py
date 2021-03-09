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




"""Tests for google.appengine.api.cmp_compat."""

from __future__ import absolute_import
from __future__ import division

from __future__ import print_function

import enum

from google.appengine.api import cmp_compat

from absl import app
from absl.testing import absltest


class NoComparator(object):

  def __init__(self):
    pass


@cmp_compat.total_ordering_from_cmp
class IHaveACmp(object):

  def __init__(self, val):
    self.val = val

  def __cmp__(self, other):
    return cmp_compat.cmp(self.val, other.val)


@cmp_compat.total_ordering_from_cmp
class ICompareToPrimitives(object):

  def __init__(self, val):
    self.val = val

  def __cmp__(self, other):
    return cmp_compat.cmp(self.val, other)


class Outcome(enum.Enum):

  LT = 0
  EQ = 1
  NE = 2


test_cases = [

    (1, 1, Outcome.EQ),
    (1, 2, Outcome.LT),


    (u'foo', u'foo', Outcome.EQ),
    (u'bar', u'foo', Outcome.LT),


    (b'foo', b'foo', Outcome.EQ),
    (b'bar', b'foo', Outcome.LT),


    ((1, 2), (1, 2), Outcome.EQ),
    ((1, 2), (1, 3), Outcome.LT),
    ((1, 2), (1, 2, 1), Outcome.LT),


    ([1, 2], [1, 2], Outcome.EQ),
    ([1, 2], [1, 3], Outcome.LT),
    ([1, 2], [1, 2, 1], Outcome.LT),


    (1, '0', Outcome.LT),

    ([1, 1], (1, 2), Outcome.LT),


    (NoComparator(), NoComparator(), Outcome.NE),



    ((1, 1), (1, '0'), Outcome.LT),
    ([1, 1], [1, '0'], Outcome.LT),


    (dict(a=1, b=1), dict(a=1, b=2), Outcome.LT),
    (dict(a=1, b=1), dict(a=1, b=1, c=1), Outcome.LT),
    (dict(a=1, b=1), dict(a=1, c=1), Outcome.LT),



    (ICompareToPrimitives(1), 1, Outcome.EQ),
    (ICompareToPrimitives(1), 2, Outcome.LT),
]


class CmpTest(absltest.TestCase):
  """Tests for the croninfo.CronEntry class."""

  def testCmp(self):
    """Tests the Python 3 polyfill for Python 2's cmp."""

    for a, b, outcome in test_cases:
      if outcome == Outcome.LT:
        self.assertLess(cmp_compat.cmp(a, b), 0)
        self.assertGreater(cmp_compat.cmp(b, a), 0)
      elif outcome == Outcome.EQ:
        self.assertEqual(cmp_compat.cmp(a, b), 0)
        self.assertEqual(cmp_compat.cmp(b, a), 0)
      elif outcome == Outcome.NE:
        self.assertNotEqual(cmp_compat.cmp(a, b), 0)
        self.assertNotEqual(cmp_compat.cmp(b, a), 0)

  def testTotalOrderingFromCmp(self):
    for a_val, b_val, outcome in test_cases:
      a = IHaveACmp(a_val)
      b = IHaveACmp(b_val)

      if outcome == Outcome.LT:
        self.assertLess(a, b)
        self.assertGreater(b, a)
      elif outcome == Outcome.EQ:
        self.assertEqual(a, b)
        self.assertEqual(b, a)
      elif outcome == Outcome.NE:
        self.assertNotEqual(a, b)
        self.assertNotEqual(b, a)


def main(unused_argv):
  absltest.main()


if __name__ == '__main__':
  absltest.main()
