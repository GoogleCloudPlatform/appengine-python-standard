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

"""Provides utility methods used by modules in the FTS API stub."""



import datetime
import re
import unicodedata

import six

from google.appengine.api.search import QueryParser
from google.appengine.datastore import document_pb2

DEFAULT_MAX_SNIPPET_LENGTH = 160

EXPRESSION_RETURN_TYPE_TEXT = 1
EXPRESSION_RETURN_TYPE_NUMERIC = 2

TEXT_DOCUMENT_FIELD_TYPES = [
    document_pb2.FieldValue.ATOM,
    document_pb2.FieldValue.TEXT,
    document_pb2.FieldValue.HTML,
    document_pb2.FieldValue.UNTOKENIZED_PREFIX,
    document_pb2.FieldValue.TOKENIZED_PREFIX,
]

TEXT_QUERY_TYPES = [
    QueryParser.STRING,
    QueryParser.TEXT,
]

NUMBER_DOCUMENT_FIELD_TYPES = [
    document_pb2.FieldValue.NUMBER,
]


BASE_DATE = datetime.datetime(1970, 1, 1, tzinfo=None)


class UnsupportedOnDevError(Exception):
  """Indicates attempt to perform an action unsupported on the dev server."""


def GetFieldInDocument(document, field_name, return_type=None):
  """Find and return the field with the provided name and type."""
  if return_type is not None:

    field_list = [f for f in document.field if f.name == field_name]
    field_types_dict = {}
    for f in field_list:
      field_types_dict.setdefault(f.value.type, f)
    if return_type == EXPRESSION_RETURN_TYPE_TEXT:
      if document_pb2.FieldValue.HTML in field_types_dict:
        return field_types_dict[document_pb2.FieldValue.HTML]
      if document_pb2.FieldValue.ATOM in field_types_dict:
        return field_types_dict[document_pb2.FieldValue.ATOM]
      return field_types_dict.get(document_pb2.FieldValue.TEXT)
    elif return_type == EXPRESSION_RETURN_TYPE_NUMERIC:
      if document_pb2.FieldValue.NUMBER in field_types_dict:
        return field_types_dict[document_pb2.FieldValue.NUMBER]
      return field_types_dict.get(document_pb2.FieldValue.DATE)
    else:
      return field_types_dict.get(return_type)
  else:

    for f in document.field:
      if f.name == field_name:
        return f
  return None


def GetAllFieldInDocument(document, field_name):
  """Find and return all fields with the provided name in the document."""
  fields = []
  for f in document.field:
    if f.name == field_name:
      fields.append(f)
  return fields


def AddFieldsToDocumentPb(doc_id, fields, document):
  """Add the id and fields to document.

  Args:
    doc_id: The document id.
    fields: List of tuples of field name, value and optionally type.
    document: The document to add the fields to.
  """
  if doc_id is not None:
    document.id = doc_id
  for field_tuple in fields:
    name = field_tuple[0]
    value = field_tuple[1]
    field = document.field.add()
    field.name = name
    field_value = field.value
    if len(field_tuple) > 2:
      field_value.type = field_tuple[2]
    if field_value.type == document_pb2.FieldValue.GEO:
      field_value.geo.lat = value.latitude
      field_value.geo.lng = value.longitude
    else:
      field_value.string_value = value.encode('utf-8')


def GetFieldCountInDocument(document, field_name):
  count = 0
  for field in document.field:
    if field.name == field_name:
      count += 1
  return count


def EpochTime(date):
  """Returns millisecond epoch time for a date or datetime."""
  if isinstance(date, datetime.datetime):
    td = date - BASE_DATE
  else:
    td = date - BASE_DATE.date()
  milliseconds_since_epoch = int(
      (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**3)
  return milliseconds_since_epoch


def SerializeDate(date):
  return str(EpochTime(date))


def DeserializeDate(date_str):



  if re.match(r'^\d+\-\d+\-\d+$', date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')
  else:
    dt = BASE_DATE + datetime.timedelta(milliseconds=int(date_str))
    return dt


def Repr(class_instance, ordered_dictionary):
  """Generates an unambiguous representation for instance and ordered dict."""
  return 'search.%s(%s)' % (class_instance.__class__.__name__, ', '.join([
      "%s='%s'" % (key, value) for (key, value) in ordered_dictionary if value
  ]))


def TreeRepr(tree, depth=0):
  """Generate a string representation of an ANTLR parse tree for debugging."""

  def _NodeRepr(node):
    text = str(node.getType())
    if node.getText():
      text = '%s: %s' % (text, node.getText())
    return text

  children = ''
  if tree.children:
    children = '\n' + '\n'.join(
        [TreeRepr(child, depth=depth + 1) for child in tree.children if child])
  return depth * '  ' + _NodeRepr(tree) + children


def RemoveAccents(text):
  if not isinstance(text, (six.text_type, six.binary_type)):
    return text

  text = six.ensure_text(text)

  return six.u('').join([c for c in text if not unicodedata.combining(c)])


def ConvertToNfkd(text):
  if not isinstance(text, (six.text_type, six.binary_type)):
    return text

  text = six.ensure_text(text)

  return unicodedata.normalize('NFKD', text)


def RemoveAccentsNfkd(text):
  if not isinstance(text, (six.text_type, six.binary_type)):
    return text

  text = six.ensure_text(text)

  return six.u('').join([
      c for c in unicodedata.normalize('NFKD', text)
      if not unicodedata.combining(c)
  ])
