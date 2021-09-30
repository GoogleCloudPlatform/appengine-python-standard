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


"""Tests for google.appengine.api.namespace_manager."""



import os

import google

from google.appengine.api import module_testutil
from google.appengine.api import namespace_manager
from absl.testing import absltest

INITIAL_ENVIRON = dict(os.environ)

class ModuleInterfaceTest(module_testutil.ModuleInterfaceTest,
                          absltest.TestCase):

  MODULE = namespace_manager.namespace_manager


class NamespaceManagerTest(absltest.TestCase):

  def tearDown(self):
    """Restore environment."""
    os.environ = dict(INITIAL_ENVIRON)

  def testNamespaceNoEnvironment(self):
    """Basic namespace test."""
    self.assertEqual('', namespace_manager.get_namespace())

  def testGoogleAppsNamespaceNoEnvironment(self):
    self.assertIsNone(namespace_manager.google_apps_namespace())

  def testGoogleAppsNamespaceFromEnvironment(self):
    os.environ['HTTP_X_APPENGINE_DEFAULT_NAMESPACE'] = 'apps_ns_from_http'
    self.assertEqual('apps_ns_from_http',
                     namespace_manager.google_apps_namespace())

  def testSetNamespaceEmptyString(self):
    """Makes sure that None is never returned from get_namespace()."""
    self.assertEqual('', namespace_manager.get_namespace())
    namespace_manager.set_namespace('foo')
    self.assertEqual('foo', namespace_manager.get_namespace())
    namespace_manager.set_namespace('')
    self.assertEqual('', namespace_manager.get_namespace())
    namespace_manager.set_namespace(None)
    self.assertEqual('', namespace_manager.get_namespace())

  def verifyException(self, value):
    try:
      namespace_manager.set_namespace(value)
      self.fail("Expected namespace_manager.BadValueError exception")
    except namespace_manager.BadValueError:
      pass

  def testNamespaceValid(self):
    """Test namespace validator."""
    namespace_manager.set_namespace('')
    namespace_manager.set_namespace('__a.namespace.123__')
    namespace_manager.set_namespace('-_A....NAMESPACE-_')
    namespace_manager.set_namespace('-')
    namespace_manager.set_namespace('.')
    namespace_manager.set_namespace('.-')

  def testNamespaceInvalid(self):
    self.verifyException("?")
    self.verifyException("+")
    self.verifyException("!")
    self.verifyException(" ")


if __name__ == '__main__':
  absltest.main()

