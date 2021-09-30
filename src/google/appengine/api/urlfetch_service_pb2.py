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
  name='google/appengine/api/urlfetch_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n!com.google.appengine.api.urlfetchB\021URLFetchServicePb\210\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+google/appengine/api/urlfetch_service.proto\x12\x10google.appengine\"\xc2\x02\n\x14URLFetchServiceError\"\xa9\x02\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x0f\n\x0bINVALID_URL\x10\x01\x12\x0f\n\x0b\x46\x45TCH_ERROR\x10\x02\x12\x15\n\x11UNSPECIFIED_ERROR\x10\x03\x12\x16\n\x12RESPONSE_TOO_LARGE\x10\x04\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x05\x12\x19\n\x15SSL_CERTIFICATE_ERROR\x10\x06\x12\r\n\tDNS_ERROR\x10\x07\x12\n\n\x06\x43LOSED\x10\x08\x12\x1c\n\x18INTERNAL_TRANSIENT_ERROR\x10\t\x12\x16\n\x12TOO_MANY_REDIRECTS\x10\n\x12\x13\n\x0fMALFORMED_REPLY\x10\x0b\x12\x14\n\x10\x43ONNECTION_ERROR\x10\x0c\x12\x15\n\x11PAYLOAD_TOO_LARGE\x10\r\"\x80\x03\n\x0fURLFetchRequest\x12?\n\x06Method\x18\x01 \x02(\x0e\x32/.google.appengine.URLFetchRequest.RequestMethod\x12\x0b\n\x03Url\x18\x02 \x02(\t\x12\x38\n\x06header\x18\x03 \x03(\n2(.google.appengine.URLFetchRequest.Header\x12\x13\n\x07Payload\x18\x06 \x01(\x0c\x42\x02\x08\x01\x12\x1d\n\x0f\x46ollowRedirects\x18\x07 \x01(\x08:\x04true\x12\x10\n\x08\x44\x65\x61\x64line\x18\x08 \x01(\x01\x12+\n\x1dMustValidateServerCertificate\x18\t \x01(\x08:\x04true\x1a$\n\x06Header\x12\x0b\n\x03Key\x18\x04 \x02(\t\x12\r\n\x05Value\x18\x05 \x02(\t\"L\n\rRequestMethod\x12\x07\n\x03GET\x10\x01\x12\x08\n\x04POST\x10\x02\x12\x08\n\x04HEAD\x10\x03\x12\x07\n\x03PUT\x10\x04\x12\n\n\x06\x44\x45LETE\x10\x05\x12\t\n\x05PATCH\x10\x06\"\xdd\x02\n\x10URLFetchResponse\x12\x0f\n\x07\x43ontent\x18\x01 \x01(\x0c\x12\x12\n\nStatusCode\x18\x02 \x02(\x05\x12\x39\n\x06header\x18\x03 \x03(\n2).google.appengine.URLFetchResponse.Header\x12\"\n\x13\x43ontentWasTruncated\x18\x06 \x01(\x08:\x05\x66\x61lse\x12\x19\n\x11\x45xternalBytesSent\x18\x07 \x01(\x03\x12\x1d\n\x15\x45xternalBytesReceived\x18\x08 \x01(\x03\x12\x10\n\x08\x46inalUrl\x18\t \x01(\t\x12\x1d\n\x12\x41piCpuMilliseconds\x18\n \x01(\x03:\x01\x30\x12\x17\n\x0c\x41piBytesSent\x18\x0b \x01(\x03:\x01\x30\x12\x1b\n\x10\x41piBytesReceived\x18\x0c \x01(\x03:\x01\x30\x1a$\n\x06Header\x12\x0b\n\x03Key\x18\x04 \x02(\t\x12\r\n\x05Value\x18\x05 \x02(\tB9\n!com.google.appengine.api.urlfetchB\x11URLFetchServicePb\x88\x01\x01'
)



_URLFETCHSERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.URLFetchServiceError.ErrorCode',
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
      name='INVALID_URL', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FETCH_ERROR', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED_ERROR', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESPONSE_TOO_LARGE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEADLINE_EXCEEDED', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SSL_CERTIFICATE_ERROR', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DNS_ERROR', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CLOSED', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INTERNAL_TRANSIENT_ERROR', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TOO_MANY_REDIRECTS', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MALFORMED_REPLY', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONNECTION_ERROR', index=12, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PAYLOAD_TOO_LARGE', index=13, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=91,
  serialized_end=388,
)
_sym_db.RegisterEnumDescriptor(_URLFETCHSERVICEERROR_ERRORCODE)

_URLFETCHREQUEST_REQUESTMETHOD = _descriptor.EnumDescriptor(
  name='RequestMethod',
  full_name='google.appengine.URLFetchRequest.RequestMethod',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GET', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='POST', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HEAD', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PUT', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DELETE', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PATCH', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=699,
  serialized_end=775,
)
_sym_db.RegisterEnumDescriptor(_URLFETCHREQUEST_REQUESTMETHOD)


_URLFETCHSERVICEERROR = _descriptor.Descriptor(
  name='URLFetchServiceError',
  full_name='google.appengine.URLFetchServiceError',
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
    _URLFETCHSERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=66,
  serialized_end=388,
)


_URLFETCHREQUEST_HEADER = _descriptor.Descriptor(
  name='Header',
  full_name='google.appengine.URLFetchRequest.Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Key', full_name='google.appengine.URLFetchRequest.Header.Key', index=0,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Value', full_name='google.appengine.URLFetchRequest.Header.Value', index=1,
      number=5, type=9, cpp_type=9, label=2,
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
  serialized_end=697,
)

