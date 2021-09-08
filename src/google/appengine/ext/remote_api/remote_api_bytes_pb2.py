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


from google.appengine.datastore import datastore_v3_bytes_pb2 as google_dot_appengine_dot_datastore_dot_datastore__v3__bytes__pb2
from google.appengine.datastore import entity_bytes_pb2 as google_dot_appengine_dot_datastore_dot_entity__bytes__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6google/appengine/ext/remote_api/remote_api_bytes.proto\x12%google.appengine.ext.remote_api_bytes\x1a\x33google/appengine/datastore/datastore_v3_bytes.proto\x1a-google/appengine/datastore/entity_bytes.proto\"k\n\x07Request\x12\x14\n\x0cservice_name\x18\x02 \x02(\t\x12\x0e\n\x06method\x18\x03 \x02(\t\x12\x0f\n\x07request\x18\x04 \x02(\x0c\x12\x12\n\nrequest_id\x18\x05 \x01(\t\x12\x15\n\rtrace_context\x18\x06 \x01(\x0c\"0\n\x10\x41pplicationError\x12\x0c\n\x04\x63ode\x18\x01 \x02(\x05\x12\x0e\n\x06\x64\x65tail\x18\x02 \x02(\t\"\xb7\x02\n\x08RpcError\x12\x0c\n\x04\x63ode\x18\x01 \x02(\x05\x12\x0e\n\x06\x64\x65tail\x18\x02 \x01(\t\"\x8c\x02\n\tErrorCode\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x12\n\x0e\x43\x41LL_NOT_FOUND\x10\x01\x12\x0f\n\x0bPARSE_ERROR\x10\x02\x12\x16\n\x12SECURITY_VIOLATION\x10\x03\x12\x0e\n\nOVER_QUOTA\x10\x04\x12\x15\n\x11REQUEST_TOO_LARGE\x10\x05\x12\x17\n\x13\x43\x41PABILITY_DISABLED\x10\x06\x12\x14\n\x10\x46\x45\x41TURE_DISABLED\x10\x07\x12\x0f\n\x0b\x42\x41\x44_REQUEST\x10\x08\x12\x16\n\x12RESPONSE_TOO_LARGE\x10\t\x12\r\n\tCANCELLED\x10\n\x12\x10\n\x0cREPLAY_ERROR\x10\x0b\x12\x15\n\x11\x44\x45\x41\x44LINE_EXCEEDED\x10\x0c\"\xdf\x01\n\x08Response\x12\x10\n\x08response\x18\x01 \x01(\x0c\x12\x11\n\texception\x18\x02 \x01(\x0c\x12R\n\x11\x61pplication_error\x18\x03 \x01(\x0b\x32\x37.google.appengine.ext.remote_api_bytes.ApplicationError\x12\x16\n\x0ejava_exception\x18\x04 \x01(\x0c\x12\x42\n\trpc_error\x18\x05 \x01(\x0b\x32/.google.appengine.ext.remote_api_bytes.RpcError\"\xd6\x02\n\x12TransactionRequest\x12\\\n\x0cprecondition\x18\x01 \x03(\n2F.google.appengine.ext.remote_api_bytes.TransactionRequest.Precondition\x12\x37\n\x04puts\x18\x04 \x01(\x0b\x32).apphosting_datastore_v3_bytes.PutRequest\x12=\n\x07\x64\x65letes\x18\x05 \x01(\x0b\x32,.apphosting_datastore_v3_bytes.DeleteRequest\x12\x19\n\x11\x61llow_multiple_eg\x18\x06 \x01(\x08\x1aO\n\x0cPrecondition\x12\x31\n\x03key\x18\x02 \x02(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x0c\n\x04hash\x18\x03 \x01(\x0c\"\xd2\x01\n\x16TransactionQueryResult\x12:\n\x06result\x18\x01 \x02(\x0b\x32*.apphosting_datastore_v3_bytes.QueryResult\x12>\n\x10\x65ntity_group_key\x18\x02 \x02(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12<\n\x0c\x65ntity_group\x18\x03 \x01(\x0b\x32&.storage_onestore_v3_bytes.EntityProtoBF\n+com.google.google.appengine.utils.remoteapiB\x0bRemoteApiPbZ\nremote_api')



_REQUEST = DESCRIPTOR.message_types_by_name['Request']
_APPLICATIONERROR = DESCRIPTOR.message_types_by_name['ApplicationError']
_RPCERROR = DESCRIPTOR.message_types_by_name['RpcError']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
_TRANSACTIONREQUEST = DESCRIPTOR.message_types_by_name['TransactionRequest']
_TRANSACTIONREQUEST_PRECONDITION = _TRANSACTIONREQUEST.nested_types_by_name['Precondition']
_TRANSACTIONQUERYRESULT = DESCRIPTOR.message_types_by_name['TransactionQueryResult']
_RPCERROR_ERRORCODE = _RPCERROR.enum_types_by_name['ErrorCode']
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

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n+com.google.google.appengine.utils.remoteapiB\013RemoteApiPbZ\nremote_api'
  _REQUEST._serialized_start=197
  _REQUEST._serialized_end=304
  _APPLICATIONERROR._serialized_start=306
  _APPLICATIONERROR._serialized_end=354
  _RPCERROR._serialized_start=357
  _RPCERROR._serialized_end=668
  _RPCERROR_ERRORCODE._serialized_start=400
  _RPCERROR_ERRORCODE._serialized_end=668
  _RESPONSE._serialized_start=671
  _RESPONSE._serialized_end=894
  _TRANSACTIONREQUEST._serialized_start=897
  _TRANSACTIONREQUEST._serialized_end=1239
  _TRANSACTIONREQUEST_PRECONDITION._serialized_start=1160
  _TRANSACTIONREQUEST_PRECONDITION._serialized_end=1239
  _TRANSACTIONQUERYRESULT._serialized_start=1242
  _TRANSACTIONQUERYRESULT._serialized_end=1452

