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


"""Tests for google.appengine.api.dispatchinfo."""

import re

import six

from google.appengine.api import dispatchinfo
from google.appengine.api import validation
from google.appengine.api import yaml_errors
from absl.testing import absltest




class DispatchInfoTest(absltest.TestCase):
  """Tests for the dispatchinfo.DispatchInfoExternal class."""

  def testDispatchInfoConstructor(self):
    """Test dispatchinfo.DispatchInfoExternal constructor."""
    dispatch = [dispatchinfo.DispatchEntry(url='a.b/c*', module='default'),
                dispatchinfo.DispatchEntry(url='a.b.com/d', module='e1'),
                dispatchinfo.DispatchEntry(url='*x.y.com/e', module='e2')]
    info = dispatchinfo.DispatchInfoExternal(application='app1',
                                             dispatch=dispatch)
    info.CheckInitialized()
    self.assertEqual(dispatch, info.dispatch)
    self.assertEqual('app1', info.application)

  def testDispatchInfoConstructorUsesService(self):
    """Test dispatchinfo.DispatchInfoExternal constructor.

    Use 'service' instead of 'module'.
    """
    dispatch = [dispatchinfo.DispatchEntry(url='a.b/c*', service='default'),
                dispatchinfo.DispatchEntry(url='a.b.com/d', service='e1'),
                dispatchinfo.DispatchEntry(url='*x.y.com/e', service='e2')]
    info = dispatchinfo.DispatchInfoExternal(application='app1',
                                             dispatch=dispatch)
    info.CheckInitialized()
    self.assertEqual(dispatch, info.dispatch)
    self.assertEqual('app1', info.application)

  def testDispatchInfoConstructorInvalidapplication(self):
    """Test an invalid application.

       Application is using appinfo.APPLICATION_RE_STRING which is tested
       with appinfo_unittest.py.
    """
    self.assertRaises(
        validation.ValidationError,
        dispatchinfo.DispatchInfoExternal,
        application='-app1')

  def testDispatchConstructorEmpty(self):
    """Test dispatchinfo.DispatchInfoExternal constructor with no arguments."""
    info = dispatchinfo.DispatchInfoExternal()
    info.CheckInitialized()
    self.assertEqual(None, info.application)
    self.assertEqual(None, info.dispatch)


class ParsedUrlTest(absltest.TestCase):
  """Tests for dispatchinfo.ParsedURL class."""

  def Validate(self, host_pattern, host, path_pattern, path):
    holder = dispatchinfo.ParsedURL(host_pattern + path_pattern)
    self.assertEqual(host_pattern, holder.host_pattern)
    self.assertEqual(host, holder.host)
    self.assertEqual(not six.ensure_str(host_pattern).startswith('*'),
                     holder.host_exact)
    self.assertEqual(path_pattern, holder.path_pattern)
    self.assertEqual(path, holder.path)
    self.assertEqual(not six.ensure_str(path_pattern).endswith('*'),
                     holder.path_exact)

  def testExact(self):
    """Verify url pattern with exact host and path."""
    self.Validate('a.b.com', 'a.b.com', '/x/y', '/x/y')

  def testExactMinimal(self):
    """Verify url pattern with minimal exact host and path."""
    self.Validate('a', 'a', '/', '/')

  def testNotExact(self):
    """Verify url pattern with pattern host and path."""
    self.Validate('*a.b.com', 'a.b.com', '/x/y*', '/x/y')

  def testNotExactMinimal(self):
    """Verify url pattern with minimal pattern host and path."""
    self.Validate('*', '', '/*', '/')

  def testInvlid(self):
    """Verify an invlid url pattern causes a validation error."""
    self.assertRaises(validation.ValidationError, dispatchinfo.ParsedURL,
                      url_pattern='/')


