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
"""A very simple base class for titanoboa Stubs.

This base class provides a mechanism for stubs to register patchers that should
be started and stopped in local dev and/or testing environments.

These patchers are expected to be created by mock.patch().
"""

import abc
import logging
import six

logging.getLogger('google.appengine.api.stubs').setLevel(logging.INFO)


class Stub(six.with_metaclass(abc.ABCMeta, object)):

  @abc.abstractproperty
  def patchers(self):
    pass


class Patchers(list):
  """A list of patchers with helper functions to bulk start and stop them."""

  def StartAll(self):
    """Start all patchers and return a map of the created mocks."""
    mocks = {}
    for patcher in self:
      m = patcher.start()
      module_name = patcher.target.__name__




      if module_name.startswith('google.appengine'):
        module_name = module_name.replace('google.appengine',
                                          'google.appengine', 1)

      mocks[module_name + '.' + patcher.attribute] = m
    return mocks

  def StopAll(self):
    for patcher in self:
      try:
        patcher.stop()
      except RuntimeError:


        pass


