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
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    30,
    0,
    '-dev',
    'google/appengine/datastore/entity_v4.proto'
)


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*google/appengine/datastore/entity_v4.proto\x12\x1dgoogle.appengine.datastore.v4\"X\n\x0bPartitionId\x12\x12\n\ndataset_id\x18\x03 \x01(\t\x12\x11\n\tnamespace\x18\x04 \x01(\t\"\"\n\tConstants\x12\x15\n\x11MAX_DIMENSION_TAG\x10\x64\"\xc4\x01\n\x03Key\x12@\n\x0cpartition_id\x18\x01 \x01(\x0b\x32*.google.appengine.datastore.v4.PartitionId\x12\x44\n\x0cpath_element\x18\x02 \x03(\x0b\x32..google.appengine.datastore.v4.Key.PathElement\x1a\x35\n\x0bPathElement\x12\x0c\n\x04kind\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x03\x12\x0c\n\x04name\x18\x03 \x01(\t\"/\n\x08GeoPoint\x12\x10\n\x08latitude\x18\x01 \x01(\x01\x12\x11\n\tlongitude\x18\x02 \x01(\x01\"\xcb\x03\n\x05Value\x12\x15\n\rboolean_value\x18\x01 \x01(\x08\x12\x15\n\rinteger_value\x18\x02 \x01(\x03\x12\x14\n\x0c\x64ouble_value\x18\x03 \x01(\x01\x12$\n\x1ctimestamp_microseconds_value\x18\x04 \x01(\x03\x12\x35\n\tkey_value\x18\x05 \x01(\x0b\x32\".google.appengine.datastore.v4.Key\x12\x16\n\x0e\x62lob_key_value\x18\x10 \x01(\t\x12\x14\n\x0cstring_value\x18\x11 \x01(\t\x12\x12\n\nblob_value\x18\x12 \x01(\x0c\x12;\n\x0c\x65ntity_value\x18\x06 \x01(\x0b\x32%.google.appengine.datastore.v4.Entity\x12@\n\x0fgeo_point_value\x18\x08 \x01(\x0b\x32\'.google.appengine.datastore.v4.GeoPoint\x12\x38\n\nlist_value\x18\x07 \x03(\x0b\x32$.google.appengine.datastore.v4.Value\x12\x0f\n\x07meaning\x18\x0e \x01(\x05\x12\x15\n\x07indexed\x18\x0f \x01(\x08:\x04true\"\xb6\x01\n\x08Property\x12\x0c\n\x04name\x18\x01 \x01(\t\x12#\n\x10\x64\x65precated_multi\x18\x02 \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12\x42\n\x10\x64\x65precated_value\x18\x03 \x03(\x0b\x32$.google.appengine.datastore.v4.ValueB\x02\x18\x01\x12\x33\n\x05value\x18\x04 \x01(\x0b\x32$.google.appengine.datastore.v4.Value\"t\n\x06\x45ntity\x12/\n\x03key\x18\x01 \x01(\x0b\x32\".google.appengine.datastore.v4.Key\x12\x39\n\x08property\x18\x02 \x03(\x0b\x32\'.google.appengine.datastore.v4.PropertyB\'\n%com.google.google.appengine.datastore')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.appengine.datastore.entity_v4_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.google.google.appengine.datastore'
  _globals['_PROPERTY'].fields_by_name['deprecated_multi']._loaded_options = None
  _globals['_PROPERTY'].fields_by_name['deprecated_multi']._serialized_options = b'\030\001'
  _globals['_PROPERTY'].fields_by_name['deprecated_value']._loaded_options = None
  _globals['_PROPERTY'].fields_by_name['deprecated_value']._serialized_options = b'\030\001'
  _globals['_PARTITIONID']._serialized_start=77
  _globals['_PARTITIONID']._serialized_end=165
  _globals['_PARTITIONID_CONSTANTS']._serialized_start=131
  _globals['_PARTITIONID_CONSTANTS']._serialized_end=165
  _globals['_KEY']._serialized_start=168
  _globals['_KEY']._serialized_end=364
  _globals['_KEY_PATHELEMENT']._serialized_start=311
  _globals['_KEY_PATHELEMENT']._serialized_end=364
  _globals['_GEOPOINT']._serialized_start=366
  _globals['_GEOPOINT']._serialized_end=413
  _globals['_VALUE']._serialized_start=416
  _globals['_VALUE']._serialized_end=875
  _globals['_PROPERTY']._serialized_start=878
  _globals['_PROPERTY']._serialized_end=1060
  _globals['_ENTITY']._serialized_start=1062
  _globals['_ENTITY']._serialized_end=1178

