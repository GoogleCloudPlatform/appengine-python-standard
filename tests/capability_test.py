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


"""Unittest for google.appengine.api.capabilities."""



from google.appengine.api import capabilities
from absl.testing import absltest


IsEnabledRequest = capabilities.IsEnabledRequest
IsEnabledResponse = capabilities.IsEnabledResponse
CapabilityConfig = capabilities.CapabilityConfig


class MockCapabilityImpl(absltest.TestCase):
  """Stub for the apiproxy_stub_map module.

  Used for testing that RPC calls from stubby.py are formatted correctly.
  """

  def __init__(self, expected_request, apiproxy_response, failure=None):
    """Initializes Stub. Allows for different failures."""
    self.failure = failure
    self.expected_request = expected_request
    self.apiproxy_response = apiproxy_response

  def MakeSyncCall(self, service, call, request, response):
    """The main RPC entry point.

    Args:
      service: should be equal to 'stubby'
      call: a string representin the call to make. Must be part of
        StubbyService.
      request: protocol buffer of the appropriate type for the call.
      response: protocol buffer of the appropriate type for the call.
    """
    self.assertEqual('capability_service', service)

    self.assertTrue(request.IsInitialized())
    self.assertEqual(str(self.expected_request), str(request))

    if call != 'IsEnabled':
      self.fail('invalid call %s' % call)

    response.CopyFrom(self.apiproxy_response)

    if self.failure:
      raise self.failure