_URLFETCHREQUEST = _descriptor.Descriptor(
  name='URLFetchRequest',
  full_name='google.appengine.URLFetchRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Method', full_name='google.appengine.URLFetchRequest.Method', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Url', full_name='google.appengine.URLFetchRequest.Url', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='header', full_name='google.appengine.URLFetchRequest.header', index=2,
      number=3, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Payload', full_name='google.appengine.URLFetchRequest.Payload', index=3,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='FollowRedirects', full_name='google.appengine.URLFetchRequest.FollowRedirects', index=4,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Deadline', full_name='google.appengine.URLFetchRequest.Deadline', index=5,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='MustValidateServerCertificate', full_name='google.appengine.URLFetchRequest.MustValidateServerCertificate', index=6,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_URLFETCHREQUEST_HEADER, ],
  enum_types=[
    _URLFETCHREQUEST_REQUESTMETHOD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=391,
  serialized_end=775,
)


_URLFETCHRESPONSE_HEADER = _descriptor.Descriptor(
  name='Header',
  full_name='google.appengine.URLFetchResponse.Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Key', full_name='google.appengine.URLFetchResponse.Header.Key', index=0,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Value', full_name='google.appengine.URLFetchResponse.Header.Value', index=1,
      number=5, type=9, cpp_type=9, label=2,
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
  serialized_end=697,
)

_URLFETCHRESPONSE = _descriptor.Descriptor(
  name='URLFetchResponse',
  full_name='google.appengine.URLFetchResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Content', full_name='google.appengine.URLFetchResponse.Content', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='StatusCode', full_name='google.appengine.URLFetchResponse.StatusCode', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='header', full_name='google.appengine.URLFetchResponse.header', index=2,
      number=3, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ContentWasTruncated', full_name='google.appengine.URLFetchResponse.ContentWasTruncated', index=3,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ExternalBytesSent', full_name='google.appengine.URLFetchResponse.ExternalBytesSent', index=4,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ExternalBytesReceived', full_name='google.appengine.URLFetchResponse.ExternalBytesReceived', index=5,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='FinalUrl', full_name='google.appengine.URLFetchResponse.FinalUrl', index=6,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ApiCpuMilliseconds', full_name='google.appengine.URLFetchResponse.ApiCpuMilliseconds', index=7,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ApiBytesSent', full_name='google.appengine.URLFetchResponse.ApiBytesSent', index=8,
      number=11, type=3, cpp_type=2, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ApiBytesReceived', full_name='google.appengine.URLFetchResponse.ApiBytesReceived', index=9,
      number=12, type=3, cpp_type=2, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_URLFETCHRESPONSE_HEADER, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=778,
  serialized_end=1127,
)

_URLFETCHSERVICEERROR_ERRORCODE.containing_type = _URLFETCHSERVICEERROR
_URLFETCHREQUEST_HEADER.containing_type = _URLFETCHREQUEST
_URLFETCHREQUEST.fields_by_name['Method'].enum_type = _URLFETCHREQUEST_REQUESTMETHOD
_URLFETCHREQUEST.fields_by_name['header'].message_type = _URLFETCHREQUEST_HEADER
_URLFETCHREQUEST_REQUESTMETHOD.containing_type = _URLFETCHREQUEST
_URLFETCHRESPONSE_HEADER.containing_type = _URLFETCHRESPONSE
_URLFETCHRESPONSE.fields_by_name['header'].message_type = _URLFETCHRESPONSE_HEADER
DESCRIPTOR.message_types_by_name['URLFetchServiceError'] = _URLFETCHSERVICEERROR
DESCRIPTOR.message_types_by_name['URLFetchRequest'] = _URLFETCHREQUEST
DESCRIPTOR.message_types_by_name['URLFetchResponse'] = _URLFETCHRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

URLFetchServiceError = _reflection.GeneratedProtocolMessageType('URLFetchServiceError', (_message.Message,), {
  'DESCRIPTOR' : _URLFETCHSERVICEERROR,
  '__module__' : 'google.appengine.api.urlfetch_service_pb2'

  })
_sym_db.RegisterMessage(URLFetchServiceError)

URLFetchRequest = _reflection.GeneratedProtocolMessageType('URLFetchRequest', (_message.Message,), {

  'Header' : _reflection.GeneratedProtocolMessageType('Header', (_message.Message,), {
    'DESCRIPTOR' : _URLFETCHREQUEST_HEADER,
    '__module__' : 'google.appengine.api.urlfetch_service_pb2'

    })
  ,
  'DESCRIPTOR' : _URLFETCHREQUEST,
  '__module__' : 'google.appengine.api.urlfetch_service_pb2'

  })
_sym_db.RegisterMessage(URLFetchRequest)
_sym_db.RegisterMessage(URLFetchRequest.Header)

URLFetchResponse = _reflection.GeneratedProtocolMessageType('URLFetchResponse', (_message.Message,), {

  'Header' : _reflection.GeneratedProtocolMessageType('Header', (_message.Message,), {
    'DESCRIPTOR' : _URLFETCHRESPONSE_HEADER,
    '__module__' : 'google.appengine.api.urlfetch_service_pb2'

    })
  ,
  'DESCRIPTOR' : _URLFETCHRESPONSE,
  '__module__' : 'google.appengine.api.urlfetch_service_pb2'

  })
_sym_db.RegisterMessage(URLFetchResponse)
_sym_db.RegisterMessage(URLFetchResponse.Header)


DESCRIPTOR._options = None
_URLFETCHREQUEST.fields_by_name['Payload']._options = None

