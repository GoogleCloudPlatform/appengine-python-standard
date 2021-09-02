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

@ctx_test_util.isolated_context()
class MySuite(unittest.TestCase):
  ...

or

class MySuite(unittest.TestCase):

  @ctx_test_util.isolated_context()
  def testFoo(self):
    ...

"""
import contextvars
import functools
import os

from google.appengine.runtime import context


def isolated_context(*args, **kwargs):
  """Decorates a test function or class to run itself in a clean context.

  When used with a class, it will also run setUp and tearDown in that context
  by default.

  Args:
    *args: See _decorate_class and _decorate_callable
    **kwargs: See _decorate_class and _decorate_callable

  Returns:
    The raw function decorator.
  """
  def argless_decorator(func_or_class):
    if isinstance(func_or_class, type):
      return _decorate_class(*args, **kwargs)(func_or_class)
    return _decorate_callable(*args, **kwargs)(func_or_class)
  return argless_decorator


def _decorate_callable(
    backup_and_restore_os_environ=context.USE_LEGACY_CONTEXT_MODE,
    set_up=None,
    tear_down=None):
  """Decorates a test function to run itself in a clean context."""

  def argless_decorator(func):
    def func_with_setup_teardown(*args, **kwargs):
      self = kwargs.get('self') or args[0]
      if set_up:
        set_up(self)
      try:
        return func(*args, **kwargs)
      finally:
        if tear_down:
          tear_down(self)

    @functools.wraps(func)
    def run_in_clean_context(*args, **kwargs):
      if backup_and_restore_os_environ:
        previous_os_environ = os.environ.copy()
      try:
        contextvars.Context().run(func_with_setup_teardown, *args, **kwargs)
      finally:
        if backup_and_restore_os_environ:
          os.environ.clear()
          os.environ.update(previous_os_environ)
    return run_in_clean_context

  return argless_decorator


def _decorate_class(
    backup_and_restore_os_environ=context.USE_LEGACY_CONTEXT_MODE,
    run_setup_and_teardown_inside_context=True):
  """Decorates a test class to run itself in a clean context."""

  def argless_decorator(klass):
    set_up, tear_down = None, None
    if run_setup_and_teardown_inside_context:
      set_up = getattr(klass, 'setUp', lambda self: super(klass, self).setUp())
      tear_down = getattr(klass, 'tearDown',
                          lambda self: super(klass, self).tearDown())
      setattr(klass, 'setUp', lambda self: None)
      setattr(klass, 'tearDown', lambda self: None)

    for func_name, func in vars(klass).items():
      if callable(func) and func_name.startswith('test'):
        setattr(klass, func_name, _decorate_callable(
            backup_and_restore_os_environ, set_up, tear_down)(func))
    return klass
  return argless_decorator
