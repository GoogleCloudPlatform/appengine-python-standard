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
















"""Low-level utilities used internally by NDB.

These are not meant for use by code outside NDB.
"""

import functools
import logging
import os
import sys

import six

__all__ = []

DEBUG = True



def logging_debug(*args):


  if DEBUG and logging.getLogger().level < logging.DEBUG:
    logging.debug(*args)


def _wrapping(wrapped):
  """A decorator to decorate a decorator's wrapper.

  Following the lead of Twisted and Monocle, this is supposed to make debugging
  heavily decorated code easier.  We'll see...
  # TODO: This copies the functionality of functools.wraps
  # following the patch in http://bugs.python.org/issue3445. We can replace
  # this once upgrading to python 3.3.

  Args:
    wrapped: The decorator to wrap.

  Returns:
    The decorator, now wrapped.
  """
  def wrapping_wrapper(wrapper):
    try:
      wrapper.__wrapped__ = wrapped
      wrapper.__name__ = wrapped.__name__
      wrapper.__doc__ = wrapped.__doc__
      wrapper.__dict__.update(wrapped.__dict__)

      if hasattr(wrapped, '__module__'):
        wrapper.__module__ = wrapped.__module__
    except Exception:
      pass
    return wrapper
  return wrapping_wrapper








wrapping = _wrapping if six.PY2 else functools.wraps


def get_stack(limit=10):

  if not DEBUG:
    return ()
  frame = sys._getframe(1)
  lines = []
  while len(lines) < limit and frame is not None:
    f_locals = frame.f_locals
    ndb_debug = f_locals.get('__ndb_debug__')
    if ndb_debug != 'SKIP':
      line = frame_info(frame)
      if ndb_debug is not None:
        line += ' # ' + str(ndb_debug)
      lines.append(line)
    frame = frame.f_back
  return lines


def func_info(func, lineno=None):
  if not DEBUG:
    return None
  func = getattr(func, '__wrapped__', func)
  code = getattr(func, 'func_code' if six.PY2 else '__code__', None)
  return code_info(code, lineno)


def gen_info(gen):
  if not DEBUG:
    return None
  frame = gen.gi_frame
  if gen.gi_running:
    prefix = 'running generator '
  elif frame:
    if frame.f_lasti < 0:
      prefix = 'initial generator '
    else:
      prefix = 'suspended generator '
  else:
    prefix = 'terminated generator '
  if frame:
    return prefix + frame_info(frame)
  code = getattr(gen, 'gi_code', None)
  if code:
    return prefix + code_info(code)
  return prefix + hex(id(gen))


def frame_info(frame):
  if not DEBUG:
    return None
  return code_info(frame.f_code, frame.f_lineno)


def code_info(code, lineno=None):
  if not DEBUG or not code:
    return ''
  funcname = code.co_name


  filename = os.path.basename(code.co_filename)
  if lineno is None:
    lineno = code.co_firstlineno
  return '%s(%s:%s)' % (funcname, filename, lineno)


def positional(max_pos_args):
  """A decorator to declare that only the first N arguments may be positional.

  Note that for methods, n includes 'self'.
  """
  __ndb_debug__ = 'SKIP'

  def positional_decorator(wrapped):
    if not DEBUG:
      return wrapped
    __ndb_debug__ = 'SKIP'

    @wrapping(wrapped)
    def positional_wrapper(*args, **kwds):
      __ndb_debug__ = 'SKIP'
      if len(args) > max_pos_args:
        plural_s = ''
        if max_pos_args != 1:
          plural_s = 's'
        raise TypeError(
            '%s() takes at most %d positional argument%s (%d given)' %
            (wrapped.__name__, max_pos_args, plural_s, len(args)))
      return wrapped(*args, **kwds)
    return positional_wrapper
  return positional_decorator


def decorator(wrapped_decorator):
  """Converts a function into a decorator that optionally accepts keyword
  arguments in its declaration.

  Example usage:
    @utils.decorator
    def decorator(func, args, kwds, op1=None):
      ... apply op1 ...
      return func(*args, **kwds)

    # Form (1), vanilla
    @decorator
    foo(...)
      ...

    # Form (2), with options
    @decorator(op1=5)
    foo(...)
      ...

  Args:
    wrapped_decorator: A function that accepts positional args (func, args,
      kwds) and any additional supported keyword arguments.

  Returns:
    A decorator with an additional 'wrapped_decorator' property that is set to
  the original function.
  """
  def helper(_func=None, **options):
    def outer_wrapper(func):
      @wrapping(func)
      def inner_wrapper(*args, **kwds):
        return wrapped_decorator(func, args, kwds, **options)
      return inner_wrapper

    if _func is None:

      return outer_wrapper


    if options:

      raise TypeError('positional arguments not supported')
    return outer_wrapper(_func)
  helper.wrapped_decorator = wrapped_decorator
  return helper


def tweak_logging():






  q = 0
  v = 0
  for arg in sys.argv[1:]:
    if arg.startswith('-v'):
      v += arg.count('v')
    if arg.startswith('-q'):
      q += arg.count('q')
  if v >= 2:
    level = logging.INFO
    if v >= 3:
      level = logging.DEBUG - 1
    logging.basicConfig(level=level)
  if q > 0:
    global DEBUG
    DEBUG = False

legacy_bytes_mode = os.environ.get('NDB_KEY_USE_BYTES', '0') == '1'


def use_bytes():
  """Tell if NDB should expose kind/id/namespace/app as bytes or strings.

  Internally, these attributes are represented as bytes no matter how NDB is
  configured, but this implementation detail should not have leaked into the
  public API in python3.  During a short transition period, the
  NDB_KEY_USE_BYTES env var can be used to configure NDB to expose these
  attributes as bytes (legacy behavior) or strings (new behavior).  Once no apps
  depend on the old behavior, this setting will be removed.

  Returns:
    True for bytes (legacy behavior) or False for string (new behavior)
  """
  return legacy_bytes_mode


if 'test' in os.path.basename(sys.argv[0]):
  tweak_logging()
