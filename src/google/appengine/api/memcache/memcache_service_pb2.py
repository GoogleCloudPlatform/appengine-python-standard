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
  name='google/appengine/api/memcache/memcache_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n!com.google.appengine.api.memcacheB\021MemcacheServicePb\210\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n4google/appengine/api/memcache/memcache_service.proto\x12\x10google.appengine\"\x94\x01\n\x14MemcacheServiceError\"|\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x15\n\x11UNSPECIFIED_ERROR\x10\x01\x12\x15\n\x11NAMESPACE_NOT_SET\x10\x02\x12\x15\n\x11PERMISSION_DENIED\x10\x03\x12\x11\n\rINVALID_VALUE\x10\x06\x12\x0f\n\x0bUNAVAILABLE\x10\t\"\x1d\n\x0b\x41ppOverride\x12\x0e\n\x06\x61pp_id\x18\x01 \x02(\t\"y\n\x12MemcacheGetRequest\x12\x0b\n\x03key\x18\x01 \x03(\x0c\x12\x14\n\nname_space\x18\x02 \x01(\t:\x00\x12\x0f\n\x07\x66or_cas\x18\x04 \x01(\x08\x12/\n\x08override\x18\x05 \x01(\x0b\x32\x1d.google.appengine.AppOverride\"\xe3\x02\n\x13MemcacheGetResponse\x12\x38\n\x04item\x18\x01 \x03(\n2*.google.appengine.MemcacheGetResponse.Item\x12G\n\nget_status\x18\x07 \x03(\x0e\x32\x33.google.appengine.MemcacheGetResponse.GetStatusCode\x1a]\n\x04Item\x12\x0b\n\x03key\x18\x02 \x02(\x0c\x12\r\n\x05value\x18\x03 \x02(\x0c\x12\r\n\x05\x66lags\x18\x04 \x01(\x07\x12\x0e\n\x06\x63\x61s_id\x18\x05 \x01(\x06\x12\x1a\n\x12\x65xpires_in_seconds\x18\x06 \x01(\x05\"j\n\rGetStatusCode\x12\x07\n\x03HIT\x10\x01\x12\x08\n\x04MISS\x10\x02\x12\r\n\tTRUNCATED\x10\x03\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x04\x12\x0f\n\x0bUNREACHABLE\x10\x05\x12\x0f\n\x0bOTHER_ERROR\x10\x06\"\x83\x03\n\x12MemcacheSetRequest\x12\x37\n\x04item\x18\x01 \x03(\n2).google.appengine.MemcacheSetRequest.Item\x12\x14\n\nname_space\x18\x07 \x01(\t:\x00\x12/\n\x08override\x18\n \x01(\x0b\x32\x1d.google.appengine.AppOverride\x1a\xb7\x01\n\x04Item\x12\x0b\n\x03key\x18\x02 \x02(\x0c\x12\r\n\x05value\x18\x03 \x02(\x0c\x12\r\n\x05\x66lags\x18\x04 \x01(\x07\x12G\n\nset_policy\x18\x05 \x01(\x0e\x32..google.appengine.MemcacheSetRequest.SetPolicy:\x03SET\x12\x1a\n\x0f\x65xpiration_time\x18\x06 \x01(\x07:\x01\x30\x12\x0e\n\x06\x63\x61s_id\x18\x08 \x01(\x06\x12\x0f\n\x07\x66or_cas\x18\t \x01(\x08\"3\n\tSetPolicy\x12\x07\n\x03SET\x10\x01\x12\x07\n\x03\x41\x44\x44\x10\x02\x12\x0b\n\x07REPLACE\x10\x03\x12\x07\n\x03\x43\x41S\x10\x04\"\xdb\x01\n\x13MemcacheSetResponse\x12G\n\nset_status\x18\x01 \x03(\x0e\x32\x33.google.appengine.MemcacheSetResponse.SetStatusCode\"{\n\rSetStatusCode\x12\n\n\x06STORED\x10\x01\x12\x0e\n\nNOT_STORED\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\n\n\x06\x45XISTS\x10\x04\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x05\x12\x0f\n\x0bUNREACHABLE\x10\x06\x12\x0f\n\x0bOTHER_ERROR\x10\x07\"\xc7\x01\n\x15MemcacheDeleteRequest\x12:\n\x04item\x18\x01 \x03(\n2,.google.appengine.MemcacheDeleteRequest.Item\x12\x14\n\nname_space\x18\x04 \x01(\t:\x00\x12/\n\x08override\x18\x05 \x01(\x0b\x32\x1d.google.appengine.AppOverride\x1a+\n\x04Item\x12\x0b\n\x03key\x18\x02 \x02(\x0c\x12\x16\n\x0b\x64\x65lete_time\x18\x03 \x01(\x07:\x01\x30\"\xd3\x01\n\x16MemcacheDeleteResponse\x12P\n\rdelete_status\x18\x01 \x03(\x0e\x32\x39.google.appengine.MemcacheDeleteResponse.DeleteStatusCode\"g\n\x10\x44\x65leteStatusCode\x12\x0b\n\x07\x44\x45LETED\x10\x01\x12\r\n\tNOT_FOUND\x10\x02\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x03\x12\x0f\n\x0bUNREACHABLE\x10\x04\x12\x0f\n\x0bOTHER_ERROR\x10\x05\"\xad\x02\n\x18MemcacheIncrementRequest\x12\x0b\n\x03key\x18\x01 \x02(\x0c\x12\x14\n\nname_space\x18\x04 \x01(\t:\x00\x12\x10\n\x05\x64\x65lta\x18\x02 \x01(\x04:\x01\x31\x12R\n\tdirection\x18\x03 \x01(\x0e\x32\x34.google.appengine.MemcacheIncrementRequest.Direction:\tINCREMENT\x12\x15\n\rinitial_value\x18\x05 \x01(\x04\x12\x15\n\rinitial_flags\x18\x06 \x01(\x07\x12/\n\x08override\x18\x07 \x01(\x0b\x32\x1d.google.appengine.AppOverride\")\n\tDirection\x12\r\n\tINCREMENT\x10\x01\x12\r\n\tDECREMENT\x10\x02\"\xfd\x01\n\x19MemcacheIncrementResponse\x12\x11\n\tnew_value\x18\x01 \x01(\x04\x12Y\n\x10increment_status\x18\x02 \x01(\x0e\x32?.google.appengine.MemcacheIncrementResponse.IncrementStatusCode\"r\n\x13IncrementStatusCode\x12\x06\n\x02OK\x10\x01\x12\x0f\n\x0bNOT_CHANGED\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x04\x12\x0f\n\x0bUNREACHABLE\x10\x05\x12\x0f\n\x0bOTHER_ERROR\x10\x06\"\xa0\x01\n\x1dMemcacheBatchIncrementRequest\x12\x14\n\nname_space\x18\x01 \x01(\t:\x00\x12\x38\n\x04item\x18\x02 \x03(\x0b\x32*.google.appengine.MemcacheIncrementRequest\x12/\n\x08override\x18\x03 \x01(\x0b\x32\x1d.google.appengine.AppOverride\"[\n\x1eMemcacheBatchIncrementResponse\x12\x39\n\x04item\x18\x01 \x03(\x0b\x32+.google.appengine.MemcacheIncrementResponse\"G\n\x14MemcacheFlushRequest\x12/\n\x08override\x18\x01 \x01(\x0b\x32\x1d.google.appengine.AppOverride\"\x17\n\x15MemcacheFlushResponse\"d\n\x14MemcacheStatsRequest\x12/\n\x08override\x18\x01 \x01(\x0b\x32\x1d.google.appengine.AppOverride\x12\x1b\n\x10max_hotkey_count\x18\x02 \x01(\x05:\x01\x30\"\xb1\x01\n\x14MergedNamespaceStats\x12\x0c\n\x04hits\x18\x01 \x02(\x04\x12\x0e\n\x06misses\x18\x02 \x02(\x04\x12\x11\n\tbyte_hits\x18\x03 \x02(\x04\x12\r\n\x05items\x18\x04 \x02(\x04\x12\r\n\x05\x62ytes\x18\x05 \x02(\x04\x12\x17\n\x0foldest_item_age\x18\x06 \x02(\x07\x12\x31\n\x07hotkeys\x18\x07 \x03(\x0b\x32 .google.appengine.MemcacheHotKey\">\n\x0eMemcacheHotKey\x12\x0b\n\x03key\x18\x01 \x02(\x0c\x12\x0b\n\x03qps\x18\x02 \x02(\x01\x12\x12\n\nname_space\x18\x03 \x01(\t\"N\n\x15MemcacheStatsResponse\x12\x35\n\x05stats\x18\x01 \x01(\x0b\x32&.google.appengine.MergedNamespaceStatsB9\n!com.google.appengine.api.memcacheB\x11MemcacheServicePb\x88\x01\x01'
)



_MEMCACHESERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.MemcacheServiceError.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED_ERROR', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NAMESPACE_NOT_SET', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PERMISSION_DENIED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_VALUE', index=4, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNAVAILABLE', index=5, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=99,
  serialized_end=223,
)
_sym_db.RegisterEnumDescriptor(_MEMCACHESERVICEERROR_ERRORCODE)

_MEMCACHEGETRESPONSE_GETSTATUSCODE = _descriptor.EnumDescriptor(
  name='GetStatusCode',
  full_name='google.appengine.MemcacheGetResponse.GetStatusCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HIT', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MISS', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRUNCATED', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEADLINE_EXCEEDED', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNREACHABLE', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OTHER_ERROR', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=629,
  serialized_end=735,
)
_sym_db.RegisterEnumDescriptor(_MEMCACHEGETRESPONSE_GETSTATUSCODE)

_MEMCACHESETREQUEST_SETPOLICY = _descriptor.EnumDescriptor(
  name='SetPolicy',
  full_name='google.appengine.MemcacheSetRequest.SetPolicy',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SET', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ADD', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REPLACE', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CAS', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1074,
  serialized_end=1125,
)
_sym_db.RegisterEnumDescriptor(_MEMCACHESETREQUEST_SETPOLICY)

_MEMCACHESETRESPONSE_SETSTATUSCODE = _descriptor.EnumDescriptor(
  name='SetStatusCode',
  full_name='google.appengine.MemcacheSetResponse.SetStatusCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STORED', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_STORED', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXISTS', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEADLINE_EXCEEDED', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNREACHABLE', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OTHER_ERROR', index=6, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1224,
  serialized_end=1347,
)
_sym_db.RegisterEnumDescriptor(_MEMCACHESETRESPONSE_SETSTATUSCODE)

