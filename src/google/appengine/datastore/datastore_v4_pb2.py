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


from google.appengine.datastore import entity_v4_pb2 as google_dot_appengine_dot_datastore_dot_entity__v4__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/datastore/datastore_v4.proto',
  package='google.appengine.datastore.v4',
  syntax='proto2',
  serialized_options=b'\n%com.google.google.appengine.datastore',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-google/appengine/datastore/datastore_v4.proto\x12\x1dgoogle.appengine.datastore.v4\x1a*google/appengine/datastore/entity_v4.proto\"\x9f\x03\n\x05\x45rror\"\x95\x03\n\tErrorCode\x12\x0f\n\x0b\x42\x41\x44_REQUEST\x10\x01\x12\x1a\n\x16\x43ONCURRENT_TRANSACTION\x10\x02\x12\x12\n\x0eINTERNAL_ERROR\x10\x03\x12\x0e\n\nNEED_INDEX\x10\x04\x12\x0b\n\x07TIMEOUT\x10\x05\x12\x15\n\x11PERMISSION_DENIED\x10\x06\x12\x12\n\x0e\x42IGTABLE_ERROR\x10\x07\x12 \n\x1c\x43OMMITTED_BUT_STILL_APPLYING\x10\x08\x12\x17\n\x13\x43\x41PABILITY_DISABLED\x10\t\x12\x19\n\x15TRY_ALTERNATE_BACKEND\x10\n\x12\x15\n\x11SAFE_TIME_TOO_OLD\x10\x0b\x12\x16\n\x12RESOURCE_EXHAUSTED\x10\x0c\x12\x1c\n\x18SNAPSHOT_VERSION_TOO_OLD\x10\x12\x12\r\n\tNOT_FOUND\x10\r\x12\x12\n\x0e\x41LREADY_EXISTS\x10\x0e\x12\x17\n\x13\x46\x41ILED_PRECONDITION\x10\x0f\x12\x13\n\x0fUNAUTHENTICATED\x10\x10\x12\x0b\n\x07\x41\x42ORTED\x10\x11\"\x9c\x01\n\x0c\x45ntityResult\x12\x35\n\x06\x65ntity\x18\x01 \x02(\x0b\x32%.google.appengine.datastore.v4.Entity\x12\x0f\n\x07version\x18\x02 \x01(\x03\x12\x0e\n\x06\x63ursor\x18\x03 \x01(\x0c\"4\n\nResultType\x12\x08\n\x04\x46ULL\x10\x01\x12\x0e\n\nPROJECTION\x10\x02\x12\x0c\n\x08KEY_ONLY\x10\x03\"\x8f\x03\n\x05Query\x12\x45\n\nprojection\x18\x02 \x03(\x0b\x32\x31.google.appengine.datastore.v4.PropertyExpression\x12;\n\x04kind\x18\x03 \x03(\x0b\x32-.google.appengine.datastore.v4.KindExpression\x12\x35\n\x06\x66ilter\x18\x04 \x01(\x0b\x32%.google.appengine.datastore.v4.Filter\x12;\n\x05order\x18\x05 \x03(\x0b\x32,.google.appengine.datastore.v4.PropertyOrder\x12\x42\n\x08group_by\x18\x06 \x03(\x0b\x32\x30.google.appengine.datastore.v4.PropertyReference\x12\x14\n\x0cstart_cursor\x18\x07 \x01(\x0c\x12\x12\n\nend_cursor\x18\x08 \x01(\x0c\x12\x11\n\x06offset\x18\n \x01(\x05:\x01\x30\x12\r\n\x05limit\x18\x0b \x01(\x05\"\x1e\n\x0eKindExpression\x12\x0c\n\x04name\x18\x01 \x02(\t\"!\n\x11PropertyReference\x12\x0c\n\x04name\x18\x02 \x02(\t\"\xdf\x01\n\x12PropertyExpression\x12\x42\n\x08property\x18\x01 \x02(\x0b\x32\x30.google.appengine.datastore.v4.PropertyReference\x12\x63\n\x14\x61ggregation_function\x18\x02 \x01(\x0e\x32\x45.google.appengine.datastore.v4.PropertyExpression.AggregationFunction\" \n\x13\x41ggregationFunction\x12\t\n\x05\x46IRST\x10\x01\"\xd5\x01\n\rPropertyOrder\x12\x42\n\x08property\x18\x01 \x02(\x0b\x32\x30.google.appengine.datastore.v4.PropertyReference\x12T\n\tdirection\x18\x02 \x01(\x0e\x32\x36.google.appengine.datastore.v4.PropertyOrder.Direction:\tASCENDING\"*\n\tDirection\x12\r\n\tASCENDING\x10\x01\x12\x0e\n\nDESCENDING\x10\x02\"\x9a\x01\n\x06\x46ilter\x12H\n\x10\x63omposite_filter\x18\x01 \x01(\x0b\x32..google.appengine.datastore.v4.CompositeFilter\x12\x46\n\x0fproperty_filter\x18\x02 \x01(\x0b\x32-.google.appengine.datastore.v4.PropertyFilter\"\xa8\x01\n\x0f\x43ompositeFilter\x12I\n\x08operator\x18\x01 \x02(\x0e\x32\x37.google.appengine.datastore.v4.CompositeFilter.Operator\x12\x35\n\x06\x66ilter\x18\x02 \x03(\x0b\x32%.google.appengine.datastore.v4.Filter\"\x13\n\x08Operator\x12\x07\n\x03\x41ND\x10\x01\"\xd0\x02\n\x0ePropertyFilter\x12\x42\n\x08property\x18\x01 \x02(\x0b\x32\x30.google.appengine.datastore.v4.PropertyReference\x12H\n\x08operator\x18\x02 \x02(\x0e\x32\x36.google.appengine.datastore.v4.PropertyFilter.Operator\x12\x33\n\x05value\x18\x03 \x02(\x0b\x32$.google.appengine.datastore.v4.Value\"{\n\x08Operator\x12\r\n\tLESS_THAN\x10\x01\x12\x16\n\x12LESS_THAN_OR_EQUAL\x10\x02\x12\x10\n\x0cGREATER_THAN\x10\x03\x12\x19\n\x15GREATER_THAN_OR_EQUAL\x10\x04\x12\t\n\x05\x45QUAL\x10\x05\x12\x10\n\x0cHAS_ANCESTOR\x10\x0b\"\xbc\x01\n\x08GqlQuery\x12\x14\n\x0cquery_string\x18\x01 \x02(\t\x12\x1c\n\rallow_literal\x18\x02 \x01(\x08:\x05\x66\x61lse\x12<\n\x08name_arg\x18\x03 \x03(\x0b\x32*.google.appengine.datastore.v4.GqlQueryArg\x12>\n\nnumber_arg\x18\x04 \x03(\x0b\x32*.google.appengine.datastore.v4.GqlQueryArg\"`\n\x0bGqlQueryArg\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x33\n\x05value\x18\x02 \x01(\x0b\x32$.google.appengine.datastore.v4.Value\x12\x0e\n\x06\x63ursor\x18\x03 \x01(\x0c\"\xbb\x03\n\x10QueryResultBatch\x12R\n\x12\x65ntity_result_type\x18\x01 \x02(\x0e\x32\x36.google.appengine.datastore.v4.EntityResult.ResultType\x12\x42\n\rentity_result\x18\x02 \x03(\x0b\x32+.google.appengine.datastore.v4.EntityResult\x12\x16\n\x0eskipped_cursor\x18\x03 \x01(\x0c\x12\x12\n\nend_cursor\x18\x04 \x01(\x0c\x12U\n\x0cmore_results\x18\x05 \x02(\x0e\x32?.google.appengine.datastore.v4.QueryResultBatch.MoreResultsType\x12\x1a\n\x0fskipped_results\x18\x06 \x01(\x05:\x01\x30\x12\x18\n\x10snapshot_version\x18\x07 \x01(\x03\"V\n\x0fMoreResultsType\x12\x10\n\x0cNOT_FINISHED\x10\x01\x12\x1c\n\x18MORE_RESULTS_AFTER_LIMIT\x10\x02\x12\x13\n\x0fNO_MORE_RESULTS\x10\x03\"\x84\x02\n\x08Mutation\x12\x46\n\x02op\x18\x01 \x01(\x0e\x32\x31.google.appengine.datastore.v4.Mutation.Operation:\x07UNKNOWN\x12/\n\x03key\x18\x02 \x01(\x0b\x32\".google.appengine.datastore.v4.Key\x12\x35\n\x06\x65ntity\x18\x03 \x01(\x0b\x32%.google.appengine.datastore.v4.Entity\"H\n\tOperation\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06INSERT\x10\x01\x12\n\n\x06UPDATE\x10\x02\x12\n\n\x06UPSERT\x10\x03\x12\n\n\x06\x44\x45LETE\x10\x04\"Y\n\x0eMutationResult\x12/\n\x03key\x18\x03 \x01(\x0b\x32\".google.appengine.datastore.v4.Key\x12\x16\n\x0bnew_version\x18\x04 \x01(\x03:\x01\x30\"\xbb\x02\n\x12\x44\x65precatedMutation\x12\x35\n\x06upsert\x18\x01 \x03(\x0b\x32%.google.appengine.datastore.v4.Entity\x12\x35\n\x06update\x18\x02 \x03(\x0b\x32%.google.appengine.datastore.v4.Entity\x12\x35\n\x06insert\x18\x03 \x03(\x0b\x32%.google.appengine.datastore.v4.Entity\x12=\n\x0einsert_auto_id\x18\x04 \x03(\x0b\x32%.google.appengine.datastore.v4.Entity\x12\x32\n\x06\x64\x65lete\x18\x05 \x03(\x0b\x32\".google.appengine.datastore.v4.Key\x12\r\n\x05\x66orce\x18\x06 \x01(\x08\"\xf1\x01\n\x18\x44\x65precatedMutationResult\x12\x15\n\rindex_updates\x18\x01 \x02(\x05\x12>\n\x12insert_auto_id_key\x18\x02 \x03(\x0b\x32\".google.appengine.datastore.v4.Key\x12\x16\n\x0eupsert_version\x18\x03 \x03(\x03\x12\x16\n\x0eupdate_version\x18\x04 \x03(\x03\x12\x16\n\x0einsert_version\x18\x05 \x03(\x03\x12\x1e\n\x16insert_auto_id_version\x18\x06 \x03(\x03\x12\x16\n\x0e\x64\x65lete_version\x18\x07 \x03(\x03\"\xbb\x01\n\x0bReadOptions\x12]\n\x10read_consistency\x18\x01 \x01(\x0e\x32:.google.appengine.datastore.v4.ReadOptions.ReadConsistency:\x07\x44\x45\x46\x41ULT\x12\x13\n\x0btransaction\x18\x02 \x01(\x0c\"8\n\x0fReadConsistency\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\n\n\x06STRONG\x10\x01\x12\x0c\n\x08\x45VENTUAL\x10\x02\"\x82\x01\n\rLookupRequest\x12@\n\x0cread_options\x18\x01 \x01(\x0b\x32*.google.appengine.datastore.v4.ReadOptions\x12/\n\x03key\x18\x03 \x03(\x0b\x32\".google.appengine.datastore.v4.Key\"\xc0\x01\n\x0eLookupResponse\x12:\n\x05\x66ound\x18\x01 \x03(\x0b\x32+.google.appengine.datastore.v4.EntityResult\x12<\n\x07missing\x18\x02 \x03(\x0b\x32+.google.appengine.datastore.v4.EntityResult\x12\x34\n\x08\x64\x65\x66\x65rred\x18\x03 \x03(\x0b\x32\".google.appengine.datastore.v4.Key\"\xc3\x02\n\x0fRunQueryRequest\x12@\n\x0cread_options\x18\x01 \x01(\x0b\x32*.google.appengine.datastore.v4.ReadOptions\x12@\n\x0cpartition_id\x18\x02 \x01(\x0b\x32*.google.appengine.datastore.v4.PartitionId\x12\x33\n\x05query\x18\x03 \x01(\x0b\x32$.google.appengine.datastore.v4.Query\x12:\n\tgql_query\x18\x07 \x01(\x0b\x32\'.google.appengine.datastore.v4.GqlQuery\x12\x1d\n\x15min_safe_time_seconds\x18\x04 \x01(\x03\x12\x1c\n\x14suggested_batch_size\x18\x05 \x01(\x05\"h\n\x10RunQueryResponse\x12>\n\x05\x62\x61tch\x18\x01 \x02(\x0b\x32/.google.appengine.datastore.v4.QueryResultBatch\x12\x14\n\x0cquery_handle\x18\x02 \x01(\x0c\",\n\x14\x43ontinueQueryRequest\x12\x14\n\x0cquery_handle\x18\x01 \x02(\x0c\"W\n\x15\x43ontinueQueryResponse\x12>\n\x05\x62\x61tch\x18\x01 \x02(\x0b\x32/.google.appengine.datastore.v4.QueryResultBatch\"S\n\x17\x42\x65ginTransactionRequest\x12\x1a\n\x0b\x63ross_group\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x1c\n\rcross_request\x18\x02 \x01(\x08:\x05\x66\x61lse\"/\n\x18\x42\x65ginTransactionResponse\x12\x13\n\x0btransaction\x18\x01 \x02(\x0c\"&\n\x0fRollbackRequest\x12\x13\n\x0btransaction\x18\x01 \x02(\x0c\"\x12\n\x10RollbackResponse\"\xd2\x02\n\rCommitRequest\x12\x13\n\x0btransaction\x18\x01 \x01(\x0c\x12\x39\n\x08mutation\x18\x05 \x03(\x0b\x32\'.google.appengine.datastore.v4.Mutation\x12N\n\x13\x64\x65precated_mutation\x18\x02 \x01(\x0b\x32\x31.google.appengine.datastore.v4.DeprecatedMutation\x12N\n\x04mode\x18\x04 \x01(\x0e\x32\x31.google.appengine.datastore.v4.CommitRequest.Mode:\rTRANSACTIONAL\x12\x1f\n\x10ignore_read_only\x18\x06 \x01(\x08:\x05\x66\x61lse\"0\n\x04Mode\x12\x11\n\rTRANSACTIONAL\x10\x01\x12\x15\n\x11NON_TRANSACTIONAL\x10\x02\"\xcc\x01\n\x0e\x43ommitResponse\x12\x46\n\x0fmutation_result\x18\x03 \x03(\x0b\x32-.google.appengine.datastore.v4.MutationResult\x12[\n\x1a\x64\x65precated_mutation_result\x18\x01 \x01(\x0b\x32\x37.google.appengine.datastore.v4.DeprecatedMutationResult\x12\x15\n\rindex_updates\x18\x04 \x01(\x05\"\x7f\n\x12\x41llocateIdsRequest\x12\x34\n\x08\x61llocate\x18\x01 \x03(\x0b\x32\".google.appengine.datastore.v4.Key\x12\x33\n\x07reserve\x18\x02 \x03(\x0b\x32\".google.appengine.datastore.v4.Key\"L\n\x13\x41llocateIdsResponse\x12\x35\n\tallocated\x18\x01 \x03(\x0b\x32\".google.appengine.datastore.v4.KeyB\'\n%com.google.google.appengine.datastore'
  ,
  dependencies=[google_dot_appengine_dot_datastore_dot_entity__v4__pb2.DESCRIPTOR,])



_ERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.datastore.v4.Error.ErrorCode',
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
  serialized_start=135,
  serialized_end=540,
)
_sym_db.RegisterEnumDescriptor(_ERROR_ERRORCODE)

_ENTITYRESULT_RESULTTYPE = _descriptor.EnumDescriptor(
  name='ResultType',
  full_name='google.appengine.datastore.v4.EntityResult.ResultType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FULL', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PROJECTION', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='KEY_ONLY', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=647,
  serialized_end=699,
)
_sym_db.RegisterEnumDescriptor(_ENTITYRESULT_RESULTTYPE)

_PROPERTYEXPRESSION_AGGREGATIONFUNCTION = _descriptor.EnumDescriptor(
  name='AggregationFunction',
  full_name='google.appengine.datastore.v4.PropertyExpression.AggregationFunction',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FIRST', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1362,
  serialized_end=1394,
)
_sym_db.RegisterEnumDescriptor(_PROPERTYEXPRESSION_AGGREGATIONFUNCTION)

_PROPERTYORDER_DIRECTION = _descriptor.EnumDescriptor(
  name='Direction',
  full_name='google.appengine.datastore.v4.PropertyOrder.Direction',
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
  serialized_start=1568,
  serialized_end=1610,
)
_sym_db.RegisterEnumDescriptor(_PROPERTYORDER_DIRECTION)

