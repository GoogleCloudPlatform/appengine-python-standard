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
"""Tests for google.appengine.api.modules.modules_stub."""
import logging

import google
import mox

from absl.testing import absltest
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import request_info
from google.appengine.api.modules import modules
from google.appengine.api.modules import modules_stub


class ModulesStubTest(absltest.TestCase):

  def setUp(self):
    self.mox = mox.Mox()
    self.request_data = self.mox.CreateMock(request_info.RequestInfo)
    self.dispatcher = self.mox.CreateMock(request_info.Dispatcher)
    self.stub = modules_stub.ModulesServiceStub(self.request_data)
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.GetDefaultAPIProxy()
    apiproxy_stub_map.apiproxy.RegisterStub('modules', self.stub)

  def tearDown(self):
    self.mox.UnsetStubs()

  def testGetModules(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_module_names().AndReturn(['default', 'other'])
    self.mox.ReplayAll()
    self.assertEqual(['default', 'other'], modules.get_modules())
    self.mox.VerifyAll()

  def testGetVersions(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_versions('default').AndReturn(['1', '2'])
    self.mox.ReplayAll()
    self.assertEqual(['1', '2'], modules.get_versions('default'))
    self.mox.VerifyAll()

  def testGetVersions_CurrentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.dispatcher.get_versions('default').AndReturn(['1', '2'])
    self.mox.ReplayAll()
    self.assertEqual(['1', '2'], modules.get_versions())
    self.mox.VerifyAll()

  def testGetVersions_ModuleDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_versions('default').AndRaise(
        request_info.ModuleDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidModuleError,
                      modules.get_versions, 'default')
    self.mox.VerifyAll()

  def testGetDefaultVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_default_version('default').AndReturn('1')
    self.mox.ReplayAll()
    self.assertEqual('1', modules.get_default_version('default'))
    self.mox.VerifyAll()

  def testGetDefaultVersion_CurrentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.dispatcher.get_default_version('default').AndReturn('1')
    self.mox.ReplayAll()
    self.assertEqual('1', modules.get_default_version())
    self.mox.VerifyAll()

  def testGetDefaultVersion_ModuleDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_default_version('default').AndRaise(
        request_info.ModuleDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidModuleError,
                      modules.get_default_version, 'default')
    self.mox.VerifyAll()

  def testGetNumInstances(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_num_instances('default', '1').AndReturn(5)
    self.mox.ReplayAll()
    self.assertEqual(5, modules.get_num_instances('default', '1'))
    self.mox.VerifyAll()

  def testGetNumInstances_CurrentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.dispatcher.get_num_instances('default', '1').AndReturn(5)
    self.mox.ReplayAll()
    self.assertEqual(5, modules.get_num_instances(version='1'))
    self.mox.VerifyAll()

  def testGetNumInstances_CurrentVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('default').AndReturn(['1'])
    self.dispatcher.get_num_instances('default', '1').AndReturn(5)
    self.mox.ReplayAll()
    self.assertEqual(5, modules.get_num_instances(module='default'))
    self.mox.VerifyAll()

  def testGetNumInstances_CurrentVersionDifferentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('other').AndReturn(['1'])
    self.dispatcher.get_num_instances('other', '1').AndReturn(5)
    self.mox.ReplayAll()
    self.assertEqual(5, modules.get_num_instances(module='other'))
    self.mox.VerifyAll()

  def testGetNumInstances_CurrentVersionDoesNotExistInOtherModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('other').AndReturn(['2'])
    self.dispatcher.get_default_version('other').AndReturn('2')
    self.dispatcher.get_num_instances('other', '2').AndReturn(5)
    self.mox.ReplayAll()
    self.assertEqual(5, modules.get_num_instances(module='other'))
    self.mox.VerifyAll()

  def testGetNumInstances_CurrentModuleAndVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('default').AndReturn(['1'])
    self.dispatcher.get_num_instances('default', '1').AndReturn(5)
    self.mox.ReplayAll()
    self.assertEqual(5, modules.get_num_instances())
    self.mox.VerifyAll()

  def testGetNumInstances_ModuleDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('fake').AndRaise(
        request_info.ModuleDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.get_num_instances, module='fake')
    self.mox.VerifyAll()

  def testGetNumInstances_VersionDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_num_instances('fake', '1').AndRaise(
        request_info.VersionDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.get_num_instances, module='fake', version='1')
    self.mox.VerifyAll()

  def testGetNumInstances_AutoScaled(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_num_instances('default', '1').AndRaise(
        request_info.NotSupportedWithAutoScalingError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.get_num_instances, module='default', version='1')
    self.mox.VerifyAll()

  def testSetNumInstances(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.set_num_instances('default', '1', 2)
    self.mox.ReplayAll()
    modules.set_num_instances(2, 'default', '1')
    self.mox.VerifyAll()

  def testSetNumInstances_CurrentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.dispatcher.set_num_instances('default', '1', 2)
    self.mox.ReplayAll()
    modules.set_num_instances(version='1', instances=2)
    self.mox.VerifyAll()

  def testSetNumInstances_CurrentVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('default').AndReturn(['1'])
    self.dispatcher.set_num_instances('default', '1', 2)
    self.mox.ReplayAll()
    modules.set_num_instances(module='default', instances=2)
    self.mox.VerifyAll()

  def testSetNumInstances_CurrentVersionDifferentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('other').AndReturn(['1'])
    self.dispatcher.set_num_instances('other', '1', 2)
    self.mox.ReplayAll()
    modules.set_num_instances(module='other', instances=2)
    self.mox.VerifyAll()

  def testSetNumInstances_CurrentVersionDoesNotExistInOtherModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('other').AndReturn(['2'])
    self.dispatcher.get_default_version('other').AndReturn('2')
    self.dispatcher.set_num_instances('other', '2', 2)
    self.mox.ReplayAll()
    modules.set_num_instances(module='other', instances=2)
    self.mox.VerifyAll()

  def testSetNumInstances_CurrentModuleAndVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('default').AndReturn(['1'])
    self.dispatcher.set_num_instances('default', '1', 2)
    self.mox.ReplayAll()
    modules.set_num_instances(instances=2)
    self.mox.VerifyAll()

  def testSetNumInstances_ModuleDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.set_num_instances('fake', '1', 2).AndRaise(
        request_info.VersionDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.set_num_instances, 2, 'fake', '1')
    self.mox.VerifyAll()

  def testSetNumInstances_VersionDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.set_num_instances('fake', '1', 2).AndRaise(
        request_info.VersionDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.set_num_instances, 2, 'fake', '1')
    self.mox.VerifyAll()

  def testSetNumInstances_AutoScaled(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.set_num_instances('default', '1', 2).AndRaise(
        request_info.NotSupportedWithAutoScalingError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError, modules.set_num_instances,
                      module='default', version='1', instances=2)
    self.mox.VerifyAll()

  def testStartVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.start_version('default', '1').AndReturn(5)
    self.mox.ReplayAll()
    modules.start_version('default', '1')
    self.mox.VerifyAll()

  def testStartVersion_ModuleDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.start_version('fake', '1').AndRaise(
        request_info.ModuleDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.start_version, module='fake', version='1')
    self.mox.VerifyAll()

  def testStartVersion_VersionDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.start_version('fake', '1').AndRaise(
        request_info.VersionDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.start_version, module='fake', version='1')
    self.mox.VerifyAll()

  def testStartVersion_AutoScaled(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.start_version('default', '1').AndRaise(
        request_info.NotSupportedWithAutoScalingError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.start_version, module='default', version='1')
    self.mox.VerifyAll()

  def testStartVersion_AlreadyStarted(self):
    """Tests that no error is raised if the version is already started."""
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.start_version('default', '1').AndRaise(
        request_info.VersionAlreadyStartedError)
    self.mox.StubOutWithMock(logging, 'info')
    logging.info('The specified module: default, version: 1 is already '
                 'started.')
    self.mox.ReplayAll()
    modules.start_version(module='default', version='1')
    self.mox.VerifyAll()

  def testStopVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.stop_version('default', '1').AndReturn(5)
    self.mox.ReplayAll()
    modules.stop_version('default', '1')
    self.mox.VerifyAll()

  def testStopVersion_CurrentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.dispatcher.stop_version('default', '1').AndReturn(5)
    self.mox.ReplayAll()
    modules.stop_version(version='1')
    self.mox.VerifyAll()

  def testStopVersion_CurrentVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('default').AndReturn(['1'])
    self.dispatcher.stop_version('default', '1').AndReturn(5)
    self.mox.ReplayAll()
    modules.stop_version(module='default')
    self.mox.VerifyAll()

  def testStopVersion_CurrentVersionDifferentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('other').AndReturn(['1'])
    self.dispatcher.stop_version('other', '1').AndReturn(5)
    self.mox.ReplayAll()
    modules.stop_version(module='other')
    self.mox.VerifyAll()

  def testStopVersion_CurrentVersionDoesNotExistInOtherModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('other').AndReturn(['2'])
    self.dispatcher.get_default_version('other').AndReturn('2')
    self.dispatcher.stop_version('other', '2').AndReturn(5)
    self.mox.ReplayAll()
    modules.stop_version(module='other')
    self.mox.VerifyAll()

  def testStopVersion_CurrentModuleAndVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('default').AndReturn(['1'])
    self.dispatcher.stop_version('default', '1').AndReturn(5)
    self.mox.ReplayAll()
    modules.stop_version()
    self.mox.VerifyAll()

  def testStopVersion_ModuleDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('fake').AndRaise(
        request_info.ModuleDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.stop_version, module='fake')
    self.mox.VerifyAll()

  def testStopVersion_VersionDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.stop_version('fake', '1').AndRaise(
        request_info.VersionDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.stop_version, module='fake', version='1')
    self.mox.VerifyAll()

  def testStopVersion_AutoScaled(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.stop_version('default', '1').AndRaise(
        request_info.NotSupportedWithAutoScalingError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidVersionError,
                      modules.stop_version, module='default', version='1')
    self.mox.VerifyAll()

  def testStopVersion_AlreadyStopped(self):
    """Tests that no error is raised if the version is already stopped."""
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.stop_version('default', '1').AndRaise(
        request_info.VersionAlreadyStoppedError)
    self.mox.StubOutWithMock(logging, 'info')
    logging.info('The specified module: default, version: 1 is already '
                 'stopped.')
    self.mox.ReplayAll()
    modules.stop_version('default', '1')
    self.mox.VerifyAll()

  def testGetHostname(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_hostname('default', '1', '0').AndReturn(
        'localhost:8080')
    self.mox.ReplayAll()
    self.assertEqual('localhost:8080', modules.get_hostname('default', '1',
                                                            '0'))
    self.mox.VerifyAll()

  def testGetHostname_LoadBalancedHostname(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_hostname('default', '1', None).AndReturn(
        'localhost:8080')
    self.mox.ReplayAll()
    self.assertEqual('localhost:8080', modules.get_hostname('default', '1'))
    self.mox.VerifyAll()

  def testGetHostname_CurrentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.dispatcher.get_hostname('default', '1', None).AndReturn(
        'localhost:8080')
    self.mox.ReplayAll()
    self.assertEqual('localhost:8080', modules.get_hostname(version='1'))
    self.mox.VerifyAll()

  def testGetHostname_CurrentVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('default').AndReturn(['1'])
    self.dispatcher.get_hostname('default', '1', None).AndReturn(
        'localhost:8080')
    self.mox.ReplayAll()
    self.assertEqual('localhost:8080', modules.get_hostname(module='default'))
    self.mox.VerifyAll()

  def testGetHostname_CurrentVersionDifferentModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('other').AndReturn(['1'])
    self.dispatcher.get_hostname('other', '1', None).AndReturn('localhost:8080')
    self.mox.ReplayAll()
    self.assertEqual('localhost:8080', modules.get_hostname(module='other'))
    self.mox.VerifyAll()

  def testGetHostname_CurrentVersionDoesNotExistInOtherModule(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('other').AndReturn(['2'])
    self.dispatcher.get_default_version('other').AndReturn('2')
    self.dispatcher.get_hostname('other', '2', None).AndReturn('localhost:8080')
    self.mox.ReplayAll()
    self.assertEqual('localhost:8080', modules.get_hostname(module='other'))
    self.mox.VerifyAll()

  def testGetHostname_CurrentModuleAndVersion(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_module(None).AndReturn('default')
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('default').AndReturn(['1'])
    self.dispatcher.get_hostname('default', '1',
                                 None).AndReturn('localhost:8080')
    self.mox.ReplayAll()
    self.assertEqual('localhost:8080', modules.get_hostname())
    self.mox.VerifyAll()

  def testGetHostname_ModuleDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.request_data.get_version(None).AndReturn('1')
    self.dispatcher.get_versions('fake').AndRaise(
        request_info.ModuleDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidModuleError,
                      modules.get_hostname, module='fake')
    self.mox.VerifyAll()

  def testGetHostname_VersionDoesNotExist(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_hostname('fake', '1', None).AndRaise(
        request_info.VersionDoesNotExistError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidModuleError,
                      modules.get_hostname, module='fake', version='1')
    self.mox.VerifyAll()

  def testGetHostname_InvalidInstance(self):
    self.request_data.get_dispatcher().AndReturn(self.dispatcher)
    self.dispatcher.get_hostname('default', '1', '20').AndRaise(
        request_info.InvalidInstanceIdError)
    self.mox.ReplayAll()
    self.assertRaises(modules.InvalidInstancesError, modules.get_hostname,
                      module='default', version='1', instance='20')
    self.mox.VerifyAll()


if __name__ == '__main__':
  absltest.main()
