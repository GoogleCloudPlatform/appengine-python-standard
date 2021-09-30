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
  name='google/appengine/api/app_identity/app_identity_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n$com.google.appengine.api.appidentityB\024AppIdentityServicePb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n<google/appengine/api/app_identity/app_identity_service.proto\x12\x10google.appengine\"\xe6\x01\n\x17\x41ppIdentityServiceError\"\xca\x01\n\tErrorCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x11\n\rUNKNOWN_SCOPE\x10\t\x12\x13\n\x0e\x42LOB_TOO_LARGE\x10\xe8\x07\x12\x16\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\xe9\x07\x12\x14\n\x0fNOT_A_VALID_APP\x10\xea\x07\x12\x12\n\rUNKNOWN_ERROR\x10\xeb\x07\x12\x1e\n\x19GAIAMINT_NOT_INITIAILIZED\x10\xec\x07\x12\x10\n\x0bNOT_ALLOWED\x10\xed\x07\x12\x14\n\x0fNOT_IMPLEMENTED\x10\xee\x07\"*\n\x11SignForAppRequest\x12\x15\n\rbytes_to_sign\x18\x01 \x01(\x0c\"?\n\x12SignForAppResponse\x12\x10\n\x08key_name\x18\x01 \x01(\t\x12\x17\n\x0fsignature_bytes\x18\x02 \x01(\x0c\"#\n!GetPublicCertificateForAppRequest\"C\n\x11PublicCertificate\x12\x10\n\x08key_name\x18\x01 \x01(\t\x12\x1c\n\x14x509_certificate_pem\x18\x02 \x01(\t\"\x93\x01\n\"GetPublicCertificateForAppResponse\x12\x44\n\x17public_certificate_list\x18\x01 \x03(\x0b\x32#.google.appengine.PublicCertificate\x12\'\n\x1fmax_client_cache_time_in_second\x18\x02 \x01(\x03\"\x1e\n\x1cGetServiceAccountNameRequest\"=\n\x1dGetServiceAccountNameResponse\x12\x1c\n\x14service_account_name\x18\x01 \x01(\t\"d\n\x15GetAccessTokenRequest\x12\r\n\x05scope\x18\x01 \x03(\t\x12\x1a\n\x12service_account_id\x18\x02 \x01(\x03\x12 \n\x14service_account_name\x18\x03 \x01(\tB\x02\x18\x01\"G\n\x16GetAccessTokenResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x17\n\x0f\x65xpiration_time\x18\x02 \x01(\x03\" \n\x1eGetDefaultGcsBucketNameRequest\"B\n\x1fGetDefaultGcsBucketNameResponse\x12\x1f\n\x17\x64\x65\x66\x61ult_gcs_bucket_name\x18\x01 \x01(\tB<\n$com.google.appengine.api.appidentityB\x14\x41ppIdentityServicePb'
)



_APPIDENTITYSERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.AppIdentityServiceError.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_SCOPE', index=1, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BLOB_TOO_LARGE', index=2, number=1000,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEADLINE_EXCEEDED', index=3, number=1001,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_A_VALID_APP', index=4, number=1002,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_ERROR', index=5, number=1003,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GAIAMINT_NOT_INITIAILIZED', index=6, number=1004,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_ALLOWED', index=7, number=1005,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_IMPLEMENTED', index=8, number=1006,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=111,
  serialized_end=313,
)
_sym_db.RegisterEnumDescriptor(_APPIDENTITYSERVICEERROR_ERRORCODE)


_APPIDENTITYSERVICEERROR = _descriptor.Descriptor(
  name='AppIdentityServiceError',
  full_name='google.appengine.AppIdentityServiceError',
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
    _APPIDENTITYSERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=313,
)


_SIGNFORAPPREQUEST = _descriptor.Descriptor(
  name='SignForAppRequest',
  full_name='google.appengine.SignForAppRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bytes_to_sign', full_name='google.appengine.SignForAppRequest.bytes_to_sign', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=315,
  serialized_end=357,
)


_SIGNFORAPPRESPONSE = _descriptor.Descriptor(
  name='SignForAppResponse',
  full_name='google.appengine.SignForAppResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key_name', full_name='google.appengine.SignForAppResponse.key_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='signature_bytes', full_name='google.appengine.SignForAppResponse.signature_bytes', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=359,
  serialized_end=422,
)


