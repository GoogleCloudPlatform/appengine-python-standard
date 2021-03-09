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




"""Tests for google.appengine.api.backendinfo."""

from __future__ import absolute_import

from google.appengine.api import backendinfo
from google.appengine.api import validation
from absl import app
from absl.testing import absltest




class BackendEntryTest(absltest.TestCase):
  """Tests for the backendinfo.BackendEntry class."""

  def testCheckInitialized(self):
    entry = backendinfo.BackendEntry(name='foo')
    entry.CheckInitialized()


    entry = backendinfo.BackendEntry()
    self.assertRaises(validation.ValidationError,
                      backendinfo.BackendEntry.CheckInitialized,
                      entry)

  def testName(self):
    entry = backendinfo.BackendEntry(name='1')
    self.assertEqual('1', entry.name)


    entry.name = '1' * 100
    self.assertEqual('1' * 100, entry.name)
    try:
      entry.name = '1' * 101
      self.fail()
    except validation.ValidationError:
      pass

  def testStart(self):
    entry = backendinfo.BackendEntry(name='1', start='bar/foo.py')
    self.assertEqual('bar/foo.py', entry.start)


    entry.start = 'a' * 256
    self.assertEqual('a' * 256, entry.start)
    try:
      entry.name = 'a' * 257
      self.fail()
    except validation.ValidationError:
      pass

  def testClass(self):
    entry = backendinfo.BackendEntry(name='1')

    entry.set_class('B1')
    self.assertEqual('B1', entry.get_class())
    entry.set_class('B2')
    self.assertEqual('B2', entry.get_class())
    entry.set_class('B4')
    self.assertEqual('B4', entry.get_class())
    entry.set_class('B8')
    self.assertEqual('B8', entry.get_class())

    entry.set_class('b1')
    self.assertEqual('b1', entry.get_class())
    entry.set_class('b2')
    self.assertEqual('b2', entry.get_class())
    entry.set_class('b4')
    self.assertEqual('b4', entry.get_class())
    entry.set_class('b8')
    self.assertEqual('b8', entry.get_class())

    self.assertRaises(validation.ValidationError,
                      backendinfo.BackendEntry.set_class,
                      entry, 'B0')
    self.assertRaises(validation.ValidationError,
                      backendinfo.BackendEntry.set_class,
                      entry, 'B3')
    self.assertRaises(validation.ValidationError,
                      backendinfo.BackendEntry.set_class,
                      entry, 'B5')
    self.assertRaises(validation.ValidationError,
                      backendinfo.BackendEntry.set_class,
                      entry, 'B7')
    self.assertRaises(validation.ValidationError,
                      backendinfo.BackendEntry.set_class,
                      entry, 'B9')

  def testOptions(self):
    entry = backendinfo.BackendEntry(name='foo')
    self.assertFalse(entry.public)
    self.assertFalse(entry.dynamic)
    self.assertFalse(entry.failfast)
    self.assertEqual(None, entry.options)

    entry = backendinfo.BackendEntry(name='foo', options='public')
    self.assertTrue(entry.public)
    self.assertFalse(entry.failfast)
    self.assertEqual('public', entry.options)

    entry = backendinfo.BackendEntry(name='foo', options='dynamic')
    self.assertFalse(entry.public)
    self.assertTrue(entry.dynamic)
    self.assertFalse(entry.failfast)
    self.assertEqual('dynamic', entry.options)

    entry = backendinfo.BackendEntry(name='foo', options='failfast')
    self.assertFalse(entry.public)
    self.assertFalse(entry.dynamic)
    self.assertTrue(entry.failfast)
    self.assertEqual('failfast', entry.options)

    entry = backendinfo.BackendEntry(name='foo',
                                     options='public, dynamic, failfast')
    self.assertTrue(entry.public)
    self.assertTrue(entry.dynamic)
    self.assertTrue(entry.failfast)
    self.assertEqual('public, dynamic, failfast', entry.options)


    try:
      backendinfo.BackendEntry(name='foo', public=True)
      fail()
    except backendinfo.BadConfig:
      pass
    try:
      backendinfo.BackendEntry(name='foo', dynamic=True)
      fail()
    except backendinfo.BadConfig:
      pass
    try:
      backendinfo.BackendEntry(name='foo', failfast=True)
      fail()
    except backendinfo.BadConfig:
      pass


    try:
      backendinfo.BackendEntry(name='foo', options='hello')
      fail()
    except backendinfo.BadConfig:
      pass

  def testToYAML(self):

    backend = backendinfo.BackendEntry(name='s1',
                                       instances=2,
                                       start='test/foo.py',
                                       options='public, dynamic, failfast',
                                       max_concurrent_requests=5,
                                       state='START',
                                       )
    backend.set_class('B2')
    self.assertEqual('name: s1\n'
                      'class: B2\n'
                      'instances: 2\n'
                      'start: test/foo.py\n'
                      'options: public, dynamic, failfast\n'
                      'max_concurrent_requests: 5\n'
                      'state: START\n',
                      backend.ToYAML())
    backend.set_class(None)
    self.assertEqual('name: s1\n'
                      'instances: 2\n'
                      'start: test/foo.py\n'
                      'options: public, dynamic, failfast\n'
                      'max_concurrent_requests: 5\n'
                      'state: START\n',
                      backend.ToYAML())
    backend.instances = None
    self.assertEqual('name: s1\n'
                      'start: test/foo.py\n'
                      'options: public, dynamic, failfast\n'
                      'max_concurrent_requests: 5\n'
                      'state: START\n',
                      backend.ToYAML())
    backend.start = None
    self.assertEqual('name: s1\n'
                      'options: public, dynamic, failfast\n'
                      'max_concurrent_requests: 5\n'
                      'state: START\n',
                      backend.ToYAML())
    backend.options = None
    self.assertEqual('name: s1\n'
                      'max_concurrent_requests: 5\n'
                      'state: START\n',
                      backend.ToYAML())
    backend.max_concurrent_requests = None
    self.assertEqual('name: s1\n'
                      'state: START\n',
                      backend.ToYAML())
    backend.state = None
    self.assertEqual('name: s1\n',
                      backend.ToYAML())

  def testLoadBackendEntry(self):
    input_data = ('name: s1\n'
                  'class: B1\n'
                  'instances: 2\n'
                  'start: test/foo.py\n'
                  'state: START\n'
                 )
    entry = backendinfo.LoadBackendEntry(input_data)
    self.assertIsInstance(entry, backendinfo.BackendEntry)
    self.assertEqual(entry.name, 's1')
    self.assertEqual(entry.get_class(), 'B1')
    self.assertEqual(entry.instances, 2)
    self.assertEqual(entry.start, 'test/foo.py')
    self.assertEqual(entry.options, None)
    self.assertEqual(entry.public, False)
    self.assertEqual(entry.dynamic, False)
    self.assertEqual(entry.failfast, False)
    self.assertEqual(entry.state, 'START')

    self.assertRaises(backendinfo.BadConfig,
                      backendinfo.LoadBackendEntry,
                      'name: s1\n'
                      'dynamic: True\n')

    self.assertRaises(backendinfo.BadConfig,
                      backendinfo.LoadBackendEntry,
                      'name: s1\n'
                      'failfast: True\n')

    entry = backendinfo.LoadBackendEntry('name: foo\n'
                                         'options: public\n')
    self.assertEqual(entry.options, 'public')
    self.assertEqual(entry.public, True)
    self.assertEqual(entry.dynamic, False)
    self.assertEqual(entry.failfast, False)

    entry = backendinfo.LoadBackendEntry('name: foo\n'
                                         'options: dynamic\n')
    self.assertEqual(entry.options, 'dynamic')
    self.assertEqual(entry.public, False)
    self.assertEqual(entry.dynamic, True)
    self.assertEqual(entry.failfast, False)

    entry = backendinfo.LoadBackendEntry('name: foo\n'
                                         'options: failfast\n')
    self.assertEqual(entry.options, 'failfast')
    self.assertEqual(entry.public, False)
    self.assertEqual(entry.dynamic, False)
    self.assertEqual(entry.failfast, True)

    entry = backendinfo.LoadBackendEntry('name: foo\n'
                                         'options: public, dynamic, failfast\n')
    self.assertEqual(entry.options, 'public, dynamic, failfast')
    self.assertEqual(entry.public, True)
    self.assertEqual(entry.dynamic, True)
    self.assertEqual(entry.failfast, True)


