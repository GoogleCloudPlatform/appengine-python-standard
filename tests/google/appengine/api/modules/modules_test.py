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
"""Tests for google.appengine.api.modules."""

import logging
import os

import google

from google.appengine.api.modules import modules
from google.appengine.api.modules import modules_service_pb2
from google.appengine.runtime import apiproxy_errors
from google.appengine.runtime.context import ctx_test_util
import mox

from absl.testing import absltest


@ctx_test_util.isolated_context()
class ModulesTest(absltest.TestCase):

  def setUp(self):
    """Setup testing environment."""
    self.mox = mox.Mox()

  def tearDown(self):
    """Tear down testing environment."""
    self.mox.VerifyAll()
    self.mox.UnsetStubs()

  def testGetCurrentModuleName_DefaultModule(self):
    """Test get_current_module_name for default engine."""
    os.environ['CURRENT_MODULE_ID'] = 'default'
    os.environ['CURRENT_VERSION_ID'] = 'v1.123'
    self.assertEqual('default', modules.get_current_module_name())

  def testGetCurrentModuleName_NonDefaultModule(self):
    """Test get_current_module_name for a non default engine."""
    os.environ['CURRENT_MODULE_ID'] = 'module1'
    os.environ['CURRENT_VERSION_ID'] = 'v1.123'
    self.assertEqual('module1', modules.get_current_module_name())

  def testGetCurrentModuleName_GaeService(self):
    """Test get_current_module_name from GAE_SERVICE."""
    os.environ['GAE_SERVICE'] = 'module1'
    os.environ['GAE_VERSION'] = 'v1'
    self.assertEqual('module1', modules.get_current_module_name())

  def testGetCurrentVersionName_DefaultModule(self):
    """Test get_current_version_name for default engine."""
    os.environ['CURRENT_VERSION_ID'] = 'v1.123'
    self.assertEqual('v1', modules.get_current_version_name())

  def testGetCurrentVersionName_NonDefaultModule(self):
    """Test get_current_version_name for a non default engine."""
    os.environ['CURRENT_MODULE_ID'] = 'module1'
    os.environ['CURRENT_VERSION_ID'] = 'v1.123'
    self.assertEqual('v1', modules.get_current_version_name())

  def testGetCurrentVersionName_VersionIdContainsNone(self):
    """Test get_current_version_name when 'None' is in version id."""
    os.environ['CURRENT_MODULE_ID'] = 'module1'
    os.environ['CURRENT_VERSION_ID'] = 'None.123'
    self.assertEqual(None, modules.get_current_version_name())

  def testGetCurrentVersionName_GaeVersion(self):
    """Test get_current_module_name from GAE_SERVICE."""
    os.environ['GAE_SERVICE'] = 'module1'
    os.environ['GAE_VERSION'] = 'v1'
    self.assertEqual('v1', modules.get_current_version_name())

  def testGetCurrentInstanceId_Empty(self):
    """Test get_current_instance_id when none has been set in the environ."""
    self.assertEqual(None, modules.get_current_instance_id())

  def testGetCurrentInstanceId(self):
    """Test get_current_instance_id."""
    os.environ['INSTANCE_ID'] = '123'
    self.assertEqual('123', modules.get_current_instance_id())

  def testGetCurrentInstanceId_GaeInstance(self):
    """Test get_current_instance_id."""
    os.environ['GAE_INSTANCE'] = '123'
    self.assertEqual('123', modules.get_current_instance_id())

  def SetSuccessExpectations(self, method, expected_request, service_response):
    rpc = MockRpc(method, expected_request, service_response)
    self.mox.StubOutWithMock(modules, '_GetRpc')
    modules._GetRpc().AndReturn(rpc)
    self.mox.ReplayAll()

  def SetExceptionExpectations(self, method, expected_request,
                               application_error_number):
    rpc = MockRpc(method, expected_request, None, application_error_number)
    self.mox.StubOutWithMock(modules, '_GetRpc')
    modules._GetRpc().AndReturn(rpc)
    self.mox.ReplayAll()

  def testGetModules(self):
    """Test we return the expected results."""
    service_response = modules_service_pb2.GetModulesResponse()
    service_response.module.append('module1')
    service_response.module.append('module2')
    self.SetSuccessExpectations('GetModules',
                                modules_service_pb2.GetModulesRequest(),
                                service_response)
    self.assertEqual(['module1', 'module2'], modules.get_modules())

  def testGetVersions(self):
    """Test we return the expected results."""
    expected_request = modules_service_pb2.GetVersionsRequest()
    expected_request.module = 'module1'
    service_response = modules_service_pb2.GetVersionsResponse()
    service_response.version.append('v1')
    service_response.version.append('v2')
    self.SetSuccessExpectations('GetVersions',
                                expected_request,
                                service_response)
    self.assertEqual(['v1', 'v2'], modules.get_versions('module1'))

  def testGetVersions_NoModule(self):
    """Test we return the expected results when no module is passed."""
    expected_request = modules_service_pb2.GetVersionsRequest()
    service_response = modules_service_pb2.GetVersionsResponse()
    service_response.version.append('v1')
    service_response.version.append('v2')
    self.SetSuccessExpectations('GetVersions',
                                expected_request,
                                service_response)
    self.assertEqual(['v1', 'v2'], modules.get_versions())

  def testGetVersions_InvalidModuleError(self):
    """Test we raise the right error when the given module is invalid."""
    self.SetExceptionExpectations(
        'GetVersions', modules_service_pb2.GetVersionsRequest(),
        modules_service_pb2.ModulesServiceError.INVALID_MODULE)
    self.assertRaises(modules.InvalidModuleError, modules.get_versions)

  def testGetVersions_TransientError(self):
    """Test we raise the right error when a transient error is encountered."""
    self.SetExceptionExpectations(
        'GetVersions', modules_service_pb2.GetVersionsRequest(),
        modules_service_pb2.ModulesServiceError.TRANSIENT_ERROR)
    self.assertRaises(modules.TransientError, modules.get_versions)

  def testGetDefaultVersion(self):
    """Test we return the expected results."""
    expected_request = modules_service_pb2.GetDefaultVersionRequest()
    expected_request.module = 'module1'
    service_response = modules_service_pb2.GetDefaultVersionResponse()
    service_response.version = 'v1'
    self.SetSuccessExpectations('GetDefaultVersion',
                                expected_request,
                                service_response)
    self.assertEqual('v1', modules.get_default_version('module1'))

  def testGetDefaultVersion_NoModule(self):
    """Test we return the expected results when no module is passed."""
    expected_request = modules_service_pb2.GetDefaultVersionRequest()
    service_response = modules_service_pb2.GetDefaultVersionResponse()
    service_response.version = 'v1'
    self.SetSuccessExpectations('GetDefaultVersion',
                                expected_request,
                                service_response)
    self.assertEqual('v1', modules.get_default_version())

  def testGetDefaultVersion_InvalidModuleError(self):
    """Test we raise an error when one is received from the lower API."""
    self.SetExceptionExpectations(
        'GetDefaultVersion', modules_service_pb2.GetDefaultVersionRequest(),
        modules_service_pb2.ModulesServiceError.INVALID_MODULE)
    self.assertRaises(modules.InvalidModuleError, modules.get_default_version)

  def testGetDefaultVersion_InvalidVersionError(self):
    """Test we raise an error when one is received from the lower API."""
    self.SetExceptionExpectations(
        'GetDefaultVersion', modules_service_pb2.GetDefaultVersionRequest(),
        modules_service_pb2.ModulesServiceError.INVALID_VERSION)
    self.assertRaises(modules.InvalidVersionError, modules.get_default_version)

  def testGetNumInstances(self):
    """Test we return the expected results."""
    expected_request = modules_service_pb2.GetNumInstancesRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    service_response = modules_service_pb2.GetNumInstancesResponse()
    service_response.instances = 11
    self.SetSuccessExpectations('GetNumInstances',
                                expected_request,
                                service_response)
    self.assertEqual(11, modules.get_num_instances('module1', 'v1'))

  def testGetNumInstances_NoVersion(self):
    """Test we return the expected results when no version is passed."""
    expected_request = modules_service_pb2.GetNumInstancesRequest()
    expected_request.module = 'module1'
    service_response = modules_service_pb2.GetNumInstancesResponse()
    service_response.instances = 11
    self.SetSuccessExpectations('GetNumInstances',
                                expected_request,
                                service_response)
    self.assertEqual(11, modules.get_num_instances('module1'))

  def testGetNumInstances_NoModule(self):
    """Test we return the expected results when no module is passed."""
    expected_request = modules_service_pb2.GetNumInstancesRequest()
    expected_request.version = 'v1'
    service_response = modules_service_pb2.GetNumInstancesResponse()
    service_response.instances = 11
    self.SetSuccessExpectations('GetNumInstances',
                                expected_request,
                                service_response)
    self.assertEqual(11, modules.get_num_instances(version='v1'))

  def testGetNumInstances_AllDefaults(self):
    """Test we return the expected results when no args are passed."""
    expected_request = modules_service_pb2.GetNumInstancesRequest()
    service_response = modules_service_pb2.GetNumInstancesResponse()
    service_response.instances = 11
    self.SetSuccessExpectations('GetNumInstances',
                                expected_request,
                                service_response)
    self.assertEqual(11, modules.get_num_instances())

  def testGetNumInstances_InvalidVersionError(self):
    """Test we raise the expected error when the API call fails."""
    expected_request = modules_service_pb2.GetNumInstancesRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    self.SetExceptionExpectations(
        'GetNumInstances', expected_request,
        modules_service_pb2.ModulesServiceError.INVALID_VERSION)
    self.assertRaises(modules.InvalidVersionError,
                      modules.get_num_instances, 'module1', 'v1')

  def testSetNumInstances(self):
    """Test we return the expected results."""
    expected_request = modules_service_pb2.SetNumInstancesRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    expected_request.instances = 12
    service_response = modules_service_pb2.SetNumInstancesResponse()
    self.SetSuccessExpectations('SetNumInstances',
                                expected_request,
                                service_response)
    modules.set_num_instances(12, 'module1', 'v1')

  def testSetNumInstances_NoVersion(self):
    """Test we return the expected results when no version is passed."""
    expected_request = modules_service_pb2.SetNumInstancesRequest()
    expected_request.module = 'module1'
    expected_request.instances = 13
    service_response = modules_service_pb2.SetNumInstancesResponse()
    self.SetSuccessExpectations('SetNumInstances',
                                expected_request,
                                service_response)
    modules.set_num_instances(13, 'module1')

  def testSetNumInstances_NoModule(self):
    """Test we return the expected results when no module is passed."""
    expected_request = modules_service_pb2.SetNumInstancesRequest()
    expected_request.version = 'v1'
    expected_request.instances = 14
    service_response = modules_service_pb2.SetNumInstancesResponse()
    self.SetSuccessExpectations('SetNumInstances',
                                expected_request,
                                service_response)
    modules.set_num_instances(14, version='v1')

  def testSetNumInstances_AllDefaults(self):
    """Test we return the expected results when no args are passed."""
    expected_request = modules_service_pb2.SetNumInstancesRequest()
    expected_request.instances = 15
    service_response = modules_service_pb2.SetNumInstancesResponse()
    self.SetSuccessExpectations('SetNumInstances',
                                expected_request,
                                service_response)
    modules.set_num_instances(15)

  def testSetNumInstances_BadInstancesType(self):
    """Test we raise an error when we receive a bad instances type."""
    self.assertRaises(TypeError, modules.set_num_instances, 'no good')

  def testSetNumInstances_InvalidVersionError(self):
    """Test we raise an error when we receive on from the underlying API."""
    expected_request = modules_service_pb2.SetNumInstancesRequest()
    expected_request.instances = 23
    self.SetExceptionExpectations(
        'SetNumInstances', expected_request,
        modules_service_pb2.ModulesServiceError.INVALID_VERSION)
    self.assertRaises(modules.InvalidVersionError,
                      modules.set_num_instances, 23)

  def testSetNumInstances_TransientError(self):
    """Test we raise an error when we receive on from the underlying API."""
    expected_request = modules_service_pb2.SetNumInstancesRequest()
    expected_request.instances = 23
    self.SetExceptionExpectations(
        'SetNumInstances', expected_request,
        modules_service_pb2.ModulesServiceError.TRANSIENT_ERROR)
    self.assertRaises(modules.TransientError, modules.set_num_instances, 23)

  def testStartVersion(self):
    """Test we pass through the expected args."""
    expected_request = modules_service_pb2.StartModuleRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    service_response = modules_service_pb2.StartModuleResponse()
    self.SetSuccessExpectations('StartModule',
                                expected_request,
                                service_response)
    modules.start_version('module1', 'v1')

  def testStartVersion_InvalidVersionError(self):
    """Test we raise an error when we receive one from the API."""
    expected_request = modules_service_pb2.StartModuleRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    self.SetExceptionExpectations(
        'StartModule', expected_request,
        modules_service_pb2.ModulesServiceError.INVALID_VERSION)
    self.assertRaises(modules.InvalidVersionError,
                      modules.start_version,
                      'module1',
                      'v1')

  def testStartVersion_UnexpectedStateError(self):
    """Test we don't raise an error if the version is already started."""
    expected_request = modules_service_pb2.StartModuleRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    self.mox.StubOutWithMock(logging, 'info')
    logging.info('The specified module: module1, version: v1 is already '
                 'started.')
    self.SetExceptionExpectations(
        'StartModule', expected_request,
        modules_service_pb2.ModulesServiceError.UNEXPECTED_STATE)
    modules.start_version('module1', 'v1')

  def testStartVersion_TransientError(self):
    """Test we raise an error when we receive one from the API."""
    expected_request = modules_service_pb2.StartModuleRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    self.SetExceptionExpectations(
        'StartModule', expected_request,
        modules_service_pb2.ModulesServiceError.TRANSIENT_ERROR)
    self.assertRaises(modules.TransientError,
                      modules.start_version,
                      'module1',
                      'v1')

  def testStopVersion(self):
    """Test we pass through the expected args."""
    expected_request = modules_service_pb2.StopModuleRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    service_response = modules_service_pb2.StopModuleResponse()
    self.SetSuccessExpectations('StopModule',
                                expected_request,
                                service_response)
    modules.stop_version('module1', 'v1')

  def testStopVersion_NoModule(self):
    """Test we pass through the expected args."""
    expected_request = modules_service_pb2.StopModuleRequest()
    expected_request.version = 'v1'
    service_response = modules_service_pb2.StopModuleResponse()
    self.SetSuccessExpectations('StopModule',
                                expected_request,
                                service_response)
    modules.stop_version(version='v1')

  def testStopVersion_NoVersion(self):
    """Test we pass through the expected args."""
    expected_request = modules_service_pb2.StopModuleRequest()
    expected_request.module = 'module1'
    service_response = modules_service_pb2.StopModuleResponse()
    self.SetSuccessExpectations('StopModule',
                                expected_request,
                                service_response)
    modules.stop_version('module1')

  def testStopVersion_InvalidVersionError(self):
    """Test we raise an error when we receive one from the API."""
    expected_request = modules_service_pb2.StopModuleRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    self.SetExceptionExpectations(
        'StopModule', expected_request,
        modules_service_pb2.ModulesServiceError.INVALID_VERSION)
    self.assertRaises(modules.InvalidVersionError,
                      modules.stop_version,
                      'module1',
                      'v1')

  def testStopVersion_AlreadyStopped(self):
    """Test we don't raise an error if the version is already stopped."""
    expected_request = modules_service_pb2.StopModuleRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    self.mox.StubOutWithMock(logging, 'info')
    logging.info('The specified module: module1, version: v1 is already '
                 'stopped.')
    self.SetExceptionExpectations(
        'StopModule', expected_request,
        modules_service_pb2.ModulesServiceError.UNEXPECTED_STATE)
    modules.stop_version('module1', 'v1')

  def testStopVersion_TransientError(self):
    """Test we raise an error when we receive one from the API."""
    self.SetExceptionExpectations(
        'StopModule', modules_service_pb2.StopModuleRequest(),
        modules_service_pb2.ModulesServiceError.TRANSIENT_ERROR)
    self.assertRaises(modules.TransientError, modules.stop_version)

  def testGetHostname(self):
    """Test we pass through the expected args."""
    expected_request = modules_service_pb2.GetHostnameRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    expected_request.instance = '3'
    service_response = modules_service_pb2.GetHostnameResponse()
    service_response.hostname = 'abc'
    self.SetSuccessExpectations('GetHostname',
                                expected_request,
                                service_response)
    self.assertEqual('abc', modules.get_hostname('module1', 'v1', '3'))

  def testGetHostname_NoModule(self):
    """Test we pass through the expected args when no module is specified."""
    expected_request = modules_service_pb2.GetHostnameRequest()
    expected_request.version = 'v1'
    expected_request.instance = '3'
    service_response = modules_service_pb2.GetHostnameResponse()
    service_response.hostname = 'abc'
    self.SetSuccessExpectations('GetHostname',
                                expected_request,
                                service_response)
    self.assertEqual('abc', modules.get_hostname(version='v1', instance='3'))

  def testGetHostname_NoVersion(self):
    """Test we pass through the expected args when no version is specified."""
    expected_request = modules_service_pb2.GetHostnameRequest()
    expected_request.module = 'module1'
    expected_request.instance = '3'
    service_response = modules_service_pb2.GetHostnameResponse()
    service_response.hostname = 'abc'
    self.SetSuccessExpectations('GetHostname',
                                expected_request,
                                service_response)
    self.assertEqual('abc',
                     modules.get_hostname(module='module1', instance='3'))

  def testGetHostname_IntInstance(self):
    """Test we pass through the expected args when an int instance is given."""
    expected_request = modules_service_pb2.GetHostnameRequest()
    expected_request.module = 'module1'
    expected_request.instance = '3'
    service_response = modules_service_pb2.GetHostnameResponse()
    service_response.hostname = 'abc'
    self.SetSuccessExpectations('GetHostname',
                                expected_request,
                                service_response)
    self.assertEqual('abc', modules.get_hostname(module='module1', instance=3))

  def testGetHostname_InstanceZero(self):
    """Test we pass through the expected args when instance zero is given."""
    expected_request = modules_service_pb2.GetHostnameRequest()
    expected_request.module = 'module1'
    expected_request.instance = '0'
    service_response = modules_service_pb2.GetHostnameResponse()
    service_response.hostname = 'abc'
    self.SetSuccessExpectations('GetHostname',
                                expected_request,
                                service_response)
    self.assertEqual('abc', modules.get_hostname(module='module1', instance=0))

  def testGetHostname_NoArgs(self):
    """Test we pass through the expected args when none are given."""
    expected_request = modules_service_pb2.GetHostnameRequest()
    service_response = modules_service_pb2.GetHostnameResponse()
    service_response.hostname = 'abc'
    self.SetSuccessExpectations('GetHostname',
                                expected_request,
                                service_response)
    self.assertEqual('abc', modules.get_hostname())

  def testGetHostname_BadInstanceType(self):
    """Test get_hostname throws a TypeError when passed a float for instance."""
    self.assertRaises(TypeError,
                      modules.get_hostname,
                      'module1',
                      'v1',
                      1.2)

  def testGetHostname_InvalidModuleError(self):
    """Test we raise an error when we receive one from the API."""
    expected_request = modules_service_pb2.GetHostnameRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    self.SetExceptionExpectations(
        'GetHostname', expected_request,
        modules_service_pb2.ModulesServiceError.INVALID_MODULE)
    self.assertRaises(modules.InvalidModuleError,
                      modules.get_hostname,
                      'module1',
                      'v1')

  def testGetHostname_InvalidInstancesError(self):
    """Test we raise an error when we receive one from the API."""
    self.SetExceptionExpectations(
        'GetHostname', modules_service_pb2.GetHostnameRequest(),
        modules_service_pb2.ModulesServiceError.INVALID_INSTANCES)
    self.assertRaises(modules.InvalidInstancesError, modules.get_hostname)

  def testGetHostname_UnKnownError(self):
    """Test we raise an error when we receive one from the API."""
    expected_request = modules_service_pb2.GetHostnameRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    self.SetExceptionExpectations(
        'GetHostname', expected_request, 1099)
    self.assertRaisesRegex(modules.Error,
                           'ApplicationError: 1099',
                           modules.get_hostname,
                           'module1',
                           'v1')

  def testGetHostname_UnMappedError(self):
    """Test we raise an error when we receive one from the API."""
    expected_request = modules_service_pb2.GetHostnameRequest()
    expected_request.module = 'module1'
    expected_request.version = 'v1'
    self.SetExceptionExpectations(
        'GetHostname', expected_request,
        modules_service_pb2.ModulesServiceError.INVALID_VERSION)
    expected_message = 'ApplicationError: %s' % (
        modules_service_pb2.ModulesServiceError.INVALID_VERSION)
    self.assertRaisesRegex(modules.Error,
                           expected_message,
                           modules.get_hostname,
                           'module1',
                           'v1')


class MockRpc(object):
  """Mock UserRPC class."""

  def __init__(self, expected_method, expected_request, service_response=None,
               application_error_number=None):
    self._expected_method = expected_method
    self._expected_request = expected_request
    self._service_response = service_response
    self._application_error_number = application_error_number

  def check_success(self):
    self._check_success_called = True
    if self._application_error_number is not None:
      raise apiproxy_errors.ApplicationError(self._application_error_number)
    self.response.CopyFrom(self._service_response)

  def get_result(self):
    self._check_success_called = False
    result = self._hook(self)
    if not self._check_success_called:
      raise AssertionError('The hook is expected to call check_success()')
    return result

  def make_call(self, method,
                request, response, get_result_hook=None, user_data=None):
    self.method = method
    if self._expected_method != method:
      raise ValueError('expected method %s but got method %s' %
                       (self._expected_method, method))
    self.request = request
    if self._expected_request != request:
      raise ValueError('expected request %s but got request %s' %
                       (self._expected_request, request))
    self.response = response
    self._hook = get_result_hook
    self.user_data = user_data


if __name__ == '__main__':
  absltest.main()

