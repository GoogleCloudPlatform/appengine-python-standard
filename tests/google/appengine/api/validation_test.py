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

"""Unittest for google.appengine.api.validation."""

import re

import six

from google.appengine.api import validation
from absl.testing import absltest


class ValidatedTest(absltest.TestCase):
  """Unit test for Validated class."""

  def testBadAttributeVariable(self):
    """Class that does not properly define ATTRIBUTES can not be used."""

    class MissingAttributeVariable(validation.Validated):
      pass

    self.assertRaises(validation.AttributeDefinitionError,
                      MissingAttributeVariable)

    class WrongAttributeVariableType(validation.Validated):
      ATTRIBUTES = ['a', 'b', 'c']

    self.assertRaises(validation.AttributeDefinitionError,
                      WrongAttributeVariableType)

  def testUndefinedAttributes(self):
    """Getting undefined attribute raises exception."""

    class NoAttributes(validation.Validated):
      ATTRIBUTES = {}

    no_attributes = NoAttributes()
    self.assertRaises(AttributeError, getattr, no_attributes,
                      'not_an_attribute')
    self.assertRaisesRegex(
        validation.ValidationError, 'Unexpected attribute \'new_value\' for '
        'object of type NoAttributes.$', setattr, no_attributes, 'new_value',
        'value')

  def testUnvalidatedAttributes(self):
    """Test setting works with other attributes defined in class."""

    class HasOtherAttributes(validation.Validated):
      ATTRIBUTES = {}

      def __init__(self):
        self.__dict__['other_attribute'] = 'hello'

    other = HasOtherAttributes()
    self.assertEqual('hello', other.other_attribute)
    self.assertRaises(validation.ValidationError, setattr, other,
                      'other_attribute', 'goodbye')
    self.assertEqual('hello', other.other_attribute)

  def testSetAndGet(self):
    """Test setting various attributes."""

    class HasAttributes(validation.Validated):
      ATTRIBUTES = {
          'a': validation.TYPE_STR,
          'b': validation.TYPE_STR,
          'c': validation.TYPE_INT,
      }

    has_attributes = HasAttributes()
    with self.assertRaises(validation.MissingAttribute):
      has_attributes.CheckInitialized()

    self.assertEqual(validation.TYPE_STR, HasAttributes.GetValidator('a'))
    self.assertEqual(validation.TYPE_STR, HasAttributes.GetValidator('b'))
    self.assertEqual(validation.TYPE_INT, HasAttributes.GetValidator('c'))

    self.assertEqual(None, has_attributes.a)
    self.assertEqual(None, has_attributes.b)
    self.assertEqual(None, has_attributes.c)
    self.assertEqual(None, has_attributes.Get('a'))
    self.assertEqual(None, has_attributes.Get('b'))
    self.assertEqual(None, has_attributes.Get('c'))

    has_attributes.a = 'a string'
    has_attributes.b = 'another string'

    self.assertRaises(validation.ValidationError, validation.Validated.Get,
                      has_attributes, 'd')

    self.assertEqual('a string', has_attributes.a)
    self.assertEqual('another string', has_attributes.b)
    self.assertEqual(None, has_attributes.c)
    self.assertEqual('a string', has_attributes.Get('a'))
    self.assertEqual('another string', has_attributes.Get('b'))
    self.assertEqual(None, has_attributes.Get('c'))

    has_attributes.SetMultiple({'a': 1, 'b': 2, 'c': 3})

    self.assertEqual('1', has_attributes.a)
    self.assertEqual('2', has_attributes.b)
    self.assertEqual(3, has_attributes.c)
    self.assertEqual('1', has_attributes.Get('a'))
    self.assertEqual('2', has_attributes.Get('b'))
    self.assertEqual(3, has_attributes.Get('c'))

  def testDefaults(self):
    """Test default values."""

    class HasDefault(validation.Validated):
      ATTRIBUTES = {'a': validation.Type(str, default='a string')}

    self.assertEqual('a string', HasDefault().a)

  def testNormalizedValidators(self):

    class AbsValidator(validation.Normalized):

      def Get(self, value, key, obj):
        return abs(value)

      def Validate(self, value, key):
        if not isinstance(value, int):
          raise validation.ValidationError('Value for %s is not an int' % key)
        return value

    class WithNormalized(validation.Validated):
      ATTRIBUTES = {
          'a': AbsValidator(),
      }

    pos = WithNormalized(a=10)
    neg = WithNormalized(a=-10)
    self.assertEqual(pos.a, 10)
    self.assertEqual(neg.a, 10)
    self.assertEqual(pos.ToDict()['a'], 10)
    self.assertEqual(neg.ToDict()['a'], -10)
    self.assertRaises(validation.ValidationError, setattr, pos, 'a', 'ten')

  def testWarnings(self):

    class WarnValidator(validation.Validator):

      def Validate(self, value, key):
        return value

      def GetWarnings(self, value, key, obj):
        return [(key, 'Warning for %s' % value)]

    class InnerWithWarnings(validation.Validated):
      ATTRIBUTES = {'baz': WarnValidator()}

    class ValidatedWarningDict(validation.ValidatedDict):
      KEY_VALIDATOR = str
      VALUE_VALIDATOR = WarnValidator()

    class WithWarnings(validation.Validated):
      ATTRIBUTES = {
          'foo': WarnValidator(),
          'bar': InnerWithWarnings,
          'quux': ValidatedWarningDict,
      }

    w = WithWarnings(
        foo='x',
        bar=InnerWithWarnings(baz='y'),
        quux=ValidatedWarningDict(xyzzy='z'))
    self.assertEqual(
        set(w.GetWarnings()),
        set([('bar.baz', 'Warning for y'), ('foo', 'Warning for x'),
             ('quux.xyzzy', 'Warning for z')]))

  def testImplicitValidators(self):
    """Test setting various attributes."""

    class HasAttributes(validation.Validated):
      ATTRIBUTES = {'a': str, 'b': '[0-9]+', 'c': int, 'd': ('x', 'y', 'z')}

    has_attributes = HasAttributes()
    with self.assertRaises(validation.MissingAttribute):
      has_attributes.CheckInitialized()

    self.assertIsInstance(has_attributes.GetValidator('a'), validation.Type)
    self.assertIsInstance(has_attributes.GetValidator('b'), validation.Regex)
    self.assertIsInstance(has_attributes.GetValidator('c'), validation.Type)
    self.assertIsInstance(has_attributes.GetValidator('d'), validation.Options)


    self.assertRaises(validation.ValidationError, setattr, has_attributes, 'b',
                      'a string')
    self.assertRaises(validation.ValidationError, setattr, has_attributes, 'c',
                      'another string')
    self.assertRaises(validation.ValidationError, setattr, has_attributes, 'd',
                      'a')

    has_attributes.SetMultiple({'a': 1, 'b': 2, 'c': 3, 'd': 'y'})

    self.assertEqual('1', has_attributes.a)
    self.assertEqual('2', has_attributes.b)
    self.assertEqual(3, has_attributes.c)
    self.assertEqual('y', has_attributes.d)

  def testNonValidatedAttributes(self):
    """Validation does not interfere with setting normal attributes."""

    class HasNormalAttribute(validation.Validated):
      ATTRIBUTES = {}

      def __init__(self):
        super(HasNormalAttribute, self).__init__()
        self.__dict__['b'] = None

    has_normal_attribute = HasNormalAttribute()
    self.assertRaises(validation.ValidationError, setattr, has_normal_attribute,
                      'b', 'a string')
    self.assertEqual(None, has_normal_attribute.b)

  def testSetOnlyValidatedAttributes(self):
    """Only validated attributes of a class can be used in set."""

    class HasMixedAttributes(validation.Validated):
      ATTRIBUTES = {'a': str}

      def __init__(self):
        super(HasMixedAttributes, self).__init__()
        self.__dict__['b'] = None

    has_mixed_attributes = HasMixedAttributes()
    self.assertRaises(validation.ValidationError,
                      has_mixed_attributes.SetMultiple, {
                          'a': 'pple',
                          'b': 'erry'
                      })

  def testEquality(self):
    """Tests the equality operator."""

    class HasAttributes(validation.Validated):
      ATTRIBUTES = {
          'a': str,
          'b': validation.Repeated(int),
          'c': validation.Optional(str),
      }

    self.assertEqual(
        HasAttributes(a='str1', b=[1], c='str2'),
        HasAttributes(a='str1', b=[1], c='str2'))
    self.assertEqual(
        HasAttributes(a='str1', b=[1]), HasAttributes(a='str1', b=[1]))
    self.assertEqual(
        HasAttributes(a='str1', b=[1], c=None), HasAttributes(a='str1', b=[1]))
    self.assertNotEqual(
        HasAttributes(a='str3', b=[1], c='str2'),
        HasAttributes(a='str1', b=[1], c='str2'))
    self.assertNotEqual(
        HasAttributes(a='str1', b=[2], c='str2'),
        HasAttributes(a='str1', b=[1], c='str2'))
    self.assertNotEqual(
        HasAttributes(a='str1', b=[1], c='str4'),
        HasAttributes(a='str1', b=[1], c='str2'))

  def testHash(self):
    """Tests the hash operator."""

    class HasAttributes(validation.Validated):
      ATTRIBUTES = {
          'a': str,
          'b': validation.Repeated(int),
          'c': validation.Optional(str),
      }

    self.assertEqual(
        hash(HasAttributes(a='str1', b=[1], c='str2')),
        hash(HasAttributes(a='str1', b=[1], c='str2')))
    self.assertEqual(
        hash(HasAttributes(a='str1', b=[1])),
        hash(HasAttributes(a='str1', b=[1])))
    self.assertEqual(
        hash(HasAttributes(a='str1', b=[1], c=None)),
        hash(HasAttributes(a='str1', b=[1])))
    self.assertNotEqual(
        hash(HasAttributes(a='str3', b=[1], c='str2')),
        hash(HasAttributes(a='str1', b=[1], c='str2')))
    self.assertNotEqual(
        hash(HasAttributes(a='str1', b=[2], c='str2')),
        hash(HasAttributes(a='str1', b=[1], c='str2')))
    self.assertNotEqual(
        hash(HasAttributes(a='str1', b=[1], c='str4')),
        hash(HasAttributes(a='str1', b=[1], c='str2')))


