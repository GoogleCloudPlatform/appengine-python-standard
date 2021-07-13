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


"""Tests for Datastore abstraction library."""




import datetime

from google.appengine.api import module_testutil
from google.appengine.api.blobstore import blobstore
from google.appengine.api.blobstore import blobstore_service_pb2
from google.appengine.runtime import apiproxy_errors
from absl.testing import absltest


def call_with_error(error, message):
  def make_sync_call(service, method, request, response):
    raise apiproxy_errors.ApplicationError(error, message)
  return make_sync_call


class ModuleInterfaceTest(module_testutil.ModuleInterfaceTest,
                          absltest.TestCase):

  MODULE = blobstore


class MockRPC(object):
  """Mock UserRPC class."""

  def __init__(self, side_effect=None, error=None, message=None):
    self._side_effect = side_effect
    self._error = error
    self._message = message

  def check_success(self):
    if self._side_effect is not None:
      self._side_effect(self)
    if self._error is not None:
      raise apiproxy_errors.ApplicationError(self._error, self._message)

  def get_result(self):
    if self._hook is None:
      self.check_success()
      return self.response
    else:

      return self._hook(self)

  def make_call(self, method, request, response,
                get_result_hook=None, user_data=None):
    self.method = method
    self.request = request
    self.response = response
    self._hook = get_result_hook
    self.user_data = user_data


