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
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    30,
    0,
    '-dev',
    'google/appengine/api/urlfetch_service.proto'
)


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+google/appengine/api/urlfetch_service.proto\x12\x10google.appengine\"\xc2\x02\n\x14URLFetchServiceError\"\xa9\x02\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x0f\n\x0bINVALID_URL\x10\x01\x12\x0f\n\x0b\x46\x45TCH_ERROR\x10\x02\x12\x15\n\x11UNSPECIFIED_ERROR\x10\x03\x12\x16\n\x12RESPONSE_TOO_LARGE\x10\x04\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x05\x12\x19\n\x15SSL_CERTIFICATE_ERROR\x10\x06\x12\r\n\tDNS_ERROR\x10\x07\x12\n\n\x06\x43LOSED\x10\x08\x12\x1c\n\x18INTERNAL_TRANSIENT_ERROR\x10\t\x12\x16\n\x12TOO_MANY_REDIRECTS\x10\n\x12\x13\n\x0fMALFORMED_REPLY\x10\x0b\x12\x14\n\x10\x43ONNECTION_ERROR\x10\x0c\x12\x15\n\x11PAYLOAD_TOO_LARGE\x10\r\"\x80\x03\n\x0fURLFetchRequest\x12?\n\x06Method\x18\x01 \x01(\x0e\x32/.google.appengine.URLFetchRequest.RequestMethod\x12\x0b\n\x03Url\x18\x02 \x01(\t\x12\x38\n\x06header\x18\x03 \x03(\n2(.google.appengine.URLFetchRequest.Header\x12\x13\n\x07Payload\x18\x06 \x01(\x0c\x42\x02\x08\x01\x12\x1d\n\x0f\x46ollowRedirects\x18\x07 \x01(\x08:\x04true\x12\x10\n\x08\x44\x65\x61\x64line\x18\x08 \x01(\x01\x12+\n\x1dMustValidateServerCertificate\x18\t \x01(\x08:\x04true\x1a$\n\x06Header\x12\x0b\n\x03Key\x18\x04 \x01(\t\x12\r\n\x05Value\x18\x05 \x01(\t\"L\n\rRequestMethod\x12\x07\n\x03GET\x10\x01\x12\x08\n\x04POST\x10\x02\x12\x08\n\x04HEAD\x10\x03\x12\x07\n\x03PUT\x10\x04\x12\n\n\x06\x44\x45LETE\x10\x05\x12\t\n\x05PATCH\x10\x06\"\xdd\x02\n\x10URLFetchResponse\x12\x0f\n\x07\x43ontent\x18\x01 \x01(\x0c\x12\x12\n\nStatusCode\x18\x02 \x01(\x05\x12\x39\n\x06header\x18\x03 \x03(\n2).google.appengine.URLFetchResponse.Header\x12\"\n\x13\x43ontentWasTruncated\x18\x06 \x01(\x08:\x05\x66\x61lse\x12\x19\n\x11\x45xternalBytesSent\x18\x07 \x01(\x03\x12\x1d\n\x15\x45xternalBytesReceived\x18\x08 \x01(\x03\x12\x10\n\x08\x46inalUrl\x18\t \x01(\t\x12\x1d\n\x12\x41piCpuMilliseconds\x18\n \x01(\x03:\x01\x30\x12\x17\n\x0c\x41piBytesSent\x18\x0b \x01(\x03:\x01\x30\x12\x1b\n\x10\x41piBytesReceived\x18\x0c \x01(\x03:\x01\x30\x1a$\n\x06Header\x12\x0b\n\x03Key\x18\x04 \x01(\t\x12\r\n\x05Value\x18\x05 \x01(\tB9\n!com.google.appengine.api.urlfetchB\x11URLFetchServicePb\x88\x01\x01')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.appengine.api.urlfetch_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n!com.google.appengine.api.urlfetchB\021URLFetchServicePb\210\001\001'
  _globals['_URLFETCHREQUEST'].fields_by_name['Payload']._loaded_options = None
  _globals['_URLFETCHREQUEST'].fields_by_name['Payload']._serialized_options = b'\010\001'
  _globals['_URLFETCHSERVICEERROR']._serialized_start=66
  _globals['_URLFETCHSERVICEERROR']._serialized_end=388
  _globals['_URLFETCHSERVICEERROR_ERRORCODE']._serialized_start=91
  _globals['_URLFETCHSERVICEERROR_ERRORCODE']._serialized_end=388
  _globals['_URLFETCHREQUEST']._serialized_start=391
  _globals['_URLFETCHREQUEST']._serialized_end=775
  _globals['_URLFETCHREQUEST_HEADER']._serialized_start=661
  _globals['_URLFETCHREQUEST_HEADER']._serialized_end=697
  _globals['_URLFETCHREQUEST_REQUESTMETHOD']._serialized_start=699
  _globals['_URLFETCHREQUEST_REQUESTMETHOD']._serialized_end=775
  _globals['_URLFETCHRESPONSE']._serialized_start=778
  _globals['_URLFETCHRESPONSE']._serialized_end=1127
  _globals['_URLFETCHRESPONSE_HEADER']._serialized_start=661
  _globals['_URLFETCHRESPONSE_HEADER']._serialized_end=697

