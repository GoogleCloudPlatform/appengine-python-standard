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
"""Wrapper for contextvars that can fall back to old os.environ hack."""
import contextvars
import functools
import os
from typing import Dict

from google.appengine.runtime.context import gae_headers
from google.appengine.runtime.context import wsgi

READ_FROM_OS_ENVIRON = os.environ.get('READ_GAE_CONTEXT_FROM_OS_ENVIRON',
                                      'true') == 'true'






_UNSET = object()


@functools.cache
def _get_defined_vars():
  return {
      key: var for (key, var)
      in tuple(vars(gae_headers).items()) + tuple(vars(wsgi).items())
      if isinstance(var, contextvars.ContextVar)
  }


def get(key, default=_UNSET):
  """Read context from os.environ if READ_GAE_CONTEXT_FROM_OS_ENVIRON else, from contextvars."""
  defined_vars = _get_defined_vars()
  if key not in defined_vars:
    raise LookupError(f'Unknow context variable "{key}"')
  if READ_FROM_OS_ENVIRON:
    return os.environ.get(key, None if default is _UNSET else default)
  ctxvar = defined_vars[key]
  val = ctxvar.get() if default == _UNSET else ctxvar.get(default)
  if isinstance(val, bool):
    return '1' if val else '0'
  return val


def init_from_wsgi_environ(
    wsgi_env) -> Dict[contextvars.ContextVar, contextvars.Token]:
  return {
      **gae_headers.init_from_wsgi_environ(wsgi_env),
      **wsgi.init_from_wsgi_environ(wsgi_env),
  }
