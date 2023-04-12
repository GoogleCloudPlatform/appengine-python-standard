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
import unittest

class BrokenTest(unittest.TestCase.failureException):

  def __repr__(self):
    name, reason = self.args
    return '%s: %s: %s works now' % ((self.__class__.__name__, name, reason))


def broken(reason, *exceptions):
  """Indicates a failing (or erroneous) test case fails that should succeed.

    If the test fails with an exception, list the exception type in args
  """

  def wrapper(test_method):

    def replacement(*args, **kwargs):
      try:
        test_method(*args, **kwargs)
      except exceptions or unittest.TestCase.failureException:
        pass
      else:
        raise BrokenTest(test_method.__name__, reason)

    replacement.__doc__ = test_method.__doc__
    replacement.__name__ = 'XXX_' + test_method.__name__
    replacement.todo = reason
    return replacement

  return wrapper
