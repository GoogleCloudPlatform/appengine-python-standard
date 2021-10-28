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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4google/appengine/api/memcache/memcache_service.proto\x12\x10google.appengine\"\x94\x01\n\x14MemcacheServiceError\"|\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x15\n\x11UNSPECIFIED_ERROR\x10\x01\x12\x15\n\x11NAMESPACE_NOT_SET\x10\x02\x12\x15\n\x11PERMISSION_DENIED\x10\x03\x12\x11\n\rINVALID_VALUE\x10\x06\x12\x0f\n\x0bUNAVAILABLE\x10\t\"\x1d\n\x0b\x41ppOverride\x12\x0e\n\x06\x61pp_id\x18\x01 \x02(\t\"y\n\x12MemcacheGetRequest\x12\x0b\n\x03key\x18\x01 \x03(\x0c\x12\x14\n\nname_space\x18\x02 \x01(\t:\x00\x12\x0f\n\x07\x66or_cas\x18\x04 \x01(\x08\x12/\n\x08override\x18\x05 \x01(\x0b\x32\x1d.google.appengine.AppOverride\"\xe3\x02\n\x13MemcacheGetResponse\x12\x38\n\x04item\x18\x01 \x03(\n2*.google.appengine.MemcacheGetResponse.Item\x12G\n\nget_status\x18\x07 \x03(\x0e\x32\x33.google.appengine.MemcacheGetResponse.GetStatusCode\x1a]\n\x04Item\x12\x0b\n\x03key\x18\x02 \x02(\x0c\x12\r\n\x05value\x18\x03 \x02(\x0c\x12\r\n\x05\x66lags\x18\x04 \x01(\x07\x12\x0e\n\x06\x63\x61s_id\x18\x05 \x01(\x06\x12\x1a\n\x12\x65xpires_in_seconds\x18\x06 \x01(\x05\"j\n\rGetStatusCode\x12\x07\n\x03HIT\x10\x01\x12\x08\n\x04MISS\x10\x02\x12\r\n\tTRUNCATED\x10\x03\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x04\x12\x0f\n\x0bUNREACHABLE\x10\x05\x12\x0f\n\x0bOTHER_ERROR\x10\x06\"\x83\x03\n\x12MemcacheSetRequest\x12\x37\n\x04item\x18\x01 \x03(\n2).google.appengine.MemcacheSetRequest.Item\x12\x14\n\nname_space\x18\x07 \x01(\t:\x00\x12/\n\x08override\x18\n \x01(\x0b\x32\x1d.google.appengine.AppOverride\x1a\xb7\x01\n\x04Item\x12\x0b\n\x03key\x18\x02 \x02(\x0c\x12\r\n\x05value\x18\x03 \x02(\x0c\x12\r\n\x05\x66lags\x18\x04 \x01(\x07\x12G\n\nset_policy\x18\x05 \x01(\x0e\x32..google.appengine.MemcacheSetRequest.SetPolicy:\x03SET\x12\x1a\n\x0f\x65xpiration_time\x18\x06 \x01(\x07:\x01\x30\x12\x0e\n\x06\x63\x61s_id\x18\x08 \x01(\x06\x12\x0f\n\x07\x66or_cas\x18\t \x01(\x08\"3\n\tSetPolicy\x12\x07\n\x03SET\x10\x01\x12\x07\n\x03\x41\x44\x44\x10\x02\x12\x0b\n\x07REPLACE\x10\x03\x12\x07\n\x03\x43\x41S\x10\x04\"\xdb\x01\n\x13MemcacheSetResponse\x12G\n\nset_status\x18\x01 \x03(\x0e\x32\x33.google.appengine.MemcacheSetResponse.SetStatusCode\"{\n\rSetStatusCode\x12\n\n\x06STORED\x10\x01\x12\x0e\n\nNOT_STORED\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\n\n\x06\x45XISTS\x10\x04\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x05\x12\x0f\n\x0bUNREACHABLE\x10\x06\x12\x0f\n\x0bOTHER_ERROR\x10\x07\"\xc7\x01\n\x15MemcacheDeleteRequest\x12:\n\x04item\x18\x01 \x03(\n2,.google.appengine.MemcacheDeleteRequest.Item\x12\x14\n\nname_space\x18\x04 \x01(\t:\x00\x12/\n\x08override\x18\x05 \x01(\x0b\x32\x1d.google.appengine.AppOverride\x1a+\n\x04Item\x12\x0b\n\x03key\x18\x02 \x02(\x0c\x12\x16\n\x0b\x64\x65lete_time\x18\x03 \x01(\x07:\x01\x30\"\xd3\x01\n\x16MemcacheDeleteResponse\x12P\n\rdelete_status\x18\x01 \x03(\x0e\x32\x39.google.appengine.MemcacheDeleteResponse.DeleteStatusCode\"g\n\x10\x44\x65leteStatusCode\x12\x0b\n\x07\x44\x45LETED\x10\x01\x12\r\n\tNOT_FOUND\x10\x02\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x03\x12\x0f\n\x0bUNREACHABLE\x10\x04\x12\x0f\n\x0bOTHER_ERROR\x10\x05\"\xad\x02\n\x18MemcacheIncrementRequest\x12\x0b\n\x03key\x18\x01 \x02(\x0c\x12\x14\n\nname_space\x18\x04 \x01(\t:\x00\x12\x10\n\x05\x64\x65lta\x18\x02 \x01(\x04:\x01\x31\x12R\n\tdirection\x18\x03 \x01(\x0e\x32\x34.google.appengine.MemcacheIncrementRequest.Direction:\tINCREMENT\x12\x15\n\rinitial_value\x18\x05 \x01(\x04\x12\x15\n\rinitial_flags\x18\x06 \x01(\x07\x12/\n\x08override\x18\x07 \x01(\x0b\x32\x1d.google.appengine.AppOverride\")\n\tDirection\x12\r\n\tINCREMENT\x10\x01\x12\r\n\tDECREMENT\x10\x02\"\xfd\x01\n\x19MemcacheIncrementResponse\x12\x11\n\tnew_value\x18\x01 \x01(\x04\x12Y\n\x10increment_status\x18\x02 \x01(\x0e\x32?.google.appengine.MemcacheIncrementResponse.IncrementStatusCode\"r\n\x13IncrementStatusCode\x12\x06\n\x02OK\x10\x01\x12\x0f\n\x0bNOT_CHANGED\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x04\x12\x0f\n\x0bUNREACHABLE\x10\x05\x12\x0f\n\x0bOTHER_ERROR\x10\x06\"\xa0\x01\n\x1dMemcacheBatchIncrementRequest\x12\x14\n\nname_space\x18\x01 \x01(\t:\x00\x12\x38\n\x04item\x18\x02 \x03(\x0b\x32*.google.appengine.MemcacheIncrementRequest\x12/\n\x08override\x18\x03 \x01(\x0b\x32\x1d.google.appengine.AppOverride\"[\n\x1eMemcacheBatchIncrementResponse\x12\x39\n\x04item\x18\x01 \x03(\x0b\x32+.google.appengine.MemcacheIncrementResponse\"G\n\x14MemcacheFlushRequest\x12/\n\x08override\x18\x01 \x01(\x0b\x32\x1d.google.appengine.AppOverride\"\x17\n\x15MemcacheFlushResponse\"d\n\x14MemcacheStatsRequest\x12/\n\x08override\x18\x01 \x01(\x0b\x32\x1d.google.appengine.AppOverride\x12\x1b\n\x10max_hotkey_count\x18\x02 \x01(\x05:\x01\x30\"\xb1\x01\n\x14MergedNamespaceStats\x12\x0c\n\x04hits\x18\x01 \x02(\x04\x12\x0e\n\x06misses\x18\x02 \x02(\x04\x12\x11\n\tbyte_hits\x18\x03 \x02(\x04\x12\r\n\x05items\x18\x04 \x02(\x04\x12\r\n\x05\x62ytes\x18\x05 \x02(\x04\x12\x17\n\x0foldest_item_age\x18\x06 \x02(\x07\x12\x31\n\x07hotkeys\x18\x07 \x03(\x0b\x32 .google.appengine.MemcacheHotKey\">\n\x0eMemcacheHotKey\x12\x0b\n\x03key\x18\x01 \x02(\x0c\x12\x0b\n\x03qps\x18\x02 \x02(\x01\x12\x12\n\nname_space\x18\x03 \x01(\t\"N\n\x15MemcacheStatsResponse\x12\x35\n\x05stats\x18\x01 \x01(\x0b\x32&.google.appengine.MergedNamespaceStatsB9\n!com.google.appengine.api.memcacheB\x11MemcacheServicePb\x88\x01\x01')



