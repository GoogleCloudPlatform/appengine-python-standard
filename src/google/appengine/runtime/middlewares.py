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
"""Methods for gluing a user's application into the GAE environment."""

import binascii
import contextvars
import functools
import logging
import logging.handlers
import os
import sys
import traceback

from google.appengine.api import namespace_manager
from google.appengine.api.runtime import runtime
from google.appengine.ext.deferred import deferred
from google.appengine.runtime import background
from google.appengine.runtime import callback
from google.appengine.runtime import context
from google.appengine.runtime import default_api_stub
from google.appengine.runtime import request_environment
import six
from six.moves import urllib



MAX_CONCURRENT_REQUESTS = 501



ENV_VARS_FROM_HTTP_X_APPENGINE_HEADERS = [
    'AUTH_DOMAIN',
    'DATACENTER',
    'DEFAULT_VERSION_HOSTNAME',
    'HTTPS',
    'REMOTE_ADDR',
    'REQUEST_ID_HASH',
    'REQUEST_LOG_ID',
    'USER_EMAIL',
    'USER_ID',
    'USER_IS_ADMIN',
    'USER_NICKNAME',
    'USER_ORGANIZATION',



    'APPSERVER_DATACENTER',
    'APPSERVER_TASK_BNS',
    'GAIA_AUTHUSER',
    'GAIA_ID',
    'GAIA_SESSION',
    'LOAS_PEER_USERNAME',
    'LOAS_SECURITY_LEVEL',
    'TRUSTED_IP_REQUEST',
]

LOCAL_OVERRIDABLE_VARS = [
    'USER_ID',
    'USER_EMAIL',
    'USER_IS_ADMIN',
    'AUTH_DOMAIN',
]


def middleware(f):
  """Function decorator for making WSGI middlewares."""
  return functools.update_wrapper(
      lambda app: lambda wsgi_env, start_resp: f(app, wsgi_env, start_resp),
      f)


def Wrap(app, middlewares):
  """Wrap(app, [a,b,c]) is equivalent to a(b(c(app)))."""
  return functools.reduce(lambda app, mw: mw(app), reversed(middlewares), app)


@middleware
def UseRequestSecurityTicketForApiMiddleware(app, wsgi_env, start_response):
  """WSGI middleware wrapper that sets the thread to use the security ticket.

  This sets up the appengine api so that if a security ticket is passed in with
  the request, it will be used.

  Args:
    app: (callable) a WSGI app per PEP 3333.
    wsgi_env: see PEP 3333
    start_response: see PEP 3333

  Returns:
    A wrapped <app>, which is also a valid WSGI app.
  """
  try:
    default_api_stub.DefaultApiStub.SetUseRequestSecurityTicketForThread(True)
    return app(wsgi_env, start_response)
  finally:

    default_api_stub.DefaultApiStub.SetUseRequestSecurityTicketForThread(False)


@middleware
def WaitForResponseMiddleware(app, wsgi_env, start_response):
  """WSGI middleware wrapper that waits until response is ready.

  Some middlewares here and some external middlewares rely on behavior that app
  calls finish when response is ready and they do post-processing that should
  be done when handler has returned all response.
  This middleware added for compatibility with such middlewares,
  once all users migrated to Python3, all middlewares should use `yield app()`
  instead of `return app()` and this one should be removed.

  Args:
    app: (callable) a WSGI app per PEP 3333.
    wsgi_env: see PEP 3333
    start_response: see PEP 3333

  Returns:
    A wrapped <app>, which is also a valid WSGI app.
  """
  return list(app(wsgi_env, start_response))


@middleware
def ErrorLoggingMiddleware(app, wsgi_env, start_response):
  """Catch and log unhandled errors for the given app."""
  try:
    return app(wsgi_env, start_response)
  except:








    log_message = traceback.format_exception(
        sys.exc_info()[0],
        sys.exc_info()[1],
        sys.exc_info()[2])

    logging.error(''.join(log_message))
    raise


