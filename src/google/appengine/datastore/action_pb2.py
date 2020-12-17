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




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/datastore/action.proto',
  package='storage_onestore_v3',
  syntax='proto2',
  serialized_options=b'\n\036com.google.storage.onestore.v3B\016OnestoreActionZ\023storage_onestore_v3',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\'google/appengine/datastore/action.proto\x12\x13storage_onestore_v3\"\x93\x01\n\x06\x41\x63tion\x12>\n\x10transaction_data\x18\x02 \x01(\x0b\x32$.storage_onestore_v3.TransactionData\x12;\n\x0f\x61\x63tion_rpc_info\x18\x03 \x01(\x0b\x32\".storage_onestore_v3.ActionRpcInfo\x12\x0c\n\x04uuid\x18\x04 \x01(\t\"F\n\x0fTransactionData\x12\x0e\n\x06handle\x18\x01 \x01(\x06\x12\x0e\n\x06\x61pp_id\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x61tabase_id\x18\x03 \x01(\t\"Z\n\rActionRpcInfo\x12\x1f\n\x17\x65nqueuing_rpc_global_id\x18\x01 \x01(\x03\x12(\n enqueuing_rpc_start_timestamp_us\x18\x02 \x01(\x03\x42\x45\n\x1e\x63om.google.storage.onestore.v3B\x0eOnestoreActionZ\x13storage_onestore_v3'
)




_ACTION = _descriptor.Descriptor(
  name='Action',
  full_name='storage_onestore_v3.Action',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='transaction_data', full_name='storage_onestore_v3.Action.transaction_data', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='action_rpc_info', full_name='storage_onestore_v3.Action.action_rpc_info', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uuid', full_name='storage_onestore_v3.Action.uuid', index=2,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=65,
  serialized_end=212,
)


_TRANSACTIONDATA = _descriptor.Descriptor(
  name='TransactionData',
  full_name='storage_onestore_v3.TransactionData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='handle', full_name='storage_onestore_v3.TransactionData.handle', index=0,
      number=1, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='app_id', full_name='storage_onestore_v3.TransactionData.app_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='database_id', full_name='storage_onestore_v3.TransactionData.database_id', index=2,
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
  serialized_start=214,
  serialized_end=284,
)


_ACTIONRPCINFO = _descriptor.Descriptor(
  name='ActionRpcInfo',
  full_name='storage_onestore_v3.ActionRpcInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='enqueuing_rpc_global_id', full_name='storage_onestore_v3.ActionRpcInfo.enqueuing_rpc_global_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enqueuing_rpc_start_timestamp_us', full_name='storage_onestore_v3.ActionRpcInfo.enqueuing_rpc_start_timestamp_us', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  serialized_start=286,
  serialized_end=376,
)

_ACTION.fields_by_name['transaction_data'].message_type = _TRANSACTIONDATA
_ACTION.fields_by_name['action_rpc_info'].message_type = _ACTIONRPCINFO
DESCRIPTOR.message_types_by_name['Action'] = _ACTION
DESCRIPTOR.message_types_by_name['TransactionData'] = _TRANSACTIONDATA
DESCRIPTOR.message_types_by_name['ActionRpcInfo'] = _ACTIONRPCINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

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


DESCRIPTOR._options = None

