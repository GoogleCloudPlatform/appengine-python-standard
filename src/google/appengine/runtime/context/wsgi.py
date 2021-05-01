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
"""Save a few WSGI vars into request context."""

import contextvars


HTTP_HOST = contextvars.ContextVar('HTTP_HOST')
HTTP_USER_AGENT = contextvars.ContextVar('HTTP_USER_AGENT')

HTTP_X_CLOUD_TRACE_CONTEXT = contextvars.ContextVar(
    'HTTP_X_CLOUD_TRACE_CONTEXT')


PATH_INFO = contextvars.ContextVar('PATH_INFO')
PATH_TRANSLATED = contextvars.ContextVar('PATH_TRANSLATED')
QUERY_STRING = contextvars.ContextVar('QUERY_STRING')
SERVER_NAME = contextvars.ContextVar('SERVER_NAME')
SERVER_PORT = contextvars.ContextVar('SERVER_PORT')
SERVER_PROTOCOL = contextvars.ContextVar('SERVER_PROTOCOL')


def init_from_wsgi_environ(wsgi_env):
  for ctxvar in [v for _, v in globals().items()
                 if isinstance(v, contextvars.ContextVar)]:
    if ctxvar.name in wsgi_env:
      ctxvar.set(wsgi_env[ctxvar.name])
