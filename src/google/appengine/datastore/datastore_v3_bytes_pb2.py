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


from google.appengine.datastore import action_pb2 as google_dot_appengine_dot_datastore_dot_action__pb2
from google.appengine.datastore import entity_bytes_pb2 as google_dot_appengine_dot_datastore_dot_entity__bytes__pb2
from google.appengine.datastore import snapshot_pb2 as google_dot_appengine_dot_datastore_dot_snapshot__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/datastore/datastore_v3_bytes.proto',
  package='apphosting_datastore_v3_bytes',
  syntax='proto2',
  serialized_options=b'\n%com.google.google.appengine.datastoreB\rDatastoreV3Pb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n3google/appengine/datastore/datastore_v3_bytes.proto\x12\x1d\x61pphosting_datastore_v3_bytes\x1a\'google/appengine/datastore/action.proto\x1a-google/appengine/datastore/entity_bytes.proto\x1a)google/appengine/datastore/snapshot.proto\"\xa0\x01\n\x0bTransaction\x12\x0e\n\x06handle\x18\x01 \x02(\x06\x12\x0b\n\x03\x61pp\x18\x02 \x02(\t\x12\x13\n\x0b\x64\x61tabase_id\x18\x06 \x01(\t\x12\x1b\n\x0cmark_changes\x18\x03 \x01(\x08:\x05\x66\x61lse\x12\x42\n\x0f\x63omposite_index\x18\x05 \x03(\x0b\x32).storage_onestore_v3_bytes.CompositeIndex\"\xa1\x0c\n\x05Query\x12\x0b\n\x03\x61pp\x18\x01 \x02(\t\x12\x13\n\x0b\x64\x61tabase_id\x18* \x01(\t\x12\x12\n\nname_space\x18\x1d \x01(\t\x12\x0c\n\x04kind\x18\x03 \x01(\t\x12\x36\n\x08\x61ncestor\x18\x11 \x01(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x0f\n\x07shallow\x18+ \x01(\x08\x12;\n\x06\x66ilter\x18\x04 \x03(\n2+.apphosting_datastore_v3_bytes.Query.Filter\x12\x14\n\x0csearch_query\x18\x08 \x01(\t\x12\x39\n\x05order\x18\t \x03(\n2*.apphosting_datastore_v3_bytes.Query.Order\x12\x37\n\x04hint\x18\x12 \x01(\x0e\x32).apphosting_datastore_v3_bytes.Query.Hint\x12\r\n\x05\x63ount\x18\x17 \x01(\x05\x12\x11\n\x06offset\x18\x0c \x01(\x05:\x01\x30\x12\r\n\x05limit\x18\x10 \x01(\x05\x12\x46\n\x0f\x63ompiled_cursor\x18\x1e \x01(\x0b\x32-.apphosting_datastore_v3_bytes.CompiledCursor\x12J\n\x13\x65nd_compiled_cursor\x18\x1f \x01(\x0b\x32-.apphosting_datastore_v3_bytes.CompiledCursor\x12\x42\n\x0f\x63omposite_index\x18\x13 \x03(\x0b\x32).storage_onestore_v3_bytes.CompositeIndex\x12#\n\x14require_perfect_plan\x18\x14 \x01(\x08:\x05\x66\x61lse\x12\x18\n\tkeys_only\x18\x15 \x01(\x08:\x05\x66\x61lse\x12?\n\x0btransaction\x18\x16 \x01(\x0b\x32*.apphosting_datastore_v3_bytes.Transaction\x12\x16\n\x07\x63ompile\x18\x19 \x01(\x08:\x05\x66\x61lse\x12\x13\n\x0b\x66\x61ilover_ms\x18\x1a \x01(\x03\x12\x0e\n\x06strong\x18  \x01(\x08\x12\x15\n\rproperty_name\x18! \x03(\t\x12\x1e\n\x16group_by_property_name\x18\" \x03(\t\x12\x10\n\x08\x64istinct\x18\x18 \x01(\x08\x12\x1d\n\x15min_safe_time_seconds\x18# \x01(\x03\x12\x19\n\x11safe_replica_name\x18$ \x03(\t\x12 \n\x0epersist_offset\x18% \x01(\x08:\x04trueB\x02\x18\x01\x12\x14\n\x0cread_time_us\x18, \x01(\x03\x1a\xe7\x02\n\x06\x46ilter\x12@\n\x02op\x18\x06 \x02(\x0e\x32\x34.apphosting_datastore_v3_bytes.Query.Filter.Operator\x12\x35\n\x08property\x18\x0e \x03(\x0b\x32#.storage_onestore_v3_bytes.Property\x12<\n\ngeo_region\x18( \x01(\x0b\x32(.apphosting_datastore_v3_bytes.GeoRegion\"\xa5\x01\n\x08Operator\x12\r\n\tLESS_THAN\x10\x01\x12\x16\n\x12LESS_THAN_OR_EQUAL\x10\x02\x12\x10\n\x0cGREATER_THAN\x10\x03\x12\x19\n\x15GREATER_THAN_OR_EQUAL\x10\x04\x12\t\n\x05\x45QUAL\x10\x05\x12\x06\n\x02IN\x10\x06\x12\n\n\x06\x45XISTS\x10\x07\x12\x17\n\x13\x43ONTAINED_IN_REGION\x10\x08\x12\r\n\tNOT_EQUAL\x10\t\x1a\x99\x01\n\x05Order\x12\x10\n\x08property\x18\n \x02(\t\x12R\n\tdirection\x18\x0b \x01(\x0e\x32\x34.apphosting_datastore_v3_bytes.Query.Order.Direction:\tASCENDING\"*\n\tDirection\x12\r\n\tASCENDING\x10\x01\x12\x0e\n\nDESCENDING\x10\x02\"=\n\x04Hint\x12\x0f\n\x0bORDER_FIRST\x10\x01\x12\x12\n\x0e\x41NCESTOR_FIRST\x10\x02\x12\x10\n\x0c\x46ILTER_FIRST\x10\x03\"2\n\x0bRegionPoint\x12\x10\n\x08latitude\x18\x01 \x02(\x01\x12\x11\n\tlongitude\x18\x02 \x02(\x01\"a\n\x0c\x43ircleRegion\x12:\n\x06\x63\x65nter\x18\x01 \x02(\x0b\x32*.apphosting_datastore_v3_bytes.RegionPoint\x12\x15\n\rradius_meters\x18\x02 \x02(\x01\"\x8f\x01\n\x0fRectangleRegion\x12=\n\tsouthwest\x18\x01 \x02(\x0b\x32*.apphosting_datastore_v3_bytes.RegionPoint\x12=\n\tnortheast\x18\x02 \x02(\x0b\x32*.apphosting_datastore_v3_bytes.RegionPoint\"\x8b\x01\n\tGeoRegion\x12;\n\x06\x63ircle\x18\x01 \x01(\x0b\x32+.apphosting_datastore_v3_bytes.CircleRegion\x12\x41\n\trectangle\x18\x02 \x01(\x0b\x32..apphosting_datastore_v3_bytes.RectangleRegion\"\xec\x06\n\rCompiledQuery\x12M\n\x0bprimaryscan\x18\x01 \x02(\n28.apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan\x12Q\n\rmergejoinscan\x18\x07 \x03(\n2:.apphosting_datastore_v3_bytes.CompiledQuery.MergeJoinScan\x12\x33\n\tindex_def\x18\x15 \x01(\x0b\x32 .storage_onestore_v3_bytes.Index\x12\x11\n\x06offset\x18\n \x01(\x05:\x01\x30\x12\r\n\x05limit\x18\x0b \x01(\x05\x12\x11\n\tkeys_only\x18\x0c \x02(\x08\x12\x15\n\rproperty_name\x18\x18 \x03(\t\x12\x1b\n\x13\x64istinct_infix_size\x18\x19 \x01(\x05\x12\x17\n\x0fkey_path_length\x18\x1b \x01(\x05\x12O\n\x0c\x65ntityfilter\x18\r \x01(\n29.apphosting_datastore_v3_bytes.CompiledQuery.EntityFilter\x12\x12\n\nplan_label\x18\x1a \x01(\t\x1a\xd5\x01\n\x0bPrimaryScan\x12\x12\n\nindex_name\x18\x02 \x01(\t\x12\x11\n\tstart_key\x18\x03 \x01(\x0c\x12\x17\n\x0fstart_inclusive\x18\x04 \x01(\x08\x12\x0f\n\x07\x65nd_key\x18\x05 \x01(\x0c\x12\x15\n\rend_inclusive\x18\x06 \x01(\x08\x12\x1b\n\x13start_postfix_value\x18\x16 \x03(\x0c\x12\x19\n\x11\x65nd_postfix_value\x18\x17 \x03(\x0c\x12&\n\x1e\x65nd_unapplied_log_timestamp_us\x18\x13 \x01(\x03\x1aV\n\rMergeJoinScan\x12\x12\n\nindex_name\x18\x08 \x02(\t\x12\x14\n\x0cprefix_value\x18\t \x03(\x0c\x12\x1b\n\x0cvalue_prefix\x18\x14 \x01(\x08:\x05\x66\x61lse\x1am\n\x0c\x45ntityFilter\x12\x17\n\x08\x64istinct\x18\x0e \x01(\x08:\x05\x66\x61lse\x12\x0c\n\x04kind\x18\x11 \x01(\t\x12\x36\n\x08\x61ncestor\x18\x12 \x01(\x0b\x32$.storage_onestore_v3_bytes.Reference\"\xbe\x04\n\x0e\x43ompiledCursor\x12L\n\x08position\x18\x02 \x01(\n26.apphosting_datastore_v3_bytes.CompiledCursor.PositionB\x02\x18\x01\x12\x41\n\x10postfix_position\x18\x01 \x01(\x0b\x32\'.storage_onestore_v3_bytes.IndexPostfix\x12\x43\n\x11\x61\x62solute_position\x18\x03 \x01(\x0b\x32(.storage_onestore_v3_bytes.IndexPosition\x1a\xd5\x02\n\x08Position\x12\x15\n\tstart_key\x18\x1b \x01(\x0c\x42\x02\x18\x01\x12Y\n\nindexvalue\x18\x1d \x03(\n2A.apphosting_datastore_v3_bytes.CompiledCursor.Position.IndexValueB\x02\x18\x01\x12\x35\n\x03key\x18  \x01(\x0b\x32$.storage_onestore_v3_bytes.ReferenceB\x02\x18\x01\x12!\n\x0fstart_inclusive\x18\x1c \x01(\x08:\x04trueB\x02\x18\x01\x12\x1c\n\x10\x62\x65\x66ore_ascending\x18! \x01(\x08\x42\x02\x18\x01\x1a_\n\nIndexValue\x12\x14\n\x08property\x18\x1e \x01(\tB\x02\x18\x01\x12;\n\x05value\x18\x1f \x02(\x0b\x32(.storage_onestore_v3_bytes.PropertyValueB\x02\x18\x01\":\n\x06\x43ursor\x12\x0e\n\x06\x63ursor\x18\x01 \x02(\x06\x12\x0b\n\x03\x61pp\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x61tabase_id\x18\x03 \x01(\t\"\x9f\x03\n\x05\x45rror\"\x95\x03\n\tErrorCode\x12\x0f\n\x0b\x42\x41\x44_REQUEST\x10\x01\x12\x1a\n\x16\x43ONCURRENT_TRANSACTION\x10\x02\x12\x12\n\x0eINTERNAL_ERROR\x10\x03\x12\x0e\n\nNEED_INDEX\x10\x04\x12\x0b\n\x07TIMEOUT\x10\x05\x12\x15\n\x11PERMISSION_DENIED\x10\x06\x12\x12\n\x0e\x42IGTABLE_ERROR\x10\x07\x12 \n\x1c\x43OMMITTED_BUT_STILL_APPLYING\x10\x08\x12\x17\n\x13\x43\x41PABILITY_DISABLED\x10\t\x12\x19\n\x15TRY_ALTERNATE_BACKEND\x10\n\x12\x15\n\x11SAFE_TIME_TOO_OLD\x10\x0b\x12\x16\n\x12RESOURCE_EXHAUSTED\x10\x0c\x12\x1c\n\x18SNAPSHOT_VERSION_TOO_OLD\x10\x12\x12\r\n\tNOT_FOUND\x10\r\x12\x12\n\x0e\x41LREADY_EXISTS\x10\x0e\x12\x17\n\x13\x46\x41ILED_PRECONDITION\x10\x0f\x12\x13\n\x0fUNAUTHENTICATED\x10\x10\x12\x0b\n\x07\x41\x42ORTED\x10\x11\"\xbd\x02\n\x04\x43ost\x12\x14\n\x0cindex_writes\x18\x01 \x01(\x05\x12\x19\n\x11index_write_bytes\x18\x02 \x01(\x05\x12\x15\n\rentity_writes\x18\x03 \x01(\x05\x12\x1a\n\x12\x65ntity_write_bytes\x18\x04 \x01(\x05\x12\x42\n\ncommitcost\x18\x05 \x01(\n2..apphosting_datastore_v3_bytes.Cost.CommitCost\x12!\n\x19\x61pproximate_storage_delta\x18\x08 \x01(\x05\x12\x1b\n\x13id_sequence_updates\x18\t \x01(\x05\x1aM\n\nCommitCost\x12\x1d\n\x15requested_entity_puts\x18\x06 \x01(\x05\x12 \n\x18requested_entity_deletes\x18\x07 \x01(\x05\"\xc4\x01\n\nGetRequest\x12\x31\n\x03key\x18\x01 \x03(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12?\n\x0btransaction\x18\x02 \x01(\x0b\x32*.apphosting_datastore_v3_bytes.Transaction\x12\x13\n\x0b\x66\x61ilover_ms\x18\x03 \x01(\x03\x12\x0e\n\x06strong\x18\x04 \x01(\x08\x12\x1d\n\x0e\x61llow_deferred\x18\x05 \x01(\x08:\x05\x66\x61lse\"\xa7\x02\n\x0bGetResponse\x12\x41\n\x06\x65ntity\x18\x01 \x03(\n21.apphosting_datastore_v3_bytes.GetResponse.Entity\x12\x36\n\x08\x64\x65\x66\x65rred\x18\x05 \x03(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x16\n\x08in_order\x18\x06 \x01(\x08:\x04true\x1a\x84\x01\n\x06\x45ntity\x12\x36\n\x06\x65ntity\x18\x02 \x01(\x0b\x32&.storage_onestore_v3_bytes.EntityProto\x12\x31\n\x03key\x18\x04 \x01(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x0f\n\x07version\x18\x03 \x01(\x03\"\xe4\x03\n\nPutRequest\x12\x36\n\x06\x65ntity\x18\x01 \x03(\x0b\x32&.storage_onestore_v3_bytes.EntityProto\x12?\n\x0btransaction\x18\x02 \x01(\x0b\x32*.apphosting_datastore_v3_bytes.Transaction\x12\x42\n\x0f\x63omposite_index\x18\x03 \x03(\x0b\x32).storage_onestore_v3_bytes.CompositeIndex\x12\x16\n\x07trusted\x18\x04 \x01(\x08:\x05\x66\x61lse\x12\x14\n\x05\x66orce\x18\x07 \x01(\x08:\x05\x66\x61lse\x12\x1b\n\x0cmark_changes\x18\x08 \x01(\x08:\x05\x66\x61lse\x12/\n\x08snapshot\x18\t \x03(\x0b\x32\x1d.storage_onestore_v3.Snapshot\x12W\n\x0e\x61uto_id_policy\x18\n \x01(\x0e\x32\x36.apphosting_datastore_v3_bytes.PutRequest.AutoIdPolicy:\x07\x43URRENT\x12\x17\n\x0fsequence_number\x18\x0c \x01(\x03\"+\n\x0c\x41utoIdPolicy\x12\x0b\n\x07\x43URRENT\x10\x00\x12\x0e\n\nSEQUENTIAL\x10\x01\"\x84\x01\n\x0bPutResponse\x12\x31\n\x03key\x18\x01 \x03(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x31\n\x04\x63ost\x18\x02 \x01(\x0b\x32#.apphosting_datastore_v3_bytes.Cost\x12\x0f\n\x07version\x18\x03 \x03(\x03\"\xcc\x01\n\x0cTouchRequest\x12\x31\n\x03key\x18\x01 \x03(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x42\n\x0f\x63omposite_index\x18\x02 \x03(\x0b\x32).storage_onestore_v3_bytes.CompositeIndex\x12\x14\n\x05\x66orce\x18\x03 \x01(\x08:\x05\x66\x61lse\x12/\n\x08snapshot\x18\t \x03(\x0b\x32\x1d.storage_onestore_v3.Snapshot\"B\n\rTouchResponse\x12\x31\n\x04\x63ost\x18\x01 \x01(\x0b\x32#.apphosting_datastore_v3_bytes.Cost\"\xdc\x02\n\rDeleteRequest\x12\x31\n\x03key\x18\x06 \x03(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12?\n\x0btransaction\x18\x05 \x01(\x0b\x32*.apphosting_datastore_v3_bytes.Transaction\x12\x42\n\x0f\x63omposite_index\x18\x0b \x03(\x0b\x32).storage_onestore_v3_bytes.CompositeIndex\x12\x16\n\x07trusted\x18\x04 \x01(\x08:\x05\x66\x61lse\x12\x14\n\x05\x66orce\x18\x07 \x01(\x08:\x05\x66\x61lse\x12\x1b\n\x0cmark_changes\x18\x08 \x01(\x08:\x05\x66\x61lse\x12/\n\x08snapshot\x18\t \x03(\x0b\x32\x1d.storage_onestore_v3.Snapshot\x12\x17\n\x0fsequence_number\x18\x0c \x01(\x03\"T\n\x0e\x44\x65leteResponse\x12\x31\n\x04\x63ost\x18\x01 \x01(\x0b\x32#.apphosting_datastore_v3_bytes.Cost\x12\x0f\n\x07version\x18\x03 \x03(\x03\"\x82\x01\n\x0bNextRequest\x12\x35\n\x06\x63ursor\x18\x01 \x02(\x0b\x32%.apphosting_datastore_v3_bytes.Cursor\x12\r\n\x05\x63ount\x18\x02 \x01(\x05\x12\x15\n\x06offset\x18\x04 \x01(\x05:\x01\x30\x42\x02\x18\x01\x12\x16\n\x07\x63ompile\x18\x03 \x01(\x08:\x05\x66\x61lse\"\xe5\x04\n\x0bQueryResult\x12\x35\n\x06\x63ursor\x18\x01 \x01(\x0b\x32%.apphosting_datastore_v3_bytes.Cursor\x12\x36\n\x06result\x18\x02 \x03(\x0b\x32&.storage_onestore_v3_bytes.EntityProto\x12\x17\n\x0fskipped_results\x18\x07 \x01(\x05\x12\x14\n\x0cmore_results\x18\x03 \x02(\x08\x12\x11\n\tkeys_only\x18\x04 \x01(\x08\x12\x12\n\nindex_only\x18\t \x01(\x08\x12\x11\n\tsmall_ops\x18\n \x01(\x08\x12\x44\n\x0e\x63ompiled_query\x18\x05 \x01(\x0b\x32,.apphosting_datastore_v3_bytes.CompiledQuery\x12\x46\n\x0f\x63ompiled_cursor\x18\x06 \x01(\x0b\x32-.apphosting_datastore_v3_bytes.CompiledCursor\x12\x38\n\x05index\x18\x08 \x03(\x0b\x32).storage_onestore_v3_bytes.CompositeIndex\x12\x0f\n\x07version\x18\x0b \x03(\x03\x12M\n\x16result_compiled_cursor\x18\x0c \x03(\x0b\x32-.apphosting_datastore_v3_bytes.CompiledCursor\x12V\n\x1fskipped_results_compiled_cursor\x18\r \x01(\x0b\x32-.apphosting_datastore_v3_bytes.CompiledCursor\"\xb7\x01\n\x12\x41llocateIdsRequest\x12\x37\n\tmodel_key\x18\x01 \x01(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x0c\n\x04size\x18\x02 \x01(\x03\x12\x0b\n\x03max\x18\x03 \x01(\x03\x12\x35\n\x07reserve\x18\x05 \x03(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x16\n\x07trusted\x18\x06 \x01(\x08:\x05\x66\x61lse\"d\n\x13\x41llocateIdsResponse\x12\r\n\x05start\x18\x01 \x02(\x03\x12\x0b\n\x03\x65nd\x18\x02 \x02(\x03\x12\x31\n\x04\x63ost\x18\x03 \x01(\x0b\x32#.apphosting_datastore_v3_bytes.Cost\"L\n\x10\x43ompositeIndices\x12\x38\n\x05index\x18\x01 \x03(\x0b\x32).storage_onestore_v3_bytes.CompositeIndex\"\x81\x01\n\x11\x41\x64\x64\x41\x63tionsRequest\x12?\n\x0btransaction\x18\x01 \x02(\x0b\x32*.apphosting_datastore_v3_bytes.Transaction\x12+\n\x06\x61\x63tion\x18\x02 \x03(\x0b\x32\x1b.storage_onestore_v3.Action\"\x14\n\x12\x41\x64\x64\x41\x63tionsResponse\"\xc5\x02\n\x17\x42\x65ginTransactionRequest\x12\x0b\n\x03\x61pp\x18\x01 \x02(\t\x12 \n\x11\x61llow_multiple_eg\x18\x02 \x01(\x08:\x05\x66\x61lse\x12\x13\n\x0b\x64\x61tabase_id\x18\x04 \x01(\t\x12]\n\x04mode\x18\x05 \x01(\x0e\x32\x46.apphosting_datastore_v3_bytes.BeginTransactionRequest.TransactionMode:\x07UNKNOWN\x12H\n\x14previous_transaction\x18\x07 \x01(\x0b\x32*.apphosting_datastore_v3_bytes.Transaction\"=\n\x0fTransactionMode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\r\n\tREAD_ONLY\x10\x01\x12\x0e\n\nREAD_WRITE\x10\x02\"\xe6\x01\n\x0e\x43ommitResponse\x12\x31\n\x04\x63ost\x18\x01 \x01(\x0b\x32#.apphosting_datastore_v3_bytes.Cost\x12\x46\n\x07version\x18\x03 \x03(\n25.apphosting_datastore_v3_bytes.CommitResponse.Version\x1aY\n\x07Version\x12=\n\x0froot_entity_key\x18\x04 \x02(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x0f\n\x07version\x18\x05 \x02(\x03\"8\n\x11GetIndicesRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x02(\t\x12\x13\n\x0b\x64\x61tabase_id\x18\x02 \x01(\t\"6\n\x13UpdateIndexResponse\x12\x10\n\x08type_url\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\"\x86\x02\n\x12\x44\x61tastoreService_3\"\xef\x01\n\x06Method\x12\x07\n\x03Get\x10\x01\x12\x07\n\x03Put\x10\x02\x12\t\n\x05Touch\x10\x03\x12\n\n\x06\x44\x65lete\x10\x04\x12\x0c\n\x08RunQuery\x10\x05\x12\x0e\n\nAddActions\x10\x06\x12\x08\n\x04Next\x10\x07\x12\x10\n\x0c\x44\x65leteCursor\x10\x08\x12\x14\n\x10\x42\x65ginTransaction\x10\t\x12\n\n\x06\x43ommit\x10\n\x12\x0c\n\x08Rollback\x10\x0b\x12\x0f\n\x0b\x41llocateIds\x10\x0c\x12\x0f\n\x0b\x43reateIndex\x10\r\x12\x0f\n\x0bUpdateIndex\x10\x0e\x12\x0e\n\nGetIndices\x10\x0f\x12\x0f\n\x0b\x44\x65leteIndex\x10\x10\x42\x36\n%com.google.google.appengine.datastoreB\rDatastoreV3Pb'
  ,
  dependencies=[google_dot_appengine_dot_datastore_dot_action__pb2.DESCRIPTOR,google_dot_appengine_dot_datastore_dot_entity__bytes__pb2.DESCRIPTOR,google_dot_appengine_dot_datastore_dot_snapshot__pb2.DESCRIPTOR,])