_MEMCACHESERVICEERROR = DESCRIPTOR.message_types_by_name['MemcacheServiceError']
_APPOVERRIDE = DESCRIPTOR.message_types_by_name['AppOverride']
_MEMCACHEGETREQUEST = DESCRIPTOR.message_types_by_name['MemcacheGetRequest']
_MEMCACHEGETRESPONSE = DESCRIPTOR.message_types_by_name['MemcacheGetResponse']
_MEMCACHEGETRESPONSE_ITEM = _MEMCACHEGETRESPONSE.nested_types_by_name['Item']
_MEMCACHESETREQUEST = DESCRIPTOR.message_types_by_name['MemcacheSetRequest']
_MEMCACHESETREQUEST_ITEM = _MEMCACHESETREQUEST.nested_types_by_name['Item']
_MEMCACHESETRESPONSE = DESCRIPTOR.message_types_by_name['MemcacheSetResponse']
_MEMCACHEDELETEREQUEST = DESCRIPTOR.message_types_by_name['MemcacheDeleteRequest']
_MEMCACHEDELETEREQUEST_ITEM = _MEMCACHEDELETEREQUEST.nested_types_by_name['Item']
_MEMCACHEDELETERESPONSE = DESCRIPTOR.message_types_by_name['MemcacheDeleteResponse']
_MEMCACHEINCREMENTREQUEST = DESCRIPTOR.message_types_by_name['MemcacheIncrementRequest']
_MEMCACHEINCREMENTRESPONSE = DESCRIPTOR.message_types_by_name['MemcacheIncrementResponse']
_MEMCACHEBATCHINCREMENTREQUEST = DESCRIPTOR.message_types_by_name['MemcacheBatchIncrementRequest']
_MEMCACHEBATCHINCREMENTRESPONSE = DESCRIPTOR.message_types_by_name['MemcacheBatchIncrementResponse']
_MEMCACHEFLUSHREQUEST = DESCRIPTOR.message_types_by_name['MemcacheFlushRequest']
_MEMCACHEFLUSHRESPONSE = DESCRIPTOR.message_types_by_name['MemcacheFlushResponse']
_MEMCACHESTATSREQUEST = DESCRIPTOR.message_types_by_name['MemcacheStatsRequest']
_MERGEDNAMESPACESTATS = DESCRIPTOR.message_types_by_name['MergedNamespaceStats']
_MEMCACHEHOTKEY = DESCRIPTOR.message_types_by_name['MemcacheHotKey']
_MEMCACHESTATSRESPONSE = DESCRIPTOR.message_types_by_name['MemcacheStatsResponse']
_MEMCACHESERVICEERROR_ERRORCODE = _MEMCACHESERVICEERROR.enum_types_by_name['ErrorCode']
_MEMCACHEGETRESPONSE_GETSTATUSCODE = _MEMCACHEGETRESPONSE.enum_types_by_name['GetStatusCode']
_MEMCACHESETREQUEST_SETPOLICY = _MEMCACHESETREQUEST.enum_types_by_name['SetPolicy']
_MEMCACHESETRESPONSE_SETSTATUSCODE = _MEMCACHESETRESPONSE.enum_types_by_name['SetStatusCode']
_MEMCACHEDELETERESPONSE_DELETESTATUSCODE = _MEMCACHEDELETERESPONSE.enum_types_by_name['DeleteStatusCode']
_MEMCACHEINCREMENTREQUEST_DIRECTION = _MEMCACHEINCREMENTREQUEST.enum_types_by_name['Direction']
_MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE = _MEMCACHEINCREMENTRESPONSE.enum_types_by_name['IncrementStatusCode']
MemcacheServiceError = _reflection.GeneratedProtocolMessageType('MemcacheServiceError', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHESERVICEERROR,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheServiceError)

