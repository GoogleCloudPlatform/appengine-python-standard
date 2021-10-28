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
a private key specified when starting `dev_appserver.py`.
"""











import base64
import json
import os
import threading
import time

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


_DEFAULT_OAUTH_URL = 'https://accounts.google.com/o/oauth2/token'


def BitStringToByteString(bs):
  """Convert a pyasn1.type.univ.BitString object to a string of bytes."""
  def BitsToInt(bits):
    return sum(v * (2 ** (7 - j)) for j, v in enumerate(bits))
  return bytes(
      bytearray([BitsToInt(bs[i:i + 8]) for i in range(0, len(bs), 8)]))


class KeyBasedAppIdentityServiceStub(
    app_identity_stub_base.AppIdentityServiceStubBase):
  """A stub for the AppIdentityService API for offline development.

  Provides stub functions which allow a developer to test integration before
  deployment.
  """
  THREADSAFE = True

  def __init__(self, service_name='app_identity_service',
               email_address=None, private_key_path=None,
               oauth_url=None):
    """Constructor."""
    super(KeyBasedAppIdentityServiceStub, self).__init__(service_name)
    self.__x509_init_lock = threading.Lock()
    self.__access_token_cache_lock = threading.Lock()
    self.__default_gcs_bucket_name = (
        app_identity_stub_base.APP_DEFAULT_GCS_BUCKET_NAME)
    if email_address is None:
      raise ValueError('Email address for service account must be specified.')
    self.__email_address = email_address
    if private_key_path is None:
      raise ValueError('Path to the private key must be specified '
                       'if an email address is specified.')
    if not os.path.exists(private_key_path):
      raise ValueError(private_key_path + ' not found.')
    if private_key_path.endswith('.p12'):

      raise ValueError(('Please convert .p12 format to .pem format: '
                        'cat %s | openssl pkcs12 -nodes -nocerts -passin '
                        'pass:notasecret | openssl rsa > %s') % (
                            private_key_path,
                            '%s.pem' % os.path.splitext(private_key_path)[0]))
    self.__private_key = rsa.key.PrivateKey.load_pkcs1(
        open(private_key_path, 'rb').read(), 'PEM')
    self.__access_token_cache = {}
    self.__x509 = None
    self.__signing_key = None
    self.__oauth_url = oauth_url or _DEFAULT_OAUTH_URL

  def _PopulateX509(self):
    with self.__x509_init_lock:
      if not self.__x509:
        url = ('https://www.googleapis.com/service_accounts/v1/metadata/x509/%s'
               % urllib.parse.unquote_plus(self.__email_address))
        resp = urlfetch.fetch(
            url=url,
            validate_certificate=True,
            method=urlfetch.GET)
        if resp.status_code != 200:
          raise apiproxy_errors.ApplicationError(
              app_identity_service_pb2.AppIdentityServiceError.UNKNOWN_ERROR,
              'Unable to load X509 cert: %s Response code: %i, Content: %s' % (
                  url, resp.status_code, resp.content))

        msg = b'test'
        sig = rsa.pkcs1.sign(msg, self.__private_key, 'SHA-256')




        for signing_key, x509 in json.loads(resp.content).items():
          der = rsa.pem.load_pem(x509, 'CERTIFICATE')
          asn1_cert, _ = decoder.decode(der, asn1Spec=Certificate())

          key_bitstring = (
              asn1_cert['tbsCertificate']
              ['subjectPublicKeyInfo']
              ['subjectPublicKey'])
          key_bytearray = BitStringToByteString(key_bitstring)

          pub = rsa.PublicKey.load_pkcs1(key_bytearray, 'DER')
          try:
            if rsa.pkcs1.verify(msg, sig, pub):
              self.__x509 = x509
              self.__signing_key = signing_key
              return
          except rsa.pkcs1.VerificationError:
            pass


        raise apiproxy_errors.ApplicationError(
            app_identity_service_pb2.AppIdentityServiceError.UNKNOWN_ERROR,
            'Unable to find matching X509 cert for private key: %s' % url)

  def _Dynamic_SignForApp(self, request, response):
    """Implementation of AppIdentityService::SignForApp."""
    self._PopulateX509()
    response.signature_bytes = rsa.pkcs1.sign(
        request.bytes_to_sign, self.__private_key, 'SHA-256')
    response.key_name = self.__signing_key

  def _Dynamic_GetPublicCertificatesForApp(self, request, response):
    """Implementation of AppIdentityService::GetPublicCertificatesForApp."""
    self._PopulateX509()
    cert = response.public_certificate_list.add()
    cert.key_name = self.__signing_key
    cert.x509_certificate_pem = self.__x509

  def _Dynamic_GetServiceAccountName(self, request, response):
    """Implementation of AppIdentityService::GetServiceAccountName."""
    response.service_account_name = self.get_service_account_name()

  def _Dynamic_GetDefaultGcsBucketName(self, unused_request, response):
    """Implementation of AppIdentityService::GetDefaultGcsBucketName."""
    response.default_gcs_bucket_name = self.__default_gcs_bucket_name

  def SetDefaultGcsBucketName(self, default_gcs_bucket_name):
    if default_gcs_bucket_name:
      self.__default_gcs_bucket_name = default_gcs_bucket_name
    else:
      self.__default_gcs_bucket_name = (
          app_identity_stub_base.APP_DEFAULT_GCS_BUCKET_NAME)

  def get_service_account_token(self, scopes, service_account=None):
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
    with self.__access_token_cache_lock:
      rv = self.__access_token_cache.get(scope, None)
    now = int(time.time())



    if not (rv and rv['expires'] > (now + 60)):

      assertion_input = '%s.%s' % (
          base64.urlsafe_b64encode(json.dumps({
              'alg': 'RS256',
              'typ': 'JWT'
          }).encode('UTF-8')).decode('utf-8').rstrip('='),
          base64.urlsafe_b64encode(json.dumps({
              'iss': self.__email_address,
              'scope': scope,
              'aud': self.__oauth_url,
              'exp': now + (60 * 60),
              'iat': now
          }).encode('UTF-8')).decode('utf-8').rstrip('='))


      signature = base64.urlsafe_b64encode(rsa.pkcs1.sign(
          assertion_input.encode('utf-8'),
          self.__private_key, 'SHA-256')).decode('utf-8').rstrip('=')


      message = urllib.parse.urlencode({
          'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
          'assertion': '%s.%s' % (assertion_input, signature)
      })

      resp = urlfetch.fetch(
          url=self.__oauth_url,
          validate_certificate=True,
          payload=message,
          method=urlfetch.POST,
          headers={'Content-Type': 'application/x-www-form-urlencoded'})

      if resp.status_code != 200:
        raise RuntimeError('Error getting access token. '
                           'Response code: %i, Content: %s' % (
                               resp.status_code, resp.content))

      rv = json.loads(resp.content)


      rv['expires'] = now + int(rv.get('expires_in', '0'))
      with self.__access_token_cache_lock:
        self.__access_token_cache[scope] = rv

    return rv['access_token'], rv['expires']

  def get_service_account_name(self):
    return self.__email_address