_QUERY_FILTER_OPERATOR = _descriptor.EnumDescriptor(
  name='Operator',
  full_name='apphosting_datastore_v3_bytes.Query.Filter.Operator',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LESS_THAN', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LESS_THAN_OR_EQUAL', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GREATER_THAN', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GREATER_THAN_OR_EQUAL', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EQUAL', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='IN', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXISTS', index=6, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONTAINED_IN_REGION', index=7, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_EQUAL', index=8, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1566,
  serialized_end=1731,
)
_sym_db.RegisterEnumDescriptor(_QUERY_FILTER_OPERATOR)

_QUERY_ORDER_DIRECTION = _descriptor.EnumDescriptor(
  name='Direction',
  full_name='apphosting_datastore_v3_bytes.Query.Order.Direction',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ASCENDING', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DESCENDING', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1845,
  serialized_end=1887,
)
_sym_db.RegisterEnumDescriptor(_QUERY_ORDER_DIRECTION)

_QUERY_HINT = _descriptor.EnumDescriptor(
  name='Hint',
  full_name='apphosting_datastore_v3_bytes.Query.Hint',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ORDER_FIRST', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ANCESTOR_FIRST', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FILTER_FIRST', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1889,
  serialized_end=1950,
)
_sym_db.RegisterEnumDescriptor(_QUERY_HINT)

_ERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='apphosting_datastore_v3_bytes.Error.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BAD_REQUEST', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONCURRENT_TRANSACTION', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INTERNAL_ERROR', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NEED_INDEX', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TIMEOUT', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PERMISSION_DENIED', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BIGTABLE_ERROR', index=6, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COMMITTED_BUT_STILL_APPLYING', index=7, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CAPABILITY_DISABLED', index=8, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRY_ALTERNATE_BACKEND', index=9, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SAFE_TIME_TOO_OLD', index=10, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESOURCE_EXHAUSTED', index=11, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SNAPSHOT_VERSION_TOO_OLD', index=12, number=18,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_FOUND', index=13, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ALREADY_EXISTS', index=14, number=14,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FAILED_PRECONDITION', index=15, number=15,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNAUTHENTICATED', index=16, number=16,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ABORTED', index=17, number=17,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=3918,
  serialized_end=4323,
)
_sym_db.RegisterEnumDescriptor(_ERROR_ERRORCODE)

_PUTREQUEST_AUTOIDPOLICY = _descriptor.EnumDescriptor(
  name='AutoIdPolicy',
  full_name='apphosting_datastore_v3_bytes.PutRequest.AutoIdPolicy',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CURRENT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SEQUENTIAL', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=5584,
  serialized_end=5627,
)
_sym_db.RegisterEnumDescriptor(_PUTREQUEST_AUTOIDPOLICY)

_BEGINTRANSACTIONREQUEST_TRANSACTIONMODE = _descriptor.EnumDescriptor(
  name='TransactionMode',
  full_name='apphosting_datastore_v3_bytes.BeginTransactionRequest.TransactionMode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='READ_ONLY', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='READ_WRITE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=8010,
  serialized_end=8071,
)
_sym_db.RegisterEnumDescriptor(_BEGINTRANSACTIONREQUEST_TRANSACTIONMODE)

_DATASTORESERVICE_3_METHOD = _descriptor.EnumDescriptor(
  name='Method',
  full_name='apphosting_datastore_v3_bytes.DatastoreService_3.Method',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Get', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Put', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Touch', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Delete', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RunQuery', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AddActions', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Next', index=6, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DeleteCursor', index=7, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BeginTransaction', index=8, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Commit', index=9, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Rollback', index=10, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AllocateIds', index=11, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CreateIndex', index=12, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UpdateIndex', index=13, number=14,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GetIndices', index=14, number=15,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DeleteIndex', index=15, number=16,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=8444,
  serialized_end=8683,
)
_sym_db.RegisterEnumDescriptor(_DATASTORESERVICE_3_METHOD)


