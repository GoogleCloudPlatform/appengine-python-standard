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


"""Test utilties for YAML parsing tests.
"""



from google.appengine.api import yaml_listener
from google.appengine.api import yaml_builder

import google
from ruamel import yaml


class FakeDocument(object):
  """Simple document with single object root."""

  def __init__(self):
    """Initialize fake document.

    Fake document has single value, the root, which is where its contents
    is stored.
    """
    self.root = None


class FakeEventHandler(yaml_listener.EventHandler):
  """Fake event handler

  All this class does is receive events, check that they are the right type
  and append it to an event list so that they can be checked for proper call
  sequence later by unit tests.
  """

  def __init__(self, test, expect_loader=None):
    """Initializer for fake event handler.

    Args:
      test: Test from which fake handler is called.
      expect_loader: Which loader should be passed along as a parameter
       by listener calls.  Can be set to None for tests which do not
       involve use of a loader.
    """
    self.events = []
    self.test = test
    self.expect_loader = expect_loader

  def HandleEvent(self, event, loader, event_class):
    """Handle event

    If fake handler constructed with a loader, will check that it has received
    it as its loader parameter.  Checks that the received event is of the
    expected class.  If successful, appends event to list of received events.

    Args:
      event: Event received from emitter or test harness.
      loader: Loader received from emitter or test harness.
      event_class: Expected class which event should be instance of.
    """

    if self.expect_loader:
      self.test.assertEquals(self.expect_loader, loader)

    self.test.assertTrue(isinstance(event, event_class),
                         "Expected %s, was %s" %
                         (event.__class__.__name__,
                          event_class.__name__))
    self.events.append(event)

  def StreamStart(self, event, loader):
    """Handle start of stream event"""
    self.HandleEvent(event, loader, yaml.events.StreamStartEvent)

  def StreamEnd(self, event, loader):
    """Handle end of stream event"""
    self.HandleEvent(event, loader, yaml.events.StreamEndEvent)

  def DocumentStart(self, event, loader):
    """Handle start of document event"""
    self.HandleEvent(event, loader, yaml.events.DocumentStartEvent)

  def DocumentEnd(self, event, loader):
    """Handle end of document event"""
    self.HandleEvent(event, loader, yaml.events.DocumentEndEvent)

  def Alias(self, event, loader):
    """Handle alias event"""
    self.HandleEvent(event, loader, yaml.events.AliasEvent)

  def Scalar(self, event, loader):
    """Handle scalar event"""
    self.HandleEvent(event, loader, yaml.events.ScalarEvent)

  def SequenceStart(self, event, loader):
    """Handle start of sequence event"""
    self.HandleEvent(event, loader, yaml.events.SequenceStartEvent)

  def SequenceEnd(self, event, loader):
    """Handle end of sequence event"""
    self.HandleEvent(event, loader, yaml.events.SequenceEndEvent)

  def MappingStart(self, event, loader):
    """Handle start of mapping event"""
    self.HandleEvent(event, loader, yaml.events.MappingStartEvent)

  def MappingEnd(self, event, loader):
    """Handle end of mapping event"""
    self.HandleEvent(event, loader, yaml.events.MappingEndEvent)


class FakeBuilder(yaml_builder.Builder):
  """Maps YAML events directly to collection types for easy inspection.

  Note, this is very similar if not identical to what yaml.load creates.
  """

  def BuildDocument(self):
    """Construct new fake document"""
    return FakeDocument()

  def InitializeDocument(self, document, value):
    """Initialize root with scalar value"""
    document.root = value

  def BuildMapping(self, top_value):
    """Use dict as mapping object.

    Args:
      top_value: Not used

    Returns:
      An new dict object.
    """
    return {}

  def EndMapping(self, top_value, mapping):
    """Append 'end-mapping' to mapping.

    Args:
      top_value: Not used.
      mapping: Ending mapping.
    """
    mapping['end-mapping'] = True

  def BuildSequence(self, top_value):
    """Use list as sequence object.

    Args:
      top_value: Not used

    Returns:
      An new list object.
    """
    return []

  def EndSequence(self, top_value, sequence):
    """Append 'end-sequence' to sequence.

    Args:
      top_value: Not used.
      sequence: Ending sequence.
    """
    sequence.append('end-sequence')

  def MapTo(self, subject, key, value):
    """Map value to dict.

    Args:
      subject: dict object to map to.
      key: Key for dict object.
      value: Value to map to.
    """
    subject[key] = value

  def AppendTo(self, subject, value):
    """Append value to list.

    Args:
      subject: list object to append to.
      value: Value to append to list.
    """
    subject.append(value)
