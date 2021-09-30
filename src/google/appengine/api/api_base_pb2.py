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
  name='google/appengine/api/api_base.proto',
  package='google.appengine.base',
  syntax='proto2',
  serialized_options=b'\n\037com.google.google.appengine.apiB\tApiBasePb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n#google/appengine/api/api_base.proto\x12\x15google.appengine.base\"\x1c\n\x0bStringProto\x12\r\n\x05value\x18\x01 \x02(\t\"\x1f\n\x0eInteger32Proto\x12\r\n\x05value\x18\x01 \x02(\x05\"\x1f\n\x0eInteger64Proto\x12\r\n\x05value\x18\x01 \x02(\x03\"\x1a\n\tBoolProto\x12\r\n\x05value\x18\x01 \x02(\x08\"\x1c\n\x0b\x44oubleProto\x12\r\n\x05value\x18\x01 \x02(\x01\"\x1f\n\nBytesProto\x12\x11\n\x05value\x18\x01 \x02(\x0c\x42\x02\x08\x01\"\x0b\n\tVoidProtoB,\n\x1f\x63om.google.google.appengine.apiB\tApiBasePb'
)




_STRINGPROTO = _descriptor.Descriptor(
  name='StringProto',
  full_name='google.appengine.base.StringProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.base.StringProto.value', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  serialized_start=62,
  serialized_end=90,
)


_INTEGER32PROTO = _descriptor.Descriptor(
  name='Integer32Proto',
  full_name='google.appengine.base.Integer32Proto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.base.Integer32Proto.value', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=92,
  serialized_end=123,
)


_INTEGER64PROTO = _descriptor.Descriptor(
  name='Integer64Proto',
  full_name='google.appengine.base.Integer64Proto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.base.Integer64Proto.value', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=125,
  serialized_end=156,
)


_BOOLPROTO = _descriptor.Descriptor(
  name='BoolProto',
  full_name='google.appengine.base.BoolProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.base.BoolProto.value', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
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
  serialized_start=158,
  serialized_end=184,
)


_DOUBLEPROTO = _descriptor.Descriptor(
  name='DoubleProto',
  full_name='google.appengine.base.DoubleProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.base.DoubleProto.value', index=0,
      number=1, type=1, cpp_type=5, label=2,
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
  serialized_start=186,
  serialized_end=214,
)


_BYTESPROTO = _descriptor.Descriptor(
  name='BytesProto',
  full_name='google.appengine.base.BytesProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.base.BytesProto.value', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=216,
  serialized_end=247,
)


_VOIDPROTO = _descriptor.Descriptor(
  name='VoidProto',
  full_name='google.appengine.base.VoidProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=249,
  serialized_end=260,
)

DESCRIPTOR.message_types_by_name['StringProto'] = _STRINGPROTO
DESCRIPTOR.message_types_by_name['Integer32Proto'] = _INTEGER32PROTO
DESCRIPTOR.message_types_by_name['Integer64Proto'] = _INTEGER64PROTO
DESCRIPTOR.message_types_by_name['BoolProto'] = _BOOLPROTO
DESCRIPTOR.message_types_by_name['DoubleProto'] = _DOUBLEPROTO
DESCRIPTOR.message_types_by_name['BytesProto'] = _BYTESPROTO
DESCRIPTOR.message_types_by_name['VoidProto'] = _VOIDPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StringProto = _reflection.GeneratedProtocolMessageType('StringProto', (_message.Message,), {
  'DESCRIPTOR' : _STRINGPROTO,
  '__module__' : 'google.appengine.api.api_base_pb2'

  })
_sym_db.RegisterMessage(StringProto)

Integer32Proto = _reflection.GeneratedProtocolMessageType('Integer32Proto', (_message.Message,), {
  'DESCRIPTOR' : _INTEGER32PROTO,
  '__module__' : 'google.appengine.api.api_base_pb2'

  })
_sym_db.RegisterMessage(Integer32Proto)

Integer64Proto = _reflection.GeneratedProtocolMessageType('Integer64Proto', (_message.Message,), {
  'DESCRIPTOR' : _INTEGER64PROTO,
  '__module__' : 'google.appengine.api.api_base_pb2'

  })
_sym_db.RegisterMessage(Integer64Proto)

BoolProto = _reflection.GeneratedProtocolMessageType('BoolProto', (_message.Message,), {
  'DESCRIPTOR' : _BOOLPROTO,
  '__module__' : 'google.appengine.api.api_base_pb2'

  })
_sym_db.RegisterMessage(BoolProto)

DoubleProto = _reflection.GeneratedProtocolMessageType('DoubleProto', (_message.Message,), {
  'DESCRIPTOR' : _DOUBLEPROTO,
  '__module__' : 'google.appengine.api.api_base_pb2'

  })
_sym_db.RegisterMessage(DoubleProto)

BytesProto = _reflection.GeneratedProtocolMessageType('BytesProto', (_message.Message,), {
  'DESCRIPTOR' : _BYTESPROTO,
  '__module__' : 'google.appengine.api.api_base_pb2'

  })
_sym_db.RegisterMessage(BytesProto)

VoidProto = _reflection.GeneratedProtocolMessageType('VoidProto', (_message.Message,), {
  'DESCRIPTOR' : _VOIDPROTO,
  '__module__' : 'google.appengine.api.api_base_pb2'

  })
_sym_db.RegisterMessage(VoidProto)


DESCRIPTOR._options = None
_BYTESPROTO.fields_by_name['value']._options = None