_MEMCACHEDELETERESPONSE_DELETESTATUSCODE = _descriptor.EnumDescriptor(
  name='DeleteStatusCode',
  full_name='google.appengine.MemcacheDeleteResponse.DeleteStatusCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DELETED', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_FOUND', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEADLINE_EXCEEDED', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNREACHABLE', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OTHER_ERROR', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1660,
  serialized_end=1763,
)
_sym_db.RegisterEnumDescriptor(_MEMCACHEDELETERESPONSE_DELETESTATUSCODE)

_MEMCACHEINCREMENTREQUEST_DIRECTION = _descriptor.EnumDescriptor(
  name='Direction',
  full_name='google.appengine.MemcacheIncrementRequest.Direction',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INCREMENT', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DECREMENT', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2026,
  serialized_end=2067,
)
_sym_db.RegisterEnumDescriptor(_MEMCACHEINCREMENTREQUEST_DIRECTION)

_MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE = _descriptor.EnumDescriptor(
  name='IncrementStatusCode',
  full_name='google.appengine.MemcacheIncrementResponse.IncrementStatusCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_CHANGED', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEADLINE_EXCEEDED', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNREACHABLE', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OTHER_ERROR', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2209,
  serialized_end=2323,
)
_sym_db.RegisterEnumDescriptor(_MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE)


