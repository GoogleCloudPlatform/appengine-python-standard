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

"""Tests for google.appengine.api.search.search."""

import copy
import datetime
import logging
import math
import pickle
import re
import sys

import google

from absl import app
import mox
import six
from six.moves import range

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import module_testutil
from google.appengine.api import namespace_manager
from google.appengine.api.search import search
from google.appengine.api.search import search_service_pb2
from google.appengine.runtime import apiproxy_errors
from google.appengine.datastore import document_pb2
from absl.testing import absltest



NUMBERS = [1, 1.0]


OK = search_service_pb2.SearchServiceError.OK
TRANSIENT_ERROR = search_service_pb2.SearchServiceError.TRANSIENT_ERROR
INTERNAL_ERROR = search_service_pb2.SearchServiceError.INTERNAL_ERROR
INVALID_REQUEST = search_service_pb2.SearchServiceError.INVALID_REQUEST

PUBLIC_OK = search.OperationResult.OK
PUBLIC_TRANSIENT_ERROR = search.OperationResult.TRANSIENT_ERROR
PUBLIC_INTERNAL_ERROR = search.OperationResult.INTERNAL_ERROR
PUBLIC_INVALID_REQUEST = search.OperationResult.INVALID_REQUEST


_NON_STRING_VALUES = NUMBERS


_NON_NUMBER_VALUES = ['test', True, search_service_pb2, datetime]


_ILLEGAL_LANGUAGE_CODES = ['', 'e', 'burt', 'en_USA', '_', 'three', '_zzz']


_UNICODE_STRING = u'ma\xe7a'
_UNICODE_AS_UTF8 = b'ma\xc3\xa7a'
_UNICODE_QUERY = u'text:"ma\xe7a" OR post_title:ma\xe7a'
_UNICODE_QUERY_ESCAPED = u'text:\\\"ma\xe7a\\\" OR post_title:ma\xe7a'

_DATE = datetime.date(2010, 1, 1)
_DATE_STRING = _DATE.isoformat()
_DATE_LONG_STRING = '1262304000000'

_DATE_TIME = datetime.datetime(2010, 1, 1, 11, 45, 25, tzinfo=None)
_DATE_TIME_STRING = _DATE_TIME.isoformat()
_DATE_TIME_LONG_STRING = '1262346325000'

_VISIBLE_PRINTABLE_ASCII = ''.join(
    [chr(printable) for printable in range(33, 127)]).replace('!', '')
_VISIBLE_PRINTABLE_ASCII_UNICODE = u'' + _VISIBLE_PRINTABLE_ASCII
_LOWER_NON_VISIBLE_PRINTABLE_ASCII = [
    str(chr(lower_non)) for lower_non in range(0, 32)]
_UPPER_NON_VISIBLE_PRINTABLE_ASCII = [
    str(chr(past_printable)) for past_printable in range(127, 250)]


_GEO_POINT = search.GeoPoint(latitude=-33.84, longitude=151.26)


_MAX_STORAGE = 1024 * 1024 * 1024

class EqualsProto(mox.Comparator):
  """A mox comparator for protocol buffers.

  If the protos are different a warning is logged, which includes the contents
  of the expected and actual protos.
  """

  def __init__(self, expected):
    self._expected = expected

  def equals(self, actual):
    if not self._expected == actual:
      logging.warning('EqualsProto match failed:')
      logging.warning('EXPECTED: %s', self._expected)
      logging.warning('ACTUAL  : %s', actual)
      return False
    return True


class ModuleInterfaceTest(module_testutil.ModuleInterfaceTest,
                          absltest.TestCase):
  MODULE = search


class TestCase(absltest.TestCase):

  def assertReprEqual(self, expected_text, actual_text):
    """Asserts equality between the given string and the object representation.

    NOTE(user): I wouldn't say I'm proud of this approach, but I think it's the
    least-bad way to modernize these tests. The core issue is that
    repr(six.text_type('asdf')) legitimately differs between Python 2 and 3
    (e.g. the 'u' unicode prefix is now omitted in PY3). Unfortunately, this
    module contains *tons* of assertions of the exact output of __repr__(). As I
    see it, the available options are:

    1) Modify the __repr__() implementations in question to give PY3 results for
       PY2 (e.g. omit the 'u' prefix for PY2 unicodes), which *could* break
       existing code, and would technically be inaccurate.

    2) Modify the __repr__() implementations to give PY2 results for PY3 (e.g.
       reintroduce the 'u' prefix for PY3 strs), which would also be technically
       inaccurate.

    3) Modify the tests to make slightly different assertions depending on the
       Python version, which is what's going on below. Rather than just dupe
       piles of assertions en masse, I created this helper method to make things
       slightly less messy.
    """
    if six.PY3:


      expected_text = re.sub(r"=u'", "='", expected_text)



      expected_text = expected_text.encode('utf-8').decode('unicode_escape')

    self.assertEqual(expected_text, actual_text)


class GeoPointTest(absltest.TestCase):

  def testRequiredArgumentsMissing(self):
    self.assertRaises(TypeError, search.GeoPoint)
    self.assertRaises(TypeError, search.GeoPoint, latitude=_GEO_POINT.latitude)
    self.assertRaises(TypeError, search.GeoPoint,
                      longitude=_GEO_POINT.longitude)

  def testRanges(self):
    geo = search.GeoPoint(latitude=-90.0, longitude=-180.0)
    self.assertEqual(-90.0, geo.latitude)
    self.assertEqual(-180.0, geo.longitude)
    geo = search.GeoPoint(latitude=90.0, longitude=-180.0)
    self.assertEqual(90.0, geo.latitude)
    self.assertEqual(-180.0, geo.longitude)
    geo = search.GeoPoint(latitude=90.0, longitude=180.0)
    self.assertEqual(90.0, geo.latitude)
    self.assertEqual(180.0, geo.longitude)
    self.assertRaises(
        ValueError, search.GeoPoint, latitude=-90.1, longitude=0.0)
    self.assertRaises(
        ValueError, search.GeoPoint, latitude=0.0, longitude=-180.1)
    self.assertRaises(
        ValueError, search.GeoPoint, latitude=90.1, longitude=0)
    self.assertRaises(
        ValueError, search.GeoPoint, latitude=0.0, longitude=180.1)

  def testWrongTypes(self):
    self.assertRaises(TypeError, search.GeoPoint, latitude='-90.0')
    self.assertRaises(TypeError, search.GeoPoint, longitude='-90.0')

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.GeoPoint, foo='bar')

  def testRepr(self):
    self.assertEqual(
        'search.GeoPoint(latitude=%r, longitude=%r)' % (-33.84, 151.26),
        repr(_GEO_POINT))

  def testEq(self):
    gp1 = search.GeoPoint(latitude=-10.00, longitude=10.00)
    gp2 = search.GeoPoint(latitude=-20.00, longitude=20.00)
    self.assertEqual(gp1, gp1)
    self.assertEqual(gp2, gp2)
    self.assertNotEqual(gp1, gp2)
    self.assertNotEqual(gp1, None)
    self.assertNotEqual(gp2, [])
    self.assertNotEqual(gp1, 'gp2')


class FacetTest(TestCase):

  def testNumberFacetOutOfRange(self):
    valid_num = [0, -1, 1, -2147483647, 2147483647]
    invalid_num = [float('nan'), float('inf'), float('-inf'),
                   -2147483648, 2147483648]

    facet_request = search.FacetRequest('test', values=None)
    self.assertEqual(0, len(facet_request.values))
    self.assertRaises(
        TypeError, search.NumberFacet, name='test', value=None)
    self.assertRaises(ValueError, search.FacetRange, start=None, end=None)

    facet_request = search.FacetRequest('test', values='foo')
    self.assertEqual('foo', facet_request.values[0])
    self.assertRaises(
        TypeError, search.NumberFacet, name='test', value='foo')
    self.assertRaises(TypeError, search.FacetRange, start='foo')
    self.assertRaises(TypeError, search.FacetRange, end='foo')
    for num in valid_num:
      facet_request = search.FacetRequest('test', values=num)
      self.assertEqual(num, facet_request.values[0])
      facet = search.NumberFacet('test', num)
      self.assertEqual(num, facet.value)
      frange = search.FacetRange(start=num, end=num)
      self.assertEqual(num, frange.start)
      self.assertEqual(num, frange.end)
    for num in invalid_num:
      self.assertRaises(
          ValueError, search.FacetRequest, name='test', values=num)
      self.assertRaises(
          ValueError, search.NumberFacet, name='test', value=num)
      self.assertRaises(ValueError, search.FacetRange, start=num)
      self.assertRaises(ValueError, search.FacetRange, end=num)

    self.assertTrue(
        math.isnan(search.ScoredDocument(
            sort_scores=[float('nan')]).sort_scores[0]))
    self.assertTrue(
        math.isinf(search.ScoredDocument(
            sort_scores=[float('inf')]).sort_scores[0]))
    self.assertTrue(
        math.isinf(search.ScoredDocument(
            sort_scores=[float('-inf')]).sort_scores[0]))

  def testFacetValueType(self):
    facet_request = search.FacetRequest('test', values=[1, 1.0, 1234, 'test'])
    facet_request_pb = search_service_pb2.FacetRequest()
    facet_request._CopyToProtocolBuffer(facet_request_pb)
    for value in facet_request_pb.params.value_constraint:
      self.assertIsInstance(value, six.string_types)

  def testFieldWithoutAtomValue(self):
    facet = search.AtomField(name='name')
    self.assertEqual('name', facet.name)
    self.assertEqual(None, facet.value)

  def testFacetWithoutNumberValue(self):
    self.assertRaises(TypeError, search.NumberFacet, name='name')

  def testLegalName(self):
    for string in _LOWER_NON_VISIBLE_PRINTABLE_ASCII:
      self.assertRaises(ValueError, search.AtomFacet, name=string)
    self.assertRaises(
        ValueError, search.AtomFacet, name=_VISIBLE_PRINTABLE_ASCII)
    self.assertRaises(
        ValueError, search.AtomFacet, name=_VISIBLE_PRINTABLE_ASCII_UNICODE)
    self.assertRaises(ValueError, search.AtomFacet, name='!')
    for string in ['ABYZ', 'A09', 'A_Za_z0_9']:
      self.assertEqual(string, search.AtomFacet(name=string).name)
    self.assertRaises(ValueError, search.AtomFacet, name='_')
    self.assertRaises(ValueError, search.AtomFacet, name='0')
    self.assertRaises(ValueError, search.AtomFacet, name='0a')
    self.assertRaises(ValueError, search.AtomFacet, name='_RESERVEDNAME')
    self.assertRaises(ValueError, search.AtomFacet, name='_RESERVED_NAME')
    self.assertEqual('NOTRESERVED',
                      search.AtomFacet(name='NOTRESERVED').name)

  def testZeroValue(self):
    facet = search.NumberFacet(name='name', value=0)
    self.assertEqual('name', facet.name)
    self.assertEqual(0, facet.value)
    facet_value_pb = document_pb2.FacetValue()
    facet._CopyValueToProtocolBuffer(facet_value_pb)
    self.assertEqual(document_pb2.FacetValue.NUMBER, facet_value_pb.type)
    self.assertTrue(facet_value_pb.HasField('string_value'))
    self.assertEqual('0', facet_value_pb.string_value)

  def testNumberRanges(self):
    facet = search.NumberFacet(name='name', value=search.MAX_NUMBER_VALUE)
    self.assertEqual('name', facet.name)
    self.assertEqual(search.MAX_NUMBER_VALUE, facet.value)

    facet = search.NumberFacet(name='name', value=search.MIN_NUMBER_VALUE)
    self.assertEqual('name', facet.name)
    self.assertEqual(search.MIN_NUMBER_VALUE, facet.value)

    self.assertRaises(ValueError, search.NumberFacet, name='name',
                      value=search.MAX_NUMBER_VALUE + 1)
    self.assertRaises(ValueError, search.NumberFacet, name='name',
                      value=search.MIN_NUMBER_VALUE - 1)

  def testEmptyString(self):
    facet = search.AtomFacet(name='name', value='')
    self.assertEqual('name', facet.name)
    self.assertEqual('', facet.value)
    facet_value_pb = document_pb2.FacetValue()
    facet._CopyValueToProtocolBuffer(facet_value_pb)
    self.assertEqual(document_pb2.FacetValue.ATOM, facet_value_pb.type)
    self.assertTrue(facet_value_pb.HasField('string_value'))
    self.assertEqual('', facet_value_pb.string_value)

  def testValueUnicode(self):
    self.assertEqual(
        _UNICODE_STRING,
        search.AtomFacet(name='name', value=_UNICODE_STRING).value)

  def testUnicodeValuesOutput(self):
    facet = search.AtomFacet(name='atom', value='value')
    self.assertIsInstance(facet.name, six.text_type)
    self.assertIsInstance(facet.value, six.text_type)

  def testPositionalArgs(self):
    facet = search.AtomField('a_name', 'some-text')
    self.assertEqual('a_name', facet.name)
    self.assertEqual('some-text', facet.value)

  def testNumber(self):
    self.assertEqual(999,
                      search.NumberFacet(name='name', value=999).value)
    self.assertEqual(9.99,
                      search.NumberFacet(name='name', value=9.99).value)
    self.assertRaises(TypeError, search.NumberFacet, name='name',
                      value='number')
    self.assertRaises(ValueError, search.NumberFacet, name='name',
                      value=float('-inf'))
    self.assertRaises(ValueError, search.NumberFacet, name='name',
                      value=float('inf'))
    self.assertRaises(ValueError, search.NumberFacet, name='name',
                      value=float('nan'))

  def testWrongTypes(self):
    self.assertRaises(TypeError, search.AtomFacet, name=1)
    self.assertRaises(TypeError, search.AtomFacet, name='name', value=1)

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.AtomFacet, name='name', foo='bar')
    self.assertRaises(TypeError, search.NumberFacet, name='name', foo='bar')

  def testNameTooLong(self):
    name = 's' * search.MAXIMUM_FIELD_NAME_LENGTH
    self.assertEqual(name, search.AtomFacet(name=name).name)
    self.assertRaises(ValueError, search.AtomFacet, name=name + 's')

  def testNameWrongType(self):
    for value in _NON_STRING_VALUES:
      self.assertRaises(TypeError, search.AtomFacet, name=value)

  def testNameUnicode(self):
    self.assertRaises(ValueError, search.AtomFacet, name=_UNICODE_STRING)

  def testNameTooShort(self):
    self.assertRaises(ValueError, search.AtomFacet, name='')

  def testAtomShort(self):
    self.assertEqual(None, search.AtomFacet(name='name', value=None).value)
    self.assertEqual('', search.AtomFacet(name='name', value='').value)
    self.assertEqual(' ', search.AtomFacet(name='name', value=' ').value)

  def testAtomTooLong(self):
    value = 'v' * search.MAXIMUM_FIELD_ATOM_LENGTH
    self.assertEqual(value, search.AtomFacet(name='name',
                                              value=value).value)
    self.assertRaises(ValueError, search.AtomFacet, name='name',
                      value=value + 'v')

  def testTextWrongType(self):
    for value in _NON_STRING_VALUES:
      self.assertRaises(TypeError, search.AtomFacet, name='name',
                        value=value)

  def testNewFacetFromProtocolBuffer(self):
    facet_pb = document_pb2.Facet()
    facet_pb.name = 'subject'
    facet = search._NewFacetFromPb(facet_pb)
    self.assertEqual('subject', facet.name)
    self.assertIsInstance(facet.name, six.text_type)
    self.assertEqual(None, facet.value)

    facet_pb = document_pb2.Facet()
    facet_pb.name = 'subject'
    facet_value_pb = facet_pb.value
    facet_value_pb.string_value = ''
    facet = search._NewFacetFromPb(facet_pb)
    self.assertEqual('subject', facet.name)
    self.assertIsInstance(facet.name, six.text_type)
    self.assertEqual('', facet.value)

    facet_value_pb = facet_pb.value
    facet_value_pb.string_value = 'some good stuff'

    facet = search._NewFacetFromPb(facet_pb)
    self.assertEqual('subject', facet.name)
    self.assertEqual('some good stuff', facet.value)

    facet_value_pb.type = document_pb2.FacetValue.ATOM
    facet = search._NewFacetFromPb(facet_pb)
    self.assertIsInstance(facet, search.AtomFacet)
    self.assertEqual('some good stuff', facet.value)
    self.assertIsInstance(facet.value, six.text_type)

    facet_value_pb.string_value = _UNICODE_STRING.encode('utf-8')
    facet_value_pb.type = document_pb2.FacetValue.ATOM
    facet = search._NewFacetFromPb(facet_pb)
    self.assertEqual(_UNICODE_STRING, facet.value)

    facet_value_pb.type = document_pb2.FacetValue.NUMBER
    facet_value_pb.string_value = str(9.99)
    facet = search._NewFacetFromPb(facet_pb)
    self.assertEqual(9.99, facet.value)

    facet_pb = document_pb2.Facet()
    facet_pb.name = 'name'
    facet_pb.value.type = document_pb2.FacetValue.ATOM
    facet = search._NewFacetFromPb(facet_pb)
    self.assertIsInstance(facet, search.AtomFacet)
    self.assertEqual(None, facet.value)

    facet_pb = document_pb2.Facet()
    facet_value_pb = facet_pb.value
    facet_pb.name = 'name'
    facet_pb.value.type = document_pb2.FacetValue.NUMBER
    self.assertRaises(TypeError, search._NewFacetFromPb, facet_pb)

    facet_value_pb.type = document_pb2.FacetValue.ATOM
    facet_value_pb.string_value = 'x' * search.MAXIMUM_FIELD_ATOM_LENGTH
    self.assertEqual('x' * search.MAXIMUM_FIELD_ATOM_LENGTH,
                      search._NewFacetFromPb(facet_pb).value)
    facet_value_pb.string_value = 'x' * (search.MAXIMUM_FIELD_VALUE_LENGTH + 1)
    self.assertRaises(ValueError, search._NewFacetFromPb, facet_pb)

  def testCopyFacetToProtocolBuffer(self):
    facet_pb = document_pb2.Facet()
    search.AtomFacet(name='name')._CopyToProtocolBuffer(facet_pb)
    self.assertEqual('name', facet_pb.name)
    value = facet_pb.value
    self.assertEqual(document_pb2.FacetValue.ATOM, value.type)
    self.assertFalse(value.HasField('string_value'))

    facet_pb = document_pb2.Facet()
    search.AtomFacet(name='name', value='')._CopyToProtocolBuffer(facet_pb)
    self.assertEqual('name', facet_pb.name)
    value = facet_pb.value
    self.assertEqual(document_pb2.FacetValue.ATOM, value.type)
    self.assertTrue(value.HasField('string_value'))
    self.assertEqual('', value.string_value)

    facet_pb = document_pb2.Facet()
    search.AtomFacet(name='name', value='atom')._CopyToProtocolBuffer(facet_pb)
    self.assertEqual('atom', facet_pb.value.string_value)
    self.assertEqual(document_pb2.FacetValue.ATOM, facet_pb.value.type)

    facet_pb = document_pb2.Facet()
    search.NumberFacet(name='nmbr', value=0)._CopyToProtocolBuffer(facet_pb)
    self.assertEqual('0', facet_pb.value.string_value)
    self.assertEqual(document_pb2.FacetValue.NUMBER, facet_pb.value.type)

    facet_pb = document_pb2.Facet()
    search.NumberFacet(name='name', value=9.99)._CopyToProtocolBuffer(facet_pb)
    self.assertEqual(str(9.99), facet_pb.value.string_value)
    self.assertEqual(document_pb2.FacetValue.NUMBER, facet_pb.value.type)

    facet_pb = document_pb2.Facet()
    search.AtomFacet(
        name='name', value=_UNICODE_STRING)._CopyToProtocolBuffer(facet_pb)
    self.assertEqual(_UNICODE_STRING, facet_pb.value.string_value)
    self.assertEqual(document_pb2.FacetValue.ATOM, facet_pb.value.type)

  def testUnicodeInUnicodeOut(self):
    facet_pb = document_pb2.Facet()
    original_facet = search.AtomFacet(name='name', value=_UNICODE_STRING)
    self.assertEqual('name', original_facet.name)
    self.assertEqual(_UNICODE_STRING, original_facet.value)
    self.assertEqual(
        six.ensure_text(_UNICODE_AS_UTF8, 'utf-8'), original_facet.value)
    original_facet._CopyToProtocolBuffer(facet_pb)
    self.assertEqual(_UNICODE_STRING, facet_pb.value.string_value)
    self.assertEqual(document_pb2.FacetValue.ATOM, facet_pb.value.type)
    facet = search._NewFacetFromPb(facet_pb)
    self.assertEqual(original_facet.name, facet.name)
    self.assertEqual(original_facet.value, facet.value)

  def testRepr(self):
    self.assertReprEqual(
        "search.NumberFacet(name=u'facet_name', value=123)",
        repr(search.NumberFacet(name='facet_name', value=123)))
    self.assertReprEqual(
        "search.AtomFacet(name=u'facet_name', value=u'text')",
        repr(search.AtomFacet(name='facet_name', value='text')))
    self.assertReprEqual(
        "search.AtomFacet(name=u'facet_name', value=u'text')",
        repr(search.AtomFacet(name='facet_name', value='text')))
    self.assertReprEqual(
        "search.AtomFacet(name=u'name', value=u'Hofbr\\xe4uhaus')",
        repr(search.AtomFacet(name='name', value=u'Hofbr\xe4uhaus')))
    self.assertEqual(
        'search.FacetRange(start=1.0, end=2.0)',
        repr(search.FacetRange(start=1.0, end=2.0)))
    self.assertEqual(
        'search.FacetRange(start=1.0, end=2.0)',
        repr(search.FacetRange(start=1.0, end=2.0)))
    self.assertReprEqual(
        "search.FacetRequest(name=u'test', value_limit=10, values=[1, '2'])",
        repr(search.FacetRequest(name='test', values=[1, '2'])))
    self.assertReprEqual(
        "search.FacetRequest(name=u'test', value_limit=10, "
        "ranges=[search.FacetRange(start=1.0, end=2.0)])",
        repr(search.FacetRequest(
            name='test', ranges=search.FacetRange(start=1.0, end=2.0))))
    self.assertReprEqual(
        "search.FacetRefinement(name=u'test', value=12)",
        repr(search.FacetRefinement(name='test', value=12)))
    self.assertReprEqual(
        "search.FacetRefinement(name=u'test', "
        "facet_range=search.FacetRange(start=1.0, end=2.0))",
        repr(search.FacetRefinement(
            name='test', facet_range=search.FacetRange(start=1.0, end=2.0))))


