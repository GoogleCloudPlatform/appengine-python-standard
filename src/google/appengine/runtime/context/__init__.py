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
import os

from google.appengine.runtime.context import gae_headers
from google.appengine.runtime.context import wsgi

USE_LEGACY_CONTEXT_MODE = True


def _getvar(key):
  return vars(gae_headers).get(key, vars(wsgi).get(key))


def get(key, default=None):
  """Read context from os.environ if USE_LEGACY_CONTEXT_MODE else, from contextvars."""
  if USE_LEGACY_CONTEXT_MODE:
    return os.environ.get(key, default)
  ctxvar = _getvar(key)
  assert isinstance(ctxvar, contextvars.ContextVar)
  val = ctxvar.get(default)
  if isinstance(val, bool):
    return '1' if val else '0'
  return val


def put(key, value):
  """Write context to os.environ if USE_LEGACY_CONTEXT_MODE and to contextvars if they exist."""
  if USE_LEGACY_CONTEXT_MODE:
    os.environ[key] = value
  ctxvar = _getvar(key)
  assert isinstance(ctxvar, contextvars.ContextVar)
  if key == 'USER_IS_ADMIN':
    ctxvar.set(value == '1')
  ctxvar.set(value)


def init_from_wsgi_environ(wsgi_env):
  gae_headers.init_from_wsgi_environ(wsgi_env)
  wsgi.init_from_wsgi_environ(wsgi_env)
