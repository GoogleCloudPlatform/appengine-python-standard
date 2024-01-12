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
"""MessageProperty -- a property storing ProtoRPC Message objects.
"""

from google.appengine.ext.ndb import model
from google.appengine.ext.ndb import utils
from google.appengine._internal.protorpc import messages
from google.appengine._internal.protorpc import remote
import six
from six.moves import map

__all__ = ['MessageProperty', 'EnumProperty']


_protocols_registry = remote.Protocols.new_default()
_default_protocol = 'protobuf'


class EnumProperty(model.IntegerProperty):
  """Enums are represented in Cloud Datastore as integers.

  While this is less user-friendly in the Datastore viewer, it matches
  the representation of enums in the protobuf serialization (although
  not in JSON), and it allows renaming enum values without requiring
  changes to values already stored in the Datastore.
  """

  _enum_type = None


  _attributes = ['_enum_type'] + model.IntegerProperty._attributes
  _positional = 1 + model.IntegerProperty._positional

  @utils.positional(1 + _positional)
  def __init__(self, enum_type, name=None, default=None, choices=None, **kwds):
    """Constructor.

    Args:
      enum_type: A subclass of protorpc.messages.Enum.
      name: Optional datastore name (defaults to the property name).

    Additional keywords arguments specify the same options as
    supported by IntegerProperty.
    """
    self._enum_type = enum_type
    if default is not None:
      self._validate(default)
    if choices is not None:
      list(map(self._validate, choices))
    super(EnumProperty, self).__init__(name, default=default,
                                       choices=choices, **kwds)

  def _validate(self, value):
    """Validate an Enum value.

    Raises:
      TypeError if the value is not an instance of self._enum_type.
    """
    if not isinstance(value, self._enum_type):
      raise TypeError('Expected a %s instance, got %r instead' %
                      (self._enum_type.__name__, value))

  def _to_base_type(self, enum):
    """Convert an Enum value to a base type (integer) value."""
    return enum.number

  def _from_base_type(self, val):
    """Convert a base type (integer) value to an Enum value."""
    return self._enum_type(val)


def _analyze_indexed_fields(indexed_fields):
  """Internal helper to check a list of indexed fields.

  Args:
    indexed_fields: A list of names, possibly dotted names.

  (A dotted name is a string containing names separated by dots,
  e.g. 'foo.bar.baz'.  An undotted name is a string containing no
  dots, e.g. 'foo'.)

  Returns:
    A dict whose keys are undotted names.  For each undotted name in
    the argument, the dict contains that undotted name as a key with
    None as a value.  For each dotted name in the argument, the dict
    contains the first component as a key with a list of remainders as
    values.

  Example:
    If the argument is ['foo.bar.baz', 'bar', 'foo.bletch'], the return
    value is {'foo': ['bar.baz', 'bletch'], 'bar': None}.

  Raises:
    TypeError if an argument is not a string.
    ValueError for duplicate arguments and for conflicting arguments
      (when an undotted name also appears as the first component of
      a dotted name).
  """
  result = {}
  for field_name in indexed_fields:
    if not isinstance(field_name, six.string_types):
      raise TypeError('Field names must be strings; got %r' % (field_name,))
    if '.' not in field_name:
      if field_name in result:
        raise ValueError('Duplicate field name %s' % field_name)
      result[field_name] = None
    else:
      head, tail = field_name.split('.', 1)
      if head not in result:
        result[head] = [tail]
      elif result[head] is None:
        raise ValueError('Field name %s conflicts with ancestor %s' %
                         (field_name, head))
      else:
        result[head].append(tail)
  return result


def _make_model_class(message_type, indexed_fields, **props):
  """Construct a Model subclass corresponding to a Message subclass.

  Args:
    message_type: A Message subclass.
    indexed_fields: A list of dotted and undotted field names.
    **props: Additional properties with which to seed the class.

  Returns:
    A Model subclass whose properties correspond to those fields of
    message_type whose field name is listed in indexed_fields, plus
    the properties specified by the **props arguments.  For dotted
    field names, a StructuredProperty is generated using a Model
    subclass created by a recursive call.

  Raises:
    Whatever _analyze_indexed_fields() raises.
    ValueError if a field name conflicts with a name in **props.
    ValueError if a field name is not valid field of message_type.
    ValueError if an undotted field name designates a MessageField.
  """
  analyzed = _analyze_indexed_fields(indexed_fields)
  for field_name, sub_fields in six.iteritems(analyzed):
    if field_name in props:
      raise ValueError('field name %s is reserved' % field_name)
    try:
      field = message_type.field_by_name(field_name)
    except KeyError:
      raise ValueError('Message type %s has no field named %s' %
                       (message_type.__name__, field_name))
    if isinstance(field, messages.MessageField):
      if not sub_fields:
        raise ValueError(
            'MessageField %s cannot be indexed, only sub-fields' % field_name)
      sub_model_class = _make_model_class(field.type, sub_fields)
      prop = model.StructuredProperty(sub_model_class, field_name,
                                      repeated=field.repeated)
    else:
      if sub_fields is not None:
        raise ValueError(
            'Unstructured field %s cannot have indexed sub-fields' % field_name)
      if isinstance(field, messages.EnumField):
        prop = EnumProperty(field.type, field_name, repeated=field.repeated)
      elif isinstance(field, messages.BytesField):
        prop = model.BlobProperty(field_name,
                                  repeated=field.repeated, indexed=True)
      else:

        prop = model.GenericProperty(field_name, repeated=field.repeated)
    props[field_name] = prop
  return model.MetaModel('_%s__Model' % message_type.__name__,
                         (model.Model,), props)


