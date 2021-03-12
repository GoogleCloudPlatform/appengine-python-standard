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


"""Unit-test for google.appengine.api.yaml_listener module"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import google

from ruamel import yaml
from six.moves import zip

from google.appengine.api import yaml_errors
from google.appengine.api import yaml_listener
from google.appengine.api import yaml_test_util
from absl.testing import absltest




class TestEventListener(absltest.TestCase):
  """Tests for EventListener class"""

  def _AssertEventClass(self, next, event_class, value=None):
    """Assert that the next value in an iterator is of the correct class.

    Args:
      next: Next event object.
      event_class: Class that next objects class should equal
      value: (optional) Check the value of scalar events.

    Raises:
      AssertionError: When event is not of the expected class or when
       the value stored in the event is unpexpected.
    """
    self.assertEqual(event_class, next.__class__,
                     "Was expecting %s, was %s" %
                     (next.__class__.__name__,
                      event_class.__name__))
    if value is not None:
      self.assertEqual(value, next.value)

  def testMustProvideValidHandler(self):
    """Check to make sure can not pass in invalid handler"""
    self.failUnlessRaises(yaml_errors.ListenerConfigurationError,
                          yaml_listener.EventListener,
                          None)
    self.failUnlessRaises(yaml_errors.ListenerConfigurationError,
                          yaml_listener.EventListener,
                          object())

  def testUnexpectedEventClass(self):
    """Check when parser sends illegal event type."""
    listener = yaml_listener.EventListener(
      yaml_test_util.FakeEventHandler(self))

    self.failUnlessRaises(yaml_errors.IllegalEvent,
                          listener.HandleEvent,
                          object())

  def testForwardsEventsInOrderReceived(self):
    """Check to make sure listener forwards events in order received."""
    events = [
      yaml.events.StreamStartEvent(),
      yaml.events.StreamEndEvent(),
      yaml.events.DocumentStartEvent(),
      yaml.events.DocumentEndEvent(),
      yaml.events.AliasEvent(None),
      yaml.events.ScalarEvent(None, None, (True, False), None),
      yaml.events.SequenceStartEvent(None, None, None),
      yaml.events.SequenceEndEvent(),
      yaml.events.MappingStartEvent(None, None, None),
      yaml.events.MappingEndEvent(),


      yaml.events.SequenceEndEvent(),
      yaml.events.DocumentEndEvent(),
      yaml.events.MappingStartEvent(None, None, None),
    ]
    FAKE_LOADER = object()


    event_generator = [(event, FAKE_LOADER) for event in events]

    handler = yaml_test_util.FakeEventHandler(self, FAKE_LOADER)
    listener = yaml_listener.EventListener(handler)
    listener._HandleEvents(event_generator)
    self.assertEqual(events, handler.events)

  def testParseYaml(self):
    """Test events generated by PyYAML parser correctly forwarded."""
    document = ('item1: string1\n'
                'item2:\n'
                '  - listitem1\n'
                '  - listitem2\n'
                'item3: &item3\n'
                '  mapkey1: mapvalue1\n'
                '  mapkey2: mapvalue2\n'
                'item4: *item3\n')
    handler = yaml_test_util.FakeEventHandler(self)
    listener = yaml_listener.EventListener(handler)
    listener.Parse(document)

    expected_event_list = [
      (yaml.events.StreamStartEvent,),
      (yaml.events.DocumentStartEvent,),
      (yaml.events.MappingStartEvent,),
      (yaml.events.ScalarEvent, 'item1'),
      (yaml.events.ScalarEvent, 'string1'),
      (yaml.events.ScalarEvent, 'item2'),
      (yaml.events.SequenceStartEvent,),
      (yaml.events.ScalarEvent, 'listitem1'),
      (yaml.events.ScalarEvent, 'listitem2'),
      (yaml.events.SequenceEndEvent,),
      (yaml.events.ScalarEvent, 'item3'),
      (yaml.events.MappingStartEvent,),
      (yaml.events.ScalarEvent, 'mapkey1'),
      (yaml.events.ScalarEvent, 'mapvalue1'),
      (yaml.events.ScalarEvent, 'mapkey2'),
      (yaml.events.ScalarEvent, 'mapvalue2'),
      (yaml.events.MappingEndEvent,),
      (yaml.events.ScalarEvent, 'item4'),
      (yaml.events.AliasEvent,),
      (yaml.events.MappingEndEvent,),
      (yaml.events.DocumentEndEvent,),
      (yaml.events.StreamEndEvent,),
    ]

    self.assertEqual(len(expected_event_list), len(handler.events))
    for expected_event, event in zip(expected_event_list, handler.events):
      self._AssertEventClass(event, *expected_event)

  def testUsesSafeParsingByDefault(self):
    """Tests that yaml parsing does not by default allow unsafe parsing."""

    class SafeFakeEventHandler(yaml_test_util.FakeEventHandler):
      def HandleEvent(self, event, loader, event_class):
        self.test.assertTrue(isinstance(loader, yaml.loader.SafeLoader))
        self.test.assertFalse(isinstance(loader, yaml.loader.Loader))
        super(SafeFakeEventHandler, self).HandleEvent(event,
                                                      loader,
                                                      event_class)

    document = ('yaml_var: value')

    handler = SafeFakeEventHandler(self)
    listener = yaml_listener.EventListener(handler)
    listener.Parse(document)

  def testYAMLErrorParser(self):
    """Test handling of YAML error from Parser."""
    document = ('item1: string1\n'
                '- item2\n')

    expected_event_list = [
      (yaml.events.StreamStartEvent,),
      (yaml.events.DocumentStartEvent,),
      (yaml.events.MappingStartEvent,),
      (yaml.events.ScalarEvent, 'item1'),
      (yaml.events.ScalarEvent, 'string1'),
    ]

    handler = yaml_test_util.FakeEventHandler(self)
    listener = yaml_listener.EventListener(handler)
    with self.assertRaises(yaml_errors.EventListenerYAMLError) as e:
      listener.Parse(document)
      self.fail('No parser error raised')
    self.assertTrue(str(e.exception).startswith('while parsing a block'))
    self.assertIsInstance(e.exception.cause, yaml.parser.ParserError)

    self.assertEqual(len(expected_event_list), len(handler.events))
    for expected_event, event in zip(expected_event_list, handler.events):
      self._AssertEventClass(event, *expected_event)

  def testYAMLErrorScanner(self):
    """Test handling of parser error."""
    document = 'item1:\x09bad\n'

    expected_event_list = [
      (yaml.events.StreamStartEvent,),
      (yaml.events.DocumentStartEvent,),
      (yaml.events.MappingStartEvent,),
      (yaml.events.ScalarEvent, 'item1'),
    ]

    handler = yaml_test_util.FakeEventHandler(self)
    listener = yaml_listener.EventListener(handler)
    with self.assertRaises(yaml_errors.EventListenerYAMLError) as e:
      listener.Parse(document)
      self.fail('No parser error raised')
    self.assertTrue(
        str(e.exception).startswith('while scanning for the next token'))
    self.assertIsInstance(e.exception.cause, yaml.scanner.ScannerError)

    self.assertEqual(len(expected_event_list), len(handler.events))
    for expected_event, event in zip(expected_event_list, handler.events):
      self._AssertEventClass(event, *expected_event)

  def testEventHandlerError(self):
    """Test handling of EventHandlerError."""
    class BlowUpEventHandler(yaml_test_util.FakeEventHandler):
      def Scalar(self, event, loader):
        if event.value == 'kaboom':
          raise ValueError('I blew up')
        super(BlowUpEventHandler, self).Scalar(event, loader)

    document = ('item1:\n'
                '- item2: alpha\n'
                '  item3: kaboom\n'
                '  item4: you will never see me.\n')

    expected_event_list = [
      (yaml.events.StreamStartEvent,),
      (yaml.events.DocumentStartEvent,),
      (yaml.events.MappingStartEvent,),
      (yaml.events.ScalarEvent, 'item1'),
      (yaml.events.SequenceStartEvent,),
      (yaml.events.MappingStartEvent,),
      (yaml.events.ScalarEvent, 'item2'),
      (yaml.events.ScalarEvent, 'alpha'),
      (yaml.events.ScalarEvent, 'item3'),
    ]

    handler = BlowUpEventHandler(self)
    listener = yaml_listener.EventListener(handler)
    with self.assertRaises(yaml_errors.EventError) as e:
      listener.Parse(document)
      self.fail('No event-listener error raised')
    self.assertTrue(str(e.exception).startswith('I blew up'))
    self.assertIsInstance(e.exception.cause, ValueError)
    self.assertIsInstance(e.exception.event, yaml.events.ScalarEvent)
    self.assertEqual(u'kaboom', e.exception.event.value)

    self.assertEqual(len(expected_event_list), len(handler.events))
    for expected_event, event in zip(expected_event_list, handler.events):
      self._AssertEventClass(event, *expected_event)



if __name__ == '__main__':
  absltest.main()

