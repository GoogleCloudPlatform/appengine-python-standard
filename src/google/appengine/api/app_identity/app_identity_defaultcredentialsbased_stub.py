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
application default credentials.
"""

import datetime
import json
import threading
import time
import typing

from pyasn1.codec.der import decoder
from pyasn1_modules.rfc2459 import Certificate
import rsa
import six
from six.moves import range
from six.moves import urllib

from google.appengine.api import urlfetch
from google.appengine.api.app_identity import app_identity_service_pb2
from google.appengine.api.app_identity import app_identity_stub_base
from google.appengine.runtime import apiproxy_errors

from google import auth as google_auth
from google.auth import app_engine
from google.auth import credentials as ga_credentials
from google.auth import exceptions
from google.auth.transport import requests as transport
from google.oauth2 import service_account as oauth2_service_account


def BitStringToByteString(bs):
  """Convert a pyasn1.type.univ.BitString object to a string of bytes."""
  def BitsToInt(bits):
    return sum(v * (2 ** (7 - j)) for j, v in enumerate(bits))
  return bytes(
      bytearray([BitsToInt(bs[i:i + 8]) for i in range(0, len(bs), 8)]))


class DefaultCredentialsBasedAppIdentityServiceStub(
    app_identity_stub_base.AppIdentityServiceStubBase):
  """A stub for the AppIdentityService API for offline development.

  Provides stub functions which allow a developer to test integration before
  deployment.
  """

  THREADSAFE = True

  _credentials = None

  def __init__(self, service_name='app_identity_service'):
    super(DefaultCredentialsBasedAppIdentityServiceStub,
          self).__init__(service_name)
    self._credentials, _ = google_auth.default()
    if isinstance(self._credentials, app_engine.Credentials):



      raise exceptions.DefaultCredentialsError(
          'Could not automatically determine credentials.')
    self._access_token_cache_lock = threading.Lock()
    self._access_token_cache = {}
    self._x509_init_lock = threading.Lock()
    self._default_gcs_bucket_name = (
        app_identity_stub_base.APP_DEFAULT_GCS_BUCKET_NAME)
    self._x509 = None
    self._signing_key = None
    self._non_service_account_credentials = not isinstance(
        self._credentials, oauth2_service_account.Credentials)

  def _PopulateX509(self):
    with self._x509_init_lock:
      if self._x509 is None:

        url = ('https://www.googleapis.com/service_accounts/v1/metadata/x509/%s'
               % urllib.parse.unquote_plus(
                   self._credentials.service_account_email))
        response = urlfetch.fetch(
            url=url,
            validate_certificate=True,
            method=urlfetch.GET)
        if response.status_code != 200:
          raise apiproxy_errors.ApplicationError(
              app_identity_service_pb2.AppIdentityServiceError.UNKNOWN_ERROR,
              'Unable to load X509 cert: %s Response code: %i, Content: %s' % (
                  url, response.status_code, response.content))

        message = b'dummy'
        signature = self._credentials.sign_bytes(message)

        for signing_key, x509 in json.loads(response.content).items():
          der = rsa.pem.load_pem(x509, 'CERTIFICATE')
          asn1_cert, _ = decoder.decode(der, asn1Spec=Certificate())

          key_bitstring = (
              asn1_cert['tbsCertificate']
              ['subjectPublicKeyInfo']
              ['subjectPublicKey'])
          key_bytearray = BitStringToByteString(key_bitstring)

          public_key = rsa.PublicKey.load_pkcs1(key_bytearray, 'DER')
          try:
            if rsa.pkcs1.verify(message, signature, public_key):
              self._x509 = x509
              self._signing_key = signing_key
              return
          except rsa.pkcs1.VerificationError:
            pass

        raise apiproxy_errors.ApplicationError(
            app_identity_service_pb2.AppIdentityServiceError.UNKNOWN_ERROR,
            'Unable to find matching X509 cert for private key: %s' % url)

  def _Dynamic_SignForApp(self, request, response):
    """Implementation of AppIdentityService::SignForApp."""
    if self._non_service_account_credentials:




      return super(DefaultCredentialsBasedAppIdentityServiceStub,
                   self)._Dynamic_SignForApp(request, response)
    self._PopulateX509()
    signature = self._credentials.sign_bytes(
        request.bytes_to_sign)
    private_key_id = self._credentials.signer.key_id
    assert private_key_id == self._signing_key
    response.signature_bytes = signature
    response.key_name = self._signing_key

  def _Dynamic_GetPublicCertificatesForApp(self, request, response):
    """Implementation of AppIdentityService::GetPublicCertificatesForApp."""
    if self._non_service_account_credentials:




      return super(DefaultCredentialsBasedAppIdentityServiceStub,
                   self)._Dynamic_GetPublicCertificatesForApp(request, response)
    self._PopulateX509()
    certificate = response.public_certificate_list.add()
    certificate.key_name = self._signing_key
    certificate.x509_certificate_pem = self._x509

  def _Dynamic_GetServiceAccountName(self, request, response):
    """Implementation of AppIdentityService::GetServiceAccountName."""
    if self._non_service_account_credentials:


      response.service_account_name = ''
    else:
      response.service_account_name = self._credentials.service_account_email

  def _Dynamic_GetDefaultGcsBucketName(self, unused_request, response):
    """Implementation of AppIdentityService::GetDefaultGcsBucketName."""
    response.default_gcs_bucket_name = self._default_gcs_bucket_name

  def SetDefaultGcsBucketName(self, default_gcs_bucket_name):
    if default_gcs_bucket_name:
      self._default_gcs_bucket_name = default_gcs_bucket_name
    else:
      self._default_gcs_bucket_name = (
          app_identity_stub_base.APP_DEFAULT_GCS_BUCKET_NAME)

  def _patch_get_service_account_token(self, scopes, service_account=None):
    """Implementation of AppIdentityService::GetAccessToken.

    This API requires internet access.

    Args:
      scopes: a list of oauth2 scopes.
      service_account: the service account to get the token for

    Returns:
      Tuple of access token and expiration time in epoch

    Raises:
      RuntimeError: If unexpected response from Google server.
    """
    scope = ' '.join(scopes)
    with self._access_token_cache_lock:
      rv = self._access_token_cache.get(scope, None)

    if not (rv and rv['expires'] > (time.time() + 60)):
      credentials = self._credentials
      if (isinstance(credentials, ga_credentials.Scoped) and
          credentials.requires_scopes):
        credentials = credentials.with_scopes(scopes)
      if not credentials.valid:
        credentials.refresh(transport.Request())

      expiration = 0
      if credentials.expiry:
        expiration = TimestampFromNaiveUtcDatetime(credentials.expiry)
      rv = {
          'access_token': credentials.token,
          'expires': expiration,
      }
      with self._access_token_cache_lock:
        self._access_token_cache[scope] = rv

    return rv['access_token'], rv['expires']


def TimestampFromNaiveUtcDatetime(dt):
  if dt.tzinfo is not None:
    raise ValueError('Expected a naive UTC datetime')
  if six.PY2:
    return (dt - datetime.datetime(1970, 1, 1)).total_seconds()

  return dt.replace(tzinfo=datetime.timezone.utc).timestamp()