_TRANSACTION = _descriptor.Descriptor(
  name='Transaction',
  full_name='apphosting_datastore_v3_bytes.Transaction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='handle', full_name='apphosting_datastore_v3_bytes.Transaction.handle', index=0,
      number=1, type=6, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='app', full_name='apphosting_datastore_v3_bytes.Transaction.app', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='database_id', full_name='apphosting_datastore_v3_bytes.Transaction.database_id', index=2,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mark_changes', full_name='apphosting_datastore_v3_bytes.Transaction.mark_changes', index=3,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='composite_index', full_name='apphosting_datastore_v3_bytes.Transaction.composite_index', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=218,
  serialized_end=378,
)


_QUERY_FILTER = _descriptor.Descriptor(
  name='Filter',
  full_name='apphosting_datastore_v3_bytes.Query.Filter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='op', full_name='apphosting_datastore_v3_bytes.Query.Filter.op', index=0,
      number=6, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='property', full_name='apphosting_datastore_v3_bytes.Query.Filter.property', index=1,
      number=14, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='geo_region', full_name='apphosting_datastore_v3_bytes.Query.Filter.geo_region', index=2,
      number=40, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _QUERY_FILTER_OPERATOR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1372,
  serialized_end=1731,
)

_QUERY_ORDER = _descriptor.Descriptor(
  name='Order',
  full_name='apphosting_datastore_v3_bytes.Query.Order',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='property', full_name='apphosting_datastore_v3_bytes.Query.Order.property', index=0,
      number=10, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='direction', full_name='apphosting_datastore_v3_bytes.Query.Order.direction', index=1,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _QUERY_ORDER_DIRECTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1734,
  serialized_end=1887,
)

_QUERY = _descriptor.Descriptor(
  name='Query',
  full_name='apphosting_datastore_v3_bytes.Query',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app', full_name='apphosting_datastore_v3_bytes.Query.app', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='database_id', full_name='apphosting_datastore_v3_bytes.Query.database_id', index=1,
      number=42, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name_space', full_name='apphosting_datastore_v3_bytes.Query.name_space', index=2,
      number=29, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kind', full_name='apphosting_datastore_v3_bytes.Query.kind', index=3,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ancestor', full_name='apphosting_datastore_v3_bytes.Query.ancestor', index=4,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shallow', full_name='apphosting_datastore_v3_bytes.Query.shallow', index=5,
      number=43, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filter', full_name='apphosting_datastore_v3_bytes.Query.filter', index=6,
      number=4, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='search_query', full_name='apphosting_datastore_v3_bytes.Query.search_query', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='order', full_name='apphosting_datastore_v3_bytes.Query.order', index=8,
      number=9, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hint', full_name='apphosting_datastore_v3_bytes.Query.hint', index=9,
      number=18, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='count', full_name='apphosting_datastore_v3_bytes.Query.count', index=10,
      number=23, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='offset', full_name='apphosting_datastore_v3_bytes.Query.offset', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='limit', full_name='apphosting_datastore_v3_bytes.Query.limit', index=12,
      number=16, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compiled_cursor', full_name='apphosting_datastore_v3_bytes.Query.compiled_cursor', index=13,
      number=30, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_compiled_cursor', full_name='apphosting_datastore_v3_bytes.Query.end_compiled_cursor', index=14,
      number=31, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='composite_index', full_name='apphosting_datastore_v3_bytes.Query.composite_index', index=15,
      number=19, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='require_perfect_plan', full_name='apphosting_datastore_v3_bytes.Query.require_perfect_plan', index=16,
      number=20, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keys_only', full_name='apphosting_datastore_v3_bytes.Query.keys_only', index=17,
      number=21, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transaction', full_name='apphosting_datastore_v3_bytes.Query.transaction', index=18,
      number=22, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compile', full_name='apphosting_datastore_v3_bytes.Query.compile', index=19,
      number=25, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='failover_ms', full_name='apphosting_datastore_v3_bytes.Query.failover_ms', index=20,
      number=26, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='strong', full_name='apphosting_datastore_v3_bytes.Query.strong', index=21,
      number=32, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='property_name', full_name='apphosting_datastore_v3_bytes.Query.property_name', index=22,
      number=33, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_by_property_name', full_name='apphosting_datastore_v3_bytes.Query.group_by_property_name', index=23,
      number=34, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='distinct', full_name='apphosting_datastore_v3_bytes.Query.distinct', index=24,
      number=24, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='min_safe_time_seconds', full_name='apphosting_datastore_v3_bytes.Query.min_safe_time_seconds', index=25,
      number=35, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='safe_replica_name', full_name='apphosting_datastore_v3_bytes.Query.safe_replica_name', index=26,
      number=36, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='persist_offset', full_name='apphosting_datastore_v3_bytes.Query.persist_offset', index=27,
      number=37, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='read_time_us', full_name='apphosting_datastore_v3_bytes.Query.read_time_us', index=28,
      number=44, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_QUERY_FILTER, _QUERY_ORDER, ],
  enum_types=[
    _QUERY_HINT,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=381,
  serialized_end=1950,
)


_REGIONPOINT = _descriptor.Descriptor(
  name='RegionPoint',
  full_name='apphosting_datastore_v3_bytes.RegionPoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='latitude', full_name='apphosting_datastore_v3_bytes.RegionPoint.latitude', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='apphosting_datastore_v3_bytes.RegionPoint.longitude', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
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
  serialized_start=1952,
  serialized_end=2002,
)


_CIRCLEREGION = _descriptor.Descriptor(
  name='CircleRegion',
  full_name='apphosting_datastore_v3_bytes.CircleRegion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='center', full_name='apphosting_datastore_v3_bytes.CircleRegion.center', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radius_meters', full_name='apphosting_datastore_v3_bytes.CircleRegion.radius_meters', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
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
  serialized_start=2004,
  serialized_end=2101,
)


_RECTANGLEREGION = _descriptor.Descriptor(
  name='RectangleRegion',
  full_name='apphosting_datastore_v3_bytes.RectangleRegion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='southwest', full_name='apphosting_datastore_v3_bytes.RectangleRegion.southwest', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='northeast', full_name='apphosting_datastore_v3_bytes.RectangleRegion.northeast', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
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
  serialized_start=2104,
  serialized_end=2247,
)


_GEOREGION = _descriptor.Descriptor(
  name='GeoRegion',
  full_name='apphosting_datastore_v3_bytes.GeoRegion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='circle', full_name='apphosting_datastore_v3_bytes.GeoRegion.circle', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rectangle', full_name='apphosting_datastore_v3_bytes.GeoRegion.rectangle', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=2250,
  serialized_end=2389,
)


_COMPILEDQUERY_PRIMARYSCAN = _descriptor.Descriptor(
  name='PrimaryScan',
  full_name='apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index_name', full_name='apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan.index_name', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_key', full_name='apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan.start_key', index=1,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_inclusive', full_name='apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan.start_inclusive', index=2,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_key', full_name='apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan.end_key', index=3,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_inclusive', full_name='apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan.end_inclusive', index=4,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_postfix_value', full_name='apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan.start_postfix_value', index=5,
      number=22, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_postfix_value', full_name='apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan.end_postfix_value', index=6,
      number=23, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_unapplied_log_timestamp_us', full_name='apphosting_datastore_v3_bytes.CompiledQuery.PrimaryScan.end_unapplied_log_timestamp_us', index=7,
      number=19, type=3, cpp_type=2, label=1,
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
  serialized_start=2856,
  serialized_end=3069,
)

_COMPILEDQUERY_MERGEJOINSCAN = _descriptor.Descriptor(
  name='MergeJoinScan',
  full_name='apphosting_datastore_v3_bytes.CompiledQuery.MergeJoinScan',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index_name', full_name='apphosting_datastore_v3_bytes.CompiledQuery.MergeJoinScan.index_name', index=0,
      number=8, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='prefix_value', full_name='apphosting_datastore_v3_bytes.CompiledQuery.MergeJoinScan.prefix_value', index=1,
      number=9, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value_prefix', full_name='apphosting_datastore_v3_bytes.CompiledQuery.MergeJoinScan.value_prefix', index=2,
      number=20, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
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
  serialized_start=3071,
  serialized_end=3157,
)

_COMPILEDQUERY_ENTITYFILTER = _descriptor.Descriptor(
  name='EntityFilter',
  full_name='apphosting_datastore_v3_bytes.CompiledQuery.EntityFilter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='distinct', full_name='apphosting_datastore_v3_bytes.CompiledQuery.EntityFilter.distinct', index=0,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kind', full_name='apphosting_datastore_v3_bytes.CompiledQuery.EntityFilter.kind', index=1,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ancestor', full_name='apphosting_datastore_v3_bytes.CompiledQuery.EntityFilter.ancestor', index=2,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=3159,
  serialized_end=3268,
)

