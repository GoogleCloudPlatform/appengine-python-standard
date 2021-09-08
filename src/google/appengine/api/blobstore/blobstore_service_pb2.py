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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6google/appengine/api/blobstore/blobstore_service.proto\x12\x10google.appengine\"\xeb\x01\n\x15\x42lobstoreServiceError\"\xd1\x01\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x12\n\x0eINTERNAL_ERROR\x10\x01\x12\x10\n\x0cURL_TOO_LONG\x10\x02\x12\x15\n\x11PERMISSION_DENIED\x10\x03\x12\x12\n\x0e\x42LOB_NOT_FOUND\x10\x04\x12\x1b\n\x17\x44\x41TA_INDEX_OUT_OF_RANGE\x10\x05\x12\x1d\n\x19\x42LOB_FETCH_SIZE_TOO_LARGE\x10\x06\x12\x19\n\x15\x41RGUMENT_OUT_OF_RANGE\x10\x08\x12\x14\n\x10INVALID_BLOB_KEY\x10\t\"\xae\x01\n\x16\x43reateUploadURLRequest\x12\x14\n\x0csuccess_path\x18\x01 \x02(\t\x12\x1d\n\x15max_upload_size_bytes\x18\x02 \x01(\x03\x12&\n\x1emax_upload_size_per_blob_bytes\x18\x03 \x01(\x03\x12\x16\n\x0egs_bucket_name\x18\x04 \x01(\t\x12\x1f\n\x17url_expiry_time_seconds\x18\x05 \x01(\x05\"&\n\x17\x43reateUploadURLResponse\x12\x0b\n\x03url\x18\x01 \x02(\t\"4\n\x11\x44\x65leteBlobRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x03(\t\x12\r\n\x05token\x18\x02 \x01(\t\"L\n\x10\x46\x65tchDataRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\t\x12\x13\n\x0bstart_index\x18\x02 \x02(\x03\x12\x11\n\tend_index\x18\x03 \x02(\x03\"&\n\x11\x46\x65tchDataResponse\x12\x11\n\x04\x64\x61ta\x18\xe8\x07 \x02(\x0c\x42\x02\x08\x01\"N\n\x10\x43loneBlobRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\x0c\x12\x11\n\tmime_type\x18\x02 \x02(\x0c\x12\x15\n\rtarget_app_id\x18\x03 \x02(\x0c\"%\n\x11\x43loneBlobResponse\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\x0c\"(\n\x14\x44\x65\x63odeBlobKeyRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x03(\t\"(\n\x15\x44\x65\x63odeBlobKeyResponse\x12\x0f\n\x07\x64\x65\x63oded\x18\x01 \x03(\t\"8\n$CreateEncodedGoogleStorageKeyRequest\x12\x10\n\x08\x66ilename\x18\x01 \x02(\t\"9\n%CreateEncodedGoogleStorageKeyResponse\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\tB8\n\"com.google.appengine.api.blobstoreB\x12\x42lobstoreServicePb')