_COMPOSITEFILTER_OPERATOR = _descriptor.EnumDescriptor(
  name='Operator',
  full_name='google.appengine.datastore.v4.CompositeFilter.Operator',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='AND', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1919,
  serialized_end=1938,
)
_sym_db.RegisterEnumDescriptor(_COMPOSITEFILTER_OPERATOR)

_PROPERTYFILTER_OPERATOR = _descriptor.EnumDescriptor(
  name='Operator',
  full_name='google.appengine.datastore.v4.PropertyFilter.Operator',
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
      name='HAS_ANCESTOR', index=5, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2154,
  serialized_end=2277,
)
_sym_db.RegisterEnumDescriptor(_PROPERTYFILTER_OPERATOR)

_QUERYRESULTBATCH_MORERESULTSTYPE = _descriptor.EnumDescriptor(
  name='MoreResultsType',
  full_name='google.appengine.datastore.v4.QueryResultBatch.MoreResultsType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NOT_FINISHED', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MORE_RESULTS_AFTER_LIMIT', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NO_MORE_RESULTS', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2926,
  serialized_end=3012,
)
_sym_db.RegisterEnumDescriptor(_QUERYRESULTBATCH_MORERESULTSTYPE)

_MUTATION_OPERATION = _descriptor.EnumDescriptor(
  name='Operation',
  full_name='google.appengine.datastore.v4.Mutation.Operation',
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
      name='INSERT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UPDATE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UPSERT', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DELETE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=3203,
  serialized_end=3275,
)
_sym_db.RegisterEnumDescriptor(_MUTATION_OPERATION)

_READOPTIONS_READCONSISTENCY = _descriptor.EnumDescriptor(
  name='ReadConsistency',
  full_name='google.appengine.datastore.v4.ReadOptions.ReadConsistency',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DEFAULT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='STRONG', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENTUAL', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=4062,
  serialized_end=4118,
)
_sym_db.RegisterEnumDescriptor(_READOPTIONS_READCONSISTENCY)

