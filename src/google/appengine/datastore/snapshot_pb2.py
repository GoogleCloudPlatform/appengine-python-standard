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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)google/appengine/datastore/snapshot.proto\x12\x13storage_onestore_v3\":\n\x08Snapshot\x12\n\n\x02ts\x18\x01 \x02(\x03\"\"\n\x06Status\x12\x0c\n\x08INACTIVE\x10\x00\x12\n\n\x06\x41\x43TIVE\x10\x01\x42G\n\x1e\x63om.google.storage.onestore.v3B\x10OnestoreSnapshotZ\x13storage_onestore_v3')



_SNAPSHOT = DESCRIPTOR.message_types_by_name['Snapshot']
_SNAPSHOT_STATUS = _SNAPSHOT.enum_types_by_name['Status']
Snapshot = _reflection.GeneratedProtocolMessageType('Snapshot', (_message.Message,), {
  'DESCRIPTOR' : _SNAPSHOT,
  '__module__' : 'google.appengine.datastore.snapshot_pb2'

  })
_sym_db.RegisterMessage(Snapshot)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.google.storage.onestore.v3B\020OnestoreSnapshotZ\023storage_onestore_v3'
  _SNAPSHOT._serialized_start=66
  _SNAPSHOT._serialized_end=124
  _SNAPSHOT_STATUS._serialized_start=90
  _SNAPSHOT_STATUS._serialized_end=124

