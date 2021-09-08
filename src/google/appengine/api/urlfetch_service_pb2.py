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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+google/appengine/api/urlfetch_service.proto\x12\x10google.appengine\"\xc2\x02\n\x14URLFetchServiceError\"\xa9\x02\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x0f\n\x0bINVALID_URL\x10\x01\x12\x0f\n\x0b\x46\x45TCH_ERROR\x10\x02\x12\x15\n\x11UNSPECIFIED_ERROR\x10\x03\x12\x16\n\x12RESPONSE_TOO_LARGE\x10\x04\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x05\x12\x19\n\x15SSL_CERTIFICATE_ERROR\x10\x06\x12\r\n\tDNS_ERROR\x10\x07\x12\n\n\x06\x43LOSED\x10\x08\x12\x1c\n\x18INTERNAL_TRANSIENT_ERROR\x10\t\x12\x16\n\x12TOO_MANY_REDIRECTS\x10\n\x12\x13\n\x0fMALFORMED_REPLY\x10\x0b\x12\x14\n\x10\x43ONNECTION_ERROR\x10\x0c\x12\x15\n\x11PAYLOAD_TOO_LARGE\x10\r\"\x80\x03\n\x0fURLFetchRequest\x12?\n\x06Method\x18\x01 \x02(\x0e\x32/.google.appengine.URLFetchRequest.RequestMethod\x12\x0b\n\x03Url\x18\x02 \x02(\t\x12\x38\n\x06header\x18\x03 \x03(\n2(.google.appengine.URLFetchRequest.Header\x12\x13\n\x07Payload\x18\x06 \x01(\x0c\x42\x02\x08\x01\x12\x1d\n\x0f\x46ollowRedirects\x18\x07 \x01(\x08:\x04true\x12\x10\n\x08\x44\x65\x61\x64line\x18\x08 \x01(\x01\x12+\n\x1dMustValidateServerCertificate\x18\t \x01(\x08:\x04true\x1a$\n\x06Header\x12\x0b\n\x03Key\x18\x04 \x02(\t\x12\r\n\x05Value\x18\x05 \x02(\t\"L\n\rRequestMethod\x12\x07\n\x03GET\x10\x01\x12\x08\n\x04POST\x10\x02\x12\x08\n\x04HEAD\x10\x03\x12\x07\n\x03PUT\x10\x04\x12\n\n\x06\x44\x45LETE\x10\x05\x12\t\n\x05PATCH\x10\x06\"\xdd\x02\n\x10URLFetchResponse\x12\x0f\n\x07\x43ontent\x18\x01 \x01(\x0c\x12\x12\n\nStatusCode\x18\x02 \x02(\x05\x12\x39\n\x06header\x18\x03 \x03(\n2).google.appengine.URLFetchResponse.Header\x12\"\n\x13\x43ontentWasTruncated\x18\x06 \x01(\x08:\x05\x66\x61lse\x12\x19\n\x11\x45xternalBytesSent\x18\x07 \x01(\x03\x12\x1d\n\x15\x45xternalBytesReceived\x18\x08 \x01(\x03\x12\x10\n\x08\x46inalUrl\x18\t \x01(\t\x12\x1d\n\x12\x41piCpuMilliseconds\x18\n \x01(\x03:\x01\x30\x12\x17\n\x0c\x41piBytesSent\x18\x0b \x01(\x03:\x01\x30\x12\x1b\n\x10\x41piBytesReceived\x18\x0c \x01(\x03:\x01\x30\x1a$\n\x06Header\x12\x0b\n\x03Key\x18\x04 \x02(\t\x12\r\n\x05Value\x18\x05 \x02(\tB9\n!com.google.appengine.api.urlfetchB\x11URLFetchServicePb\x88\x01\x01')



_URLFETCHSERVICEERROR = DESCRIPTOR.message_types_by_name['URLFetchServiceError']
_URLFETCHREQUEST = DESCRIPTOR.message_types_by_name['URLFetchRequest']
_URLFETCHREQUEST_HEADER = _URLFETCHREQUEST.nested_types_by_name['Header']
_URLFETCHRESPONSE = DESCRIPTOR.message_types_by_name['URLFetchResponse']
_URLFETCHRESPONSE_HEADER = _URLFETCHRESPONSE.nested_types_by_name['Header']
_URLFETCHSERVICEERROR_ERRORCODE = _URLFETCHSERVICEERROR.enum_types_by_name['ErrorCode']
_URLFETCHREQUEST_REQUESTMETHOD = _URLFETCHREQUEST.enum_types_by_name['RequestMethod']
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

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!com.google.appengine.api.urlfetchB\021URLFetchServicePb\210\001\001'
  _URLFETCHREQUEST.fields_by_name['Payload']._options = None
  _URLFETCHREQUEST.fields_by_name['Payload']._serialized_options = b'\010\001'
  _URLFETCHSERVICEERROR._serialized_start=66
  _URLFETCHSERVICEERROR._serialized_end=388
  _URLFETCHSERVICEERROR_ERRORCODE._serialized_start=91
  _URLFETCHSERVICEERROR_ERRORCODE._serialized_end=388
  _URLFETCHREQUEST._serialized_start=391
  _URLFETCHREQUEST._serialized_end=775
  _URLFETCHREQUEST_HEADER._serialized_start=661
  _URLFETCHREQUEST_HEADER._serialized_end=697
  _URLFETCHREQUEST_REQUESTMETHOD._serialized_start=699
  _URLFETCHREQUEST_REQUESTMETHOD._serialized_end=775
  _URLFETCHRESPONSE._serialized_start=778
  _URLFETCHRESPONSE._serialized_end=1127
  _URLFETCHRESPONSE_HEADER._serialized_start=661
  _URLFETCHRESPONSE_HEADER._serialized_end=697

