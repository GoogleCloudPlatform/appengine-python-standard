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


"""Unittest for google.appengine.api.yaml_object."""





import re

from google.appengine.api import validation as v
from google.appengine.api import yaml_builder
from google.appengine.api import yaml_errors
from google.appengine.api import yaml_listener
from google.appengine.api import yaml_object
from absl.testing import absltest


class Pet(v.Validated):
  """Pet is used to test repeated fields."""
  ATTRIBUTES = {'name': v.Type(str),
                'age': v.Optional(int),
                'color': v.Optional(['black', 'brown', 'white']),
                }


class PhoneNumberDict(v.ValidatedDict):
  """Maps nonempty strings to strings, used to test ValidatedDict fields."""
  KEY_VALIDATOR = v.Regex('.+')
  VALUE_VALIDATOR = str


class PetStore(v.Validated):
  """Each test document maps to a PetStore."""
  ATTRIBUTES = {'name': v.Type(str),
                'address': v.Optional(str),
                'pets': v.Optional(v.Repeated(Pet)),
                'mascot': v.Optional(v.Type(Pet, False)),
                'phones': v.Optional(PhoneNumberDict),
                }


class YamlObjectTest(absltest.TestCase):
  """Tests for object yaml parser."""

  def setUp(self):
    """Set up parsing frame work."""
    self.builder = yaml_object.ObjectBuilder(PetStore)
    self.handler = yaml_builder.BuilderHandler(self.builder)
    self.listener = yaml_listener.EventListener(self.handler)

  def parse(self, document):
    """Helper method for parsing file with single document."""
    self.listener.Parse(document)
    return self.handler.GetResults()[0]

  def testMinimalFields(self):
    """Test the case where minimal required fields are parsed."""
    store = self.parse('---\n'
                       'name: The Grand Petstore\n')

    self.assertEquals('The Grand Petstore', store.name)
    self.assertEquals(None, store.address)
    self.assertEquals(None, store.pets)
    self.assertEquals(None, store.mascot)

  def testTwoFields(self):
    """Tests parsing required field and only one optional field."""
    store = self.parse('---\n'
                       'name: Dog House\n'
                       'address: 32 Nepotism st.')

    self.assertEquals('Dog House', store.name)
    self.assertEquals('32 Nepotism st.', store.address)
    self.assertEquals(None, store.pets)
    self.assertEquals(None, store.mascot)

  def testMissingRequiredField(self):
    """Tests what happens when required field does not exist."""
    try:
      self.parse('---\n'
                 'address: does not exist')
      self.fail('Did not raise EventError.')
    except yaml_errors.EventError as e:
      self.assertTrue(isinstance(e.cause, v.MissingAttribute))

  def testMapInsteadOfString(self):
    """Pass an empty map instead of a string."""
    try:
      self.parse('---\n'
                 'name: {}\n')
      self.fail('Did not raise EventError.')
    except yaml_errors.EventError as e:
      self.assertNotIn('CheckInitialized', str(e))
      self.assertIn('Cannot convert map', str(e))

  def testMapInsteadOfInt(self):
    """Pass an empty map instead of an integer."""
    try:
      self.parse('---\n'
                 'name: store_name\n'
                 'pets:\n'
                 '  - name: aname\n'
                 '    age: {}\n')
      self.fail('Did not raise EventError.')
    except yaml_errors.EventError as e:
      self.assertNotIn('CheckInitialized', str(e))
      self.assertIn('Cannot convert map', str(e))

  def testMapInsteadOfSequence(self):
    """Pass an empty map instead of a sequence."""
    try:
      self.parse('---\n'
                 'name: store_name\n'
                 'pets: {}\n')
      self.fail('Did not raise EventError.')
    except yaml_errors.EventError as e:
      self.assertNotIn('CheckInitialized', str(e))
      self.assertIn('Cannot convert map', str(e))

  def testObjectField(self):
    """Tests nested object - reference to another validated type."""
    store = self.parse('---\n'
                       'name: Harleys hound shop\n'
                       'mascot:\n'
                       ' name: Barky\n'
                       ' age: 4\n'
                       ' color: brown\n')

  def testDictField(self):
    """Tests nested ValidatedDict."""
    store = self.parse('---\n'
                       'name: Harleys hound shop\n'
                       'phones:\n'
                       ' reception: 555-3131\n'
                       ' sales: 555-2212\n'
                       ' vet-affairs: 555-3234\n')
    self.assertDictEqual(store.phones, {
        'reception': '555-3131',
        'sales': '555-2212',
        'vet-affairs': '555-3234'
        })
    self.assertEqual(store.name, 'Harleys hound shop')

  def testRepeatedField(self):
    """Tests repeated fields - references to another validated type"""
    store = self.parse('---\n'
                       'name: Cheap cats\n'
                       'pets:\n'
                       '- name: Meowy\n'
                       '  age: 2\n'
                       '  color: black\n'
                       '- name: Jack de\'Blackat\n')

  def testUndefinedField(self):
    """Tests using undefined fields of validated type."""
    try:
      self.parse('---\n'
                 'name: Cattery\n'
                 'number_pets: 7\n')
      self.fail('Did not raise EventError.')
    except yaml_errors.EventError as e:
      self.assertTrue(isinstance(e.cause,
                                 yaml_errors.UnexpectedAttribute))

  def testDuplicateFields(self):
    """Tests that attempting to define duplicates raises exception."""
    for document in (('---\n'
                      'name: Cattery\n'
                      'name: Cattery\n'),
                     ('---\n'
                      'name: Cattery\n'
                      'mascot:\n'
                      ' name: Barky\n'
                      ' age: 4\n'
                      ' color: brown\n'
                      'mascot:\n'
                      ' name: Ruffers\n'
                      ' age: 3\n'
                      ' color: spotty\n'),
                     ):
      try:
        self.parse(document)
        self.fail('Did not raise EventError.')
      except yaml_errors.EventError as e:
        self.assertTrue(isinstance(e.cause,
                                   yaml_errors.DuplicateAttribute))

        self.handler._stack = None


