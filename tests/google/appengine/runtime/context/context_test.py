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
"""Tests for google.appengine.runtime.context."""

import os
from unittest import mock

from google.appengine.runtime import context
from google.appengine.runtime.context import ctx_test_util

from absl.testing import absltest


@ctx_test_util.isolated_context()
class ContextTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    orig_val = context.READ_FROM_OS_ENVIRON
    def restore():
      context.READ_FROM_OS_ENVIRON = orig_val
    self.addCleanup(restore)

  def testBooleanConversionOnWrite(self):
    context.init_from_wsgi_environ({
        'HTTP_X_APPENGINE_USER_IS_ADMIN': '1',
    })
    self.assertEqual(context.gae_headers.USER_IS_ADMIN.get(), True)

  def testBooleanConversionOnRead(self):
    context.READ_FROM_OS_ENVIRON = False
    context.gae_headers.USER_IS_ADMIN.set(True)
    self.assertEqual(context.get('USER_IS_ADMIN'), '1')

  @mock.patch.dict(os.environ)
  @mock.patch.object(context, 'READ_FROM_OS_ENVIRON')
  def testReadFrom(self, mock_read_from_os_environ):
    del mock_read_from_os_environ
    context.gae_headers.USER_ID.set('value in context')
    os.environ['USER_ID'] = 'value in os.environ'

    with self.subTest('contextvars'):
      context.READ_FROM_OS_ENVIRON = False
      self.assertEqual(context.get('USER_ID'), 'value in context')
    with self.subTest('os.environ'):
      context.READ_FROM_OS_ENVIRON = True
      self.assertEqual(context.get('USER_ID'), 'value in os.environ')

if __name__ == '__main__':
  absltest.main()
