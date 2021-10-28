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


from google.appengine.api import api_base_pb2 as google_dot_appengine_dot_api_dot_api__base__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9google/appengine/api/memcache/memcache_stub_service.proto\x12\x10google.appengine\x1a#google/appengine/api/api_base.proto\"+\n\x11SetMaxSizeRequest\x12\x16\n\x0emax_size_bytes\x18\x01 \x02(\x03\"1\n\x19GetLruChainLengthResponse\x12\x14\n\x0c\x63hain_length\x18\x01 \x02(\x03\"2\n\x0fSetClockRequest\x12\x1f\n\x17\x63lock_time_milliseconds\x18\x01 \x02(\x03\"+\n\x13\x41\x64vanceClockRequest\x12\x14\n\x0cmilliseconds\x18\x01 \x02(\x03\"7\n\x14\x41\x64vanceClockResponse\x12\x1f\n\x17\x63lock_time_milliseconds\x18\x01 \x02(\x03\x42:\n!com.google.appengine.api.memcacheB\x15MemcacheStubServicePb')



_SETMAXSIZEREQUEST = DESCRIPTOR.message_types_by_name['SetMaxSizeRequest']
_GETLRUCHAINLENGTHRESPONSE = DESCRIPTOR.message_types_by_name['GetLruChainLengthResponse']
_SETCLOCKREQUEST = DESCRIPTOR.message_types_by_name['SetClockRequest']
_ADVANCECLOCKREQUEST = DESCRIPTOR.message_types_by_name['AdvanceClockRequest']
_ADVANCECLOCKRESPONSE = DESCRIPTOR.message_types_by_name['AdvanceClockResponse']
SetMaxSizeRequest = _reflection.GeneratedProtocolMessageType('SetMaxSizeRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETMAXSIZEREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(SetMaxSizeRequest)

GetLruChainLengthResponse = _reflection.GeneratedProtocolMessageType('GetLruChainLengthResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETLRUCHAINLENGTHRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(GetLruChainLengthResponse)

SetClockRequest = _reflection.GeneratedProtocolMessageType('SetClockRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETCLOCKREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(SetClockRequest)

AdvanceClockRequest = _reflection.GeneratedProtocolMessageType('AdvanceClockRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADVANCECLOCKREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(AdvanceClockRequest)

AdvanceClockResponse = _reflection.GeneratedProtocolMessageType('AdvanceClockResponse', (_message.Message,), {
  'DESCRIPTOR' : _ADVANCECLOCKRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(AdvanceClockResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!com.google.appengine.api.memcacheB\025MemcacheStubServicePb'
  _SETMAXSIZEREQUEST._serialized_start=116
  _SETMAXSIZEREQUEST._serialized_end=159
  _GETLRUCHAINLENGTHRESPONSE._serialized_start=161
  _GETLRUCHAINLENGTHRESPONSE._serialized_end=210
  _SETCLOCKREQUEST._serialized_start=212
  _SETCLOCKREQUEST._serialized_end=262
  _ADVANCECLOCKREQUEST._serialized_start=264
  _ADVANCECLOCKREQUEST._serialized_end=307
  _ADVANCECLOCKRESPONSE._serialized_start=309
  _ADVANCECLOCKRESPONSE._serialized_end=364