_MEMCACHESERVICEERROR = _descriptor.Descriptor(
  name='MemcacheServiceError',
  full_name='google.appengine.MemcacheServiceError',
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
    _MEMCACHESERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=223,
)


_APPOVERRIDE = _descriptor.Descriptor(
  name='AppOverride',
  full_name='google.appengine.AppOverride',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='google.appengine.AppOverride.app_id', index=0,
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
  serialized_start=225,
  serialized_end=254,
)


_MEMCACHEGETREQUEST = _descriptor.Descriptor(
  name='MemcacheGetRequest',
  full_name='google.appengine.MemcacheGetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.MemcacheGetRequest.key', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name_space', full_name='google.appengine.MemcacheGetRequest.name_space', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='for_cas', full_name='google.appengine.MemcacheGetRequest.for_cas', index=2,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='override', full_name='google.appengine.MemcacheGetRequest.override', index=3,
      number=5, type=11, cpp_type=10, label=1,
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
  serialized_start=256,
  serialized_end=377,
)


_MEMCACHEGETRESPONSE_ITEM = _descriptor.Descriptor(
  name='Item',
  full_name='google.appengine.MemcacheGetResponse.Item',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.MemcacheGetResponse.Item.key', index=0,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.MemcacheGetResponse.Item.value', index=1,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flags', full_name='google.appengine.MemcacheGetResponse.Item.flags', index=2,
      number=4, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cas_id', full_name='google.appengine.MemcacheGetResponse.Item.cas_id', index=3,
      number=5, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expires_in_seconds', full_name='google.appengine.MemcacheGetResponse.Item.expires_in_seconds', index=4,
      number=6, type=5, cpp_type=1, label=1,
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
  serialized_start=534,
  serialized_end=627,
)

_MEMCACHEGETRESPONSE = _descriptor.Descriptor(
  name='MemcacheGetResponse',
  full_name='google.appengine.MemcacheGetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='item', full_name='google.appengine.MemcacheGetResponse.item', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='get_status', full_name='google.appengine.MemcacheGetResponse.get_status', index=1,
      number=7, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_MEMCACHEGETRESPONSE_ITEM, ],
  enum_types=[
    _MEMCACHEGETRESPONSE_GETSTATUSCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=380,
  serialized_end=735,
)


_MEMCACHESETREQUEST_ITEM = _descriptor.Descriptor(
  name='Item',
  full_name='google.appengine.MemcacheSetRequest.Item',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.MemcacheSetRequest.Item.key', index=0,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.MemcacheSetRequest.Item.value', index=1,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flags', full_name='google.appengine.MemcacheSetRequest.Item.flags', index=2,
      number=4, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='set_policy', full_name='google.appengine.MemcacheSetRequest.Item.set_policy', index=3,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expiration_time', full_name='google.appengine.MemcacheSetRequest.Item.expiration_time', index=4,
      number=6, type=7, cpp_type=3, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cas_id', full_name='google.appengine.MemcacheSetRequest.Item.cas_id', index=5,
      number=8, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='for_cas', full_name='google.appengine.MemcacheSetRequest.Item.for_cas', index=6,
      number=9, type=8, cpp_type=7, label=1,
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
  serialized_start=889,
  serialized_end=1072,
)

_MEMCACHESETREQUEST = _descriptor.Descriptor(
  name='MemcacheSetRequest',
  full_name='google.appengine.MemcacheSetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='item', full_name='google.appengine.MemcacheSetRequest.item', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name_space', full_name='google.appengine.MemcacheSetRequest.name_space', index=1,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='override', full_name='google.appengine.MemcacheSetRequest.override', index=2,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_MEMCACHESETREQUEST_ITEM, ],
  enum_types=[
    _MEMCACHESETREQUEST_SETPOLICY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=738,
  serialized_end=1125,
)


_MEMCACHESETRESPONSE = _descriptor.Descriptor(
  name='MemcacheSetResponse',
  full_name='google.appengine.MemcacheSetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='set_status', full_name='google.appengine.MemcacheSetResponse.set_status', index=0,
      number=1, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MEMCACHESETRESPONSE_SETSTATUSCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1128,
  serialized_end=1347,
)


