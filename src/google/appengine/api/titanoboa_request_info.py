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
"""Request info implementation for Titanoboa Applauncher."""

import threading

import requests
from requests import structures
import six

from google.appengine.api import request_info


class NotSupportedError(request_info.Error):
  pass


class LocalDispatcher(request_info.Dispatcher):
  """Dispatch requests across all instances and modules of application.

  As Titanoboa doesn't support multiple instances, this dispatcher always
  refers to a single module, version, and instance.
  """

  def __init__(self, default_hostname=None, app=None):
    self._default_hostname = default_hostname
    self._app = app

  def get_module_names(self):
    return ['default']

  def get_versions(self, module):
    return ['1']

  def get_default_version(self, module):
    return '1'

  def get_hostname(self, module, version, instance=None):
    return self._default_hostname

  def set_num_instances(self, module, version, instances):
    raise NotSupportedError('Cannot change number of instances.')

  def get_num_instances(self, module, version):
    return None

  def start_version(self, module, version):
    raise NotSupportedError('Multiple versions is not supported.')

  def stop_version(self, module, version):
    raise NotSupportedError('Multiple versions is not supported.')

  def add_event(self, runnable, eta, service=None, event_id=None):

    raise NotImplementedError()

  def update_event(self, eta, service, event_id):

    raise NotImplementedError()

  def add_request(
      self, method, relative_url, headers, body, source_ip,
      module_name=None, version=None, instance_id=None):
    requests_headers = structures.CaseInsensitiveDict()
    for k, v in headers:

      requests_headers[six.ensure_str(k)] = v
    requests_headers['X-AppEngine-User-IP'] = source_ip
    requests_headers['X-AppEngine-Fake-Is-Admin'] = '1'
    if 'host' in requests_headers:
      hostname = requests_headers['host']
    else:
      hostname = self.get_hostname(module_name, version)
    response = requests.request(
        method, 'http://' + hostname + six.ensure_str(relative_url),
        headers=requests_headers, data=body)


    return request_info.ResponseTuple(
        response.status_code, response.headers, response.content)

  def add_async_request(
      self, method, relative_url, headers, body, source_ip,
      module_name=None, version=None, instance_id=None):
    t = threading.Thread(target=self.add_request, kwargs=dict(
        method=method, relative_url=relative_url, headers=headers, body=body,
        source_ip=source_ip, module_name=module_name, version=version,
        instance_id=instance_id))
    t.start()

  def send_background_request(
      self, module_name, version, instance, background_request_id):
    if self._app:
      if not (self._app.app_yaml.basic_scaling or
              self._app.app_yaml.manual_scaling):
        raise request_info.NotSupportedWithAutoScalingError()
      if self._app.cfg.workers > 1:



        raise NotSupportedError(
            'Background requests not supported with multi-process server.')
    headers = (
        ('X-AppEngine-BackgroundRequest', background_request_id),
    )
    self.add_async_request(
        'get', '/_ah/background', headers, body='', source_ip='0.1.0.3',
        module_name=module_name, version=version, instance_id=instance)


class LocalRequestInfo(request_info._LocalRequestInfo):
  """Request info for Titanoboa local launcher."""

  def __init__(self, default_address=None, app=None):
    if default_address is None:
      default_address = '127.0.0.1:8080'
    self._address = 'http://' + default_address
    self._dispatcher = LocalDispatcher(default_address, app)

  def get_dispatcher(self):
    return self._dispatcher

  def get_address(self):
    return self._address