class MessageProperty(model.StructuredProperty):
  """Messages are represented in Cloud Datastore as structured properties.

  By default, the structured property has a single subproperty
  containing the serialized message.  This property is named 'blob_'
  in Python but __<protocol>__ in the Datastore, where <protocol> is
  the value of the protocol argument (default 'protobuf').
  """

  _message_type = None
  _indexed_fields = ()
  _protocol = _default_protocol
  _protocol_impl = None



  _attributes = (['_message_type'] + model.StructuredProperty._attributes[1:] +
                 ['_indexed_fields', '_protocol'])

  @utils.positional(1 + model.StructuredProperty._positional)
  def __init__(self, message_type, name=None,
               indexed_fields=None, protocol=None, **kwds):
    """Constructor.

    Args:
      message_tyoe: A subclass of protorpc.messages.Message.
      name: Optional datastore name (defaults to the property name).
      indexed_fields: Optional list of dotted and undotted field names.
      protocol: Optional protocol name default 'protobuf'.

    Additional keywords arguments specify the same options as
    supported by StructuredProperty, except 'indexed'.
    """
    if not (isinstance(message_type, type) and
            issubclass(message_type, messages.Message)):
      raise TypeError('MessageProperty argument must be a Message subclass')
    self._message_type = message_type
    if indexed_fields is not None:

      self._indexed_fields = tuple(indexed_fields)

    if protocol is None:
      protocol = _default_protocol
    self._protocol = protocol
    self._protocol_impl = _protocols_registry.lookup_by_name(protocol)
    blob_prop = model.BlobProperty('__%s__' % self._protocol)

    message_class = _make_model_class(message_type, self._indexed_fields,
                                      blob_=blob_prop)
    super(MessageProperty, self).__init__(message_class, name, **kwds)

  def _validate(self, msg):
    """Validate an Enum value.

    Raises:
      TypeError if the value is not an instance of self._message_type.
    """
    if not isinstance(msg, self._message_type):
      raise TypeError('Expected a %s instance for %s property',
                      self._message_type.__name__,
                      self._code_name or self._name)

  def _to_base_type(self, msg):
    """Convert a Message value to a Model instance (entity)."""
    ent = _message_to_entity(msg, self._modelclass)

    ent.blob_ = six.ensure_binary(self._protocol_impl.encode_message(msg))
    return ent

  def _from_base_type(self, ent):
    """Convert a Model instance (entity) to a Message value."""
    if ent._projection:

      return _projected_entity_to_message(ent, self._message_type)

    blob = ent.blob_
    if blob is not None:
      protocol = self._protocol_impl
    else:

      protocol = None
      for name in _protocols_registry.names:
        key = six.ensure_binary('__%s__' % name)
        if key in ent._values:
          blob = ent._values[key]
          if isinstance(blob, model._BaseValue):
            blob = blob.b_val
          protocol = _protocols_registry.lookup_by_name(name)
          break
    if blob is None or protocol is None:
      return None
    msg = protocol.decode_message(self._message_type, blob)
    return msg


def _message_to_entity(msg, modelclass):
  """Recursive helper for _to_base_type() to convert a message to an entity.

  Args:
    msg: A Message instance.
    modelclass: A Model subclass.

  Returns:
    An instance of modelclass.
  """
  ent = modelclass()

  for prop_name, prop in six.iteritems(modelclass._properties):
    if prop._code_name == 'blob_':
      continue
    value = getattr(msg, prop_name)
    if value is not None and isinstance(prop, model.StructuredProperty):
      if prop._repeated:
        value = [_message_to_entity(v, prop._modelclass) for v in value]
      else:
        value = _message_to_entity(value, prop._modelclass)
    setattr(ent, prop_name, value)

  return ent


def _projected_entity_to_message(ent, message_type):
  """Recursive helper for _from_base_type() to convert an entity to a message.

  Args:
    ent: A Model instance.
    message_type: A Message subclass.

  Returns:
    An instance of message_type.
  """
  msg = message_type()
  analyzed = _analyze_indexed_fields(ent._projection)
  for name, sublist in six.iteritems(analyzed):
    prop = ent._properties[name]
    val = prop._get_value(ent)
    assert isinstance(prop, model.StructuredProperty) == bool(sublist)
    if sublist:
      field = message_type.field_by_name(name)
      assert isinstance(field, messages.MessageField)
      assert prop._repeated == field.repeated
      if prop._repeated:
        assert isinstance(val, list)
        val = [_projected_entity_to_message(v, field.type) for v in val]
      else:
        assert isinstance(val, prop._modelclass)
        val = _projected_entity_to_message(val, field.type)
    if (six.PY3 and
        isinstance(val, bytes) and
        isinstance(getattr(message_type, name), messages.StringField)):




      val = val.decode('utf-8')
    setattr(msg, name, val)
  return msg