_GETPUBLICCERTIFICATEFORAPPREQUEST = _descriptor.Descriptor(
  name='GetPublicCertificateForAppRequest',
  full_name='google.appengine.GetPublicCertificateForAppRequest',
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
  serialized_start=424,
  serialized_end=459,
)


_PUBLICCERTIFICATE = _descriptor.Descriptor(
  name='PublicCertificate',
  full_name='google.appengine.PublicCertificate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key_name', full_name='google.appengine.PublicCertificate.key_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='x509_certificate_pem', full_name='google.appengine.PublicCertificate.x509_certificate_pem', index=1,
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
  serialized_start=461,
  serialized_end=528,
)


_GETPUBLICCERTIFICATEFORAPPRESPONSE = _descriptor.Descriptor(
  name='GetPublicCertificateForAppResponse',
  full_name='google.appengine.GetPublicCertificateForAppResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='public_certificate_list', full_name='google.appengine.GetPublicCertificateForAppResponse.public_certificate_list', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_client_cache_time_in_second', full_name='google.appengine.GetPublicCertificateForAppResponse.max_client_cache_time_in_second', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  serialized_start=531,
  serialized_end=678,
)


_GETSERVICEACCOUNTNAMEREQUEST = _descriptor.Descriptor(
  name='GetServiceAccountNameRequest',
  full_name='google.appengine.GetServiceAccountNameRequest',
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
  serialized_start=680,
  serialized_end=710,
)


_GETSERVICEACCOUNTNAMERESPONSE = _descriptor.Descriptor(
  name='GetServiceAccountNameResponse',
  full_name='google.appengine.GetServiceAccountNameResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='service_account_name', full_name='google.appengine.GetServiceAccountNameResponse.service_account_name', index=0,
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
  serialized_start=712,
  serialized_end=773,
)


_GETACCESSTOKENREQUEST = _descriptor.Descriptor(
  name='GetAccessTokenRequest',
  full_name='google.appengine.GetAccessTokenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='scope', full_name='google.appengine.GetAccessTokenRequest.scope', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='service_account_id', full_name='google.appengine.GetAccessTokenRequest.service_account_id', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='service_account_name', full_name='google.appengine.GetAccessTokenRequest.service_account_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=775,
  serialized_end=875,
)


_GETACCESSTOKENRESPONSE = _descriptor.Descriptor(
  name='GetAccessTokenResponse',
  full_name='google.appengine.GetAccessTokenResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='access_token', full_name='google.appengine.GetAccessTokenResponse.access_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expiration_time', full_name='google.appengine.GetAccessTokenResponse.expiration_time', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  serialized_start=877,
  serialized_end=948,
)


_GETDEFAULTGCSBUCKETNAMEREQUEST = _descriptor.Descriptor(
  name='GetDefaultGcsBucketNameRequest',
  full_name='google.appengine.GetDefaultGcsBucketNameRequest',
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
  serialized_start=950,
  serialized_end=982,
)


_GETDEFAULTGCSBUCKETNAMERESPONSE = _descriptor.Descriptor(
  name='GetDefaultGcsBucketNameResponse',
  full_name='google.appengine.GetDefaultGcsBucketNameResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='default_gcs_bucket_name', full_name='google.appengine.GetDefaultGcsBucketNameResponse.default_gcs_bucket_name', index=0,
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
  serialized_start=984,
  serialized_end=1050,
)

