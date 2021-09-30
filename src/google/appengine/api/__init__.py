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
"""Helper for users of the public App Engine SDK.

This is for use as part of the code at:
https://github.com/GoogleCloudPlatform/appengine-python-standard

Example for a standard WSGI app:

  ```python
  import google.appengine.api

  app = google.appengine.api.wrap_wsgi_app(app)
  ```

Example for a Flask app:

  ```python
  import google.appengine.api
  from flask import Flask, request

  app = Flask(__name__)
  app.wsgi_app = google.appengine.api.wrap_wsgi_app(app.wsgi_app)
  ```
"""
import os
from google.appengine.api import full_app_id




def wrap_wsgi_app(app, use_legacy_context_mode=True, use_deferred=False):
  """Wrap a WSGI app with middlewares required to access App Engine APIs."""


  from google.appengine.runtime import initialize
  from google.appengine.runtime import middlewares
  from google.appengine.runtime import default_api_stub




  initialize.InitializeThreadingApis()

  default_api_stub.Register(default_api_stub.DefaultApiStub())



  full_app_id.normalize()

  def if_legacy(array):
    return array if use_legacy_context_mode else []

  def if_deferred_enabled(array):
    return array if use_deferred else []

  return middlewares.Wrap(
      app,
      if_legacy([
          middlewares.MakeInitLegacyRequestOsEnvironMiddleware(),
      ]) + [
          middlewares.RunInNewContextMiddleware,
          middlewares.SetContextFromHeadersMiddleware,
          middlewares.CallbackMiddleware,
          middlewares.UseRequestSecurityTicketForApiMiddleware,
          middlewares.WaitForResponseMiddleware,
          middlewares.WsgiEnvSettingMiddleware,

          middlewares.MakeLegacyWsgiEnvSettingMiddleware(),
      ] + if_legacy([
          middlewares.LegacyWsgiRemoveXAppenginePrefixMiddleware,
          middlewares.LegacyCopyWsgiEnvToOsEnvMiddleware,
      ]) + [
          middlewares.ErrorLoggingMiddleware,
          middlewares.BackgroundAndShutdownMiddleware,
          middlewares.SetNamespaceFromHeader,
      ] + if_deferred_enabled([
          middlewares.AddDeferredMiddleware,
      ]))