_COMMITREQUEST_MODE = _descriptor.EnumDescriptor(
  name='Mode',
  full_name='google.appengine.datastore.v4.CommitRequest.Mode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TRANSACTIONAL', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NON_TRANSACTIONAL', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=5500,
  serialized_end=5548,
)
_sym_db.RegisterEnumDescriptor(_COMMITREQUEST_MODE)


_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='google.appengine.datastore.v4.Error',
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
  serialized_start=125,
  serialized_end=540,
)


_ENTITYRESULT = _descriptor.Descriptor(
  name='EntityResult',
  full_name='google.appengine.datastore.v4.EntityResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity', full_name='google.appengine.datastore.v4.EntityResult.entity', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='google.appengine.datastore.v4.EntityResult.version', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cursor', full_name='google.appengine.datastore.v4.EntityResult.cursor', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ENTITYRESULT_RESULTTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=543,
  serialized_end=699,
)


_QUERY = _descriptor.Descriptor(
  name='Query',
  full_name='google.appengine.datastore.v4.Query',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='projection', full_name='google.appengine.datastore.v4.Query.projection', index=0,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kind', full_name='google.appengine.datastore.v4.Query.kind', index=1,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filter', full_name='google.appengine.datastore.v4.Query.filter', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='order', full_name='google.appengine.datastore.v4.Query.order', index=3,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_by', full_name='google.appengine.datastore.v4.Query.group_by', index=4,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_cursor', full_name='google.appengine.datastore.v4.Query.start_cursor', index=5,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_cursor', full_name='google.appengine.datastore.v4.Query.end_cursor', index=6,
      number=8, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='offset', full_name='google.appengine.datastore.v4.Query.offset', index=7,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='limit', full_name='google.appengine.datastore.v4.Query.limit', index=8,
      number=11, type=5, cpp_type=1, label=1,
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
  serialized_start=702,
  serialized_end=1101,
)


_KINDEXPRESSION = _descriptor.Descriptor(
  name='KindExpression',
  full_name='google.appengine.datastore.v4.KindExpression',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='google.appengine.datastore.v4.KindExpression.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  serialized_start=1103,
  serialized_end=1133,
)


_PROPERTYREFERENCE = _descriptor.Descriptor(
  name='PropertyReference',
  full_name='google.appengine.datastore.v4.PropertyReference',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='google.appengine.datastore.v4.PropertyReference.name', index=0,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=1135,
  serialized_end=1168,
)


_PROPERTYEXPRESSION = _descriptor.Descriptor(
  name='PropertyExpression',
  full_name='google.appengine.datastore.v4.PropertyExpression',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='property', full_name='google.appengine.datastore.v4.PropertyExpression.property', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='aggregation_function', full_name='google.appengine.datastore.v4.PropertyExpression.aggregation_function', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PROPERTYEXPRESSION_AGGREGATIONFUNCTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1171,
  serialized_end=1394,
)


_PROPERTYORDER = _descriptor.Descriptor(
  name='PropertyOrder',
  full_name='google.appengine.datastore.v4.PropertyOrder',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='property', full_name='google.appengine.datastore.v4.PropertyOrder.property', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='direction', full_name='google.appengine.datastore.v4.PropertyOrder.direction', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PROPERTYORDER_DIRECTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1397,
  serialized_end=1610,
)


_FILTER = _descriptor.Descriptor(
  name='Filter',
  full_name='google.appengine.datastore.v4.Filter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='composite_filter', full_name='google.appengine.datastore.v4.Filter.composite_filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='property_filter', full_name='google.appengine.datastore.v4.Filter.property_filter', index=1,
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
  serialized_start=1613,
  serialized_end=1767,
)


_COMPOSITEFILTER = _descriptor.Descriptor(
  name='CompositeFilter',
  full_name='google.appengine.datastore.v4.CompositeFilter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='operator', full_name='google.appengine.datastore.v4.CompositeFilter.operator', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filter', full_name='google.appengine.datastore.v4.CompositeFilter.filter', index=1,
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
    _COMPOSITEFILTER_OPERATOR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1770,
  serialized_end=1938,
)


_PROPERTYFILTER = _descriptor.Descriptor(
  name='PropertyFilter',
  full_name='google.appengine.datastore.v4.PropertyFilter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='property', full_name='google.appengine.datastore.v4.PropertyFilter.property', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='operator', full_name='google.appengine.datastore.v4.PropertyFilter.operator', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.datastore.v4.PropertyFilter.value', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PROPERTYFILTER_OPERATOR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1941,
  serialized_end=2277,
)


_GQLQUERY = _descriptor.Descriptor(
  name='GqlQuery',
  full_name='google.appengine.datastore.v4.GqlQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query_string', full_name='google.appengine.datastore.v4.GqlQuery.query_string', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='allow_literal', full_name='google.appengine.datastore.v4.GqlQuery.allow_literal', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name_arg', full_name='google.appengine.datastore.v4.GqlQuery.name_arg', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='number_arg', full_name='google.appengine.datastore.v4.GqlQuery.number_arg', index=3,
      number=4, type=11, cpp_type=10, label=3,
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
  serialized_start=2280,
  serialized_end=2468,
)


_GQLQUERYARG = _descriptor.Descriptor(
  name='GqlQueryArg',
  full_name='google.appengine.datastore.v4.GqlQueryArg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='google.appengine.datastore.v4.GqlQueryArg.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.datastore.v4.GqlQueryArg.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cursor', full_name='google.appengine.datastore.v4.GqlQueryArg.cursor', index=2,
      number=3, type=12, cpp_type=9, label=1,
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
  serialized_start=2470,
  serialized_end=2566,
)


_QUERYRESULTBATCH = _descriptor.Descriptor(
  name='QueryResultBatch',
  full_name='google.appengine.datastore.v4.QueryResultBatch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity_result_type', full_name='google.appengine.datastore.v4.QueryResultBatch.entity_result_type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_result', full_name='google.appengine.datastore.v4.QueryResultBatch.entity_result', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='skipped_cursor', full_name='google.appengine.datastore.v4.QueryResultBatch.skipped_cursor', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_cursor', full_name='google.appengine.datastore.v4.QueryResultBatch.end_cursor', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='more_results', full_name='google.appengine.datastore.v4.QueryResultBatch.more_results', index=4,
      number=5, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='skipped_results', full_name='google.appengine.datastore.v4.QueryResultBatch.skipped_results', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='snapshot_version', full_name='google.appengine.datastore.v4.QueryResultBatch.snapshot_version', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _QUERYRESULTBATCH_MORERESULTSTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2569,
  serialized_end=3012,
)