class FieldTest(TestCase):

  def testRequiredArgumentsMissing(self):
    self.assertRaises(TypeError, search.TextField)
    self.assertRaises(TypeError, search.UntokenizedPrefixField, value='no name')
    self.assertRaises(TypeError, search.TokenizedPrefixField, value='no name')
    self.assertRaises(TypeError, search.TextField, value='no name')
    self.assertRaises(TypeError, search.HtmlField, value='no name')
    self.assertRaises(TypeError, search.HtmlField, value='no name',
                      language='en')
    self.assertRaises(TypeError, search.GeoField, value=_GEO_POINT)
    self.assertRaises(TypeError, search.VectorField, value=[1, 2, 3])

  def testFieldWithoutTextValue(self):
    field = search.TextField(name='name')
    self.assertEqual('name', field.name)
    self.assertEqual(None, field.value)

  def testFieldWithoutHtmlValue(self):
    field = search.HtmlField(name='name')
    self.assertEqual('name', field.name)
    self.assertEqual(None, field.value)

  def testFieldWithoutAtomValue(self):
    field = search.AtomField(name='name')
    self.assertEqual('name', field.name)
    self.assertEqual(None, field.value)

  def testFieldWithoutVectorValue(self):
    field = search.VectorField(name='name')
    self.assertEqual('name', field.name)
    self.assertEqual([], field.value)

  def testFieldWithoutUntokenizedPrefixValue(self):
    field = search.UntokenizedPrefixField(name='name')
    self.assertEqual('name', field.name)
    self.assertEqual(None, field.value)

  def testFieldWithoutTokenizedPrefixValue(self):
    field = search.TokenizedPrefixField(name='name')
    self.assertEqual('name', field.name)
    self.assertEqual(None, field.value)

  def testFieldWithoutDateValue(self):
    self.assertRaises(TypeError, search.DateField, name='name')

  def testFieldWithoutNumberValue(self):
    self.assertRaises(TypeError, search.NumberField, name='name')

  def testFieldithoutGeoValue(self):
    self.assertRaises(TypeError, search.GeoField, name='name')

  def testLegalName(self):
    for string in _LOWER_NON_VISIBLE_PRINTABLE_ASCII:
      self.assertRaises(ValueError, search.TextField, name=string)
    self.assertRaises(
        ValueError, search.TextField, name=_VISIBLE_PRINTABLE_ASCII)
    self.assertRaises(
        ValueError, search.TextField, name=_VISIBLE_PRINTABLE_ASCII_UNICODE)
    self.assertRaises(ValueError, search.TextField, name='!')
    for string in ['ABYZ', 'A09', 'A_Za_z0_9']:
      self.assertEqual(string, search.TextField(name=string).name)
    self.assertRaises(ValueError, search.TextField, name='_')
    self.assertRaises(ValueError, search.TextField, name='0')
    self.assertRaises(ValueError, search.TextField, name='0a')
    self.assertRaises(ValueError, search.TextField, name='_RESERVEDNAME')
    self.assertRaises(ValueError, search.TextField, name='_RESERVED_NAME')
    self.assertEqual('NOTRESERVED',
                      search.TextField(name='NOTRESERVED').name)

  def testSimpleValue(self):
    field = search.TextField(name='name')
    self.assertEqual('name', field.name)
    self.assertEqual(None, field.value)

  def testZeroValue(self):
    field = search.NumberField(name='name', value=0)
    self.assertEqual('name', field.name)
    self.assertEqual(0, field.value)
    field_value_pb = document_pb2.FieldValue()
    field._CopyValueToProtocolBuffer(field_value_pb)
    self.assertEqual(document_pb2.FieldValue.NUMBER, field_value_pb.type)
    self.assertTrue(field_value_pb.HasField('string_value'))
    self.assertEqual('0', field_value_pb.string_value)

  def testNumberRanges(self):
    field = search.NumberField(name='name', value=search.MAX_NUMBER_VALUE)
    self.assertEqual('name', field.name)
    self.assertEqual(search.MAX_NUMBER_VALUE, field.value)

    field = search.NumberField(name='name', value=search.MIN_NUMBER_VALUE)
    self.assertEqual('name', field.name)
    self.assertEqual(search.MIN_NUMBER_VALUE, field.value)

    self.assertRaises(ValueError, search.NumberField, name='name',
                      value=search.MAX_NUMBER_VALUE + 1)
    self.assertRaises(ValueError, search.NumberField, name='name',
                      value=search.MIN_NUMBER_VALUE - 1)

  def testEmptyString(self):
    field = search.TextField(name='name', value='')
    self.assertEqual('name', field.name)
    self.assertEqual('', field.value)
    field_value_pb = document_pb2.FieldValue()
    field._CopyValueToProtocolBuffer(field_value_pb)
    self.assertEqual(document_pb2.FieldValue.TEXT, field_value_pb.type)
    self.assertTrue(field_value_pb.HasField('string_value'))
    self.assertEqual('', field_value_pb.string_value)

  def testValueUnicode(self):
    self.assertEqual(
        _UNICODE_STRING,
        search.TextField(name='name', value=_UNICODE_STRING).value)
    self.assertEqual(
        _UNICODE_STRING,
        search.HtmlField(name='name', value=_UNICODE_STRING).value)
    self.assertEqual(
        _UNICODE_STRING,
        search.AtomField(name='name', value=_UNICODE_STRING).value)
    self.assertEqual(
        _UNICODE_STRING,
        search.UntokenizedPrefixField(name='name', value=_UNICODE_STRING).value)
    self.assertEqual(
        _UNICODE_STRING,
        search.TokenizedPrefixField(name='name', value=_UNICODE_STRING).value)

  def testUnicodeValuesOutput(self):
    field = search.TextField(name='text', value='value', language='en')
    self.assertIsInstance(field.name, six.text_type)
    self.assertIsInstance(field.value, six.text_type)
    self.assertIsInstance(field.language, six.text_type)
    field = search.HtmlField(name='html', value='value', language='en')
    self.assertIsInstance(field.name, six.text_type)
    self.assertIsInstance(field.value, six.text_type)
    self.assertIsInstance(field.language, six.text_type)
    field = search.AtomField(name='atom', value='value', language='en')
    self.assertIsInstance(field.name, six.text_type)
    self.assertIsInstance(field.value, six.text_type)
    self.assertIsInstance(field.language, six.text_type)
    field = search.UntokenizedPrefixField(name='uprefix',
                                          value='value', language='en')
    self.assertIsInstance(field.name, six.text_type)
    self.assertIsInstance(field.value, six.text_type)
    self.assertIsInstance(field.language, six.text_type)
    field = search.TokenizedPrefixField(name='tprefix',
                                        value='value', language='en')
    self.assertIsInstance(field.name, six.text_type)
    self.assertIsInstance(field.value, six.text_type)
    self.assertIsInstance(field.language, six.text_type)

  def testFullySpecified(self):
    field = search.TextField(name='name', value='text', language='pl')
    self.assertEqual('name', field.name)
    self.assertEqual('text', field.value)
    self.assertEqual('pl', field.language)

  def testPositionalArgs(self):
    field = search.TextField('a_name', 'some-text', 'pl')
    self.assertEqual('a_name', field.name)
    self.assertEqual('some-text', field.value)
    self.assertEqual('pl', field.language)
    field = search.UntokenizedPrefixField('a_name', 'some-text', 'pl')
    self.assertEqual('a_name', field.name)
    self.assertEqual('some-text', field.value)
    self.assertEqual('pl', field.language)
    field = search.TokenizedPrefixField('a_name', 'some-text', 'pl')
    self.assertEqual('a_name', field.name)
    self.assertEqual('some-text', field.value)
    self.assertEqual('pl', field.language)

  def testDate(self):
    self.assertEqual(_DATE,
                      search.DateField(name='name', value=_DATE).value)
    self.assertEqual(_DATE_TIME,
                      search.DateField(name='name', value=_DATE_TIME).value)
    self.assertRaises(TypeError, search.DateField, name='name',
                      value='date')

  def testNumber(self):
    self.assertEqual(999,
                      search.NumberField(name='name', value=999).value)
    self.assertEqual(9.99,
                      search.NumberField(name='name', value=9.99).value)
    self.assertRaises(TypeError, search.NumberField, name='name',
                      value='number')

  def testGeoPoint(self):
    self.assertEqual(_GEO_POINT,
                      search.GeoField(name='name', value=_GEO_POINT).value)

  def testWrongTypes(self):
    self.assertRaises(TypeError, search.TextField, name=1)
    self.assertRaises(TypeError, search.TextField, name='name', value=1)
    self.assertRaises(TypeError, search.TextField, name='name', language=1)
    self.assertRaises(TypeError, search.GeoField, name='geo', value=(0, 0))
    self.assertRaises(TypeError, search.UntokenizedPrefixField, name='name',
                      value=1)
    self.assertRaises(TypeError, search.TokenizedPrefixField, name='name',
                      value=1)
    self.assertRaises(TypeError, search.VectorField, name='name', value='v')

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.TextField, name='name', foo='bar')
    self.assertRaises(TypeError, search.HtmlField, name='name', foo='bar')
    self.assertRaises(TypeError, search.AtomField, name='name', foo='bar')
    self.assertRaises(TypeError, search.UntokenizedPrefixField, name='name',
                      foo='bar')
    self.assertRaises(TypeError, search.TokenizedPrefixField, name='name',
                      foo='bar')
    self.assertRaises(TypeError, search.DateField, name='name', foo='bar')
    self.assertRaises(TypeError, search.NumberField, name='name', foo='bar')

  def testNameTooLong(self):
    name = 's' * search.MAXIMUM_FIELD_NAME_LENGTH
    self.assertEqual(name, search.TextField(name=name).name)
    self.assertRaises(ValueError, search.TextField, name=name + 's')

  def testNameWrongType(self):
    for value in _NON_STRING_VALUES:
      self.assertRaises(TypeError, search.TextField, name=value)

  def testNameUnicode(self):
    self.assertRaises(ValueError, search.TextField, name=_UNICODE_STRING)

  def testNameTooShort(self):
    self.assertRaises(ValueError, search.TextField, name='')

  def testTextShort(self):
    self.assertEqual(None, search.TextField(name='name', value=None).value)
    self.assertEqual('', search.TextField(name='name', value='').value)
    self.assertEqual(' ', search.TextField(name='name', value=' ').value)

  def testUntokenizedPrefixShort(self):
    self.assertEqual(None, search.UntokenizedPrefixField(name='name',
                                                          value=None).value)
    self.assertEqual('', search.UntokenizedPrefixField(name='name',
                                                        value='').value)
    self.assertEqual(' ', search.UntokenizedPrefixField(name='name',
                                                         value=' ').value)

  def testTokenizedPrefixShort(self):
    self.assertEqual(None, search.TokenizedPrefixField(name='name',
                                                        value=None).value)
    self.assertEqual('', search.TokenizedPrefixField(name='name',
                                                      value='').value)
    self.assertEqual(' ', search.TokenizedPrefixField(name='name',
                                                       value=' ').value)

  def testTextTooLong(self):
    value = 'v' * search.MAXIMUM_FIELD_VALUE_LENGTH
    self.assertEqual(value, search.TextField(name='name',
                                              value=value).value)
    self.assertRaises(ValueError, search.TextField, name='name',
                      value=value + 'v')

  def testHtmlTooLong(self):
    value = 'v' * search.MAXIMUM_FIELD_VALUE_LENGTH
    self.assertEqual(value, search.HtmlField(name='name',
                                              value=value).value)
    self.assertRaises(ValueError, search.HtmlField, name='name',
                      value=value + 'v')

  def testAtomTooLong(self):
    value = 'v' * search.MAXIMUM_FIELD_ATOM_LENGTH
    self.assertEqual(value, search.AtomField(name='name',
                                              value=value).value)
    self.assertRaises(ValueError, search.AtomField, name='name',
                      value=value + 'v')

  def testVectorFieldInvalidNumber(self):
    self.assertRaises(ValueError, search.VectorField, name='name',
                      value=[float('inf')])
    self.assertRaises(ValueError, search.VectorField, name='name',
                      value=[float('nan')])

  def testVectorFieldLongVector(self):
    value = list(range(search.VECTOR_FIELD_MAX_SIZE))
    self.assertEqual(value, search.VectorField(name='name', value=value).value)
    self.assertRaises(ValueError, search.VectorField, name='name',
                      value=value + [0])

  def testUntokenizedPrefixTooLong(self):
    value = 'u' * search.MAXIMUM_FIELD_PREFIX_LENGTH
    self.assertEqual(value, search.UntokenizedPrefixField(name='name',
                                                           value=value).value)
    self.assertRaises(ValueError, search.UntokenizedPrefixField, name='name',
                      value=value + 'v')

  def testTokenizedPrefixTooLong(self):
    value = 't' * search.MAXIMUM_FIELD_PREFIX_LENGTH
    self.assertEqual(value, search.TokenizedPrefixField(name='name',
                                                         value=value).value)
    self.assertRaises(ValueError, search.TokenizedPrefixField, name='name',
                      value=value + 't')

  def testTextWrongType(self):
    for value in _NON_STRING_VALUES:
      self.assertRaises(TypeError, search.TextField, name='name',
                        value=value)

  def testUntokenizedPrefixWrongType(self):
    for value in _NON_STRING_VALUES:
      self.assertRaises(TypeError, search.UntokenizedPrefixField, name='name',
                        value=value)

  def testTokenizedPrefixWrongType(self):
    for value in _NON_STRING_VALUES:
      self.assertRaises(TypeError, search.TokenizedPrefixField, name='name',
                        value=value)

  def testLanguage(self):
    self.assertEqual('en',
                      search.TextField(name='name', language='en').language)
    self.assertEqual(None, search.TextField(name='name',
                                             language=None).language)
    self.assertEqual('kab',
                     search.TextField(name='name', language='kab').language)
    for value in _ILLEGAL_LANGUAGE_CODES:
      self.assertRaises(ValueError, search.TextField, name='name',
                        language=value)

  def testNewFieldFromProtocolBuffer(self):
    field_pb = document_pb2.Field()
    field_pb.name = 'subject'
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual('subject', field.name)
    self.assertIsInstance(field.name, six.text_type)
    self.assertEqual(None, field.value)

    field_pb = document_pb2.Field()
    field_pb.name = 'subject'
    field_value_pb = field_pb.value
    field_value_pb.string_value = ''
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual('subject', field.name)
    self.assertIsInstance(field.name, six.text_type)
    self.assertEqual('', field.value)

    field_value_pb = field_pb.value
    field_value_pb.string_value = 'some good stuff'

    field = search._NewFieldFromPb(field_pb)
    self.assertEqual('subject', field.name)
    self.assertEqual('some good stuff', field.value)

    field_value_pb.type = document_pb2.FieldValue.TEXT
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.TextField)
    self.assertEqual('some good stuff', field.value)
    self.assertIsInstance(field.value, six.text_type)

    field_value_pb.type = document_pb2.FieldValue.HTML
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.HtmlField)
    self.assertEqual('some good stuff', field.value)
    self.assertIsInstance(field.value, six.text_type)

    field_value_pb.type = document_pb2.FieldValue.ATOM
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.AtomField)
    self.assertEqual('some good stuff', field.value)
    self.assertIsInstance(field.value, six.text_type)

    field_value_pb.type = document_pb2.FieldValue.UNTOKENIZED_PREFIX
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.UntokenizedPrefixField)
    self.assertEqual('some good stuff', field.value)
    self.assertIsInstance(field.value, six.text_type)

    field_value_pb.type = document_pb2.FieldValue.TOKENIZED_PREFIX
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.TokenizedPrefixField)
    self.assertEqual('some good stuff', field.value)
    self.assertIsInstance(field.value, six.text_type)

    field_value_pb.string_value = _UNICODE_STRING.encode('utf-8')
    field_value_pb.type = document_pb2.FieldValue.TEXT
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual(_UNICODE_STRING, field.value)
    self.assertIsInstance(field.value, six.text_type)

    field_value_pb.string_value = _UNICODE_STRING.encode('utf-8')
    field_value_pb.type = document_pb2.FieldValue.HTML
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual(_UNICODE_STRING, field.value)

    field_value_pb.string_value = _UNICODE_STRING.encode('utf-8')
    field_value_pb.type = document_pb2.FieldValue.ATOM
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual(_UNICODE_STRING, field.value)

    field_value_pb.string_value = _UNICODE_STRING.encode('utf-8')
    field_value_pb.type = document_pb2.FieldValue.UNTOKENIZED_PREFIX
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.UntokenizedPrefixField)
    self.assertEqual(_UNICODE_STRING, field.value)

    field_value_pb.string_value = _UNICODE_STRING.encode('utf-8')
    field_value_pb.type = document_pb2.FieldValue.TOKENIZED_PREFIX
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.TokenizedPrefixField)
    self.assertEqual(_UNICODE_STRING, field.value)

    field_value_pb.type = document_pb2.FieldValue.NUMBER
    field_value_pb.string_value = str(9.99)
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual(9.99, field.value)

    field_value_pb.type = document_pb2.FieldValue.GEO
    geo_pb = field_value_pb.geo
    geo_pb.lat = _GEO_POINT.latitude
    geo_pb.lng = _GEO_POINT.longitude
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.GeoField)
    self.assertEqual(_GEO_POINT.latitude, field.value.latitude)
    self.assertEqual(_GEO_POINT.longitude, field.value.longitude)

    field_value_pb.type = document_pb2.FieldValue.VECTOR
    field_value_pb.vector_value.append(1.0)
    field_value_pb.vector_value.append(2.0)
    field_value_pb.vector_value.append(3.0)
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.VectorField)
    self.assertEqual([1.0, 2.0, 3.0], field.value)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_pb.value.type = document_pb2.FieldValue.TEXT
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.TextField)
    self.assertEqual(None, field.value)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_pb.value.type = document_pb2.FieldValue.HTML
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.HtmlField)
    self.assertEqual(None, field.value)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_pb.value.type = document_pb2.FieldValue.ATOM
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.AtomField)
    self.assertEqual(None, field.value)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_pb.value.type = document_pb2.FieldValue.UNTOKENIZED_PREFIX
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.UntokenizedPrefixField)
    self.assertEqual(None, field.value)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_pb.value.type = document_pb2.FieldValue.TOKENIZED_PREFIX
    field = search._NewFieldFromPb(field_pb)
    self.assertIsInstance(field, search.TokenizedPrefixField)
    self.assertEqual(None, field.value)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_pb.value.type = document_pb2.FieldValue.GEO
    self.assertRaises(TypeError, search._NewFieldFromPb, field_pb)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_pb.value.type = document_pb2.FieldValue.NUMBER
    self.assertRaises(TypeError, search._NewFieldFromPb, field_pb)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_pb.value.type = document_pb2.FieldValue.DATE
    self.assertRaises(TypeError, search._NewFieldFromPb, field_pb)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_value_pb = field_pb.value
    field_value_pb.type = document_pb2.FieldValue.DATE
    field_value_pb.string_value = _DATE_STRING
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual(_DATE, field.value.date())

    field_value_pb.string_value = _DATE_TIME_STRING
    self.assertRaises(ValueError, search._NewFieldFromPb, field_pb)
    field_value_pb.type = document_pb2.FieldValue.TEXT
    field_value_pb.language = 'pl'
    self.assertEqual('pl', search._NewFieldFromPb(field_pb).language)
    field_value_pb.language = 'kab'
    self.assertEqual('kab', search._NewFieldFromPb(field_pb).language)
    field_value_pb.language = 'burt'
    self.assertRaises(ValueError, search._NewFieldFromPb, field_pb)
    field_value_pb.ClearField('language')
    field_value_pb.string_value = 'x' * search.MAXIMUM_FIELD_VALUE_LENGTH
    self.assertEqual('x' * search.MAXIMUM_FIELD_VALUE_LENGTH,
                      search._NewFieldFromPb(field_pb).value)
    field_value_pb.string_value = 'x' * (search.MAXIMUM_FIELD_VALUE_LENGTH + 1)
    self.assertRaises(ValueError, search._NewFieldFromPb, field_pb)

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_value_pb = field_pb.value
    field_value_pb.type = document_pb2.FieldValue.DATE
    field_value_pb.string_value = _DATE_LONG_STRING
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual(_DATE, field.value.date())

    field_pb = document_pb2.Field()
    field_pb.name = 'name'
    field_value_pb = field_pb.value
    field_value_pb.type = document_pb2.FieldValue.DATE
    field_value_pb.string_value = _DATE_TIME_LONG_STRING
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual(_DATE_TIME, field.value)

  def testCopyFieldToProtocolBuffer(self):
    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.TextField(name='name', language='pl'), field_pb)
    self.assertEqual('name', field_pb.name)
    value = field_pb.value
    self.assertEqual(document_pb2.FieldValue.TEXT, value.type)
    self.assertFalse(value.HasField('string_value'))
    self.assertEqual('pl', value.language)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.TextField(name='name', value='', language='pl'), field_pb)
    self.assertEqual('name', field_pb.name)
    value = field_pb.value
    self.assertEqual(document_pb2.FieldValue.TEXT, value.type)
    self.assertTrue(value.HasField('string_value'))
    self.assertEqual('', value.string_value)
    self.assertEqual('pl', value.language)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.TextField(name='name', value='text'), field_pb)
    self.assertEqual('text', field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.TEXT, field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.HtmlField(name='name', value='<html>'), field_pb)
    self.assertEqual('<html>', field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.HTML, field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.AtomField(name='name', value='atom'), field_pb)
    self.assertEqual('atom', field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.ATOM, field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.UntokenizedPrefixField(name='name', value='uprefix'), field_pb)
    self.assertEqual('uprefix', field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.UNTOKENIZED_PREFIX,
                      field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.TokenizedPrefixField(name='name', value='tprefix'), field_pb)
    self.assertEqual('tprefix', field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.TOKENIZED_PREFIX,
                      field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.DateField(name='name', value=_DATE), field_pb)
    self.assertEqual(_DATE_LONG_STRING, field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.DATE, field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.NumberField(name='nmbr', value=0), field_pb)
    self.assertEqual('0', field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.NUMBER, field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.NumberField(name='name', value=9.99), field_pb)
    self.assertEqual(str(9.99), field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.NUMBER, field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.GeoField(name='name', value=_GEO_POINT), field_pb)
    self.assertEqual('name', field_pb.name)
    self.assertEqual(document_pb2.FieldValue.GEO, field_pb.value.type)
    geo_pb = field_pb.value.geo
    self.assertEqual(_GEO_POINT.latitude, geo_pb.lat)
    self.assertEqual(_GEO_POINT.longitude, geo_pb.lng)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.VectorField(name='name', value=[1.0, 2.0, 3.0]), field_pb)
    self.assertEqual('name', field_pb.name)
    self.assertEqual(document_pb2.FieldValue.VECTOR, field_pb.value.type)
    self.assertEqual([1.0, 2.0, 3.0], field_pb.value.vector_value)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.TextField(name='name', value=_UNICODE_STRING), field_pb)
    self.assertEqual(_UNICODE_STRING, field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.TEXT, field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(

        search.TextField(name='name', value='text', language='00'), field_pb)
    self.assertEqual('text', field_pb.value.string_value)
    self.assertEqual('00', field_pb.value.language)
    self.assertEqual(document_pb2.FieldValue.TEXT, field_pb.value.type)

    search._CopyFieldToProtocolBuffer(
        search.HtmlField(name='name', value=_UNICODE_STRING), field_pb)
    self.assertEqual(_UNICODE_STRING, field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.HTML, field_pb.value.type)

    field_pb = document_pb2.Field()
    search._CopyFieldToProtocolBuffer(
        search.AtomField(name='name', value=_UNICODE_STRING), field_pb)
    self.assertEqual(_UNICODE_STRING, field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.ATOM, field_pb.value.type)

    search._CopyFieldToProtocolBuffer(
        search.UntokenizedPrefixField(name='name', value=_UNICODE_STRING),
        field_pb)
    self.assertEqual(_UNICODE_STRING, field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.UNTOKENIZED_PREFIX,
                      field_pb.value.type)

    search._CopyFieldToProtocolBuffer(
        search.TokenizedPrefixField(name='name', value=_UNICODE_STRING),
        field_pb)
    self.assertEqual(_UNICODE_STRING, field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.TOKENIZED_PREFIX,
                      field_pb.value.type)

    unicode_str = u'won\u2019t'
    search._CopyFieldToProtocolBuffer(
        search.HtmlField(name='name', value=unicode_str), field_pb)
    self.assertEqual(unicode_str, field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.HTML, field_pb.value.type)

  def testUnicodeInUnicodeOut(self):
    field_pb = document_pb2.Field()
    original_field = search.TextField(name='name', value=_UNICODE_STRING)
    self.assertEqual('name', original_field.name)
    self.assertEqual(_UNICODE_STRING, original_field.value)
    self.assertEqual(
        six.ensure_text(_UNICODE_AS_UTF8, 'utf-8'), original_field.value)
    search._CopyFieldToProtocolBuffer(original_field, field_pb)
    self.assertEqual(_UNICODE_STRING, field_pb.value.string_value)
    self.assertEqual(document_pb2.FieldValue.TEXT, field_pb.value.type)
    field = search._NewFieldFromPb(field_pb)
    self.assertEqual(original_field.name, field.name)
    self.assertEqual(original_field.value, field.value)
    self.assertEqual(original_field.language, field.language)

  def testRepr(self):

    self.assertReprEqual(
        "search.TextField(name=u'field_name', language=u'pl', value=u'text')",
        repr(search.TextField(name='field_name', language='pl', value='text')))
    self.assertReprEqual(
        "search.TextField(name=u'field_name', language=u'pl', value=u'text')",
        str(search.TextField(name='field_name', language='pl', value='text')))
    self.assertReprEqual(
        "search.TextField(name=u'name', language=u'de', "
        "value=u'Hofbr\\xe4uhaus')",
        repr(search.TextField(name='name', language='de',
                              value=u'Hofbr\xe4uhaus')))
    self.assertReprEqual(
        "search.VectorField(name=u'field_name', value=[1.0, 2.0, 3.0])",
        str(search.VectorField(name='field_name', value=[1.0, 2.0, 3.0])))
    self.assertReprEqual(
        "search.GeoField(name=u'field_name', "
        "value=search.GeoPoint(latitude=%r, longitude=%r))" % (-33.84, 151.26),
        str(search.GeoField(name='field_name', value=_GEO_POINT)))
    self.assertReprEqual(
        "search.UntokenizedPrefixField(name=u'field_name', language=u'pl', "
        "value=u'text')",
        repr(search.UntokenizedPrefixField(name='field_name', language='pl',
                                           value='text')))
    self.assertReprEqual(
        "search.TokenizedPrefixField(name=u'field_name', language=u'pl', "
        "value=u'text')",
        repr(search.TokenizedPrefixField(name='field_name', language='pl',
                                         value='text')))


class DocumentTest(TestCase):

  DEFAULT_FIELD = search.TextField(name='subject', value='some good news')
  DEFAULT_FACET = search.AtomFacet(name='kind', value='some_good_kind')

  def testDocId(self):
    self.assertEqual(None, search.Document().doc_id)
    self.assertRaises(ValueError, search.Document, doc_id='')
    self.assertEqual('id', search.Document(doc_id='id').doc_id)
    self.assertRaises(ValueError, search.Document, doc_id='document id')
    self.assertEqual('document_id',
                      search.Document(doc_id='document_id').doc_id)

  def testMinimalDocument(self):
    doc = search.Document()
    self.assertEqual(None, doc.doc_id)
    self.assertTrue(doc.rank)
    self.assertEqual('en', doc.language)

  def testSimpleDocPositionalArgs(self):
    doc = search.Document('an-id', [self.DEFAULT_FIELD])
    self.assertEqual('an-id', doc.doc_id)
    self.assertEqual([self.DEFAULT_FIELD], doc.fields)
    self.assertTrue(doc.rank)
    self.assertEqual('en', doc.language)

  def testUnicodeOutput(self):
    doc = search.Document(doc_id='doc_id', language='en')
    self.assertIsInstance(doc.doc_id, six.text_type)
    self.assertIsInstance(doc.language, six.text_type)

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.Document, foo='bar')

  def testWrongTypes(self):
    self.assertRaises(TypeError, search.Document, doc_id=1)
    self.assertRaises(TypeError, search.Document, fields=self.DEFAULT_FIELD)
    self.assertRaises(TypeError, search.Document, facets=self.DEFAULT_FACET)
    self.assertRaises(TypeError, search.Document, language=1)
    self.assertRaises(ValueError, search.Document, rank='abc')

  def testInvalidId(self):
    for string in _LOWER_NON_VISIBLE_PRINTABLE_ASCII:
      self.assertRaises(ValueError, search.Document, doc_id=string)
    self.assertEqual(_VISIBLE_PRINTABLE_ASCII,
                      search.Document(doc_id=_VISIBLE_PRINTABLE_ASCII).doc_id)
    self.assertEqual(_VISIBLE_PRINTABLE_ASCII_UNICODE,
                      search.Document(
                          doc_id=_VISIBLE_PRINTABLE_ASCII_UNICODE).doc_id)
    self.assertRaises(ValueError, search.Document, doc_id='!')
    for string in _UPPER_NON_VISIBLE_PRINTABLE_ASCII:
      self.assertRaises(ValueError, search.Document, doc_id=string)
    ok = 'x' * search.MAXIMUM_DOCUMENT_ID_LENGTH
    self.assertEqual(ok, search.Document(doc_id=ok).doc_id)
    self.assertRaises(ValueError, search.Document, doc_id=ok + 'x')
    for value in _NON_STRING_VALUES:
      self.assertRaises(TypeError, search.Document, doc_id=value)

  def testIdUnicode(self):
    self.assertEqual(u'id', search.Document(doc_id=u'id').doc_id)
    self.assertRaises(ValueError, search.Document, doc_id=u'!~')

  def testLanguage(self):
    self.assertEqual('pl', search.Document(language='pl').language)
    self.assertEqual('en_US', search.Document(language='en_US').language)
    self.assertEqual('kab', search.Document(language='kab').language)

    for value in _ILLEGAL_LANGUAGE_CODES:
      self.assertRaises(ValueError, search.Document, language=value)

  def testRank(self):
    rank = search.Document().rank
    self.assertTrue(isinstance(rank, int) and rank > 0)
    self.assertRaises(ValueError, search.Document, rank=-1)
    self.assertEqual(0, search.Document(rank=0).rank)
    self.assertEqual(sys.maxsize, search.Document(rank=sys.maxsize).rank)

  def testCopyDocumentToProtocolBuffer(self):
    doc_pb = document_pb2.Document()
    search._CopyDocumentToProtocolBuffer(
        search.Document(doc_id='id', fields=[self.DEFAULT_FIELD],
                        language='pl', rank=999,
                        facets=[self.DEFAULT_FACET]), doc_pb)
    self.assertEqual('id', doc_pb.id)
    self.assertEqual('pl', doc_pb.language)
    self.assertEqual(1, len(doc_pb.field))
    self.assertEqual(1, len(doc_pb.facet))
    field_pb = doc_pb.field[0]
    self.assertEqual(self.DEFAULT_FIELD.name, field_pb.name)
    field_value_pb = field_pb.value
    self.assertEqual(self.DEFAULT_FIELD.value, field_value_pb.string_value)
    self.assertEqual(document_pb2.FieldValue.TEXT, field_value_pb.type)
    facet_pb = doc_pb.facet[0]
    self.assertEqual(self.DEFAULT_FACET.name, facet_pb.name)
    facet_value_pb = facet_pb.value
    self.assertEqual(self.DEFAULT_FACET.value, facet_value_pb.string_value)
    self.assertEqual(document_pb2.FacetValue.ATOM, facet_value_pb.type)
    self.assertEqual(999, doc_pb.order_id)
    self.assertEqual(document_pb2.Document.SUPPLIED, doc_pb.order_id_source)

    doc_pb = document_pb2.Document()
    search._CopyDocumentToProtocolBuffer(search.Document(), doc_pb)
    self.assertFalse(doc_pb.HasField('id'))

    doc_pb = document_pb2.Document()
    search._CopyDocumentToProtocolBuffer(search.Document(doc_id='0'), doc_pb)
    self.assertEqual('0', doc_pb.id)

  def testCopyDocumentToProtocolBufferWithDefaultedRank(self):
    doc_pb = document_pb2.Document()
    search._CopyDocumentToProtocolBuffer(
        search.Document(doc_id='id', fields=[self.DEFAULT_FIELD],
                        language='pl', rank=None,
                        facets=[self.DEFAULT_FACET]), doc_pb)
    self.assertEqual(document_pb2.Document.DEFAULTED, doc_pb.order_id_source)

  def testCopyToProtocolBufferZeroValue(self):
    doc_pb = document_pb2.Document()
    document = search.Document(
        fields=[search.TextField(name='author', value='nickname'),
                search.HtmlField(name='comment', value='content'),
                search.NumberField(name='nmbr', value=0),
                search.DateField(name='date', value=_DATE),
                search.GeoField(name='geo', value=_GEO_POINT),
                search.UntokenizedPrefixField(name='uprefix', value='up'),
                search.TokenizedPrefixField(name='tprefix', value='tp'),
                search.VectorField(name='vector', value=[0])],
        facets=[search.AtomFacet(name='type', value='typename'),
                search.NumberFacet(name='number', value=0)])
    search._CopyDocumentToProtocolBuffer(document, doc_pb)
    self.assertFalse(doc_pb.HasField('id'))
    self.assertEqual('en', doc_pb.language)
    self.assertLen(doc_pb.field, 8)
    self.assertLen(doc_pb.facet, 2)

    field_pb = doc_pb.field[0]
    self.assertEqual('author', field_pb.name)
    field_value_pb = field_pb.value
    self.assertEqual('nickname', field_value_pb.string_value)
    self.assertEqual(document_pb2.FieldValue.TEXT, field_value_pb.type)

    field_pb = doc_pb.field[1]
    self.assertEqual('comment', field_pb.name)
    field_value_pb = field_pb.value
    self.assertEqual('content', field_value_pb.string_value)
    self.assertEqual(document_pb2.FieldValue.HTML, field_value_pb.type)

    field_pb = doc_pb.field[2]
    self.assertEqual('nmbr', field_pb.name)
    field_value_pb = field_pb.value
    self.assertEqual('0', field_value_pb.string_value)
    self.assertEqual(document_pb2.FieldValue.NUMBER, field_value_pb.type)

    field_pb = doc_pb.field[3]
    self.assertEqual('date', field_pb.name)
    field_value_pb = field_pb.value
    self.assertEqual(_DATE_LONG_STRING, field_value_pb.string_value)
    self.assertEqual(document_pb2.FieldValue.DATE, field_value_pb.type)

    field_pb = doc_pb.field[4]
    self.assertEqual('geo', field_pb.name)
    field_value_pb = field_pb.value
    self.assertEqual(document_pb2.FieldValue.GEO, field_value_pb.type)
    geo_pb = field_value_pb.geo
    self.assertEqual(_GEO_POINT.latitude, geo_pb.lat)
    self.assertEqual(_GEO_POINT.longitude, geo_pb.lng)

    field_pb = doc_pb.field[5]
    self.assertEqual('uprefix', field_pb.name)
    field_value_pb = field_pb.value
    self.assertEqual('up', field_value_pb.string_value)
    self.assertEqual(document_pb2.FieldValue.UNTOKENIZED_PREFIX,
                      field_value_pb.type)

    field_pb = doc_pb.field[6]
    self.assertEqual('tprefix', field_pb.name)
    field_value_pb = field_pb.value
    self.assertEqual('tp', field_value_pb.string_value)
    self.assertEqual(document_pb2.FieldValue.TOKENIZED_PREFIX,
                      field_value_pb.type)

    field_pb = doc_pb.field[7]
    self.assertEqual('vector', field_pb.name)
    field_value_pb = field_pb.value
    self.assertEqual([0], field_value_pb.vector_value)
    self.assertEqual(document_pb2.FieldValue.VECTOR, field_value_pb.type)

    facet_pb = doc_pb.facet[0]
    self.assertEqual('type', facet_pb.name)
    facet_value_pb = facet_pb.value
    self.assertEqual('typename', facet_value_pb.string_value)
    self.assertEqual(document_pb2.FacetValue.ATOM, facet_value_pb.type)

    facet_pb = doc_pb.facet[1]
    self.assertEqual('number', facet_pb.name)
    facet_value_pb = facet_pb.value
    self.assertEqual('0', facet_value_pb.string_value)
    self.assertEqual(document_pb2.FacetValue.NUMBER, facet_value_pb.type)

  def testEquals(self):
    doc1_id = 'doc1_id'
    doc1_field1 = search.TextField(name='field1', value='field1 value1')
    doc1_field1_html = search.HtmlField(name='field1', value='field1 value1')
    doc1_field2 = search.TextField(name='field2', value='field2 value2')
    doc1_field3 = search.UntokenizedPrefixField(name='field3',
                                                value='field3 value3')
    doc1_field4 = search.TokenizedPrefixField(name='field4',
                                              value='field4 value4')
    doc1_facet1 = search.AtomFacet(name='facet1', value='facet1 value1')
    doc1_facet2 = search.AtomFacet(name='facet2', value='facet2 value1')
    doc1 = search.Document(doc_id=doc1_id, fields=[doc1_field1, doc1_field2,
                                                   doc1_field3, doc1_field4],
                           facets=[doc1_facet1, doc1_facet2], rank=123)
    doc2 = search.Document(doc_id=doc1_id, fields=[doc1_field1, doc1_field2,
                                                   doc1_field3, doc1_field4],
                           facets=[doc1_facet1, doc1_facet2], rank=123)
    self.assertEqual(doc1, doc2)

    doc1_pb = document_pb2.Document()
    search._CopyDocumentToProtocolBuffer(doc1, doc1_pb)
    doc2_pb = document_pb2.Document()
    search._CopyDocumentToProtocolBuffer(doc2, doc2_pb)
    self.assertEqual(doc1_pb, doc2_pb)

    doc2 = search.Document(doc_id=doc1_id, fields=[doc1_field2, doc1_field1],
                           facets=[doc1_facet1, doc1_facet2], rank=123)

    self.assertFalse(doc1 == doc2)

    doc2_pb = document_pb2.Document()
    search._CopyDocumentToProtocolBuffer(doc2, doc2_pb)
    self.assertFalse(doc1_pb == doc2_pb)

    doc2 = search.Document(doc_id=doc1_id, fields=[doc1_field1, doc1_field2],
                           facets=[doc1_facet2, doc1_facet1], rank=123)

    self.assertFalse(doc1 == doc2)

    doc2_pb = document_pb2.Document()
    search._CopyDocumentToProtocolBuffer(doc2, doc2_pb)
    self.assertFalse(doc1_pb == doc2_pb)

    doc2 = search.Document(doc_id=doc1_id,
                           fields=[doc1_field1_html, doc1_field2],
                           facets=[doc1_facet1, doc1_facet2], rank=123)
    self.assertFalse(doc1 == doc2)
    doc2_pb = document_pb2.Document()
    search._CopyDocumentToProtocolBuffer(doc2, doc2_pb)
    self.assertFalse(doc1_pb == doc2_pb)


    self.assertFalse(search.Document(
            doc_id=doc1_id,
            facets=[doc1_facet1, doc1_facet2], rank=123) == doc1)


    self.assertFalse(search.Document(
            doc_id=doc1_id,
            fields=[doc1_field1, doc1_field2], rank=123) == doc1)


    doc1_field2 = search.TextField(name='field2', value='field2 another value')
    doc2 = search.Document(doc_id=doc1_id, fields=[doc1_field2, doc1_field1],
                           facets=[doc1_facet1, doc1_facet2], rank=123)
    self.assertFalse(doc1 == doc2)


    doc1_facet2 = search.AtomFacet(name='facet2', value='facet2 another value')
    doc2 = search.Document(doc_id=doc1_id, fields=[doc1_field2, doc1_field1],
                           facets=[doc1_facet1, doc1_facet2], rank=123)
    self.assertFalse(doc1 == doc2)


    doc1 = search.Document(doc_id=doc1_id, fields=[doc1_field1])
    doc2 = search.Document(doc_id=doc1_id, fields=[doc1_field1, doc1_field1])
    self.assertFalse(doc1 == doc2)


    doc1 = search.Document(doc_id=doc1_id, facets=[doc1_facet1])
    doc2 = search.Document(doc_id=doc1_id, facets=[doc1_facet1, doc1_facet1])
    self.assertFalse(doc1 == doc2)


    text_field_1 = search.TextField(name='text', value='some text')
    text_field_2 = search.TextField(name='text', value='some text')
    self.assertEqual(text_field_1, text_field_2)
    self.assertFalse(text_field_1 != text_field_2)


    text_facet_1 = search.AtomFacet(name='text', value='some text')
    text_facet_2 = search.AtomFacet(name='text', value='some text')
    self.assertEqual(text_facet_1, text_facet_2)
    self.assertFalse(text_facet_1 != text_facet_2)


    doc_1 = search.Document(doc_id='abc', fields=[text_field_1],
                            facets=[doc1_facet1])
    doc_2 = search.Document(doc_id='abc', fields=[text_field_2],
                            facets=[doc1_facet1])
    self.assertEqual(doc_1, doc_2)
    self.assertFalse(doc_1 != doc_2)


    geo_point1 = search.GeoPoint(47.443511, -122.357398)
    geo_point2 = search.GeoPoint(47.443511, -122.357398)
    geo_point3 = search.GeoPoint(47.443511, 122)
    self.assertEqual(geo_point1, geo_point2)
    self.assertFalse(geo_point1 == geo_point3)
    doc_1 = search.Document(doc_id='abc',
                            fields=[search.GeoField(name='field',
                                                    value=geo_point1)])
    doc_2 = search.Document(doc_id='abc',
                            fields=[search.GeoField(name='field',
                                                    value=geo_point2)])
    doc_3 = search.Document(doc_id='abc',
                            fields=[search.GeoField(name='field',
                                                    value=geo_point3)])
    self.assertEqual(doc_1, doc_2)
    self.assertFalse(doc_1 != doc_2)
    self.assertFalse(doc_1 == doc_3)


    doc1 = search.Document(
        doc_id='doc', fields=[search.VectorField(name='name', value=[1, 2, 3])])
    doc2 = search.Document(
        doc_id='doc',
        fields=[search.VectorField(name='name', value=[1, 2.0, 3])])
    doc3 = search.Document(
        doc_id='doc', fields=[search.VectorField(name='name', value=[1, 2])])
    doc4 = search.Document(
        doc_id='doc', fields=[search.VectorField(name='name', value=[1, 2, 4])])
    self.assertEqual(doc1, doc2)
    self.assertFalse(doc1 != doc2)
    self.assertNotEqual(doc1, doc3)
    self.assertNotEqual(doc1, doc4)

  def testNewDocumentFromProtocolBuffer(self):
    doc_pb = document_pb2.Document()
    doc_pb.id = 'some_id'
    doc_pb.language = 'pl'
    doc = search._NewDocumentFromPb(doc_pb)
    self.assertEqual('some_id', doc.doc_id)
    self.assertEqual('pl', doc.language)
    self.assertIsInstance(doc.doc_id, six.text_type)
    self.assertIsInstance(doc.language, six.text_type)

  def testGetFieldByName(self):
    repeated = ['keep', 'calm', 'and', 'continue', 'testing']
    doc = search.Document(
        doc_id='id1',
        fields=[search.TextField(name='text', value=val) for val in repeated] +
               [search.NumberField(name='number', value=6),])

    self.assertEqual(len(repeated), len(doc['text']))
    self.assertEqual(set(repeated), set(f.value for f in doc['text']))

    self.assertEqual(1, len(doc['number']))
    self.assertEqual(6, doc['number'][0].value)

    self.assertEqual(0, len(doc['portals']))

    self.assertEqual('number', doc.field('number').name)
    self.assertEqual(6, doc.field('number').value)

    self.assertRaises(ValueError, doc.field, 'portals')
    self.assertRaises(ValueError, doc.field, 'text')

  def testGetFacetByName(self):
    doc = search.Document(
        doc_id='id1',
        facets=[search.AtomFacet(name='text', value='value'),
                search.NumberFacet(name='number', value=6)])

    self.assertEqual(1, len(doc.facet('text')))
    self.assertEqual('text', doc.facet('text')[0].name)
    self.assertEqual('value', doc.facet('text')[0].value)

    self.assertEqual('number', doc.facet('number')[0].name)
    self.assertEqual(6, doc.facet('number')[0].value)

    self.assertEqual(0, len(doc.facet('portals')))





















  def testHash(self):
    self.assertEqual(hash(search.Document()), hash(search.Document()))
    self.assertEqual(
        hash(search.Document(doc_id='abc')),
        hash(search.Document(doc_id='abc',
                             fields=[DocumentTest.DEFAULT_FIELD],
                             facets=[DocumentTest.DEFAULT_FACET])))
    self.assertEqual(hash(search.Document(doc_id='abc')),
                      hash(search.Document(doc_id='abc', language='pl')))

  def _testReprOrStr(self, func):

    self.assertReprEqual(
        "search.Document(doc_id=u'id', fields=["
        "search.TextField(name=u'field_name', language=u'pl', "
        "value=u'text')], facets=[search.AtomFacet(name=u'facet_name', "
        "value=u'text')], language=u'en', rank=999)",
        func(search.Document(
            doc_id='id',
            fields=[search.TextField(name='field_name', language='pl',
                                     value='text')],
            facets=[search.AtomFacet(name='facet_name', value='text')],
            language='en',
            rank=999)))

  def testRepr(self):
    self._testReprOrStr(repr)

  def testStr(self):
    self._testReprOrStr(str)

  def testRepeatedFields(self):
    self.assertRaises(
        ValueError, search.Document, 'should-break', [
            search.NumberField(name='repeat', value=1),
            search.NumberField(name='repeat', value=6),
            ])
    self.assertRaises(
        ValueError, search.Document, 'should-break', [
            search.DateField(name='repeat', value=datetime.date(2011, 5, 3)),
            search.DateField(name='repeat', value=datetime.date(1978, 5, 3)),
            ])

    self.assertRaises(
        ValueError, search.Document, 'should-break', [
            search.VectorField(name='repeat', value=[1, 2, 3]),
            search.VectorField(name='repeat', value=[1, 2, 3, 4]),
            ])
    self.assertRaises(
        ValueError, search.Document, 'should-break', [
            search.VectorField(name='repeat', value=[1, 2, 3]),
            search.VectorField(name='repeat', value=[1, 2, 3]),
            ])

    search.Document(
        'should-not-break', [
            search.NumberField(name='repeat', value=-10.2),
            search.DateField(name='repeat', value=datetime.date(1978, 5, 3)),
            ])
    search.Document(
        'should-not-break', [
            search.TextField(name='repeat', value='test one'),
            search.TextField(name='repeat', value='test two'),
            search.UntokenizedPrefixField(name='repeat', value='test one'),
            search.UntokenizedPrefixField(name='repeat', value='test two'),
            search.TokenizedPrefixField(name='repeat', value='test one'),
            search.TokenizedPrefixField(name='repeat', value='test two'),
            search.GeoField(name='repeat', value=search.GeoPoint(40, 100)),
            search.VectorField(name='repeat', value=[1, 2, 3]),
            search.DateField(name='repeat', value=datetime.date(1978, 5, 3)),
            ])

  def testRepeatedFacets(self):


    search.Document(
        'should-not-break', facets=[
            search.NumberFacet(name='repeat', value=-10.2),
            search.AtomFacet(name='repeat', value='value')])
    search.Document(
        'should-not-break', facets=[
            search.AtomFacet(name='repeat', value='test one'),
            search.AtomFacet(name='repeat', value='test two'),
            search.NumberFacet(name='repeat', value=10.2),
            search.NumberFacet(name='repeat', value=-5.1),])


