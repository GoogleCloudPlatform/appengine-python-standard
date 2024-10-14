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


N = 0x97746090905af40c6beecbfe8ac2b770f4855b6474091e1928a4b93e14ee636bc41b8e6806f10881a145b51eda9faebd117a319b4bbe853587da84168ff00150ce1cde161e1c3754b97f395bab79d45f7bc6c14e2d0aa9d81406b2abf15eb59f6e8ddc1e0c6bd7644cc6dc3830bf5c27cf2112674c87f8675be7a047d64042437d6f502c9172245d7b869a7d9794b5bae3090718d832c6771312ea48584cec86cdd4f0c101beb31ad23b6fd0153fe8314b58635e2268640df621620d01988f57ed24f76e5e72c574064234cd5e136b4e8525ec4dc74e34cb98afaf80b6d7819150cdd42a2862ad37043814b56bb4918b9c023e1ff04f403c80de8d35b4cd8dcd
MODULUS_BYTES = 256

E = 65537



D = 0x868f1ce4137cdb6ad5d1f96792fce061f8bd2aaf9af026cf8f6e9a2df006c44a1097b2f3f586dc59df60c1444254b0b8c5f85c6e6ee33c128d3ab5341e79cb91712df09a91f1dbaee88781fc51e311ae2b983052366e4cebef0eec5b1b3d5bfbe40b214f89159eee3bd04a039a3bc9b28cb20359c782de4d6637ea0d28eb3a72bfab74c0d7f9d64dacc825bc3f274adb78d0c17512e419760a6b47ba33b001f634ce3d2458635f3e30406a044c815804d53742555163459a1d5fb5be50e8f8bcb7609d52fb6a607e001aa97e3b5fe5bcf91a7aa94f9107b671d4ed5110d23793605f5bd3fc950cf525f1dd7df3cc459c103a08e5e426e13aee54aa813f605fb9
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
            side_effect=self.get_service_account_token)])

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
    response.service_account_name = self.get_service_account_name()

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

  def get_service_account_token(self, scopes, service_account=None):
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

  def get_service_account_name(self):
    return APP_SERVICE_ACCOUNT_NAME

  @staticmethod
  def Create(email_address=None, private_key_path=None, oauth_url=None):
    raise NotImplementedError(
        'Base class AppIdentityServiceStubBase doesn\'t implement '
        'Create(), use AppIdentityServiceStub instead.')

  def Clear(self):
    """Resets the state on the App Identity stub."""
    self.__default_gcs_bucket_name = APP_DEFAULT_GCS_BUCKET_NAME

stublib.Stub.register(AppIdentityServiceStubBase)
