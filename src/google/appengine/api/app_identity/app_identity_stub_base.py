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
"""Base class and constants for app identity stubs.

The module offers following objects available for app identity stubs:

Constants:
  RSA_LIB_INSTALLED: boolean, pure-Python crypto enabled/disabled.
  CRYPTO_LIB_INSTALLED: boolean, C crypto enabled/disabled.
  APP_SERVICE_ACCOUNT_NAME: service account hardcoded in the stubs.
  APP_DEFAULT_GCS_BUCKET_NAME: GCS bucket hardcoded in the stubs.
  X509_PUBLIC_CERT: public certificate hardcoded in the stubs.

Classes:
  AppIdentityServiceStubBase: base for app identity stub.

"""







import time

import mock
import rsa

from google.appengine.api import apiproxy_stub
from google.appengine.api import stublib


APP_SERVICE_ACCOUNT_NAME = 'test@localhost'
APP_DEFAULT_GCS_BUCKET_NAME = 'app_default_bucket'

SIGNING_KEY_NAME = 'key'


N = 19119371788959611760073322421014045870056498252163411380847152703712917776733759011400972099255719579701566470175077491500050513917658074590935646529525468755348555932670175295728802986097707368373781743941167574738113348515272061138933984990014969297930973127363812200790406743271047572192133912023914306041356562363557723417403707408838823620411045628159183655215061768071407845537324145892973481372872161981015237572556138317222082306397041309823528068650373958169977675424007883635551170458356632131122901683151395297447872184074888239102348331222079943386530179883880518236689216575776729057173406091195993394637
MODULUS_BYTES = 256

E = 65537

D = 16986504444572720056487621821047100642841595850137583213470349776864799280835251113078612103869013355016302383270733509621770011190160658118800356360958694229960556902751935956316359959542321272425222634888969943798180994410031448370776358545990991384123912313866752051562052322103544805811361355593091450379904792608637886965065110019212136239200637553477192566763015004249754677600683846556806159369233241157779976231822757855748068765507787598014034587835400718727569389998321277712761796543890788269130617890866139616903097422259980026836628018133574943835504630997228592718738382001678104796538128020421537193913
X509_PUBLIC_CERT = """
-----BEGIN CERTIFICATE-----
MIIC/jCCAeagAwIBAgIIQTBFcRw3moMwDQYJKoZIhvcNAQEFBQAwIjEgMB4GA1UE
AxMXcm9ib3RqYXZhLmEuYXBwc3BvdC5jb20wHhcNMTEwMjIzMTUwNzQ5WhcNMTEw
MjI0MTYwNzQ5WjAiMSAwHgYDVQQDExdyb2JvdGphdmEuYS5hcHBzcG90LmNvbTCC
ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJd0YJCQWvQMa+7L/orCt3D0
hVtkdAkeGSikuT4U7mNrxBuOaAbxCIGhRbUe2p+uvRF6MZtLvoU1h9qEFo/wAVDO
HN4WHhw3VLl/OVuredRfe8bBTi0KqdgUBrKr8V61n26N3B4Ma9dkTMbcODC/XCfP
IRJnTIf4Z1vnoEfWQEJDfW9QLJFyJF17hpp9l5S1uuMJBxjYMsZ3ExLqSFhM7IbN
1PDBAb6zGtI7b9AVP+gxS1hjXiJoZA32IWINAZiPV+0k925ecsV0BkI0zV4Ta06F
JexNx040y5ivr4C214GRUM3UKihirTcEOBS1a7SRi5wCPh/wT0A8gN6NNbTNjc0C
AwEAAaM4MDYwDAYDVR0TAQH/BAIwADAOBgNVHQ8BAf8EBAMCB4AwFgYDVR0lAQH/
BAwwCgYIKwYBBQUHAwIwDQYJKoZIhvcNAQEFBQADggEBAD+h2D+XGIHWMwPCA2DN
JgMhN1yTTJ8dtwbiQIhfy8xjOJbrzZaSEX8g2gDm50qaEl5TYHHr2zvAI1UMWdR4
nx9TN7I9u3GoOcQsmn9TaOKkBDpMv8sPtFBal3AR5PwR5Sq8/4L/M22LX/TN0eIF
Y4LnkW+X/h442N8a1oXn05UYtFo+p/6emZb1S84WZAnONGtF5D1Z6HuX4ikDI5m+
iZbwm47mLkV8yuTZGKI1gJsWmAsElPkoWVy2X0t69ecBOYyn3wMmQhkLk2+7lLlD
/c4kygP/941fe1Wb/T9yGeBXFwEvJ4jWbX93Q4Xhk9UgHlso9xkCu9QeWFvJqufR
5Cc=
-----END CERTIFICATE-----
"""