_COMPILEDQUERY = _descriptor.Descriptor(
  name='CompiledQuery',
  full_name='apphosting_datastore_v3_bytes.CompiledQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='primaryscan', full_name='apphosting_datastore_v3_bytes.CompiledQuery.primaryscan', index=0,
      number=1, type=10, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mergejoinscan', full_name='apphosting_datastore_v3_bytes.CompiledQuery.mergejoinscan', index=1,
      number=7, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='index_def', full_name='apphosting_datastore_v3_bytes.CompiledQuery.index_def', index=2,
      number=21, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='offset', full_name='apphosting_datastore_v3_bytes.CompiledQuery.offset', index=3,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='limit', full_name='apphosting_datastore_v3_bytes.CompiledQuery.limit', index=4,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keys_only', full_name='apphosting_datastore_v3_bytes.CompiledQuery.keys_only', index=5,
      number=12, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='property_name', full_name='apphosting_datastore_v3_bytes.CompiledQuery.property_name', index=6,
      number=24, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='distinct_infix_size', full_name='apphosting_datastore_v3_bytes.CompiledQuery.distinct_infix_size', index=7,
      number=25, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key_path_length', full_name='apphosting_datastore_v3_bytes.CompiledQuery.key_path_length', index=8,
      number=27, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entityfilter', full_name='apphosting_datastore_v3_bytes.CompiledQuery.entityfilter', index=9,
      number=13, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='plan_label', full_name='apphosting_datastore_v3_bytes.CompiledQuery.plan_label', index=10,
      number=26, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_COMPILEDQUERY_PRIMARYSCAN, _COMPILEDQUERY_MERGEJOINSCAN, _COMPILEDQUERY_ENTITYFILTER, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2392,
  serialized_end=3268,
)


_COMPILEDCURSOR_POSITION_INDEXVALUE = _descriptor.Descriptor(
  name='IndexValue',
  full_name='apphosting_datastore_v3_bytes.CompiledCursor.Position.IndexValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='property', full_name='apphosting_datastore_v3_bytes.CompiledCursor.Position.IndexValue.property', index=0,
      number=30, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='apphosting_datastore_v3_bytes.CompiledCursor.Position.IndexValue.value', index=1,
      number=31, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
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
  serialized_start=3750,
  serialized_end=3845,
)

_COMPILEDCURSOR_POSITION = _descriptor.Descriptor(
  name='Position',
  full_name='apphosting_datastore_v3_bytes.CompiledCursor.Position',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='start_key', full_name='apphosting_datastore_v3_bytes.CompiledCursor.Position.start_key', index=0,
      number=27, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='indexvalue', full_name='apphosting_datastore_v3_bytes.CompiledCursor.Position.indexvalue', index=1,
      number=29, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key', full_name='apphosting_datastore_v3_bytes.CompiledCursor.Position.key', index=2,
      number=32, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_inclusive', full_name='apphosting_datastore_v3_bytes.CompiledCursor.Position.start_inclusive', index=3,
      number=28, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='before_ascending', full_name='apphosting_datastore_v3_bytes.CompiledCursor.Position.before_ascending', index=4,
      number=33, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_COMPILEDCURSOR_POSITION_INDEXVALUE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3504,
  serialized_end=3845,
)

_COMPILEDCURSOR = _descriptor.Descriptor(
  name='CompiledCursor',
  full_name='apphosting_datastore_v3_bytes.CompiledCursor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='apphosting_datastore_v3_bytes.CompiledCursor.position', index=0,
      number=2, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='postfix_position', full_name='apphosting_datastore_v3_bytes.CompiledCursor.postfix_position', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='absolute_position', full_name='apphosting_datastore_v3_bytes.CompiledCursor.absolute_position', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_COMPILEDCURSOR_POSITION, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3271,
  serialized_end=3845,
)


_CURSOR = _descriptor.Descriptor(
  name='Cursor',
  full_name='apphosting_datastore_v3_bytes.Cursor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cursor', full_name='apphosting_datastore_v3_bytes.Cursor.cursor', index=0,
      number=1, type=6, cpp_type=4, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='app', full_name='apphosting_datastore_v3_bytes.Cursor.app', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='database_id', full_name='apphosting_datastore_v3_bytes.Cursor.database_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=3847,
  serialized_end=3905,
)


_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='apphosting_datastore_v3_bytes.Error',
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
    _ERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3908,
  serialized_end=4323,
)


_COST_COMMITCOST = _descriptor.Descriptor(
  name='CommitCost',
  full_name='apphosting_datastore_v3_bytes.Cost.CommitCost',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='requested_entity_puts', full_name='apphosting_datastore_v3_bytes.Cost.CommitCost.requested_entity_puts', index=0,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='requested_entity_deletes', full_name='apphosting_datastore_v3_bytes.Cost.CommitCost.requested_entity_deletes', index=1,
      number=7, type=5, cpp_type=1, label=1,
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
  serialized_start=4566,
  serialized_end=4643,
)

_COST = _descriptor.Descriptor(
  name='Cost',
  full_name='apphosting_datastore_v3_bytes.Cost',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index_writes', full_name='apphosting_datastore_v3_bytes.Cost.index_writes', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='index_write_bytes', full_name='apphosting_datastore_v3_bytes.Cost.index_write_bytes', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_writes', full_name='apphosting_datastore_v3_bytes.Cost.entity_writes', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_write_bytes', full_name='apphosting_datastore_v3_bytes.Cost.entity_write_bytes', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='commitcost', full_name='apphosting_datastore_v3_bytes.Cost.commitcost', index=4,
      number=5, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='approximate_storage_delta', full_name='apphosting_datastore_v3_bytes.Cost.approximate_storage_delta', index=5,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id_sequence_updates', full_name='apphosting_datastore_v3_bytes.Cost.id_sequence_updates', index=6,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_COST_COMMITCOST, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4326,
  serialized_end=4643,
)


_GETREQUEST = _descriptor.Descriptor(
  name='GetRequest',
  full_name='apphosting_datastore_v3_bytes.GetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='apphosting_datastore_v3_bytes.GetRequest.key', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transaction', full_name='apphosting_datastore_v3_bytes.GetRequest.transaction', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='failover_ms', full_name='apphosting_datastore_v3_bytes.GetRequest.failover_ms', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='strong', full_name='apphosting_datastore_v3_bytes.GetRequest.strong', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='allow_deferred', full_name='apphosting_datastore_v3_bytes.GetRequest.allow_deferred', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
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
  serialized_start=4646,
  serialized_end=4842,
)


_GETRESPONSE_ENTITY = _descriptor.Descriptor(
  name='Entity',
  full_name='apphosting_datastore_v3_bytes.GetResponse.Entity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity', full_name='apphosting_datastore_v3_bytes.GetResponse.Entity.entity', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key', full_name='apphosting_datastore_v3_bytes.GetResponse.Entity.key', index=1,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='apphosting_datastore_v3_bytes.GetResponse.Entity.version', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  serialized_start=5008,
  serialized_end=5140,
)

_GETRESPONSE = _descriptor.Descriptor(
  name='GetResponse',
  full_name='apphosting_datastore_v3_bytes.GetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity', full_name='apphosting_datastore_v3_bytes.GetResponse.entity', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deferred', full_name='apphosting_datastore_v3_bytes.GetResponse.deferred', index=1,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='in_order', full_name='apphosting_datastore_v3_bytes.GetResponse.in_order', index=2,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_GETRESPONSE_ENTITY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4845,
  serialized_end=5140,
)


_PUTREQUEST = _descriptor.Descriptor(
  name='PutRequest',
  full_name='apphosting_datastore_v3_bytes.PutRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity', full_name='apphosting_datastore_v3_bytes.PutRequest.entity', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transaction', full_name='apphosting_datastore_v3_bytes.PutRequest.transaction', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='composite_index', full_name='apphosting_datastore_v3_bytes.PutRequest.composite_index', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='trusted', full_name='apphosting_datastore_v3_bytes.PutRequest.trusted', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='force', full_name='apphosting_datastore_v3_bytes.PutRequest.force', index=4,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mark_changes', full_name='apphosting_datastore_v3_bytes.PutRequest.mark_changes', index=5,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='snapshot', full_name='apphosting_datastore_v3_bytes.PutRequest.snapshot', index=6,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auto_id_policy', full_name='apphosting_datastore_v3_bytes.PutRequest.auto_id_policy', index=7,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sequence_number', full_name='apphosting_datastore_v3_bytes.PutRequest.sequence_number', index=8,
      number=12, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PUTREQUEST_AUTOIDPOLICY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5143,
  serialized_end=5627,
)


_PUTRESPONSE = _descriptor.Descriptor(
  name='PutResponse',
  full_name='apphosting_datastore_v3_bytes.PutResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='apphosting_datastore_v3_bytes.PutResponse.key', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cost', full_name='apphosting_datastore_v3_bytes.PutResponse.cost', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='apphosting_datastore_v3_bytes.PutResponse.version', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=5630,
  serialized_end=5762,
)


_TOUCHREQUEST = _descriptor.Descriptor(
  name='TouchRequest',
  full_name='apphosting_datastore_v3_bytes.TouchRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='apphosting_datastore_v3_bytes.TouchRequest.key', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='composite_index', full_name='apphosting_datastore_v3_bytes.TouchRequest.composite_index', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='force', full_name='apphosting_datastore_v3_bytes.TouchRequest.force', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='snapshot', full_name='apphosting_datastore_v3_bytes.TouchRequest.snapshot', index=3,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=5765,
  serialized_end=5969,
)


_TOUCHRESPONSE = _descriptor.Descriptor(
  name='TouchResponse',
  full_name='apphosting_datastore_v3_bytes.TouchResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cost', full_name='apphosting_datastore_v3_bytes.TouchResponse.cost', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=5971,
  serialized_end=6037,
)


