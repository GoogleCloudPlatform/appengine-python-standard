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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import binascii
import logging
import logging.handlers
import os
import sys
import traceback

import six
from six.moves import urllib

from google.appengine.ext.vmruntime import callback
from google.appengine.ext.vmruntime import vmstub
from google.appengine.runtime import request_environment



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


X_APPENGINE_USER_IP_ENV_KEY = 'HTTP_X_APPENGINE_USER_IP'

WSGI_REMOTE_ADDR_ENV_KEY = 'REMOTE_ADDR'


def UseRequestSecurityTicketForApiMiddleware(app):
  """WSGI middleware wrapper that sets the thread to use the security ticket.

  This sets up the appengine api so that if a security ticket is passed in with
  the request, it will be used.

  Args:
    app: (callable) a WSGI app per PEP 333.

  Returns:
    A wrapped <app>, which is also a valid WSGI app.
  """

  def TicketWrapper(wsgi_env, start_response):
    try:
      vmstub.VMStub.SetUseRequestSecurityTicketForThread(True)
      return app(wsgi_env, start_response)
    finally:

      vmstub.VMStub.SetUseRequestSecurityTicketForThread(False)

  return TicketWrapper


def WaitForResponseMiddleware(app):
  """WSGI middleware wrapper that waits until response is ready.

  Some middlewares here and some external middlewares rely on behavior that app
  calls finish when response is ready and they do post-processing that should
  be done when handler has returned all response.
  This middleware added for compatibility with such middlewares,
  once all users migrated to Python3, all middlewares should use `yield app()`
  instead of `return app()` and this one should be removed.

  Args:
    app: (callable) a WSGI app per PEP 333.

  Returns:
    A wrapped <app>, which is also a valid WSGI app.
  """
  def Wrapper(wsgi_env, start_response):
    return list(app(wsgi_env, start_response))
  return Wrapper


def ErrorLoggingMiddleware(app):
  """Catch and log unhandled errors for the given app."""

  def ErrorLoggingWrapper(wsgi_env, start_response):
    """Wrap the application into an error handler."""
    try:
      return app(wsgi_env, start_response)
    except:








      log_message = traceback.format_exception(
          sys.exc_info()[0],
          sys.exc_info()[1],
          sys.exc_info()[2])

      logging.error(''.join(log_message))
      raise

  return ErrorLoggingWrapper


def _MakeRequestIdHash(log_id):
  """Invent a REQUEST_ID_HASH to replace the one the python27g runtime had."""









  request_id_hash = binascii.crc32(six.ensure_binary(log_id))
  request_id_hash &= 0xffffffff
  request_id_hash_hex = '%08X' % request_id_hash
  return request_id_hash_hex


def WsgiEnvSettingMiddleware(app, appinfo_external):
  """Modify the wsgi env variable according to this application."""




  def SetWsgiEnv(wsgi_env, start_response):
    """The middleware WSGI app."""



    for key in LOCAL_OVERRIDABLE_VARS:
      val = os.environ.get(key)
      if val:
        wsgi_env['HTTP_X_APPENGINE_' + key] = val


    wsgi_env.setdefault('HTTP_X_APPENGINE_AUTH_DOMAIN', 'gmail.com')
    wsgi_env.setdefault('HTTP_X_APPENGINE_USER_IS_ADMIN', '0')

    log_id = wsgi_env.get('HTTP_X_APPENGINE_REQUEST_LOG_ID')
    if log_id:
      wsgi_env['HTTP_X_APPENGINE_REQUEST_ID_HASH'] = _MakeRequestIdHash(log_id)


    for key in ENV_VARS_FROM_HTTP_X_APPENGINE_HEADERS:
      value = wsgi_env.get('HTTP_X_APPENGINE_' + key)
      if value:
        wsgi_env[key] = value




    wsgi_env['CLOUD_TRACE_ENABLE_STACK_TRACE'] = ''
    if 'GAE_RUNTIME' in os.environ:
      wsgi_env['GAE_RUNTIME'] = os.environ['GAE_RUNTIME']
    wsgi_env['wsgi.multithread'] = appinfo_external.threadsafe










    protocol = wsgi_env.get('HTTP_X_FORWARDED_PROTO')
    if protocol:
      wsgi_env['wsgi.url_scheme'] = protocol

      if protocol == 'http':
        wsgi_env['SERVER_PORT'] = '80'
      elif protocol == 'https':
        wsgi_env['SERVER_PORT'] = '443'
      else:
        logging.warning('Unrecognized value for HTTP_X_FORWARDED_PROTO (%s)'
                        ", won't modify SERVER_PORT", protocol)

    http_host = wsgi_env.get('HTTP_HOST')
    if http_host:
      server_name = urllib.parse.urlparse('//' + http_host).hostname
      wsgi_env['SERVER_NAME'] = server_name



    user_ip = wsgi_env.get(X_APPENGINE_USER_IP_ENV_KEY)
    if user_ip:
      wsgi_env[WSGI_REMOTE_ADDR_ENV_KEY] = user_ip

    return app(wsgi_env, start_response)

  return SetWsgiEnv


def InitRequestEnvironMiddleware(app, copy_gae_application=False):
  """Patch os.environ to be thread local, and stamp it with default values.

  When this function is called, we remember the values of os.environ. When the
  wrapped inner function (i.e. the WSGI middleware) is called, we patch
  os.environ to be thread local, and we fill in the remembered values, and merge
  in WSGI env vars.

  Args:
    app: The WSGI app to wrap.
    copy_gae_application: GAE_APPLICATION is copied to APPLICATION_ID if set.

  Returns:
    The wrapped app, also a WSGI app.
  """


  if copy_gae_application:
    os.environ['APPLICATION_ID'] = os.environ['GAE_APPLICATION']




  original_environ = dict(os.environ)


  request_environment.PatchOsEnviron()


  os.environ.update(original_environ)

  def PatchEnv(wsgi_env, start_response):
    """The middleware WSGI app."""







    request_environment.current_request.Init(
        errors=None,
        environ=original_environ.copy())

    return app(wsgi_env, start_response)

  return PatchEnv


def OsEnvSetupMiddleware(app):
  """Copy WSGI variables to os.environ.

  When the wrapped inner function (i.e. the WSGI middleware) is called, we copy
  WSGI environment variables to os.environ. As a precondition, we assume
  os.environ has already been patched to be request-specific.

  Args:
    app: The WSGI app to wrap.

  Returns:
    The wrapped app, also a WSGI app.
  """

  def CopyWsgiToEnv(wsgi_env, start_response):
    """The middleware WSGI app."""
    for key, val in six.iteritems(wsgi_env):
      if isinstance(val, six.string_types):
        os.environ[key] = val

    return app(wsgi_env, start_response)

  return CopyWsgiToEnv


def CallbackMiddleware(app):
  """Calls the request-end callback that the app may have set."""

  def CallbackWrapper(wsgi_env, start_response):
    """Calls the WSGI app and the invokes the request-end callback."""
    try:
      return app(wsgi_env, start_response)
    finally:
      callback.InvokeCallbacks()

  return CallbackWrapper