class FieldExpressionTest(TestCase):

  def ExpressionIsParseable(self, expression):
    self.assertEqual(
        expression,
        search.FieldExpression(name='name', expression=expression).expression)

  def testRequiredArgumentMissing(self):
    self.assertRaises(ValueError, search.FieldExpression, name='name',
                      expression=None)
    self.assertRaises(TypeError, search.FieldExpression, name='tax-price')
    self.assertRaises(TypeError, search.FieldExpression,
                      expression='tax + price')

  def testMinimalFieldExpression(self):
    expr = search.FieldExpression(name='tax_price',
                                  expression='tax + price')
    self.assertEqual('tax_price', expr.name)
    self.assertEqual('tax + price', expr.expression)

  def testUnicodeOut(self):
    expr = search.FieldExpression(name='name', expression='expression')
    self.assertIsInstance(expr.name, six.text_type)
    self.assertIsInstance(expr.expression, six.text_type)

  def testParsingExpression(self):
    snippet = 'snippet("' + _UNICODE_QUERY_ESCAPED + '", content)'
    search._CheckExpression(snippet)
    self.ExpressionIsParseable('tax + price < 100')
    self.ExpressionIsParseable('snippet("query this", content)')
    self.ExpressionIsParseable('snippet("\\\"query this\\\"", content)')
    self.ExpressionIsParseable('snippet("\\\"query this\\\" that", content)')
    self.ExpressionIsParseable('snippet("' + _UNICODE_QUERY_ESCAPED +
                               '", content)')
    self.ExpressionIsParseable('count(tag) <= 2')
    self.ExpressionIsParseable('55 / 11')
    try:
      search.FieldExpression(name='unparseable', expression='snippet(')
      self.fail('Expected ExpressionError')
    except search.ExpressionError as e:
      self.assertEqual(u'Failed to parse expression "snippet("', str(e))
    self.assertRaises(search.ExpressionError,
                      search.FieldExpression, name='unparseable',
                      expression='tax > ')

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.FieldExpression, foo='bar')

  def testName(self):
    expression = 'snippet(query, content)'

    self.assertRaises(ValueError, search.FieldExpression,
                      name='_RESERVED', expression=expression)

    name = 's' * search.MAXIMUM_FIELD_NAME_LENGTH
    self.assertEqual(name,
                      search.FieldExpression(name=name,
                                             expression=expression).name)
    self.assertRaises(ValueError, search.FieldExpression,
                      name=name + 's', expression=expression)

    self.assertRaises(ValueError, search.FieldExpression,
                      name=None, expression=expression)

  def testWrongTypes(self):
    self.assertRaises(TypeError, search.FieldExpression, name=0)
    self.assertRaises(TypeError, search.FieldExpression, name='name',
                      expression=0)

  def testCopyFieldExpressionToProtocolBuffer(self):
    expression = search.FieldExpression(
        name='snippet', expression='snippet(query, content)')
    expr_pb = search_service_pb2.FieldSpec.Expression()
    search._CopyFieldExpressionToProtocolBuffer(expression, expr_pb)
    self.assertEqual('snippet', expr_pb.name)
    self.assertEqual('snippet(query, content)', expr_pb.expression)

  def testCopyFieldExpressionToProtocolBufferUnicode(self):
    expr = 'snippet("' + _UNICODE_QUERY_ESCAPED + '", content)'
    expression = search.FieldExpression(name='snippet', expression=expr)
    expr_pb = search_service_pb2.FieldSpec.Expression()
    search._CopyFieldExpressionToProtocolBuffer(expression, expr_pb)
    self.assertEqual('snippet', expr_pb.name)
    self.assertEqual(expr, expr_pb.expression)

  def testRepr(self):
    self.assertReprEqual(
        "search.FieldExpression(name=u'tax_price', "
        "expression=u'tax + price')",
        repr(search.FieldExpression(name='tax_price',
                                    expression='tax + price')))

  def testScore(self):
    self.assertReprEqual(
        "search.FieldExpression(name=u'score', "
        "expression=u'_score')",
        repr(search.FieldExpression(name='score',
                                    expression='_score')))
    self.ExpressionIsParseable('0.1 + _score * 0.01')


