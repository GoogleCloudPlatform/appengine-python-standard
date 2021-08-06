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
"""Helpers providing a bridge between the Python 2 `__cmp__` and Python 3.

Python 2 uses methods called `__cmp__` to override object comparison behavior;
in Python 3 `__cmp__` is replaced by rich comparison functions.

Additionally, Python 2 allows code to compare objects of different types,
falling back to lexographical class-name comparisons if types are different (so
instance of "int" are always less than instances of "str").

This file offers some utilities to bridge the gap between Python 2 and 3.
"""


import functools
import six
from six.moves import zip


def total_ordering_from_cmp(cls):
  """Class decorator that fills in missing ordering methods from `__cmp__`.

  This lets us take a class defined for Python 2's ordering system (using
  `__cmp__`) and use it with minimal changes — just a decorator — in Python 3.

  This implementation is adapted from the Python 2 version of
  `functools.total_ordering`, which derives these methods from each other
  instead of from `__cmp__`.

  Args:
    cls: The class to decorate.

  Returns:
    The decorated class.
  """

  convert = [('__gt__', lambda self, other: self.__cmp__(other) > 0),
             ('__lt__', lambda self, other: self.__cmp__(other) < 0),
             ('__le__', lambda self, other: self.__cmp__(other) <= 0),
             ('__eq__', lambda self, other: self.__cmp__(other) == 0),
             ('__ne__', lambda self, other: self.__cmp__(other) != 0),
             ('__ge__', lambda self, other: self.__cmp__(other) >= 0)]

  for opname, opfunc in convert:
    opfunc.__name__ = opname
    opfunc.__doc__ = getattr(int, opname).__doc__
    setattr(cls, opname, opfunc)
  return cls


if six.PY2:
  cmp = cmp
else:

  def _cmp_fallback(a, b):
    """cmp fallback for types not directly comparable via __gt__ and __lt__."""

    if type(a) is type(b):

      return cmp(id(a), id(b))


    return cmp(str(type(a)), str(type(b)))

  def _cmp_gt_lt(a, b):
    """cmp using __gt__ and __lt__."""

    a_type = type(a)

    gt = a_type.__gt__(a, b)
    if gt is NotImplemented:
      return gt

    lt = a_type.__lt__(a, b)
    if lt is NotImplemented:
      return lt

    return gt - lt

  def cmp(a, b):
    """Emulate Python 2 cmp in Python 3.

    This is not necessarily a complete emulation; it's simply enough to support
    Titanoboa's port of apphosting.

    Args:
      a: An object to compare
      b: Another object to compare

    Returns:
      Negative if a is less than b, 0 if a equals b, and positive otherwise.
    """

    a_type = type(a)
    b_type = type(b)

    if a_type is b_type and isinstance(a, (list, tuple)):

      for a_elem, b_elem in zip(a, b):
        rc = cmp(a_elem, b_elem)
        if rc != 0:
          return rc
      return cmp(len(a), len(b))

    if a_type is b_type and isinstance(a, dict):

      a_sorted = sorted(six.iteritems(a), key=functools.cmp_to_key(cmp))
      b_sorted = sorted(six.iteritems(b), key=functools.cmp_to_key(cmp))
      return cmp(a_sorted, b_sorted)

    result = _cmp_gt_lt(a, b)
    if result is not NotImplemented:
      return result

    result = _cmp_gt_lt(b, a)
    if result is not NotImplemented:
      return -result

    return _cmp_fallback(a, b)
