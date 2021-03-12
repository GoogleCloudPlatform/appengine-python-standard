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

  import google.appengine.api

  app = google.appengine.api.wrap_wsgi_app(app)

Example for a Flask app:

  import google.appengine.api
  from flask import Flask, request

  app = Flask(__name__)
  app.wsgi_app = google.appengine.api.wrap_wsgi_app(app.wsgi_app)

"""


def wrap_wsgi_app(app):
  """Wrap a WSGI app with middlewares required to access App Engine APIs."""

  from google.appengine.ext.vmruntime import middlewares
  from google.appengine.ext.vmruntime import vmstub

  vmstub.Register(vmstub.VMStub())

  app = middlewares.ErrorLoggingMiddleware(app)
  app = middlewares.OsEnvSetupMiddleware(app)

  class FakeAppinfoExternal:
    """As we don't have an app.yaml to parse, just assume threadsafe."""
    threadsafe = True

  app = middlewares.WsgiEnvSettingMiddleware(app, FakeAppinfoExternal)
  app = middlewares.WaitForResponseMiddleware(app)
  app = middlewares.UseRequestSecurityTicketForApiMiddleware(app)
  app = middlewares.CallbackMiddleware(app)





  app = middlewares.InitRequestEnvironMiddleware(app, copy_gae_application=True)

  return app
