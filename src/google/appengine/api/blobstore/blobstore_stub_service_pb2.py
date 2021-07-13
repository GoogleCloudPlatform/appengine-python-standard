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


from google.appengine.api import api_base_pb2 as google_dot_appengine_dot_api_dot_api__base__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/api/blobstore/blobstore_stub_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n\"com.google.appengine.api.blobstoreB\026BlobstoreStubServicePb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n;google/appengine/api/blobstore/blobstore_stub_service.proto\x12\x10google.appengine\x1a#google/appengine/api/api_base.proto\"5\n\x10StoreBlobRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"\x8f\x01\n\x19SetBlobStorageTypeRequest\x12M\n\x0cstorage_type\x18\x01 \x02(\x0e\x32\x37.google.appengine.SetBlobStorageTypeRequest.StorageType\"#\n\x0bStorageType\x12\n\n\x06MEMORY\x10\x00\x12\x08\n\x04\x46ILE\x10\x01\x42<\n\"com.google.appengine.api.blobstoreB\x16\x42lobstoreStubServicePb'
  ,
  dependencies=[google_dot_appengine_dot_api_dot_api__base__pb2.DESCRIPTOR,])



_SETBLOBSTORAGETYPEREQUEST_STORAGETYPE = _descriptor.EnumDescriptor(
  name='StorageType',
  full_name='google.appengine.SetBlobStorageTypeRequest.StorageType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MEMORY', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FILE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=282,
  serialized_end=317,
)
_sym_db.RegisterEnumDescriptor(_SETBLOBSTORAGETYPEREQUEST_STORAGETYPE)


_STOREBLOBREQUEST = _descriptor.Descriptor(
  name='StoreBlobRequest',
  full_name='google.appengine.StoreBlobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='google.appengine.StoreBlobRequest.blob_key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content', full_name='google.appengine.StoreBlobRequest.content', index=1,
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
  serialized_start=118,
  serialized_end=171,
)


_SETBLOBSTORAGETYPEREQUEST = _descriptor.Descriptor(
  name='SetBlobStorageTypeRequest',
  full_name='google.appengine.SetBlobStorageTypeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='storage_type', full_name='google.appengine.SetBlobStorageTypeRequest.storage_type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SETBLOBSTORAGETYPEREQUEST_STORAGETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=174,
  serialized_end=317,
)

_SETBLOBSTORAGETYPEREQUEST.fields_by_name['storage_type'].enum_type = _SETBLOBSTORAGETYPEREQUEST_STORAGETYPE
_SETBLOBSTORAGETYPEREQUEST_STORAGETYPE.containing_type = _SETBLOBSTORAGETYPEREQUEST
DESCRIPTOR.message_types_by_name['StoreBlobRequest'] = _STOREBLOBREQUEST
DESCRIPTOR.message_types_by_name['SetBlobStorageTypeRequest'] = _SETBLOBSTORAGETYPEREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

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


DESCRIPTOR._options = None

