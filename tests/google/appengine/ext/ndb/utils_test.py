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

"""Tests for utils."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pickle

from google.appengine.ext.ndb import utils
from absl.testing import absltest


def example_decorator_1(func):

  @utils.wrapping(func)
  def example_wrapper():
    return func() + 10

  return example_wrapper


@example_decorator_1
def example_func_1():
  return 5


@utils.positional(3)
def example_func_2(*unused_args):
  pass


@utils.decorator
def example_decorator_2(func, *unused_args, **unused_kwargs):
  return func() * 2


@example_decorator_2
def example_func_3():
  return 6


@utils.decorator
def squaring_decorator(func, args, unused_kwargs):
  result = func(*args)
  return result * result


@squaring_decorator
def sum_func(x, y):
  return x + y


class UtilsTest(absltest.TestCase):

  def testWrapping(self):
    self.assertEqual(15, example_func_1())

  def testDecoratorPicklingUnpickling(self):
    tup = (sum_func, 3, 3)
    s = pickle.dumps(tup, protocol=pickle.HIGHEST_PROTOCOL)
    f, x, y = pickle.loads(s)
    actual = f(x, y)
    self.assertEqual(36, actual)

  def testGetStack(self):
    stack = utils.get_stack()
    self.assertGreater(len(stack), 1)

  def testFuncInfo(self):
    self.assertIsNotNone(utils.func_info(example_func_1))

  def testGenInfo(self):
    gen = (x for x in range(10))
    next(gen)
    info = utils.gen_info(gen)
    self.assertStartsWith(info, 'suspended generator')

  def testFrameInfo(self):
    gen = (x for x in range(10))
    frame = gen.gi_frame
    self.assertIsNotNone(utils.frame_info(frame))

  def testCodeInfo(self):
    gen = (x for x in range(10))
    code = gen.gi_code
    self.assertIsNotNone(utils.code_info(code))

  def testPositional(self):
    with self.assertRaises(TypeError):
      example_func_2(1, 2, 3, 4)

  def testDecorator(self):
    self.assertEqual(12, example_func_3())


if __name__ == '__main__':
  absltest.main()
