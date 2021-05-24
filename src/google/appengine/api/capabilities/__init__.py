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


"""Allows applications to identify API outages and scheduled downtime.

   Example:

   ```python
    def StoreUploadedProfileImage(self):
      uploaded_image = self.request.get('img')
      # If the images API is unavailable, we'll just skip the resize.
      if CapabilitySet('images').is_enabled():
        uploaded_image = images.resize(uploaded_image, 64, 64)
      store(uploaded_image)

    def RenderHTMLForm(self):
      datastore_readonly = CapabilitySet('datastore_v3', capabilities=['write'])
      if datastore_readonly.is_enabled():
        # ...render form normally...
      else:
        # self.response.out('<p>Not accepting submissions right now: %s</p>' %
                            datastore_readonly.admin_message())
        # ...render form with form elements disabled...
     ```

Individual API wrapper modules should expose `CapabilitySet` objects
for users rather than relying on users to create them.  They can
also create convenience methods that delegate to the relevant `CapabilitySet`;
for example, `db.IsReadOnly()`.
"""










import warnings

from google.appengine.api import apiproxy_stub_map
from google.appengine.api.capabilities import capability_service_pb2
from google.appengine.base import capabilities_pb2


IsEnabledRequest = capability_service_pb2.IsEnabledRequest
IsEnabledResponse = capability_service_pb2.IsEnabledResponse
CapabilityConfig = capabilities_pb2.CapabilityConfig


class UnknownCapabilityError(Exception):
  """An unknown capability was requested."""


class CapabilitySet(object):
  """Encapsulates one or more capabilities.

  Capabilities can either be named explicitly, or inferred from the list of
  methods provided. If no capabilities or methods are provided, this will check
  whether the entire package is enabled.
  """

  def __init__(self, package, capabilities=None, methods=None,
               stub_map=apiproxy_stub_map):
    """Constructor.

    Args:
      capabilities: List of strings
      methods: List of strings
    """
    if capabilities is None:
      capabilities = []
    if methods is None:
      methods = []
    self._package = package
    self._capabilities = ['*'] + capabilities
    self._methods = methods
    self._stub_map = stub_map

  def is_enabled(self):
    """Tests whether the capabilities are currently enabled.

    Returns:
      `True` if API calls that require these capabilities will succeed.

    Raises:
      UnknownCapabilityError: If a specified capability was not recognized.
    """
    config = self._get_status()
    return config.summary_status in (IsEnabledResponse.DEFAULT,
                                     IsEnabledResponse.ENABLED,
                                     IsEnabledResponse.SCHEDULED_FUTURE,
                                     IsEnabledResponse.SCHEDULED_NOW)

  def will_remain_enabled_for(self, time=60):
    """Returns whether a capability will remain enabled.

    DEPRECATED: Use `is_enabled()` instead. This method was never fully
    implemented.

    Args:
      time: Number of seconds in the future to look when checking for scheduled
          downtime.

    Returns:
      `True` if there is no scheduled downtime for the specified capability
      within the amount of time specified.

    Raises:
      UnknownCapabilityError: If a specified capability was not recognized.
    """
    warnings.warn('will_remain_enabled_for() is deprecated: '
                  'use is_enabled instead.',
                  DeprecationWarning,
                  stacklevel=2)
    config = self._get_status()

    status = config.summary_status

    if status in (IsEnabledResponse.DEFAULT, IsEnabledResponse.ENABLED):
      return True
    elif status == IsEnabledResponse.SCHEDULED_NOW:
      return False
    elif status == IsEnabledResponse.SCHEDULED_FUTURE:
      if config.HasField('time_until_scheduled'):
        return config.time_until_scheduled >= time
      else:

        return True
    elif status == IsEnabledResponse.DISABLED:
      return False
    else:


      return False

  def admin_message(self):
    """Retrieves any administrator notice messages for these capabilities.

    Returns:
      A string containing one or more administrator messages, or an empty
      string.

    Raises:
      UnknownCapabilityError: If a specified capability was not recognized.
    """
    message_list = []
    for config in self._get_status().config:
      message = config.admin_message
      if message and message not in message_list:
        message_list.append(message)
    return '  '.join(message_list)

  def _get_status(self):
    """Gets the `IsEnabledResponse` for the capabilities listed.

    Returns:
      `IsEnabledResponse` for the specified capabilities.

    Raises:
      UnknownCapabilityError: If an unknown capability was requested.
    """
    req = IsEnabledRequest()
    req.package = self._package
    for capability in self._capabilities:
      req.capability.append(capability)
    for method in self._methods:
      req.call.append(method)

    resp = capability_service_pb2.IsEnabledResponse()
    if (self._package == 'datastore_v3' and 'write' in self._capabilities or
        self._methods != 0):
      self._stub_map.MakeSyncCall('capability_service', 'IsEnabled', req, resp)
    else:
      resp = IsEnabledResponse()
      resp.set_summary_status(IsEnabledResponse.ENABLED)
      for capability in self._capabilities:
        resp.add_config(
            package=self._package,
            capability=capability,
            status=CapabilityConfig.ENABLED)

    return resp

