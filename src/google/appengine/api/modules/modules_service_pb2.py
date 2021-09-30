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
  name='google/appengine/api/modules/modules_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n com.google.appengine.api.modulesB\020ModulesServicePb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n2google/appengine/api/modules/modules_service.proto\x12\x10google.appengine\"\x95\x01\n\x13ModulesServiceError\"~\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x12\n\x0eINVALID_MODULE\x10\x01\x12\x13\n\x0fINVALID_VERSION\x10\x02\x12\x15\n\x11INVALID_INSTANCES\x10\x03\x12\x13\n\x0fTRANSIENT_ERROR\x10\x04\x12\x14\n\x10UNEXPECTED_STATE\x10\x05\"\x13\n\x11GetModulesRequest\"$\n\x12GetModulesResponse\x12\x0e\n\x06module\x18\x01 \x03(\t\"$\n\x12GetVersionsRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\"&\n\x13GetVersionsResponse\x12\x0f\n\x07version\x18\x01 \x03(\t\"*\n\x18GetDefaultVersionRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\",\n\x19GetDefaultVersionResponse\x12\x0f\n\x07version\x18\x01 \x01(\t\"9\n\x16GetNumInstancesRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\",\n\x17GetNumInstancesResponse\x12\x11\n\tinstances\x18\x01 \x01(\x03\"L\n\x16SetNumInstancesRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x11\n\tinstances\x18\x03 \x02(\x03\"\x19\n\x17SetNumInstancesResponse\"5\n\x12StartModuleRequest\x12\x0e\n\x06module\x18\x01 \x02(\t\x12\x0f\n\x07version\x18\x02 \x02(\t\"\x15\n\x13StartModuleResponse\"4\n\x11StopModuleRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\"\x14\n\x12StopModuleResponse\"G\n\x12GetHostnameRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x10\n\x08instance\x18\x03 \x01(\t\"\'\n\x13GetHostnameResponse\x12\x10\n\x08hostname\x18\x01 \x01(\tB4\n com.google.appengine.api.modulesB\x10ModulesServicePb'
)



_MODULESSERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.ModulesServiceError.ErrorCode',
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
      name='INVALID_MODULE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_VERSION', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_INSTANCES', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRANSIENT_ERROR', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNEXPECTED_STATE', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=96,
  serialized_end=222,
)
_sym_db.RegisterEnumDescriptor(_MODULESSERVICEERROR_ERRORCODE)


_MODULESSERVICEERROR = _descriptor.Descriptor(
  name='ModulesServiceError',
  full_name='google.appengine.ModulesServiceError',
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
    _MODULESSERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=222,
)


_GETMODULESREQUEST = _descriptor.Descriptor(
  name='GetModulesRequest',
  full_name='google.appengine.GetModulesRequest',
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
  serialized_start=224,
  serialized_end=243,
)


_GETMODULESRESPONSE = _descriptor.Descriptor(
  name='GetModulesResponse',
  full_name='google.appengine.GetModulesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='module', full_name='google.appengine.GetModulesResponse.module', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=245,
  serialized_end=281,
)


_GETVERSIONSREQUEST = _descriptor.Descriptor(
  name='GetVersionsRequest',
  full_name='google.appengine.GetVersionsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='module', full_name='google.appengine.GetVersionsRequest.module', index=0,
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
  serialized_start=283,
  serialized_end=319,
)


_GETVERSIONSRESPONSE = _descriptor.Descriptor(
  name='GetVersionsResponse',
  full_name='google.appengine.GetVersionsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='google.appengine.GetVersionsResponse.version', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=321,
  serialized_end=359,
)


_GETDEFAULTVERSIONREQUEST = _descriptor.Descriptor(
  name='GetDefaultVersionRequest',
  full_name='google.appengine.GetDefaultVersionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='module', full_name='google.appengine.GetDefaultVersionRequest.module', index=0,
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
  serialized_start=361,
  serialized_end=403,
)


_GETDEFAULTVERSIONRESPONSE = _descriptor.Descriptor(
  name='GetDefaultVersionResponse',
  full_name='google.appengine.GetDefaultVersionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='google.appengine.GetDefaultVersionResponse.version', index=0,
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
  serialized_start=405,
  serialized_end=449,
)