class DispatchEntryTest(absltest.TestCase):
  """Tests for dispatchinfo.DispatchEntry class."""

  def VerifyValidUrl(self, url):
    """Verify dispatchinfo.DispatchEntry constructor accepts url."""
    entry = dispatchinfo.DispatchEntry(url=url, module='module1')
    entry.CheckInitialized()
    self.assertEqual(entry.url, url)
    self.assertEqual(entry.module, 'module1')

  def VerifyInvalidHost(self, host):
    """Verify dispatchinfo.DispatchEntry constructor rejects host."""
    self.VerifyInvalidUrl(six.ensure_str(host) + '/path')

  def VerifyInvalidUrl(self, url):
    """Verify dispatchinfo.DispatchEntry constructor rejects url."""
    self.assertRaises(validation.ValidationError, dispatchinfo.DispatchEntry,
                      url=url, module='module1')

  def VerifyInvalidModule(self, module):
    """Verify dispatchinfo.DispatchEntry constructor rejects module."""
    self.assertRaises(validation.ValidationError, dispatchinfo.DispatchEntry,
                      url='a/b', module=module)

  def testDispatchEntryConstructorValidUrl(self):
    """Test valid URLsvalid URLs."""
    self.VerifyValidUrl('*/*')
    self.VerifyValidUrl('*a/*')
    self.VerifyValidUrl('*5/*')
    self.VerifyValidUrl('*544/*')
    self.VerifyValidUrl('*-a/*')
    self.VerifyValidUrl('*--a/*')
    self.VerifyValidUrl('*-4/*')
    self.VerifyValidUrl('*--55/*')
    self.VerifyValidUrl('*a.b/*')
    self.VerifyValidUrl('*-a.4b/*')
    self.VerifyValidUrl('*-a.b/*')
    self.VerifyValidUrl('*a.b4/*')
    self.VerifyValidUrl('*--a.b/*')
    self.VerifyValidUrl('*--a.45/*')
    self.VerifyValidUrl('*a.b--c/*')
    self.VerifyValidUrl('*1.23--c/*')
    self.VerifyValidUrl('*1.23a.c/*')
    self.VerifyValidUrl('*-a.b---c/*')
    self.VerifyValidUrl('*--a.b-c/*')
    self.VerifyValidUrl('*a.b--c.d/*')
    self.VerifyValidUrl('*-a.b---c.d.e/*')
    self.VerifyValidUrl('*--a.b-c.xx--yyy-zz/*')
    self.VerifyValidUrl('*--a.b-c.4x--yy-zz/*')
    self.VerifyValidUrl('*1.2.3.4/*')

    self.VerifyValidUrl('a/a*')
    self.VerifyValidUrl('ab/a*')
    self.VerifyValidUrl('ab-c/a*')
    self.VerifyValidUrl('ab--c/a*')
    self.VerifyValidUrl('ab----c/a*')
    self.VerifyValidUrl('ab.cd/a*')
    self.VerifyValidUrl('ab.c-d/a*')
    self.VerifyValidUrl('ab.cc-dd--eee.f/a*')
    self.VerifyValidUrl('ab--c--c.d-ee--ff/a*')
    self.VerifyValidUrl('0a/a')
    self.VerifyValidUrl('0-0/a')
    self.VerifyValidUrl('0a-a/a')
    self.VerifyValidUrl('0a.0a/a')
    self.VerifyValidUrl('0-0.0a/a')
    self.VerifyValidUrl('0a-a.0a/a')
    self.VerifyValidUrl('0/a')
    self.VerifyValidUrl('0.1/a')
    self.VerifyValidUrl('0.1.2/a')
    self.VerifyValidUrl('0.1.2.3.4/a')
    self.VerifyValidUrl('0.1.2.256/a')
    self.VerifyValidUrl('*/')
    self.VerifyValidUrl('a/')

  def testDispatchEntryConstructorInvalidUrl(self):
    """Test invalid urls."""
    self.VerifyInvalidUrl('')
    self.VerifyInvalidUrl('/')
    self.VerifyInvalidUrl('/*')
    self.VerifyInvalidUrl('/a')

  def testDispatchEntryConstructorInvalidUrlHostSuffixPatterns(self):
    """Test invalid host suffix patterns."""
    self.VerifyInvalidHost('*a-')
    self.VerifyInvalidHost('*a.')
    self.VerifyInvalidHost('*a-.')
    self.VerifyInvalidHost('*a.-')
    self.VerifyInvalidHost('*a.-a')
    self.VerifyInvalidHost('*a.-ab')
    self.VerifyInvalidHost('*a.a-')
    self.VerifyInvalidHost('*a.ab-')
    self.VerifyInvalidHost('*a.ab-c.')
    self.VerifyInvalidHost('*a.ab-c.-')
    self.VerifyInvalidHost('*a.ab-c.a-')
    self.VerifyInvalidHost('*a.ab-c.a-b.')
    self.VerifyInvalidHost('*a.ab-c.a-b....')
    self.VerifyInvalidHost('*-')
    self.VerifyInvalidHost('*.')
    self.VerifyInvalidHost('*-.')
    self.VerifyInvalidHost('*.-')
    self.VerifyInvalidHost('*.-a')
    self.VerifyInvalidHost('*.-ab')
    self.VerifyInvalidHost('*.a-')
    self.VerifyInvalidHost('*.ab-')
    self.VerifyInvalidHost('*.ab-c.')
    self.VerifyInvalidHost('*.ab-c.-')
    self.VerifyInvalidHost('*.ab-c.a-')
    self.VerifyInvalidHost('*.ab-c.a-b.')
    self.VerifyInvalidHost('*.ab-c.a-b....')

  def testDispatchEntryConstructorInvalidUrlHostExactPatterns(self):
    """Test invalid host exact patterns."""
    self.VerifyInvalidHost('-')
    self.VerifyInvalidHost('-a')
    self.VerifyInvalidHost('-aa')
    self.VerifyInvalidHost('.')
    self.VerifyInvalidHost('.a')
    self.VerifyInvalidHost('.aa')
    self.VerifyInvalidHost('a-')
    self.VerifyInvalidHost('aa-')
    self.VerifyInvalidHost('a--')
    self.VerifyInvalidHost('a.')
    self.VerifyInvalidHost('aa.')
    self.VerifyInvalidHost('a..')
    self.VerifyInvalidHost('a-.')
    self.VerifyInvalidHost('a-.b')
    self.VerifyInvalidHost('a-b.')
    self.VerifyInvalidHost('a-b.-')
    self.VerifyInvalidHost('a-b..')
    self.VerifyInvalidHost('a-b.a.')
    self.VerifyInvalidHost('a-b.0.')
    self.VerifyInvalidHost('a-b.a-')
    self.VerifyInvalidHost('a-b.1-')
    self.VerifyInvalidHost('a-b.aa.')
    self.VerifyInvalidHost('a-b.aa-')
    self.VerifyInvalidHost('a-b.a-b.')
    self.VerifyInvalidHost('a-b.a-b-')
    self.VerifyInvalidHost('a-b..a-b')
    self.VerifyInvalidHost('0.1.2.3')

  def testDispatchEntryConstructorInvalidModule(self):
    """Test module values.

       Spot checking as appinfo.APPLICATION_RE_STRING pattern tests go with
       appinfo_unittest.py
    """


    self.VerifyInvalidModule('')


