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

  When used with a class, it will run each test function in its own context.
  It will also run setUp, tearDown, and doCleanups in that context by default.

  Args:
    *args: See _isolated_context_class and _isolated_context_callable.
    **kwargs: See _isolated_context_class and _isolated_context_callable.

  Returns:
    The raw function decorator.
  """
  def argless_decorator(func_or_class):
    if isinstance(func_or_class, type):
      return _isolated_context_class(*args, **kwargs)(func_or_class)
    return _isolated_context_callable(*args, **kwargs)(func_or_class)
  return argless_decorator


def both_context_modes(*args, **kwargs):
  """Adds subtests which test the non-default context mode.

  This decorator also calls isolated_context for you.
  Using this as a class decorator will only wrap the functions declared directly
  on that class, not on functions inherited from parent classes.

  Args:
    *args: See _isolated_context_class and _isolated_context_callable
    **kwargs: See _isolated_context_class and _isolated_context_callable

  Returns:
    The raw function decorator.
  """
  def argless_decorator(func_or_class):
    if isinstance(func_or_class, type):
      return _both_context_modes_class(*args, **kwargs)(func_or_class)
    return _both_context_modes_callable(*args, **kwargs)(func_or_class)
  return argless_decorator


def _isolated_context_callable(
    backup_and_restore_os_environ=context.READ_FROM_OS_ENVIRON):
  """Decorates a function to run itself in a clean context."""

  def argless_decorator(func):
    def run_in_ctx(*args, **kwargs):
      contextvars.Context().run(func, *args, **kwargs)
    if backup_and_restore_os_environ:
      run_in_ctx = _isolate_os_environ(run_in_ctx)
    return run_in_ctx

  return argless_decorator


def _isolate_os_environ(func):
  """Save and restore os.environ."""

  @functools.wraps(func)
  def run_in_isolated_os_environ(*args, **kwargs):
    previous_os_environ = os.environ.copy()
    try:
      func(*args, **kwargs)
    finally:
      os.environ.clear()
      os.environ.update(previous_os_environ)

  return run_in_isolated_os_environ


def _isolated_context_class(
    backup_and_restore_os_environ=context.READ_FROM_OS_ENVIRON,
    run_setup_teardown_cleanup_inside_context=True):
  """Decorates a test class to run itself in a clean context."""

  isolate_fn_wrapper = _isolated_context_callable(backup_and_restore_os_environ)

  def argless_decorator(klass):
    if run_setup_teardown_cleanup_inside_context:
      run_fn = getattr(
          klass, 'run',
          lambda self, *args, **kwargs: super(klass, self).run(*args, **kwargs))
      setattr(klass, 'run', isolate_fn_wrapper(run_fn))
    else:
      for func_name, func in vars(klass).items():
        if callable(func) and func_name.startswith('test'):
          setattr(klass, func_name, isolate_fn_wrapper(func))
    return klass
  return argless_decorator


def _both_context_modes_class():
  """Class decorator that duplicates every test function each context mode."""

  def argless_decorator(klass):
    klass = _isolated_context_class(backup_and_restore_os_environ=True)(klass)
    for func_name, func in vars(klass).items():
      if callable(func) and func_name.startswith('test'):
        setattr(klass, func_name, _both_context_modes_callable_raw(func))
    return klass

  return argless_decorator


def _both_context_modes_callable():
  def argless_decorator(func):
    return _isolated_context_callable()(_both_context_modes_callable_raw(func))
  return argless_decorator


def set_both(key, value):
  """Write to both legacy context (os.environ) and new contextvars."""


  strval = value
  if key == 'USER_IS_ADMIN':

    if isinstance(value, str):
      value = value == '1'
    elif isinstance(value, bool):
      strval = '1' if value else '0'
  os.environ[key] = strval
  ctxvar = vars(context.gae_headers).get(key, vars(context.wsgi).get(key))
  assert isinstance(ctxvar, contextvars.ContextVar)
  ctxvar.set(value)


def _both_context_modes_callable_raw(func):
  """Tests both context modes WITHOUT isolating context.

  This is factored out of _both_context_modes_callable so that
  @both_context_modes doesn't double-isolate functions when used as a class
  decorator.

  Args:
    func: The function to wrap.

  Returns:
    The wrapped function.
  """
  @functools.wraps(func)
  def test_both(self, *args, **kwargs):
    default_context_mode = context.READ_FROM_OS_ENVIRON
    other_context_mode = not default_context_mode
    try:
      func(self, *args, **kwargs)
      context.READ_FROM_OS_ENVIRON = other_context_mode
      with self.subTest(READ_CONTEXT_FROM_OS_ENVIRON=other_context_mode):
        func(self, *args, **kwargs)
    finally:
      context.READ_FROM_OS_ENVIRON = default_context_mode
  return test_both