_GETNUMINSTANCESREQUEST = _descriptor.Descriptor(
  name='GetNumInstancesRequest',
  full_name='google.appengine.GetNumInstancesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='module', full_name='google.appengine.GetNumInstancesRequest.module', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='google.appengine.GetNumInstancesRequest.version', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=451,
  serialized_end=508,
)


_GETNUMINSTANCESRESPONSE = _descriptor.Descriptor(
  name='GetNumInstancesResponse',
  full_name='google.appengine.GetNumInstancesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='instances', full_name='google.appengine.GetNumInstancesResponse.instances', index=0,
      number=1, type=3, cpp_type=2, label=1,
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
  serialized_start=510,
  serialized_end=554,
)


_SETNUMINSTANCESREQUEST = _descriptor.Descriptor(
  name='SetNumInstancesRequest',
  full_name='google.appengine.SetNumInstancesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='module', full_name='google.appengine.SetNumInstancesRequest.module', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='google.appengine.SetNumInstancesRequest.version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='instances', full_name='google.appengine.SetNumInstancesRequest.instances', index=2,
      number=3, type=3, cpp_type=2, label=2,
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
  serialized_start=556,
  serialized_end=632,
)


_SETNUMINSTANCESRESPONSE = _descriptor.Descriptor(
  name='SetNumInstancesResponse',
  full_name='google.appengine.SetNumInstancesResponse',
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
  serialized_start=634,
  serialized_end=659,
)


_STARTMODULEREQUEST = _descriptor.Descriptor(
  name='StartModuleRequest',
  full_name='google.appengine.StartModuleRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='module', full_name='google.appengine.StartModuleRequest.module', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='google.appengine.StartModuleRequest.version', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=661,
  serialized_end=714,
)


_STARTMODULERESPONSE = _descriptor.Descriptor(
  name='StartModuleResponse',
  full_name='google.appengine.StartModuleResponse',
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
  serialized_start=716,
  serialized_end=737,
)


_STOPMODULEREQUEST = _descriptor.Descriptor(
  name='StopModuleRequest',
  full_name='google.appengine.StopModuleRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='module', full_name='google.appengine.StopModuleRequest.module', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='google.appengine.StopModuleRequest.version', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=739,
  serialized_end=791,
)


_STOPMODULERESPONSE = _descriptor.Descriptor(
  name='StopModuleResponse',
  full_name='google.appengine.StopModuleResponse',
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
  serialized_start=793,
  serialized_end=813,
)


_GETHOSTNAMEREQUEST = _descriptor.Descriptor(
  name='GetHostnameRequest',
  full_name='google.appengine.GetHostnameRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='module', full_name='google.appengine.GetHostnameRequest.module', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='google.appengine.GetHostnameRequest.version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='instance', full_name='google.appengine.GetHostnameRequest.instance', index=2,
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
  serialized_start=815,
  serialized_end=886,
)


_GETHOSTNAMERESPONSE = _descriptor.Descriptor(
  name='GetHostnameResponse',
  full_name='google.appengine.GetHostnameResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='hostname', full_name='google.appengine.GetHostnameResponse.hostname', index=0,
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
  serialized_start=888,
  serialized_end=927,
)