class MatchScorerTest(absltest.TestCase):

  def testMinimalScorer(self):
    search.MatchScorer()
    search.RescoringMatchScorer()

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.MatchScorer, foo='bar')
    self.assertRaises(TypeError, search.RescoringMatchScorer, foo='bar')
    self.assertRaises(TypeError, search.MatchScorer, limit='TEN')
    self.assertRaises(TypeError, search.RescoringMatchScorer, limit='TEN')
    self.assertRaises(TypeError, search.MatchScorer, limit=100.1)
    self.assertRaises(TypeError, search.RescoringMatchScorer, limit=100.1)

  def testCopyMatchScorerToScorerSpecProtocolBuffer(self):
    scorer_pb = search_service_pb2.ScorerSpec()
    search._CopyMatchScorerToScorerSpecProtocolBuffer(
        search.RescoringMatchScorer(),
        567,
        scorer_pb)
    self.assertEqual(search_service_pb2.ScorerSpec.RESCORING_MATCH_SCORER,
                      scorer_pb.scorer)
    self.assertEqual(567, scorer_pb.limit)

    scorer_pb = search_service_pb2.ScorerSpec()
    search._CopyMatchScorerToScorerSpecProtocolBuffer(
        search.MatchScorer(),
        678,
        scorer_pb)
    self.assertEqual(search_service_pb2.ScorerSpec.MATCH_SCORER,
                      scorer_pb.scorer)
    self.assertEqual(678, scorer_pb.limit)

    self.assertRaises(TypeError,
                      search._CopyMatchScorerToScorerSpecProtocolBuffer,
                      search.SortExpression(expression='expression'),
                      567, scorer_pb)

  def testRepr(self):
    self.assertEqual('search.MatchScorer()', repr(search.MatchScorer()))

    self.assertEqual('search.RescoringMatchScorer()',
                      repr(search.RescoringMatchScorer()))


class SortExpressionTest(TestCase):

  def testRequiredArgumentsMissing(self):
    self.assertRaises(TypeError, search.SortExpression)
    self.assertRaises(TypeError, search.SortExpression,
                      direction=search.SortExpression.DESCENDING)
    self.assertRaises(TypeError, search.SortExpression,
                      direction=search.SortExpression.DESCENDING,
                      default_value='some stuff')
    self.assertEqual(
        'name', search.SortExpression(
            expression='name',
            direction=search.SortExpression.DESCENDING).expression)
    self.assertEqual(
        'zzzz', search.SortExpression(
            expression='name',
            direction=search.SortExpression.DESCENDING,
            default_value='zzzz').default_value)

  def testDefaultValueUnicode(self):
    subject_snippet = ('snippet("' +
                       u'\xd9\x85\xd8\xb3\xd8\xa7\xd8\xb9\xd8\xaf\xd8\xa9' +
                       '", subject)')
    search._CheckExpression(subject_snippet)
    subject_snippet = 'snippet("' + _UNICODE_QUERY_ESCAPED + '", subject)'
    search._CheckExpression(subject_snippet)
    expr = search.SortExpression(expression=subject_snippet,
                                 default_value=_UNICODE_STRING)
    self.assertEqual(subject_snippet, expr.expression)
    self.assertEqual(_UNICODE_STRING, expr.default_value)

  def testUnicodeOut(self):
    sort_expr = search.SortExpression(expression='expression',
                                      default_value='default_value')
    self.assertIsInstance(sort_expr.expression, six.text_type)
    self.assertIsInstance(sort_expr.default_value, six.text_type)
    sort_expr = search.SortExpression(expression='numeric',
                                      default_value=0)
    self.assertIsInstance(sort_expr.expression, six.text_type)
    self.assertIsInstance(sort_expr.default_value, int)

  def testMinimalSortExpression(self):
    sort_expr = search.SortExpression(expression='name')
    self.assertEqual('name', sort_expr.expression)
    self.assertEqual(search.SortExpression.DESCENDING, sort_expr.direction)
    self.assertEqual(None, sort_expr.default_value)

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.SortExpression, expression='name',
                      foo='bar')
    self.assertRaises(TypeError, search.SortExpression,
                      expression='expression', limit=100)

  def testNameTooLong(self):
    name = 's' * search.MAXIMUM_EXPRESSION_LENGTH
    self.assertEqual(name, search.SortExpression(expression=name).expression)
    self.assertRaises(ValueError, search.SortExpression, expression=name + 's')

  def testNameWrongType(self):
    for value in _NON_STRING_VALUES:
      self.assertRaises(TypeError, search.SortExpression, expression=value)

  def testNameUnicode(self):

    try:
      search.SortExpression(expression=u'\xaa')
      self.fail('Expected ExpressionError')
    except search.ExpressionError as e:
      expected = u'Failed to parse expression "\xaa"'
      actual = e.message if six.PY2 else str(e)
      self.assertEqual(expected, actual)
    self.assertRaises(search.ExpressionError,
                      search.SortExpression, expression=_UNICODE_STRING)

  def testNameTooShort(self):
    self.assertRaises(ValueError, search.SortExpression, expression='')

  def testValueTooLong(self):
    value = 'v' * search.MAXIMUM_FIELD_VALUE_LENGTH
    self.assertEqual(
        value, search.SortExpression(expression='name',
                                     default_value=value).default_value)
    self.assertRaises(ValueError, search.SortExpression, expression='name',
                      default_value=value + 'v')

  def testValueWrongType(self):
    self.assertRaises(TypeError, search.SortExpression, expression='name',
                      default_value=datetime.time())

  def testDefaultValues(self):
    self.assertEqual(
        search.SortExpression.MAX_FIELD_VALUE,
        search.SortExpression(
            expression='name',
            default_value=search.SortExpression.MAX_FIELD_VALUE).default_value)
    self.assertEqual(
        search.SortExpression.MIN_FIELD_VALUE,
        search.SortExpression(
            expression='name',
            default_value=search.SortExpression.MIN_FIELD_VALUE).default_value)
    someday = datetime.date(year=1999, month=12, day=31)
    self.assertEqual(
        someday, search.SortExpression('published_date',
                                       default_value=someday).default_value)

  def testWrongTypes(self):
    self.assertRaises(TypeError, search.SortExpression, expression=1)
    self.assertEqual(
        search.SortExpression.DESCENDING,
        search.SortExpression(expression='name',
                              direction='DESCENDING').direction)
    self.assertRaises(ValueError, search.SortExpression, expression='name',
                      direction=0)

    self.assertEqual(
        1, search.SortExpression(expression='name',
                                 default_value=1).default_value)

  def testCopySortExpressionToProtocolBuffer(self):
    sort_pb = search_service_pb2.SortSpec()
    search._CopySortExpressionToProtocolBuffer(
        search.SortExpression(expression='name'), sort_pb)
    self.assertEqual('name', sort_pb.sort_expression)
    self.assertTrue(sort_pb.sort_descending)
    self.assertFalse(sort_pb.HasField('default_value_text'))

    sort_pb = search_service_pb2.SortSpec()
    search._CopySortExpressionToProtocolBuffer(
        search.SortExpression(
            expression='name', direction=search.SortExpression.ASCENDING,
            default_value='default'),
        sort_pb)
    self.assertEqual('name', sort_pb.sort_expression)
    self.assertFalse(sort_pb.sort_descending)
    self.assertEqual('default', sort_pb.default_value_text)

    sort_pb = search_service_pb2.SortSpec()
    search._CopySortExpressionToProtocolBuffer(
        search.SortExpression(
            expression='name', direction=search.SortExpression.ASCENDING,
            default_value=0),
        sort_pb)
    self.assertEqual('name', sort_pb.sort_expression)
    self.assertFalse(sort_pb.sort_descending)
    self.assertFalse(sort_pb.HasField('default_value_text'))
    self.assertEqual(0, sort_pb.default_value_numeric)

    sort_pb = search_service_pb2.SortSpec()
    search._CopySortExpressionToProtocolBuffer(
        search.SortExpression(
            expression='name', direction=search.SortExpression.ASCENDING,
            default_value=123),
        sort_pb)
    self.assertEqual('name', sort_pb.sort_expression)
    self.assertFalse(sort_pb.sort_descending)
    self.assertFalse(sort_pb.HasField('default_value_text'))
    self.assertEqual(123, sort_pb.default_value_numeric)

    sort_pb = search_service_pb2.SortSpec()
    someday = datetime.date(year=2011, month=1, day=1)
    search._CopySortExpressionToProtocolBuffer(
        search.SortExpression('published_date', default_value=someday),
        sort_pb)
    self.assertEqual('published_date', sort_pb.sort_expression)
    self.assertTrue(sort_pb.sort_descending)
    self.assertFalse(sort_pb.HasField('default_value_numeric'))

    self.assertEqual('1293840000000', sort_pb.default_value_text)

    sort_pb = search_service_pb2.SortSpec()
    someday = datetime.date(year=1969, month=12, day=31)
    search._CopySortExpressionToProtocolBuffer(
        search.SortExpression('published_date', default_value=someday),
        sort_pb)
    self.assertFalse(sort_pb.HasField('default_value_numeric'))

    self.assertEqual('-86400000', sort_pb.default_value_text)

    sort_pb = search_service_pb2.SortSpec()
    someday = datetime.date(year=1970, month=1, day=1)
    search._CopySortExpressionToProtocolBuffer(
        search.SortExpression('published_date', default_value=someday),
        sort_pb)
    self.assertEqual(0, sort_pb.default_value_numeric)

    sort_pb = search_service_pb2.SortSpec()
    someday = datetime.date(year=1970, month=1, day=2)
    search._CopySortExpressionToProtocolBuffer(
        search.SortExpression('published_date', default_value=someday),
        sort_pb)
    self.assertFalse(sort_pb.HasField('default_value_numeric'))
    self.assertEqual('86400000', sort_pb.default_value_text)

    sort_pb = search_service_pb2.SortSpec()
    someday = datetime.date(year=1914, month=0o4, day=19)
    search._CopySortExpressionToProtocolBuffer(
        search.SortExpression('published_date', default_value=someday),
        sort_pb)
    self.assertFalse(sort_pb.HasField('default_value_numeric'))
    self.assertEqual('-1757894400000', sort_pb.default_value_text)

  def testCopySortExpressionToProtocolBufferUnicode(self):
    sort_pb = search_service_pb2.SortSpec()
    subject_snippet = u'snippet("' + _UNICODE_QUERY_ESCAPED + u'", subject)'
    search._CheckExpression(subject_snippet)
    expr = search.SortExpression(expression=subject_snippet,
                                 default_value=_UNICODE_STRING)
    search._CopySortExpressionToProtocolBuffer(expr, sort_pb)
    self.assertEqual(subject_snippet, sort_pb.sort_expression)
    self.assertEqual(True, sort_pb.sort_descending)
    self.assertEqual(_UNICODE_STRING, sort_pb.default_value_text)

  def testRepr(self):
    self.assertReprEqual(
        "search.SortExpression(expression=u'price', direction='DESCENDING', "
        "default_value=9999)",
        repr(search.SortExpression(expression='price', default_value=9999)))

  def testSystemFields(self):
    self.assertReprEqual(
        "search.SortExpression(expression=u'_doc_id', direction='DESCENDING', "
        "default_value=u'')",
        repr(search.SortExpression(
            expression=search.DOCUMENT_ID_FIELD_NAME, default_value='')))
    self.assertReprEqual(
        "search.SortExpression(expression=u'_lang', direction='DESCENDING', "
        "default_value=u'')",
        repr(search.SortExpression(
            expression=search.LANGUAGE_FIELD_NAME, default_value='')))
    self.assertReprEqual(
        "search.SortExpression(expression=u'_rank', direction='DESCENDING', "
        "default_value=0)",
        repr(search.SortExpression(
            expression=search.RANK_FIELD_NAME, default_value=0)))
    self.assertReprEqual(
        "search.SortExpression(expression=u'_score', direction='DESCENDING', "
        "default_value=0)",
        repr(search.SortExpression(
            expression=search.SCORE_FIELD_NAME, default_value=0)))
    self.assertReprEqual(
        "search.SortExpression(expression=u'_timestamp', "
        "direction='DESCENDING', default_value=0)",
        repr(search.SortExpression(
            expression=search.TIMESTAMP_FIELD_NAME, default_value=0)))


class OperationResultTest(TestCase):

  def testUnknownArguments(self):
    self.assertRaises(TypeError, search.OperationResult, foo='bar')

  def testMinimal(self):
    result = search.OperationResult(
        code=search.OperationResult.OK)
    self.assertEqual(search.OperationResult.OK, result.code)
    self.assertEqual(None, result.message)

    result = search.OperationResult(code='OK')
    self.assertEqual(search.OperationResult.OK, result.code)

  def testWrongTypes(self):
    self.assertRaises(ValueError, search.OperationResult, code=0)
    self.assertRaises(TypeError, search.OperationResult,
                      code=search.OperationResult.OK, message=0)

  def testFullSpec(self):
    result = search.OperationResult(
        code=search.OperationResult.OK, message='message')
    self.assertEqual(search.OperationResult.OK, result.code)
    self.assertEqual('message', result.message)

  def testRepr(self):
    self.assertReprEqual(
        "search.OperationResult(code='OK', message=u'message')",
        repr(search.OperationResult(
            code=search.OperationResult.OK, message='message')))


class ScoredDocumentTest(TestCase):

  FIELDS = [search.TextField(name='name')]

  DEFAULT_EXPRESSION = search.TextField(name='snippet',
                                        value='some <b>snippet</b> text'),

  def testToWebSafeStringUnicode(self):
    web_safe_string = search._ToWebSafeString(True, _UNICODE_STRING)
    self.assertIsInstance(web_safe_string, six.text_type)
    web_safe_string = search._ToWebSafeString(True, u'abc')
    self.assertIsInstance(web_safe_string, six.text_type)
    if six.PY2:
      web_safe_string = search._ToWebSafeString(True, 'abc')
      self.assertNotIsInstance(web_safe_string, six.text_type)

  def testFullResult(self):
    cursor = search.Cursor(web_safe_string='False:someposition')
    document = search.ScoredDocument(
        doc_id='id9',
        fields=self.FIELDS,
        language='fr',
        rank=999,
        sort_scores=[1.0],
        expressions=[self.DEFAULT_EXPRESSION],
        cursor=cursor)
    self.assertEqual('id9', document.doc_id)
    self.assertEqual(self.FIELDS, document.fields)
    self.assertEqual('fr', document.language)
    self.assertEqual(999, document.rank)
    self.assertEqual([1.0], document.sort_scores)
    self.assertEqual([self.DEFAULT_EXPRESSION], document.expressions)
    self.assertEqual(cursor, document.cursor)

  def testUnicodeOut(self):
    document = search.ScoredDocument(doc_id='id9', language='fr')
    self.assertIsInstance(document.doc_id, six.text_type)
    self.assertIsInstance(document.language, six.text_type)

  def testUnknownAttribute(self):
    self.assertRaises(TypeError, search.ScoredDocument, foo='bar')

  def testInvalidTypes(self):
    self.assertRaises(TypeError, search.ScoredDocument, sort_scores=1.0)
    self.assertRaises(TypeError, search.ScoredDocument, sort_scores=['good'])
    self.assertRaises(TypeError, search.ScoredDocument, cursor=999)
    self.assertRaises(TypeError, search.ScoredDocument, cursor=[])

  def testExpressions(self):
    self.assertEqual([], search.ScoredDocument().expressions)

  def testRepr(self):
    self.assertReprEqual(
        "search.ScoredDocument(doc_id=u'id', language=u'en', rank=999)",
        repr(search.ScoredDocument(doc_id='id', rank=999)))


class FacetRefinementTest(absltest.TestCase):

  VALUE_REFINEMENT = search.FacetRefinement(name='name', value='value')
  RANGE_REFINEMENT = search.FacetRefinement(
        name='name', facet_range=search.FacetRange(start=1, end=2))

  def testValueRefinement(self):
    ref = self.VALUE_REFINEMENT
    self.assertEqual('name', ref.name)
    self.assertEqual('value', ref.value)
    self.assertEqual(None, ref.facet_range)

    ref_pb = search_service_pb2.FacetRefinement()
    ref._CopyToProtocolBuffer(ref_pb)
    self.assertEqual('name', ref_pb.name)
    self.assertEqual('value', ref_pb.value)
    self.assertFalse(ref_pb.HasField('range'))


    ref = search.FacetRefinement(name='name', value=12)
    self.assertEqual('name', ref.name)
    self.assertEqual(12, ref.value)
    self.assertEqual(None, ref.facet_range)

    ref_pb = search_service_pb2.FacetRefinement()
    ref._CopyToProtocolBuffer(ref_pb)
    self.assertEqual('name', ref_pb.name)
    self.assertEqual('12', ref_pb.value)
    self.assertFalse(ref_pb.HasField('range'))

  def testRangeRefinement(self):
    ref = self.RANGE_REFINEMENT
    self.assertEqual('name', ref.name)
    self.assertEqual(None, ref.value)
    self.assertEqual(1, ref.facet_range.start)
    self.assertEqual(2, ref.facet_range.end)

    ref_pb = search_service_pb2.FacetRefinement()
    ref._CopyToProtocolBuffer(ref_pb)
    self.assertEqual('name', ref_pb.name)
    self.assertFalse(ref_pb.HasField('value'))
    self.assertEqual('1', ref_pb.range.start)
    self.assertEqual('2', ref_pb.range.end)

  def testInvalidRefinement(self):
    self.assertRaises(ValueError, search.FacetRefinement,
                      name='name', value='value',
                      facet_range=search.FacetRange(start=1, end=2))
    self.assertRaises(TypeError, search.FacetRefinement,
                      'name', 'value')
    self.assertRaises(ValueError, search.FacetRefinement,
                      'name')

  def testTokenString(self):
    ref = search.FacetRefinement.FromTokenString(
        self.VALUE_REFINEMENT.ToTokenString())
    self.assertEqual('name', ref.name)
    self.assertEqual('value', ref.value)
    self.assertEqual(None, ref.facet_range)

    ref = search.FacetRefinement.FromTokenString(
        self.RANGE_REFINEMENT.ToTokenString())
    self.assertEqual('name', ref.name)
    self.assertEqual(None, ref.value)
    self.assertEqual(1, ref.facet_range.start)
    self.assertEqual(2, ref.facet_range.end)


    ref_token = self.VALUE_REFINEMENT.ToTokenString()
    invalid_token = b'abc' + ref_token[3:0]
    self.assertRaises(ValueError,
                      search.FacetRefinement.FromTokenString, invalid_token)


class FacetRangeTest(absltest.TestCase):

  def testFacetRange(self):
    facet_range = search.FacetRange(start=1, end=2)
    self.assertEqual(1, facet_range.start)
    self.assertEqual(2, facet_range.end)

    facet_range = search.FacetRange(start=1)
    self.assertEqual(1, facet_range.start)
    self.assertEqual(None, facet_range.end)

    facet_range = search.FacetRange(end=2)
    self.assertEqual(None, facet_range.start)
    self.assertEqual(2, facet_range.end)

  def testInvalidFacetRange(self):
    self.assertRaises(ValueError, search.FacetRange)
    self.assertRaises(TypeError, search.FacetRange, 1)
    self.assertRaises(TypeError, search.FacetRange, start='1')
    self.assertRaises(TypeError, search.FacetRange, end='1')


class SearchResultsTest(absltest.TestCase):

  DEFAULT_RESULT = search.ScoredDocument(
      doc_id='id', fields=[search.TextField(name='name')])

  DEFAULT_FACET_RESULT = search.FacetResult(
      name='facet1', values=[
          search.FacetResultValue(
              label='value1', count=10, refinement=search.FacetRefinement(
                  name='facet1', value='value1'))])

  def testMinimalSearchResult(self):
    results = search.SearchResults(
        results=[self.DEFAULT_RESULT], number_found=1,
        facets=[self.DEFAULT_FACET_RESULT])
    self.assertEqual([self.DEFAULT_RESULT], results.results)
    self.assertEqual([self.DEFAULT_FACET_RESULT], results.facets)
    self.assertEqual(1, results.number_found)
    self.assertEqual(1, len(results.results))

  def testEmptySearchResults(self):
    results = search.SearchResults(results=[], number_found=0)
    self.assertEqual([], results.results)
    self.assertEqual(0, results.number_found)
    self.assertEqual(0, len(results.results))
    self.assertEqual(0, len(results.facets))

  def testCursor(self):
    cursor = search.Cursor(web_safe_string='False:some_cursor')
    results = search.SearchResults(
        results=[self.DEFAULT_RESULT], number_found=1, cursor=cursor)
    self.assertEqual(cursor, results.cursor)

  def testUnknownArgument(self):
    self.assertRaises(TypeError, search.SearchResults,
                      results=[self.DEFAULT_RESULT], foo='bar')

  def testInvalidTypes(self):

    self.assertEqual(
        len('some results'),
        len(search.SearchResults(0, results='some results').results))
    self.assertEqual(
        ['some result'],
        search.SearchResults(0, results=['some result']).results)
    self.assertRaises(ValueError, search.SearchResults, results=[],
                      number_found='none')
    self.assertRaises(ValueError, search.SearchResults, results=[],
                      number_found=[])
    self.assertRaises(TypeError, search.SearchResults, number_found=0,
                      results=[], cursor='some string')

  def testIterable(self):
    self.assertEqual([1, 2, 3],
                      [x for x in search.SearchResults(
                          results=[1, 2, 3], number_found=1)])

  def testRepr(self):
    cursor = search.Cursor()
    self.assertEqual(
        'search.SearchResults(number_found=0, cursor=%s)' % repr(cursor),
        repr(search.SearchResults(number_found=0, cursor=cursor)))


class CursorTest(TestCase):

  def testCursorUnicode(self):
    cursor = u'False:' + _UNICODE_STRING
    self.assertEqual(cursor,
                      search.Cursor(web_safe_string=cursor).web_safe_string)

  def testWrongTypes(self):
    self.assertRaises(TypeError, search.Cursor, web_safe_string=9999)

  def testCursorEmpty(self):
    self.assertEqual('', search.Cursor(web_safe_string='').web_safe_string)

  def testCursorWrongFormat(self):
    self.assertRaises(ValueError, search.Cursor, web_safe_string=' ')
    self.assertRaises(ValueError, search.Cursor, web_safe_string='a:b:c')
    self.assertRaises(ValueError, search.Cursor, web_safe_string='truely:foo')

  def testCursorTooLong(self):
    prefix = 'True:'
    length = search._MAXIMUM_CURSOR_LENGTH - len(prefix)
    web_safe_string = prefix + ('c' * length)
    self.assertEqual(
        web_safe_string,
        search.Cursor(web_safe_string=web_safe_string).web_safe_string)
    self.assertRaises(ValueError, search.Cursor,
                      web_safe_string=web_safe_string + 'c')

  def testFullySpecified(self):
    cursor = search.Cursor('False:rrrr')
    self.assertFalse(cursor.per_result)
    self.assertEqual('False:rrrr', cursor.web_safe_string)

    cursor = search.Cursor('False:rrrr', per_result=True)
    self.assertFalse(cursor.per_result)
    self.assertEqual('False:rrrr', cursor.web_safe_string)

  def testUnicodeOut(self):
    cursor = search.Cursor('False:rrrr')
    self.assertIsInstance(cursor.web_safe_string, six.text_type)
    self.assertFalse(cursor.per_result)

  def testRepr(self):
    self.assertReprEqual(
        "search.Cursor(web_safe_string=u'True:rrrr')",
        repr(search.Cursor(web_safe_string='True:rrrr')))
    self.assertReprEqual(
        "search.Cursor(web_safe_string=u'True:r\\xe7')",
        repr(search.Cursor(web_safe_string=u'True:r\xe7')))

  def testCopyCursorToProtocolBuffer(self):
    params = search_service_pb2.SearchParams()
    web_safe_string = 'False:' + _UNICODE_STRING
    search._CopyQueryOptionsObjectToProtocolBuffer(
        'query',
        search.QueryOptions(
            cursor=search.Cursor(web_safe_string=web_safe_string)),
        params)
    self.assertEqual(_UNICODE_STRING, params.cursor)