_DELETEREQUEST = _descriptor.Descriptor(
  name='DeleteRequest',
  full_name='apphosting_datastore_v3_bytes.DeleteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='apphosting_datastore_v3_bytes.DeleteRequest.key', index=0,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transaction', full_name='apphosting_datastore_v3_bytes.DeleteRequest.transaction', index=1,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='composite_index', full_name='apphosting_datastore_v3_bytes.DeleteRequest.composite_index', index=2,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='trusted', full_name='apphosting_datastore_v3_bytes.DeleteRequest.trusted', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='force', full_name='apphosting_datastore_v3_bytes.DeleteRequest.force', index=4,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mark_changes', full_name='apphosting_datastore_v3_bytes.DeleteRequest.mark_changes', index=5,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='snapshot', full_name='apphosting_datastore_v3_bytes.DeleteRequest.snapshot', index=6,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sequence_number', full_name='apphosting_datastore_v3_bytes.DeleteRequest.sequence_number', index=7,
      number=12, type=3, cpp_type=2, label=1,
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
  serialized_start=6040,
  serialized_end=6388,
)


_DELETERESPONSE = _descriptor.Descriptor(
  name='DeleteResponse',
  full_name='apphosting_datastore_v3_bytes.DeleteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cost', full_name='apphosting_datastore_v3_bytes.DeleteResponse.cost', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='apphosting_datastore_v3_bytes.DeleteResponse.version', index=1,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=6390,
  serialized_end=6474,
)


_NEXTREQUEST = _descriptor.Descriptor(
  name='NextRequest',
  full_name='apphosting_datastore_v3_bytes.NextRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cursor', full_name='apphosting_datastore_v3_bytes.NextRequest.cursor', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='count', full_name='apphosting_datastore_v3_bytes.NextRequest.count', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='offset', full_name='apphosting_datastore_v3_bytes.NextRequest.offset', index=2,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compile', full_name='apphosting_datastore_v3_bytes.NextRequest.compile', index=3,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
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
  serialized_start=6477,
  serialized_end=6607,
)


_QUERYRESULT = _descriptor.Descriptor(
  name='QueryResult',
  full_name='apphosting_datastore_v3_bytes.QueryResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cursor', full_name='apphosting_datastore_v3_bytes.QueryResult.cursor', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result', full_name='apphosting_datastore_v3_bytes.QueryResult.result', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='skipped_results', full_name='apphosting_datastore_v3_bytes.QueryResult.skipped_results', index=2,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='more_results', full_name='apphosting_datastore_v3_bytes.QueryResult.more_results', index=3,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keys_only', full_name='apphosting_datastore_v3_bytes.QueryResult.keys_only', index=4,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='index_only', full_name='apphosting_datastore_v3_bytes.QueryResult.index_only', index=5,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='small_ops', full_name='apphosting_datastore_v3_bytes.QueryResult.small_ops', index=6,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compiled_query', full_name='apphosting_datastore_v3_bytes.QueryResult.compiled_query', index=7,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compiled_cursor', full_name='apphosting_datastore_v3_bytes.QueryResult.compiled_cursor', index=8,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='index', full_name='apphosting_datastore_v3_bytes.QueryResult.index', index=9,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='apphosting_datastore_v3_bytes.QueryResult.version', index=10,
      number=11, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='result_compiled_cursor', full_name='apphosting_datastore_v3_bytes.QueryResult.result_compiled_cursor', index=11,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='skipped_results_compiled_cursor', full_name='apphosting_datastore_v3_bytes.QueryResult.skipped_results_compiled_cursor', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=6610,
  serialized_end=7223,
)


_ALLOCATEIDSREQUEST = _descriptor.Descriptor(
  name='AllocateIdsRequest',
  full_name='apphosting_datastore_v3_bytes.AllocateIdsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='model_key', full_name='apphosting_datastore_v3_bytes.AllocateIdsRequest.model_key', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size', full_name='apphosting_datastore_v3_bytes.AllocateIdsRequest.size', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max', full_name='apphosting_datastore_v3_bytes.AllocateIdsRequest.max', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reserve', full_name='apphosting_datastore_v3_bytes.AllocateIdsRequest.reserve', index=3,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='trusted', full_name='apphosting_datastore_v3_bytes.AllocateIdsRequest.trusted', index=4,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
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
  serialized_start=7226,
  serialized_end=7409,
)


_ALLOCATEIDSRESPONSE = _descriptor.Descriptor(
  name='AllocateIdsResponse',
  full_name='apphosting_datastore_v3_bytes.AllocateIdsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='apphosting_datastore_v3_bytes.AllocateIdsResponse.start', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end', full_name='apphosting_datastore_v3_bytes.AllocateIdsResponse.end', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cost', full_name='apphosting_datastore_v3_bytes.AllocateIdsResponse.cost', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=7411,
  serialized_end=7511,
)


_COMPOSITEINDICES = _descriptor.Descriptor(
  name='CompositeIndices',
  full_name='apphosting_datastore_v3_bytes.CompositeIndices',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='apphosting_datastore_v3_bytes.CompositeIndices.index', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=7513,
  serialized_end=7589,
)


_ADDACTIONSREQUEST = _descriptor.Descriptor(
  name='AddActionsRequest',
  full_name='apphosting_datastore_v3_bytes.AddActionsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction', full_name='apphosting_datastore_v3_bytes.AddActionsRequest.transaction', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='action', full_name='apphosting_datastore_v3_bytes.AddActionsRequest.action', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=7592,
  serialized_end=7721,
)


_ADDACTIONSRESPONSE = _descriptor.Descriptor(
  name='AddActionsResponse',
  full_name='apphosting_datastore_v3_bytes.AddActionsResponse',
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
  serialized_start=7723,
  serialized_end=7743,
)


_BEGINTRANSACTIONREQUEST = _descriptor.Descriptor(
  name='BeginTransactionRequest',
  full_name='apphosting_datastore_v3_bytes.BeginTransactionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app', full_name='apphosting_datastore_v3_bytes.BeginTransactionRequest.app', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='allow_multiple_eg', full_name='apphosting_datastore_v3_bytes.BeginTransactionRequest.allow_multiple_eg', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='database_id', full_name='apphosting_datastore_v3_bytes.BeginTransactionRequest.database_id', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode', full_name='apphosting_datastore_v3_bytes.BeginTransactionRequest.mode', index=3,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='previous_transaction', full_name='apphosting_datastore_v3_bytes.BeginTransactionRequest.previous_transaction', index=4,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BEGINTRANSACTIONREQUEST_TRANSACTIONMODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7746,
  serialized_end=8071,
)


_COMMITRESPONSE_VERSION = _descriptor.Descriptor(
  name='Version',
  full_name='apphosting_datastore_v3_bytes.CommitResponse.Version',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='root_entity_key', full_name='apphosting_datastore_v3_bytes.CommitResponse.Version.root_entity_key', index=0,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='apphosting_datastore_v3_bytes.CommitResponse.Version.version', index=1,
      number=5, type=3, cpp_type=2, label=2,
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
  serialized_start=8215,
  serialized_end=8304,
)

_COMMITRESPONSE = _descriptor.Descriptor(
  name='CommitResponse',
  full_name='apphosting_datastore_v3_bytes.CommitResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cost', full_name='apphosting_datastore_v3_bytes.CommitResponse.cost', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='apphosting_datastore_v3_bytes.CommitResponse.version', index=1,
      number=3, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_COMMITRESPONSE_VERSION, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=8074,
  serialized_end=8304,
)


_GETINDICESREQUEST = _descriptor.Descriptor(
  name='GetIndicesRequest',
  full_name='apphosting_datastore_v3_bytes.GetIndicesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_datastore_v3_bytes.GetIndicesRequest.app_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='database_id', full_name='apphosting_datastore_v3_bytes.GetIndicesRequest.database_id', index=1,
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
  serialized_start=8306,
  serialized_end=8362,
)


_UPDATEINDEXRESPONSE = _descriptor.Descriptor(
  name='UpdateIndexResponse',
  full_name='apphosting_datastore_v3_bytes.UpdateIndexResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type_url', full_name='apphosting_datastore_v3_bytes.UpdateIndexResponse.type_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='apphosting_datastore_v3_bytes.UpdateIndexResponse.value', index=1,
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
  serialized_start=8364,
  serialized_end=8418,
)


_DATASTORESERVICE_3 = _descriptor.Descriptor(
  name='DatastoreService_3',
  full_name='apphosting_datastore_v3_bytes.DatastoreService_3',
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
    _DATASTORESERVICE_3_METHOD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=8421,
  serialized_end=8683,
)

