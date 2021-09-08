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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'google/appengine/datastore/action.proto\x12\x13storage_onestore_v3\"\x93\x01\n\x06\x41\x63tion\x12>\n\x10transaction_data\x18\x02 \x01(\x0b\x32$.storage_onestore_v3.TransactionData\x12;\n\x0f\x61\x63tion_rpc_info\x18\x03 \x01(\x0b\x32\".storage_onestore_v3.ActionRpcInfo\x12\x0c\n\x04uuid\x18\x04 \x01(\t\"F\n\x0fTransactionData\x12\x0e\n\x06handle\x18\x01 \x01(\x06\x12\x0e\n\x06\x61pp_id\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x61tabase_id\x18\x03 \x01(\t\"Z\n\rActionRpcInfo\x12\x1f\n\x17\x65nqueuing_rpc_global_id\x18\x01 \x01(\x03\x12(\n enqueuing_rpc_start_timestamp_us\x18\x02 \x01(\x03\x42\x45\n\x1e\x63om.google.storage.onestore.v3B\x0eOnestoreActionZ\x13storage_onestore_v3')



_ACTION = DESCRIPTOR.message_types_by_name['Action']
_TRANSACTIONDATA = DESCRIPTOR.message_types_by_name['TransactionData']
_ACTIONRPCINFO = DESCRIPTOR.message_types_by_name['ActionRpcInfo']
Action = _reflection.GeneratedProtocolMessageType('Action', (_message.Message,), {
  'DESCRIPTOR' : _ACTION,
  '__module__' : 'google.appengine.datastore.action_pb2'

  })
_sym_db.RegisterMessage(Action)

TransactionData = _reflection.GeneratedProtocolMessageType('TransactionData', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTIONDATA,
  '__module__' : 'google.appengine.datastore.action_pb2'

  })
_sym_db.RegisterMessage(TransactionData)

ActionRpcInfo = _reflection.GeneratedProtocolMessageType('ActionRpcInfo', (_message.Message,), {
  'DESCRIPTOR' : _ACTIONRPCINFO,
  '__module__' : 'google.appengine.datastore.action_pb2'

  })
_sym_db.RegisterMessage(ActionRpcInfo)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.google.storage.onestore.v3B\016OnestoreActionZ\023storage_onestore_v3'
  _ACTION._serialized_start=65
  _ACTION._serialized_end=212
  _TRANSACTIONDATA._serialized_start=214
  _TRANSACTIONDATA._serialized_end=284
  _ACTIONRPCINFO._serialized_start=286
  _ACTIONRPCINFO._serialized_end=376