class SortOptionsTest(TestCase):

  def testFullySpecified(self):
    sort_options = search.SortOptions(
        expressions=[
            search.SortExpression(expression='_SCORE + (goodness * .001)',
                                  default_value=0.0)],
        match_scorer=search.MatchScorer(),
        limit=237)
    self.assertEqual(1, len(sort_options.expressions))
    self.assertIsInstance(sort_options.match_scorer, search.MatchScorer)
    self.assertEqual(237, sort_options.limit)



  def testCopyToProtocolBuffer(self):
    sort_options = search.SortOptions(
        expressions=[
            search.SortExpression(expression='author')],
        limit=123)

    self.assertEqual(1, len(sort_options.expressions))
    self.assertEqual(None, sort_options.match_scorer)
    self.assertEqual(123, sort_options.limit)

    params_pb = search_service_pb2.SearchParams()
    search._CopySortOptionsToProtocolBuffer(sort_options, params_pb)

    self.assertFalse(params_pb.HasField('cursor'))
    self.assertLen(params_pb.sort_spec, 1)
    sort_spec_pb = params_pb.sort_spec[0]
    self.assertEqual('author', sort_spec_pb.sort_expression)
    self.assertTrue(sort_spec_pb.sort_descending)
    self.assertFalse(sort_spec_pb.HasField('default_value_text'))
    scorer_spec_pb = params_pb.scorer_spec
    self.assertEqual(123, scorer_spec_pb.limit)
    self.assertFalse(scorer_spec_pb.HasField('scorer'))
    self.assertEqual(search_service_pb2.ScorerSpec.MATCH_SCORER,
                      scorer_spec_pb.scorer)


    params_pb = search_service_pb2.SearchParams()
    params_pb.scorer_spec.limit = 123
    scorer_spec_pb = params_pb.scorer_spec
    self.assertEqual(123, scorer_spec_pb.limit)
    self.assertFalse(scorer_spec_pb.HasField('scorer'))
    self.assertEqual(search_service_pb2.ScorerSpec.MATCH_SCORER,
                      scorer_spec_pb.scorer)

    sort_options = search.SortOptions(
        expressions=[
            search.SortExpression(expression='author'),
            search.SortExpression(expression='birthday',
                                  default_value=datetime.date(2014, 1, 1))],
        limit=123,
        match_scorer=search.RescoringMatchScorer())

    self.assertEqual(2, len(sort_options.expressions))
    self.assertIsInstance(sort_options.match_scorer,
                          search.RescoringMatchScorer)
    self.assertEqual(123, sort_options.limit)

    params_pb = search_service_pb2.SearchParams()
    search._CopySortOptionsToProtocolBuffer(sort_options, params_pb)

    self.assertFalse(params_pb.HasField('cursor'))
    self.assertLen(params_pb.sort_spec, 2)
    sort_spec_pb = params_pb.sort_spec[0]
    self.assertEqual('author', sort_spec_pb.sort_expression)
    self.assertTrue(sort_spec_pb.sort_descending)
    self.assertFalse(sort_spec_pb.HasField('default_value_text'))
    sort_spec_pb = params_pb.sort_spec[1]
    self.assertEqual('birthday', sort_spec_pb.sort_expression)
    self.assertTrue(sort_spec_pb.sort_descending)
    self.assertTrue(sort_spec_pb.HasField('default_value_text'))
    self.assertEqual('1388534400000', sort_spec_pb.default_value_text)
    scorer_spec_pb = params_pb.scorer_spec
    self.assertEqual(123, scorer_spec_pb.limit)
    self.assertTrue(scorer_spec_pb.HasField('scorer'))
    self.assertEqual(search_service_pb2.ScorerSpec.RESCORING_MATCH_SCORER,
                      scorer_spec_pb.scorer)

  def testRepr(self):
    sort_options = search.SortOptions(
        expressions=[
            search.SortExpression(
                expression=search.SCORE_FIELD_NAME + ' + (goodness * .001)',
                default_value=0.0)],
        match_scorer=search.MatchScorer(),
        limit=237)
    self.assertReprEqual(
        "search.SortOptions(match_scorer=search.MatchScorer(), "
        "expressions=[search.SortExpression(expression=u'_score + "
        "(goodness * .001)', direction='DESCENDING', default_value=0.0)], "
        "limit=237)", repr(sort_options))
    sort_options = search.SortOptions(
        expressions=[
            search.SortExpression(
                expression=search.RANK_FIELD_NAME + ' * -1',
                default_value=0.0)],
        match_scorer=search.MatchScorer(),
        limit=237)
    self.assertReprEqual(
        "search.SortOptions(match_scorer=search.MatchScorer(), "
        "expressions=[search.SortExpression(expression=u'_rank * "
        "-1', direction='DESCENDING', default_value=0.0)], "
        "limit=237)", repr(sort_options))


class FacetOptionsTest(absltest.TestCase):

  def testDiscoveryLimit(self):
    n = search.MAXIMUM_FACETS_TO_RETURN
    self.assertEqual(n, search.FacetOptions(discovery_limit=n).discovery_limit)
    self.assertRaises(ValueError, search.FacetOptions, discovery_limit=n + 1)
    self.assertRaises(ValueError, search.FacetOptions, discovery_limit=-1)

  def testDiscoveryValueLimit(self):
    n = search.MAXIMUM_FACET_VALUES_TO_RETURN
    self.assertEqual(
        n, search.FacetOptions(discovery_value_limit=n).discovery_value_limit)
    self.assertRaises(ValueError, search.FacetOptions,
                      discovery_value_limit=n + 1)
    self.assertRaises(ValueError, search.FacetOptions,
                      discovery_value_limit=-1)

  def testDepth(self):
    n = search.MAXIMUM_DEPTH_FOR_FACETED_SEARCH
    self.assertEqual(n, search.FacetOptions(depth=n).depth)
    self.assertRaises(ValueError, search.FacetOptions, depth=n + 1)
    self.assertRaises(ValueError, search.FacetOptions, depth=-1)

  def testUnknownAttribute(self):
    self.assertRaises(TypeError, search.FacetOptions, unknown_attr=0)

  def testCopyFacetOptionsObjectToProtocolBuffer(self):
    facet_options = search.FacetOptions(
        discovery_limit=5, discovery_value_limit=6, depth=4000)
    request = search_service_pb2.SearchRequest()
    params = request.params
    facet_options._CopyToProtocolBuffer(params)
    self.assertEqual(5, params.auto_discover_facet_count)
    self.assertEqual(6, params.facet_auto_detect_param.value_limit)
    self.assertEqual(4000, params.facet_depth)

    facet_options = search.FacetOptions()
    request = search_service_pb2.SearchRequest()
    params = request.params
    facet_options._CopyToProtocolBuffer(params)
    self.assertTrue(
        params.HasField('auto_discover_facet_count') and
        params.auto_discover_facet_count > 0)
    self.assertFalse(
        params.HasField('facet_auto_detect_param') and
        params.facet_auto_detect_param.HasField('value_limit'))
    self.assertFalse(params.HasField('facet_depth'))


class QueryOptionsTest(absltest.TestCase):

  def testNumDocsToReturn(self):
    n = search.MAXIMUM_DOCUMENTS_RETURNED_PER_SEARCH
    self.assertEqual(n, search.QueryOptions(limit=n).limit)
    self.assertRaises(ValueError, search.QueryOptions, limit=n + 1)

  def testMinDocsFoundAccuracy(self):
    self.assertIsNone(search.QueryOptions().number_found_accuracy)
    n = search.MAXIMUM_NUMBER_FOUND_ACCURACY
    self.assertEqual(n, search.QueryOptions(
        number_found_accuracy=n).number_found_accuracy)
    self.assertRaises(ValueError, search.QueryOptions,
                      number_found_accuracy=n + 1)

  def testCursor(self):
    self.assertRaises(TypeError, search.QueryOptions,
                      cursor='some string')
    cursor = search.Cursor()
    self.assertEqual(cursor, search.QueryOptions(cursor=cursor).cursor)

  def testOffset(self):
    self.assertEqual(19, search.QueryOptions(offset=19).offset)
    self.assertEqual(
        search.MAXIMUM_SEARCH_OFFSET,
        search.QueryOptions(offset=search.MAXIMUM_SEARCH_OFFSET).offset)
    self.assertRaises(ValueError, search.QueryOptions,
                      offset=search.MAXIMUM_SEARCH_OFFSET + 1)
    self.assertRaises(ValueError, search.QueryOptions,
                      offset='some string')

    cursor = search.Cursor()
    self.assertRaises(ValueError, search.QueryOptions, cursor=cursor, offset=19)


    cursor = search.Cursor()
    self.assertRaises(ValueError, search.QueryOptions, cursor=cursor, offset=19)

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.QueryOptions, foo='bar')

  def testIdsOnlyWithReturnedFields(self):
    self.assertRaises(ValueError, search.QueryOptions, ids_only=True,
                      returned_fields=['somefield'])

  def testFullySpecified(self):
    cursor = search.Cursor()
    sort_options = search.SortOptions(
        expressions=[search.SortExpression(expression='subject',
                                           default_value='ZZZZZ')])
    returned_fields = ['subject', 'body']
    snippeted_fields = ['subject', 'body']
    returned_expressions = [
        search.FieldExpression(name='content_snippet',
                               expression='snippet("very important", content)')]
    options = search.QueryOptions(cursor=cursor,
                                  sort_options=sort_options,
                                  returned_fields=returned_fields,
                                  snippeted_fields=snippeted_fields,
                                  returned_expressions=returned_expressions)
    self.assertEqual(cursor, options.cursor)
    self.assertEqual(sort_options, options.sort_options)
    self.assertEqual(returned_fields, options.returned_fields)
    self.assertEqual(snippeted_fields, options.snippeted_fields)
    self.assertEqual(returned_expressions, options.returned_expressions)

  def testUnicodeOut(self):
    returned_fields = ['subject', 'body']
    snippeted_fields = ['subject', 'body']
    options = search.QueryOptions(returned_fields=returned_fields,
                                  snippeted_fields=snippeted_fields)
    self.assertEqual(returned_fields, options.returned_fields)
    self.assertEqual(snippeted_fields, options.snippeted_fields)
    for returned_field in options.returned_fields:
      self.assertIsInstance(returned_field, six.text_type)
    for snippeted_field in options.snippeted_fields:
      self.assertIsInstance(snippeted_field, six.text_type)

  def testFullySpecifiedSortOptions(self):
    cursor = search.Cursor()
    sort_options = search.SortOptions(
        [search.SortExpression(expression='subject', default_value='ZZZZZ')])
    returned_fields = ['subject', 'body']
    snippeted_fields = ['subject', 'body']
    returned_expressions = [
        search.FieldExpression(name='content_snippet',
                               expression='snippet("very important", content)')]
    options = search.QueryOptions(cursor=cursor,
                                  sort_options=sort_options,
                                  returned_fields=returned_fields,
                                  snippeted_fields=snippeted_fields,
                                  returned_expressions=returned_expressions)
    self.assertEqual(cursor, options.cursor)
    self.assertEqual(sort_options, options.sort_options)
    self.assertEqual(returned_fields, options.returned_fields)
    self.assertEqual(snippeted_fields, options.snippeted_fields)
    self.assertEqual(returned_expressions, options.returned_expressions)

  def testWrongTypes(self):
    expr = search.SortExpression(expression='subject',
                                 default_value='ZZZZZ')
    self.assertRaises(TypeError, search.QueryOptions, sort_options=expr)
    self.assertRaises(TypeError, search.QueryOptions, sort_options=[expr])
    self.assertRaises(TypeError, search.QueryOptions,
                      sort_options=['sort by this'])

    sort_options = [search.MatchScorer()]
    self.assertRaises(TypeError, search.QueryOptions,
                      sort_options=sort_options)

  def testReturnedFieldsNone(self):
    self.assertEqual(
        [], search.QueryOptions(returned_fields=None).returned_fields)

  def testReturnedFieldsEmpty(self):
    self.assertEqual(
        [], search.QueryOptions(returned_fields=[]).returned_fields)

  def testReturnedFieldsOne(self):
    self.assertEqual(
        ['subject'],
        search.QueryOptions(returned_fields='subject').returned_fields)

  def testReturnedFieldsListOne(self):
    self.assertEqual(
        ['subject'],
        search.QueryOptions(returned_fields=['subject']).returned_fields)

  def testReturnedFieldsWrongValues(self):
    self.assertRaises(ValueError, search.QueryOptions, returned_fields='')
    self.assertRaises(ValueError, search.QueryOptions,
                      returned_fields=['field with spaces'])
    self.assertRaises(ValueError, search.QueryOptions,
                      returned_fields='_RESERVEDNAME')
    self.assertRaises(TypeError, search.QueryOptions, returned_fields=[1])

  def testReturnedFieldsFieldNameLength(self):
    name = 's' * search.MAXIMUM_FIELD_NAME_LENGTH
    self.assertEqual(
        [name], search.QueryOptions(returned_fields=name).returned_fields)
    self.assertRaises(ValueError, search.QueryOptions,
                      returned_fields=name + 's')

  def testReturnedExpressionsNone(self):
    self.assertEqual(
        [],
        search.QueryOptions(returned_expressions=None).returned_expressions)

  def testReturnedExpressionsEmpty(self):
    self.assertEqual(
        [],
        search.QueryOptions(returned_expressions=[]).returned_expressions)

  def testReturnedExpressionsNotExpression(self):
    self.assertRaises(AttributeError, search.QueryOptions,
                      returned_expressions=['not expr'])

  def testReturnedExpressionsDict(self):
    expressions = [dict(name='name', expression='expression')]
    self.assertRaises(AttributeError,
                      search.QueryOptions, returned_expressions=expressions)

  def testMaximumFieldNames(self):
    field_names = ['id_%d' % x for x in
                   range(search.MAXIMUM_FIELDS_RETURNED_PER_SEARCH)]
    self.assertEqual(
        field_names,
        search.QueryOptions(returned_fields=field_names).returned_fields)
    field_names.append('too_many')
    self.assertRaises(ValueError,
                      search.QueryOptions, returned_fields=field_names)

  def testMaximumExpressions(self):
    expressions = [
        search.FieldExpression(name='id_%d' % x, expression='a + b')
        for x in
        range(search.MAXIMUM_FIELDS_RETURNED_PER_SEARCH)]
    self.assertEqual(
        expressions,
        search.QueryOptions(
            returned_expressions=expressions).returned_expressions)
    expressions.append(search.FieldExpression(
        name='ab', expression='a + b'))
    self.assertRaises(ValueError,
                      search.QueryOptions, returned_expressions=expressions)

  def testCopyQueryOptionsToProtocolBufferOffset(self):
    options = search.QueryOptions(offset=33)
    params = search_service_pb2.SearchParams()
    search._CopyQueryOptionsObjectToProtocolBuffer(
        'very important', options, params)
    self.assertEqual(33, params.offset)

  def CheckCopyQueryOptionsToProtocolBuffer(self, cursor):
    sort_options = search.SortOptions(
        [search.SortExpression(expression='subject', default_value='ZZZZZ')])
    returned_fields = ['subject', 'body']
    snippeted_fields = ['subject', 'body']
    returned_expressions = [
        search.FieldExpression(name='content_snippet',
                               expression='snippet("very important", content)')]
    options = search.QueryOptions(limit=9,
                                  number_found_accuracy=100,
                                  cursor=cursor,
                                  sort_options=sort_options,
                                  returned_fields=returned_fields,
                                  snippeted_fields=snippeted_fields,
                                  returned_expressions=returned_expressions)

    params = search_service_pb2.SearchParams()
    search._CopyQueryOptionsObjectToProtocolBuffer(
        'very important', options, params)
    self.assertEqual(search_service_pb2.SearchParams.SINGLE,
                      params.cursor_type)
    self.assertEqual(9, params.limit)
    self.assertEqual(100, params.matched_count_accuracy)
    self.assertFalse(params.keys_only)
    self.assertLen(params.sort_spec, 1)
    sort_spec = params.sort_spec[0]
    self.assertEqual('subject', sort_spec.sort_expression)
    self.assertTrue(sort_spec.sort_descending)
    self.assertEqual('ZZZZZ', sort_spec.default_value_text)
    self.assertTrue(params.HasField('scorer_spec'))
    scorer_spec = params.scorer_spec
    self.assertTrue(scorer_spec.HasField('limit'))
    self.assertEqual(1000, scorer_spec.limit)
    field_spec = params.field_spec
    self.assertEqual(['subject', 'body'], field_spec.name)
    self.assertLen(field_spec.expression, 3)
    field_expression = field_spec.expression[0]
    self.assertEqual('subject', field_expression.name)
    self.assertEqual('snippet("very important", subject)',
                      field_expression.expression)
    field_expression = field_spec.expression[1]
    self.assertEqual('body', field_expression.name)
    self.assertEqual('snippet("very important", body)',
                      field_expression.expression)
    field_expression = field_spec.expression[2]
    self.assertEqual('content_snippet', field_expression.name)
    self.assertEqual('snippet("very important", content)',
                      field_expression.expression)

  def testCopyQueryOptionsToProtocolBuffer(self):
    self.CheckCopyQueryOptionsToProtocolBuffer(search.Cursor())

  def CheckCopyQueryOptionsToProtocolBufferSortOptions(self, cursor):
    sort_options = search.SortOptions(
        [search.SortExpression(expression='subject', default_value='ZZZZZ')])
    returned_fields = ['subject', 'body']
    snippeted_fields = ['subject', 'body']
    returned_expressions = [
        search.FieldExpression(name='content_snippet',
                               expression='snippet("very important", content)')]
    options = search.QueryOptions(limit=9,
                                  number_found_accuracy=100,
                                  cursor=cursor,
                                  sort_options=sort_options,
                                  returned_fields=returned_fields,
                                  snippeted_fields=snippeted_fields,
                                  returned_expressions=returned_expressions)

    params = search_service_pb2.SearchParams()
    search._CopyQueryOptionsObjectToProtocolBuffer(
        'very important', options, params)
    self.assertEqual(search_service_pb2.SearchParams.SINGLE,
                      params.cursor_type)
    self.assertEqual(9, params.limit)
    self.assertEqual(100, params.matched_count_accuracy)
    self.assertFalse(params.keys_only)
    self.assertLen(params.sort_spec, 1)
    sort_spec = params.sort_spec[0]
    self.assertEqual('subject', sort_spec.sort_expression)
    self.assertTrue(sort_spec.sort_descending)
    self.assertEqual('ZZZZZ', sort_spec.default_value_text)
    self.assertTrue(params.HasField('scorer_spec'))

    scorer_spec = params.scorer_spec
    self.assertFalse(scorer_spec.HasField('scorer'))
    self.assertEqual(1000, scorer_spec.limit)
    field_spec = params.field_spec
    self.assertEqual(['subject', 'body'], field_spec.name)
    self.assertLen(field_spec.expression, 3)
    field_expression = field_spec.expression[0]
    self.assertEqual('subject', field_expression.name)
    self.assertEqual('snippet("very important", subject)',
                      field_expression.expression)
    field_expression = field_spec.expression[1]
    self.assertEqual('body', field_expression.name)
    self.assertEqual('snippet("very important", body)',
                      field_expression.expression)
    field_expression = field_spec.expression[2]
    self.assertEqual('content_snippet', field_expression.name)
    self.assertEqual('snippet("very important", content)',
                      field_expression.expression)

  def CheckCopyQueryOptionsToProtocolBufferSortOptionsUnicode(self, cursor):
    sort_options = search.SortOptions(
        [search.SortExpression(expression=_UNICODE_STRING,
                               default_value=_UNICODE_STRING)])
    returned_fields = ['subject', 'body']
    snippeted_fields = ['subject', 'body']
    content_snippet = 'snippet("' + _UNICODE_QUERY_ESCAPED + '", content)'
    returned_expressions = [
        search.FieldExpression(name='content_snippet',
                               expression=content_snippet)]
    options = search.QueryOptions(limit=9,
                                  cursor=cursor,
                                  sort_options=sort_options,
                                  returned_fields=returned_fields,
                                  snippeted_fields=snippeted_fields,
                                  returned_expressions=returned_expressions)

    params = search_service_pb2.SearchParams()
    search._CopyQueryOptionsObjectToProtocolBuffer(
        _UNICODE_QUERY, options, params)
    self.assertEqual(search_service_pb2.SearchParams.SINGLE,
                      params.cursor_type)
    self.assertEqual(9, params.limit)
    self.assertEqual(100, params.matched_count_accuracy)
    self.assertFalse(params.keys_only)
    self.assertLen(params.sort_spec, 1)
    sort_spec = params.sort_spec[0]
    self.assertEqual('subject', sort_spec.sort_expression)
    self.assertTrue(sort_spec.sort_descending)
    self.assertEqual('ZZZZZ', sort_spec.default_value_text)
    self.assertTrue(params.HasField('scorer_spec'))

    scorer_spec = params.scorer_spec
    self.assertFalse(scorer_spec.HasField('scorer'))
    self.assertEqual(1000, scorer_spec.limit)
    field_spec = params.field_spec
    self.assertEqual(['subject', 'body'], field_spec.name)
    self.assertLen(field_spec.expression, 3)
    field_expression = field_spec.expression[0]
    self.assertEqual('subject', field_expression.name)
    subject_snippet = 'snippet("' + _UNICODE_QUERY_ESCAPED + '", subject)'
    self.assertEqual(
        subject_snippet.encode('utf-8'), field_expression.expression)
    field_expression = field_spec.expression[1]
    self.assertEqual('body', field_expression.name)
    body_snippet = 'snippet("' + _UNICODE_QUERY_ESCAPED + '", body)'
    self.assertEqual(body_snippet.encode('utf-8'), field_expression.expression)
    field_expression = field_spec.expression[2]
    self.assertEqual('content_snippet', field_expression.name)
    self.assertEqual(
        content_snippet.encode('utf-8'), field_expression.expression)

  def testCopyQueryOptionsToProtocolBufferSortOptions(self):
    self.CheckCopyQueryOptionsToProtocolBufferSortOptions(search.Cursor())

  def testCopyQueryOptionsToProtocolBufferCursorFromPreviousSearch(self):
    cursor = search.Cursor(web_safe_string='False:internal_part')
    options = search.QueryOptions(cursor=cursor)
    self.assertEqual('internal_part', cursor._internal_cursor)
    params_pb = search_service_pb2.SearchParams()
    search._CopyQueryOptionsObjectToProtocolBuffer(
        'some query', options, params_pb)
    self.assertEqual('internal_part', params_pb.cursor)

  def testRepr(self):
    self.assertEqual(
        'search.QueryOptions(limit=20, '
        'number_found_accuracy=100, ids_only=True)',
        repr(search.QueryOptions(ids_only=True,
                                 number_found_accuracy=100)))
    self.assertEqual(
        'search.QueryOptions(limit=20, ids_only=True)',
        repr(search.QueryOptions(ids_only=True)))