class LoadSingleDispatchTest(absltest.TestCase):
  """Tests for loading yaml files."""

  def testLoaderSaneFile(self):
    input_data = """
    application: guestbook
    dispatch:
    - url: a.b.eric.com/c
      module: default
    - url: "*x/larry*"
      module: module1
    """
    config = dispatchinfo.LoadSingleDispatch(input_data)
    self.assertEqual('guestbook', config.application)
    self.assertLen(config.dispatch, 2)
    self.assertIsInstance(config.dispatch[0], dispatchinfo.DispatchEntry)
    self.assertIsInstance(config.dispatch[1], dispatchinfo.DispatchEntry)
    self.assertEqual(config.dispatch[0].url, 'a.b.eric.com/c')
    self.assertEqual(config.dispatch[0].module, 'default')
    self.assertEqual(config.dispatch[0].service, 'default')
    self.assertEqual(config.dispatch[1].url, '*x/larry*')
    self.assertEqual(config.dispatch[1].module, 'module1')
    self.assertEqual(config.dispatch[1].service, 'module1')

  def testLoaderSaneFileUsesService(self):
    input_data = """
    application: guestbook
    dispatch:
    - url: a.b.eric.com/c
      service: default
    - url: "*x/larry*"
      service: module1
    """
    config = dispatchinfo.LoadSingleDispatch(input_data)
    self.assertEqual('guestbook', config.application)
    self.assertLen(config.dispatch, 2)
    self.assertIsInstance(config.dispatch[0], dispatchinfo.DispatchEntry)
    self.assertIsInstance(config.dispatch[1], dispatchinfo.DispatchEntry)


    self.assertEqual(config.dispatch[0].url, 'a.b.eric.com/c')
    self.assertEqual(config.dispatch[0].module, 'default')
    self.assertEqual(config.dispatch[0].service, 'default')
    self.assertEqual(config.dispatch[1].url, '*x/larry*')
    self.assertEqual(config.dispatch[1].module, 'module1')
    self.assertEqual(config.dispatch[1].service, 'module1')

  def testLoaderInvalidDispatchBothModuleAndService(self):
    input_data = """
    dispatch:
    - url: a.b.eric.com/c
      module: default
      service: default
    """
    with self.assertRaisesRegex(
        yaml_errors.EventError, re.escape(
            r'Only one of the two fields [service] (preferred) and [module] '
            r'(deprecated) may be set.')):
      dispatchinfo.LoadSingleDispatch(input_data)

  def testLoaderInvalidDispatchNeitherModuleNorService(self):
    input_data = """
    dispatch:
    - url: a.b.eric.com/c
    """
    with self.assertRaisesRegex(
        yaml_errors.EventError,
        re.escape(r'Missing required value [service].')):
      dispatchinfo.LoadSingleDispatch(input_data)

  def testLoaderSaneFileNoApplication(self):
    input_data = """
    dispatch:
    - url: a.b.eric.com/c
      module: default
    """
    config = dispatchinfo.LoadSingleDispatch(input_data)
    self.assertEqual(None, config.application)
    self.assertLen(config.dispatch, 1)
    self.assertIsInstance(config.dispatch[0], dispatchinfo.DispatchEntry)
    self.assertEqual(config.dispatch[0].url, 'a.b.eric.com/c')
    self.assertEqual(config.dispatch[0].module, 'default')

  def testLoaderEmptyFile(self):
    """Test for loading an empty yaml file."""
    config = dispatchinfo.LoadSingleDispatch('')
    config.CheckInitialized()
    self.assertEqual(None, config.application)
    self.assertEqual(None, config.dispatch)

  def testLoaderMultipleDocuments(self):
    input_data = """---
application: guestbook
dispatch:
  - url: a.b.eric.com/c
    module: default
  - url: "*x/larry*"
    module: module1
---
application: snippets
"""
    self.assertRaises(dispatchinfo.MalformedDispatchConfigurationError,
                      dispatchinfo.LoadSingleDispatch,
                      input_data)

  def testLoaderMultipleApplications(self):
    input_data = """
    application: guestbook
    application: guestbook2
    dispatch:
    - url: a.b.eric.com/c
      module: default
    """
    self.assertRaises(yaml_errors.EventError,
                      dispatchinfo.LoadSingleDispatch,
                      input_data)

  def testLoaderMultipleDispatches(self):
    input_data = """
    application: guestbook
    dispatch:
    - url: a.b.eric.com/c
      module: default
    dispatch:
    - url: user.com/c
      module: default
    """
    self.assertRaises(yaml_errors.EventError,
                      dispatchinfo.LoadSingleDispatch,
                      input_data)


if __name__ == '__main__':
  absltest.main()
