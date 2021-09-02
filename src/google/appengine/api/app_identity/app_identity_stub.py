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
"""App identity stub service implementation.

This service behaves the same as the production service, except using
constant values instead of app-specific values:
* Signing key is constant; in production this rotates.
* Public key is constant; in production this varies per app.
* Service account name is constant; in production this varies per app.
"""






import logging

from google.auth import exceptions

from google.appengine.api.app_identity import app_identity_defaultcredentialsbased_stub as ai_default_stub
from google.appengine.api.app_identity import app_identity_keybased_stub
from google.appengine.api.app_identity import app_identity_stub_base


APP_SERVICE_ACCOUNT_NAME = app_identity_stub_base.APP_SERVICE_ACCOUNT_NAME


class AppIdentityServiceStub(app_identity_stub_base.AppIdentityServiceStubBase):
  """A stub for the AppIdentityService API for offline development.

  Provides stub functions which allow a developer to test integration before
  deployment.

  Automatically creates appropriate stub (default credentials or key based)
  using `Create()`.
  """
  THREADSAFE = True

  @staticmethod
  def Create(email_address=None, private_key_path=None, oauth_url=None):
    if email_address:
      logging.debug('Using the KeyBasedAppIdentityServiceStub.')
      return app_identity_keybased_stub.KeyBasedAppIdentityServiceStub(
          email_address=email_address,
          private_key_path=private_key_path,
          oauth_url=oauth_url)
    else:
      try:
        dc = ai_default_stub.DefaultCredentialsBasedAppIdentityServiceStub()
        logging.debug('Successfully loaded Application Default Credentials.')
        return dc
      except exceptions.DefaultCredentialsError as error:
        if not str(error).startswith(
            'Could not automatically determine credentials.'):

          logging.warning('An exception has been encountered when attempting '
                          'to use Application Default Credentials: %s'
                          '. Falling back on dummy AppIdentityServiceStub.',
                          str(error))
        return AppIdentityServiceStub()
