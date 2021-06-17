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
"""Minimal library for communicating with the metadata server.

Branched from
http://google/third_party/py/google/auth/compute_engine/_metadata.py
and enhanced to support explicit oauth2 scopes.
"""



import os
import time
from typing import List, Optional, Text, Tuple

import frozendict
import requests

_METADATA_ROOT = 'http://{}/computeMetadata/v1/'.format(
    os.getenv('GCE_METADATA_HOST', 'metadata.google.internal'))

_METADATA_HEADERS = frozendict.frozendict({'metadata-flavor': 'Google'})


class TransportError(Exception):
  """Metadata server response not 200 OK."""


def _get(path: Text, root: Text = _METADATA_ROOT, **kwargs):
  kwargs.setdefault('headers', _METADATA_HEADERS)
  url = root + path
  response = requests.get(url, **kwargs)
  if response.status_code != requests.codes.ok:
    raise TransportError(
        'Failed to retrieve {} from the metadata service. '
        'Status: {} Response:\n{}'.format(
            url, response.status_code, response.content))
  return response.json()


def get_service_account_token(
    scopes: List[Text],
    service_account: Optional[Text] = None) -> Tuple[Text, int]:
  """Get the OAuth 2.0 access token for a service account.

  Args:
      scopes: A list of scopes to be sent with the credentials.
      service_account: The string 'default' or a service account email
          address. The determines which service account for which to acquire
          an access token.

  Returns:
      The access token and its expiration in epoch time.

  Raises:
      TransportError: if an error occurred while
          retrieving metadata.
  """
  if service_account is None:
    service_account = 'default'

  token_json = _get(
      path='instance/service-accounts/{0}/token'.format(service_account),
      params={'scopes': ','.join(scopes)}
  )
  return token_json['access_token'], time.time()+token_json['expires_in']
