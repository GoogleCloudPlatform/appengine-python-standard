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

from google.appengine.api import lib_config
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
    namespace_manager.enable_request_namespace()
    self.assertEqual('', namespace_manager.get_namespace())

  def testNamespaceWithEnvironment(self):
    """Checks that the dasher domain becomes namespace when enabled."""
    os.environ['HTTP_X_APPENGINE_DEFAULT_NAMESPACE'] = 'namespace_from_http'
    self.assertEqual('', namespace_manager.get_namespace())
    namespace_manager.enable_request_namespace()
    self.assertEqual('namespace_from_http', namespace_manager.get_namespace())
    namespace_manager.set_namespace('foo')
    self.assertEqual('foo', namespace_manager.get_namespace())
    namespace_manager.enable_request_namespace()
    self.assertEqual('foo', namespace_manager.get_namespace())

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


class LocalException(Exception):
  """Exception class unique to these tests."""


class NamespaceManagerConfigTest(absltest.TestCase):

  def setUp(self):
    """Get a config handle for the namespace_manager."""
    self.handle = lib_config.register('namespace_manager_', {})
    self.default_namespace_functions = self.handle._defaults.copy()

  def tearDown(self):
    """Restore environment."""
    os.environ = dict(INITIAL_ENVIRON)
    self.handle = lib_config.register('namespace_manager_',
                                      self.default_namespace_functions)

  def _SetDefaultNamespaceForRequestFn(self, fn):
    self.handle._update_defaults({'default_namespace_for_request': fn})

  def testDefaultNamespaceForRequestIsCalled(self):
    def default_namespace():
      raise LocalException

    self._SetDefaultNamespaceForRequestFn(default_namespace)
    self.assertRaises(LocalException, namespace_manager.get_namespace)

  def testDefaultNamespaceNotCalledAfterSetNamespace(self):
    def default_namespace():
      raise LocalException

    self._SetDefaultNamespaceForRequestFn(default_namespace)
    namespace_manager.set_namespace('foo')
    try:
      name = namespace_manager.get_namespace()
    except LocalException:
      self.fail('Unexpected LocalException')

    self.assertEqual('foo', name)

  def testDefaultNamespaceNotCalledAfterEmptySetNamespace(self):
    def default_namespace():
      raise LocalException

    self._SetDefaultNamespaceForRequestFn(default_namespace)
    namespace_manager.set_namespace('')
    try:
      name = namespace_manager.get_namespace()
    except LocalException:
      self.fail('Unexpected LocalException')

    self.assertEqual('', name)

  def testDefaultNamespaceReturnedOnlyWhenSetNamespaceUncalled(self):
    self._SetDefaultNamespaceForRequestFn(lambda: 'footy')
    self.assertEqual('footy', namespace_manager.get_namespace())

    namespace_manager.set_namespace('ball')
    self.assertEqual('ball', namespace_manager.get_namespace())

if __name__ == '__main__':
  absltest.main()