class QueryTest(absltest.TestCase):

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.Query, foo='bar')

  def QueryIsParseable(self, query):
    options = search.QueryOptions(number_found_accuracy=100)
    search.Query(query_string=query, options=options)

  def testParseQuerySimple(self):
    self.QueryIsParseable('ok')

  def testParseQueryComplex(self):
    self.QueryIsParseable('to be or not to be')

  def testParseQueryComplexSequence(self):
    self.QueryIsParseable('"to be" or "not to" be')

  def testParseQueryComplexRestricts(self):
    self.QueryIsParseable('to:be OR NOT to:be')


  def testParseQueryComplexBoolean(self):
    self.QueryIsParseable(
        '(p4347646e:7361756e612062656e636820626f617264) AND '
        '(p41753547:31383030 OR p41753547:5f5f414c4c5f5f) AND '
        '(p42333248:6669 '
        'OR p42333248:6c696e6b2d61637776746234303033) AND '
        '(p41745671:3432) AND '
        '(p494c3368:5f6f74686572) AND (p507a7377:3134) AND '
        '(p574e4f55:333130) '
        'AND (p47385867:3630) AND '
        '(p3a6367:62726f6b656e2c20696e2062616420636f6e646974'
        '696f6e206f7220696e636f6d706c657465) '
        'AND (p3a64767279:6350424a) AND '
        '(p3a7374617465:7075626c6963) AND '
        '(p3a74797065:6f66666572)')
    self.QueryIsParseable(
        '(p4347646e: '
        '62726f6b656e2c20696e2062616420636f6e646974696f6e206f7220696e63'
        '6f6d706c657465'
        ' OR p4347646e:5f5f414c4c5f5f) AND (p41753547:3630 OR'
        ' p41753547:5f5f414c4c5f5f)'
        ' AND (p42333248:333130 OR'
        ' p42333248:5f5f414c4c5f5f) AND (p41745671:3134 OR'
        ' p41745671:5f5f414c4c5f5f)'
        ' AND (p494c3368:5f6f74686572 OR'
        '     p494c3368:5f5f414c4c5f5f) AND'
        ' (p507a7377:3432 OR'
        ' p507a7377:5f5f414c4c5f5f) AND'
        ' (p574e4f55:7361756e612062656e636820626f617264 OR'
        ' p574e4f55:5f5f414c4c5f5f) AND'
        ' (p47385867:31383030 OR'
        ' p47385867:5f5f414c4c5f5f) AND (p3a6367:6350424a)'
        ' AND (p3a64767279:6669'
        ' OR p3a64767279:6c696e6b2d61637776746234303033)'
        ' AND (p3a7374617465:7075626c6963) AND'
        ' (p3a74797065:6f66666572)')

  def testParseQueryUnfinished(self):
    try:
      search.Query(query_string='be NOT')
    except search.QueryError as e:
      self.assertEqual(u'Failed to parse query "be NOT"', str(e))

  def testUnicodeOut(self):
    query = search.Query(query_string='query')
    self.assertEqual('query', query.query_string)
    self.assertIsInstance(query.query_string, six.text_type)

  def testQueryTooLong(self):
    query = 'q' * search.MAXIMUM_QUERY_LENGTH
    self.assertEqual(query, search.Query(query_string=query).query_string)
    self.assertRaises(ValueError, search.Query, query_string=query + 'q')

  def testQueryWrongType(self):
    for value in _NON_STRING_VALUES:
      self.assertRaises(TypeError, search.Query, query_string=value)

  def testQueryEmpty(self):
    self.assertEqual('', search.Query(query_string='').query_string)

  def testQuerySpace(self):
    self.assertEqual(' ', search.Query(query_string=' ').query_string)

  def testQueryUnicode(self):
    for query in [u'\xe4-', u'\xe4-a', u'a-\xe4', u'a-r\xe4u',
                  u'MUC-ALT-3-Hofbr\xe4uhaus', u'#Habl\xE9', u'$USER',
                  u'$téphane', '']:
      search.Query(query_string=query)

    search._CheckQuery(u'Hofbr\xe4uhaus')
    search._CheckQuery(u'-\xe4')
    search._CheckQuery('a-')
    search._CheckQuery('a-a')
    search._CheckQuery(u'MUC-ALT')
    search._CheckQuery(u'MUC-ALT-3')
    search._CheckQuery(u'MUC-ALT-3-Hofbr')

    search._CheckQuery(u'#Habl\xE9')
    search._CheckQuery(u'$USER')
    search._CheckQuery(u'$téphane')

    search._CheckQuery(u'\u3042\u3042\u3042\uff11\uff12\uff13')
    search._CheckQuery(_UNICODE_STRING)
    search._CheckQuery(_UNICODE_QUERY)
    self.assertEqual(_UNICODE_STRING,
                      search.Query(query_string=_UNICODE_STRING).query_string)
    self.assertEqual(_UNICODE_QUERY,
                      search.Query(query_string=_UNICODE_QUERY).query_string)

  def testSearchNullQuery(self):
    self.assertRaises(TypeError, search.Query, None)

  def testRequiredArgumentsMissing(self):
    self.assertRaises(TypeError, search.Query)
    options = search.QueryOptions()
    self.assertRaises(TypeError, search.Query, options=options)

  def testUnicodeQueryWithSnippetingCopyToProtocolBuffer(self):
    query = search.Query(
        query_string=_UNICODE_QUERY,
        options=search.QueryOptions(snippeted_fields=['subject', 'body']))
    params = search_service_pb2.SearchParams()
    search._CopyQueryObjectToProtocolBuffer(query, params)
    self.assertEqual(_UNICODE_QUERY, params.query)
    field_spec = params.field_spec
    self.assertEqual(2, len(field_spec.expression))
    expr = field_spec.expression[0]
    self.assertEqual('subject', expr.name)
    subject_snippet = u'snippet("' + _UNICODE_QUERY_ESCAPED + u'", subject)'
    self.assertEqual(subject_snippet, expr.expression)
    expr = field_spec.expression[1]
    self.assertEqual('body', expr.name)
    body_snippet = u'snippet("' + _UNICODE_QUERY_ESCAPED + u'", body)'
    self.assertEqual(body_snippet, expr.expression)