class TestValidators(absltest.TestCase):
  """Tests for various validator classes."""

  def testType(self):
    """Tests typed values."""

    class Typed(validation.Validated):
      ATTRIBUTES = {
          'astring': validation.Type(str),
          'alist': validation.Type(list),
          'anint': validation.Type(int, False)
      }

    typed = Typed()

    typed.astring = 'string'
    self.assertEqual('string', typed.astring)
    typed.astring = 100
    self.assertEqual('100', typed.astring)

    typed.alist = ['a', 'b', 'c']
    self.assertEqual(['a', 'b', 'c'], typed.alist)
    typed.alist = 'def'
    self.assertEqual(['d', 'e', 'f'], typed.alist)
    self.assertRaises(validation.ValidationError, setattr, typed, 'alist', 10)

    typed.anint = 10
    self.assertEqual(10, typed.anint)
    self.assertRaises(validation.ValidationError, setattr, typed, 'anint',
                      '100')

    self.assertEqual(str, Typed.ATTRIBUTES['astring'].expected_type)
    self.assertEqual(list, Typed.ATTRIBUTES['alist'].expected_type)
    self.assertEqual(int, Typed.ATTRIBUTES['anint'].expected_type)

  def testExec(self):
    """Tests setting entrypoint commands."""

    class Entrypoint(validation.Validated):
      ATTRIBUTES = {'entrypoint': validation.Exec()}

    validated = Entrypoint()
    validated.entrypoint = 'python main.py'
    self.assertEqual('exec python main.py', validated.entrypoint)

    validated_shell_exec = Entrypoint()
    validated_shell_exec.entrypoint = 'exec python main.py'
    self.assertEqual('exec python main.py', validated_shell_exec.entrypoint)

    validated_noshell_exec = Entrypoint()
    validated_noshell_exec.entrypoint = '["python", "main.py"]'
    self.assertEqual('["python", "main.py"]', validated_noshell_exec.entrypoint)

    validated_integer = Entrypoint()
    validated_integer.entrypoint = 1234
    self.assertEqual('exec 1234', validated_integer.entrypoint)

  def testOptions(self):
    """Tests setting option values."""

    class Optioned(validation.Validated):
      ATTRIBUTES = {
          'color': validation.Options('red', 'green', 'blue'),
          'size': validation.Options('big', 'small', 'medium')
      }

    optioned = Optioned()
    with self.assertRaises(validation.MissingAttribute):
      optioned.CheckInitialized()

    optioned.color = 'red'
    self.assertEqual('red', optioned.color)
    optioned.color = 'green'
    self.assertEqual('green', optioned.color)
    optioned.color = 'blue'
    self.assertEqual('blue', optioned.color)

    optioned.size = 'big'
    self.assertEqual('big', optioned.size)
    optioned.size = 'small'
    self.assertEqual('small', optioned.size)
    optioned.size = 'medium'
    self.assertEqual('medium', optioned.size)

    self.assertRaises(validation.ValidationError, setattr, optioned, 'color',
                      'purple')
    self.assertRaises(validation.ValidationError, setattr, optioned, 'size',
                      'wee')

    self.assertEqual(object, Optioned.ATTRIBUTES['color'].expected_type)
    self.assertEqual(object, Optioned.ATTRIBUTES['size'].expected_type)

  def testOptionsAlias(self):
    """Test option aliases."""

    class AliasOptioned(validation.Validated):
      ATTRIBUTES = {
          'color':
              validation.Options(('red', ['r', 'RED']),
                                 ('green', ('g', 'GREEN')),
                                 ('blue', ['b', 'BLUE']))
      }

    self.assertEqual('red', AliasOptioned(color='red').color)
    self.assertEqual('red', AliasOptioned(color='r').color)
    self.assertEqual('red', AliasOptioned(color='RED').color)
    self.assertEqual('green', AliasOptioned(color='green').color)
    self.assertEqual('green', AliasOptioned(color='g').color)
    self.assertEqual('green', AliasOptioned(color='GREEN').color)
    self.assertEqual('blue', AliasOptioned(color='blue').color)
    self.assertEqual('blue', AliasOptioned(color='b').color)
    self.assertEqual('blue', AliasOptioned(color='BLUE').color)

  def testOptionsMustBeStr(self):
    """Test that using option that is not str fails."""





    self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                      1)

    if six.PY2:
      self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                        u'must-be-str')

    elif six.PY3:
      self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                        b'must-be-str')
    self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                      (1, ('must-be-str',)))
    self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                      ('original', (1,)))

  def testNoDuplicatesAllowed(self):
    """Test that duplicate options are caught."""
    self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                      'name1', 'name1')
    self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                      'name1', ('name1', 'name2'))
    self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                      ('name1', ('name2', 'name1')))

  def testAliasesMustBeListOrTuple(self):
    """Tests that alias lists must be a list or tuple"""
    self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                      ('original', 'no!'))

  def testAliasListOnlyTwoElements(self):
    """Tests that the alias list can only have two elements.

    This feature helps make it easier for users to detect errors by
    raises a specific message using an attribute definition error
    rather than ValueError (from too many/few values to unpack).
    """
    self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                      ('original', ('like-this!',), 'What'))
    self.assertRaises(validation.AttributeDefinitionError, validation.Options,
                      ('original',))

  def testOptionsValidateConvertsToStr(self):
    """Test that Options.Validate converts values to str before check."""

    class Application(validation.Validated):
      ATTRIBUTES = {'api_version': validation.Options('1', '1.2')}

    self.assertEqual('1', Application(api_version=1).api_version)
    self.assertEqual('1.2', Application(api_version=1.2).api_version)

  def testOptional(self):
    """Test required attribute."""

    class OptionalStuff(validation.Validated):
      ATTRIBUTES = {
          'optional': validation.Optional(validation.TYPE_STR),
          'implicit_type': validation.Optional(int, default=2001),
          'implicit_regex': validation.Optional('[0-9]+'),
          'implicit_options': validation.Optional(('a', 'b', 'c')),
      }

    optional_stuff = OptionalStuff()

    self.assertEqual(None, optional_stuff.optional)
    self.assertEqual(2001, optional_stuff.implicit_type)
    self.assertEqual(None, optional_stuff.implicit_regex)
    self.assertEqual(None, optional_stuff.implicit_options)

    for attribute, valid_value, invalid_value in (
        ('optional', 'a string', None),
        ('implicit_type', 20, 'a string'),
        ('implicit_regex', '25', 'not numeric'),
        ('implicit_options', 'a', 'z'),
    ):

      setattr(optional_stuff, attribute, valid_value)
      self.assertEqual(valid_value, getattr(optional_stuff, attribute))


      setattr(optional_stuff, attribute, None)
      self.assertEqual(None, getattr(optional_stuff, attribute))



      if invalid_value is not None:
        try:
          setattr(optional_stuff, attribute, invalid_value)
        except validation.ValidationError:
          pass
        else:
          self.fail(
              'Setting Attribute %s to %s does not raise ValidationError' %
              (attribute, str(invalid_value)))

  def testRegex(self):
    """Test regular expressions."""

    class Regexes(validation.Validated):
      ATTRIBUTES = {
          'number':
              validation.Regex(r'-?[0-9]+(\.[0-9]+)?', str),
          'identifier':
              validation.Regex(r'[a-zA-Z0-9_]+', six.text_type),
          'choice':
              validation.Regex(r'dog|cat|pony', str),
      }

    regexes = Regexes()
    with self.assertRaises(validation.MissingAttribute):
      regexes.CheckInitialized()

    regexes.number = '100'
    self.assertEqual('100', regexes.number)
    regexes.number = '3.14'
    self.assertEqual('3.14', regexes.number)
    regexes.number = -20
    self.assertEqual('-20', regexes.number)
    self.assertIsInstance(regexes.number, str)
    self.assertRaises(validation.ValidationError, setattr, regexes, 'number',
                      'I do not match')
    self.assertRaises(validation.ValidationError, setattr, regexes, 'number',
                      '-1a2')

    regexes.identifier = 'an_identifier'
    self.assertEqual('an_identifier', regexes.identifier)
    self.assertIsInstance(regexes.identifier, six.text_type)

    regexes.choice = 'dog'
    self.assertEqual('dog', regexes.choice)
    regexes.choice = 'cat'
    self.assertEqual('cat', regexes.choice)
    regexes.choice = 'pony'
    self.assertEqual('pony', regexes.choice)

    self.assertRaises(validation.ValidationError, setattr, regexes, 'choice',
                      'dogonalog')
    self.assertRaises(validation.ValidationError, setattr, regexes, 'choice',
                      'catinahat')
    self.assertRaises(validation.ValidationError, setattr, regexes, 'choice',
                      'ponycalledtony')
    self.assertRaises(validation.ValidationError, setattr, regexes, 'choice',
                      'fatcat')

    self.assertEqual(str, Regexes.ATTRIBUTES['number'].expected_type)
    self.assertEqual(six.text_type,
                     Regexes.ATTRIBUTES['identifier'].expected_type)
    self.assertEqual(str, Regexes.ATTRIBUTES['choice'].expected_type)

  def testBadRegexDefinitions(self):
    """Tests bad constructors for regex."""
    self.assertRaises(validation.AttributeDefinitionError, validation.Regex,
                      r'.', int)
    self.assertRaises(validation.AttributeDefinitionError,
                      validation.Regex, re.compile('\w'))

  def testRegexStr(self):
    """Test fields that are supposed to be regular expressions."""

    class RegexStrs(validation.Validated):
      ATTRIBUTES = {
          're1': validation.RegexStr(),
          'has_default': validation.RegexStr(string_type=str, default='foo.*'),
      }

    regex_strs = RegexStrs()
    with self.assertRaises(validation.MissingAttribute):
      regex_strs.CheckInitialized()

    regex_strs.re1 = 'a|b.*'
    self.assertEqual('a|b.*', str(regex_strs.re1))
    regex_strs.re1 = 'a|\nb.*'
    self.assertEqual('a|b.*', str(regex_strs.re1))
    self.assertEqual('foo.*', str(regex_strs.has_default))

    self.assertIsInstance(regex_strs.re1.regex.pattern, six.text_type)
    self.assertIsInstance(str(regex_strs.has_default), str)

    self.assertRaises(validation.ValidationError, setattr, regex_strs, 're1',
                      'a(b')

  def testRegexStrEquality(self):
    """Tests equality comparison of regular expression objects."""

    class RegexStrs(validation.Validated):
      ATTRIBUTES = {
          're': validation.RegexStr(),
      }

    validated1 = RegexStrs()
    validated1.re = r'a|b'

    validated2 = RegexStrs()
    validated2.re = ['a', 'b']

    validated3 = RegexStrs()
    validated3.re = ['b', 'c']

    self.assertEqual(validated1, validated2)
    self.assertNotEqual(validated1, validated3)
    self.assertNotEqual(validated2, validated3)

  def testBadRegexStrDefinitions(self):
    """Tests bad constructors for RegexStr."""
    self.assertRaises(validation.AttributeDefinitionError, validation.Regex,
                      int)

  def testRange(self):
    """Tests range validator."""

    class Ranged(validation.Validated):
      ATTRIBUTES = {'rating': validation.Range(1, 10)}

    ranged = Ranged()

    ranged.rating = 1
    self.assertEqual(1, ranged.rating)
    ranged.rating = 4
    self.assertEqual(4, ranged.rating)
    ranged.rating = 10
    self.assertEqual(10, ranged.rating)
    ranged.rating = 3.4
    self.assertEqual(3, ranged.rating)
    self.assertRaises(validation.ValidationError, setattr, ranged, 'rating', 0)
    self.assertRaises(validation.ValidationError, setattr, ranged, 'rating', 11)

    self.assertEqual(int, Ranged.ATTRIBUTES['rating'].expected_type)
    self.assertEqual(float, validation.Range(0.0, 1.0, float).expected_type)

  def testRangeNoMin(self):
    """Tests range validation with no minimum value."""

    class Ranged(validation.Validated):
      ATTRIBUTES = {'rating': validation.Range(None, 10)}

    ranged = Ranged()

    ranged.rating = -100
    self.assertEqual(-100, ranged.rating)
    ranged.rating = -100.1
    self.assertEqual(-100, ranged.rating)
    ranged.rating = 10
    self.assertEqual(10, ranged.rating)
    self.assertRaises(validation.ValidationError, setattr, ranged, 'rating', 11)

  def testRangeNoMax(self):
    """Tests range validation with no maximum value."""

    class Ranged(validation.Validated):
      ATTRIBUTES = {'rating': validation.Range(1, None)}

    ranged = Ranged()

    ranged.rating = 100
    self.assertEqual(100, ranged.rating)
    ranged.rating = 100.1
    self.assertEqual(100, ranged.rating)
    ranged.rating = 1
    self.assertEqual(1, ranged.rating)
    self.assertRaises(validation.ValidationError, setattr, ranged, 'rating', 0)

  def testBadRangeDefinitions(self):
    """Tests bad constructors for range."""
    self.assertRaises(validation.AttributeDefinitionError, validation.Range,
                      '10', 20, int)
    self.assertRaises(validation.AttributeDefinitionError, validation.Range, 10,
                      10.2, int)
    self.assertRaises(validation.AttributeDefinitionError, validation.Range,
                      None, None, int)

  def testRepeated(self):
    """Tests a repeated field."""

    class Stuff(validation.Validated):
      ATTRIBUTES = {
          'names': validation.Repeated(str),
          'numbers': validation.Repeated(int),
      }

    stuff = Stuff()
    with self.assertRaises(validation.MissingAttribute):
      stuff.CheckInitialized()
    stuff.names = ['jon', 'ryan', 'ken', 'kevin']
    self.assertEqual(['jon', 'ryan', 'ken', 'kevin'], stuff.names)
    stuff.numbers = [12, 23, 34, 54]
    self.assertEqual([12, 23, 34, 54], stuff.numbers)
    stuff.names = []
    self.assertEqual([], stuff.names)

    self.assertRaises(validation.ValidationError, setattr, stuff, 'names',
                      'jon')
    self.assertRaises(validation.ValidationError, setattr, stuff, 'names',
                      ['jon', 1])

    self.assertEqual(str, Stuff.ATTRIBUTES['names'].constructor)
    self.assertEqual(int, Stuff.ATTRIBUTES['numbers'].constructor)

    self.assertEqual(list, Stuff.ATTRIBUTES['names'].expected_type)
    self.assertEqual(list, Stuff.ATTRIBUTES['numbers'].expected_type)

  def testOptionalRepeated(self):
    """Validators run on CheckInitialized too."""



    class Name(validation.Validated):
      ATTRIBUTES = {
          'name':
              validation.Optional(
                  validation.Repeated(validation.Options('anders', 'stefan'))),
      }

    n = Name()
    n.CheckInitialized()
    n.name = []
    n.CheckInitialized()
    n.name.append('branders')
    with self.assertRaises(validation.ValidationError):
      n.CheckInitialized()

  def testRepeatedValidator(self):
    """Tests a repeated validator field."""

    class Stuff(validation.Validated):
      ATTRIBUTES = {
          'services': validation.Repeated(validation.Regex('mail|xmpp')),
      }

    stuff = Stuff()
    with self.assertRaises(validation.MissingAttribute):
      stuff.CheckInitialized()
    stuff.services = ['mail']
    self.assertEqual(['mail'], stuff.services)
    stuff.services = ['xmpp']
    self.assertEqual(['xmpp'], stuff.services)
    stuff.services = ['mail', 'xmpp']
    self.assertEqual(['mail', 'xmpp'], stuff.services)
    stuff.services = []
    self.assertEqual([], stuff.services)

    def AssertRegexError(value, expected_message):
      with self.assertRaises(validation.ValidationError) as e:
        stuff.services = value
        self.fail('Did not raise validation error.')
      self.assertEqual(expected_message, str(e.exception))

    AssertRegexError(
        'mail', "Value 'mail' for services should be a sequence but is not.")
    AssertRegexError(['blobstore'],
                     "Value 'blobstore' for services does not match expression "
                     "'^(?:mail|xmpp)$'")

  def testTimeValue(self):
    """Test a time value field."""

    class Stuff(validation.Validated):
      ATTRIBUTES = {
          'time': validation.TimeValue(),
      }

    stuff = Stuff()
    stuff.time = '1h'
    self.assertEqual('1h', stuff.time)

    stuff = Stuff()
    stuff.time = '1.3d'
    self.assertEqual('1.3d', stuff.time)

    stuff = Stuff()
    stuff.time = '1.3e+9s'
    self.assertEqual('1.3e+9s', stuff.time)

    def AssertTimeValueError(value, expected_message):
      with self.assertRaises(validation.ValidationError) as e:
        stuff.time = value
        self.fail('Did not raise validation error for %s' % value)
      self.assertEqual(expected_message, str(e.exception))

    AssertTimeValueError(
        23, "Value '23' for time is not a string "
        '(must be a non-negative number followed by a time unit, '
        'such as 1h or 3.5d)')
    AssertTimeValueError(
        '', 'Value for time is empty '
        '(must be a non-negative number followed by a time unit, '
        'such as 1h or 3.5d)')
    for bad_time_unit in ['23', '5x']:
      AssertTimeValueError(
          bad_time_unit, "Value '%s' for time must end with a time unit, "
          'one of s (seconds), m (minutes), h (hours), or d (days)' %
          bad_time_unit)
    for bad_number in ['s', '97.2.3s', '9e--5s']:
      AssertTimeValueError(
          bad_number, "Value '%s' for time is not a valid time value "
          '(must be a non-negative number followed by a time '
          'unit, such as 1h or 3.5d)' % bad_number)
    AssertTimeValueError(
        '-2s', "Value '-2s' for time is negative "
        '(must be a non-negative number followed by a time '
        'unit, such as 1h or 3.5d)')

  def testDeprecatedValue(self):

    class WithDeprecated(validation.Validated):
      ATTRIBUTES = {
          'old': validation.Deprecated('new', str),
          'new': validation.Preferred('old', str),
      }

    new_normal = WithDeprecated(new='foo')
    new_normal.CheckInitialized()
    old_normal = WithDeprecated(old='bar')
    old_normal.CheckInitialized()


    with self.assertRaises(validation.ValidationError):
      WithDeprecated(new='foo', old='bar').CheckInitialized()


    with self.assertRaises(validation.ValidationError):
      WithDeprecated().CheckInitialized()

    self.assertEqual(new_normal.new, 'foo')
    self.assertEqual(new_normal.old, 'foo')
    self.assertEqual(new_normal.GetWarnings(), [])

    self.assertEqual(old_normal.new, 'bar')
    self.assertEqual(old_normal.old, 'bar')
    warnings = old_normal.GetWarnings()
    self.assertLen(warnings, 1)
    key, warn = warnings[0]
    self.assertEqual(key, 'old')
    self.assertIn('deprecated', warn)

    self.assertEqual(new_normal.ToDict(), {'new': 'foo'})
    self.assertEqual(old_normal.ToDict(), {'old': 'bar'})

  def testDeprecatedWithOptional(self):

    class WithDeprecated(validation.Validated):
      ATTRIBUTES = {
          'old': validation.Deprecated('new', validation.Optional(str)),
          'new': validation.Preferred('old', validation.Optional(str)),
      }

    new_normal = WithDeprecated(new='foo')
    new_normal.CheckInitialized()
    old_normal = WithDeprecated(old='bar')
    old_normal.CheckInitialized()


    with self.assertRaises(validation.ValidationError):
      WithDeprecated(new='foo', old='bar').CheckInitialized()


    WithDeprecated().CheckInitialized()

    self.assertEqual(new_normal.new, 'foo')
    self.assertEqual(new_normal.old, 'foo')
    self.assertEqual(new_normal.GetWarnings(), [])

    self.assertEqual(old_normal.new, 'bar')
    self.assertEqual(old_normal.old, 'bar')
    warnings = old_normal.GetWarnings()
    self.assertLen(warnings, 1)
    key, warn = warnings[0]
    self.assertEqual(key, 'old')
    self.assertIn('deprecated', warn)

    self.assertEqual(new_normal.ToDict(), {'new': 'foo'})
    self.assertEqual(old_normal.ToDict(), {'old': 'bar'})

  def testDeprecatedValueWithDefaults(self):

    class WithDeprecated(validation.Validated):
      ATTRIBUTES = {
          'old': validation.Deprecated('new', str, 'oldold'),
          'new': validation.Preferred('old', str, 'newnew'),
      }

    nothing_set = WithDeprecated()
    new_normal = WithDeprecated(new='foo')
    new_normal.CheckInitialized()
    old_normal = WithDeprecated(old='bar')
    old_normal.CheckInitialized()
    with self.assertRaises(validation.ValidationError):
      WithDeprecated(new='foo', old='bar').CheckInitialized()

    self.assertEqual(new_normal.new, 'foo')
    self.assertEqual(new_normal.old, 'foo')
    self.assertEqual(new_normal.GetWarnings(), [])

    self.assertEqual(old_normal.new, 'bar')
    self.assertEqual(old_normal.old, 'bar')
    warnings = old_normal.GetWarnings()
    self.assertLen(warnings, 1)
    key, warn = warnings[0]
    self.assertEqual(key, 'old')
    self.assertIn('deprecated', warn)

    self.assertEqual(new_normal.ToDict(), {'new': 'foo'})
    self.assertEqual(old_normal.ToDict(), {'old': 'bar'})

    self.assertEqual(nothing_set.new, 'newnew')
    self.assertEqual(nothing_set.old, 'oldold')

    self.assertEqual(new_normal.ToDict(), {'new': 'foo'})
    self.assertEqual(old_normal.ToDict(), {'old': 'bar'})
    self.assertEqual(nothing_set.ToDict(), {})