PREFIX = '3031300d060960864801650304020105000420'
LEN_OF_PREFIX = 19
HEADER1 = '0001'
HEADER2 = '00'
PADDING = 'ff'


LENGTH_OF_SHA256_HASH = 32


class AppIdentityServiceStubBase(apiproxy_stub.APIProxyStub):
  """A base class for the AppIdentityService API stub.

  Offers base implementations for following AppIdentityService RPCs:

   * AppIdentityService::SignForApp ->
       _Dynamic_SignForApp
   * AppIdentityService::GetPublicCertificatesForApp ->
       _Dynamic_GetPublicCertificatesForApp
   * AppIdentityService::GetServiceAccountName ->
       _Dynamic_GetServiceAccountName
   * AppIdentityService::GetDefaultGcsBucketName ->
       _Dynamic_GetDefaultGcsBucketName
   * AppIdentityStubService::SetDefaultGcsBucketName ->
       _Dynamic_SetDefaultGcsBucketName
   * AppIdentityService::GetAccessToken ->
       _Dynamic_GetAccessToken

  And provides following helpers:
    * SetDefaultGcsBucketName: set default bucket name from the request if
                               possible, set from `APP_DEFAULT_GCS_BUCKET_NAME`
                               constant otherwise.
    * Clear: Reset state of the stub.

  Not implemented and must be implemented in an inherited class:
    * Create: static method, create a stub.
  """
  THREADSAFE = True

  def __init__(self, service_name='app_identity_service'):
    """Constructor."""
    super(AppIdentityServiceStubBase, self).__init__(service_name)
    self.__default_gcs_bucket_name = APP_DEFAULT_GCS_BUCKET_NAME
    self.patchers = stublib.Patchers([
        mock.patch(
            'google.appengine.api.app_identity._metadata_server.'
            'get_service_account_token',
            side_effect=self._patch_get_service_account_token)])

  def _Dynamic_SignForApp(self, request, response):
    """Implementation of AppIdentityService::SignForApp."""
    bytes_to_sign = request.bytes_to_sign
    signature_bytes = rsa.pkcs1.sign(
        bytes_to_sign,
        rsa.key.PrivateKey(N, E, D, 3, 5),
        'SHA-256')
    response.signature_bytes = signature_bytes
    response.key_name = SIGNING_KEY_NAME

  def _Dynamic_GetPublicCertificatesForApp(self, request, response):
    """Implementation of AppIdentityService::GetPublicCertificatesForApp."""
    cert = response.public_certificate_list.add()
    cert.key_name = SIGNING_KEY_NAME
    cert.x509_certificate_pem = X509_PUBLIC_CERT

  def _Dynamic_GetServiceAccountName(self, request, response):
    """Implementation of AppIdentityService::GetServiceAccountName."""
    response.service_account_name = APP_SERVICE_ACCOUNT_NAME

  def _Dynamic_GetDefaultGcsBucketName(self, unused_request, response):
    """Implementation of AppIdentityService::GetDefaultGcsBucketName."""
    response.default_gcs_bucket_name = self.__default_gcs_bucket_name

  def _Dynamic_SetDefaultGcsBucketName(self, request, unused_response):
    """Implementation of AppIdentityStubService::SetDefaultGcsBucketName."""
    self.SetDefaultGcsBucketName(request.default_gcs_bucket_name)

  def SetDefaultGcsBucketName(self, default_gcs_bucket_name):
    if default_gcs_bucket_name:
      self.__default_gcs_bucket_name = default_gcs_bucket_name
    else:
      self.__default_gcs_bucket_name = APP_DEFAULT_GCS_BUCKET_NAME

  def _patch_get_service_account_token(self, scopes, service_account=None):
    """test implementation for _metadata_server.get_service_account_token.

    This API returns an invalid token, as the `dev_appserver` does not have
    access to an actual service account.  Subclasses override this function with
    more useful implementations.

    Args:
      scopes: a list of oauth2 scopes.
      service_account: the service account to get the token for

    Returns:
      Tuple of access token and expiration time in epoch
    """
    token = ':'.join(scopes)
    if service_account:
      token += '.%s' % service_account
    access_token = 'InvalidToken:%s:%s' % (token, time.time() % 100)

    expiration_time = int(time.time()) + 1800
    return access_token, expiration_time

  @staticmethod
  def Create(email_address=None, private_key_path=None, oauth_url=None):
    raise NotImplementedError(
        'Base class AppIdentityServiceStubBase doesn\'t implement '
        'Create(), use AppIdentityServiceStub instead.')

  def Clear(self):
    """Resets the state on the App Identity stub."""
    self.__default_gcs_bucket_name = APP_DEFAULT_GCS_BUCKET_NAME

stublib.Stub.register(AppIdentityServiceStubBase)
