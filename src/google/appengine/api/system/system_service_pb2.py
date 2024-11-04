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
    'google/appengine/api/system/system_service.proto'
)


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0google/appengine/api/system/system_service.proto\x12\x10google.appengine\"f\n\x12SystemServiceError\"P\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x12\n\x0eINTERNAL_ERROR\x10\x01\x12\x14\n\x10\x42\x41\x43KEND_REQUIRED\x10\x02\x12\x11\n\rLIMIT_REACHED\x10\x03\"t\n\nSystemStat\x12\x0f\n\x07\x63urrent\x18\x01 \x01(\x01\x12\x11\n\taverage1m\x18\x03 \x01(\x01\x12\x12\n\naverage10m\x18\x04 \x01(\x01\x12\r\n\x05total\x18\x02 \x01(\x01\x12\x0e\n\x06rate1m\x18\x05 \x01(\x01\x12\x0f\n\x07rate10m\x18\x06 \x01(\x01\"\x17\n\x15GetSystemStatsRequest\"q\n\x16GetSystemStatsResponse\x12)\n\x03\x63pu\x18\x01 \x01(\x0b\x32\x1c.google.appengine.SystemStat\x12,\n\x06memory\x18\x02 \x01(\x0b\x32\x1c.google.appengine.SystemStat\"\x1f\n\x1dStartBackgroundRequestRequest\"4\n\x1eStartBackgroundRequestResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\tB2\n\x1f\x63om.google.appengine.api.systemB\x0fSystemServicePb')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.appengine.api.system.system_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\037com.google.appengine.api.systemB\017SystemServicePb'
  _globals['_SYSTEMSERVICEERROR']._serialized_start=70
  _globals['_SYSTEMSERVICEERROR']._serialized_end=172
  _globals['_SYSTEMSERVICEERROR_ERRORCODE']._serialized_start=92
  _globals['_SYSTEMSERVICEERROR_ERRORCODE']._serialized_end=172
  _globals['_SYSTEMSTAT']._serialized_start=174
  _globals['_SYSTEMSTAT']._serialized_end=290
  _globals['_GETSYSTEMSTATSREQUEST']._serialized_start=292
  _globals['_GETSYSTEMSTATSREQUEST']._serialized_end=315
  _globals['_GETSYSTEMSTATSRESPONSE']._serialized_start=317
  _globals['_GETSYSTEMSTATSRESPONSE']._serialized_end=430
  _globals['_STARTBACKGROUNDREQUESTREQUEST']._serialized_start=432
  _globals['_STARTBACKGROUNDREQUESTREQUEST']._serialized_end=463
  _globals['_STARTBACKGROUNDREQUESTRESPONSE']._serialized_start=465
  _globals['_STARTBACKGROUNDREQUESTRESPONSE']._serialized_end=517