class CapabilitiesTest(absltest.TestCase):
  """Tests for CapabilitySet."""

  def testEnabledCapability(self):
    admin_msg = 'Write performance is degraded for the next 15-20 minutes.'
    expected_request = IsEnabledRequest()
    expected_request.package = 'datastore_v3'
    expected_request.capability.append('*')
    expected_request.capability.append('write')

    actual_response = IsEnabledResponse()
    actual_response.summary_status = IsEnabledResponse.ENABLED
    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = '*'
    config.status = CapabilityConfig.ENABLED
    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'write'
    config.status = CapabilityConfig.ENABLED
    config.admin_message = admin_msg

    stub_map = MockCapabilityImpl(expected_request, actual_response)
    capability_set = capabilities.CapabilitySet(
        'datastore_v3', capabilities=['write'], stub_map=stub_map)

    self.assertEqual(True, capability_set.is_enabled());
    self.assertEqual(admin_msg, capability_set.admin_message())
    self.assertEqual(actual_response, capability_set._get_status())

  def testDisabledCapability(self):
    admin_msg = 'The datastore is in read-only mode for scheduled maintenance.'
    expected_request = IsEnabledRequest()
    expected_request.package = 'datastore_v3'
    expected_request.capability.append('*')
    expected_request.capability.append('write')

    actual_response = IsEnabledResponse()
    actual_response.summary_status = IsEnabledResponse.DISABLED
    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = '*'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'write'
    config.status = CapabilityConfig.DISABLED
    config.admin_message = admin_msg

    stub_map = MockCapabilityImpl(expected_request, actual_response)
    capability_set = capabilities.CapabilitySet(
        'datastore_v3', capabilities=['write'], stub_map=stub_map)

    self.assertEqual(False, capability_set.is_enabled());
    self.assertEqual(admin_msg, capability_set.admin_message())
    self.assertEqual(actual_response, capability_set._get_status())

  def testEnabledCall(self):
    admin_msg = 'Write performance is degraded for the next 15-20 minutes.'

    expected_request = IsEnabledRequest()
    expected_request.package = 'datastore_v3'
    expected_request.capability.append('*')
    expected_request.call.append('Put')

    actual_response = IsEnabledResponse()
    actual_response.summary_status = IsEnabledResponse.ENABLED
    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = '*'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'write'
    config.status = CapabilityConfig.ENABLED
    config.admin_message = admin_msg

    stub_map = MockCapabilityImpl(expected_request, actual_response)
    capability_set = capabilities.CapabilitySet(
        'datastore_v3', methods=['Put'], stub_map=stub_map)

    self.assertEqual(True, capability_set.is_enabled());
    self.assertEqual(admin_msg, capability_set.admin_message())
    self.assertEqual(actual_response, capability_set._get_status())

  def testMultipleCapabilities(self):
    expected_request = IsEnabledRequest()
    expected_request.package = 'datastore_v3'
    expected_request.capability.append('*')
    expected_request.capability.append('write')
    expected_request.capability.append('erase')

    actual_response = IsEnabledResponse()
    actual_response.summary_status = IsEnabledResponse.ENABLED
    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = '*'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'write'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'erase'
    config.status = CapabilityConfig.ENABLED

    stub_map = MockCapabilityImpl(expected_request, actual_response)
    capability_set = capabilities.CapabilitySet(
        'datastore_v3', capabilities=['write', 'erase'], stub_map=stub_map)
    self.assertEqual(True, capability_set.is_enabled());
    self.assertEqual('', capability_set.admin_message())
    self.assertEqual(actual_response, capability_set._get_status())

  def testMultipleCalls(self):
    expected_request = IsEnabledRequest()
    expected_request.package = 'datastore_v3'
    expected_request.capability.append('*')
    expected_request.call.append('Put')
    expected_request.call.append('Delete')


    actual_response = IsEnabledResponse()
    actual_response.summary_status = IsEnabledResponse.ENABLED
    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = '*'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'write'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'erase'
    config.status = CapabilityConfig.ENABLED

    stub_map = MockCapabilityImpl(expected_request, actual_response)
    capability_set = capabilities.CapabilitySet(
        'datastore_v3', methods=['Put', 'Delete'], stub_map=stub_map)
    self.assertEqual(True, capability_set.is_enabled());
    self.assertEqual('', capability_set.admin_message())
    self.assertEqual(actual_response, capability_set._get_status())

  def testMultipleCapabilitiesAndCalls(self):
    expected_request = IsEnabledRequest()
    expected_request.package = 'datastore_v3'
    expected_request.capability.append('*')
    expected_request.capability.append('backup')
    expected_request.capability.append('erase')
    expected_request.call.append('Put')
    expected_request.call.append('Delete')

    actual_response = IsEnabledResponse()
    actual_response.summary_status = IsEnabledResponse.ENABLED
    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = '*'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'write'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'erase'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = 'backup'
    config.status = CapabilityConfig.ENABLED

    stub_map = MockCapabilityImpl(expected_request, actual_response)
    capability_set = capabilities.CapabilitySet(
        'datastore_v3',
        capabilities=['backup', 'erase'],
        methods=['Put', 'Delete'],
        stub_map=stub_map)
    self.assertEqual(True, capability_set.is_enabled())
    self.assertEqual('', capability_set.admin_message())
    self.assertEqual(actual_response, capability_set._get_status())

  def testUnknownCapability(self):
    expected_request = IsEnabledRequest()
    expected_request.package = 'datastore_v3'
    expected_request.capability.append('*')
    expected_request.capability.append('backup')

    actual_response = IsEnabledResponse()
    actual_response.summary_status = IsEnabledResponse.ENABLED
    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = '*'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    expected_request.package = 'datastore_v3'
    config.capability = 'backup'
    config.status = CapabilityConfig.ENABLED

    stub_map = MockCapabilityImpl(expected_request, actual_response)
    capability_set = capabilities.CapabilitySet(
        'datastore_v3', capabilities=['backup'], stub_map=stub_map)

    self.assertEqual(True, capability_set.is_enabled())
    self.assertEqual(actual_response, capability_set._get_status())

  def testUnknownCall(self):
    expected_request = IsEnabledRequest()
    expected_request.package = 'datastore_v3'
    expected_request.capability.append('*')
    expected_request.call.append('ShipMeADVD')

    actual_response = IsEnabledResponse()
    actual_response.summary_status = IsEnabledResponse.ENABLED
    config = actual_response.config.add()
    config.package = 'datastore_v3'
    config.capability = '*'
    config.status = CapabilityConfig.ENABLED

    stub_map = MockCapabilityImpl(expected_request, actual_response)
    capability_set = capabilities.CapabilitySet(
        'datastore_v3', methods=['ShipMeADVD'], stub_map=stub_map)



    self.assertEqual(True, capability_set.is_enabled())
    self.assertEqual(actual_response, capability_set._get_status())

  def testUnknownApi(self):
    expected_request = IsEnabledRequest()
    expected_request.package = 'kittens'
    expected_request.capability.append('*')
    expected_request.capability.append('cuteness')
    expected_request.call.append('Meow')

    actual_response = IsEnabledResponse()
    actual_response.summary_status = IsEnabledResponse.ENABLED
    config = actual_response.config.add()
    config.package = 'kittens'
    config.capability = '*'
    config.status = CapabilityConfig.ENABLED

    config = actual_response.config.add()
    config.package = 'kittens'
    config.capability = 'cuteness'
    config.status = CapabilityConfig.ENABLED

    stub_map = MockCapabilityImpl(expected_request, actual_response)
    capability_set = capabilities.CapabilitySet('kittens',
                                                capabilities=['cuteness'],
                                                methods=['Meow'],
                                                stub_map=stub_map)

    self.assertEqual(True, capability_set.is_enabled())
    self.assertEqual(actual_response, capability_set._get_status())


if __name__ == '__main__':
  absltest.main()