_APPIDENTITYSERVICEERROR_ERRORCODE.containing_type = _APPIDENTITYSERVICEERROR
_GETPUBLICCERTIFICATEFORAPPRESPONSE.fields_by_name['public_certificate_list'].message_type = _PUBLICCERTIFICATE
DESCRIPTOR.message_types_by_name['AppIdentityServiceError'] = _APPIDENTITYSERVICEERROR
DESCRIPTOR.message_types_by_name['SignForAppRequest'] = _SIGNFORAPPREQUEST
DESCRIPTOR.message_types_by_name['SignForAppResponse'] = _SIGNFORAPPRESPONSE
DESCRIPTOR.message_types_by_name['GetPublicCertificateForAppRequest'] = _GETPUBLICCERTIFICATEFORAPPREQUEST
DESCRIPTOR.message_types_by_name['PublicCertificate'] = _PUBLICCERTIFICATE
DESCRIPTOR.message_types_by_name['GetPublicCertificateForAppResponse'] = _GETPUBLICCERTIFICATEFORAPPRESPONSE
DESCRIPTOR.message_types_by_name['GetServiceAccountNameRequest'] = _GETSERVICEACCOUNTNAMEREQUEST
DESCRIPTOR.message_types_by_name['GetServiceAccountNameResponse'] = _GETSERVICEACCOUNTNAMERESPONSE
DESCRIPTOR.message_types_by_name['GetAccessTokenRequest'] = _GETACCESSTOKENREQUEST
DESCRIPTOR.message_types_by_name['GetAccessTokenResponse'] = _GETACCESSTOKENRESPONSE
DESCRIPTOR.message_types_by_name['GetDefaultGcsBucketNameRequest'] = _GETDEFAULTGCSBUCKETNAMEREQUEST
DESCRIPTOR.message_types_by_name['GetDefaultGcsBucketNameResponse'] = _GETDEFAULTGCSBUCKETNAMERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AppIdentityServiceError = _reflection.GeneratedProtocolMessageType('AppIdentityServiceError', (_message.Message,), {
  'DESCRIPTOR' : _APPIDENTITYSERVICEERROR,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(AppIdentityServiceError)

SignForAppRequest = _reflection.GeneratedProtocolMessageType('SignForAppRequest', (_message.Message,), {
  'DESCRIPTOR' : _SIGNFORAPPREQUEST,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(SignForAppRequest)

SignForAppResponse = _reflection.GeneratedProtocolMessageType('SignForAppResponse', (_message.Message,), {
  'DESCRIPTOR' : _SIGNFORAPPRESPONSE,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(SignForAppResponse)

GetPublicCertificateForAppRequest = _reflection.GeneratedProtocolMessageType('GetPublicCertificateForAppRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETPUBLICCERTIFICATEFORAPPREQUEST,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(GetPublicCertificateForAppRequest)

PublicCertificate = _reflection.GeneratedProtocolMessageType('PublicCertificate', (_message.Message,), {
  'DESCRIPTOR' : _PUBLICCERTIFICATE,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(PublicCertificate)

GetPublicCertificateForAppResponse = _reflection.GeneratedProtocolMessageType('GetPublicCertificateForAppResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETPUBLICCERTIFICATEFORAPPRESPONSE,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(GetPublicCertificateForAppResponse)

GetServiceAccountNameRequest = _reflection.GeneratedProtocolMessageType('GetServiceAccountNameRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSERVICEACCOUNTNAMEREQUEST,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(GetServiceAccountNameRequest)

GetServiceAccountNameResponse = _reflection.GeneratedProtocolMessageType('GetServiceAccountNameResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETSERVICEACCOUNTNAMERESPONSE,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(GetServiceAccountNameResponse)

GetAccessTokenRequest = _reflection.GeneratedProtocolMessageType('GetAccessTokenRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETACCESSTOKENREQUEST,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(GetAccessTokenRequest)

GetAccessTokenResponse = _reflection.GeneratedProtocolMessageType('GetAccessTokenResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETACCESSTOKENRESPONSE,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(GetAccessTokenResponse)

GetDefaultGcsBucketNameRequest = _reflection.GeneratedProtocolMessageType('GetDefaultGcsBucketNameRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETDEFAULTGCSBUCKETNAMEREQUEST,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(GetDefaultGcsBucketNameRequest)

GetDefaultGcsBucketNameResponse = _reflection.GeneratedProtocolMessageType('GetDefaultGcsBucketNameResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETDEFAULTGCSBUCKETNAMERESPONSE,
  '__module__' : 'google.appengine.api.app_identity.app_identity_service_pb2'

  })
_sym_db.RegisterMessage(GetDefaultGcsBucketNameResponse)


DESCRIPTOR._options = None
_GETACCESSTOKENREQUEST.fields_by_name['service_account_name']._options = None