class APIFunctionTest(absltest.TestCase):

  def testCreateUploadURL(self):
    request = blobstore_service_pb2.CreateUploadURLRequest()
    request.success_path = '/success_path'
    request.max_upload_size_per_blob_bytes = 1024
    request.max_upload_size_bytes = 1024 * 10
    request.gs_bucket_name = 'bucket'

    def side_effect(rpc):
      rpc.response.url = 'go here to post data'

    rpc = MockRPC(side_effect)

    self.assertEqual(
        'go here to post data',
        blobstore.create_upload_url(
            '/success_path',
            max_bytes_per_blob=1024,
            max_bytes_total=1024 * 10,
            gs_bucket_name='bucket',
            rpc=rpc))

  def testCreateUploadURLBadArguments(self):
    self.assertRaises(TypeError,
                      blobstore.create_upload_url,
                      '/foo',
                      'param1')

  def testCreateUploadURLUploadSizes(self):
    self.assertRaises(ValueError,
                      blobstore.create_upload_url,
                      '/foo',
                      max_bytes_total=1,
                      max_bytes_per_blob=2)

  def testCreateUploadURLError(self):
    rpc = MockRPC(error=-1, message='detail')
    try:
      blobstore.create_upload_url('/success_path', rpc=rpc)
      self.fail('Expected raise ApplicationError')
    except apiproxy_errors.ApplicationError as e:
      self.assertEqual(-1, e.application_error)
      self.assertEqual('detail', e.error_detail)

    rpc = MockRPC(
        error=blobstore_service_pb2.BlobstoreServiceError.INTERNAL_ERROR,
        message='detail2')
    try:
      blobstore.create_upload_url('/success_path', rpc=rpc)
      self.fail('Expected raise InternalError')
    except blobstore.InternalError as e:
      self.assertEqual('detail2', str(e))

  def testCreateUploadURLBytesPerBlobError(self):
    self.assertRaisesWithLiteralMatch(
        TypeError, 'max_bytes_per_blob must be integer.',
        blobstore.create_upload_url, '/success_path', max_bytes_per_blob='foo')

    self.assertRaisesWithLiteralMatch(
        ValueError,
        'max_bytes_per_blob must be positive.',
        blobstore.create_upload_url, '/success_path', max_bytes_per_blob=0)

  def testCreateUploadURLBytesTotalError(self):
    self.assertRaisesWithLiteralMatch(
        TypeError, 'max_bytes_total must be integer.',
        blobstore.create_upload_url, '/success_path', max_bytes_total='foo')

    self.assertRaisesWithLiteralMatch(
        ValueError,
        'max_bytes_total must be positive.',
        blobstore.create_upload_url, '/success_path', max_bytes_total=0)

  def testCreateUploadURLGoogleStorageNameError(self):
    self.assertRaisesWithLiteralMatch(
        TypeError, 'gs_bucket_name must be a string.',
        blobstore.create_upload_url, '/success_path', gs_bucket_name=1)

  def testDeleteBlob(self):
    def side_effect(rpc):
      self.assertEqual('DeleteBlob', rpc.method)
      self.assertEqual(['my giant blob'], rpc.request.blob_key)
      self.sync_was_called = True
    rpc = MockRPC(side_effect)
    blobstore.delete('my giant blob', rpc=rpc)
    self.assertTrue(self.sync_was_called)

  def testDeleteBlob_BlobKey(self):
    def side_effect(rpc):
      self.assertEqual('DeleteBlob', rpc.method)
      self.assertEqual(['my giant blob'], rpc.request.blob_key)
      self.sync_was_called = True
    rpc = MockRPC(side_effect)
    blobstore.delete(blobstore.BlobKey('my giant blob'), rpc=rpc)
    self.assertTrue(self.sync_was_called)

  def testDeleteBlob_Multiple(self):
    def side_effect(rpc):
      self.assertEqual('DeleteBlob', rpc.method)
      self.assertEqual(['my giant blob 1', 'my giant blob 2'],
                       rpc.request.blob_key)
      self.sync_was_called = True
    rpc = MockRPC(side_effect)
    blobstore.delete([blobstore.BlobKey('my giant blob 1'),
                      'my giant blob 2'],
                     rpc)
    self.assertTrue(self.sync_was_called)

  def testDeleteBlob_Token(self):
    def side_effect(rpc):
      self.assertEqual('DeleteBlob', rpc.method)
      self.assertEqual(['my giant blob'], rpc.request.blob_key)
      self.assertEqual('token', rpc.request.token)
      self.sync_was_called = True
    rpc = MockRPC(side_effect)
    blobkey = blobstore.BlobKey('my giant blob')
    blobstore.delete([blobkey], rpc, 'token')

  def testDeleteBlobError(self):
    rpc = MockRPC(error=-1, message='detail1')
    try:
      blobstore.delete('a blob', rpc=rpc)
      self.fail('Expected raise ApplicationError')
    except apiproxy_errors.ApplicationError as e:
      self.assertEqual(-1, e.application_error)
      self.assertEqual('detail1', e.error_detail)

    rpc = MockRPC(
        error=blobstore_service_pb2.BlobstoreServiceError.INTERNAL_ERROR,
        message='detail2')
    try:
      blobstore.delete('a blob', rpc=rpc)
      self.fail('Expected raise InternalError')
    except blobstore.InternalError as e:
      self.assertEqual('detail2', str(e))

  def testFormatCreation(self):
    """Test formatting creation time stamp function."""
    self.assertEqual(
        '2000-09-08 07:06:05.432121',
        blobstore._format_creation(
            datetime.datetime(2000, 9, 8, 7, 6, 5, 432121)))
    self.assertEqual(
        '2000-09-08 07:06:05.000000',
        blobstore._format_creation(datetime.datetime(2000, 9, 8, 7, 6, 5)))

  def testParseCreation(self):
    """Test the creation timestamp parsing function."""
    self.assertEqual(
        datetime.datetime(1999, 0o2, 0o3, 0o4, 0o5, 0o6, 78910),
        blobstore._parse_creation('1999-02-03 04:05:06.078910', 'not-used'))

  def testParseCreation_BadFormats(self):
    """Test the creation timestamp parsing function."""
    for creation in ('',
                     '1999',
                     '1999-02',
                     '1999-02-03',
                     '1999-02-03 04',
                     '1999-02-03 04:05',
                     '1999-02-03 04:05:06',
                     '1999-02-03 04:05:06:078910',
                     '1999-02-03-04:05:06.078910',
                     'x999-02-03 04:05:06.078910',
                     '1999-x2-03 04:05:06.078910',
                     '1999-02-x3 04:05:06.078910',
                     '1999-02-03 x4:05:06.078910',
                     '1999-02-03 04:x5:06.078910',
                     '1999-02-03 04:05:x6.078910',
                     '1999-02-03 04:05:06.x78910',
                     ):
      self.assertRaisesRegex(
          blobstore._CreationFormatError,
          'Could not parse creation %s in field my_field' % creation,
          blobstore._parse_creation, creation, 'my_field')

  def testFetchData_InvalidIndexType(self):
    """Test a set of invalid index types to fetch_data."""
    self.assertRaises(TypeError,
                      blobstore.fetch_data,
                      'my-blob',
                      0,
                      '1')

    self.assertRaises(TypeError,
                      blobstore.fetch_data,
                      'my-blob',
                      '0',
                      1)

  def testFetchData_InvalidBlobKeyType(self):
    """Test a set of invalid blob-key types to fetch_data."""
    self.assertRaises(TypeError,
                      blobstore.fetch_data,
                      10,
                      0,
                      1)

    self.assertRaises(TypeError,
                      blobstore.fetch_data,
                      ['my-blob'],
                      0,
                      1)

  def testFetchData_IndexOutOfRange(self):
    """Test a set of bad indexes to fetch_data."""
    self.assertRaises(blobstore.DataIndexOutOfRangeError,
                      blobstore.fetch_data,
                      'my-blob',
                      -1,
                      1)

    self.assertRaises(blobstore.DataIndexOutOfRangeError,
                      blobstore.fetch_data,
                      'my-blob',
                      1,
                      0)

  def testFetchData_FetchSizeTooLarge(self):
    """Test fetching a blob fragment that is too large."""
    self.assertRaises(blobstore.BlobFetchSizeTooLargeError,
                      blobstore.fetch_data,
                      'my-blob',
                      0,
                      blobstore.MAX_BLOB_FETCH_SIZE + 1)

    self.assertRaises(blobstore.BlobFetchSizeTooLargeError,
                      blobstore.fetch_data,
                      'my-blob',
                      1,
                      blobstore.MAX_BLOB_FETCH_SIZE + 2)

  def testFetchData_GoodRequests(self):
    """Test a bunch of good requests."""
    for blob_key, start, end in (
        ('my-blob', 0, 1),
        (u'my-blob', 0, 1),
        (blobstore.BlobKey('my-blob'), 0, 1),
        ('my-blob', int(0), 1),
        ('my-blob', 0, 0),
    ):
      self.async_called = False
      def side_effect(rpc):
        self.assertEqual('FetchData', rpc.method)
        self.assertEqual(u'my-blob', rpc.request.blob_key)
        self.assertEqual(0, rpc.request.start_index)
        self.assertEqual(end, rpc.request.end_index)

        rpc.response.data = b'x'

        self.async_called = True

      rpc = MockRPC(side_effect=side_effect)

      self.assertEqual(b'x', blobstore.fetch_data(
          blob_key, start, end, rpc=rpc))
      self.assertEqual(True, self.async_called)

  def testFetchData_HandleErrors(self):
    """Test RPC error handling."""
    for error_code, expected_exception in (
        (blobstore_service_pb2.BlobstoreServiceError.BLOB_NOT_FOUND,
         blobstore.BlobNotFoundError),
        (blobstore_service_pb2.BlobstoreServiceError.DATA_INDEX_OUT_OF_RANGE,
         blobstore.DataIndexOutOfRangeError),
        (blobstore_service_pb2.BlobstoreServiceError.BLOB_FETCH_SIZE_TOO_LARGE,
         blobstore.BlobFetchSizeTooLargeError),
    ):
      rpc = MockRPC(error=error_code)
      self.assertRaises(expected_exception,
                        blobstore.fetch_data,
                        'my-blob',
                        0,
                        1,
                        rpc=rpc)

  def test_ToBlobstoreError_Success(self):
    """Test that the conversion of error type to exception works."""
    error_mapping = [
        ('INTERNAL_ERROR', 'InternalError'),
        ('BLOB_NOT_FOUND', 'BlobNotFoundError'),
        ('DATA_INDEX_OUT_OF_RANGE', 'DataIndexOutOfRangeError'),
        ('BLOB_FETCH_SIZE_TOO_LARGE', 'BlobFetchSizeTooLargeError'),
        ('PERMISSION_DENIED', 'PermissionDeniedError'),
        ]

    for error_name, exc_name in error_mapping:
      error_code = getattr(blobstore_service_pb2.BlobstoreServiceError,
                           error_name)
      expected_exc = getattr(blobstore, exc_name)
      application_exc = apiproxy_errors.ApplicationError(error_code)
      given_exc = blobstore._ToBlobstoreError(application_exc)
      self.assertTrue(isinstance(given_exc, expected_exc))

  def test_ToBlobstoreError_UnknownApplicationError(self):
    """Test that an ApplicationError's error is not known is simply returned."""
    application_err = apiproxy_errors.ApplicationError(100000000)
    given_exc = blobstore._ToBlobstoreError(application_err)
    self.assertEqual(given_exc, application_err)

  def testCreateGoogleStorageKey(self):
    """Basic test for creating a bigstore key."""
    request = blobstore_service_pb2.CreateEncodedGoogleStorageKeyRequest()
    request.filename = 'some_bucket/some_object'

    def side_effect(rpc):
      rpc.response.blob_key = 'encoded-key'

    rpc = MockRPC(side_effect)

    self.assertEqual(
        'encoded-key',
        blobstore.create_gs_key('/gs/some_bucket/some_object', rpc=rpc))

  def testCreateGoogleStorageKey_BadFilename(self):
    self.assertRaises(TypeError,
                      blobstore.create_gs_key,
                      100)

    self.assertRaises(ValueError,
                      blobstore.create_gs_key,
                      'some_bucket/some_object')

    self.assertRaises(ValueError,
                      blobstore.create_gs_key,
                      '/gs/some_bucketsome_obect')


if __name__ == '__main__':
  absltest.main()