_MEMCACHEDELETEREQUEST_ITEM = _descriptor.Descriptor(
  name='Item',
  full_name='google.appengine.MemcacheDeleteRequest.Item',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.MemcacheDeleteRequest.Item.key', index=0,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='delete_time', full_name='google.appengine.MemcacheDeleteRequest.Item.delete_time', index=1,
      number=3, type=7, cpp_type=3, label=1,
      has_default_value=True, default_value=0,
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
  serialized_start=1506,
  serialized_end=1549,
)

_MEMCACHEDELETEREQUEST = _descriptor.Descriptor(
  name='MemcacheDeleteRequest',
  full_name='google.appengine.MemcacheDeleteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='item', full_name='google.appengine.MemcacheDeleteRequest.item', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name_space', full_name='google.appengine.MemcacheDeleteRequest.name_space', index=1,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='override', full_name='google.appengine.MemcacheDeleteRequest.override', index=2,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_MEMCACHEDELETEREQUEST_ITEM, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1350,
  serialized_end=1549,
)


_MEMCACHEDELETERESPONSE = _descriptor.Descriptor(
  name='MemcacheDeleteResponse',
  full_name='google.appengine.MemcacheDeleteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='delete_status', full_name='google.appengine.MemcacheDeleteResponse.delete_status', index=0,
      number=1, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MEMCACHEDELETERESPONSE_DELETESTATUSCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1552,
  serialized_end=1763,
)


_MEMCACHEINCREMENTREQUEST = _descriptor.Descriptor(
  name='MemcacheIncrementRequest',
  full_name='google.appengine.MemcacheIncrementRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.MemcacheIncrementRequest.key', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name_space', full_name='google.appengine.MemcacheIncrementRequest.name_space', index=1,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='delta', full_name='google.appengine.MemcacheIncrementRequest.delta', index=2,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='direction', full_name='google.appengine.MemcacheIncrementRequest.direction', index=3,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='initial_value', full_name='google.appengine.MemcacheIncrementRequest.initial_value', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='initial_flags', full_name='google.appengine.MemcacheIncrementRequest.initial_flags', index=5,
      number=6, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='override', full_name='google.appengine.MemcacheIncrementRequest.override', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MEMCACHEINCREMENTREQUEST_DIRECTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1766,
  serialized_end=2067,
)


_MEMCACHEINCREMENTRESPONSE = _descriptor.Descriptor(
  name='MemcacheIncrementResponse',
  full_name='google.appengine.MemcacheIncrementResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='new_value', full_name='google.appengine.MemcacheIncrementResponse.new_value', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='increment_status', full_name='google.appengine.MemcacheIncrementResponse.increment_status', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2070,
  serialized_end=2323,
)


_MEMCACHEBATCHINCREMENTREQUEST = _descriptor.Descriptor(
  name='MemcacheBatchIncrementRequest',
  full_name='google.appengine.MemcacheBatchIncrementRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name_space', full_name='google.appengine.MemcacheBatchIncrementRequest.name_space', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='item', full_name='google.appengine.MemcacheBatchIncrementRequest.item', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='override', full_name='google.appengine.MemcacheBatchIncrementRequest.override', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=2326,
  serialized_end=2486,
)


_MEMCACHEBATCHINCREMENTRESPONSE = _descriptor.Descriptor(
  name='MemcacheBatchIncrementResponse',
  full_name='google.appengine.MemcacheBatchIncrementResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='item', full_name='google.appengine.MemcacheBatchIncrementResponse.item', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=2488,
  serialized_end=2579,
)


_MEMCACHEFLUSHREQUEST = _descriptor.Descriptor(
  name='MemcacheFlushRequest',
  full_name='google.appengine.MemcacheFlushRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='override', full_name='google.appengine.MemcacheFlushRequest.override', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=2581,
  serialized_end=2652,
)


_MEMCACHEFLUSHRESPONSE = _descriptor.Descriptor(
  name='MemcacheFlushResponse',
  full_name='google.appengine.MemcacheFlushResponse',
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
  serialized_start=2654,
  serialized_end=2677,
)


