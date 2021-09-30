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
  name='google/appengine/api/system/system_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n\037com.google.appengine.api.systemB\017SystemServicePb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n0google/appengine/api/system/system_service.proto\x12\x10google.appengine\"f\n\x12SystemServiceError\"P\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x12\n\x0eINTERNAL_ERROR\x10\x01\x12\x14\n\x10\x42\x41\x43KEND_REQUIRED\x10\x02\x12\x11\n\rLIMIT_REACHED\x10\x03\"t\n\nSystemStat\x12\x0f\n\x07\x63urrent\x18\x01 \x01(\x01\x12\x11\n\taverage1m\x18\x03 \x01(\x01\x12\x12\n\naverage10m\x18\x04 \x01(\x01\x12\r\n\x05total\x18\x02 \x01(\x01\x12\x0e\n\x06rate1m\x18\x05 \x01(\x01\x12\x0f\n\x07rate10m\x18\x06 \x01(\x01\"\x17\n\x15GetSystemStatsRequest\"q\n\x16GetSystemStatsResponse\x12)\n\x03\x63pu\x18\x01 \x01(\x0b\x32\x1c.google.appengine.SystemStat\x12,\n\x06memory\x18\x02 \x01(\x0b\x32\x1c.google.appengine.SystemStat\"\x1f\n\x1dStartBackgroundRequestRequest\"4\n\x1eStartBackgroundRequestResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\tB2\n\x1f\x63om.google.appengine.api.systemB\x0fSystemServicePb'
)



_SYSTEMSERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.SystemServiceError.ErrorCode',
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
      name='INTERNAL_ERROR', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BACKEND_REQUIRED', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LIMIT_REACHED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=92,
  serialized_end=172,
)
_sym_db.RegisterEnumDescriptor(_SYSTEMSERVICEERROR_ERRORCODE)


_SYSTEMSERVICEERROR = _descriptor.Descriptor(
  name='SystemServiceError',
  full_name='google.appengine.SystemServiceError',
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
    _SYSTEMSERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=70,
  serialized_end=172,
)


_SYSTEMSTAT = _descriptor.Descriptor(
  name='SystemStat',
  full_name='google.appengine.SystemStat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='current', full_name='google.appengine.SystemStat.current', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='average1m', full_name='google.appengine.SystemStat.average1m', index=1,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='average10m', full_name='google.appengine.SystemStat.average10m', index=2,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total', full_name='google.appengine.SystemStat.total', index=3,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rate1m', full_name='google.appengine.SystemStat.rate1m', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rate10m', full_name='google.appengine.SystemStat.rate10m', index=5,
      number=6, type=1, cpp_type=5, label=1,
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
  serialized_start=174,
  serialized_end=290,
)


_GETSYSTEMSTATSREQUEST = _descriptor.Descriptor(
  name='GetSystemStatsRequest',
  full_name='google.appengine.GetSystemStatsRequest',
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
  serialized_start=292,
  serialized_end=315,
)


_GETSYSTEMSTATSRESPONSE = _descriptor.Descriptor(
  name='GetSystemStatsResponse',
  full_name='google.appengine.GetSystemStatsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cpu', full_name='google.appengine.GetSystemStatsResponse.cpu', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='memory', full_name='google.appengine.GetSystemStatsResponse.memory', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=317,
  serialized_end=430,
)


_STARTBACKGROUNDREQUESTREQUEST = _descriptor.Descriptor(
  name='StartBackgroundRequestRequest',
  full_name='google.appengine.StartBackgroundRequestRequest',
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
  serialized_start=432,
  serialized_end=463,
)


_STARTBACKGROUNDREQUESTRESPONSE = _descriptor.Descriptor(
  name='StartBackgroundRequestResponse',
  full_name='google.appengine.StartBackgroundRequestResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_id', full_name='google.appengine.StartBackgroundRequestResponse.request_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=465,
  serialized_end=517,
)

_SYSTEMSERVICEERROR_ERRORCODE.containing_type = _SYSTEMSERVICEERROR
_GETSYSTEMSTATSRESPONSE.fields_by_name['cpu'].message_type = _SYSTEMSTAT
_GETSYSTEMSTATSRESPONSE.fields_by_name['memory'].message_type = _SYSTEMSTAT
DESCRIPTOR.message_types_by_name['SystemServiceError'] = _SYSTEMSERVICEERROR
DESCRIPTOR.message_types_by_name['SystemStat'] = _SYSTEMSTAT
DESCRIPTOR.message_types_by_name['GetSystemStatsRequest'] = _GETSYSTEMSTATSREQUEST
DESCRIPTOR.message_types_by_name['GetSystemStatsResponse'] = _GETSYSTEMSTATSRESPONSE
DESCRIPTOR.message_types_by_name['StartBackgroundRequestRequest'] = _STARTBACKGROUNDREQUESTREQUEST
DESCRIPTOR.message_types_by_name['StartBackgroundRequestResponse'] = _STARTBACKGROUNDREQUESTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SystemServiceError = _reflection.GeneratedProtocolMessageType('SystemServiceError', (_message.Message,), {
  'DESCRIPTOR' : _SYSTEMSERVICEERROR,
  '__module__' : 'google.appengine.api.system.system_service_pb2'

  })
_sym_db.RegisterMessage(SystemServiceError)

SystemStat = _reflection.GeneratedProtocolMessageType('SystemStat', (_message.Message,), {
  'DESCRIPTOR' : _SYSTEMSTAT,
  '__module__' : 'google.appengine.api.system.system_service_pb2'

  })
_sym_db.RegisterMessage(SystemStat)

GetSystemStatsRequest = _reflection.GeneratedProtocolMessageType('GetSystemStatsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSYSTEMSTATSREQUEST,
  '__module__' : 'google.appengine.api.system.system_service_pb2'

  })
_sym_db.RegisterMessage(GetSystemStatsRequest)

GetSystemStatsResponse = _reflection.GeneratedProtocolMessageType('GetSystemStatsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETSYSTEMSTATSRESPONSE,
  '__module__' : 'google.appengine.api.system.system_service_pb2'

  })
_sym_db.RegisterMessage(GetSystemStatsResponse)

StartBackgroundRequestRequest = _reflection.GeneratedProtocolMessageType('StartBackgroundRequestRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTBACKGROUNDREQUESTREQUEST,
  '__module__' : 'google.appengine.api.system.system_service_pb2'

  })
_sym_db.RegisterMessage(StartBackgroundRequestRequest)

StartBackgroundRequestResponse = _reflection.GeneratedProtocolMessageType('StartBackgroundRequestResponse', (_message.Message,), {
  'DESCRIPTOR' : _STARTBACKGROUNDREQUESTRESPONSE,
  '__module__' : 'google.appengine.api.system.system_service_pb2'

  })
_sym_db.RegisterMessage(StartBackgroundRequestResponse)


DESCRIPTOR._options = None