_MODULESSERVICEERROR_ERRORCODE.containing_type = _MODULESSERVICEERROR
DESCRIPTOR.message_types_by_name['ModulesServiceError'] = _MODULESSERVICEERROR
DESCRIPTOR.message_types_by_name['GetModulesRequest'] = _GETMODULESREQUEST
DESCRIPTOR.message_types_by_name['GetModulesResponse'] = _GETMODULESRESPONSE
DESCRIPTOR.message_types_by_name['GetVersionsRequest'] = _GETVERSIONSREQUEST
DESCRIPTOR.message_types_by_name['GetVersionsResponse'] = _GETVERSIONSRESPONSE
DESCRIPTOR.message_types_by_name['GetDefaultVersionRequest'] = _GETDEFAULTVERSIONREQUEST
DESCRIPTOR.message_types_by_name['GetDefaultVersionResponse'] = _GETDEFAULTVERSIONRESPONSE
DESCRIPTOR.message_types_by_name['GetNumInstancesRequest'] = _GETNUMINSTANCESREQUEST
DESCRIPTOR.message_types_by_name['GetNumInstancesResponse'] = _GETNUMINSTANCESRESPONSE
DESCRIPTOR.message_types_by_name['SetNumInstancesRequest'] = _SETNUMINSTANCESREQUEST
DESCRIPTOR.message_types_by_name['SetNumInstancesResponse'] = _SETNUMINSTANCESRESPONSE
DESCRIPTOR.message_types_by_name['StartModuleRequest'] = _STARTMODULEREQUEST
DESCRIPTOR.message_types_by_name['StartModuleResponse'] = _STARTMODULERESPONSE
DESCRIPTOR.message_types_by_name['StopModuleRequest'] = _STOPMODULEREQUEST
DESCRIPTOR.message_types_by_name['StopModuleResponse'] = _STOPMODULERESPONSE
DESCRIPTOR.message_types_by_name['GetHostnameRequest'] = _GETHOSTNAMEREQUEST
DESCRIPTOR.message_types_by_name['GetHostnameResponse'] = _GETHOSTNAMERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ModulesServiceError = _reflection.GeneratedProtocolMessageType('ModulesServiceError', (_message.Message,), {
  'DESCRIPTOR' : _MODULESSERVICEERROR,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(ModulesServiceError)

GetModulesRequest = _reflection.GeneratedProtocolMessageType('GetModulesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETMODULESREQUEST,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetModulesRequest)

GetModulesResponse = _reflection.GeneratedProtocolMessageType('GetModulesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETMODULESRESPONSE,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetModulesResponse)

GetVersionsRequest = _reflection.GeneratedProtocolMessageType('GetVersionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETVERSIONSREQUEST,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetVersionsRequest)

GetVersionsResponse = _reflection.GeneratedProtocolMessageType('GetVersionsResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETVERSIONSRESPONSE,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetVersionsResponse)

GetDefaultVersionRequest = _reflection.GeneratedProtocolMessageType('GetDefaultVersionRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETDEFAULTVERSIONREQUEST,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetDefaultVersionRequest)

GetDefaultVersionResponse = _reflection.GeneratedProtocolMessageType('GetDefaultVersionResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETDEFAULTVERSIONRESPONSE,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetDefaultVersionResponse)

GetNumInstancesRequest = _reflection.GeneratedProtocolMessageType('GetNumInstancesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETNUMINSTANCESREQUEST,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetNumInstancesRequest)

GetNumInstancesResponse = _reflection.GeneratedProtocolMessageType('GetNumInstancesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETNUMINSTANCESRESPONSE,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetNumInstancesResponse)

SetNumInstancesRequest = _reflection.GeneratedProtocolMessageType('SetNumInstancesRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETNUMINSTANCESREQUEST,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(SetNumInstancesRequest)

SetNumInstancesResponse = _reflection.GeneratedProtocolMessageType('SetNumInstancesResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETNUMINSTANCESRESPONSE,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(SetNumInstancesResponse)

StartModuleRequest = _reflection.GeneratedProtocolMessageType('StartModuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTMODULEREQUEST,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(StartModuleRequest)

StartModuleResponse = _reflection.GeneratedProtocolMessageType('StartModuleResponse', (_message.Message,), {
  'DESCRIPTOR' : _STARTMODULERESPONSE,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(StartModuleResponse)

StopModuleRequest = _reflection.GeneratedProtocolMessageType('StopModuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _STOPMODULEREQUEST,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(StopModuleRequest)

StopModuleResponse = _reflection.GeneratedProtocolMessageType('StopModuleResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOPMODULERESPONSE,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(StopModuleResponse)

GetHostnameRequest = _reflection.GeneratedProtocolMessageType('GetHostnameRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETHOSTNAMEREQUEST,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetHostnameRequest)

GetHostnameResponse = _reflection.GeneratedProtocolMessageType('GetHostnameResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETHOSTNAMERESPONSE,
  '__module__' : 'google.appengine.api.modules.modules_service_pb2'

  })
_sym_db.RegisterMessage(GetHostnameResponse)


DESCRIPTOR._options = None

