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



"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/datastore/entity_v4.proto',
  package='google.appengine.datastore.v4',
  syntax='proto2',
  serialized_options=b'\n%com.google.google.appengine.datastore',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n*google/appengine/datastore/entity_v4.proto\x12\x1dgoogle.appengine.datastore.v4\"X\n\x0bPartitionId\x12\x12\n\ndataset_id\x18\x03 \x01(\t\x12\x11\n\tnamespace\x18\x04 \x01(\t\"\"\n\tConstants\x12\x15\n\x11MAX_DIMENSION_TAG\x10\x64\"\xc4\x01\n\x03Key\x12@\n\x0cpartition_id\x18\x01 \x01(\x0b\x32*.google.appengine.datastore.v4.PartitionId\x12\x44\n\x0cpath_element\x18\x02 \x03(\x0b\x32..google.appengine.datastore.v4.Key.PathElement\x1a\x35\n\x0bPathElement\x12\x0c\n\x04kind\x18\x01 \x02(\t\x12\n\n\x02id\x18\x02 \x01(\x03\x12\x0c\n\x04name\x18\x03 \x01(\t\"/\n\x08GeoPoint\x12\x10\n\x08latitude\x18\x01 \x02(\x01\x12\x11\n\tlongitude\x18\x02 \x02(\x01\"\xcb\x03\n\x05Value\x12\x15\n\rboolean_value\x18\x01 \x01(\x08\x12\x15\n\rinteger_value\x18\x02 \x01(\x03\x12\x14\n\x0c\x64ouble_value\x18\x03 \x01(\x01\x12$\n\x1ctimestamp_microseconds_value\x18\x04 \x01(\x03\x12\x35\n\tkey_value\x18\x05 \x01(\x0b\x32\".google.appengine.datastore.v4.Key\x12\x16\n\x0e\x62lob_key_value\x18\x10 \x01(\t\x12\x14\n\x0cstring_value\x18\x11 \x01(\t\x12\x12\n\nblob_value\x18\x12 \x01(\x0c\x12;\n\x0c\x65ntity_value\x18\x06 \x01(\x0b\x32%.google.appengine.datastore.v4.Entity\x12@\n\x0fgeo_point_value\x18\x08 \x01(\x0b\x32\'.google.appengine.datastore.v4.GeoPoint\x12\x38\n\nlist_value\x18\x07 \x03(\x0b\x32$.google.appengine.datastore.v4.Value\x12\x0f\n\x07meaning\x18\x0e \x01(\x05\x12\x15\n\x07indexed\x18\x0f \x01(\x08:\x04true\"\xb6\x01\n\x08Property\x12\x0c\n\x04name\x18\x01 \x02(\t\x12#\n\x10\x64\x65precated_multi\x18\x02 \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12\x42\n\x10\x64\x65precated_value\x18\x03 \x03(\x0b\x32$.google.appengine.datastore.v4.ValueB\x02\x18\x01\x12\x33\n\x05value\x18\x04 \x01(\x0b\x32$.google.appengine.datastore.v4.Value\"t\n\x06\x45ntity\x12/\n\x03key\x18\x01 \x01(\x0b\x32\".google.appengine.datastore.v4.Key\x12\x39\n\x08property\x18\x02 \x03(\x0b\x32\'.google.appengine.datastore.v4.PropertyB\'\n%com.google.google.appengine.datastore'
)



_PARTITIONID_CONSTANTS = _descriptor.EnumDescriptor(
  name='Constants',
  full_name='google.appengine.datastore.v4.PartitionId.Constants',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MAX_DIMENSION_TAG', index=0, number=100,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=131,
  serialized_end=165,
)
_sym_db.RegisterEnumDescriptor(_PARTITIONID_CONSTANTS)


_PARTITIONID = _descriptor.Descriptor(
  name='PartitionId',
  full_name='google.appengine.datastore.v4.PartitionId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dataset_id', full_name='google.appengine.datastore.v4.PartitionId.dataset_id', index=0,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='namespace', full_name='google.appengine.datastore.v4.PartitionId.namespace', index=1,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PARTITIONID_CONSTANTS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=165,
)


_KEY_PATHELEMENT = _descriptor.Descriptor(
  name='PathElement',
  full_name='google.appengine.datastore.v4.Key.PathElement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='kind', full_name='google.appengine.datastore.v4.Key.PathElement.kind', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.appengine.datastore.v4.Key.PathElement.id', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.appengine.datastore.v4.Key.PathElement.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=311,
  serialized_end=364,
)

_KEY = _descriptor.Descriptor(
  name='Key',
  full_name='google.appengine.datastore.v4.Key',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='partition_id', full_name='google.appengine.datastore.v4.Key.partition_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='path_element', full_name='google.appengine.datastore.v4.Key.path_element', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_KEY_PATHELEMENT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=168,
  serialized_end=364,
)


_GEOPOINT = _descriptor.Descriptor(
  name='GeoPoint',
  full_name='google.appengine.datastore.v4.GeoPoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='latitude', full_name='google.appengine.datastore.v4.GeoPoint.latitude', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='google.appengine.datastore.v4.GeoPoint.longitude', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=366,
  serialized_end=413,
)


