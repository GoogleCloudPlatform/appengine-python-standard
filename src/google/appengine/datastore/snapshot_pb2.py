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
  name='google/appengine/datastore/snapshot.proto',
  package='storage_onestore_v3',
  syntax='proto2',
  serialized_options=b'\n\036com.google.storage.onestore.v3B\020OnestoreSnapshotZ\023storage_onestore_v3',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n)google/appengine/datastore/snapshot.proto\x12\x13storage_onestore_v3\":\n\x08Snapshot\x12\n\n\x02ts\x18\x01 \x02(\x03\"\"\n\x06Status\x12\x0c\n\x08INACTIVE\x10\x00\x12\n\n\x06\x41\x43TIVE\x10\x01\x42G\n\x1e\x63om.google.storage.onestore.v3B\x10OnestoreSnapshotZ\x13storage_onestore_v3'
)



_SNAPSHOT_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='storage_onestore_v3.Snapshot.Status',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INACTIVE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ACTIVE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=90,
  serialized_end=124,
)
_sym_db.RegisterEnumDescriptor(_SNAPSHOT_STATUS)


_SNAPSHOT = _descriptor.Descriptor(
  name='Snapshot',
  full_name='storage_onestore_v3.Snapshot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ts', full_name='storage_onestore_v3.Snapshot.ts', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SNAPSHOT_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=66,
  serialized_end=124,
)

_SNAPSHOT_STATUS.containing_type = _SNAPSHOT
DESCRIPTOR.message_types_by_name['Snapshot'] = _SNAPSHOT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Snapshot = _reflection.GeneratedProtocolMessageType('Snapshot', (_message.Message,), {
  'DESCRIPTOR' : _SNAPSHOT,
  '__module__' : 'google.appengine.datastore.snapshot_pb2'

  })
_sym_db.RegisterMessage(Snapshot)


DESCRIPTOR._options = None

