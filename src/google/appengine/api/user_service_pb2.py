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
  name='google/appengine/api/user_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n\037com.google.google.appengine.apiB\rUserServicePb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\'google/appengine/api/user_service.proto\x12\x10google.appengine\"\x99\x01\n\x10UserServiceError\"\x84\x01\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x19\n\x15REDIRECT_URL_TOO_LONG\x10\x01\x12\x0f\n\x0bNOT_ALLOWED\x10\x02\x12\x17\n\x13OAUTH_INVALID_TOKEN\x10\x03\x12\x19\n\x15OAUTH_INVALID_REQUEST\x10\x04\x12\x0f\n\x0bOAUTH_ERROR\x10\x05\"a\n\x15\x43reateLoginURLRequest\x12\x17\n\x0f\x64\x65stination_url\x18\x01 \x02(\t\x12\x13\n\x0b\x61uth_domain\x18\x02 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_identity\x18\x03 \x01(\t\"+\n\x16\x43reateLoginURLResponse\x12\x11\n\tlogin_url\x18\x01 \x01(\t\"F\n\x16\x43reateLogoutURLRequest\x12\x17\n\x0f\x64\x65stination_url\x18\x01 \x02(\t\x12\x13\n\x0b\x61uth_domain\x18\x02 \x01(\t\"-\n\x17\x43reateLogoutURLResponse\x12\x12\n\nlogout_url\x18\x01 \x01(\t\"[\n\x13GetOAuthUserRequest\x12\r\n\x05scope\x18\x01 \x01(\t\x12\x0e\n\x06scopes\x18\x02 \x03(\t\x12%\n\x19request_writer_permission\x18\x03 \x01(\x08\x42\x02\x18\x01\"\xba\x01\n\x14GetOAuthUserResponse\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x13\n\x0b\x61uth_domain\x18\x03 \x01(\t\x12\x19\n\x11user_organization\x18\x04 \x01(\t\x12\x10\n\x08is_admin\x18\x05 \x01(\x08\x12\x11\n\tclient_id\x18\x06 \x01(\t\x12\x0e\n\x06scopes\x18\x07 \x03(\t\x12\x1d\n\x11is_project_writer\x18\x08 \x01(\x08\x42\x02\x18\x01\x42\x30\n\x1f\x63om.google.google.appengine.apiB\rUserServicePb'
)



_USERSERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.UserServiceError.ErrorCode',
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
      name='REDIRECT_URL_TOO_LONG', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_ALLOWED', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OAUTH_INVALID_TOKEN', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OAUTH_INVALID_REQUEST', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OAUTH_ERROR', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=83,
  serialized_end=215,
)
_sym_db.RegisterEnumDescriptor(_USERSERVICEERROR_ERRORCODE)


_USERSERVICEERROR = _descriptor.Descriptor(
  name='UserServiceError',
  full_name='google.appengine.UserServiceError',
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
    _USERSERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=215,
)


_CREATELOGINURLREQUEST = _descriptor.Descriptor(
  name='CreateLoginURLRequest',
  full_name='google.appengine.CreateLoginURLRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='destination_url', full_name='google.appengine.CreateLoginURLRequest.destination_url', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auth_domain', full_name='google.appengine.CreateLoginURLRequest.auth_domain', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='federated_identity', full_name='google.appengine.CreateLoginURLRequest.federated_identity', index=2,
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
  serialized_start=217,
  serialized_end=314,
)


_CREATELOGINURLRESPONSE = _descriptor.Descriptor(
  name='CreateLoginURLResponse',
  full_name='google.appengine.CreateLoginURLResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='login_url', full_name='google.appengine.CreateLoginURLResponse.login_url', index=0,
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
  serialized_start=316,
  serialized_end=359,
)


_CREATELOGOUTURLREQUEST = _descriptor.Descriptor(
  name='CreateLogoutURLRequest',
  full_name='google.appengine.CreateLogoutURLRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='destination_url', full_name='google.appengine.CreateLogoutURLRequest.destination_url', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auth_domain', full_name='google.appengine.CreateLogoutURLRequest.auth_domain', index=1,
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
  serialized_start=361,
  serialized_end=431,
)


_CREATELOGOUTURLRESPONSE = _descriptor.Descriptor(
  name='CreateLogoutURLResponse',
  full_name='google.appengine.CreateLogoutURLResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='logout_url', full_name='google.appengine.CreateLogoutURLResponse.logout_url', index=0,
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
  serialized_start=433,
  serialized_end=478,
)