def _MakeRequestIdHash(log_id):
  """Invent a REQUEST_ID_HASH to replace the one the python27g runtime had."""









  request_id_hash = binascii.crc32(six.ensure_binary(log_id))
  request_id_hash &= 0xffffffff
  request_id_hash_hex = '%08X' % request_id_hash
  return request_id_hash_hex


@middleware
def WsgiEnvSettingMiddleware(app, wsgi_env, start_response):
  """Initialize wsgi_env with reasonable values derived from HTTP headers."""

  https = wsgi_env.get('HTTP_X_APPENGINE_HTTPS')
  if https is not None:
    wsgi_env['HTTPS'] = https










  protocol = wsgi_env.get('HTTP_X_FORWARDED_PROTO')
  if protocol is not None:
    wsgi_env['wsgi.url_scheme'] = protocol
    if protocol == 'http':
      wsgi_env['SERVER_PORT'] = '80'
    elif protocol == 'https':
      wsgi_env['SERVER_PORT'] = '443'
    else:
      logging.warning('Unrecognized value for HTTP_X_FORWARDED_PROTO (%s)'
                      ", won't modify SERVER_PORT", protocol)

  http_host = wsgi_env.get('HTTP_HOST')
  if http_host is not None:
    server_name = urllib.parse.urlparse('//' + http_host).hostname
    wsgi_env['SERVER_NAME'] = server_name



  user_ip = wsgi_env.get('HTTP_X_APPENGINE_USER_IP')
  if user_ip is not None:
    wsgi_env['REMOTE_ADDR'] = user_ip

  return app(wsgi_env, start_response)


@middleware
def SetContextFromHeadersMiddleware(app, wsgi_env, start_response):
  """Set the contextvars from the X_APPENGINE headers."""
  context.init_from_wsgi_environ(wsgi_env)
  return app(wsgi_env, start_response)


@middleware
def OverrideHttpHeadersFromOsEnvironMiddleware(app, wsgi_env, start_response):
  """Override certain HTTP headers with env vars for testing."""
  for key in LOCAL_OVERRIDABLE_VARS:
    val = os.environ.get(key)
    if val is not None:
      wsgi_env['HTTP_X_APPENGINE_'+key] = val
  return app(wsgi_env, start_response)


@middleware
def LegacyWsgiRemoveXAppenginePrefixMiddleware(app, wsgi_env, start_response):
  """Reset HTTP_X_APPENGINE_<foo> as just <foo>."""

  wsgi_env.setdefault('HTTP_X_APPENGINE_AUTH_DOMAIN', 'gmail.com')
  wsgi_env.setdefault('HTTP_X_APPENGINE_USER_IS_ADMIN', '0')
  for key in ENV_VARS_FROM_HTTP_X_APPENGINE_HEADERS:
    value = wsgi_env.get('HTTP_X_APPENGINE_' + key)
    if value is not None:
      wsgi_env[key] = value
  return app(wsgi_env, start_response)


def MakeLegacyWsgiEnvSettingMiddleware(threadsafe=None):
  """Set wsgi_env like it was set in python27."""

  @middleware
  def LegacyWsgiEnvSettingMiddleware(app, wsgi_env, start_response):



    wsgi_env['CLOUD_TRACE_ENABLE_STACK_TRACE'] = ''
    if 'GAE_RUNTIME' in os.environ:
      wsgi_env['GAE_RUNTIME'] = os.environ['GAE_RUNTIME']
    if threadsafe is not None:
      wsgi_env['wsgi.multithread'] = threadsafe
    log_id = wsgi_env.get('HTTP_X_APPENGINE_REQUEST_LOG_ID')
    if log_id is not None:
      wsgi_env['HTTP_X_APPENGINE_REQUEST_ID_HASH'] = _MakeRequestIdHash(log_id)
    return app(wsgi_env, start_response)

  return LegacyWsgiEnvSettingMiddleware


