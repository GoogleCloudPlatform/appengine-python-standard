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



"""Unit tests for the lib_config module."""

from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import sys

from google.appengine.api import lib_config
from google.appengine.api import module_testutil
from absl.testing import absltest






class ModuleInterfaceTest(module_testutil.ModuleInterfaceTest,
                          absltest.TestCase):

  MODULE = lib_config


class ConfigHandleTests(absltest.TestCase):
  """Tests for the ConfigHandle class."""

  def setUp(self):
    self.modname = 'foo_test'
    self.registry = lib_config.LibConfigRegistry(self.modname)
    sys.modules[self.modname] = None
    self.log_data = []
    logging.warn = self.add_to_log_data

  def add_to_log_data(self, msg, *args):
    self.log_data.append(msg % args)

  def tearDown(self):
    del sys.modules['foo_test']

  def testHandle_AttributeError(self):
    handle = lib_config.ConfigHandle('foo_', self.registry)
    self.assertEqual(handle._initialized, False)

    self.assertRaises(AttributeError, lambda: handle.abc)
    self.assertEqual(handle._initialized, True)

  def testHandle_Basics(self):
    handle = lib_config.ConfigHandle('foo_', self.registry)
    handle._update_defaults({'abc': 42, 'xyz': 'zy'})
    self.assertEqual(handle._initialized, False)

    self.assertEqual(handle.abc, 42)
    self.assertEqual(handle.xyz, 'zy')
    self.assertEqual(handle._initialized, True)

    handle._update_defaults({'abc': 123, 'cde': 'def'})

    self.assertEqual(handle._initialized, True)
    self.assertEqual(handle.abc, 123)
    self.assertEqual(handle.cde, 'def')
    self.assertEqual(handle.xyz, 'zy')

  def testHandle_Overrides(self):
    class Overrides(object):
      def __init__(self):
        self.foo_abc = 1000
        self.foo_cde = 'abc'
    sys.modules[self.modname] = Overrides()

    handle = lib_config.ConfigHandle('foo_', self.registry)
    handle._update_defaults({'abc': 42, 'xyz': 'zy'})

    self.assertEqual(handle.abc, 1000)
    self.assertEqual(self.log_data, ['Configuration "foo_cde" not recognized'])

    handle._update_defaults({'abc': 123, 'cde': 'def'})

    self.assertEqual(handle.abc, 1000)
    self.assertEqual(handle.cde, 'abc')



    handle._clear_cache()
    sys.modules[self.modname] = None

    self.assertEqual(handle.abc, 123)
    self.assertEqual(handle.cde, 'def')


class LibConfigRegistryTests(absltest.TestCase):
  """Tests for the LibConfigRegistry class."""

  def setUp(self):
    self.modname = 'foo_test'
    self.registry = lib_config.LibConfigRegistry(self.modname)
    sys.modules[self.modname] = None

  def tearDown(self):
    del sys.modules[self.modname]

  def testRegistry_Basics(self):
    self.assertEqual(self.registry._module, None)
    self.registry.initialize()
    self.assertNotEqual(self.registry._module, None)

  def testRegistry_Register(self):
    handle = self.registry.register('foo', {'suffix': 42})
    self.assertEqual(list(self.registry._registrations.keys()), ['foo_'])
    self.assertEqual(self.registry._registrations['foo_'], handle)
    self.assertEqual(handle._prefix, 'foo_')
    self.assertEqual(handle._defaults, {'suffix': 42})
    handle2 = self.registry.register('foo', {'more': 123})
    self.assertEqual(handle2, handle2)
    self.assertEqual(handle._defaults, {'suffix': 42, 'more': 123})

  def testRegistry_InitializeCaching(self):
    trace = []
    token = object()
    def import_func_mock(name, *args):
      sys.modules[name] = token
      trace.append(len(trace))


    self.registry.initialize(import_func=import_func_mock)
    self.assertEqual(trace, [0])


    self.registry.initialize(import_func=import_func_mock)
    self.assertEqual(trace, [0])

  def testRegistry_Reset(self):
    trace = []
    token = object()
    def import_func_mock(name, *args):
      sys.modules[name] = token
      trace.append(len(trace))

    self.registry.initialize(import_func=import_func_mock)
    self.assertEqual(trace, [0])

    self.registry.reset()

    self.registry.initialize(import_func=import_func_mock)
    self.assertEqual(trace, [0, 1])


  def testRegistry_InitializeImportErrorGood(self):

    trace = []
    def import_func_mock(name, *args):
      trace.append(len(trace))
      raise ImportError('No module named %s' % name)
    self.registry.initialize(import_func=import_func_mock)
    self.assertEqual(trace, [0])

  def testRegistry_InitializeImportErrorBad(self):

    def import_func_mock(name, *args):
      raise ImportError('No module named something.else')
    self.assertRaises(ImportError,
                      self.registry.initialize, import_func=import_func_mock)


if __name__ == '__main__':
  absltest.main()
