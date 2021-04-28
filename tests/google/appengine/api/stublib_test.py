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


"""Tests for google.third_party.py.google.appengine.api.stub."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import mock

from google.appengine.api import stublib
from absl.testing import absltest


class PatcherMock(object):
  """MagicMocks have their own "attribute" attr, so make this mock by hand."""

  def __init__(self, module, attribute):
    self.target = mock.MagicMock()
    self.target.__name__ = module
    self.attribute = attribute
    self.start = mock.MagicMock()
    self.stop = mock.MagicMock()


class PatchersTest(absltest.TestCase):
  """Tests for API proxy stub."""

  def setUp(self):
    super(PatchersTest, self).setUp()
    self.stub = mock.MagicMock()
    self.stub.patchers = stublib.Patchers([
        PatcherMock('test', 'foo'),
        PatcherMock('test', 'bar')])

  def testStartAll(self):
    self.stub.patchers.StartAll()
    for p in self.stub.patchers:
      p.start.assert_called_once_with()

  def testCanonicalName(self):
    self.stub.patchers.append(PatcherMock('titanoboa_apphosting.foo', 'bar'))
    mocks = self.stub.patchers.StartAll()
    self.assertIn('google.appengine.foo.bar', mocks)

  def testStopAll(self):
    self.stub.patchers.StopAll()
    for p in self.stub.patchers:
      p.stop.assert_called_once_with()

  def testStopFailure(self):
    """Make sure a failure in the middle of the list doesn't cause problems."""
    failpatcher = PatcherMock('full.of', 'fail')
    failpatcher.stop = mock.MagicMock(side_effect=RuntimeError)
    self.stub.patchers.insert(1, failpatcher)
    self.stub.patchers.StopAll()
    for p in self.stub.patchers:
      p.stop.assert_called_once_with()

if __name__ == '__main__':
  absltest.main()