def MakeInitLegacyRequestOsEnvironMiddleware():
  """Patch os.environ to be thread local, and stamp it with default values.

  When this function is called, we remember the values of os.environ. When the
  wrapped inner function (i.e. the WSGI middleware) is called, we patch
  os.environ to be thread local, and we fill in the remembered values, and merge
  in WSGI env vars.

  Returns:
    The InitLegacyRequestOsEnviron Middleware.
  """




  original_environ = dict(os.environ)


  request_environment.PatchOsEnviron()


  os.environ.update(original_environ)

  @middleware
  def InitLegacyRequestOsEnvironMiddleware(app, wsgi_env, start_response):
    """The middleware WSGI app."""







    request_environment.current_request.Init(
        errors=None,
        environ=original_environ.copy())

    return app(wsgi_env, start_response)

  return InitLegacyRequestOsEnvironMiddleware


@middleware
def LegacyCopyWsgiEnvToOsEnvMiddleware(app, wsgi_env, start_response):
  """Copy WSGI variables to os.environ.

  When the wrapped inner function (i.e. the WSGI middleware) is called, we copy
  WSGI environment variables to os.environ. As a precondition, we assume
  os.environ has already been patched to be request-specific.

  Args:
    app: The WSGI app to wrap.
    wsgi_env: see PEP 3333
    start_response: see PEP 3333

  Returns:
    The wrapped app, also a WSGI app.
  """

  assert isinstance(os.environ, request_environment.RequestLocalEnviron)
  for key, val in six.iteritems(wsgi_env):
    if isinstance(val, six.string_types):
      os.environ[key] = val
  return app(wsgi_env, start_response)


@middleware
def CallbackMiddleware(app, wsgi_env, start_response):
  """Calls the request-end callback that the app may have set."""
  try:
    return app(wsgi_env, start_response)
  finally:
    callback.InvokeCallbacks()


@middleware
def RunInNewContextMiddleware(app, wsgi_env, start_response):
  """Runs the app in a copy of the current context.

  Start every request by calling contextvars.copy_context() and running the
  rest of the request in the newly copied context. This ensures that
  each request has its own context that is isolated from all other requests.

  In other words, this "scopes" all ContextVars to the current request.

  Args:
    app: the WSGI app to wrap
    wsgi_env: see PEP 3333
    start_response: see PEP 3333
  Returns:
    The wrapped WSGI app
  """
  ctx = contextvars.copy_context()
  return ctx.run(app, wsgi_env, start_response)



WARMUP_IP = '0.1.0.3'


@middleware
def BackgroundAndShutdownMiddleware(app, wsgi_env, start_response):
  path = wsgi_env['PATH_INFO']
  if (path == '/_ah/background' and wsgi_env.get('REMOTE_ADDR') == WARMUP_IP):
    return background.App(wsgi_env, start_response)
  elif (path == '/_ah/stop' and wsgi_env.get('REMOTE_ADDR') == WARMUP_IP):
    runtime.__BeginShutdown()
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'ok']
  return app(wsgi_env, start_response)


@middleware
def AddDeferredMiddleware(app, wsgi_env, start_response):
  """Intercept calls to the default endpoint for Deferred.

  Handle requests made to /_ah/queue/deferred

  Args:
    app: the WSGI app to wrap
    wsgi_env: see PEP 3333
    start_response: see PEP 3333
  Returns:
    The wrapped WSGI app response in UTF-8 format
  """
  path = wsgi_env['PATH_INFO']
  if path == '/_ah/queue/deferred':
    return deferred.application(wsgi_env, start_response)
  return app(wsgi_env, start_response)


@middleware
def SetNamespaceFromHeader(app, wsgi_env, start_response):
  ns_from_header = wsgi_env.get('HTTP_X_APPENGINE_CURRENT_NAMESPACE')
  if ns_from_header is not None:
    namespace_manager.set_namespace(ns_from_header)
  return app(wsgi_env, start_response)