class BuildObjectsTest(absltest.TestCase):
  """Tests loading multiple object documents from file."""

  def testEmptyDocument(self):
    """Test empty file."""
    self.assertEquals((), yaml_object.BuildObjects(Pet, ''))

  def testSingleDocument(self):
    """Test single document in file."""
    pets = yaml_object.BuildObjects(Pet, ('name: Jack\n'
                                          'age: 7\n'
                                          'color: black'))
    self.assertEquals((Pet(name='Jack',
                           age=7,
                           color='black'),),
                      pets)

  def testMultipleDocument(self):
    """Test single document in file."""
    pets = yaml_object.BuildObjects(Pet, ('name: Jack\n'
                                          'age: 7\n'
                                          'color: black\n'
                                          '---\n'
                                          'name: Vespa\n'
                                          'color: brown'
                                          ))
    self.assertEquals((Pet(name='Jack',
                           age=7,
                           color='black'),
                       Pet(name='Vespa',
                           color='brown')),
                      pets)


class BuildSingleObjectTest(absltest.TestCase):
  """Tests loading single object from file."""

  def testEmptyDocument(self):
    """Test failure when file is empty."""
    self.failUnlessRaises(yaml_errors.EmptyConfigurationFile,
                          yaml_object.BuildSingleObject, Pet, '')

  def testMultipleDocuments(self):
    """Test failure when file contains multiple documents."""
    self.failUnlessRaises(yaml_errors.MultipleConfigurationFile,
                          yaml_object.BuildSingleObject,
                          Pet,
                          ('name: Jack\n'
                           '---\n'
                           'name: Vespa\n'))

  def testLoadDocument(self):
    """Test basic loading of indexes files."""
    pet = yaml_object.BuildSingleObject(Pet, ('name: Jack\n'
                                              'age: 7\n'
                                              'color: black'))
    self.assertEquals(Pet(name='Jack',
                          age=7,
                          color='black'),
                      pet)


class ValidatorTest(absltest.TestCase):
  """Tests specific types of validation.

  The validation tests are done via the _RunTest method.  To do a test
  write a test validated class, pass it in to the _RunTest method with
  the YAML that is being parsed followed by a dictionary that maps to
  expected values of properties of a resulting object.
  """

  def _RunTest(self, klass, doc, expected):
    """Run a validation test against a validated class.

    Builds an object of type klass

    Args:
      klass: Validated class with validator attributes being tested.
      doc: YAML document with source representation of object.
      expected: Dictionary represented the expected object state.
    """
    obj = yaml_object.BuildSingleObject(klass, doc)
    for key in klass.ATTRIBUTES.keys():
      value = getattr(obj, key)
      if not value == expected[key]:
        self.fail("Property '%s' did not match: %s != %s" % (key,
                                                             expected[key],
                                                             value))

  def testTypeValidator(self):
    """Test validation of basic int and str types"""
    class HasType(v.Validated):
      ATTRIBUTES = {
          'prop_int': v.Type(int),
          'prop_string': v.Type(str),
          }

    self._RunTest(HasType,
                  'prop_int: 123\n'
                  'prop_string: abc\n',
                  {'prop_int': 123,
                   'prop_string': 'abc'})

  def testOptionsValidator(self):
    """Test validation of basic string options."""
    class HasOptions(v.Validated):
      ATTRIBUTES = {
          'options': v.Options('a', 'b'),
          }

    self._RunTest(HasOptions,
                  'options: a\n',
                  {'options': 'a'})

  def testOptional(self):
    """Test optional properties."""
    class HasOptional(v.Validated):
      ATTRIBUTES = {
          'required': v.Type(int),
          'optional': v.Optional(v.Type(int)),
          }

    self._RunTest(HasOptional,
                  'required: 5\n'
                  'optional: 10\n',
                  {'required': 5,
                   'optional': 10,
                   })

    self._RunTest(HasOptional,
                  'required: 5\n',
                  {'required': 5,
                   'optional': None,
                   })

  def testRegex(self):
    """Test regular expression validated properties."""
    class HasRegex(v.Validated):
      ATTRIBUTES = {
          'regex': v.Regex(r'ab+a')
          }

    self._RunTest(HasRegex,
                  'regex: abbbba\n',
                  {'regex': 'abbbba',
                   })

  def testRegexStr(self):
    """Test regular expression definition properties."""
    class HasRegexStr(v.Validated):
      ATTRIBUTES = {
          'regexstr': v.RegexStr()
          }

    self._RunTest(HasRegexStr,
                  'regexstr: "[a-z]+"\n',
                  {'regexstr': '[a-z]+',
                   })

    self._RunTest(HasRegexStr,
                  'regexstr:\n'
                  '- "[a-z]+"\n'
                  '- "(a-z)+"\n',
                  {'regexstr': '[a-z]+|(a-z)+',
                   })


if __name__ == '__main__':
  absltest.main()
