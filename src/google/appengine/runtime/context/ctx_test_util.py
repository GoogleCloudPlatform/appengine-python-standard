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
"""Test func/class decorator that runs tests in a clean context.

Usage:

@ctx_test_util.isolated_context
class MySuite(unittest.TestCase):
  ...

or

class MySuite(unittest.TestCase):

  @ctx_test_util.isolated_context
  def testFoo(self):
    ...

"""

import functools
import contextvars


def isolated_context(func_or_class):
  """Test func/class decorator functions in a class in a clean context."""
  if isinstance(func_or_class, type):
    return _decorate_class(func_or_class)
  return _decorate_callable(func_or_class)


def _decorate_callable(func):
  @functools.wraps(func)
  def run_in_clean_context(*args, **kwargs):
    contextvars.Context().run(func, *args, **kwargs)
  return run_in_clean_context


def _decorate_class(klass):
  for func_name, func in vars(klass).items():
    if callable(func) and func_name.startswith('test'):
      setattr(klass, func_name, _decorate_callable(func))
  return klass
