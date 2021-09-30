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


from google.appengine.datastore import datastore_v3_bytes_pb2 as google_dot_appengine_dot_datastore_dot_datastore__v3__bytes__pb2
from google.appengine.datastore import entity_bytes_pb2 as google_dot_appengine_dot_datastore_dot_entity__bytes__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/ext/remote_api/remote_api_bytes.proto',
  package='google.appengine.ext.remote_api_bytes',
  syntax='proto2',
  serialized_options=b'\n+com.google.google.appengine.utils.remoteapiB\013RemoteApiPbZ\nremote_api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n6google/appengine/ext/remote_api/remote_api_bytes.proto\x12%google.appengine.ext.remote_api_bytes\x1a\x33google/appengine/datastore/datastore_v3_bytes.proto\x1a-google/appengine/datastore/entity_bytes.proto\"k\n\x07Request\x12\x14\n\x0cservice_name\x18\x02 \x02(\t\x12\x0e\n\x06method\x18\x03 \x02(\t\x12\x0f\n\x07request\x18\x04 \x02(\x0c\x12\x12\n\nrequest_id\x18\x05 \x01(\t\x12\x15\n\rtrace_context\x18\x06 \x01(\x0c\"0\n\x10\x41pplicationError\x12\x0c\n\x04\x63ode\x18\x01 \x02(\x05\x12\x0e\n\x06\x64\x65tail\x18\x02 \x02(\t\"\xb7\x02\n\x08RpcError\x12\x0c\n\x04\x63ode\x18\x01 \x02(\x05\x12\x0e\n\x06\x64\x65tail\x18\x02 \x01(\t\"\x8c\x02\n\tErrorCode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x12\n\x0e\x43\x41LL_NOT_FOUND\x10\x01\x12\x0f\n\x0bPARSE_ERROR\x10\x02\x12\x16\n\x12SECURITY_VIOLATION\x10\x03\x12\x0e\n\nOVER_QUOTA\x10\x04\x12\x15\n\x11REQUEST_TOO_LARGE\x10\x05\x12\x17\n\x13\x43\x41PABILITY_DISABLED\x10\x06\x12\x14\n\x10\x46\x45\x41TURE_DISABLED\x10\x07\x12\x0f\n\x0b\x42\x41\x44_REQUEST\x10\x08\x12\x16\n\x12RESPONSE_TOO_LARGE\x10\t\x12\r\n\tCANCELLED\x10\n\x12\x10\n\x0cREPLAY_ERROR\x10\x0b\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x0c\"\xdf\x01\n\x08Response\x12\x10\n\x08response\x18\x01 \x01(\x0c\x12\x11\n\texception\x18\x02 \x01(\x0c\x12R\n\x11\x61pplication_error\x18\x03 \x01(\x0b\x32\x37.google.appengine.ext.remote_api_bytes.ApplicationError\x12\x16\n\x0ejava_exception\x18\x04 \x01(\x0c\x12\x42\n\trpc_error\x18\x05 \x01(\x0b\x32/.google.appengine.ext.remote_api_bytes.RpcError\"\xd6\x02\n\x12TransactionRequest\x12\\\n\x0cprecondition\x18\x01 \x03(\n2F.google.appengine.ext.remote_api_bytes.TransactionRequest.Precondition\x12\x37\n\x04puts\x18\x04 \x01(\x0b\x32).apphosting_datastore_v3_bytes.PutRequest\x12=\n\x07\x64\x65letes\x18\x05 \x01(\x0b\x32,.apphosting_datastore_v3_bytes.DeleteRequest\x12\x19\n\x11\x61llow_multiple_eg\x18\x06 \x01(\x08\x1aO\n\x0cPrecondition\x12\x31\n\x03key\x18\x02 \x02(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x0c\n\x04hash\x18\x03 \x01(\x0c\"\xd2\x01\n\x16TransactionQueryResult\x12:\n\x06result\x18\x01 \x02(\x0b\x32*.apphosting_datastore_v3_bytes.QueryResult\x12>\n\x10\x65ntity_group_key\x18\x02 \x02(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12<\n\x0c\x65ntity_group\x18\x03 \x01(\x0b\x32&.storage_onestore_v3_bytes.EntityProtoBF\n+com.google.google.appengine.utils.remoteapiB\x0bRemoteApiPbZ\nremote_api'
  ,
  dependencies=[google_dot_appengine_dot_datastore_dot_datastore__v3__bytes__pb2.DESCRIPTOR,google_dot_appengine_dot_datastore_dot_entity__bytes__pb2.DESCRIPTOR,])



_RPCERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.ext.remote_api_bytes.RpcError.ErrorCode',
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
      name='CALL_NOT_FOUND', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PARSE_ERROR', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SECURITY_VIOLATION', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OVER_QUOTA', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REQUEST_TOO_LARGE', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CAPABILITY_DISABLED', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_DISABLED', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BAD_REQUEST', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESPONSE_TOO_LARGE', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CANCELLED', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='REPLAY_ERROR', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DEADLINE_EXCEEDED', index=12, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=400,
  serialized_end=668,
)
_sym_db.RegisterEnumDescriptor(_RPCERROR_ERRORCODE)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='google.appengine.ext.remote_api_bytes.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='service_name', full_name='google.appengine.ext.remote_api_bytes.Request.service_name', index=0,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='method', full_name='google.appengine.ext.remote_api_bytes.Request.method', index=1,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request', full_name='google.appengine.ext.remote_api_bytes.Request.request', index=2,
      number=4, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_id', full_name='google.appengine.ext.remote_api_bytes.Request.request_id', index=3,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='trace_context', full_name='google.appengine.ext.remote_api_bytes.Request.trace_context', index=4,
      number=6, type=12, cpp_type=9, label=1,
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
  serialized_start=197,
  serialized_end=304,
)


_APPLICATIONERROR = _descriptor.Descriptor(
  name='ApplicationError',
  full_name='google.appengine.ext.remote_api_bytes.ApplicationError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='google.appengine.ext.remote_api_bytes.ApplicationError.code', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detail', full_name='google.appengine.ext.remote_api_bytes.ApplicationError.detail', index=1,
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
  serialized_start=306,
  serialized_end=354,
)


_RPCERROR = _descriptor.Descriptor(
  name='RpcError',
  full_name='google.appengine.ext.remote_api_bytes.RpcError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='google.appengine.ext.remote_api_bytes.RpcError.code', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detail', full_name='google.appengine.ext.remote_api_bytes.RpcError.detail', index=1,
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
    _RPCERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=357,
  serialized_end=668,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='google.appengine.ext.remote_api_bytes.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='google.appengine.ext.remote_api_bytes.Response.response', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='exception', full_name='google.appengine.ext.remote_api_bytes.Response.exception', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='application_error', full_name='google.appengine.ext.remote_api_bytes.Response.application_error', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='java_exception', full_name='google.appengine.ext.remote_api_bytes.Response.java_exception', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rpc_error', full_name='google.appengine.ext.remote_api_bytes.Response.rpc_error', index=4,
      number=5, type=11, cpp_type=10, label=1,
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
  serialized_start=671,
  serialized_end=894,
)


_TRANSACTIONREQUEST_PRECONDITION = _descriptor.Descriptor(
  name='Precondition',
  full_name='google.appengine.ext.remote_api_bytes.TransactionRequest.Precondition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='google.appengine.ext.remote_api_bytes.TransactionRequest.Precondition.key', index=0,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hash', full_name='google.appengine.ext.remote_api_bytes.TransactionRequest.Precondition.hash', index=1,
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
  serialized_start=1160,
  serialized_end=1239,
)

_TRANSACTIONREQUEST = _descriptor.Descriptor(
  name='TransactionRequest',
  full_name='google.appengine.ext.remote_api_bytes.TransactionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='precondition', full_name='google.appengine.ext.remote_api_bytes.TransactionRequest.precondition', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='puts', full_name='google.appengine.ext.remote_api_bytes.TransactionRequest.puts', index=1,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deletes', full_name='google.appengine.ext.remote_api_bytes.TransactionRequest.deletes', index=2,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='allow_multiple_eg', full_name='google.appengine.ext.remote_api_bytes.TransactionRequest.allow_multiple_eg', index=3,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TRANSACTIONREQUEST_PRECONDITION, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=897,
  serialized_end=1239,
)