_BLOBSTORESERVICEERROR = DESCRIPTOR.message_types_by_name['BlobstoreServiceError']
_CREATEUPLOADURLREQUEST = DESCRIPTOR.message_types_by_name['CreateUploadURLRequest']
_CREATEUPLOADURLRESPONSE = DESCRIPTOR.message_types_by_name['CreateUploadURLResponse']
_DELETEBLOBREQUEST = DESCRIPTOR.message_types_by_name['DeleteBlobRequest']
_FETCHDATAREQUEST = DESCRIPTOR.message_types_by_name['FetchDataRequest']
_FETCHDATARESPONSE = DESCRIPTOR.message_types_by_name['FetchDataResponse']
_CLONEBLOBREQUEST = DESCRIPTOR.message_types_by_name['CloneBlobRequest']
_CLONEBLOBRESPONSE = DESCRIPTOR.message_types_by_name['CloneBlobResponse']
_DECODEBLOBKEYREQUEST = DESCRIPTOR.message_types_by_name['DecodeBlobKeyRequest']
_DECODEBLOBKEYRESPONSE = DESCRIPTOR.message_types_by_name['DecodeBlobKeyResponse']
_CREATEENCODEDGOOGLESTORAGEKEYREQUEST = DESCRIPTOR.message_types_by_name['CreateEncodedGoogleStorageKeyRequest']
_CREATEENCODEDGOOGLESTORAGEKEYRESPONSE = DESCRIPTOR.message_types_by_name['CreateEncodedGoogleStorageKeyResponse']
_BLOBSTORESERVICEERROR_ERRORCODE = _BLOBSTORESERVICEERROR.enum_types_by_name['ErrorCode']
BlobstoreServiceError = _reflection.GeneratedProtocolMessageType('BlobstoreServiceError', (_message.Message,), {
  'DESCRIPTOR' : _BLOBSTORESERVICEERROR,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(BlobstoreServiceError)

CreateUploadURLRequest = _reflection.GeneratedProtocolMessageType('CreateUploadURLRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUPLOADURLREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CreateUploadURLRequest)

CreateUploadURLResponse = _reflection.GeneratedProtocolMessageType('CreateUploadURLResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUPLOADURLRESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CreateUploadURLResponse)

DeleteBlobRequest = _reflection.GeneratedProtocolMessageType('DeleteBlobRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEBLOBREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(DeleteBlobRequest)

FetchDataRequest = _reflection.GeneratedProtocolMessageType('FetchDataRequest', (_message.Message,), {
  'DESCRIPTOR' : _FETCHDATAREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(FetchDataRequest)

FetchDataResponse = _reflection.GeneratedProtocolMessageType('FetchDataResponse', (_message.Message,), {
  'DESCRIPTOR' : _FETCHDATARESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(FetchDataResponse)

CloneBlobRequest = _reflection.GeneratedProtocolMessageType('CloneBlobRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLONEBLOBREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CloneBlobRequest)

CloneBlobResponse = _reflection.GeneratedProtocolMessageType('CloneBlobResponse', (_message.Message,), {
  'DESCRIPTOR' : _CLONEBLOBRESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CloneBlobResponse)

DecodeBlobKeyRequest = _reflection.GeneratedProtocolMessageType('DecodeBlobKeyRequest', (_message.Message,), {
  'DESCRIPTOR' : _DECODEBLOBKEYREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(DecodeBlobKeyRequest)

DecodeBlobKeyResponse = _reflection.GeneratedProtocolMessageType('DecodeBlobKeyResponse', (_message.Message,), {
  'DESCRIPTOR' : _DECODEBLOBKEYRESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(DecodeBlobKeyResponse)

CreateEncodedGoogleStorageKeyRequest = _reflection.GeneratedProtocolMessageType('CreateEncodedGoogleStorageKeyRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEENCODEDGOOGLESTORAGEKEYREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CreateEncodedGoogleStorageKeyRequest)

CreateEncodedGoogleStorageKeyResponse = _reflection.GeneratedProtocolMessageType('CreateEncodedGoogleStorageKeyResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEENCODEDGOOGLESTORAGEKEYRESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CreateEncodedGoogleStorageKeyResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\"com.google.appengine.api.blobstoreB\022BlobstoreServicePb'
  _FETCHDATARESPONSE.fields_by_name['data']._options = None
  _FETCHDATARESPONSE.fields_by_name['data']._serialized_options = b'\010\001'
  _BLOBSTORESERVICEERROR._serialized_start=77
  _BLOBSTORESERVICEERROR._serialized_end=312
  _BLOBSTORESERVICEERROR_ERRORCODE._serialized_start=103
  _BLOBSTORESERVICEERROR_ERRORCODE._serialized_end=312
  _CREATEUPLOADURLREQUEST._serialized_start=315
  _CREATEUPLOADURLREQUEST._serialized_end=489
  _CREATEUPLOADURLRESPONSE._serialized_start=491
  _CREATEUPLOADURLRESPONSE._serialized_end=529
  _DELETEBLOBREQUEST._serialized_start=531
  _DELETEBLOBREQUEST._serialized_end=583
  _FETCHDATAREQUEST._serialized_start=585
  _FETCHDATAREQUEST._serialized_end=661
  _FETCHDATARESPONSE._serialized_start=663
  _FETCHDATARESPONSE._serialized_end=701
  _CLONEBLOBREQUEST._serialized_start=703
  _CLONEBLOBREQUEST._serialized_end=781
  _CLONEBLOBRESPONSE._serialized_start=783
  _CLONEBLOBRESPONSE._serialized_end=820
  _DECODEBLOBKEYREQUEST._serialized_start=822
  _DECODEBLOBKEYREQUEST._serialized_end=862
  _DECODEBLOBKEYRESPONSE._serialized_start=864
  _DECODEBLOBKEYRESPONSE._serialized_end=904
  _CREATEENCODEDGOOGLESTORAGEKEYREQUEST._serialized_start=906
  _CREATEENCODEDGOOGLESTORAGEKEYREQUEST._serialized_end=962
  _CREATEENCODEDGOOGLESTORAGEKEYRESPONSE._serialized_start=964
  _CREATEENCODEDGOOGLESTORAGEKEYRESPONSE._serialized_end=1021

