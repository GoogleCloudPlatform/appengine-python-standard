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


"""Tests for the download handler in google.appengine.ext.blobstore."""

import datetime

from google.appengine.ext.blobstore import blobstore
from absl.testing import absltest


class SendBlobContentDispositionTest(absltest.TestCase):
  """Tests the Content-Disposition header set by send_blob."""

  def setUp(self):
    super().setUp()
    self.handler = blobstore.BlobstoreDownloadHandler()

  def _create_blob_info(self, filename):
    return blobstore.BlobInfo(
        blobstore.BlobKey('my blob'),
        {
            'filename': filename,
            'content_type': b'application/pdf',
            'size': 1024,
            'creation': datetime.datetime(2009, 1, 2, 3, 4, 5),
        },
    )

  def _send_blob(self, blob_key_or_info, save_as):
    headers = self.handler.send_blob({}, blob_key_or_info, save_as=save_as)
    return headers['Content-Disposition']

  def test_bytes_filename(self):
    self.assertEqual(
        b'attachment; filename="alternate.txt"',
        self._send_blob('my blob', b'alternate.txt'),
    )

  def test_text_filename(self):
    self.assertEqual(
        b'attachment; filename="alternate.txt"; '
        b"filename*=utf-8''alternate.txt",
        self._send_blob('my blob', 'alternate.txt'),
    )

  def test_non_ascii_uploaded_filename(self):
    self.assertEqual(
        b'attachment; filename="\xe2\x82\xac rates";'
        b" filename*=utf-8''%E2%82%AC%20rates",
        self._send_blob(self._create_blob_info('\u20ac rates'), True),
    )

  def test_double_quote_is_replaced(self):
    self.assertEqual(
        b'attachment; filename="a_; filename=_evil.exe"',
        self._send_blob('my blob', b'a"; filename="evil.exe'),
    )

  def test_backslash_is_replaced(self):
    self.assertEqual(
        b'attachment; filename="a_b.txt"',
        self._send_blob('my blob', b'a\\b.txt'),
    )

  def test_backslash_and_double_quote_are_replaced(self):
    self.assertEqual(
        b'attachment; filename="a__b"',
        self._send_blob('my blob', b'a\\"b'),
    )

  def test_text_filename_keeps_backslash_in_extended_parameter(self):
    self.assertEqual(
        b"attachment; filename=\"a_b\"; filename*=utf-8''a%5Cb",
        self._send_blob('my blob', 'a\\b'),
    )

  def test_slash_is_encoded_in_extended_parameter(self):
    self.assertEqual(
        b'attachment; filename="dir/file.txt"; '
        b"filename*=utf-8''dir%2Ffile.txt",
        self._send_blob('my blob', 'dir/file.txt'),
    )

  def test_control_characters_removed_from_text_filename(self):
    self.assertEqual(
        b'attachment; filename="a_Set-Cookie: x=1"; '
        b"filename*=utf-8''a%22Set-Cookie%3A%20x%3D1",
        self._send_blob('my blob', 'a"\r\n\x00\t\x7f\x85Set-Cookie: x=1'),
    )

  def test_control_characters_removed_from_uploaded_filename(self):
    self.assertEqual(
        b'attachment; filename="x_Location: evil"',
        self._send_blob(
            self._create_blob_info(b'x"\r\nLocation: evil'), True
        ),
    )

  def test_no_filename_when_only_control_characters(self):
    self.assertEqual(b'attachment', self._send_blob('my blob', '\r\n'))


if __name__ == '__main__':
  absltest.main()