_TRANSACTIONQUERYRESULT = _descriptor.Descriptor(
  name='TransactionQueryResult',
  full_name='google.appengine.ext.remote_api_bytes.TransactionQueryResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='google.appengine.ext.remote_api_bytes.TransactionQueryResult.result', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_group_key', full_name='google.appengine.ext.remote_api_bytes.TransactionQueryResult.entity_group_key', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_group', full_name='google.appengine.ext.remote_api_bytes.TransactionQueryResult.entity_group', index=2,
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
  serialized_start=1242,
  serialized_end=1452,
)

_RPCERROR_ERRORCODE.containing_type = _RPCERROR
_RESPONSE.fields_by_name['application_error'].message_type = _APPLICATIONERROR
_RESPONSE.fields_by_name['rpc_error'].message_type = _RPCERROR
_TRANSACTIONREQUEST_PRECONDITION.fields_by_name['key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_TRANSACTIONREQUEST_PRECONDITION.containing_type = _TRANSACTIONREQUEST
_TRANSACTIONREQUEST.fields_by_name['precondition'].message_type = _TRANSACTIONREQUEST_PRECONDITION
_TRANSACTIONREQUEST.fields_by_name['puts'].message_type = google_dot_appengine_dot_datastore_dot_datastore__v3__bytes__pb2._PUTREQUEST
_TRANSACTIONREQUEST.fields_by_name['deletes'].message_type = google_dot_appengine_dot_datastore_dot_datastore__v3__bytes__pb2._DELETEREQUEST
_TRANSACTIONQUERYRESULT.fields_by_name['result'].message_type = google_dot_appengine_dot_datastore_dot_datastore__v3__bytes__pb2._QUERYRESULT
_TRANSACTIONQUERYRESULT.fields_by_name['entity_group_key'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._REFERENCE
_TRANSACTIONQUERYRESULT.fields_by_name['entity_group'].message_type = google_dot_appengine_dot_datastore_dot_entity__bytes__pb2._ENTITYPROTO
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['ApplicationError'] = _APPLICATIONERROR
DESCRIPTOR.message_types_by_name['RpcError'] = _RPCERROR
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
DESCRIPTOR.message_types_by_name['TransactionRequest'] = _TRANSACTIONREQUEST
DESCRIPTOR.message_types_by_name['TransactionQueryResult'] = _TRANSACTIONQUERYRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'google.appengine.ext.remote_api.remote_api_bytes_pb2'

  })
_sym_db.RegisterMessage(Request)

ApplicationError = _reflection.GeneratedProtocolMessageType('ApplicationError', (_message.Message,), {
  'DESCRIPTOR' : _APPLICATIONERROR,
  '__module__' : 'google.appengine.ext.remote_api.remote_api_bytes_pb2'

  })
_sym_db.RegisterMessage(ApplicationError)

RpcError = _reflection.GeneratedProtocolMessageType('RpcError', (_message.Message,), {
  'DESCRIPTOR' : _RPCERROR,
  '__module__' : 'google.appengine.ext.remote_api.remote_api_bytes_pb2'

  })
_sym_db.RegisterMessage(RpcError)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'google.appengine.ext.remote_api.remote_api_bytes_pb2'

  })
_sym_db.RegisterMessage(Response)

TransactionRequest = _reflection.GeneratedProtocolMessageType('TransactionRequest', (_message.Message,), {

  'Precondition' : _reflection.GeneratedProtocolMessageType('Precondition', (_message.Message,), {
    'DESCRIPTOR' : _TRANSACTIONREQUEST_PRECONDITION,
    '__module__' : 'google.appengine.ext.remote_api.remote_api_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _TRANSACTIONREQUEST,
  '__module__' : 'google.appengine.ext.remote_api.remote_api_bytes_pb2'

  })
_sym_db.RegisterMessage(TransactionRequest)
_sym_db.RegisterMessage(TransactionRequest.Precondition)

TransactionQueryResult = _reflection.GeneratedProtocolMessageType('TransactionQueryResult', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTIONQUERYRESULT,
  '__module__' : 'google.appengine.ext.remote_api.remote_api_bytes_pb2'

  })
_sym_db.RegisterMessage(TransactionQueryResult)


DESCRIPTOR._options = None

