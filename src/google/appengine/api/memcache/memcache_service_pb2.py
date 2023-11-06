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
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4google/appengine/api/memcache/memcache_service.proto\x12\x10google.appengine\"\x94\x01\n\x14MemcacheServiceError\"|\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x15\n\x11UNSPECIFIED_ERROR\x10\x01\x12\x15\n\x11NAMESPACE_NOT_SET\x10\x02\x12\x15\n\x11PERMISSION_DENIED\x10\x03\x12\x11\n\rINVALID_VALUE\x10\x06\x12\x0f\n\x0bUNAVAILABLE\x10\t\"\x1d\n\x0b\x41ppOverride\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\"\x8b\x01\n\x12MemcacheGetRequest\x12\x0b\n\x03key\x18\x01 \x03(\x0c\x12\x14\n\nname_space\x18\x02 \x01(\t:\x00\x12\x0f\n\x07\x66or_cas\x18\x04 \x01(\x08\x12/\n\x08override\x18\x05 \x01(\x0b\x32\x1d.google.appengine.AppOverride\x12\x10\n\x08\x66or_peek\x18\x06 \x01(\x08\"i\n\x0eItemTimestamps\x12\x1b\n\x13\x65xpiration_time_sec\x18\x01 \x01(\x03\x12\x1c\n\x14last_access_time_sec\x18\x02 \x01(\x03\x12\x1c\n\x14\x64\x65lete_lock_time_sec\x18\x03 \x01(\x03\"\xb4\x03\n\x13MemcacheGetResponse\x12\x38\n\x04item\x18\x01 \x03(\n2*.google.appengine.MemcacheGetResponse.Item\x12G\n\nget_status\x18\x07 \x03(\x0e\x32\x33.google.appengine.MemcacheGetResponse.GetStatusCode\x1a\xad\x01\n\x04Item\x12\x0b\n\x03key\x18\x02 \x01(\x0c\x12\r\n\x05value\x18\x03 \x01(\x0c\x12\r\n\x05\x66lags\x18\x04 \x01(\x07\x12\x0e\n\x06\x63\x61s_id\x18\x05 \x01(\x06\x12\x1a\n\x12\x65xpires_in_seconds\x18\x06 \x01(\x05\x12\x34\n\ntimestamps\x18\x08 \x01(\x0b\x32 .google.appengine.ItemTimestamps\x12\x18\n\x10is_delete_locked\x18\t \x01(\x08\"j\n\rGetStatusCode\x12\x07\n\x03HIT\x10\x01\x12\x08\n\x04MISS\x10\x02\x12\r\n\tTRUNCATED\x10\x03\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x04\x12\x0f\n\x0bUNREACHABLE\x10\x05\x12\x0f\n\x0bOTHER_ERROR\x10\x06\"\x83\x03\n\x12MemcacheSetRequest\x12\x37\n\x04item\x18\x01 \x03(\n2).google.appengine.MemcacheSetRequest.Item\x12\x14\n\nname_space\x18\x07 \x01(\t:\x00\x12/\n\x08override\x18\n \x01(\x0b\x32\x1d.google.appengine.AppOverride\x1a\xb7\x01\n\x04Item\x12\x0b\n\x03key\x18\x02 \x01(\x0c\x12\r\n\x05value\x18\x03 \x01(\x0c\x12\r\n\x05\x66lags\x18\x04 \x01(\x07\x12G\n\nset_policy\x18\x05 \x01(\x0e\x32..google.appengine.MemcacheSetRequest.SetPolicy:\x03SET\x12\x1a\n\x0f\x65xpiration_time\x18\x06 \x01(\x07:\x01\x30\x12\x0e\n\x06\x63\x61s_id\x18\x08 \x01(\x06\x12\x0f\n\x07\x66or_cas\x18\t \x01(\x08\"3\n\tSetPolicy\x12\x07\n\x03SET\x10\x01\x12\x07\n\x03\x41\x44\x44\x10\x02\x12\x0b\n\x07REPLACE\x10\x03\x12\x07\n\x03\x43\x41S\x10\x04\"\xdb\x01\n\x13MemcacheSetResponse\x12G\n\nset_status\x18\x01 \x03(\x0e\x32\x33.google.appengine.MemcacheSetResponse.SetStatusCode\"{\n\rSetStatusCode\x12\n\n\x06STORED\x10\x01\x12\x0e\n\nNOT_STORED\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\n\n\x06\x45XISTS\x10\x04\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x05\x12\x0f\n\x0bUNREACHABLE\x10\x06\x12\x0f\n\x0bOTHER_ERROR\x10\x07\"\xc7\x01\n\x15MemcacheDeleteRequest\x12:\n\x04item\x18\x01 \x03(\n2,.google.appengine.MemcacheDeleteRequest.Item\x12\x14\n\nname_space\x18\x04 \x01(\t:\x00\x12/\n\x08override\x18\x05 \x01(\x0b\x32\x1d.google.appengine.AppOverride\x1a+\n\x04Item\x12\x0b\n\x03key\x18\x02 \x01(\x0c\x12\x16\n\x0b\x64\x65lete_time\x18\x03 \x01(\x07:\x01\x30\"\xd3\x01\n\x16MemcacheDeleteResponse\x12P\n\rdelete_status\x18\x01 \x03(\x0e\x32\x39.google.appengine.MemcacheDeleteResponse.DeleteStatusCode\"g\n\x10\x44\x65leteStatusCode\x12\x0b\n\x07\x44\x45LETED\x10\x01\x12\r\n\tNOT_FOUND\x10\x02\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x03\x12\x0f\n\x0bUNREACHABLE\x10\x04\x12\x0f\n\x0bOTHER_ERROR\x10\x05\"\xad\x02\n\x18MemcacheIncrementRequest\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\x14\n\nname_space\x18\x04 \x01(\t:\x00\x12\x10\n\x05\x64\x65lta\x18\x02 \x01(\x04:\x01\x31\x12R\n\tdirection\x18\x03 \x01(\x0e\x32\x34.google.appengine.MemcacheIncrementRequest.Direction:\tINCREMENT\x12\x15\n\rinitial_value\x18\x05 \x01(\x04\x12\x15\n\rinitial_flags\x18\x06 \x01(\x07\x12/\n\x08override\x18\x07 \x01(\x0b\x32\x1d.google.appengine.AppOverride\")\n\tDirection\x12\r\n\tINCREMENT\x10\x01\x12\r\n\tDECREMENT\x10\x02\"\xfd\x01\n\x19MemcacheIncrementResponse\x12\x11\n\tnew_value\x18\x01 \x01(\x04\x12Y\n\x10increment_status\x18\x02 \x01(\x0e\x32?.google.appengine.MemcacheIncrementResponse.IncrementStatusCode\"r\n\x13IncrementStatusCode\x12\x06\n\x02OK\x10\x01\x12\x0f\n\x0bNOT_CHANGED\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x04\x12\x0f\n\x0bUNREACHABLE\x10\x05\x12\x0f\n\x0bOTHER_ERROR\x10\x06\"\xa0\x01\n\x1dMemcacheBatchIncrementRequest\x12\x14\n\nname_space\x18\x01 \x01(\t:\x00\x12\x38\n\x04item\x18\x02 \x03(\x0b\x32*.google.appengine.MemcacheIncrementRequest\x12/\n\x08override\x18\x03 \x01(\x0b\x32\x1d.google.appengine.AppOverride\"[\n\x1eMemcacheBatchIncrementResponse\x12\x39\n\x04item\x18\x01 \x03(\x0b\x32+.google.appengine.MemcacheIncrementResponse\"G\n\x14MemcacheFlushRequest\x12/\n\x08override\x18\x01 \x01(\x0b\x32\x1d.google.appengine.AppOverride\"\x17\n\x15MemcacheFlushResponse\"d\n\x14MemcacheStatsRequest\x12/\n\x08override\x18\x01 \x01(\x0b\x32\x1d.google.appengine.AppOverride\x12\x1b\n\x10max_hotkey_count\x18\x02 \x01(\x05:\x01\x30\"\xb1\x01\n\x14MergedNamespaceStats\x12\x0c\n\x04hits\x18\x01 \x01(\x04\x12\x0e\n\x06misses\x18\x02 \x01(\x04\x12\x11\n\tbyte_hits\x18\x03 \x01(\x04\x12\r\n\x05items\x18\x04 \x01(\x04\x12\r\n\x05\x62ytes\x18\x05 \x01(\x04\x12\x17\n\x0foldest_item_age\x18\x06 \x01(\x07\x12\x31\n\x07hotkeys\x18\x07 \x03(\x0b\x32 .google.appengine.MemcacheHotKey\">\n\x0eMemcacheHotKey\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\x0b\n\x03qps\x18\x02 \x01(\x01\x12\x12\n\nname_space\x18\x03 \x01(\t\"N\n\x15MemcacheStatsResponse\x12\x35\n\x05stats\x18\x01 \x01(\x0b\x32&.google.appengine.MergedNamespaceStatsB9\n!com.google.appengine.api.memcacheB\x11MemcacheServicePb\x88\x01\x01')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.appengine.api.memcache.memcache_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n!com.google.appengine.api.memcacheB\021MemcacheServicePb\210\001\001'
  _globals['_MEMCACHESERVICEERROR']._serialized_start=75
  _globals['_MEMCACHESERVICEERROR']._serialized_end=223
  _globals['_MEMCACHESERVICEERROR_ERRORCODE']._serialized_start=99
  _globals['_MEMCACHESERVICEERROR_ERRORCODE']._serialized_end=223
  _globals['_APPOVERRIDE']._serialized_start=225
  _globals['_APPOVERRIDE']._serialized_end=254
  _globals['_MEMCACHEGETREQUEST']._serialized_start=257
  _globals['_MEMCACHEGETREQUEST']._serialized_end=396
  _globals['_ITEMTIMESTAMPS']._serialized_start=398
  _globals['_ITEMTIMESTAMPS']._serialized_end=503
  _globals['_MEMCACHEGETRESPONSE']._serialized_start=506
  _globals['_MEMCACHEGETRESPONSE']._serialized_end=942
  _globals['_MEMCACHEGETRESPONSE_ITEM']._serialized_start=661
  _globals['_MEMCACHEGETRESPONSE_ITEM']._serialized_end=834
  _globals['_MEMCACHEGETRESPONSE_GETSTATUSCODE']._serialized_start=836
  _globals['_MEMCACHEGETRESPONSE_GETSTATUSCODE']._serialized_end=942
  _globals['_MEMCACHESETREQUEST']._serialized_start=945
  _globals['_MEMCACHESETREQUEST']._serialized_end=1332
  _globals['_MEMCACHESETREQUEST_ITEM']._serialized_start=1096
  _globals['_MEMCACHESETREQUEST_ITEM']._serialized_end=1279
  _globals['_MEMCACHESETREQUEST_SETPOLICY']._serialized_start=1281
  _globals['_MEMCACHESETREQUEST_SETPOLICY']._serialized_end=1332
  _globals['_MEMCACHESETRESPONSE']._serialized_start=1335
  _globals['_MEMCACHESETRESPONSE']._serialized_end=1554
  _globals['_MEMCACHESETRESPONSE_SETSTATUSCODE']._serialized_start=1431
  _globals['_MEMCACHESETRESPONSE_SETSTATUSCODE']._serialized_end=1554
  _globals['_MEMCACHEDELETEREQUEST']._serialized_start=1557
  _globals['_MEMCACHEDELETEREQUEST']._serialized_end=1756
  _globals['_MEMCACHEDELETEREQUEST_ITEM']._serialized_start=1713
  _globals['_MEMCACHEDELETEREQUEST_ITEM']._serialized_end=1756
  _globals['_MEMCACHEDELETERESPONSE']._serialized_start=1759
  _globals['_MEMCACHEDELETERESPONSE']._serialized_end=1970
  _globals['_MEMCACHEDELETERESPONSE_DELETESTATUSCODE']._serialized_start=1867
  _globals['_MEMCACHEDELETERESPONSE_DELETESTATUSCODE']._serialized_end=1970
  _globals['_MEMCACHEINCREMENTREQUEST']._serialized_start=1973
  _globals['_MEMCACHEINCREMENTREQUEST']._serialized_end=2274
  _globals['_MEMCACHEINCREMENTREQUEST_DIRECTION']._serialized_start=2233
  _globals['_MEMCACHEINCREMENTREQUEST_DIRECTION']._serialized_end=2274
  _globals['_MEMCACHEINCREMENTRESPONSE']._serialized_start=2277
  _globals['_MEMCACHEINCREMENTRESPONSE']._serialized_end=2530
  _globals['_MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE']._serialized_start=2416
  _globals['_MEMCACHEINCREMENTRESPONSE_INCREMENTSTATUSCODE']._serialized_end=2530
  _globals['_MEMCACHEBATCHINCREMENTREQUEST']._serialized_start=2533
  _globals['_MEMCACHEBATCHINCREMENTREQUEST']._serialized_end=2693
  _globals['_MEMCACHEBATCHINCREMENTRESPONSE']._serialized_start=2695
  _globals['_MEMCACHEBATCHINCREMENTRESPONSE']._serialized_end=2786
  _globals['_MEMCACHEFLUSHREQUEST']._serialized_start=2788
  _globals['_MEMCACHEFLUSHREQUEST']._serialized_end=2859
  _globals['_MEMCACHEFLUSHRESPONSE']._serialized_start=2861
  _globals['_MEMCACHEFLUSHRESPONSE']._serialized_end=2884
  _globals['_MEMCACHESTATSREQUEST']._serialized_start=2886
  _globals['_MEMCACHESTATSREQUEST']._serialized_end=2986
  _globals['_MERGEDNAMESPACESTATS']._serialized_start=2989
  _globals['_MERGEDNAMESPACESTATS']._serialized_end=3166
  _globals['_MEMCACHEHOTKEY']._serialized_start=3168
  _globals['_MEMCACHEHOTKEY']._serialized_end=3230
  _globals['_MEMCACHESTATSRESPONSE']._serialized_start=3232
  _globals['_MEMCACHESTATSRESPONSE']._serialized_end=3310