_MUTATION = _descriptor.Descriptor(
  name='Mutation',
  full_name='google.appengine.datastore.v4.Mutation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='op', full_name='google.appengine.datastore.v4.Mutation.op', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.datastore.v4.Mutation.key', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity', full_name='google.appengine.datastore.v4.Mutation.entity', index=2,
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
    _MUTATION_OPERATION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3015,
  serialized_end=3275,
)


_MUTATIONRESULT = _descriptor.Descriptor(
  name='MutationResult',
  full_name='google.appengine.datastore.v4.MutationResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.datastore.v4.MutationResult.key', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='new_version', full_name='google.appengine.datastore.v4.MutationResult.new_version', index=1,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=True, default_value=0,
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
  serialized_start=3277,
  serialized_end=3366,
)


_DEPRECATEDMUTATION = _descriptor.Descriptor(
  name='DeprecatedMutation',
  full_name='google.appengine.datastore.v4.DeprecatedMutation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='upsert', full_name='google.appengine.datastore.v4.DeprecatedMutation.upsert', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='update', full_name='google.appengine.datastore.v4.DeprecatedMutation.update', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='insert', full_name='google.appengine.datastore.v4.DeprecatedMutation.insert', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='insert_auto_id', full_name='google.appengine.datastore.v4.DeprecatedMutation.insert_auto_id', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='delete', full_name='google.appengine.datastore.v4.DeprecatedMutation.delete', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='force', full_name='google.appengine.datastore.v4.DeprecatedMutation.force', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=3369,
  serialized_end=3684,
)


_DEPRECATEDMUTATIONRESULT = _descriptor.Descriptor(
  name='DeprecatedMutationResult',
  full_name='google.appengine.datastore.v4.DeprecatedMutationResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index_updates', full_name='google.appengine.datastore.v4.DeprecatedMutationResult.index_updates', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='insert_auto_id_key', full_name='google.appengine.datastore.v4.DeprecatedMutationResult.insert_auto_id_key', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='upsert_version', full_name='google.appengine.datastore.v4.DeprecatedMutationResult.upsert_version', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='update_version', full_name='google.appengine.datastore.v4.DeprecatedMutationResult.update_version', index=3,
      number=4, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='insert_version', full_name='google.appengine.datastore.v4.DeprecatedMutationResult.insert_version', index=4,
      number=5, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='insert_auto_id_version', full_name='google.appengine.datastore.v4.DeprecatedMutationResult.insert_auto_id_version', index=5,
      number=6, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='delete_version', full_name='google.appengine.datastore.v4.DeprecatedMutationResult.delete_version', index=6,
      number=7, type=3, cpp_type=2, label=3,
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
  serialized_start=3687,
  serialized_end=3928,
)


_READOPTIONS = _descriptor.Descriptor(
  name='ReadOptions',
  full_name='google.appengine.datastore.v4.ReadOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='read_consistency', full_name='google.appengine.datastore.v4.ReadOptions.read_consistency', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transaction', full_name='google.appengine.datastore.v4.ReadOptions.transaction', index=1,
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
    _READOPTIONS_READCONSISTENCY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3931,
  serialized_end=4118,
)


_LOOKUPREQUEST = _descriptor.Descriptor(
  name='LookupRequest',
  full_name='google.appengine.datastore.v4.LookupRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='read_options', full_name='google.appengine.datastore.v4.LookupRequest.read_options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.datastore.v4.LookupRequest.key', index=1,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=4121,
  serialized_end=4251,
)


_LOOKUPRESPONSE = _descriptor.Descriptor(
  name='LookupResponse',
  full_name='google.appengine.datastore.v4.LookupResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='found', full_name='google.appengine.datastore.v4.LookupResponse.found', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='missing', full_name='google.appengine.datastore.v4.LookupResponse.missing', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deferred', full_name='google.appengine.datastore.v4.LookupResponse.deferred', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=4254,
  serialized_end=4446,
)


_RUNQUERYREQUEST = _descriptor.Descriptor(
  name='RunQueryRequest',
  full_name='google.appengine.datastore.v4.RunQueryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='read_options', full_name='google.appengine.datastore.v4.RunQueryRequest.read_options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='partition_id', full_name='google.appengine.datastore.v4.RunQueryRequest.partition_id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='google.appengine.datastore.v4.RunQueryRequest.query', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gql_query', full_name='google.appengine.datastore.v4.RunQueryRequest.gql_query', index=3,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='min_safe_time_seconds', full_name='google.appengine.datastore.v4.RunQueryRequest.min_safe_time_seconds', index=4,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='suggested_batch_size', full_name='google.appengine.datastore.v4.RunQueryRequest.suggested_batch_size', index=5,
      number=5, type=5, cpp_type=1, label=1,
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
  serialized_start=4449,
  serialized_end=4772,
)


_RUNQUERYRESPONSE = _descriptor.Descriptor(
  name='RunQueryResponse',
  full_name='google.appengine.datastore.v4.RunQueryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='batch', full_name='google.appengine.datastore.v4.RunQueryResponse.batch', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query_handle', full_name='google.appengine.datastore.v4.RunQueryResponse.query_handle', index=1,
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
  serialized_start=4774,
  serialized_end=4878,
)


_CONTINUEQUERYREQUEST = _descriptor.Descriptor(
  name='ContinueQueryRequest',
  full_name='google.appengine.datastore.v4.ContinueQueryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query_handle', full_name='google.appengine.datastore.v4.ContinueQueryRequest.query_handle', index=0,
      number=1, type=12, cpp_type=9, label=2,
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
  serialized_start=4880,
  serialized_end=4924,
)


_CONTINUEQUERYRESPONSE = _descriptor.Descriptor(
  name='ContinueQueryResponse',
  full_name='google.appengine.datastore.v4.ContinueQueryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='batch', full_name='google.appengine.datastore.v4.ContinueQueryResponse.batch', index=0,
      number=1, type=11, cpp_type=10, label=2,
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
  serialized_start=4926,
  serialized_end=5013,
)