class CapitalizedKeysStringValues(validation.ValidatedDict):
  """A dictionary that maps capitalized strings to strings."""
  KEY_VALIDATOR = validation.Regex('[A-Z].*')
  VALUE_VALIDATOR = six.string_types


class ValidatedDictTest(absltest.TestCase):
  """Unit test for ValidatedDict class."""

  def testSetLegalAttribute(self):
    """Test that legal items are accepted in various ways."""
    d = CapitalizedKeysStringValues()
    d.Set('Hello', 'there')
    d['You'] = 'are'
    d['Very'] = ''

    expected = {'Hello': 'there', 'You': 'are', 'Very': ''}

    self.assertDictEqual(d, expected)

    d.clear()
    self.assertDictEqual(d, {})

    d.update(expected)
    self.assertDictEqual(d, expected)

    d.clear()
    self.assertEqual('there', d.setdefault('Hello', 'there'))
    self.assertEqual('there', d.setdefault('Hello', 'now'))
    self.assertEqual('are', d.setdefault('You', 'are'))
    self.assertEqual('', d.setdefault('Very', ''))
    self.assertDictEqual(d, expected)

  def testSetIllegalAttribute(self):
    """Test that illegal items are rejected"""
    d = CapitalizedKeysStringValues()
    illegal_keys = {
        'key': 'lowercase',
        '': 'empty',
        323: 'number',
    }
    illegal_values = {
        'Number': 1342,
        'List': ['a', 'b', 'c'],
        'Tuple': ('a', 'b', 'c')
    }

    illegal_items = {}
    illegal_items.update(illegal_keys)
    illegal_items.update(illegal_values)

    def assignWithBrackets(key, val):
      d[key] = val

    for k, v in six.iteritems(illegal_keys):
      self.assertRaisesRegex(
          validation.ValidationError,
          'Value \'%s\' for key in CapitalizedKeysStringValues '
          'does not match expression %s$' % (k, re.escape('\'^(?:[A-Z].*)$\'')),
          CapitalizedKeysStringValues.Set, d, k, v)
      self.assertRaises(validation.ValidationError,
                        CapitalizedKeysStringValues.__setitem__, d, k, v)
      self.assertRaises(validation.ValidationError, assignWithBrackets, k, v)

    for k, v in six.iteritems(illegal_values):
      self.assertRaisesRegex(
          validation.ValidationError,
          re.escape('Value %r for %s is not a valid text string' % (v, k)),
          CapitalizedKeysStringValues.Set, d, k, v)
      self.assertRaises(validation.ValidationError,
                        CapitalizedKeysStringValues.__setitem__, d, k, v)
      self.assertRaises(validation.ValidationError, assignWithBrackets, k, v)

    self.assertDictEqual(d, {})

    self.assertRaises(validation.ValidationError,
                      CapitalizedKeysStringValues.update, d, illegal_items)
    self.assertDictEqual(d, {})

    self.assertRaises(validation.ValidationError,
                      CapitalizedKeysStringValues.setdefault, d, 'key', 'value')
    self.assertRaises(validation.ValidationError,
                      CapitalizedKeysStringValues.setdefault, d, 'Key',
                      [1, 2, 3])
    self.assertDictEqual(d, {})

  def testToDict(self):
    """Test the ToDict method."""

    class ValidatedInner(validation.Validated):
      ATTRIBUTES = {'name': validation.Type(str), 'job': validation.Type(str)}

    class ValidatedMiddle(validation.ValidatedDict):

      def __init__(self):
        pass

      def GetValidator(self, key):
        if six.ensure_str(key).startswith('employee'):
          return validation.Type(ValidatedInner)
        return validation.Type(str)

    class ValidatedOuter(validation.Validated):
      ATTRIBUTES = {'params': ValidatedMiddle}

    middle = ValidatedMiddle()
    middle['employee_joe'] = ValidatedInner(name='joe', job='plumber')
    middle['employee_ed'] = ValidatedInner(name='ed', job='educator')
    middle['key1'] = 'value1'
    middle['key2'] = 'value2'

    outer = ValidatedOuter()
    outer.params = middle

    self.assertDictEqual(
        outer.ToDict(), {
            'params': {
                'employee_joe': {
                    'name': 'joe',
                    'job': 'plumber',
                },
                'employee_ed': {
                    'name': 'ed',
                    'job': 'educator',
                },
                'key1': 'value1',
                'key2': 'value2',
            }
        })