_GETOAUTHUSERREQUEST = _descriptor.Descriptor(
  name='GetOAuthUserRequest',
  full_name='google.appengine.GetOAuthUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scope', full_name='google.appengine.GetOAuthUserRequest.scope', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scopes', full_name='google.appengine.GetOAuthUserRequest.scopes', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_writer_permission', full_name='google.appengine.GetOAuthUserRequest.request_writer_permission', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=480,
  serialized_end=571,
)


_GETOAUTHUSERRESPONSE = _descriptor.Descriptor(
  name='GetOAuthUserResponse',
  full_name='google.appengine.GetOAuthUserResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='google.appengine.GetOAuthUserResponse.email', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='google.appengine.GetOAuthUserResponse.user_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auth_domain', full_name='google.appengine.GetOAuthUserResponse.auth_domain', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_organization', full_name='google.appengine.GetOAuthUserResponse.user_organization', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='is_admin', full_name='google.appengine.GetOAuthUserResponse.is_admin', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='client_id', full_name='google.appengine.GetOAuthUserResponse.client_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scopes', full_name='google.appengine.GetOAuthUserResponse.scopes', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='is_project_writer', full_name='google.appengine.GetOAuthUserResponse.is_project_writer', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=574,
  serialized_end=760,
)

_USERSERVICEERROR_ERRORCODE.containing_type = _USERSERVICEERROR
DESCRIPTOR.message_types_by_name['UserServiceError'] = _USERSERVICEERROR
DESCRIPTOR.message_types_by_name['CreateLoginURLRequest'] = _CREATELOGINURLREQUEST
DESCRIPTOR.message_types_by_name['CreateLoginURLResponse'] = _CREATELOGINURLRESPONSE
DESCRIPTOR.message_types_by_name['CreateLogoutURLRequest'] = _CREATELOGOUTURLREQUEST
DESCRIPTOR.message_types_by_name['CreateLogoutURLResponse'] = _CREATELOGOUTURLRESPONSE
DESCRIPTOR.message_types_by_name['GetOAuthUserRequest'] = _GETOAUTHUSERREQUEST
DESCRIPTOR.message_types_by_name['GetOAuthUserResponse'] = _GETOAUTHUSERRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserServiceError = _reflection.GeneratedProtocolMessageType('UserServiceError', (_message.Message,), {
  'DESCRIPTOR' : _USERSERVICEERROR,
  '__module__' : 'google.appengine.api.user_service_pb2'

  })
_sym_db.RegisterMessage(UserServiceError)

CreateLoginURLRequest = _reflection.GeneratedProtocolMessageType('CreateLoginURLRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATELOGINURLREQUEST,
  '__module__' : 'google.appengine.api.user_service_pb2'

  })
_sym_db.RegisterMessage(CreateLoginURLRequest)

CreateLoginURLResponse = _reflection.GeneratedProtocolMessageType('CreateLoginURLResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATELOGINURLRESPONSE,
  '__module__' : 'google.appengine.api.user_service_pb2'

  })
_sym_db.RegisterMessage(CreateLoginURLResponse)

CreateLogoutURLRequest = _reflection.GeneratedProtocolMessageType('CreateLogoutURLRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATELOGOUTURLREQUEST,
  '__module__' : 'google.appengine.api.user_service_pb2'

  })
_sym_db.RegisterMessage(CreateLogoutURLRequest)

CreateLogoutURLResponse = _reflection.GeneratedProtocolMessageType('CreateLogoutURLResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATELOGOUTURLRESPONSE,
  '__module__' : 'google.appengine.api.user_service_pb2'

  })
_sym_db.RegisterMessage(CreateLogoutURLResponse)

GetOAuthUserRequest = _reflection.GeneratedProtocolMessageType('GetOAuthUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETOAUTHUSERREQUEST,
  '__module__' : 'google.appengine.api.user_service_pb2'

  })
_sym_db.RegisterMessage(GetOAuthUserRequest)

GetOAuthUserResponse = _reflection.GeneratedProtocolMessageType('GetOAuthUserResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETOAUTHUSERRESPONSE,
  '__module__' : 'google.appengine.api.user_service_pb2'

  })
_sym_db.RegisterMessage(GetOAuthUserResponse)


DESCRIPTOR._options = None
_GETOAUTHUSERREQUEST.fields_by_name['request_writer_permission']._options = None
_GETOAUTHUSERRESPONSE.fields_by_name['is_project_writer']._options = None