_BEGINTRANSACTIONREQUEST = _descriptor.Descriptor(
  name='BeginTransactionRequest',
  full_name='google.appengine.datastore.v4.BeginTransactionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cross_group', full_name='google.appengine.datastore.v4.BeginTransactionRequest.cross_group', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cross_request', full_name='google.appengine.datastore.v4.BeginTransactionRequest.cross_request', index=1,
      number=2, type=8, cpp_type=7, label=1,
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
  serialized_start=5015,
  serialized_end=5098,
)


_BEGINTRANSACTIONRESPONSE = _descriptor.Descriptor(
  name='BeginTransactionResponse',
  full_name='google.appengine.datastore.v4.BeginTransactionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction', full_name='google.appengine.datastore.v4.BeginTransactionResponse.transaction', index=0,
      number=1, type=12, cpp_type=9, label=2,
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
  serialized_start=5100,
  serialized_end=5147,
)


_ROLLBACKREQUEST = _descriptor.Descriptor(
  name='RollbackRequest',
  full_name='google.appengine.datastore.v4.RollbackRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction', full_name='google.appengine.datastore.v4.RollbackRequest.transaction', index=0,
      number=1, type=12, cpp_type=9, label=2,
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
  serialized_start=5149,
  serialized_end=5187,
)


_ROLLBACKRESPONSE = _descriptor.Descriptor(
  name='RollbackResponse',
  full_name='google.appengine.datastore.v4.RollbackResponse',
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
  serialized_start=5189,
  serialized_end=5207,
)


_COMMITREQUEST = _descriptor.Descriptor(
  name='CommitRequest',
  full_name='google.appengine.datastore.v4.CommitRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction', full_name='google.appengine.datastore.v4.CommitRequest.transaction', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mutation', full_name='google.appengine.datastore.v4.CommitRequest.mutation', index=1,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_mutation', full_name='google.appengine.datastore.v4.CommitRequest.deprecated_mutation', index=2,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode', full_name='google.appengine.datastore.v4.CommitRequest.mode', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ignore_read_only', full_name='google.appengine.datastore.v4.CommitRequest.ignore_read_only', index=4,
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
    _COMMITREQUEST_MODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5210,
  serialized_end=5548,
)


_COMMITRESPONSE = _descriptor.Descriptor(
  name='CommitResponse',
  full_name='google.appengine.datastore.v4.CommitResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mutation_result', full_name='google.appengine.datastore.v4.CommitResponse.mutation_result', index=0,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_mutation_result', full_name='google.appengine.datastore.v4.CommitResponse.deprecated_mutation_result', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='index_updates', full_name='google.appengine.datastore.v4.CommitResponse.index_updates', index=2,
      number=4, type=5, cpp_type=1, label=1,
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
  serialized_start=5551,
  serialized_end=5755,
)


_ALLOCATEIDSREQUEST = _descriptor.Descriptor(
  name='AllocateIdsRequest',
  full_name='google.appengine.datastore.v4.AllocateIdsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='allocate', full_name='google.appengine.datastore.v4.AllocateIdsRequest.allocate', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reserve', full_name='google.appengine.datastore.v4.AllocateIdsRequest.reserve', index=1,
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
  serialized_start=5757,
  serialized_end=5884,
)


_ALLOCATEIDSRESPONSE = _descriptor.Descriptor(
  name='AllocateIdsResponse',
  full_name='google.appengine.datastore.v4.AllocateIdsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='allocated', full_name='google.appengine.datastore.v4.AllocateIdsResponse.allocated', index=0,
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
  serialized_start=5886,
  serialized_end=5962,
)