class BackendInfoExternalTest(absltest.TestCase):
  """Tests for the backendinfo.BackendInfoExternal class."""

  def testLoadBackendInfo_NoBackendClause(self):
    info = backendinfo.LoadBackendInfo('')
    self.assertEqual([], info.backends)

  def testLoadBackendInfo_EmptyBackendClause(self):
    info = backendinfo.LoadBackendInfo('backends:')
    self.assertEqual([], info.backends)

  def testLoadBackendInfo(self):
    input_data = ('backends:\n'
                  '- name: s1\n'
                  '- name: s2\n'
                  '  class: B1\n'
                  '  instances: 5\n'
                  '  start: test/foo.py\n'
                  '  options: public, dynamic, failfast\n'
                 )
    info = backendinfo.LoadBackendInfo(input_data)
    self.assertEqual(2, len(info.backends))


    self.assertIsInstance(info.backends[0], backendinfo.BackendEntry)
    self.assertEqual(info.backends[0].name, 's1')
    self.assertEqual(info.backends[0].get_class(), None)
    self.assertEqual(info.backends[0].instances, None)
    self.assertEqual(info.backends[0].start, None)
    self.assertEqual(info.backends[0].options, None)
    self.assertEqual(info.backends[0].public, False)
    self.assertEqual(info.backends[0].dynamic, False)
    self.assertEqual(info.backends[0].failfast, False)


    self.assertIsInstance(info.backends[1], backendinfo.BackendEntry)
    self.assertEqual(info.backends[1].name, 's2')
    self.assertEqual(info.backends[1].get_class(), 'B1')
    self.assertEqual(info.backends[1].instances, 5)
    self.assertEqual(info.backends[1].start, 'test/foo.py')
    self.assertEqual(info.backends[1].options, 'public, dynamic, failfast')
    self.assertEqual(info.backends[1].public, True)
    self.assertEqual(info.backends[1].dynamic, True)
    self.assertEqual(info.backends[1].failfast, True)


def main(unused_argv):
  absltest.main()


if __name__ == '__main__':
  absltest.main()