_VALUE = _descriptor.Descriptor(
  name='Value',
  full_name='google.appengine.datastore.v4.Value',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='boolean_value', full_name='google.appengine.datastore.v4.Value.boolean_value', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='integer_value', full_name='google.appengine.datastore.v4.Value.integer_value', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='double_value', full_name='google.appengine.datastore.v4.Value.double_value', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp_microseconds_value', full_name='google.appengine.datastore.v4.Value.timestamp_microseconds_value', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key_value', full_name='google.appengine.datastore.v4.Value.key_value', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='blob_key_value', full_name='google.appengine.datastore.v4.Value.blob_key_value', index=5,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='string_value', full_name='google.appengine.datastore.v4.Value.string_value', index=6,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='blob_value', full_name='google.appengine.datastore.v4.Value.blob_value', index=7,
      number=18, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_value', full_name='google.appengine.datastore.v4.Value.entity_value', index=8,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='geo_point_value', full_name='google.appengine.datastore.v4.Value.geo_point_value', index=9,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='list_value', full_name='google.appengine.datastore.v4.Value.list_value', index=10,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='meaning', full_name='google.appengine.datastore.v4.Value.meaning', index=11,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='indexed', full_name='google.appengine.datastore.v4.Value.indexed', index=12,
      number=15, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=416,
  serialized_end=875,
)


_PROPERTY = _descriptor.Descriptor(
  name='Property',
  full_name='google.appengine.datastore.v4.Property',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='google.appengine.datastore.v4.Property.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_multi', full_name='google.appengine.datastore.v4.Property.deprecated_multi', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_value', full_name='google.appengine.datastore.v4.Property.deprecated_value', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.datastore.v4.Property.value', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=878,
  serialized_end=1060,
)


_ENTITY = _descriptor.Descriptor(
  name='Entity',
  full_name='google.appengine.datastore.v4.Entity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.datastore.v4.Entity.key', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='property', full_name='google.appengine.datastore.v4.Entity.property', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1062,
  serialized_end=1178,
)

_PARTITIONID_CONSTANTS.containing_type = _PARTITIONID
_KEY_PATHELEMENT.containing_type = _KEY
_KEY.fields_by_name['partition_id'].message_type = _PARTITIONID
_KEY.fields_by_name['path_element'].message_type = _KEY_PATHELEMENT
_VALUE.fields_by_name['key_value'].message_type = _KEY
_VALUE.fields_by_name['entity_value'].message_type = _ENTITY
_VALUE.fields_by_name['geo_point_value'].message_type = _GEOPOINT
_VALUE.fields_by_name['list_value'].message_type = _VALUE
_PROPERTY.fields_by_name['deprecated_value'].message_type = _VALUE
_PROPERTY.fields_by_name['value'].message_type = _VALUE
_ENTITY.fields_by_name['key'].message_type = _KEY
_ENTITY.fields_by_name['property'].message_type = _PROPERTY
DESCRIPTOR.message_types_by_name['PartitionId'] = _PARTITIONID
DESCRIPTOR.message_types_by_name['Key'] = _KEY
DESCRIPTOR.message_types_by_name['GeoPoint'] = _GEOPOINT
DESCRIPTOR.message_types_by_name['Value'] = _VALUE
DESCRIPTOR.message_types_by_name['Property'] = _PROPERTY
DESCRIPTOR.message_types_by_name['Entity'] = _ENTITY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PartitionId = _reflection.GeneratedProtocolMessageType('PartitionId', (_message.Message,), {
  'DESCRIPTOR' : _PARTITIONID,
  '__module__' : 'google.appengine.datastore.entity_v4_pb2'

  })
_sym_db.RegisterMessage(PartitionId)

Key = _reflection.GeneratedProtocolMessageType('Key', (_message.Message,), {

  'PathElement' : _reflection.GeneratedProtocolMessageType('PathElement', (_message.Message,), {
    'DESCRIPTOR' : _KEY_PATHELEMENT,
    '__module__' : 'google.appengine.datastore.entity_v4_pb2'

    })
  ,
  'DESCRIPTOR' : _KEY,
  '__module__' : 'google.appengine.datastore.entity_v4_pb2'

  })
_sym_db.RegisterMessage(Key)
_sym_db.RegisterMessage(Key.PathElement)

GeoPoint = _reflection.GeneratedProtocolMessageType('GeoPoint', (_message.Message,), {
  'DESCRIPTOR' : _GEOPOINT,
  '__module__' : 'google.appengine.datastore.entity_v4_pb2'

  })
_sym_db.RegisterMessage(GeoPoint)

Value = _reflection.GeneratedProtocolMessageType('Value', (_message.Message,), {
  'DESCRIPTOR' : _VALUE,
  '__module__' : 'google.appengine.datastore.entity_v4_pb2'

  })
_sym_db.RegisterMessage(Value)

Property = _reflection.GeneratedProtocolMessageType('Property', (_message.Message,), {
  'DESCRIPTOR' : _PROPERTY,
  '__module__' : 'google.appengine.datastore.entity_v4_pb2'

  })
_sym_db.RegisterMessage(Property)

Entity = _reflection.GeneratedProtocolMessageType('Entity', (_message.Message,), {
  'DESCRIPTOR' : _ENTITY,
  '__module__' : 'google.appengine.datastore.entity_v4_pb2'

  })
_sym_db.RegisterMessage(Entity)


DESCRIPTOR._options = None
_PROPERTY.fields_by_name['deprecated_multi']._options = None
_PROPERTY.fields_by_name['deprecated_value']._options = None

