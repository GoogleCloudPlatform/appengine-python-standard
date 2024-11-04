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
    'google/appengine/api/modules/modules_service.proto'
)


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2google/appengine/api/modules/modules_service.proto\x12\x10google.appengine\"\x95\x01\n\x13ModulesServiceError\"~\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x12\n\x0eINVALID_MODULE\x10\x01\x12\x13\n\x0fINVALID_VERSION\x10\x02\x12\x15\n\x11INVALID_INSTANCES\x10\x03\x12\x13\n\x0fTRANSIENT_ERROR\x10\x04\x12\x14\n\x10UNEXPECTED_STATE\x10\x05\"\x13\n\x11GetModulesRequest\"$\n\x12GetModulesResponse\x12\x0e\n\x06module\x18\x01 \x03(\t\"$\n\x12GetVersionsRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\"&\n\x13GetVersionsResponse\x12\x0f\n\x07version\x18\x01 \x03(\t\"*\n\x18GetDefaultVersionRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\",\n\x19GetDefaultVersionResponse\x12\x0f\n\x07version\x18\x01 \x01(\t\"9\n\x16GetNumInstancesRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\",\n\x17GetNumInstancesResponse\x12\x11\n\tinstances\x18\x01 \x01(\x03\"L\n\x16SetNumInstancesRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x11\n\tinstances\x18\x03 \x01(\x03\"\x19\n\x17SetNumInstancesResponse\"5\n\x12StartModuleRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\"\x15\n\x13StartModuleResponse\"4\n\x11StopModuleRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\"\x14\n\x12StopModuleResponse\"G\n\x12GetHostnameRequest\x12\x0e\n\x06module\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x10\n\x08instance\x18\x03 \x01(\t\"\'\n\x13GetHostnameResponse\x12\x10\n\x08hostname\x18\x01 \x01(\tB4\n com.google.appengine.api.modulesB\x10ModulesServicePb')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.appengine.api.modules.modules_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n com.google.appengine.api.modulesB\020ModulesServicePb'
  _globals['_MODULESSERVICEERROR']._serialized_start=73
  _globals['_MODULESSERVICEERROR']._serialized_end=222
  _globals['_MODULESSERVICEERROR_ERRORCODE']._serialized_start=96
  _globals['_MODULESSERVICEERROR_ERRORCODE']._serialized_end=222
  _globals['_GETMODULESREQUEST']._serialized_start=224
  _globals['_GETMODULESREQUEST']._serialized_end=243
  _globals['_GETMODULESRESPONSE']._serialized_start=245
  _globals['_GETMODULESRESPONSE']._serialized_end=281
  _globals['_GETVERSIONSREQUEST']._serialized_start=283
  _globals['_GETVERSIONSREQUEST']._serialized_end=319
  _globals['_GETVERSIONSRESPONSE']._serialized_start=321
  _globals['_GETVERSIONSRESPONSE']._serialized_end=359
  _globals['_GETDEFAULTVERSIONREQUEST']._serialized_start=361
  _globals['_GETDEFAULTVERSIONREQUEST']._serialized_end=403
  _globals['_GETDEFAULTVERSIONRESPONSE']._serialized_start=405
  _globals['_GETDEFAULTVERSIONRESPONSE']._serialized_end=449
  _globals['_GETNUMINSTANCESREQUEST']._serialized_start=451
  _globals['_GETNUMINSTANCESREQUEST']._serialized_end=508
  _globals['_GETNUMINSTANCESRESPONSE']._serialized_start=510
  _globals['_GETNUMINSTANCESRESPONSE']._serialized_end=554
  _globals['_SETNUMINSTANCESREQUEST']._serialized_start=556
  _globals['_SETNUMINSTANCESREQUEST']._serialized_end=632
  _globals['_SETNUMINSTANCESRESPONSE']._serialized_start=634
  _globals['_SETNUMINSTANCESRESPONSE']._serialized_end=659
  _globals['_STARTMODULEREQUEST']._serialized_start=661
  _globals['_STARTMODULEREQUEST']._serialized_end=714
  _globals['_STARTMODULERESPONSE']._serialized_start=716
  _globals['_STARTMODULERESPONSE']._serialized_end=737
  _globals['_STOPMODULEREQUEST']._serialized_start=739
  _globals['_STOPMODULEREQUEST']._serialized_end=791
  _globals['_STOPMODULERESPONSE']._serialized_start=793
  _globals['_STOPMODULERESPONSE']._serialized_end=813
  _globals['_GETHOSTNAMEREQUEST']._serialized_start=815
  _globals['_GETHOSTNAMEREQUEST']._serialized_end=886
  _globals['_GETHOSTNAMERESPONSE']._serialized_start=888
  _globals['_GETHOSTNAMERESPONSE']._serialized_end=927

