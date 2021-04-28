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

"""Tests for google.third_party.py.google.appengine.api.app_identity._metadata_server."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import freezegun
import mock
import requests_mock

from google.appengine.api.app_identity import _metadata_server

from absl.testing import absltest


class MetadataServerTest(absltest.TestCase):

  @freezegun.freeze_time('2000-01-01')
  @mock.patch.object(_metadata_server, '_get',
                     return_value={
                         'expires_in': 42,
                         'access_token': 'mostly harmless'
                     })
  def test_get_service_account_token(self, mock_get):
    token, expiry = _metadata_server.get_service_account_token(
        scopes=['scope1', 'scope2'])
    with self.subTest(name='get method called'):
      mock_get.assert_called_with(
          path='instance/service-accounts/default/token',
          params={'scopes': 'scope1,scope2'})

    with self.subTest(name='check token'):
      self.assertEqual(token, 'mostly harmless')

    with self.subTest(name='check expiry'):
      self.assertEqual(expiry, time.time() + 42)

  @requests_mock.Mocker()
  def test_get(self, mock_requests):
    mock_requests.get(url=requests_mock.ANY,
                      json={'expires_in': 42,
                            'access_token': 'mostly harmless'})
    resp = _metadata_server._get('foo', params={'bar': 'baz'})
    self.assertEqual(resp,
                     {'expires_in': 42, 'access_token': 'mostly harmless'})
    self.assertEqual(
        mock_requests.last_request.url,
        'http://metadata.google.internal/computeMetadata/v1/foo?bar=baz')

  @requests_mock.Mocker()
  def test_get_fail(self, mock_requests):
    mock_requests.get(url=requests_mock.ANY,
                      status_code=404)
    with self.assertRaises(_metadata_server.TransportError):
      _metadata_server._get('foo', params={'bar': 'baz'})


if __name__ == '__main__':
  absltest.main()