class TestToDict(absltest.TestCase):
  """Tests conversion of validated objects to dictionaries.

  Includes tests for ToYAML as it is dependant on ToDict.
  """

  def testOneLevel(self):
    """Tests a flat one level dictionary."""

    class OneLevel(validation.Validated):
      ATTRIBUTES = {
          'key1': validation.Type(str),
          'key2': validation.Type(int),
      }

    self.assertEqual({
        'key1': 'value1',
        'key2': 100
    },
                     OneLevel(key1='value1', key2=100).ToDict())

  def testTwoLevels(self):
    """Tests a flat one level dictionary."""

    class Nested(validation.Validated):
      ATTRIBUTES = {
          'key1': validation.Type(str),
          'key2': validation.Type(int),
      }

    class HasNested(validation.Validated):
      ATTRIBUTES = {
          'key1': validation.Type(str),
          'key2': validation.Type(Nested),
      }

    self.assertEqual(
        {
            'key1': 'value1',
            'key2': {
                'key1': 'nested-value1',
                'key2': 200,
            },
        },
        HasNested(key1='value1', key2=Nested(key1='nested-value1',
                                             key2=200)).ToDict())

  def testWithRepeated(self):
    """Tests converting repeated fields to lists."""

    class HasRepeated(validation.Validated):
      ATTRIBUTES = {'list1': validation.Repeated(int)}

    self.assertEqual({'list1': [1, 2, 3]},
                     HasRepeated(list1=[1, 2, 3]).ToDict())

  def testWithRepeatedNested(self):
    """Tests converting repeated fields which are nested objects to list."""

    class Nested(validation.Validated):
      ATTRIBUTES = {'key1': validation.Type(int)}

    class HasRepeatedNested(validation.Validated):
      ATTRIBUTES = {'list1': validation.Repeated(Nested)}

    self.assertEqual({'list1': [{
        'key1': 1
    }, {
        'key1': 2
    }, {
        'key1': 3
    }]},
                     HasRepeatedNested(list1=[
                         Nested(key1=1),
                         Nested(key1=2),
                         Nested(key1=3),
                     ]).ToDict())

  def testOptional(self):
    """Tests output of optional fields."""

    class HasOptionals(validation.Validated):
      ATTRIBUTES = {
          'optional1': validation.Optional(str),
          'optional2': validation.Optional(int),
          'optional3': validation.Optional(validation.RegexStr())
      }

    self.assertEqual({'optional1': 'was-set'},
                     HasOptionals(optional1='was-set').ToDict())




    result_dict = HasOptionals(optional3='nice.regexp').ToDict()
    self.assertEqual({'optional3': 'nice.regexp'}, result_dict)
    self.assertEqual(repr('nice.regexp'), repr(result_dict['optional3']))

  def testToYAML(self):
    """Tests conversion of validated object to YAML."""

    class Cat(validation.Validated):
      ATTRIBUTES = {
          'name': validation.Type(str),
          'age': int,
          'whiskers': validation.Optional(int),
      }

    class CatStore(validation.Validated):
      ATTRIBUTES = {
          'name': validation.Type(str),
          'address': validation.Optional(str),
          'cats': validation.Repeated(Cat),
      }

    expected_output = ('address: 12 Meowy Cls.\n'
                       'cats:\n'
                       '- age: 7\n'
                       '  name: Jack\n'
                       '  whiskers: 20\n'
                       '- age: 4\n'
                       '  name: Vespa\n'
                       'name: The Cattery\n')

    self.assertEqual(
        expected_output,
        CatStore(
            name='The Cattery',
            address='12 Meowy Cls.',
            cats=[
                Cat(name='Jack', age=7, whiskers=20),
                Cat(name='Vespa', age=4)
            ]).ToYAML())

  def testToYAMLOrderedDict(self):
    """Tests conversion of validated object to YAML."""

    class Five(validation.Validated):
      ATTRIBUTES = {
          'one': int,
          'two': int,
          'three': int,
          'four': int,
          'five': int,
      }

      def ToDict(self):
        return validation.SortedDict(['one', 'two', 'three', 'four', 'five'],
                                     super(Five, self).ToDict())

    expected_output = ('one: 1\n'
                       'two: 2\n'
                       'three: 3\n'
                       'four: 4\n'
                       'five: 5\n')

    self.assertEqual(expected_output,
                     Five(one=1, two=2, three=3, four=4, five=5).ToYAML())

  def testDefaultValues(self):
    """Test that default values on optional fields are ignored."""

    class HasDefaults(validation.Validated):
      ATTRIBUTES = {
          'prop1': validation.Type(str, default='required default'),
          'prop2': validation.Optional(str),
          'prop3': validation.Optional(str, default='optional default'),
      }



    self.assertEqual('prop3: null\n', HasDefaults(prop3=None).ToYAML())
    self.assertEqual('{}\n', HasDefaults().ToYAML())

  def testRegexStr(self):
    """Test that RegexStr objects are converted to strings."""

    class HasRegex(validation.Validated):
      ATTRIBUTES = {
          'prop1': validation.RegexStr(default='.*'),
          'prop2': validation.RegexStr(),
          'prop3': validation.Regex('foo.*'),
      }

    self.assertEqual("prop2: '[a-z]*'\nprop3: foobar\n",
                     HasRegex(prop2='[a-z]*', prop3='foobar').ToYAML())
    self.assertEqual("prop2: '10'\nprop3: foobar\n",
                     HasRegex(prop2=10, prop3='foobar').ToYAML())


if __name__ == '__main__':
  absltest.main()

