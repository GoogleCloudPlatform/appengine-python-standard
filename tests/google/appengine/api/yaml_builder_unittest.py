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


"""Unit-test for google.appengine.api.yaml_builder module"""



import google

from ruamel import yaml

from google.appengine.api import yaml_builder
from google.appengine.api import yaml_errors
from google.appengine.api import yaml_test_util
from absl.testing import absltest


class TestBuilderHandler(absltest.TestCase):
  """Unit tests for BuilderHandler."""

  def setUp(self):
    """Set up test harness.

    Create BuilderHandler and connect to FakeBuilder.  Create loader
    to pass in to methods which require it.
    """
    self.builder = yaml_test_util.FakeBuilder()
    self.handler = yaml_builder.BuilderHandler(self.builder)
    self.loader = yaml.loader.Loader('')

  def testMustProvideValidBuilder(self):
    """Make sure that handler will only accept valid builder"""
    self.failUnlessRaises(yaml_errors.ListenerConfigurationError,
                          yaml_builder.BuilderHandler,
                          None)
    self.failUnlessRaises(yaml_errors.ListenerConfigurationError,
                          yaml_builder.BuilderHandler,
                          object())

  def testMustStartStream(self):
    """Make sure that handler will not function unless stream started."""
    self.failUnlessRaises(AssertionError,
                          self.handler.DocumentStart,
                          None, None)
    self.handler.StreamStart(None, None)
    self.handler.StreamEnd(None, self.loader)
    self.failUnlessRaises(AssertionError,
                          self.handler.DocumentStart,
                          None, None)

  def testStreamBalance(self):
    """Make sure stream events balanced.

    It should not be possible to end the stream until all enclosing structures
    are closed first.
    """
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.failUnlessRaises(AssertionError,
                          self.handler.StreamEnd,
                          None, None)

  def testNoDoubleStreamStart(self):
    """Make sure can not call stream start again until stream end."""
    self.handler.StreamStart(None, None)
    self.failUnlessRaises(AssertionError,
                          self.handler.StreamStart,
                          None, None)

  def testMustStartDocument(self):
    """Make sure document is opened before any other events."""
    self.handler.StreamStart(None, None)
    self.failUnlessRaises(TypeError,
                          self.handler.MappingStart,
                          None, None)
    self.failUnlessRaises(TypeError,
                          self.handler.SequenceStart,
                          None, None)
    self.failUnlessRaises(AttributeError,
                          self.handler.Scalar,
                          None, self.loader)

  def testDocumentBalance(self):
    """Make sure document events are balanced."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.MappingStart(None, None)
    self.failUnlessRaises(AssertionError,
                          self.handler.DocumentEnd,
                          None, None)

  def testSequenceBalance(self):
    """Make sure sequence events are balanced."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.SequenceStart(None, None)
    self.handler.MappingStart(None, None)
    self.failUnlessRaises(AssertionError,
                          self.handler.SequenceEnd,
                          None, None)

  def testMappingBalance(self):
    """Make sure mapping events are balanced."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.MappingStart(None, None)
    self.handler.SequenceStart(None, None)
    self.failUnlessRaises(AssertionError,
                          self.handler.MappingEnd,
                          None, None)

  def testDocumentCreation(self):
    """Make sure document creation is called when document started."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.DocumentEnd(None, None)
    self.handler.StreamEnd(None, None)


    results = self.handler.GetResults()
    self.assertEquals(1, len(results))
    self.assertIsInstance(results[0], yaml_test_util.FakeDocument)


    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.DocumentEnd(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.DocumentEnd(None, None)
    self.handler.StreamEnd(None, None)


    results = self.handler.GetResults()
    self.assertEquals(2, len(results))
    self.assertIsInstance(results[0], yaml_test_util.FakeDocument)
    self.assertIsInstance(results[1], yaml_test_util.FakeDocument)

  def testScalarDocument(self):
    """Create a document with just a single scalar value in it."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'a'),
                        self.loader)
    self.handler.DocumentEnd(None, None)
    self.handler.StreamEnd(None, None)
    self.assertEquals('a', self.handler.GetResults()[0].root)

  def testIntegerDocument(self):
    """Create a document with a single scalar integer in it."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.Scalar(yaml.events.ScalarEvent(None,
                                                u'tag:yaml.org,2002:int',
                                                (False, False), '1'),
                        self.loader)
    self.handler.DocumentEnd(None, None)
    self.handler.StreamEnd(None, None)
    self.assertEquals(1, self.handler.GetResults()[0].root)


  def testSequenceDocument(self):
    """Create a document with just a small sequence in it."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.SequenceStart(None, None)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None, (True,False), 'a'),
                        self.loader)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None, (True,False), 'b'),
                        self.loader)
    self.handler.SequenceEnd(None, None)
    self.handler.DocumentEnd(None, None)
    self.handler.StreamEnd(None, None)
    self.assertEquals(['a','b', 'end-sequence'],
                      self.handler.GetResults()[0].root)

  def testMappingDocument(self):
    """Create a document with just a small mapping in it."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.MappingStart(None, None)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'key1'),
                        self.loader)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'value1'),
                        self.loader)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'key2'),
                        self.loader)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'value2'),
                        self.loader)
    self.handler.MappingEnd(None, None)
    self.handler.DocumentEnd(None, None)
    self.handler.StreamEnd(None, None)
    self.assertEquals({'key1' : 'value1',
                       'key2' : 'value2',
                       'end-mapping': True,
                       },
                      self.handler.GetResults()[0].root)

  def testVariousNesting(self):
    """Create a document with various nested collections in it.

    Since the builder method is a re-assembling of the events that could
    be used to construct the same types of objects as the yaml.load method
    it is valid to test the results of the BuilderHandler calling in to
    FakeBuilder by comparing the results to what is produced by yaml.load.
    """
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.MappingStart(None, None)


    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'key1'),
                        self.loader)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'value1'),
                        self.loader)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'key2'),
                        self.loader)

    self.handler.SequenceStart(None, None)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'a'),
                        self.loader)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'b'),
                        self.loader)

    self.handler.MappingStart(None, None)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'nestkey1'),
                        self.loader)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'nestvalue1'),
                        self.loader)

    self.handler.MappingEnd(None, None)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'c'),
                        self.loader)

    self.handler.SequenceEnd(None, None)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), 'key3'),
                        self.loader)
    self.handler.Scalar(yaml.events.ScalarEvent(None, u'tag:yaml.org,2002:int',
                                                (True, False), '10'),
                        self.loader)
    self.handler.MappingEnd(None, None)
    self.handler.DocumentEnd(None, None)
    self.handler.StreamEnd(None, None)

    self.assertEquals(yaml.load('key1: value1\n'
                                'key2:\n'
                                '- a\n'
                                '- b\n'
                                '- nestkey1: nestvalue1\n'
                                '  end-mapping: true\n'
                                '- c\n'
                                '- end-sequence\n'
                                'key3: 10\n'
                                'end-mapping: true\n'),
                      self.handler.GetResults()[0].root)

  def testEmptyScalar(self):
    """Test to make sure builder receives scalar variable correctly."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.handler.SequenceStart(None, None)
    self.handler.Scalar(yaml.events.ScalarEvent(None, None,
                                                (True, False), u'~'),
                        self.loader)
    self.handler.SequenceEnd(None, None)
    self.handler.DocumentEnd(None, None)
    self.handler.StreamEnd(None, None)

    self.assertEquals([None, 'end-sequence'], self.handler.GetResults()[0].root)

  def testAchorsNotWorkingYet(self):
    """Make sure anchors are disabled for now."""
    self.handler.StreamStart(None, None)
    self.handler.DocumentStart(None, None)
    self.failUnlessRaises(NotImplementedError,
                          self.handler.Scalar,
                          yaml.events.ScalarEvent('x', None, None, 'a'),
                          self.loader)

  def testAliasesNotWorkingYet(self):
    """Make sure aliases are disabled for now."""
    self.failUnlessRaises(NotImplementedError,
                          lambda: self.handler.Alias(None, None))

  def testPrematureGetResults(self):
    """Fail if attempt to get results before end of stream occurs."""

    self.assertEquals(tuple(), self.handler.GetResults())
    self.handler.StreamStart(None, None)
    self.failUnlessRaises(yaml_errors.InternalError,
                          self.handler.GetResults)


if __name__ == '__main__':
  absltest.main()
