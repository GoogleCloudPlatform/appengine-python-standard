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
















"""Tests for blobstore.py."""

import cgi
import datetime

from google.appengine.ext.ndb import blobstore
from google.appengine.ext.ndb import model
from google.appengine.ext.ndb import tasklets
from google.appengine.ext.ndb import test_utils
import six

from absl.testing import absltest as unittest


def _CreateFieldStorage(file_content, headers, environ):
  """Creates a Python-version-appropriate cgi.FieldStorage object.

  In PY3, the FieldStorage class explicitly specifies that fp must be a
  file-like object that produces *bytes*:
  http://google/third_party/python_runtime/v3_6/Lib/cgi.py?l=416&rcl=151856175

  Args:
    file_content: The desired text content of the contained file-like object.
    headers: Dictionary-like header object.
    environ: Dictionary-like environment object.

  Returns:
    An initialized cgi.FieldStorage object.
  """
  if six.PY2:
    fp = six.StringIO(file_content)
  else:
    fp = six.BytesIO(six.ensure_binary(file_content))

  return cgi.FieldStorage(fp=fp, headers=headers, environ=environ)


class BlobstoreTests(test_utils.NDBTest):

  def setUp(self):
    super(BlobstoreTests, self).setUp()
    self.testbed.init_blobstore_stub()

  the_module = blobstore

  def testConstants(self):


    self.assertEqual(blobstore.BLOB_INFO_KIND, '__BlobInfo__')
    self.assertEqual(blobstore.BLOB_MIGRATION_KIND, '__BlobMigration__')
    self.assertEqual(blobstore.BLOB_KEY_HEADER, 'X-AppEngine-BlobKey')
    self.assertEqual(blobstore.BLOB_RANGE_HEADER, 'X-AppEngine-BlobRange')
    self.assertEqual(blobstore.UPLOAD_INFO_CREATION_HEADER,
                     'X-AppEngine-Upload-Creation')
    self.assertEqual(blobstore.MAX_BLOB_FETCH_SIZE, 1015808)

  def testExceptions(self):
    self.assertTrue(issubclass(blobstore.Error, Exception))
    self.assertTrue(issubclass(blobstore.InternalError, blobstore.Error))
    self.assertTrue(issubclass(blobstore.BlobFetchSizeTooLargeError,
                               blobstore.Error))
    self.assertTrue(issubclass(blobstore.BlobNotFoundError, blobstore.Error))
    self.assertTrue(issubclass(blobstore.DataIndexOutOfRangeError,
                               blobstore.Error))
    self.assertTrue(issubclass(blobstore.PermissionDeniedError,
                               blobstore.Error))
    self.assertTrue(issubclass(blobstore.BlobInfoParseError, blobstore.Error))

  def create_blobinfo(self, blobkey):
    """Handcraft a dummy BlobInfo."""
    b = blobstore.BlobInfo(key=model.Key(blobstore.BLOB_INFO_KIND, blobkey),
                           content_type='text/plain',
                           creation=datetime.datetime(2012, 1, 24, 8, 15, 0),
                           filename='hello.txt',
                           size=42,
                           md5_hash='xxx')
    model.Model._put_async(b).check_success()
    return b

  def testBlobInfo(self):
    b = self.create_blobinfo('dummy')
    self.assertEqual(b._get_kind(), blobstore.BLOB_INFO_KIND)
    self.assertEqual(b.key(), blobstore.BlobKey('dummy'))
    self.assertEqual(b.content_type, 'text/plain')
    self.assertEqual(b.creation, datetime.datetime(2012, 1, 24, 8, 15, 0))
    self.assertEqual(b.filename, 'hello.txt')
    self.assertEqual(b.md5_hash, 'xxx')

  def testBlobInfo_PutErrors(self):
    b = self.create_blobinfo('dummy')
    self.assertRaises(Exception, b.put)
    self.assertRaises(Exception, b.put_async)
    self.assertRaises(Exception, model.put_multi, [b])
    self.assertRaises(Exception, model.put_multi_async, [b])

  def testBlobInfo_Get(self):
    b = self.create_blobinfo('dummy')
    c = blobstore.BlobInfo.get(b.key())
    self.assertEqual(c, b)
    self.assertTrue(c is not b)
    c = blobstore.BlobInfo.get('dummy')
    self.assertEqual(c, b)
    self.assertTrue(c is not b)

  def testBlobInfo_GetAsync(self):
    b = self.create_blobinfo('dummy')
    cf = blobstore.BlobInfo.get_async(b.key())
    self.assertTrue(isinstance(cf, tasklets.Future))
    c = cf.get_result()
    self.assertEqual(c, b)
    self.assertTrue(c is not b)
    df = blobstore.BlobInfo.get_async(str(b.key()))
    self.assertTrue(isinstance(df, tasklets.Future))
    d = df.get_result()
    self.assertEqual(d, b)
    self.assertTrue(d is not b)

  def testBlobInfo_GetMulti(self):
    b = self.create_blobinfo('b')
    c = self.create_blobinfo('c')
    d, e = blobstore.BlobInfo.get_multi([b.key(), str(c.key())])
    self.assertEqual(d, b)
    self.assertEqual(e, c)

  def testBlobInfo_GetMultiAsync(self):
    b = self.create_blobinfo('b')
    c = self.create_blobinfo('c')
    df, ef = blobstore.BlobInfo.get_multi_async([str(b.key()), c.key()])
    self.assertTrue(isinstance(df, tasklets.Future))
    self.assertTrue(isinstance(ef, tasklets.Future))
    d, e = df.get_result(), ef.get_result()
    self.assertEqual(d, b)
    self.assertEqual(e, c)

  def testBlobInfo_Delete(self):
    b = self.create_blobinfo('dummy')
    c = blobstore.get(b._key.id())
    self.assertEqual(c, b)
    b.delete()
    d = blobstore.get(b.key())
    self.assertEqual(d, None)

  def testBlobInfo_DeleteAsync(self):
    b = self.create_blobinfo('dummy')
    df = b.delete_async()
    self.assertTrue(isinstance(df, tasklets.Future), df)
    df.get_result()
    d = blobstore.get(b.key())
    self.assertEqual(d, None)

  def testBlobstore_Get(self):
    b = self.create_blobinfo('dummy')
    c = blobstore.get(b.key())
    self.assertEqual(c, b)
    self.assertTrue(c is not b)
    c = blobstore.get('dummy')
    self.assertEqual(c, b)
    self.assertTrue(c is not b)

  def testBlobstore_GetAsync(self):
    b = self.create_blobinfo('dummy')
    cf = blobstore.get_async(b.key())
    self.assertTrue(isinstance(cf, tasklets.Future))
    c = cf.get_result()
    self.assertEqual(c, b)
    self.assertTrue(c is not b)
    cf = blobstore.get_async('dummy')
    c = cf.get_result()
    self.assertEqual(c, b)
    self.assertTrue(c is not b)

  def testBlobstore_Delete(self):
    b = self.create_blobinfo('dummy')
    blobstore.delete(b.key())
    d = blobstore.get(b.key())
    self.assertEqual(d, None)

  def testBlobstore_DeleteAsync(self):
    b = self.create_blobinfo('dummy')
    df = blobstore.delete_async(b.key())
    self.assertTrue(isinstance(df, tasklets.Future), df)
    df.get_result()
    d = blobstore.get(b.key())
    self.assertEqual(d, None)

  def testBlobstore_DeleteMulti(self):
    b = self.create_blobinfo('b')
    c = self.create_blobinfo('c')
    blobstore.delete_multi([b.key(), str(c.key())])
    d, e = blobstore.get_multi([b.key(), str(c.key())])
    self.assertEqual(d, None)
    self.assertEqual(e, None)

  def testBlobstore_DeleteMultiAsync(self):
    b = self.create_blobinfo('b')
    c = self.create_blobinfo('c')
    f = blobstore.delete_multi_async([b.key(), str(c.key())])
    self.assertTrue(isinstance(f, tasklets.Future), f)
    f.get_result()
    d, e = blobstore.get_multi([b.key(), str(c.key())])
    self.assertEqual(d, None)
    self.assertEqual(e, None)

  def testBlobstore_CreateUploadUrl(self):
    url = blobstore.create_upload_url('/foo')
    self.assertTrue('/_ah/upload/' in url, url)

  def testBlobstore_CreateUploadUrlAsync(self):
    urlf = blobstore.create_upload_url_async('/foo')
    self.assertTrue(isinstance(urlf, tasklets.Future), urlf)
    url = urlf.get_result()
    self.assertTrue('/_ah/upload/' in url, url)

  def testBlobstore_ParseBlobInfo_Errors(self):
    nope = blobstore.parse_blob_info(None)
    self.assertEqual(nope, None)

    env = {'REQUEST_METHOD': 'POST'}
    hdrs = {'content-disposition': 'blah; filename=hello.txt; name=hello',
            'content-type': 'text/plain; blob-key=xxx'}

    file_content = (
        'Content-length: 42\n'
        'X-AppEngine-Upload-Creation: 2012-01-24 17:35:00.000000\n'
        'Content-MD5: eHh4\n'
        '\n')
    fs = _CreateFieldStorage(file_content, hdrs, env)
    self.assertRaises(blobstore.BlobInfoParseError,
                      blobstore.parse_blob_info, fs)

    file_content = (
        'Content-type: image/jpeg\n'
        'Content-length: hello\n'
        'X-AppEngine-Upload-Creation: 2012-01-24 17:35:00.000000\n'
        'Content-MD5: eHh4\n'
        '\n')
    fs = _CreateFieldStorage(file_content, hdrs, env)
    self.assertRaises(blobstore.BlobInfoParseError,
                      blobstore.parse_blob_info, fs)

    file_content = (
        'Content-type: image/jpeg\n'
        'Content-length: 42\n'
        'X-AppEngine-Upload-Creation: BLAH-01-24 17:35:00.000000\n'
        'Content-MD5: eHh4\n'
        '\n')
    fs = _CreateFieldStorage(file_content, hdrs, env)
    self.assertRaises(blobstore.BlobInfoParseError,
                      blobstore.parse_blob_info, fs)

  def testBlobstore_ParseBlobInfo(self):
    env = {'REQUEST_METHOD': 'POST'}
    hdrs = {'content-disposition': 'blah; filename=hello.txt; name=hello',
            'content-type': 'text/plain; blob-key=xxx'}

    file_content = (
        'Content-type: image/jpeg\n'
        'Content-length: 42\n'
        'X-AppEngine-Upload-Creation: 2012-01-24 17:35:00.000000\n'
        'Content-MD5: eHh4\n'
        '\n')
    fs = _CreateFieldStorage(file_content, hdrs, env)
    actual_bi = blobstore.parse_blob_info(fs)
    self.assertIsInstance(actual_bi, blobstore.BlobInfo)
    expected_bi = blobstore.BlobInfo(
        key=model.Key(blobstore.BlobInfo, 'xxx'),
        content_type='image/jpeg',
        creation=datetime.datetime(2012, 1, 24, 17, 35),
        filename='hello.txt',
        md5_hash=b'xxx',
        size=42)
    self.assertEqual(expected_bi, actual_bi)

  def testBlobstore_FetchData(self):
    self.create_blobinfo('xxx')
    stub = self.testbed.get_stub('blobstore')
    storage = stub.storage
    storage._blobs['xxx'] = b'abcde'
    result = blobstore.fetch_data('xxx', 0, 3)
    self.assertEqual(result, b'abcd')

  def testBlobstore_FetchDataAsync(self):
    b = self.create_blobinfo('xxx')
    stub = self.testbed.get_stub('blobstore')
    storage = stub.storage
    storage._blobs['xxx'] = b'abcde'
    fut = blobstore.fetch_data_async(b, 0, 2)
    self.assertTrue(isinstance(fut, tasklets.Future), fut)
    result = fut.get_result()
    self.assertEqual(result, b'abc')

  def testBlobInfo_Open(self):
    b = self.create_blobinfo('xxx')
    stub = self.testbed.get_stub('blobstore')
    storage = stub.storage
    storage._blobs['xxx'] = b'abcde'
    f = b.open()
    self.assertEqual(f.read(3), b'abc')
    self.assertEqual(f.read(3), b'de')
    self.assertEqual(f.blob_info, b)

  def testBlobReader(self):
    b = self.create_blobinfo('xxx')
    stub = self.testbed.get_stub('blobstore')
    storage = stub.storage
    storage._blobs['xxx'] = b'abcde'
    f = blobstore.BlobReader('xxx')
    self.assertEqual(f.read(), b'abcde')
    self.assertEqual(f.blob_info, b)

if __name__ == '__main__':
  unittest.main()