AppOverride = _reflection.GeneratedProtocolMessageType('AppOverride', (_message.Message,), {
  'DESCRIPTOR' : _APPOVERRIDE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(AppOverride)

MemcacheGetRequest = _reflection.GeneratedProtocolMessageType('MemcacheGetRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEGETREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheGetRequest)

MemcacheGetResponse = _reflection.GeneratedProtocolMessageType('MemcacheGetResponse', (_message.Message,), {

  'Item' : _reflection.GeneratedProtocolMessageType('Item', (_message.Message,), {
    'DESCRIPTOR' : _MEMCACHEGETRESPONSE_ITEM,
    '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

    })
  ,
  'DESCRIPTOR' : _MEMCACHEGETRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheGetResponse)
_sym_db.RegisterMessage(MemcacheGetResponse.Item)

MemcacheSetRequest = _reflection.GeneratedProtocolMessageType('MemcacheSetRequest', (_message.Message,), {

  'Item' : _reflection.GeneratedProtocolMessageType('Item', (_message.Message,), {
    'DESCRIPTOR' : _MEMCACHESETREQUEST_ITEM,
    '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

    })
  ,
  'DESCRIPTOR' : _MEMCACHESETREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheSetRequest)
_sym_db.RegisterMessage(MemcacheSetRequest.Item)

MemcacheSetResponse = _reflection.GeneratedProtocolMessageType('MemcacheSetResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHESETRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheSetResponse)

MemcacheDeleteRequest = _reflection.GeneratedProtocolMessageType('MemcacheDeleteRequest', (_message.Message,), {

  'Item' : _reflection.GeneratedProtocolMessageType('Item', (_message.Message,), {
    'DESCRIPTOR' : _MEMCACHEDELETEREQUEST_ITEM,
    '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

    })
  ,
  'DESCRIPTOR' : _MEMCACHEDELETEREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheDeleteRequest)
_sym_db.RegisterMessage(MemcacheDeleteRequest.Item)

MemcacheDeleteResponse = _reflection.GeneratedProtocolMessageType('MemcacheDeleteResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEDELETERESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheDeleteResponse)

MemcacheIncrementRequest = _reflection.GeneratedProtocolMessageType('MemcacheIncrementRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEINCREMENTREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheIncrementRequest)

MemcacheIncrementResponse = _reflection.GeneratedProtocolMessageType('MemcacheIncrementResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEINCREMENTRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheIncrementResponse)

MemcacheBatchIncrementRequest = _reflection.GeneratedProtocolMessageType('MemcacheBatchIncrementRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEBATCHINCREMENTREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheBatchIncrementRequest)

MemcacheBatchIncrementResponse = _reflection.GeneratedProtocolMessageType('MemcacheBatchIncrementResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEBATCHINCREMENTRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheBatchIncrementResponse)

MemcacheFlushRequest = _reflection.GeneratedProtocolMessageType('MemcacheFlushRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEFLUSHREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheFlushRequest)

MemcacheFlushResponse = _reflection.GeneratedProtocolMessageType('MemcacheFlushResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEFLUSHRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheFlushResponse)

MemcacheStatsRequest = _reflection.GeneratedProtocolMessageType('MemcacheStatsRequest', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHESTATSREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheStatsRequest)

MergedNamespaceStats = _reflection.GeneratedProtocolMessageType('MergedNamespaceStats', (_message.Message,), {
  'DESCRIPTOR' : _MERGEDNAMESPACESTATS,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MergedNamespaceStats)

MemcacheHotKey = _reflection.GeneratedProtocolMessageType('MemcacheHotKey', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHEHOTKEY,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheHotKey)

MemcacheStatsResponse = _reflection.GeneratedProtocolMessageType('MemcacheStatsResponse', (_message.Message,), {
  'DESCRIPTOR' : _MEMCACHESTATSRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_service_pb2'

  })
_sym_db.RegisterMessage(MemcacheStatsResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n!com.google.appengine.api.memcacheB\021MemcacheServicePb\210\001\001'
  _MEMCACHESERVICEERROR._serialized_start=75
  _MEMCACHESERVICEERROR._serialized_end=223
  _MEMCACHESERVICEERROR_ERRORCODE._serialized_start=99
  _MEMCACHESERVICEERROR_ERRORCODE._serialized_end=223
  _APPOVERRIDE._serialized_start=225
  _APPOVERRIDE._serialized_end=254
  _MEMCACHEGETREQUEST._serialized_start=256
  _MEMCACHEGETREQUEST._serialized_end=377
  _MEMCACHEGETRESPONSE._serialized_start=380
  _MEMCACHEGETRESPONSE._serialized_end=735
  _MEMCACHEGETRESPONSE_ITEM._serialized_start=534
  _MEMCACHEGETRESPONSE_ITEM._serialized_end=627
  _MEMCACHEGETRESPONSE_GETSTATUSCODE._serialized_start=629
  _MEMCACHEGETRESPONSE_GETSTATUSCODE._serialized_end=735
  _MEMCACHESETREQUEST._serialized_start=738
  _MEMCACHESETREQUEST._serialized_end=1125
  _MEMCACHESETREQUEST_ITEM._serialized_start=889
  _MEMCACHESETREQUEST_ITEM._serialized_end=1072
  _MEMCACHESETREQUEST_SETPOLICY._serialized_start=1074
  _MEMCACHESETREQUEST_SETPOLICY._serialized_end=1125
  _MEMCACHESETRESPONSE._serialized_start=1128
  _MEMCACHESETRESPONSE._serialized_end=1347
  _MEMCACHESETRESPONSE_SETSTATUSCODE._serialized_start=1224
  _MEMCACHESETRESPONSE_SETSTATUSCODE._serialized_end=1347
  _MEMCACHEDELETEREQUEST._serialized_start=1350
  _MEMCACHEDELETEREQUEST._serialized_end=1549
  _MEMCACHEDELETEREQUEST_ITEM._serialized_start=1506
  _MEMCACHEDELETEREQUEST_ITEM._serialized_end=1549
  _MEMCACHEDELETERESPONSE._serialized_start=1552
  _MEMCACHEDELETERESPONSE._serialized_end=1763
  _MEMCACHEDELETERESPONSE_DELETESTATUSCODE._serialized_start=1660
  _MEMCACHEDELETERESPONSE_DELETESTATUSCODE._serialized_end=1763
  _MEMCACHEINCREMENTREQUEST._serialized_start=1766
  _MEMCACHEINCREMENTREQUEST._serialized_end=2067
  _MEMCACHEINCREMENTREQUEST_DIRECTION._serialized_start=2026
  _MEMCACHEINCREMENTREQUEST_DIRECTION._serialized_end=2067
  _MEMCACHEINCREMENTRESPONSE._serialized_start=2070
  _MEMCACHEINCREMENTRESPONSE._serialized_end=2323
  _MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE._serialized_start=2209
  _MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE._serialized_end=2323
  _MEMCACHEBATCHINCREMENTREQUEST._serialized_start=2326
  _MEMCACHEBATCHINCREMENTREQUEST._serialized_end=2486
  _MEMCACHEBATCHINCREMENTRESPONSE._serialized_start=2488
  _MEMCACHEBATCHINCREMENTRESPONSE._serialized_end=2579
  _MEMCACHEFLUSHREQUEST._serialized_start=2581
  _MEMCACHEFLUSHREQUEST._serialized_end=2652
  _MEMCACHEFLUSHRESPONSE._serialized_start=2654
  _MEMCACHEFLUSHRESPONSE._serialized_end=2677
  _MEMCACHESTATSREQUEST._serialized_start=2679
  _MEMCACHESTATSREQUEST._serialized_end=2779
  _MERGEDNAMESPACESTATS._serialized_start=2782
  _MERGEDNAMESPACESTATS._serialized_end=2959
  _MEMCACHEHOTKEY._serialized_start=2961
  _MEMCACHEHOTKEY._serialized_end=3023
  _MEMCACHESTATSRESPONSE._serialized_start=3025
  _MEMCACHESTATSRESPONSE._serialized_end=3103