_ERROR_ERRORCODE.containing_type = _ERROR
_ENTITYRESULT.fields_by_name['entity'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._ENTITY
_ENTITYRESULT_RESULTTYPE.containing_type = _ENTITYRESULT
_QUERY.fields_by_name['projection'].message_type = _PROPERTYEXPRESSION
_QUERY.fields_by_name['kind'].message_type = _KINDEXPRESSION
_QUERY.fields_by_name['filter'].message_type = _FILTER
_QUERY.fields_by_name['order'].message_type = _PROPERTYORDER
_QUERY.fields_by_name['group_by'].message_type = _PROPERTYREFERENCE
_PROPERTYEXPRESSION.fields_by_name['property'].message_type = _PROPERTYREFERENCE
_PROPERTYEXPRESSION.fields_by_name['aggregation_function'].enum_type = _PROPERTYEXPRESSION_AGGREGATIONFUNCTION
_PROPERTYEXPRESSION_AGGREGATIONFUNCTION.containing_type = _PROPERTYEXPRESSION
_PROPERTYORDER.fields_by_name['property'].message_type = _PROPERTYREFERENCE
_PROPERTYORDER.fields_by_name['direction'].enum_type = _PROPERTYORDER_DIRECTION
_PROPERTYORDER_DIRECTION.containing_type = _PROPERTYORDER
_FILTER.fields_by_name['composite_filter'].message_type = _COMPOSITEFILTER
_FILTER.fields_by_name['property_filter'].message_type = _PROPERTYFILTER
_COMPOSITEFILTER.fields_by_name['operator'].enum_type = _COMPOSITEFILTER_OPERATOR
_COMPOSITEFILTER.fields_by_name['filter'].message_type = _FILTER
_COMPOSITEFILTER_OPERATOR.containing_type = _COMPOSITEFILTER
_PROPERTYFILTER.fields_by_name['property'].message_type = _PROPERTYREFERENCE
_PROPERTYFILTER.fields_by_name['operator'].enum_type = _PROPERTYFILTER_OPERATOR
_PROPERTYFILTER.fields_by_name['value'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._VALUE
_PROPERTYFILTER_OPERATOR.containing_type = _PROPERTYFILTER
_GQLQUERY.fields_by_name['name_arg'].message_type = _GQLQUERYARG
_GQLQUERY.fields_by_name['number_arg'].message_type = _GQLQUERYARG
_GQLQUERYARG.fields_by_name['value'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._VALUE
_QUERYRESULTBATCH.fields_by_name['entity_result_type'].enum_type = _ENTITYRESULT_RESULTTYPE
_QUERYRESULTBATCH.fields_by_name['entity_result'].message_type = _ENTITYRESULT
_QUERYRESULTBATCH.fields_by_name['more_results'].enum_type = _QUERYRESULTBATCH_MORERESULTSTYPE
_QUERYRESULTBATCH_MORERESULTSTYPE.containing_type = _QUERYRESULTBATCH
_MUTATION.fields_by_name['op'].enum_type = _MUTATION_OPERATION
_MUTATION.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._KEY
_MUTATION.fields_by_name['entity'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._ENTITY
_MUTATION_OPERATION.containing_type = _MUTATION
_MUTATIONRESULT.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._KEY
_DEPRECATEDMUTATION.fields_by_name['upsert'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._ENTITY
_DEPRECATEDMUTATION.fields_by_name['update'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._ENTITY
_DEPRECATEDMUTATION.fields_by_name['insert'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._ENTITY
_DEPRECATEDMUTATION.fields_by_name['insert_auto_id'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._ENTITY
_DEPRECATEDMUTATION.fields_by_name['delete'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._KEY
_DEPRECATEDMUTATIONRESULT.fields_by_name['insert_auto_id_key'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._KEY
_READOPTIONS.fields_by_name['read_consistency'].enum_type = _READOPTIONS_READCONSISTENCY
_READOPTIONS_READCONSISTENCY.containing_type = _READOPTIONS
_LOOKUPREQUEST.fields_by_name['read_options'].message_type = _READOPTIONS
_LOOKUPREQUEST.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._KEY
_LOOKUPRESPONSE.fields_by_name['found'].message_type = _ENTITYRESULT
_LOOKUPRESPONSE.fields_by_name['missing'].message_type = _ENTITYRESULT
_LOOKUPRESPONSE.fields_by_name['deferred'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._KEY
_RUNQUERYREQUEST.fields_by_name['read_options'].message_type = _READOPTIONS
_RUNQUERYREQUEST.fields_by_name['partition_id'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._PARTITIONID
_RUNQUERYREQUEST.fields_by_name['query'].message_type = _QUERY
_RUNQUERYREQUEST.fields_by_name['gql_query'].message_type = _GQLQUERY
_RUNQUERYRESPONSE.fields_by_name['batch'].message_type = _QUERYRESULTBATCH
_CONTINUEQUERYRESPONSE.fields_by_name['batch'].message_type = _QUERYRESULTBATCH
_COMMITREQUEST.fields_by_name['mutation'].message_type = _MUTATION
_COMMITREQUEST.fields_by_name['deprecated_mutation'].message_type = _DEPRECATEDMUTATION
_COMMITREQUEST.fields_by_name['mode'].enum_type = _COMMITREQUEST_MODE
_COMMITREQUEST_MODE.containing_type = _COMMITREQUEST
_COMMITRESPONSE.fields_by_name['mutation_result'].message_type = _MUTATIONRESULT
_COMMITRESPONSE.fields_by_name['deprecated_mutation_result'].message_type = _DEPRECATEDMUTATIONRESULT
_ALLOCATEIDSREQUEST.fields_by_name['allocate'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._KEY
_ALLOCATEIDSREQUEST.fields_by_name['reserve'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._KEY
_ALLOCATEIDSRESPONSE.fields_by_name['allocated'].message_type = google_dot_appengine_dot_datastore_dot_entity__v4__pb2._KEY
DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['EntityResult'] = _ENTITYRESULT
DESCRIPTOR.message_types_by_name['Query'] = _QUERY
DESCRIPTOR.message_types_by_name['KindExpression'] = _KINDEXPRESSION
DESCRIPTOR.message_types_by_name['PropertyReference'] = _PROPERTYREFERENCE
DESCRIPTOR.message_types_by_name['PropertyExpression'] = _PROPERTYEXPRESSION
DESCRIPTOR.message_types_by_name['PropertyOrder'] = _PROPERTYORDER
DESCRIPTOR.message_types_by_name['Filter'] = _FILTER
DESCRIPTOR.message_types_by_name['CompositeFilter'] = _COMPOSITEFILTER
DESCRIPTOR.message_types_by_name['PropertyFilter'] = _PROPERTYFILTER
DESCRIPTOR.message_types_by_name['GqlQuery'] = _GQLQUERY
DESCRIPTOR.message_types_by_name['GqlQueryArg'] = _GQLQUERYARG
DESCRIPTOR.message_types_by_name['QueryResultBatch'] = _QUERYRESULTBATCH
DESCRIPTOR.message_types_by_name['Mutation'] = _MUTATION
DESCRIPTOR.message_types_by_name['MutationResult'] = _MUTATIONRESULT
DESCRIPTOR.message_types_by_name['DeprecatedMutation'] = _DEPRECATEDMUTATION
DESCRIPTOR.message_types_by_name['DeprecatedMutationResult'] = _DEPRECATEDMUTATIONRESULT
DESCRIPTOR.message_types_by_name['ReadOptions'] = _READOPTIONS
DESCRIPTOR.message_types_by_name['LookupRequest'] = _LOOKUPREQUEST
DESCRIPTOR.message_types_by_name['LookupResponse'] = _LOOKUPRESPONSE
DESCRIPTOR.message_types_by_name['RunQueryRequest'] = _RUNQUERYREQUEST
DESCRIPTOR.message_types_by_name['RunQueryResponse'] = _RUNQUERYRESPONSE
DESCRIPTOR.message_types_by_name['ContinueQueryRequest'] = _CONTINUEQUERYREQUEST
DESCRIPTOR.message_types_by_name['ContinueQueryResponse'] = _CONTINUEQUERYRESPONSE
DESCRIPTOR.message_types_by_name['BeginTransactionRequest'] = _BEGINTRANSACTIONREQUEST
DESCRIPTOR.message_types_by_name['BeginTransactionResponse'] = _BEGINTRANSACTIONRESPONSE
DESCRIPTOR.message_types_by_name['RollbackRequest'] = _ROLLBACKREQUEST
DESCRIPTOR.message_types_by_name['RollbackResponse'] = _ROLLBACKRESPONSE
DESCRIPTOR.message_types_by_name['CommitRequest'] = _COMMITREQUEST
DESCRIPTOR.message_types_by_name['CommitResponse'] = _COMMITRESPONSE
DESCRIPTOR.message_types_by_name['AllocateIdsRequest'] = _ALLOCATEIDSREQUEST
DESCRIPTOR.message_types_by_name['AllocateIdsResponse'] = _ALLOCATEIDSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
  'DESCRIPTOR' : _ERROR,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(Error)

EntityResult = _reflection.GeneratedProtocolMessageType('EntityResult', (_message.Message,), {
  'DESCRIPTOR' : _ENTITYRESULT,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(EntityResult)

Query = _reflection.GeneratedProtocolMessageType('Query', (_message.Message,), {
  'DESCRIPTOR' : _QUERY,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(Query)

KindExpression = _reflection.GeneratedProtocolMessageType('KindExpression', (_message.Message,), {
  'DESCRIPTOR' : _KINDEXPRESSION,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(KindExpression)

PropertyReference = _reflection.GeneratedProtocolMessageType('PropertyReference', (_message.Message,), {
  'DESCRIPTOR' : _PROPERTYREFERENCE,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(PropertyReference)

PropertyExpression = _reflection.GeneratedProtocolMessageType('PropertyExpression', (_message.Message,), {
  'DESCRIPTOR' : _PROPERTYEXPRESSION,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(PropertyExpression)

PropertyOrder = _reflection.GeneratedProtocolMessageType('PropertyOrder', (_message.Message,), {
  'DESCRIPTOR' : _PROPERTYORDER,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(PropertyOrder)

Filter = _reflection.GeneratedProtocolMessageType('Filter', (_message.Message,), {
  'DESCRIPTOR' : _FILTER,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(Filter)

CompositeFilter = _reflection.GeneratedProtocolMessageType('CompositeFilter', (_message.Message,), {
  'DESCRIPTOR' : _COMPOSITEFILTER,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(CompositeFilter)

PropertyFilter = _reflection.GeneratedProtocolMessageType('PropertyFilter', (_message.Message,), {
  'DESCRIPTOR' : _PROPERTYFILTER,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(PropertyFilter)

GqlQuery = _reflection.GeneratedProtocolMessageType('GqlQuery', (_message.Message,), {
  'DESCRIPTOR' : _GQLQUERY,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(GqlQuery)

GqlQueryArg = _reflection.GeneratedProtocolMessageType('GqlQueryArg', (_message.Message,), {
  'DESCRIPTOR' : _GQLQUERYARG,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(GqlQueryArg)

QueryResultBatch = _reflection.GeneratedProtocolMessageType('QueryResultBatch', (_message.Message,), {
  'DESCRIPTOR' : _QUERYRESULTBATCH,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(QueryResultBatch)

Mutation = _reflection.GeneratedProtocolMessageType('Mutation', (_message.Message,), {
  'DESCRIPTOR' : _MUTATION,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(Mutation)

MutationResult = _reflection.GeneratedProtocolMessageType('MutationResult', (_message.Message,), {
  'DESCRIPTOR' : _MUTATIONRESULT,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(MutationResult)

DeprecatedMutation = _reflection.GeneratedProtocolMessageType('DeprecatedMutation', (_message.Message,), {
  'DESCRIPTOR' : _DEPRECATEDMUTATION,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(DeprecatedMutation)

DeprecatedMutationResult = _reflection.GeneratedProtocolMessageType('DeprecatedMutationResult', (_message.Message,), {
  'DESCRIPTOR' : _DEPRECATEDMUTATIONRESULT,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(DeprecatedMutationResult)

ReadOptions = _reflection.GeneratedProtocolMessageType('ReadOptions', (_message.Message,), {
  'DESCRIPTOR' : _READOPTIONS,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(ReadOptions)

LookupRequest = _reflection.GeneratedProtocolMessageType('LookupRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOOKUPREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(LookupRequest)

LookupResponse = _reflection.GeneratedProtocolMessageType('LookupResponse', (_message.Message,), {
  'DESCRIPTOR' : _LOOKUPRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(LookupResponse)

RunQueryRequest = _reflection.GeneratedProtocolMessageType('RunQueryRequest', (_message.Message,), {
  'DESCRIPTOR' : _RUNQUERYREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(RunQueryRequest)

RunQueryResponse = _reflection.GeneratedProtocolMessageType('RunQueryResponse', (_message.Message,), {
  'DESCRIPTOR' : _RUNQUERYRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(RunQueryResponse)

ContinueQueryRequest = _reflection.GeneratedProtocolMessageType('ContinueQueryRequest', (_message.Message,), {
  'DESCRIPTOR' : _CONTINUEQUERYREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(ContinueQueryRequest)

ContinueQueryResponse = _reflection.GeneratedProtocolMessageType('ContinueQueryResponse', (_message.Message,), {
  'DESCRIPTOR' : _CONTINUEQUERYRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(ContinueQueryResponse)

BeginTransactionRequest = _reflection.GeneratedProtocolMessageType('BeginTransactionRequest', (_message.Message,), {
  'DESCRIPTOR' : _BEGINTRANSACTIONREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(BeginTransactionRequest)

BeginTransactionResponse = _reflection.GeneratedProtocolMessageType('BeginTransactionResponse', (_message.Message,), {
  'DESCRIPTOR' : _BEGINTRANSACTIONRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(BeginTransactionResponse)

RollbackRequest = _reflection.GeneratedProtocolMessageType('RollbackRequest', (_message.Message,), {
  'DESCRIPTOR' : _ROLLBACKREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(RollbackRequest)

RollbackResponse = _reflection.GeneratedProtocolMessageType('RollbackResponse', (_message.Message,), {
  'DESCRIPTOR' : _ROLLBACKRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(RollbackResponse)

CommitRequest = _reflection.GeneratedProtocolMessageType('CommitRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMMITREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(CommitRequest)

CommitResponse = _reflection.GeneratedProtocolMessageType('CommitResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMMITRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(CommitResponse)

AllocateIdsRequest = _reflection.GeneratedProtocolMessageType('AllocateIdsRequest', (_message.Message,), {
  'DESCRIPTOR' : _ALLOCATEIDSREQUEST,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(AllocateIdsRequest)

AllocateIdsResponse = _reflection.GeneratedProtocolMessageType('AllocateIdsResponse', (_message.Message,), {
  'DESCRIPTOR' : _ALLOCATEIDSRESPONSE,
  '__module__' : 'google.appengine.datastore.datastore_v4_pb2'

  })
_sym_db.RegisterMessage(AllocateIdsResponse)


DESCRIPTOR._options = None