_MEMCACHESTATSREQUEST = _descriptor.Descriptor(
  name='MemcacheStatsRequest',
  full_name='google.appengine.MemcacheStatsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='override', full_name='google.appengine.MemcacheStatsRequest.override', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_hotkey_count', full_name='google.appengine.MemcacheStatsRequest.max_hotkey_count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
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
  serialized_start=2679,
  serialized_end=2779,
)


_MERGEDNAMESPACESTATS = _descriptor.Descriptor(
  name='MergedNamespaceStats',
  full_name='google.appengine.MergedNamespaceStats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='hits', full_name='google.appengine.MergedNamespaceStats.hits', index=0,
      number=1, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='misses', full_name='google.appengine.MergedNamespaceStats.misses', index=1,
      number=2, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='byte_hits', full_name='google.appengine.MergedNamespaceStats.byte_hits', index=2,
      number=3, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='items', full_name='google.appengine.MergedNamespaceStats.items', index=3,
      number=4, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bytes', full_name='google.appengine.MergedNamespaceStats.bytes', index=4,
      number=5, type=4, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='oldest_item_age', full_name='google.appengine.MergedNamespaceStats.oldest_item_age', index=5,
      number=6, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hotkeys', full_name='google.appengine.MergedNamespaceStats.hotkeys', index=6,
      number=7, type=11, cpp_type=10, label=3,
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
  serialized_start=2782,
  serialized_end=2959,
)


_MEMCACHEHOTKEY = _descriptor.Descriptor(
  name='MemcacheHotKey',
  full_name='google.appengine.MemcacheHotKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.MemcacheHotKey.key', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='qps', full_name='google.appengine.MemcacheHotKey.qps', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name_space', full_name='google.appengine.MemcacheHotKey.name_space', index=2,
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
  serialized_start=2961,
  serialized_end=3023,
)


_MEMCACHESTATSRESPONSE = _descriptor.Descriptor(
  name='MemcacheStatsResponse',
  full_name='google.appengine.MemcacheStatsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='stats', full_name='google.appengine.MemcacheStatsResponse.stats', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=3025,
  serialized_end=3103,
)