class APIFunctionTest(TestCase):

  DOCUMENT1 = search.Document(
      doc_id='doc99',
      fields=[search.TextField(name='subject', value='some text')])
  DOCUMENT2 = search.Document(
      doc_id='doc88',
      fields=[search.TextField(name='subject', value='some other text')])
  DOCUMENT3 = search.Document(
      doc_id='doc77',
      fields=[search.TextField(name='subject', value='Let P(x)=~(x∈ x)')])

  DOCUMENT4 = search.Document(
      doc_id='doc66',
      facets=[search.AtomFacet(name='genre', value='sci-fi')])

  DOCUMENT5 = search.Document(
      doc_id='doc55',
      facets=[search.NumberFacet(name='rating', value=2.5)])

  def setUp(self):
    self.mox = mox.Mox()
    self.mox.StubOutClassWithMocks(apiproxy_stub_map, 'UserRPC')

  def tearDown(self):
    namespace_manager.set_namespace('')
    self.mox.UnsetStubs()
    self.mox.ResetAll()

  def testUnicodeOut(self):
    index = search.Index(name='index', namespace='')
    self.assertEqual('index', index.name)
    self.assertEqual('', index.namespace)
    self.assertIsInstance(index.name, six.text_type)
    self.assertIsInstance(index.namespace, six.text_type)

    index = search.Index(name='index', namespace='ns')
    self.assertEqual('index', index.name)
    self.assertEqual('ns', index.namespace)
    self.assertIsInstance(index.name, six.text_type)
    self.assertIsInstance(index.namespace, six.text_type)

    namespace_manager.set_namespace('ns_from_manager')
    index = search.Index(name='index', namespace=None)
    self.assertEqual('index', index.name)
    self.assertEqual('ns_from_manager', index.namespace)
    self.assertIsInstance(index.name, six.text_type)
    self.assertIsInstance(index.namespace, six.text_type)

    namespace_manager.set_namespace('')
    index = search.Index(name='index', namespace=None)
    self.assertEqual('index', index.name)
    self.assertEqual('', index.namespace)
    self.assertIsInstance(index.name, six.text_type)
    self.assertIsInstance(index.namespace, six.text_type)

  def testSource(self):
    index = search.Index(name='index', namespace='ns')
    self.assertEqual('index', index.name)
    self.assertEqual('ns', index.namespace)
    self.assertEqual(search.Index.SEARCH, index.source)

    spec_pb = search_service_pb2.IndexSpec()
    search._CopyMetadataToProtocolBuffer(index, spec_pb)
    self.assertEqual('index', spec_pb.name)
    self.assertEqual('ns', spec_pb.namespace)
    self.assertFalse(spec_pb.HasField('source'))

    index = search.Index(name='index', namespace='ns',
                         source=search.Index.SEARCH)
    self.assertEqual('index', index.name)
    self.assertEqual('ns', index.namespace)
    self.assertEqual(search.Index.SEARCH, index.source)
    self.assertIsInstance(index.name, six.text_type)
    self.assertIsInstance(index.namespace, six.text_type)

    spec_pb = search_service_pb2.IndexSpec()
    search._CopyMetadataToProtocolBuffer(index, spec_pb)
    self.assertEqual('index', spec_pb.name)
    self.assertEqual('ns', spec_pb.namespace)
    self.assertFalse(spec_pb.HasField('source'))

    index = search._NewIndexFromIndexSpecPb(spec_pb)
    self.assertEqual('index', index.name)
    self.assertEqual('ns', index.namespace)
    self.assertEqual(search.Index.SEARCH, index.source)

    index = search.Index(name='index', namespace='ns',
                         source=search.Index.CLOUD_STORAGE)

    self.assertEqual(search.Index.CLOUD_STORAGE, index.source)

    spec_pb = search_service_pb2.IndexSpec()
    search._CopyMetadataToProtocolBuffer(index, spec_pb)
    self.assertEqual('index', spec_pb.name)
    self.assertEqual('ns', spec_pb.namespace)
    self.assertEqual(search_service_pb2.IndexSpec.CLOUD_STORAGE,
                      spec_pb.source)

    index = search._NewIndexFromIndexSpecPb(spec_pb)
    self.assertEqual('index', index.name)
    self.assertEqual('ns', index.namespace)
    self.assertEqual(search.Index.CLOUD_STORAGE, index.source)

  def testMinimalMetadata(self):
    index = search.Index(name='index_name')
    self.assertEqual('index_name', index.name)

  def testIndexName(self):
    for string in _LOWER_NON_VISIBLE_PRINTABLE_ASCII:
      self.assertRaises(ValueError, search.Index, name=string)
    self.assertEqual(_VISIBLE_PRINTABLE_ASCII,
                      search.Index(name=_VISIBLE_PRINTABLE_ASCII).name)
    self.assertEqual(_VISIBLE_PRINTABLE_ASCII_UNICODE,
                      search.Index(name=_VISIBLE_PRINTABLE_ASCII_UNICODE).name)
    self.assertRaises(ValueError, search.Index, name='!')
    for string in _UPPER_NON_VISIBLE_PRINTABLE_ASCII:
      self.assertRaises(ValueError, search.Index, name=string)

  def testEquals(self):
    a = search.Index(name='index_name')
    b = search.Index(name='index_name')
    self.assertEqual(a, b)
    self.assertEqual(hash(a), hash(b))

  def testUnknownArgs(self):
    self.assertRaises(TypeError, search.Index, foo='bar')

  def testRepr(self):
    self.assertReprEqual(
        "search.Index(name=u'index_name', "
        "namespace=u'', source='SEARCH')",
        repr(search.Index(name='index_name')))

  def CallWithException(self,
                        service,
                        method,
                        request,
                        response,
                        exception,
                        deadline=None):
    makeTestSyncCall(service, method, request, response,
                     deadline).AndRaise(exception)
    self.mox.ReplayAll()

  def CallWithError(self,
                    service,
                    method,
                    request,
                    response,
                    error,
                    message,
                    deadline=None):
    self.CallWithException(service, method, request, response,
                           apiproxy_errors.ApplicationError(error, message),
                           deadline)

  def ExpectDeleteSchemaError(self, error, message):
    self.CallWithError('search', 'DeleteSchema',
                       mox.IsA(search_service_pb2.DeleteSchemaRequest),
                       mox.IsA(search_service_pb2.DeleteSchemaResponse), error,
                       message)

  def ExpectRemoveError(self, error, message):
    self.CallWithError('search', 'DeleteDocument',
                       mox.IsA(search_service_pb2.DeleteDocumentRequest),
                       mox.IsA(search_service_pb2.DeleteDocumentResponse),
                       error, message)

  def ExpectAddError(self, error, message):
    self.CallWithError('search', 'IndexDocument',
                       mox.IsA(search_service_pb2.IndexDocumentRequest),
                       mox.IsA(search_service_pb2.IndexDocumentResponse), error,
                       message)

  def ExpectAddOverQuotaError(self):
    self.CallWithException('search', 'IndexDocument',
                           mox.IsA(search_service_pb2.IndexDocumentRequest),
                           mox.IsA(search_service_pb2.IndexDocumentResponse),
                           apiproxy_errors.OverQuotaError('denied'))

  def ExpectSearchError(self, error, message):
    self.CallWithError('search', 'Search',
                       mox.IsA(search_service_pb2.SearchRequest),
                       mox.IsA(search_service_pb2.SearchResponse), error,
                       message)

  def ExpectListIndexesError(self, error, message):
    self.CallWithError('search', 'ListIndexes',
                       mox.IsA(search_service_pb2.ListIndexesRequest),
                       mox.IsA(search_service_pb2.ListIndexesResponse), error,
                       message)

  def ExpectListIndexesResponse(self, code, index_names, message=None,
                                request=None, field_map=None, limit=20,
                                fetch_schema=False, offset=None, deadline=None,
                                storage_map=None, namespace_list=None,
                                all_namespaces=None):
    if request is None:
      request = search_service_pb2.ListIndexesRequest()
      params = request.params
      params.namespace = ''
      params.include_start_index = True
      if offset:
        params.offset = offset
      params.limit = limit
      params.fetch_schema = fetch_schema
      if all_namespaces is not None:
        params.all_namespaces = all_namespaces

    def ResponseSideEffects(service, method, request, response):
      response_status = response.status
      response_status.code = code
      if message is not None:
        response_status.error_detail = message
      for i, index_name in enumerate(index_names):
        metadata = response.index_metadata.add()
        metadata.index_spec.name = index_name
        if namespace_list:
          metadata.index_spec.namespace = namespace_list[i]
        if field_map:
          fields = field_map[index_name]
          for field in fields:
            field_pb = metadata.field.add()
            field_pb.name = field.name
            for field_type in field.type:
              field_pb.type.append(field_type)
        if storage_map and index_name in storage_map:
          dest = metadata.storage
          dest.amount_used = storage_map[index_name]
          dest.limit = _MAX_STORAGE

    makeTestSyncCall('search', 'ListIndexes', request,
                     mox.IsA(search_service_pb2.ListIndexesResponse), deadline,
                     ResponseSideEffects)

    self.mox.ReplayAll()

  def ExpectListDocumentsError(self, error, message, deadline=None):
    self.CallWithError(
        'search',
        'ListDocuments',
        mox.IsA(search_service_pb2.ListDocumentsRequest),
        mox.IsA(search_service_pb2.ListDocumentsResponse),
        error,
        message,
        deadline=deadline)

  def ExpectListResponse(self, code, documents, limit=100,
                         start_doc_id=None, include_start_doc=True,
                         ids_only=False, message=None, deadline=None):
    request = search_service_pb2.ListDocumentsRequest()


    params = request.params
    params.limit = limit
    params.include_start_doc = include_start_doc
    if start_doc_id is not None:
      params.start_doc_id = start_doc_id
    params.keys_only = ids_only

    index = params.index_spec
    index.name = self.GetIndex().name
    index.namespace = self.GetIndex().namespace

    def ResponseSideEffects(service, method, request, response):
      response_status = response.status
      response_status.code = code
      if message is not None:
        response_status.error_detail = message
      for doc in documents:
        document = response.document.add()
        document.id = doc.doc_id
        for f in doc.fields:
          field = document.field.add()
          field.name = f.name
          value = field.value
          value.string_value = f.value

    makeTestSyncCall('search', 'ListDocuments', EqualsProto(request),
                     mox.IsA(search_service_pb2.ListDocumentsResponse),
                     deadline, ResponseSideEffects)

    self.mox.ReplayAll()

  def SetIndexSpec(self, name, namespace, index_spec):
    index_spec.name = name
    index_spec.namespace = namespace

  def ExpectDeleteSchemaResponse(self, index_name, codes, deadline=None):
    self.ExpectDeleteSchemaResponseNamespace('', index_name, codes,
                                             deadline=deadline)

  def ExpectDeleteSchemaResponseNamespace(self, namespace, index_name, codes,
                                          deadline=None):
    request = search_service_pb2.DeleteSchemaRequest()
    params = request.params
    self.SetIndexSpec(index_name, namespace, params.index_spec.add())

    def ResponseSideEffects(service, method, request, response):
      for code in codes:
        if isinstance(code, tuple):
          status = response.status.add()
          status.code = code[0]
          status.error_detail = code[1]
        else:
          response.status.add().code = code

    makeTestSyncCall('search', 'DeleteSchema', request,
                     mox.IsA(search_service_pb2.DeleteSchemaResponse), deadline,
                     ResponseSideEffects)
    self.mox.ReplayAll()

  def ExpectRemoveResponse(self, doc_ids, codes, deadline=None):
    self.ExpectRemoveResponseNamespace('', doc_ids, codes, deadline=deadline)

  def ExpectRemoveResponseNamespace(self, namespace, doc_ids, codes,
                                    deadline=None):
    request = search_service_pb2.DeleteDocumentRequest()
    params = request.params
    self.SetIndexSpec('index-name-999', namespace, params.index_spec)
    for doc_id in doc_ids:
      params.doc_id.append(doc_id)

    def ResponseSideEffects(service, method, request, response):
      for code in codes:
        if isinstance(code, tuple):
          status = response.status.add()
          status.code = code[0]
          status.error_detail = code[1]
        else:
          response.status.add().code = code

    makeTestSyncCall('search', 'DeleteDocument', request,
                     mox.IsA(search_service_pb2.DeleteDocumentResponse),
                     deadline, ResponseSideEffects)
    self.mox.ReplayAll()

  def testNewSearchResultsFromProtocolBuffer(self):
    response_pb = search_service_pb2.SearchResponse()
    response_pb.cursor = u'cursor\xe7'.encode('utf-8')
    status_pb = response_pb.status
    status_pb.code = OK
    status_pb.error_detail = 'error'
    response_pb.matched_count = 123
    result_pb = response_pb.result.add()
    doc_pb = result_pb.document
    doc_pb.id = 'doc_id'
    doc_pb.language = 'fr'
    expression_pb = result_pb.expression.add()
    expression_pb.name = 'name'
    expression_value_pb = expression_pb.value
    expression_value_pb.string_value = u'content\xe7'.encode('utf-8')
    expression_value_pb.language = 'de'
    result_pb.score.append(0.123)
    facet_result_pb = response_pb.facet_result.add()
    facet_result_pb.name = 'genre'
    facet_value_pb = facet_result_pb.value.add()
    facet_value_pb.name = 'sci-fi'
    facet_value_pb.count = 11
    facet_refinement_pb = facet_value_pb.refinement
    facet_refinement_pb.name = 'genre'
    facet_refinement_pb.value = 'sci-fi'
    facet_value_pb = facet_result_pb.value.add()
    facet_value_pb.name = 'action'
    facet_value_pb.count = 8
    facet_refinement_pb = facet_value_pb.refinement
    facet_refinement_pb.name = 'genre'
    facet_refinement_pb.value = 'action'
    facet_result_pb = response_pb.facet_result.add()
    facet_result_pb.name = 'rating'

    facet_value_pb = facet_result_pb.value.add()
    facet_value_pb.name = 'good'
    facet_value_pb.count = 16
    facet_refinement_pb = facet_value_pb.refinement
    facet_refinement_pb.name = 'rating'
    facet_ref_range_pb = facet_refinement_pb.range
    facet_ref_range_pb.start = str(3.0)
    facet_ref_range_pb.ClearField('end')

    facet_value_pb = facet_result_pb.value.add()
    facet_value_pb.name = 'average'
    facet_value_pb.count = 3
    facet_refinement_pb = facet_value_pb.refinement
    facet_refinement_pb.name = 'rating'
    facet_ref_range_pb = facet_refinement_pb.range
    facet_ref_range_pb.start = str(2.0)
    facet_ref_range_pb.end = str(3.0)

    facet_value_pb = facet_result_pb.value.add()
    facet_value_pb.name = 'bad'
    facet_value_pb.count = 4
    facet_refinement_pb = facet_value_pb.refinement
    facet_refinement_pb.name = 'rating'
    facet_ref_range_pb = facet_refinement_pb.range
    facet_ref_range_pb.end = str(2.0)
    facet_ref_range_pb.ClearField('start')


    results = search.Index(name='name')._NewSearchResults(
        response_pb, search.Cursor())

    self.assertEqual(123, results.number_found)
    cursor = results.cursor
    self.assertFalse(cursor.per_result)
    self.assertEqual(u'False:cursor\xe7', cursor.web_safe_string)
    self.assertIsInstance(cursor.web_safe_string, six.text_type)
    self.assertEqual(1, len(results.results))
    result = results.results[0]
    self.assertEqual('doc_id', result.doc_id)
    self.assertIsInstance(result.doc_id, six.text_type)
    self.assertEqual(0, len(result.fields))
    self.assertEqual('fr', result.language)
    self.assertIsInstance(result.language, six.text_type)
    self.assertEqual([0.123], result.sort_scores)
    self.assertEqual(1, len(result.expressions))
    expression = result.expressions[0]
    self.assertEqual('name', expression.name)
    self.assertIsInstance(expression.name, six.text_type)
    self.assertEqual(u'content\xe7', expression.value)
    self.assertIsInstance(expression.value, six.text_type)
    self.assertEqual('de', expression.language)
    self.assertIsInstance(expression.language, six.text_type)
    facets = results.facets
    self.assertEqual(2, len(facets))
    facet = facets[0]
    self.assertEqual('genre', facet.name)
    self.assertEqual(2, len(facet.values))
    self.assertEqual('sci-fi', facet.values[0].label)
    self.assertEqual(11, facet.values[0].count)
    self.assertEqual('action', facet.values[1].label)
    self.assertEqual(8, facet.values[1].count)
    facet = facets[1]
    self.assertEqual('rating', facet.name)
    self.assertEqual(3, len(facet.values))
    self.assertEqual('good', facet.values[0].label)
    self.assertEqual(16, facet.values[0].count)
    refinement = search.FacetRefinement.FromTokenString(
        facet.values[0].refinement_token)
    self.assertEqual('rating', refinement.name)
    self.assertEqual(3.0, refinement.facet_range.start)
    self.assertEqual(None, refinement.facet_range.end)
    self.assertEqual('average', facet.values[1].label)
    self.assertEqual(3, facet.values[1].count)
    refinement = search.FacetRefinement.FromTokenString(
        facet.values[1].refinement_token)
    self.assertEqual('rating', refinement.name)
    self.assertEqual(2.0, refinement.facet_range.start)
    self.assertEqual(3.0, refinement.facet_range.end)
    self.assertEqual('bad', facet.values[2].label)
    self.assertEqual(4, facet.values[2].count)
    refinement = search.FacetRefinement.FromTokenString(
        facet.values[2].refinement_token)
    self.assertEqual('rating', refinement.name)
    self.assertEqual(None, refinement.facet_range.start)
    self.assertEqual(2.0, refinement.facet_range.end)


  def testGetResponseRepr(self):
    self.assertReprEqual(
        "search.GetResponse(results=[search.ScoredDocument(doc_id=u'doc_id', "
        "language=u'en', rank=123)])",
        repr(search.GetResponse(
            results=[search.ScoredDocument(doc_id='doc_id', rank=123)])))

  def testGetResponseFromProtocolBuffer(self):
    response_pb = search_service_pb2.ListDocumentsResponse()
    status_pb = response_pb.status
    status_pb.code = OK
    status_pb.error_detail = 'error'
    doc_pb = response_pb.document.add()
    doc_pb.id = 'doc_id'
    doc_pb.language = 'fr'

    response = search.Index(name='name')._NewGetResponse(response_pb)

    self.assertEqual(1, len(response.results))
    result = response.results[0]
    self.assertEqual('doc_id', result.doc_id)
    self.assertEqual('fr', result.language)
    self.assertIsInstance(result.doc_id, six.text_type)
    self.assertIsInstance(result.language, six.text_type)

  def testNewSchemaFromProtocolBuffer(self):
    field_types_pb = document_pb2.FieldTypes()
    field_types_pb.name = 'name'
    field_types_pb.type.append(document_pb2.FieldValue.HTML)
    field_types_pb.type.append(document_pb2.FieldValue.ATOM)
    field_types_pb_list = [field_types_pb]

    schema = search._NewSchemaFromPb(field_types_pb_list)

    self.assertEqual(1, len(schema))
    for key in schema:
      self.assertIsInstance(key, six.text_type)
    self.assertEqual([search.Field.HTML, search.Field.ATOM], schema['name'])

  def testGetResponseIndexRepr(self):
    self.assertReprEqual(
        "search.GetResponse(results=[search.Index(name=u'name', "
        "namespace=u'', source='SEARCH')])",
        repr(search.GetResponse(results=[search.Index(name='name')])))

  def testGetResponseIter(self):
    for index in search.GetResponse(results=[search.Index(name='foo')]):
      self.assertEqual('foo', index.name)
      self.assertEqual('', index.namespace)

  def testGetResponseIsZero(self):
    response = search.GetResponse(results=[])
    self.assertFalse(response)

  def testGetResponseIsNotZero(self):
    response = search.GetResponse(results=[search.Index(name='foo')])
    self.assertTrue(response)

  def testGetResponseLen(self):
    response = search.GetResponse(results=[search.Index(name='foo')])
    self.assertEqual(1, len(response))

  def testGetResponseGetItem(self):
    response = search.GetResponse(
        results=[search.Index(name='foo'), search.Index(name='bar')])
    self.assertEqual('foo', response[0].name)
    self.assertEqual('bar', response[1].name)

  def testGetResponseFromProtocolBufferIndexes(self):
    response_pb = search_service_pb2.ListIndexesResponse()
    status_pb = response_pb.status
    status_pb.code = OK
    status_pb.error_detail = 'error'
    index_pb = response_pb.index_metadata.add()
    spec_pb = index_pb.index_spec
    spec_pb.name = 'index_name'
    spec_pb.namespace = 'ns'
    field_types_pb = index_pb.field.add()
    field_types_pb.name = 'field_name'
    field_types_pb.type.append(document_pb2.FieldValue.HTML)

    response = search._ListIndexesResponsePbToGetResponse(
        response_pb, include_schema=True)

    self.assertEqual(1, len(response.results))
    index = response.results[0]
    self.assertEqual('index_name', index.name)
    self.assertIsInstance(index.name, six.text_type)
    self.assertEqual('ns', index.namespace)
    self.assertIsInstance(index.namespace, six.text_type)
    schema = index.schema
    self.assertEqual(1, len(schema))
    for key in schema:
      self.assertIsInstance(key, six.text_type)
    self.assertEqual([search.Field.HTML], schema['field_name'])

    response_pb = search_service_pb2.ListIndexesResponse()
    status_pb = response_pb.status
    status_pb.code = OK
    status_pb.error_detail = 'error'
    index_pb = response_pb.index_metadata.add()
    spec_pb = index_pb.index_spec
    spec_pb.name = 'index_name'
    spec_pb.namespace = 'ns'
    response = search._ListIndexesResponsePbToGetResponse(
        response_pb, include_schema=True)
    index = response.results[0]
    schema = index.schema
    self.assertIsNot(schema, None)
    self.assertEqual(0, len(schema))

    response_pb = search_service_pb2.ListIndexesResponse()
    status_pb = response_pb.status
    status_pb.code = OK
    status_pb.error_detail = 'error'
    index_pb = response_pb.index_metadata.add()
    spec_pb = index_pb.index_spec
    spec_pb.name = 'index_name'
    spec_pb.namespace = 'ns'
    response = search._ListIndexesResponsePbToGetResponse(
        response_pb, include_schema=False)
    index = response.results[0]
    schema = index.schema
    self.assertIs(schema, None)

  def ExpectAddResponse(self, docs, codes, ids=None, deadline=None):
    self.ExpectAddResponseNamespace('', docs, codes, ids=ids, deadline=deadline)

  def ExpectAddResponseNamespace(self, namespace, docs, codes, ids=None,
                                 deadline=None):
    request = search_service_pb2.IndexDocumentRequest()
    params = request.params
    self.SetIndexSpec('index-name-999', namespace, params.index_spec)
    for doc in docs:
      doc_pb = params.document.add()
      search._CopyDocumentToProtocolBuffer(doc, doc_pb)

    def ResponseSideEffects(service, method, request, response):
      for code in codes:
        if isinstance(code, tuple):
          status = response.status.add()
          status.code = code[0]
          status.error_detail = code[1]
        else:
          response.status.add().code = code
      id_position = 0
      for doc in docs:
        if doc.doc_id:
          response.doc_id.append(doc.doc_id)
        else:
          response.doc_id.append(ids[id_position])
          id_position += 1

    makeTestSyncCall('search', 'IndexDocument', request,
                     mox.IsA(search_service_pb2.IndexDocumentResponse),
                     deadline, ResponseSideEffects)

    self.mox.ReplayAll()

  def ExpectSearchResponse(
      self, query, returned_fields=None, returned_expressions=None,
      offset=None, limit=None,
      number_found_accuracy=None, cursor=None,
      cursor_type=None,
      scorer=None, documents=None, code=OK, response_cursor=None,
      document_cursors=None, ids_only=None, sort_specs=None,
      deadline=None, replay=True, facets=None):
    self.ExpectSearchResponseNamespace(
        namespace='',
        query=query,
        returned_fields=returned_fields,
        returned_expressions=returned_expressions,
        offset=offset,
        limit=limit,
        number_found_accuracy=number_found_accuracy,
        cursor=cursor,
        cursor_type=cursor_type,
        scorer=scorer,
        documents=documents,
        code=code,
        response_cursor=response_cursor,
        document_cursors=document_cursors,
        ids_only=ids_only,
        sort_specs=sort_specs,
        deadline=deadline,
        replay=replay,
        facets=facets)

  def ExpectSearchResponseNamespace(
      self, namespace, query, returned_fields=None, returned_expressions=None,
      offset=None, limit=None, number_found_accuracy=None, cursor=None,
      cursor_type=None,
      scorer=None, documents=None, code=OK, response_cursor=None,
      document_cursors=None, ids_only=None, sort_specs=None, deadline=None,
      replay=True, facets=None):
    request = search_service_pb2.SearchRequest()
    params = request.params
    self.SetIndexSpec('index-name-999', namespace, params.index_spec)
    params.query = query
    field_spec = None
    if returned_fields:
      field_spec = params.field_spec
      for name in returned_fields:
        field_spec.name.add(name)
    if returned_expressions:
      if not field_spec:
        field_spec = params.field_spec
      for expression in returned_expressions:
        expr_pb = field_spec.expression.add()
        expr_pb.name = expression.name
        expr_pb.expression = expression.expression

    if scorer is not None:
      scorer_spec = params.scorer_spec
      scorer_spec.scorer = scorer
      scorer_spec.limit = 1000
    if sort_specs is not None:
      for sort_spec in sort_specs:
        sort_spec_pb = params.sort_spec.add()
        sort_spec_pb.sort_expression = sort_spec[0]
        if sort_spec[1] is not None and not sort_spec[1]:
          sort_spec_pb.sort_descending = False
        if sort_spec[2] is not None:
          sort_spec_pb.default_value_text = sort_spec[2]
        elif sort_spec[3] is not None:
          sort_spec_pb.default_value_text = sort_spec[3]
    if offset is not None:
      params.offset = offset
    if limit is not None:
      params.limit = limit
    else:
      params.limit = 20
    if number_found_accuracy is not None:
      params.matched_count_accuracy = number_found_accuracy
    if ids_only:
      params.keys_only = True
    if cursor:
      params.cursor = cursor
    if cursor_type is not None:
      params.cursor_type = cursor_type

    def _MakeSearchResponse():
      response = search_service_pb2.SearchResponse()
      if documents is not None:
        response.matched_count = len(documents)
        for (position, doc) in enumerate(documents):
          result = response.result.add()
          document = result.document
          if document_cursors:
            result.cursor = document_cursors[position]
          document.id = doc.doc_id
          if not ids_only:
            for f in doc.fields:
              field = document.field.add()
              field.name = f.name
              value = field.value
              value.string_value = six.ensure_binary(f.value, 'utf-8')
            for fc in doc.facets:
              facet = document.facet.add()
              facet.name = fc.name
              value = facet.value
              value.string_value = six.ensure_binary(fc.value, 'utf-8')
      else:
        response.matched_count = 0
      if facets is not None:
        for f in facets:
          f_pb = response.facet_result.add()
          f_pb.name = f.name
          for v in f.values:
            v_pb = f_pb.value.add()
            v_pb.name = v.label
            v_pb.count = v.count
            ref = search.FacetRefinement.FromTokenString(v.refinement_token)
            ref_pb = v_pb.refinement
            ref_pb.name = ref.name
            if ref.value:
              ref_pb.value = ref.value
            else:
              if ref.facet_range.start is not None:
                ref_pb.range.start = str(ref.facet_range.start)
              if ref.facet_range.end is not None:
                ref_pb.range.end = str(ref.facet_range.end)

      response.status.code = code
      if response_cursor:
        response.cursor = response_cursor
      return response

    def ResponseSideEffects(service, method, request, response):
      b = _MakeSearchResponse().SerializeToString()
      response.ParseFromString(b)

    makeTestSyncCall('search', 'Search', request,
                     mox.IsA(search_service_pb2.SearchResponse), deadline,
                     ResponseSideEffects)
    if replay:
      self.mox.ReplayAll()

  def GetIndex(self):
    return self.GetIndexNamespace('')

  def GetIndexNamespace(self, namespace):
    return search.Index(name='index-name-999', namespace=namespace)

  def testDeleteDocumentIdNone(self):
    self.GetIndex().delete(None)

  def testDeleteEmptyList(self):
    self.GetIndex().delete([])

  def testDeleteWrongType(self):
    for value in NUMBERS:
      self.assertRaises(TypeError, self.GetIndex().delete, value)

  def testDeleteSchemaEmpty(self):
    self.assertRaises(TypeError, self.GetIndex().delete_schema, '')

  def testDeleteDocumentIdEmpty(self):
    self.assertRaises(ValueError, self.GetIndex().delete, '')

  def testDeleteDocumentIdTooLong(self):
    self.assertRaises(ValueError, self.GetIndex().delete,
                      'a' * (search.MAXIMUM_DOCUMENT_ID_LENGTH + 1))

  def testDeleteDocumentIdInvalid(self):
    self.assertRaises(ValueError, self.GetIndex().delete, '!')

  def testDeleteLimit(self):
    docs = ['id' for _ in range(search.MAXIMUM_DOCUMENTS_PER_PUT_REQUEST)]
    self.ExpectRemoveResponse(
        docs, [OK for _ in range(search.MAXIMUM_DOCUMENTS_PER_PUT_REQUEST)])
    self.GetIndex().delete(docs)

    docs = ['id' for _ in range(search.MAXIMUM_DOCUMENTS_PER_PUT_REQUEST + 1)]
    self.assertRaises(ValueError, self.GetIndex().delete, docs)
    self.mox.VerifyAll()

  def testDeleteOk(self):
    self.ExpectRemoveResponse(['doc9'], [OK])
    self.GetIndex().delete('doc9')
    self.mox.VerifyAll()

  def testDeleteAsyncOk(self):

    request_pb_doc9 = search_service_pb2.DeleteDocumentRequest()
    self.SetIndexSpec('index-name-999', '', request_pb_doc9.params.index_spec)
    request_pb_doc9.params.doc_id.append('doc9')


    request_pb_doc10 = search_service_pb2.DeleteDocumentRequest()
    self.SetIndexSpec('index-name-999', '', request_pb_doc10.params.index_spec)
    request_pb_doc10.params.doc_id.append('doc10')


    def SideEffect(method, request, response):
      response.status.add().code = OK


    rpc_doc9 = apiproxy_stub_map.UserRPC('search', deadline=None)
    response_pb_doc9 = mox.IsA(search_service_pb2.DeleteDocumentResponse)
    rpc_doc9.make_call('DeleteDocument', request_pb_doc9,
                  response_pb_doc9).WithSideEffects(SideEffect)


    rpc_doc10 = apiproxy_stub_map.UserRPC('search', deadline=None)
    response_pb_doc10 = mox.IsA(search_service_pb2.DeleteDocumentResponse)
    rpc_doc10.make_call('DeleteDocument', request_pb_doc10,
                  response_pb_doc10).WithSideEffects(SideEffect)


    rpc_doc9.wait()
    rpc_doc9.check_success()


    rpc_doc10.wait()
    rpc_doc10.check_success()


    self.mox.ReplayAll()


    futures = [self.GetIndex().delete_async('doc9'),
               self.GetIndex().delete_async('doc10')]


    results = [future.get_result() for future in futures]


    results_doc9, results_doc10 = results
    self.assertEqual(1, len(results_doc9))
    self.assertEqual(PUBLIC_OK, results_doc9[0].code)
    self.assertEqual(1, len(results_doc10))
    self.assertEqual(PUBLIC_OK, results_doc10[0].code)


    self.mox.VerifyAll()

  def testDeleteOkWithDeadline(self):
    self.ExpectRemoveResponse(['doc9'], [OK], deadline=10.0)
    self.GetIndex().delete('doc9', deadline=10.0)
    self.mox.VerifyAll()

  def testDeleteSchemaOk(self):
    self.ExpectDeleteSchemaResponse(self.GetIndex().name, [OK])
    self.GetIndex().delete_schema()
    self.mox.VerifyAll()

  def testDeleteSchemaFailure(self):
    self.ExpectDeleteSchemaResponse(self.GetIndex().name, [])
    self.assertRaises(search.DeleteError,
                      self.GetIndex().delete_schema)

  def testDeleteFailure(self):
    self.ExpectRemoveResponse(['doc9'], [])
    self.assertRaises(search.DeleteError,
                      self.GetIndex().delete, 'doc9')

  def testDeleteSchemaTransientError(self):
    self.ExpectDeleteSchemaResponse(self.GetIndex().name, [TRANSIENT_ERROR])
    try:
      self.GetIndex().delete_schema()
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertEqual(1, len(e.results))
      self.assertEqual(PUBLIC_TRANSIENT_ERROR, e.results[0].code)

  def testDeleteTransientError(self):
    self.ExpectRemoveResponse(['doc9'], [TRANSIENT_ERROR])
    try:
      self.GetIndex().delete('doc9')
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertEqual(1, len(e.results))
      self.assertEqual(PUBLIC_TRANSIENT_ERROR, e.results[0].code)

  def testDeleteAsyncTransientError(self):
    self.ExpectRemoveResponse(['doc9'], [TRANSIENT_ERROR])
    future = self.GetIndex().delete_async('doc9')
    try:
      future.get_result()
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertEqual(1, len(e.results))
      self.assertEqual(PUBLIC_TRANSIENT_ERROR, e.results[0].code)

  def testDeleteSchemaTransientErrorWithMessage(self):
    error_detail = 'some very interesting error message'
    self.ExpectDeleteSchemaResponse(self.GetIndex().name,
                                    [(TRANSIENT_ERROR, error_detail)])
    try:
      self.GetIndex().delete_schema()
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertIn(error_detail, str(e))
      self.assertEqual(1, len(e.results))
      self.assertEqual(PUBLIC_TRANSIENT_ERROR, e.results[0].code)

  def testDeleteTransientErrorWithMessage(self):
    error_detail = 'some very interesting error message'
    self.ExpectRemoveResponse(['doc9'], [(TRANSIENT_ERROR, error_detail)])
    try:
      self.GetIndex().delete('doc9')
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertIn(error_detail, str(e))
      self.assertEqual(1, len(e.results))
      self.assertEqual(PUBLIC_TRANSIENT_ERROR, e.results[0].code)

  def testDeleteSchemaCallWithError(self):
    self.ExpectDeleteSchemaError(INTERNAL_ERROR, 'detail1')
    try:
      self.GetIndex().delete_schema()
      self.fail('Expected Internal Error')
    except search.InternalError as e:
      self.assertIn('detail1', str(e))

  def testDeleteCallWithError(self):
    self.ExpectRemoveError(INTERNAL_ERROR, 'detail1')
    try:
      self.GetIndex().delete('doc9')
      self.fail('Expected Internal Error')
    except search.InternalError as e:
      self.assertIn('detail1', str(e))

  def testDeleteAllOk(self):
    self.ExpectRemoveResponse(['doc9', 'doc8'], [OK, OK])
    self.GetIndex().delete(['doc9', 'doc8'])
    self.mox.VerifyAll()

  def testDeleteSchemaNamespaceOk(self):
    self.ExpectDeleteSchemaResponseNamespace(
        'ns', self.GetIndexNamespace('ns').name, [OK])
    self.GetIndexNamespace('ns').delete_schema()
    self.mox.VerifyAll()

  def testDeleteNamespaceAllOk(self):
    self.ExpectRemoveResponseNamespace('ns', ['doc9', 'doc8'], [OK, OK])
    self.GetIndexNamespace('ns').delete(['doc9', 'doc8'])
    self.mox.VerifyAll()

  def testDeleteSchemaNoResponse(self):
    self.ExpectDeleteSchemaResponse(self.GetIndex().name, [])
    try:
      self.GetIndex().delete_schema()
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertIn('delete exactly one', str(e))

  def testDeleteSomeNoResponse(self):
    self.ExpectRemoveResponse(['doc9', 'doc8'], [OK])
    try:
      self.GetIndex().delete(['doc9', 'doc8'])
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertIn('number', str(e))

  def testDeleteSomeFail(self):
    self.ExpectRemoveResponse(['doc9', 'doc8'], [OK, TRANSIENT_ERROR])
    try:
      self.GetIndex().delete(['doc9', 'doc8'])
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertEqual(2, len(e.results))
      self.assertEqual(PUBLIC_OK, e.results[0].code)
      self.assertEqual(PUBLIC_TRANSIENT_ERROR, e.results[1].code)

  def testDeleteSchemaMoreOksThenRequested(self):
    self.ExpectDeleteSchemaResponse(self.GetIndex().name, [OK, OK])
    try:
      self.GetIndex().delete_schema()
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertIn('delete exactly one', str(e))

  def testDeleteMoreOksThenRequested(self):
    self.ExpectRemoveResponse(['doc9', 'doc8'], [OK, OK, OK])
    try:
      self.GetIndex().delete(['doc9', 'doc8'])
      self.fail('Expected DeleteError')
    except search.DeleteError as e:
      self.assertIn('number', str(e))

  def testPutDocumentsString(self):
    index = self.GetIndex()
    self.assertRaises(TypeError, index.put, 'document')
    self.assertRaises(TypeError, index.put_async, 'document')

  def testPutDocumentsOk(self):
    doc = APIFunctionTest.DOCUMENT1
    self.ExpectAddResponse([doc], [OK])
    results = self.GetIndex().put(doc)
    self.assertEqual(1, len(results))
    result = results[0]
    self.assertEqual(doc.doc_id, result.id)
    self.mox.VerifyAll()

  def testPutDocumentsAsyncOk(self):
    doc = APIFunctionTest.DOCUMENT1
    self.ExpectAddResponse([doc], [OK])
    future = self.GetIndex().put_async(doc)
    results = future.get_result()
    self.assertEqual(1, len(results))
    result = results[0]
    self.assertEqual(doc.doc_id, result.id)
    self.mox.VerifyAll()

  def testPutDocumentsOkWithDeadline(self):
    doc = APIFunctionTest.DOCUMENT1
    self.ExpectAddResponse([doc], [OK], deadline=10.0)
    results = self.GetIndex().put(doc, deadline=10.0)
    self.assertEqual(1, len(results))
    result = results[0]
    self.assertEqual(doc.doc_id, result.id)
    self.mox.VerifyAll()

  def testPutDuplicateDocumentsSameContentOK(self):
    doc = APIFunctionTest.DOCUMENT1
    self.ExpectAddResponse([doc], [OK])
    results = self.GetIndex().put([doc, doc])
    self.assertEqual(1, len(results))
    result = results[0]
    self.assertEqual(doc.doc_id, result.id)
    self.mox.VerifyAll()

  def testPutDuplicateDocumentsFail(self):
    doc = search.Document(
        doc_id='same_doc',
        fields=[search.TextField(name='subject', value='some text')])
    updated_doc = search.Document(
        doc_id='same_doc',
        fields=[search.TextField(name='subject', value='NEW text')])
    self.assertRaises(ValueError, self.GetIndex().put, [doc, updated_doc])

  def testPutDocumentsNoIdsOk(self):
    doc = search.Document(
        fields=[search.TextField(name='subject', value='some text')])
    self.ExpectAddResponse([doc, doc], [OK, OK], ['first', 'second'])
    results = self.GetIndex().put([doc, doc])
    self.assertEqual(2, len(results))
    result = results[0]
    self.assertEqual('first', result.id)
    result = results[1]
    self.assertEqual('second', result.id)
    self.mox.VerifyAll()

  def testPutDocumentsNone(self):
    self.assertRaises(AttributeError, self.GetIndex().put, None)

  def testPutDocumentsFailure(self):
    doc = APIFunctionTest.DOCUMENT1
    self.ExpectAddResponse([doc], [])
    try:
      self.GetIndex().put(doc)
      self.fail('Expected error')
    except search.PutError as e:
      self.assertIn('number', str(e))
      self.assertFalse(e.results)

  def testPutDocumentsTransientError(self):
    doc = APIFunctionTest.DOCUMENT1
    self.ExpectAddResponse([doc], [TRANSIENT_ERROR])
    try:
      self.GetIndex().put(doc)
      self.fail('Expected PutError')
    except search.PutError as e:
      self.assertEqual(1, len(e.results))
      self.assertEqual(PUBLIC_TRANSIENT_ERROR, e.results[0].code)

  def testPutDocumentsTransientErrorWithDetail(self):
    doc = APIFunctionTest.DOCUMENT1
    error_detail = 'some very interesting error message'
    self.ExpectAddResponse([doc], [(TRANSIENT_ERROR, error_detail)])
    try:
      self.GetIndex().put(doc)
      self.fail('Expected PutError')
    except search.PutError as e:
      self.assertIn(error_detail, str(e))
      self.assertEqual(1, len(e.results))
      self.assertEqual(PUBLIC_TRANSIENT_ERROR, e.results[0].code)

  def testPutDocumentsCallWithError(self):
    self.ExpectAddError(INTERNAL_ERROR, 'detail1')
    try:
      self.GetIndex().put(APIFunctionTest.DOCUMENT1)
      self.fail('Expected Internal Error')
    except search.InternalError as e:
      self.assertIn('detail1', str(e))

  def testPutDocumentsOverQuotaErrorNoNamespace(self):
    self.ExpectAddOverQuotaError()
    try:
      self.GetIndex().put(APIFunctionTest.DOCUMENT1)
      self.fail('Expected OverQuotaError')
    except apiproxy_errors.OverQuotaError as e:
      self.assertIn('denied', str(e))
      self.assertIn('index-name-999', str(e))
      self.assertNotIn('in namespace', str(e))

  def testPutDocumentsOverQuotaErrorWithNamespace(self):
    self.ExpectAddOverQuotaError()
    try:
      self.GetIndexNamespace('mynamespace').put(APIFunctionTest.DOCUMENT1)
      self.fail('Expected OverQuotaError')
    except apiproxy_errors.OverQuotaError as e:
      self.assertIn('denied', str(e))
      self.assertIn('index-name-999', str(e))
      self.assertIn('in namespace', str(e))
      self.assertIn('mynamespace', str(e))

  def testPutDocumentsEmptyList(self):
    self.GetIndex().put([])

  def testPutDocumentsMoreThanOneOk(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectAddResponse(docs, [OK, OK])
    results = self.GetIndex().put(docs)
    self.assertEqual(2, len(results))
    result = results[0]
    self.assertEqual(APIFunctionTest.DOCUMENT1.doc_id, result.id)
    result = results[1]
    self.assertEqual(APIFunctionTest.DOCUMENT2.doc_id, result.id)
    self.mox.VerifyAll()

  def testPutDocumentsLimit(self):
    docs = [
        search.Document(doc_id=str(i))
        for i in range(search.MAXIMUM_DOCUMENTS_PER_PUT_REQUEST)
    ]
    self.ExpectAddResponse(
        docs, [OK for _ in range(search.MAXIMUM_DOCUMENTS_PER_PUT_REQUEST)])
    self.GetIndex().put(docs)
    docs = [
        search.Document(doc_id=str(i))
        for i in range(search.MAXIMUM_DOCUMENTS_PER_PUT_REQUEST + 1)
    ]
    self.assertRaises(ValueError, self.GetIndex().put, docs)
    self.mox.VerifyAll()

  def testPutDocumentsMoreThanOneNamespaceOk(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectAddResponseNamespace('ns', docs, [OK, OK])
    results = self.GetIndexNamespace('ns').put(docs)
    self.assertEqual(2, len(results))
    result = results[0]
    self.assertEqual(APIFunctionTest.DOCUMENT1.doc_id, result.id)
    result = results[1]
    self.assertEqual(APIFunctionTest.DOCUMENT2.doc_id, result.id)
    self.mox.VerifyAll()

  def testPutDocumentsOkAndFailure(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectAddResponse(docs, [OK])
    try:
      self.GetIndex().put(docs)
      self.fail('Expected PutError')
    except search.PutError as e:
      self.assertIn('number', str(e))

  def testPutDocumentsDuplicateIds(self):
    test_doc = search.Document(
        doc_id='x', fields=[search.TextField(name='a', value='a')])

    docs = [search.Document(doc_id='x'), test_doc]
    try:
      self.GetIndex().put(docs)
      self.fail('Expected ValueError on duplicate IDs with different content')
    except ValueError:
      pass

    docs = [copy.deepcopy(test_doc), copy.deepcopy(test_doc)]
    self.ExpectAddResponse([test_doc], [OK])
    self.GetIndex().put(docs)
    self.mox.VerifyAll()

  def QueryIsParseable(self, query):
    self.ExpectSearchResponse(query=query)
    self.GetIndex().search(query=query)
    self.mox.VerifyAll()

  def testRequiredArgumentsMissing(self):
    self.assertRaises(TypeError, self.GetIndex().search)

  def testParseQuerySimple(self):
    self.QueryIsParseable('ok')

  def testParseQueryComplex(self):
    self.QueryIsParseable('to be or not to be')

  def testParseQueryComplexSequence(self):
    self.QueryIsParseable('"to be" or "not to" be')

  def testParseQueryComplexRestricts(self):
    self.QueryIsParseable('to:be OR NOT to:be')

  def testParseQueryRestrictNumber(self):
    self.QueryIsParseable('foo<=100')

  def testParseQueryRestrictNegativeNumber(self):
    self.QueryIsParseable('foo>=-100')

  def testParseQueryUnfinished(self):
    self.assertRaises(search.QueryError, self.GetIndex().search,
                      query='be NOT')

  def testQueryTooLong(self):
    query = 'q' * search.MAXIMUM_QUERY_LENGTH
    self.ExpectSearchResponse(query=query)
    self.GetIndex().search(query=query)
    self.mox.VerifyAll()

    self.assertRaises(ValueError, self.GetIndex().search, query=query + 'q')

  def testQueryWrongType(self):
    for value in _NON_STRING_VALUES:
      self.assertRaises(AttributeError, self.GetIndex().search, query=value)

  def testQueryEmpty(self):
    self.ExpectSearchResponse(query='')
    self.GetIndex().search(query='')
    self.mox.VerifyAll()

  def testQuerySpace(self):
    self.ExpectSearchResponse(query=' ')
    self.GetIndex().search(query=' ')
    self.mox.VerifyAll()

  def testQueryUnicode(self):
    self.ExpectSearchResponse(query=_UNICODE_STRING.encode('utf-8'))
    self.GetIndex().search(query=_UNICODE_STRING)
    self.mox.VerifyAll()

  def testWrongTypes(self):
    self.assertRaises(AttributeError, self.GetIndex().search, query=1)

  def testSearchNullQuery(self):
    self.assertRaises(AttributeError, self.GetIndex().search, None)

  def testSearchOk(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponse(query='subject:good', documents=docs, code=OK)
    results = self.GetIndex().search('subject:good')
    self.assertIsInstance(results, search.SearchResults)
    self.assertEqual(len(docs), results.number_found)
    self.assertEqual(len(docs), len(results.results))
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
    self.mox.VerifyAll()

  def testSearchAsyncOk(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponse(query='subject:good', documents=docs, code=OK,
                              replay=False)
    self.ExpectSearchResponse(query='subject:good', documents=docs, code=OK,
                              replay=True)
    futures = [self.GetIndex().search_async('subject:good'),
               self.GetIndex().search_async('subject:good')]
    both_results = [future.get_result() for future in futures]
    self.assertEqual(2, len(both_results))
    for results in both_results:
      self.assertIsInstance(results, search.SearchResults)
      self.assertEqual(len(docs), results.number_found)
      self.assertEqual(len(docs), len(results.results))
      for i in range(len(docs)):
        self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
    self.mox.VerifyAll()

  def testSearchOkWithDeadline(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponse(query='subject:good', documents=docs, code=OK,
                              deadline=10.0)
    results = self.GetIndex().search('subject:good', deadline=10.0)
    self.assertIsInstance(results, search.SearchResults)
    self.assertEqual(len(docs), results.number_found)
    self.assertEqual(len(docs), len(results.results))
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
    self.mox.VerifyAll()

  def testSearchKeysOnlyQueryOptions(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2,
            APIFunctionTest.DOCUMENT4, APIFunctionTest.DOCUMENT5]
    self.ExpectSearchResponse(query='subject:good', documents=docs, code=OK,
                              ids_only=True)
    results = self.GetIndex().search(
        search.Query('subject:good', search.QueryOptions(ids_only=True)))
    self.assertIsInstance(results, search.SearchResults)
    self.assertEqual(len(docs), results.number_found)
    self.assertEqual(len(docs), len(results.results))
    self.assertEqual(None, results.cursor)
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
      self.assertEqual(None, results.results[i].cursor)
      self.assertFalse(results.results[i].fields)
      self.assertFalse(results.results[i].facets)
    self.mox.VerifyAll()

  def testSearchResultCursorsQueryObjectNoneSet(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponse(query='subject:good', documents=docs, code=OK,
                              response_cursor=None)
    results = self.GetIndex().search(search.Query('subject:good'))
    self.assertEqual(None, results.cursor)
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
      self.assertEqual(None, results.results[i].cursor)
    self.mox.VerifyAll()

  def CheckSearchResultCursorsQueryObjectPerResult(self, cursor):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponse(
        query='subject:good',
        documents=docs,
        code=OK,
        cursor_type=search_service_pb2.SearchParams.PER_RESULT,
        response_cursor=None,
        document_cursors=['0', '1'])
    options = search.QueryOptions(cursor=cursor)
    results = self.GetIndex().search(
        search.Query('subject:good', options=options))
    self.assertEqual(None, results.cursor)
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
      self.assertEqual('True:' + str(i),
                        results.results[i].cursor.web_safe_string)
    self.mox.VerifyAll()

  def testSearchResultCursorsQueryObjectPerResultCursor(self):
    self.CheckSearchResultCursorsQueryObjectPerResult(
        search.Cursor(per_result=True))

  def testSearchResultCursorsQueryObjectPerResult(self):
    self.CheckSearchResultCursorsQueryObjectPerResult(
        search.Cursor(per_result=True))

  def CheckSearchResultCursorsQueryObjectSingleResult(self, cursor):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponse(
        query='subject:good',
        documents=docs,
        code=OK,
        cursor_type=search_service_pb2.SearchParams.SINGLE,
        response_cursor='single')
    options = search.QueryOptions(cursor=cursor)
    results = self.GetIndex().search(
        search.Query('subject:good', options=options))
    self.assertFalse(results.cursor.per_result)
    self.assertEqual('False:single', results.cursor.web_safe_string)
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
      self.assertEqual(None, results.results[i].cursor)
    self.mox.VerifyAll()

  def testSearchResultCursorsQueryObjectSingleResultCursor(self):
    self.CheckSearchResultCursorsQueryObjectSingleResult(
        search.Cursor())

  def testSearchResultCursorsQueryObjectSingleResult(self):
    self.CheckSearchResultCursorsQueryObjectSingleResult(search.Cursor())

  def testSearchTransientError(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponse(query='subject:good', documents=docs,
                              code=TRANSIENT_ERROR)
    self.assertRaises(search.TransientError, self.GetIndex().search,
                      'subject:good')

  def testSearchCallWithError(self):
    try:
      self.ExpectSearchError(INTERNAL_ERROR, 'detail1')
      self.GetIndex().search('subject:good')
      self.fail('Expected Internal Error')
    except search.InternalError as e:
      self.assertIn('detail1', str(e))

  def testSearchNamespaceOk(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponseNamespace(namespace='ns', query='subject:good',
                                       documents=docs, code=OK)
    results = self.GetIndexNamespace('ns').search(query='subject:good')
    self.assertIsInstance(results, search.SearchResults)
    self.assertEqual(len(docs), results.number_found)
    self.assertEqual(len(docs), len(results.results))
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
    self.mox.VerifyAll()

  def testSearchNamespaceOkQueryObject(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponseNamespace(namespace='ns', query='subject:good',
                                       documents=docs, code=OK)
    results = self.GetIndexNamespace('ns').search(
        search.Query(query_string='subject:good'))
    self.assertIsInstance(results, search.SearchResults)
    self.assertEqual(len(docs), results.number_found)
    self.assertEqual(len(docs), len(results.results))
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
    self.mox.VerifyAll()

  def testSearchNamespaceUseManagerOk(self):
    namespace_manager.set_namespace('ns')
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponseNamespace(
        namespace='ns', query='subject:good', documents=docs, code=OK)
    results = self.GetIndexNamespace(None).search(query='subject:good')
    self.assertIsInstance(results, search.SearchResults)
    self.assertEqual(len(docs), results.number_found)
    self.assertEqual(len(docs), len(results.results))
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
    self.mox.VerifyAll()

  def testSearchNamespaceUseManagerOkQueryObject(self):
    namespace_manager.set_namespace('ns')
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectSearchResponseNamespace(
        namespace='ns', query='subject:good', documents=docs, code=OK)
    results = self.GetIndexNamespace(None).search(
        query=search.Query(query_string='subject:good'))
    self.assertIsInstance(results, search.SearchResults)
    self.assertEqual(len(docs), results.number_found)
    self.assertEqual(len(docs), len(results.results))
    for i in range(len(docs)):
      self.assertEqual(docs[i].doc_id, results.results[i].doc_id)
    self.mox.VerifyAll()

  def testSearchQueryWithSnippetedFields(self):
    expressions = [
        search.FieldExpression('subject',
                               'snippet("\\\"foo bar\\\" baz", subject)'),
        search.FieldExpression('body',
                               'snippet("\\\"foo bar\\\" baz", body)')]
    self.ExpectSearchResponse(query='"foo bar" baz',
                              returned_expressions=expressions,
                              code=OK)
    self.GetIndex().search(
        query=search.Query(
            query_string='"foo bar" baz',
            options=search.QueryOptions(snippeted_fields=['subject', 'body'])))
    self.mox.VerifyAll()

  def testSearchQueryWithFacets(self):
    facet1 = search.FacetResult(
        name='facet1',
        values=[search.FacetResultValue(
            'label1', 10,
            search.FacetRefinement(name='facet1', value='value1'))])
    facet2 = search.FacetResult(
        name='facet2',
        values=[search.FacetResultValue(
            'label2', 10,
            search.FacetRefinement(
                name='facet2', facet_range=search.FacetRange(start=1, end=2)))])
    self.ExpectSearchResponse(query='ignored',
                              facets=[facet1, facet2],
                              code=OK)
    self.GetIndex().search(
        query=search.Query(query_string='ignored'))
    self.mox.VerifyAll()

  def testSearchQueryWithUnicodeSnippetedFields(self):
    docs = [APIFunctionTest.DOCUMENT3]
    expressions = [
        search.FieldExpression('subject',
                               'snippet("\\"foo bar\\" baz", subject)'),
        search.FieldExpression('body',
                               'snippet("\\"foo bar\\" baz", body)')]
    self.ExpectSearchResponse(query='"foo bar" baz',
                              returned_expressions=expressions,
                              documents=docs, code=OK)
    self.GetIndex().search(
        query=search.Query(
            query_string='"foo bar" baz',
            options=search.QueryOptions(snippeted_fields=['subject', 'body'])))
    self.mox.VerifyAll()

  def testGetIndexesOk(self):
    self.ExpectListIndexesResponse(OK, ['index_name'])
    response = search.get_indexes()
    self.assertEqual(1, len(response.results))
    self.assertEqual('index_name', response.results[0].name)
    self.assertEqual(None, response.results[0].schema)
    self.assertEqual(None, response.results[0].storage_usage)
    self.assertEqual(None, response.results[0].storage_limit)
    self.mox.VerifyAll()

  def testGetIndexesOkAllNamespaces(self):
    self.ExpectListIndexesResponse(OK, ['index_name', 'another_index_name'],
                                   namespace_list=['', 'ns'],
                                   all_namespaces=True)
    response = search.get_indexes(all_namespaces=True)
    self.assertLen(response, 2)
    self.assertEqual('', response.results[0].namespace)
    self.assertEqual('index_name', response.results[0].name)
    self.assertEqual('ns', response.results[1].namespace)
    self.assertEqual('another_index_name', response.results[1].name)
    self.mox.VerifyAll()

  def testGetIndexesAsyncOk(self):
    self.ExpectListIndexesResponse(OK, ['index_name'])
    future = search.get_indexes_async()
    response = future.get_result()
    self.assertEqual(1, len(response.results))
    self.assertEqual('index_name', response.results[0].name)
    self.assertEqual(None, response.results[0].schema)
    self.assertEqual(None, response.results[0].storage_usage)
    self.assertEqual(None, response.results[0].storage_limit)
    self.mox.VerifyAll()

  def testGetIndexesOkWithDeadline(self):
    self.ExpectListIndexesResponse(OK, ['index_name'], deadline=10.0)
    response = search.get_indexes(deadline=10.0)
    self.assertEqual(1, len(response.results))
    self.assertEqual('index_name', response.results[0].name)
    self.assertEqual(None, response.results[0].schema)
    self.mox.VerifyAll()

  def testGetIndexesCheckOffsetMaximum(self):
    self.ExpectListIndexesResponse(OK, ['index_name'],
                                   offset=search.MAXIMUM_GET_INDEXES_OFFSET)
    response = search.get_indexes(offset=search.MAXIMUM_GET_INDEXES_OFFSET)
    self.assertEqual(1, len(response.results))
    self.assertEqual('index_name', response.results[0].name)
    self.assertEqual(None, response.results[0].schema)
    self.mox.VerifyAll()

    self.assertRaises(ValueError, search.get_indexes,
                      offset=search.MAXIMUM_GET_INDEXES_OFFSET + 1)

  def testGetIndexesCheckLimitMaximum(self):
    self.ExpectListIndexesResponse(
        OK, ['index_name'],
        limit=search.MAXIMUM_INDEXES_RETURNED_PER_GET_REQUEST)
    response = search.get_indexes(
        limit=search.MAXIMUM_INDEXES_RETURNED_PER_GET_REQUEST)
    self.assertEqual(1, len(response.results))
    self.assertEqual('index_name', response.results[0].name)
    self.assertEqual(None, response.results[0].schema)
    self.mox.VerifyAll()

    self.assertRaises(
        ValueError, search.get_indexes,
        limit=search.MAXIMUM_INDEXES_RETURNED_PER_GET_REQUEST + 1)

  def testGetIndexesWithSchemas(self):
    field1 = document_pb2.FieldTypes()
    field1.name = 'some_field'
    field1.type.append(document_pb2.FieldValue.HTML)
    field1.type.append(document_pb2.FieldValue.TEXT)

    field2 = document_pb2.FieldTypes()
    field2.name = 'another_field'
    field2.type.append(document_pb2.FieldValue.NUMBER)
    field2.type.append(document_pb2.FieldValue.DATE)

    self.ExpectListIndexesResponse(OK, index_names=['index_name'],
                                   field_map={'index_name': [field1, field2]},
                                   fetch_schema=True)
    response = search.get_indexes(fetch_schema=True)
    self.assertEqual(1, len(response.results))
    index = response.results[0]
    self.assertEqual('index_name', index.name)
    self.assertEqual(
        {'another_field': [search.Field.NUMBER, search.Field.DATE],
         'some_field': [search.Field.HTML, search.Field.TEXT]},
        index.schema)
    self.mox.VerifyAll()

  def testGetIndexesWithStorage(self):
    self.ExpectListIndexesResponse(OK, index_names=['foo','bar'],
                                   storage_map={'foo': 1732, 'bar': 42})
    response = search.get_indexes()
    self.assertEqual(2, len(response.results))
    index = response.results[0]
    self.assertEqual('foo', index.name)
    self.assertEqual(1732, index.storage_usage)
    self.assertEqual(_MAX_STORAGE, index.storage_limit)
    index = response.results[1]
    self.assertEqual('bar', index.name)
    self.assertEqual(42, index.storage_usage)
    self.assertEqual(_MAX_STORAGE, index.storage_limit)
    self.mox.VerifyAll()

  def testGetIndexesWithMissingStorage(self):
    request = search_service_pb2.ListIndexesRequest()
    params = request.params
    params.namespace = ''
    params.include_start_index = True
    params.limit = 20
    params.fetch_schema = False
    self.ExpectListIndexesResponse(OK, index_names=['foo','bar'],
                                   request=request)
    response = search.get_indexes()
    self.assertEqual(2, len(response.results))
    self.assertEqual(None, response.results[0].storage_usage)
    self.assertEqual(None, response.results[0].storage_limit)
    self.assertEqual(None, response.results[1].storage_usage)
    self.assertEqual(None, response.results[1].storage_limit)
    self.mox.VerifyAll()

  def testGetIndexesComplex(self):
    req = search_service_pb2.ListIndexesRequest()
    params = req.params
    params.namespace = 'a'
    params.include_start_index = False
    params.offset = 12
    params.limit = 10
    params.start_index_name = 'b'
    params.index_name_prefix = 'c'
    params.fetch_schema = False
    self.ExpectListIndexesResponse(OK, ['index_name'], request=req)
    response = search.get_indexes(offset=12, limit=10, namespace='a',
                                  start_index_name='b', index_name_prefix='c',
                                  include_start_index=False)
    self.assertEqual(1, len(response.results))
    self.assertEqual('index_name', response.results[0].name)
    self.mox.VerifyAll()

  def testGetIndexesTransientErrorIndexes(self):
    self.ExpectListIndexesResponse(TRANSIENT_ERROR, [], message='detail1')
    try:
      search.get_indexes()
      self.fail('Expected Internal Error')
    except search.TransientError as e:
      self.assertIn('detail1', str(e))

  def testGetIndexesCallWithError(self):
    self.ExpectListIndexesError(INTERNAL_ERROR, 'detail1')
    try:
      search.get_indexes()
      self.fail('Expected Internal Error')
    except search.InternalError as e:
      self.assertIn('detail1', str(e))

  def testGetRangeOkDefaultArgs(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectListResponse(OK, docs)
    response = self.GetIndex().get_range()
    self.assertEqual(2, len(response.results))
    self.assertEqual(APIFunctionTest.DOCUMENT1.doc_id,
                      response.results[0].doc_id)
    self.assertEqual(APIFunctionTest.DOCUMENT2.doc_id,
                      response.results[1].doc_id)
    self.mox.VerifyAll()

  def testGetRangeAsyncOkDefaultArgs(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectListResponse(OK, docs)
    future = self.GetIndex().get_range_async()
    response = future.get_result()
    self.assertEqual(2, len(response.results))
    self.assertEqual(APIFunctionTest.DOCUMENT1.doc_id,
                      response.results[0].doc_id)
    self.assertEqual(APIFunctionTest.DOCUMENT2.doc_id,
                      response.results[1].doc_id)
    self.mox.VerifyAll()

  def testGetRangeOkDefaultArgsWithDeadline(self):
    docs = [APIFunctionTest.DOCUMENT1, APIFunctionTest.DOCUMENT2]
    self.ExpectListResponse(OK, docs, deadline=10.0)
    response = self.GetIndex().get_range(deadline=10.0)
    self.assertEqual(2, len(response.results))
    self.assertEqual(APIFunctionTest.DOCUMENT1.doc_id,
                      response.results[0].doc_id)
    self.assertEqual(APIFunctionTest.DOCUMENT2.doc_id,
                      response.results[1].doc_id)
    self.mox.VerifyAll()

  def testGetRangeOkAllArgs(self):
    docs = [APIFunctionTest.DOCUMENT1]
    self.ExpectListResponse(OK, docs, limit=50, start_doc_id='bicycle',
                            include_start_doc=False, ids_only=True)
    response = self.GetIndex().get_range(
        limit=50, start_id='bicycle', include_start_object=False,
        ids_only=True)
    self.assertEqual(1, len(response.results))
    self.assertEqual(APIFunctionTest.DOCUMENT1.doc_id,
                      response.results[0].doc_id)
    self.mox.VerifyAll()

  def testGetRangeCheckLimit(self):
    docs = [APIFunctionTest.DOCUMENT1]
    self.ExpectListResponse(
        OK, docs, limit=search.MAXIMUM_DOCUMENTS_RETURNED_PER_SEARCH)
    response = self.GetIndex().get_range(
        limit=search.MAXIMUM_DOCUMENTS_RETURNED_PER_SEARCH)
    self.assertEqual(1, len(response.results))
    self.assertEqual(APIFunctionTest.DOCUMENT1.doc_id,
                      response.results[0].doc_id)
    self.mox.VerifyAll()

    self.assertRaises(ValueError, self.GetIndex().get_range,
                      limit=search.MAXIMUM_DOCUMENTS_RETURNED_PER_SEARCH + 1)

  def testGetRangeTransientError(self):
    self.ExpectListResponse(TRANSIENT_ERROR, [], message='detail1')
    try:
      self.GetIndex().get_range()
      self.fail('Expected Transient Error')
    except search.TransientError as e:
      self.assertIn('detail1', str(e))

  def testGetRangeInternalError(self):
    self.ExpectListResponse(INTERNAL_ERROR, [], message='detail1')
    try:
      self.GetIndex().get_range()
      self.fail('Expected Internal Error')
    except search.InternalError as e:
      self.assertEqual('detail1', str(e))

  def testGetRangeInvalidRequest(self):
    self.ExpectListResponse(INVALID_REQUEST, [], message='detail1')
    try:
      self.GetIndex().get_range()
      self.fail('Expected Invalid Request')
    except search.InvalidRequest as e:
      self.assertEqual('detail1', str(e))

  def testGetRangeTransientErrorRaised(self):
    try:
      self.ExpectListDocumentsError(TRANSIENT_ERROR, message='detail1')
      self.GetIndex().get_range()
      self.fail('Expected Transient Error')
    except search.TransientError as e:
      self.assertEqual('detail1', str(e))

  def testGetRangeAsyncTransientErrorRaised(self):
    self.ExpectListDocumentsError(TRANSIENT_ERROR, message='detail1')
    future = self.GetIndex().get_range_async()
    try:
      future.get_result()
      self.fail('Expected Transient Error')
    except search.TransientError as e:
      self.assertEqual('detail1', str(e))

  def testGetRangeInvalidArgs(self):
    self.assertRaises(TypeError, self.GetIndex().get_range, bad_arg=True)

  def testDeadlineInvalidType(self):
    for nonNumbers in _NON_NUMBER_VALUES:
      self.assertRaises(TypeError, self.GetIndex().search,
                        query='subject:good', deadline=nonNumbers)

  def testDeadlineInvalidValue(self):
    self.assertRaises(ValueError, self.GetIndex().search,
                      query='subject:good', deadline=-2)

  def testIndexGet(self):
    doc = APIFunctionTest.DOCUMENT2
    self.ExpectListResponse(OK, [doc], limit=1, start_doc_id=doc.doc_id,
                            include_start_doc=True)
    returned_doc = self.GetIndex().get(doc.doc_id)
    self.assertEqual(returned_doc.doc_id, doc.doc_id)
    self.mox.VerifyAll()

  def testIndexGetAsync(self):
    doc = APIFunctionTest.DOCUMENT2
    self.ExpectListResponse(OK, [doc], limit=1, start_doc_id=doc.doc_id,
                            include_start_doc=True)
    future = self.GetIndex().get_async(doc.doc_id)
    returned_doc = future.get_result()
    self.assertEqual(returned_doc.doc_id, doc.doc_id)
    self.mox.VerifyAll()

  def testIndexGetWithDeadline(self):
    doc = APIFunctionTest.DOCUMENT2
    self.ExpectListResponse(OK, [doc], limit=1, start_doc_id=doc.doc_id,
                            include_start_doc=True, deadline=10.0)
    returned_doc = self.GetIndex().get(doc.doc_id, deadline=10.0)
    self.assertEqual(returned_doc.doc_id, doc.doc_id)
    self.mox.VerifyAll()

  def testSerialization(self):


    doc = pickle.loads(six.ensure_binary(
        "ccopy_reg\n_reconstructor\np0\n(cgoogle.appengine.api.search.search"
        "\nDocument\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n(dp5\nS'_doc_id'"
        "\np6\nVdoc99\np7\nsS'_language'\np8\nVen\np9\nsS'_fields'\np10\n(lp11"
        "\ng0\n(cgoogle.appengine.api.search.search\nTextField\np12\ng2\n"
        "Ntp13\nRp14\n(dp15\nS'_name'\np16\nVsubject\np17\nsS'_value'\np18\n"
        "Vsome text\np19\nsg8\nNsbasS'_rank'\np20\nI120323603\nsS'_field_map"
        "'\np21\nNsb."))
    self.ExpectAddResponse([doc], [OK])
    results = self.GetIndex().put(doc)
    self.assertEqual(1, len(results))
    result = results[0]
    self.assertEqual(doc.doc_id, result.id)
    self.mox.VerifyAll()


    repr(pickle.loads(six.ensure_binary(
        "ccopy_reg\n_reconstructor\np0\n(cgoogle.appengine.api.search.search"
        "\nSearchResults\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n(dp5\nS'_re"
        "sults'\np6\n(lp7\nsS'_number_found'\np8\nI0\nsS'_cursor'\np9\nNsb.")))

    self.mox.ResetAll()


    query = pickle.loads(six.ensure_binary(
        "ccopy_reg\n_reconstructor\np0\n(cgoogle.appengine.api.search.search"
        "\nQuery\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n(dp5\nS'_options'\n"
        "p6\nNsS'_query_string'\np7\nVterm\np8\nsb."))
    self.ExpectSearchResponse(query='term')
    self.GetIndex().search(query=query)
    self.mox.VerifyAll()

    doc = search.Document(doc_id='doc_id',
                          facets=[search.AtomFacet('facet', 'value')])
    doc = pickle.loads(pickle.dumps(doc))
    self.assertEqual(len(doc.facets), 1)
    self.assertEqual(doc.facets[0].name, 'facet')
    self.assertEqual(doc.facets[0].value, 'value')

    result = search.SearchResults(number_found=0,
                                  facets=[search.FacetResult(name='facet')])
    result = pickle.loads(pickle.dumps(result))
    self.assertEqual(len(result.facets), 1)
    self.assertEqual(result.facets[0].name, 'facet')

    query = search.Query(
        query_string='term',
        enable_facet_discovery=True,
        facet_options=search.FacetOptions(depth=1234),
        return_facets=search.FacetRequest(name='facet'),
        facet_refinements=search.FacetRefinement(name='facet2',
                                                 value=['value']))
    query = pickle.loads(pickle.dumps(query))
    self.assertEqual(query.enable_facet_discovery, True)
    self.assertEqual(query.facet_options.depth, 1234)
    self.assertEqual(query.return_facets[0].name, 'facet')
    self.assertEqual(query.facet_refinements[0].name, 'facet2')


def makeTestSyncCall(service, method, request, response, deadline,
                     sideEffect=None):
  rpc = apiproxy_stub_map.UserRPC(service, deadline=deadline)
  def sideEffectWrapper(method, request, response):
    if sideEffect is not None:
      sideEffect(service, method, request, response)
  rpc.make_call(method, request,
                response).WithSideEffects(sideEffectWrapper)
  rpc.wait()
  return rpc.check_success()




def main(unused_argv):
  absltest.main()


if __name__ == '__main__':
  absltest.main(main)


