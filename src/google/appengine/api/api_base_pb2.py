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
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#google/appengine/api/api_base.proto\x12\x15google.appengine.base\"\x1c\n\x0bStringProto\x12\r\n\x05value\x18\x01 \x02(\t\"\x1f\n\x0eInteger32Proto\x12\r\n\x05value\x18\x01 \x02(\x05\"\x1f\n\x0eInteger64Proto\x12\r\n\x05value\x18\x01 \x02(\x03\"\x1a\n\tBoolProto\x12\r\n\x05value\x18\x01 \x02(\x08\"\x1c\n\x0b\x44oubleProto\x12\r\n\x05value\x18\x01 \x02(\x01\"\x1f\n\nBytesProto\x12\x11\n\x05value\x18\x01 \x02(\x0c\x42\x02\x08\x01\"\x0b\n\tVoidProtoB,\n\x1f\x63om.google.google.appengine.apiB\tApiBasePb')



_STRINGPROTO = DESCRIPTOR.message_types_by_name['StringProto']
_INTEGER32PROTO = DESCRIPTOR.message_types_by_name['Integer32Proto']
_INTEGER64PROTO = DESCRIPTOR.message_types_by_name['Integer64Proto']
_BOOLPROTO = DESCRIPTOR.message_types_by_name['BoolProto']
_DOUBLEPROTO = DESCRIPTOR.message_types_by_name['DoubleProto']
_BYTESPROTO = DESCRIPTOR.message_types_by_name['BytesProto']
_VOIDPROTO = DESCRIPTOR.message_types_by_name['VoidProto']
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

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\037com.google.google.appengine.apiB\tApiBasePb'
  _BYTESPROTO.fields_by_name['value']._options = None
  _BYTESPROTO.fields_by_name['value']._serialized_options = b'\010\001'
  _STRINGPROTO._serialized_start=62
  _STRINGPROTO._serialized_end=90
  _INTEGER32PROTO._serialized_start=92
  _INTEGER32PROTO._serialized_end=123
  _INTEGER64PROTO._serialized_start=125
  _INTEGER64PROTO._serialized_end=156
  _BOOLPROTO._serialized_start=158
  _BOOLPROTO._serialized_end=184
  _DOUBLEPROTO._serialized_start=186
  _DOUBLEPROTO._serialized_end=214
  _BYTESPROTO._serialized_start=216
  _BYTESPROTO._serialized_end=247
  _VOIDPROTO._serialized_start=249
  _VOIDPROTO._serialized_end=260