_MEMCACHESERVICEERROR_ERRORCODE.containing_type = _MEMCACHESERVICEERROR
_MEMCACHEGETREQUEST.fields_by_name['override'].message_type = _APPOVERRIDE
_MEMCACHEGETRESPONSE_ITEM.containing_type = _MEMCACHEGETRESPONSE
_MEMCACHEGETRESPONSE.fields_by_name['item'].message_type = _MEMCACHEGETRESPONSE_ITEM
_MEMCACHEGETRESPONSE.fields_by_name['get_status'].enum_type = _MEMCACHEGETRESPONSE_GETSTATUSCODE
_MEMCACHEGETRESPONSE_GETSTATUSCODE.containing_type = _MEMCACHEGETRESPONSE
_MEMCACHESETREQUEST_ITEM.fields_by_name['set_policy'].enum_type = _MEMCACHESETREQUEST_SETPOLICY
_MEMCACHESETREQUEST_ITEM.containing_type = _MEMCACHESETREQUEST
_MEMCACHESETREQUEST.fields_by_name['item'].message_type = _MEMCACHESETREQUEST_ITEM
_MEMCACHESETREQUEST.fields_by_name['override'].message_type = _APPOVERRIDE
_MEMCACHESETREQUEST_SETPOLICY.containing_type = _MEMCACHESETREQUEST
_MEMCACHESETRESPONSE.fields_by_name['set_status'].enum_type = _MEMCACHESETRESPONSE_SETSTATUSCODE
_MEMCACHESETRESPONSE_SETSTATUSCODE.containing_type = _MEMCACHESETRESPONSE
_MEMCACHEDELETEREQUEST_ITEM.containing_type = _MEMCACHEDELETEREQUEST
_MEMCACHEDELETEREQUEST.fields_by_name['item'].message_type = _MEMCACHEDELETEREQUEST_ITEM
_MEMCACHEDELETEREQUEST.fields_by_name['override'].message_type = _APPOVERRIDE
_MEMCACHEDELETERESPONSE.fields_by_name['delete_status'].enum_type = _MEMCACHEDELETERESPONSE_DELETESTATUSCODE
_MEMCACHEDELETERESPONSE_DELETESTATUSCODE.containing_type = _MEMCACHEDELETERESPONSE
_MEMCACHEINCREMENTREQUEST.fields_by_name['direction'].enum_type = _MEMCACHEINCREMENTREQUEST_DIRECTION
_MEMCACHEINCREMENTREQUEST.fields_by_name['override'].message_type = _APPOVERRIDE
_MEMCACHEINCREMENTREQUEST_DIRECTION.containing_type = _MEMCACHEINCREMENTREQUEST
_MEMCACHEINCREMENTRESPONSE.fields_by_name['increment_status'].enum_type = _MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE
_MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE.containing_type = _MEMCACHEINCREMENTRESPONSE
_MEMCACHEBATCHINCREMENTREQUEST.fields_by_name['item'].message_type = _MEMCACHEINCREMENTREQUEST
_MEMCACHEBATCHINCREMENTREQUEST.fields_by_name['override'].message_type = _APPOVERRIDE
_MEMCACHEBATCHINCREMENTRESPONSE.fields_by_name['item'].message_type = _MEMCACHEINCREMENTRESPONSE
_MEMCACHEFLUSHREQUEST.fields_by_name['override'].message_type = _APPOVERRIDE
_MEMCACHESTATSREQUEST.fields_by_name['override'].message_type = _APPOVERRIDE
_MERGEDNAMESPACESTATS.fields_by_name['hotkeys'].message_type = _MEMCACHEHOTKEY
_MEMCACHESTATSRESPONSE.fields_by_name['stats'].message_type = _MERGEDNAMESPACESTATS
DESCRIPTOR.message_types_by_name['MemcacheServiceError'] = _MEMCACHESERVICEERROR
DESCRIPTOR.message_types_by_name['AppOverride'] = _APPOVERRIDE
DESCRIPTOR.message_types_by_name['MemcacheGetRequest'] = _MEMCACHEGETREQUEST
DESCRIPTOR.message_types_by_name['MemcacheGetResponse'] = _MEMCACHEGETRESPONSE
DESCRIPTOR.message_types_by_name['MemcacheSetRequest'] = _MEMCACHESETREQUEST
DESCRIPTOR.message_types_by_name['MemcacheSetResponse'] = _MEMCACHESETRESPONSE
DESCRIPTOR.message_types_by_name['MemcacheDeleteRequest'] = _MEMCACHEDELETEREQUEST
DESCRIPTOR.message_types_by_name['MemcacheDeleteResponse'] = _MEMCACHEDELETERESPONSE
DESCRIPTOR.message_types_by_name['MemcacheIncrementRequest'] = _MEMCACHEINCREMENTREQUEST
DESCRIPTOR.message_types_by_name['MemcacheIncrementResponse'] = _MEMCACHEINCREMENTRESPONSE
DESCRIPTOR.message_types_by_name['MemcacheBatchIncrementRequest'] = _MEMCACHEBATCHINCREMENTREQUEST
DESCRIPTOR.message_types_by_name['MemcacheBatchIncrementResponse'] = _MEMCACHEBATCHINCREMENTRESPONSE
DESCRIPTOR.message_types_by_name['MemcacheFlushRequest'] = _MEMCACHEFLUSHREQUEST
DESCRIPTOR.message_types_by_name['MemcacheFlushResponse'] = _MEMCACHEFLUSHRESPONSE
DESCRIPTOR.message_types_by_name['MemcacheStatsRequest'] = _MEMCACHESTATSREQUEST
DESCRIPTOR.message_types_by_name['MergedNamespaceStats'] = _MERGEDNAMESPACESTATS
DESCRIPTOR.message_types_by_name['MemcacheHotKey'] = _MEMCACHEHOTKEY
DESCRIPTOR.message_types_by_name['MemcacheStatsResponse'] = _MEMCACHESTATSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MemcacheServiceError = _reflection.GeneratedProtocolMessageType('MemcacheServiceError', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHESERVICEERROR,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheServiceError)

