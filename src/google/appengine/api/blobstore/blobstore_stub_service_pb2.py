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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;google/appengine/api/blobstore/blobstore_stub_service.proto\x12\x10google.appengine\x1a#google/appengine/api/api_base.proto\"5\n\x10StoreBlobRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"\x8f\x01\n\x19SetBlobStorageTypeRequest\x12M\n\x0cstorage_type\x18\x01 \x02(\x0e\x32\x37.google.appengine.SetBlobStorageTypeRequest.StorageType\"#\n\x0bStorageType\x12\n\n\x06MEMORY\x10\x00\x12\x08\n\x04\x46ILE\x10\x01\x42<\n\"com.google.appengine.api.blobstoreB\x16\x42lobstoreStubServicePb')



_STOREBLOBREQUEST = DESCRIPTOR.message_types_by_name['StoreBlobRequest']
_SETBLOBSTORAGETYPEREQUEST = DESCRIPTOR.message_types_by_name['SetBlobStorageTypeRequest']
_SETBLOBSTORAGETYPEREQUEST_STORAGETYPE = _SETBLOBSTORAGETYPEREQUEST.enum_types_by_name['StorageType']
StoreBlobRequest = _reflection.GeneratedProtocolMessageType('StoreBlobRequest', (_message.Message,), {
  'DESCRIPTOR' : _STOREBLOBREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_stub_service_pb2'

  })
_sym_db.RegisterMessage(StoreBlobRequest)

SetBlobStorageTypeRequest = _reflection.GeneratedProtocolMessageType('SetBlobStorageTypeRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETBLOBSTORAGETYPEREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_stub_service_pb2'

  })
_sym_db.RegisterMessage(SetBlobStorageTypeRequest)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\"com.google.appengine.api.blobstoreB\026BlobstoreStubServicePb'
  _STOREBLOBREQUEST._serialized_start=118
  _STOREBLOBREQUEST._serialized_end=171
  _SETBLOBSTORAGETYPEREQUEST._serialized_start=174
  _SETBLOBSTORAGETYPEREQUEST._serialized_end=317
  _SETBLOBSTORAGETYPEREQUEST_STORAGETYPE._serialized_start=282
  _SETBLOBSTORAGETYPEREQUEST_STORAGETYPE._serialized_end=317