_TRANSACTION.fields_by_name['composite_index'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._COMPOSITEINDEX
_QUERY_FILTER.fields_by_name['op'].enum_type = _QUERY_FILTER_OPERATOR
_QUERY_FILTER.fields_by_name['property'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._PROPERTY
_QUERY_FILTER.fields_by_name['geo_region'].message_type = _GEOREGION
_QUERY_FILTER.containing_type = _QUERY
_QUERY_FILTER_OPERATOR.containing_type = _QUERY_FILTER
_QUERY_ORDER.fields_by_name['direction'].enum_type = _QUERY_ORDER_DIRECTION
_QUERY_ORDER.containing_type = _QUERY
_QUERY_ORDER_DIRECTION.containing_type = _QUERY_ORDER
_QUERY.fields_by_name['ancestor'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_QUERY.fields_by_name['filter'].message_type = _QUERY_FILTER
_QUERY.fields_by_name['order'].message_type = _QUERY_ORDER
_QUERY.fields_by_name['hint'].enum_type = _QUERY_HINT
_QUERY.fields_by_name['compiled_cursor'].message_type = _COMPILEDCURSOR
_QUERY.fields_by_name['end_compiled_cursor'].message_type = _COMPILEDCURSOR
_QUERY.fields_by_name['composite_index'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._COMPOSITEINDEX
_QUERY.fields_by_name['transaction'].message_type = _TRANSACTION
_QUERY_HINT.containing_type = _QUERY
_CIRCLEREGION.fields_by_name['center'].message_type = _REGIONPOINT
_RECTANGLEREGION.fields_by_name['southwest'].message_type = _REGIONPOINT
_RECTANGLEREGION.fields_by_name['northeast'].message_type = _REGIONPOINT
_GEOREGION.fields_by_name['circle'].message_type = _CIRCLEREGION
_GEOREGION.fields_by_name['rectangle'].message_type = _RECTANGLEREGION
_COMPILEDQUERY_PRIMARYSCAN.containing_type = _COMPILEDQUERY
_COMPILEDQUERY_MERGEJOINSCAN.containing_type = _COMPILEDQUERY
_COMPILEDQUERY_ENTITYFILTER.fields_by_name['ancestor'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_COMPILEDQUERY_ENTITYFILTER.containing_type = _COMPILEDQUERY
_COMPILEDQUERY.fields_by_name['primaryscan'].message_type = _COMPILEDQUERY_PRIMARYSCAN
_COMPILEDQUERY.fields_by_name['mergejoinscan'].message_type = _COMPILEDQUERY_MERGEJOINSCAN
_COMPILEDQUERY.fields_by_name['index_def'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._INDEX
_COMPILEDQUERY.fields_by_name['entityfilter'].message_type = _COMPILEDQUERY_ENTITYFILTER
_COMPILEDCURSOR_POSITION_INDEXVALUE.fields_by_name['value'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._PROPERTYVALUE
_COMPILEDCURSOR_POSITION_INDEXVALUE.containing_type = _COMPILEDCURSOR_POSITION
_COMPILEDCURSOR_POSITION.fields_by_name['indexvalue'].message_type = _COMPILEDCURSOR_POSITION_INDEXVALUE
_COMPILEDCURSOR_POSITION.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_COMPILEDCURSOR_POSITION.containing_type = _COMPILEDCURSOR
_COMPILEDCURSOR.fields_by_name['position'].message_type = _COMPILEDCURSOR_POSITION
_COMPILEDCURSOR.fields_by_name['postfix_position'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._INDEXPOSTFIX
_COMPILEDCURSOR.fields_by_name['absolute_position'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._INDEXPOSITION
_ERROR_ERRORCODE.containing_type = _ERROR
_COST_COMMITCOST.containing_type = _COST
_COST.fields_by_name['commitcost'].message_type = _COST_COMMITCOST
_GETREQUEST.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_GETREQUEST.fields_by_name['transaction'].message_type = _TRANSACTION
_GETRESPONSE_ENTITY.fields_by_name['entity'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._ENTITYPROTO
_GETRESPONSE_ENTITY.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_GETRESPONSE_ENTITY.containing_type = _GETRESPONSE
_GETRESPONSE.fields_by_name['entity'].message_type = _GETRESPONSE_ENTITY
_GETRESPONSE.fields_by_name['deferred'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_PUTREQUEST.fields_by_name['entity'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._ENTITYPROTO
_PUTREQUEST.fields_by_name['transaction'].message_type = _TRANSACTION
_PUTREQUEST.fields_by_name['composite_index'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._COMPOSITEINDEX
_PUTREQUEST.fields_by_name['snapshot'].message_type = google_dot_appengine_dot_datastore_dot_snapshot__pb2._SNAPSHOT
_PUTREQUEST.fields_by_name['auto_id_policy'].enum_type = _PUTREQUEST_AUTOIDPOLICY
_PUTREQUEST_AUTOIDPOLICY.containing_type = _PUTREQUEST
_PUTRESPONSE.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_PUTRESPONSE.fields_by_name['cost'].message_type = _COST
_TOUCHREQUEST.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_TOUCHREQUEST.fields_by_name['composite_index'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._COMPOSITEINDEX
_TOUCHREQUEST.fields_by_name['snapshot'].message_type = google_dot_appengine_dot_datastore_dot_snapshot__pb2._SNAPSHOT
_TOUCHRESPONSE.fields_by_name['cost'].message_type = _COST
_DELETEREQUEST.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_DELETEREQUEST.fields_by_name['transaction'].message_type = _TRANSACTION
_DELETEREQUEST.fields_by_name['composite_index'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._COMPOSITEINDEX
_DELETEREQUEST.fields_by_name['snapshot'].message_type = google_dot_appengine_dot_datastore_dot_snapshot__pb2._SNAPSHOT
_DELETERESPONSE.fields_by_name['cost'].message_type = _COST
_NEXTREQUEST.fields_by_name['cursor'].message_type = _CURSOR
_QUERYRESULT.fields_by_name['cursor'].message_type = _CURSOR
_QUERYRESULT.fields_by_name['result'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._ENTITYPROTO
_QUERYRESULT.fields_by_name['compiled_query'].message_type = _COMPILEDQUERY
_QUERYRESULT.fields_by_name['compiled_cursor'].message_type = _COMPILEDCURSOR
_QUERYRESULT.fields_by_name['index'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._COMPOSITEINDEX
_QUERYRESULT.fields_by_name['result_compiled_cursor'].message_type = _COMPILEDCURSOR
_QUERYRESULT.fields_by_name['skipped_results_compiled_cursor'].message_type = _COMPILEDCURSOR
_ALLOCATEIDSREQUEST.fields_by_name['model_key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_ALLOCATEIDSREQUEST.fields_by_name['reserve'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_ALLOCATEIDSRESPONSE.fields_by_name['cost'].message_type = _COST
_COMPOSITEINDICES.fields_by_name['index'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._COMPOSITEINDEX
_ADDACTIONSREQUEST.fields_by_name['transaction'].message_type = _TRANSACTION
_ADDACTIONSREQUEST.fields_by_name['action'].message_type = google_dot_appengine_dot_datastore_dot_action__pb2._ACTION
_BEGINTRANSACTIONREQUEST.fields_by_name['mode'].enum_type = _BEGINTRANSACTIONREQUEST_TRANSACTIONMODE
_BEGINTRANSACTIONREQUEST.fields_by_name['previous_transaction'].message_type = _TRANSACTION
_BEGINTRANSACTIONREQUEST_TRANSACTIONMODE.containing_type = _BEGINTRANSACTIONREQUEST
_COMMITRESPONSE_VERSION.fields_by_name['root_entity_key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_COMMITRESPONSE_VERSION.containing_type = _COMMITRESPONSE
_COMMITRESPONSE.fields_by_name['cost'].message_type = _COST
_COMMITRESPONSE.fields_by_name['version'].message_type = _COMMITRESPONSE_VERSION
_DATASTORESERVICE_3_METHOD.containing_type = _DATASTORESERVICE_3
DESCRIPTOR.message_types_by_name['Transaction'] = _TRANSACTION
DESCRIPTOR.message_types_by_name['Query'] = _QUERY
DESCRIPTOR.message_types_by_name['RegionPoint'] = _REGIONPOINT
DESCRIPTOR.message_types_by_name['CircleRegion'] = _CIRCLEREGION
DESCRIPTOR.message_types_by_name['RectangleRegion'] = _RECTANGLEREGION
DESCRIPTOR.message_types_by_name['GeoRegion'] = _GEOREGION
DESCRIPTOR.message_types_by_name['CompiledQuery'] = _COMPILEDQUERY
DESCRIPTOR.message_types_by_name['CompiledCursor'] = _COMPILEDCURSOR
DESCRIPTOR.message_types_by_name['Cursor'] = _CURSOR
DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['Cost'] = _COST
DESCRIPTOR.message_types_by_name['GetRequest'] = _GETREQUEST
DESCRIPTOR.message_types_by_name['GetResponse'] = _GETRESPONSE
DESCRIPTOR.message_types_by_name['PutRequest'] = _PUTREQUEST
DESCRIPTOR.message_types_by_name['PutResponse'] = _PUTRESPONSE
DESCRIPTOR.message_types_by_name['TouchRequest'] = _TOUCHREQUEST
DESCRIPTOR.message_types_by_name['TouchResponse'] = _TOUCHRESPONSE
DESCRIPTOR.message_types_by_name['DeleteRequest'] = _DELETEREQUEST
DESCRIPTOR.message_types_by_name['DeleteResponse'] = _DELETERESPONSE
DESCRIPTOR.message_types_by_name['NextRequest'] = _NEXTREQUEST
DESCRIPTOR.message_types_by_name['QueryResult'] = _QUERYRESULT
DESCRIPTOR.message_types_by_name['AllocateIdsRequest'] = _ALLOCATEIDSREQUEST
DESCRIPTOR.message_types_by_name['AllocateIdsResponse'] = _ALLOCATEIDSRESPONSE
DESCRIPTOR.message_types_by_name['CompositeIndices'] = _COMPOSITEINDICES
DESCRIPTOR.message_types_by_name['AddActionsRequest'] = _ADDACTIONSREQUEST
DESCRIPTOR.message_types_by_name['AddActionsResponse'] = _ADDACTIONSRESPONSE
DESCRIPTOR.message_types_by_name['BeginTransactionRequest'] = _BEGINTRANSACTIONREQUEST
DESCRIPTOR.message_types_by_name['CommitResponse'] = _COMMITRESPONSE
DESCRIPTOR.message_types_by_name['GetIndicesRequest'] = _GETINDICESREQUEST
DESCRIPTOR.message_types_by_name['UpdateIndexResponse'] = _UPDATEINDEXRESPONSE
DESCRIPTOR.message_types_by_name['DatastoreService_3'] = _DATASTORESERVICE_3
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Transaction = _reflection.GeneratedProtocolMessageType('Transaction', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTION,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(Transaction)

Query = _reflection.GeneratedProtocolMessageType('Query', (_message.Message,), {

  'Filter' : _reflection.GeneratedProtocolMessageType('Filter', (_message.Message,), {
    'DESCRIPTOR' : _QUERY_FILTER,
    '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

    })
  ,

  'Order' : _reflection.GeneratedProtocolMessageType('Order', (_message.Message,), {
    'DESCRIPTOR' : _QUERY_ORDER,
    '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _QUERY,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(Query)
_sym_db.RegisterMessage(Query.Filter)
_sym_db.RegisterMessage(Query.Order)

RegionPoint = _reflection.GeneratedProtocolMessageType('RegionPoint', (_message.Message,), {
  'DESCRIPTOR' : _REGIONPOINT,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(RegionPoint)

CircleRegion = _reflection.GeneratedProtocolMessageType('CircleRegion', (_message.Message,), {
  'DESCRIPTOR' : _CIRCLEREGION,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(CircleRegion)

RectangleRegion = _reflection.GeneratedProtocolMessageType('RectangleRegion', (_message.Message,), {
  'DESCRIPTOR' : _RECTANGLEREGION,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(RectangleRegion)

GeoRegion = _reflection.GeneratedProtocolMessageType('GeoRegion', (_message.Message,), {
  'DESCRIPTOR' : _GEOREGION,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(GeoRegion)

CompiledQuery = _reflection.GeneratedProtocolMessageType('CompiledQuery', (_message.Message,), {

  'PrimaryScan' : _reflection.GeneratedProtocolMessageType('PrimaryScan', (_message.Message,), {
    'DESCRIPTOR' : _COMPILEDQUERY_PRIMARYSCAN,
    '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

    })
  ,

  'MergeJoinScan' : _reflection.GeneratedProtocolMessageType('MergeJoinScan', (_message.Message,), {
    'DESCRIPTOR' : _COMPILEDQUERY_MERGEJOINSCAN,
    '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

    })
  ,

  'EntityFilter' : _reflection.GeneratedProtocolMessageType('EntityFilter', (_message.Message,), {
    'DESCRIPTOR' : _COMPILEDQUERY_ENTITYFILTER,
    '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _COMPILEDQUERY,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(CompiledQuery)
_sym_db.RegisterMessage(CompiledQuery.PrimaryScan)
_sym_db.RegisterMessage(CompiledQuery.MergeJoinScan)
_sym_db.RegisterMessage(CompiledQuery.EntityFilter)

CompiledCursor = _reflection.GeneratedProtocolMessageType('CompiledCursor', (_message.Message,), {

  'Position' : _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {

    'IndexValue' : _reflection.GeneratedProtocolMessageType('IndexValue', (_message.Message,), {
      'DESCRIPTOR' : _COMPILEDCURSOR_POSITION_INDEXVALUE,
      '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

      })
    ,
    'DESCRIPTOR' : _COMPILEDCURSOR_POSITION,
    '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _COMPILEDCURSOR,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(CompiledCursor)
_sym_db.RegisterMessage(CompiledCursor.Position)
_sym_db.RegisterMessage(CompiledCursor.Position.IndexValue)

Cursor = _reflection.GeneratedProtocolMessageType('Cursor', (_message.Message,), {
  'DESCRIPTOR' : _CURSOR,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(Cursor)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
  'DESCRIPTOR' : _ERROR,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(Error)

Cost = _reflection.GeneratedProtocolMessageType('Cost', (_message.Message,), {

  'CommitCost' : _reflection.GeneratedProtocolMessageType('CommitCost', (_message.Message,), {
    'DESCRIPTOR' : _COST_COMMITCOST,
    '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _COST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(Cost)
_sym_db.RegisterMessage(Cost.CommitCost)

GetRequest = _reflection.GeneratedProtocolMessageType('GetRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(GetRequest)

GetResponse = _reflection.GeneratedProtocolMessageType('GetResponse', (_message.Message,), {

  'Entity' : _reflection.GeneratedProtocolMessageType('Entity', (_message.Message,), {
    'DESCRIPTOR' : _GETRESPONSE_ENTITY,
    '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _GETRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(GetResponse)
_sym_db.RegisterMessage(GetResponse.Entity)

PutRequest = _reflection.GeneratedProtocolMessageType('PutRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUTREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(PutRequest)

PutResponse = _reflection.GeneratedProtocolMessageType('PutResponse', (_message.Message,), {
  'DESCRIPTOR' : _PUTRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(PutResponse)

TouchRequest = _reflection.GeneratedProtocolMessageType('TouchRequest', (_message.Message,), {
  'DESCRIPTOR' : _TOUCHREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(TouchRequest)

TouchResponse = _reflection.GeneratedProtocolMessageType('TouchResponse', (_message.Message,), {
  'DESCRIPTOR' : _TOUCHRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(TouchResponse)

DeleteRequest = _reflection.GeneratedProtocolMessageType('DeleteRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(DeleteRequest)

DeleteResponse = _reflection.GeneratedProtocolMessageType('DeleteResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETERESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(DeleteResponse)

NextRequest = _reflection.GeneratedProtocolMessageType('NextRequest', (_message.Message,), {
  'DESCRIPTOR' : _NEXTREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(NextRequest)

QueryResult = _reflection.GeneratedProtocolMessageType('QueryResult', (_message.Message,), {
  'DESCRIPTOR' : _QUERYRESULT,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(QueryResult)

AllocateIdsRequest = _reflection.GeneratedProtocolMessageType('AllocateIdsRequest', (_message.Message,), {
  'DESCRIPTOR' : _ALLOCATEIDSREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(AllocateIdsRequest)

AllocateIdsResponse = _reflection.GeneratedProtocolMessageType('AllocateIdsResponse', (_message.Message,), {
  'DESCRIPTOR' : _ALLOCATEIDSRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(AllocateIdsResponse)

CompositeIndices = _reflection.GeneratedProtocolMessageType('CompositeIndices', (_message.Message,), {
  'DESCRIPTOR' : _COMPOSITEINDICES,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(CompositeIndices)

AddActionsRequest = _reflection.GeneratedProtocolMessageType('AddActionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADDACTIONSREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(AddActionsRequest)

AddActionsResponse = _reflection.GeneratedProtocolMessageType('AddActionsResponse', (_message.Message,), {
  'DESCRIPTOR' : _ADDACTIONSRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(AddActionsResponse)

BeginTransactionRequest = _reflection.GeneratedProtocolMessageType('BeginTransactionRequest', (_message.Message,), {
  'DESCRIPTOR' : _BEGINTRANSACTIONREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(BeginTransactionRequest)

CommitResponse = _reflection.GeneratedProtocolMessageType('CommitResponse', (_message.Message,), {

  'Version' : _reflection.GeneratedProtocolMessageType('Version', (_message.Message,), {
    'DESCRIPTOR' : _COMMITRESPONSE_VERSION,
    '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _COMMITRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(CommitResponse)
_sym_db.RegisterMessage(CommitResponse.Version)

GetIndicesRequest = _reflection.GeneratedProtocolMessageType('GetIndicesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETINDICESREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(GetIndicesRequest)

UpdateIndexResponse = _reflection.GeneratedProtocolMessageType('UpdateIndexResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEINDEXRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(UpdateIndexResponse)

DatastoreService_3 = _reflection.GeneratedProtocolMessageType('DatastoreService_3', (_message.Message,), {
  'DESCRIPTOR' : _DATASTORESERVICE_3,
  '__module__' : 'google.appengine.datastore.datastore_v3_bytes_pb2'

  })
_sym_db.RegisterMessage(DatastoreService_3)


DESCRIPTOR._options = None
_QUERY.fields_by_name['persist_offset']._options = None
_COMPILEDCURSOR_POSITION_INDEXVALUE.fields_by_name['property']._options = None
_COMPILEDCURSOR_POSITION_INDEXVALUE.fields_by_name['value']._options = None
_COMPILEDCURSOR_POSITION.fields_by_name['start_key']._options = None
_COMPILEDCURSOR_POSITION.fields_by_name['indexvalue']._options = None
_COMPILEDCURSOR_POSITION.fields_by_name['key']._options = None
_COMPILEDCURSOR_POSITION.fields_by_name['start_inclusive']._options = None
_COMPILEDCURSOR_POSITION.fields_by_name['before_ascending']._options = None
_COMPILEDCURSOR.fields_by_name['position']._options = None
_NEXTREQUEST.fields_by_name['offset']._options = None