AppOverride = _reflection.GeneratedProtocolMessageType('AppOverride', (_message.Message,), {
  'DESCRIPTOR' : _APPOVERRIDE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(AppOverride)

MemcacheGetRequest = _reflection.GeneratedProtocolMessageType('MemcacheGetRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEGETREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheGetRequest)

MemcacheGetResponse = _reflection.GeneratedProtocolMessageType('MemcacheGetResponse', (_message.Message,), {

  'Item' : _reflection.GeneratedProtocolMessageType('Item', (_message.Message,), {
    'DESCRIPTOR' : _MEMCACHEGETRESPONSE_ITEM,
    '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

    })
  ,
  'DESCRIPTOR' : _MEMCACHEGETRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheGetResponse)
_sym_db.RegisterMessage(MemcacheGetResponse.Item)

MemcacheSetRequest = _reflection.GeneratedProtocolMessageType('MemcacheSetRequest', (_message.Message,), {

  'Item' : _reflection.GeneratedProtocolMessageType('Item', (_message.Message,), {
    'DESCRIPTOR' : _MEMCACHESETREQUEST_ITEM,
    '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

    })
  ,
  'DESCRIPTOR' : _MEMCACHESETREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheSetRequest)
_sym_db.RegisterMessage(MemcacheSetRequest.Item)

MemcacheSetResponse = _reflection.GeneratedProtocolMessageType('MemcacheSetResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHESETRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheSetResponse)

MemcacheDeleteRequest = _reflection.GeneratedProtocolMessageType('MemcacheDeleteRequest', (_message.Message,), {

  'Item' : _reflection.GeneratedProtocolMessageType('Item', (_message.Message,), {
    'DESCRIPTOR' : _MEMCACHEDELETEREQUEST_ITEM,
    '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

    })
  ,
  'DESCRIPTOR' : _MEMCACHEDELETEREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheDeleteRequest)
_sym_db.RegisterMessage(MemcacheDeleteRequest.Item)

MemcacheDeleteResponse = _reflection.GeneratedProtocolMessageType('MemcacheDeleteResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEDELETERESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheDeleteResponse)

MemcacheIncrementRequest = _reflection.GeneratedProtocolMessageType('MemcacheIncrementRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEINCREMENTREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheIncrementRequest)

MemcacheIncrementResponse = _reflection.GeneratedProtocolMessageType('MemcacheIncrementResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEINCREMENTRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheIncrementResponse)

MemcacheBatchIncrementRequest = _reflection.GeneratedProtocolMessageType('MemcacheBatchIncrementRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEBATCHINCREMENTREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheBatchIncrementRequest)

MemcacheBatchIncrementResponse = _reflection.GeneratedProtocolMessageType('MemcacheBatchIncrementResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEBATCHINCREMENTRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheBatchIncrementResponse)

MemcacheFlushRequest = _reflection.GeneratedProtocolMessageType('MemcacheFlushRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEFLUSHREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheFlushRequest)

MemcacheFlushResponse = _reflection.GeneratedProtocolMessageType('MemcacheFlushResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEFLUSHRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheFlushResponse)

MemcacheStatsRequest = _reflection.GeneratedProtocolMessageType('MemcacheStatsRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHESTATSREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheStatsRequest)

MergedNamespaceStats = _reflection.GeneratedProtocolMessageType('MergedNamespaceStats', (_message.Message,), {
  'DESCRIPTOR' : _MERGEDNAMESPACESTATS,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MergedNamespaceStats)

MemcacheHotKey = _reflection.GeneratedProtocolMessageType('MemcacheHotKey', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEHOTKEY,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheHotKey)

MemcacheStatsResponse = _reflection.GeneratedProtocolMessageType('MemcacheStatsResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHESTATSRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheStatsResponse)


DESCRIPTOR._options = None

