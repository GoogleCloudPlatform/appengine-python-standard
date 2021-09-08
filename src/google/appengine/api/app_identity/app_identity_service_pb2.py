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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n<google/appengine/api/app_identity/app_identity_service.proto\x12\x10google.appengine\"\xe6\x01\n\x17\x41ppIdentityServiceError\"\xca\x01\n\tErrorCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x11\n\rUNKNOWN_SCOPE\x10\t\x12\x13\n\x0e\x42LOB_TOO_LARGE\x10\xe8\x07\x12\x16\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\xe9\x07\x12\x14\n\x0fNOT_A_VALID_APP\x10\xea\x07\x12\x12\n\rUNKNOWN_ERROR\x10\xeb\x07\x12\x1e\n\x19GAIAMINT_NOT_INITIAILIZED\x10\xec\x07\x12\x10\n\x0bNOT_ALLOWED\x10\xed\x07\x12\x14\n\x0fNOT_IMPLEMENTED\x10\xee\x07\"*\n\x11SignForAppRequest\x12\x15\n\rbytes_to_sign\x18\x01 \x01(\x0c\"?\n\x12SignForAppResponse\x12\x10\n\x08key_name\x18\x01 \x01(\t\x12\x17\n\x0fsignature_bytes\x18\x02 \x01(\x0c\"#\n!GetPublicCertificateForAppRequest\"C\n\x11PublicCertificate\x12\x10\n\x08key_name\x18\x01 \x01(\t\x12\x1c\n\x14x509_certificate_pem\x18\x02 \x01(\t\"\x93\x01\n\"GetPublicCertificateForAppResponse\x12\x44\n\x17public_certificate_list\x18\x01 \x03(\x0b\x32#.google.appengine.PublicCertificate\x12\'\n\x1fmax_client_cache_time_in_second\x18\x02 \x01(\x03\"\x1e\n\x1cGetServiceAccountNameRequest\"=\n\x1dGetServiceAccountNameResponse\x12\x1c\n\x14service_account_name\x18\x01 \x01(\t\"d\n\x15GetAccessTokenRequest\x12\r\n\x05scope\x18\x01 \x03(\t\x12\x1a\n\x12service_account_id\x18\x02 \x01(\x03\x12 \n\x14service_account_name\x18\x03 \x01(\tB\x02\x18\x01\"G\n\x16GetAccessTokenResponse\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x01 \x01(\t\x12\x17\n\x0f\x65xpiration_time\x18\x02 \x01(\x03\" \n\x1eGetDefaultGcsBucketNameRequest\"B\n\x1fGetDefaultGcsBucketNameResponse\x12\x1f\n\x17\x64\x65\x66\x61ult_gcs_bucket_name\x18\x01 \x01(\tB<\n$com.google.appengine.api.appidentityB\x14\x41ppIdentityServicePb')



_APPIDENTITYSERVICEERROR = DESCRIPTOR.message_types_by_name['AppIdentityServiceError']
_SIGNFORAPPREQUEST = DESCRIPTOR.message_types_by_name['SignForAppRequest']
_SIGNFORAPPRESPONSE = DESCRIPTOR.message_types_by_name['SignForAppResponse']
_GETPUBLICCERTIFICATEFORAPPREQUEST = DESCRIPTOR.message_types_by_name['GetPublicCertificateForAppRequest']
_PUBLICCERTIFICATE = DESCRIPTOR.message_types_by_name['PublicCertificate']
_GETPUBLICCERTIFICATEFORAPPRESPONSE = DESCRIPTOR.message_types_by_name['GetPublicCertificateForAppResponse']
_GETSERVICEACCOUNTNAMEREQUEST = DESCRIPTOR.message_types_by_name['GetServiceAccountNameRequest']
_GETSERVICEACCOUNTNAMERESPONSE = DESCRIPTOR.message_types_by_name['GetServiceAccountNameResponse']
_GETACCESSTOKENREQUEST = DESCRIPTOR.message_types_by_name['GetAccessTokenRequest']
_GETACCESSTOKENRESPONSE = DESCRIPTOR.message_types_by_name['GetAccessTokenResponse']
_GETDEFAULTGCSBUCKETNAMEREQUEST = DESCRIPTOR.message_types_by_name['GetDefaultGcsBucketNameRequest']
_GETDEFAULTGCSBUCKETNAMERESPONSE = DESCRIPTOR.message_types_by_name['GetDefaultGcsBucketNameResponse']
_APPIDENTITYSERVICEERROR_ERRORCODE = _APPIDENTITYSERVICEERROR.enum_types_by_name['ErrorCode']
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

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n$com.google.appengine.api.appidentityB\024AppIdentityServicePb'
  _GETACCESSTOKENREQUEST.fields_by_name['service_account_name']._options = None
  _GETACCESSTOKENREQUEST.fields_by_name['service_account_name']._serialized_options = b'\030\001'
  _APPIDENTITYSERVICEERROR._serialized_start=83
  _APPIDENTITYSERVICEERROR._serialized_end=313
  _APPIDENTITYSERVICEERROR_ERRORCODE._serialized_start=111
  _APPIDENTITYSERVICEERROR_ERRORCODE._serialized_end=313
  _SIGNFORAPPREQUEST._serialized_start=315
  _SIGNFORAPPREQUEST._serialized_end=357
  _SIGNFORAPPRESPONSE._serialized_start=359
  _SIGNFORAPPRESPONSE._serialized_end=422
  _GETPUBLICCERTIFICATEFORAPPREQUEST._serialized_start=424
  _GETPUBLICCERTIFICATEFORAPPREQUEST._serialized_end=459
  _PUBLICCERTIFICATE._serialized_start=461
  _PUBLICCERTIFICATE._serialized_end=528
  _GETPUBLICCERTIFICATEFORAPPRESPONSE._serialized_start=531
  _GETPUBLICCERTIFICATEFORAPPRESPONSE._serialized_end=678
  _GETSERVICEACCOUNTNAMEREQUEST._serialized_start=680
  _GETSERVICEACCOUNTNAMEREQUEST._serialized_end=710
  _GETSERVICEACCOUNTNAMERESPONSE._serialized_start=712
  _GETSERVICEACCOUNTNAMERESPONSE._serialized_end=773
  _GETACCESSTOKENREQUEST._serialized_start=775
  _GETACCESSTOKENREQUEST._serialized_end=875
  _GETACCESSTOKENRESPONSE._serialized_start=877
  _GETACCESSTOKENRESPONSE._serialized_end=948
  _GETDEFAULTGCSBUCKETNAMEREQUEST._serialized_start=950
  _GETDEFAULTGCSBUCKETNAMEREQUEST._serialized_end=982
  _GETDEFAULTGCSBUCKETNAMERESPONSE._serialized_start=984
  _GETDEFAULTGCSBUCKETNAMERESPONSE._serialized_end=1050

