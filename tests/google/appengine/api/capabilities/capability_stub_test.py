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



"""Unittest for the capability_stub module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from six.moves import map

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import capabilities
from google.appengine.api.capabilities import capability_stub
from absl.testing import absltest




class CapabilityServiceStubTest(absltest.TestCase):
  """Tests capability service stub."""

  def setUp(self):
    """Set up test fixture."""
    self.stub = capability_stub.CapabilityServiceStub()
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub(
        'capability_service', self.stub)

  def _CheckEnabled(self, package, caps):
    """Checks that a package and capabilities list are ENABLED."""
    self._CheckStatus(package, caps, capabilities.CapabilityConfig.ENABLED)

  def _CheckDisabled(self, package, caps):
    """Checks that a package and capabilities list are DISABLED."""
    self._CheckStatus(package, caps, capabilities.CapabilityConfig.DISABLED)

  def _CheckScheduled(self, package, caps):
    """Checks that a package and capabilities list are SCHEDULED."""
    self._CheckStatus(package, caps, capabilities.CapabilityConfig.SCHEDULED)

  def _CheckStatus(self, package, caps, status):
    """Checks the status of a package and capabilities list."""
    request = capability_stub.IsEnabledRequest()
    request.package = package
    list(map(request.capability.append, caps or ['*']))
    response = capability_stub.IsEnabledResponse()
    self.stub._Dynamic_IsEnabled(request, response)
    for config in response.config:
      self.assertEqual(status, config.status)

  def _Call_Dynamic_IsEnabled(self, package, caps):
    request = capability_stub.IsEnabledRequest()
    request.package = package
    list(map(request.capability.append, caps))
    response = capability_stub.IsEnabledResponse()
    self.stub._Dynamic_IsEnabled(request, response)

    return response

  def testDefaultCapabilitiesAreEnabled(self):
    """Tests that all default packages are enabled."""
    self._CheckEnabled('blobstore', ['*'])
    self._CheckEnabled('datastore_v3', ['*', 'write'])
    self._CheckEnabled('images', ['*'])
    self._CheckEnabled('mail', ['*'])
    self._CheckEnabled('memcache', ['*'])
    self._CheckEnabled('taskqueue', ['*'])
    self._CheckEnabled('urlfetch', ['*'])
    self._CheckEnabled('xmpp', ['*'])

  def testSetPackageEnabled(self):
    """Tests setting status via SetPackageEnabled."""

    self.stub.SetPackageEnabled('datastore_v3', False)
    self.stub.SetPackageEnabled('images', False)
    self._CheckDisabled('datastore_v3', ['*', 'write'])
    self._CheckDisabled('images', ['*'])
    self._CheckEnabled('mail', ['*'])


    self.stub.SetPackageEnabled('datastore_v3', True)
    self._CheckEnabled('datastore_v3', ['*', 'write'])
    self._CheckDisabled('images', ['*'])
    self._CheckEnabled('mail', ['*'])


    self.stub.SetPackageEnabled('images', True)
    self._CheckEnabled('datastore_v3', ['*', 'write'])
    self._CheckEnabled('images', ['*'])
    self._CheckEnabled('mail', ['*'])

  def testSetPackageEnabled_UnsupportedPackage(self):
    """Tests SetPackageEnabled with an unsupported package."""
    self.assertRaises(KeyError, self.stub.SetPackageEnabled, 'foo', True)

  def testSetCapabilityStatus(self):
    """Tests setting status via SetCapabilityStatus."""

    self.stub.SetCapabilityStatus(
        'datastore_v3', 'write', capabilities.CapabilityConfig.SCHEDULED)
    self.stub.SetCapabilityStatus(
        'images', '*', capabilities.CapabilityConfig.DISABLED)
    self._CheckScheduled('datastore_v3', ['write'])
    self._CheckEnabled('datastore_v3', ['*'])
    self._CheckDisabled('images', ['*'])


    self.stub.SetCapabilityStatus(
        'datastore_v3', 'write', capabilities.CapabilityConfig.ENABLED)
    self.stub.SetCapabilityStatus(
        'images', '*', capabilities.CapabilityConfig.ENABLED)
    self._CheckEnabled('datastore_v3', ['*', 'write'])
    self._CheckEnabled('images', ['*'])

  def testSetCapabilityStatus_UnsupportedPackage(self):
    """Tests SetCapabilityStatus with an unsupported package."""
    self.assertRaises(
        KeyError, self.stub.SetCapabilityStatus, 'foo', '*',
        capabilities.CapabilityConfig.ENABLED)

  def testSetCapabilityStatus_UnsupporteCapability(self):
    """Tests SetCapabilityStatus with an unsupported package."""
    self.assertRaises(
        KeyError, self.stub.SetCapabilityStatus, 'images', 'cats',
        capabilities.CapabilityConfig.ENABLED)

  def testDynamicIsEnabled_SummaryStatus_Enabled(self):
    """Tests the summary status field in _Dynamic_IsEnabled."""
    response = self._Call_Dynamic_IsEnabled('datastore_v3', ['*', 'write'])
    self.assertEqual(
        response.summary_status, capabilities.IsEnabledResponse.ENABLED)

  def testDynamicIsEnabled_SummaryStatus_Scheduled(self):
    """Tests the summary status field in _Dynamic_IsEnabled."""
    self.stub.SetCapabilityStatus(
        'datastore_v3', 'write', capabilities.CapabilityConfig.SCHEDULED)
    response = self._Call_Dynamic_IsEnabled('datastore_v3', ['*', 'write'])
    self.assertEqual(
        response.summary_status, capabilities.IsEnabledResponse.SCHEDULED_NOW)

  def testDynamicIsEnabled_SummaryStatus_Disabled(self):
    """Tests the summary status field in _Dynamic_IsEnabled."""
    self.stub.SetCapabilityStatus(
        'datastore_v3', 'write', capabilities.CapabilityConfig.DISABLED)
    response = self._Call_Dynamic_IsEnabled('datastore_v3', ['*', 'write'])
    self.assertEqual(
        response.summary_status, capabilities.IsEnabledResponse.DISABLED)

  def testDynamicIsEnabled_SummaryStatus_Unknown(self):
    """Tests the summary status field in _Dynamic_IsEnabled."""
    self.stub.SetCapabilityStatus(
        'datastore_v3', 'write', capabilities.CapabilityConfig.UNKNOWN)
    response = self._Call_Dynamic_IsEnabled('datastore_v3', ['*', 'write'])
    self.assertEqual(
        response.summary_status, capabilities.IsEnabledResponse.UNKNOWN)


if __name__ == '__main__':
  absltest.main()
