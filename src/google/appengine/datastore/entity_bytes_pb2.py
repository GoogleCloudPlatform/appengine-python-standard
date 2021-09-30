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
  name='google/appengine/datastore/entity_bytes.proto',
  package='storage_onestore_v3_bytes',
  syntax='proto2',
  serialized_options=b'\n\036com.google.storage.onestore.v3B\016OnestoreEntityZ\023storage_onestore_v3',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-google/appengine/datastore/entity_bytes.proto\x12\x19storage_onestore_v3_bytes\"\xe9\x05\n\rPropertyValue\x12\x12\n\nint64Value\x18\x01 \x01(\x03\x12\x14\n\x0c\x62ooleanValue\x18\x02 \x01(\x08\x12\x13\n\x0bstringValue\x18\x03 \x01(\x0c\x12\x13\n\x0b\x64oubleValue\x18\x04 \x01(\x01\x12G\n\npointvalue\x18\x05 \x01(\n23.storage_onestore_v3_bytes.PropertyValue.PointValue\x12\x45\n\tuservalue\x18\x08 \x01(\n22.storage_onestore_v3_bytes.PropertyValue.UserValue\x12O\n\x0ereferencevalue\x18\x0c \x01(\n27.storage_onestore_v3_bytes.PropertyValue.ReferenceValue\x1a\"\n\nPointValue\x12\t\n\x01x\x18\x06 \x02(\x01\x12\t\n\x01y\x18\x07 \x02(\x01\x1a\xa4\x01\n\tUserValue\x12\r\n\x05\x65mail\x18\t \x02(\t\x12\x13\n\x0b\x61uth_domain\x18\n \x02(\t\x12\x10\n\x08nickname\x18\x0b \x01(\t\x12\x0e\n\x06gaiaid\x18\x12 \x02(\x03\x12\x19\n\x11obfuscated_gaiaid\x18\x13 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_identity\x18\x15 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_provider\x18\x16 \x01(\t\x1a\xd7\x01\n\x0eReferenceValue\x12\x0b\n\x03\x61pp\x18\r \x02(\t\x12\x12\n\nname_space\x18\x14 \x01(\t\x12X\n\x0bpathelement\x18\x0e \x03(\n2C.storage_onestore_v3_bytes.PropertyValue.ReferenceValue.PathElement\x12\x13\n\x0b\x64\x61tabase_id\x18\x17 \x01(\t\x1a\x35\n\x0bPathElement\x12\x0c\n\x04type\x18\x0f \x02(\t\x12\n\n\x02id\x18\x10 \x01(\x03\x12\x0c\n\x04name\x18\x11 \x01(\t\"\xc8\x04\n\x08Property\x12H\n\x07meaning\x18\x01 \x01(\x0e\x32+.storage_onestore_v3_bytes.Property.Meaning:\nNO_MEANING\x12\x13\n\x0bmeaning_uri\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x02(\t\x12\x37\n\x05value\x18\x05 \x02(\x0b\x32(.storage_onestore_v3_bytes.PropertyValue\x12\x10\n\x08multiple\x18\x04 \x02(\x08\x12\x13\n\x07stashed\x18\x06 \x01(\x05:\x02-1\x12\x17\n\x08\x63omputed\x18\x07 \x01(\x08:\x05\x66\x61lse\"\xd5\x02\n\x07Meaning\x12\x0e\n\nNO_MEANING\x10\x00\x12\x08\n\x04\x42LOB\x10\x0e\x12\x08\n\x04TEXT\x10\x0f\x12\x0e\n\nBYTESTRING\x10\x10\x12\x11\n\rATOM_CATEGORY\x10\x01\x12\r\n\tATOM_LINK\x10\x02\x12\x0e\n\nATOM_TITLE\x10\x03\x12\x10\n\x0c\x41TOM_CONTENT\x10\x04\x12\x10\n\x0c\x41TOM_SUMMARY\x10\x05\x12\x0f\n\x0b\x41TOM_AUTHOR\x10\x06\x12\x0b\n\x07GD_WHEN\x10\x07\x12\x0c\n\x08GD_EMAIL\x10\x08\x12\x10\n\x0cGEORSS_POINT\x10\t\x12\t\n\x05GD_IM\x10\n\x12\x12\n\x0eGD_PHONENUMBER\x10\x0b\x12\x14\n\x10GD_POSTALADDRESS\x10\x0c\x12\r\n\tGD_RATING\x10\r\x12\x0b\n\x07\x42LOBKEY\x10\x11\x12\x10\n\x0c\x45NTITY_PROTO\x10\x13\x12\x0e\n\nEMPTY_LIST\x10\x18\x12\x0f\n\x0bINDEX_VALUE\x10\x12\"s\n\x04Path\x12\x38\n\x07\x65lement\x18\x01 \x03(\n2\'.storage_onestore_v3_bytes.Path.Element\x1a\x31\n\x07\x45lement\x12\x0c\n\x04type\x18\x02 \x02(\t\x12\n\n\x02id\x18\x03 \x01(\x03\x12\x0c\n\x04name\x18\x04 \x01(\t\"p\n\tReference\x12\x0b\n\x03\x61pp\x18\r \x02(\t\x12\x12\n\nname_space\x18\x14 \x01(\t\x12-\n\x04path\x18\x0e \x02(\x0b\x32\x1f.storage_onestore_v3_bytes.Path\x12\x13\n\x0b\x64\x61tabase_id\x18\x17 \x01(\t\"\x9f\x01\n\x04User\x12\r\n\x05\x65mail\x18\x01 \x02(\t\x12\x13\n\x0b\x61uth_domain\x18\x02 \x02(\t\x12\x10\n\x08nickname\x18\x03 \x01(\t\x12\x0e\n\x06gaiaid\x18\x04 \x02(\x03\x12\x19\n\x11obfuscated_gaiaid\x18\x05 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_identity\x18\x06 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_provider\x18\x07 \x01(\t\"\x9c\x03\n\x0b\x45ntityProto\x12\x31\n\x03key\x18\r \x02(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x35\n\x0c\x65ntity_group\x18\x10 \x02(\x0b\x32\x1f.storage_onestore_v3_bytes.Path\x12.\n\x05owner\x18\x11 \x01(\x0b\x32\x1f.storage_onestore_v3_bytes.User\x12\x39\n\x04kind\x18\x04 \x01(\x0e\x32+.storage_onestore_v3_bytes.EntityProto.Kind\x12\x10\n\x08kind_uri\x18\x05 \x01(\t\x12\x35\n\x08property\x18\x0e \x03(\x0b\x32#.storage_onestore_v3_bytes.Property\x12\x39\n\x0craw_property\x18\x0f \x03(\x0b\x32#.storage_onestore_v3_bytes.Property\"4\n\x04Kind\x12\x0e\n\nGD_CONTACT\x10\x01\x12\x0c\n\x08GD_EVENT\x10\x02\x12\x0e\n\nGD_MESSAGE\x10\x03\"B\n\x0e\x45ntityMetadata\x12\x17\n\x0f\x63reated_version\x18\x01 \x01(\x03\x12\x17\n\x0fupdated_version\x18\x02 \x01(\x03\"\xbb\x01\n\rEntitySummary\x12T\n\x12large_raw_property\x18\x01 \x03(\x0b\x32\x38.storage_onestore_v3_bytes.EntitySummary.PropertySummary\x1aT\n\x0fPropertySummary\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x1f\n\x17property_type_for_stats\x18\x02 \x01(\t\x12\x12\n\nsize_bytes\x18\x03 \x01(\x05\"4\n\x11\x43ompositeProperty\x12\x10\n\x08index_id\x18\x01 \x02(\x03\x12\r\n\x05value\x18\x02 \x03(\x0c\"\xda\x04\n\x05Index\x12\x13\n\x0b\x65ntity_type\x18\x01 \x02(\t\x12\x10\n\x08\x61ncestor\x18\x05 \x02(\x08\x12\x0e\n\x06parent\x18\x07 \x01(\x08\x12N\n\x07version\x18\x08 \x01(\x0e\x32(.storage_onestore_v3_bytes.Index.Version:\x13VERSION_UNSPECIFIED\x12;\n\x08property\x18\x02 \x03(\n2).storage_onestore_v3_bytes.Index.Property\x1a\xd0\x02\n\x08Property\x12\x0c\n\x04name\x18\x03 \x02(\t\x12]\n\tdirection\x18\x04 \x01(\x0e\x32\x33.storage_onestore_v3_bytes.Index.Property.Direction:\x15\x44IRECTION_UNSPECIFIED\x12N\n\x04mode\x18\x06 \x01(\x0e\x32..storage_onestore_v3_bytes.Index.Property.Mode:\x10MODE_UNSPECIFIED\"E\n\tDirection\x12\x19\n\x15\x44IRECTION_UNSPECIFIED\x10\x00\x12\r\n\tASCENDING\x10\x01\x12\x0e\n\nDESCENDING\x10\x02\"@\n\x04Mode\x12\x14\n\x10MODE_UNSPECIFIED\x10\x00\x12\x0e\n\nGEOSPATIAL\x10\x03\x12\x12\n\x0e\x41RRAY_CONTAINS\x10\x04\":\n\x07Version\x12\x17\n\x13VERSION_UNSPECIFIED\x10\x00\x12\x06\n\x02V1\x10\x01\x12\x06\n\x02V2\x10\x02\x12\x06\n\x02V3\x10\x03\"\xc0\x04\n\x0e\x43ompositeIndex\x12\x0e\n\x06\x61pp_id\x18\x01 \x02(\t\x12\x13\n\x0b\x64\x61tabase_id\x18\x0c \x01(\t\x12\n\n\x02id\x18\x02 \x02(\x03\x12\x34\n\ndefinition\x18\x03 \x02(\x0b\x32 .storage_onestore_v3_bytes.Index\x12>\n\x05state\x18\x04 \x02(\x0e\x32/.storage_onestore_v3_bytes.CompositeIndex.State\x12S\n\x0eworkflow_state\x18\n \x01(\x0e\x32\x37.storage_onestore_v3_bytes.CompositeIndex.WorkflowStateB\x02\x18\x01\x12\x19\n\rerror_message\x18\x0b \x01(\tB\x02\x18\x01\x12\'\n\x14only_use_if_required\x18\x06 \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12!\n\x0e\x64isabled_index\x18\t \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12\'\n\x1f\x64\x65precated_read_division_family\x18\x07 \x03(\t\x12(\n deprecated_write_division_family\x18\x08 \x01(\t\"?\n\x05State\x12\x0e\n\nWRITE_ONLY\x10\x01\x12\x0e\n\nREAD_WRITE\x10\x02\x12\x0b\n\x07\x44\x45LETED\x10\x03\x12\t\n\x05\x45RROR\x10\x04\"7\n\rWorkflowState\x12\x0b\n\x07PENDING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x12\r\n\tCOMPLETED\x10\x03\"w\n\x10SearchIndexEntry\x12\x10\n\x08index_id\x18\x01 \x02(\x03\x12\x1d\n\x15write_division_family\x18\x02 \x02(\t\x12\x18\n\x10\x66ingerprint_1999\x18\x03 \x01(\x06\x12\x18\n\x10\x66ingerprint_2011\x18\x04 \x01(\x06\"\x98\x02\n\x0cIndexPostfix\x12G\n\x0bindex_value\x18\x01 \x03(\x0b\x32\x32.storage_onestore_v3_bytes.IndexPostfix.IndexValue\x12\x31\n\x03key\x18\x02 \x01(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x14\n\x06\x62\x65\x66ore\x18\x03 \x01(\x08:\x04true\x12\x18\n\x10\x62\x65\x66ore_ascending\x18\x04 \x01(\x08\x1a\\\n\nIndexValue\x12\x15\n\rproperty_name\x18\x01 \x02(\t\x12\x37\n\x05value\x18\x02 \x02(\x0b\x32(.storage_onestore_v3_bytes.PropertyValue\"L\n\rIndexPosition\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\x14\n\x06\x62\x65\x66ore\x18\x02 \x01(\x08:\x04true\x12\x18\n\x10\x62\x65\x66ore_ascending\x18\x03 \x01(\x08\x42\x45\n\x1e\x63om.google.storage.onestore.v3B\x0eOnestoreEntityZ\x13storage_onestore_v3'
)



_PROPERTY_MEANING = _descriptor.EnumDescriptor(
  name='Meaning',
  full_name='storage_onestore_v3_bytes.Property.Meaning',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NO_MEANING', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BLOB', index=1, number=14,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TEXT', index=2, number=15,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BYTESTRING', index=3, number=16,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ATOM_CATEGORY', index=4, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ATOM_LINK', index=5, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ATOM_TITLE', index=6, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ATOM_CONTENT', index=7, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ATOM_SUMMARY', index=8, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ATOM_AUTHOR', index=9, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GD_WHEN', index=10, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GD_EMAIL', index=11, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GEORSS_POINT', index=12, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GD_IM', index=13, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GD_PHONENUMBER', index=14, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GD_POSTALADDRESS', index=15, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GD_RATING', index=16, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BLOBKEY', index=17, number=17,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ENTITY_PROTO', index=18, number=19,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EMPTY_LIST', index=19, number=24,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INDEX_VALUE', index=20, number=18,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1068,
  serialized_end=1409,
)
_sym_db.RegisterEnumDescriptor(_PROPERTY_MEANING)

_ENTITYPROTO_KIND = _descriptor.EnumDescriptor(
  name='Kind',
  full_name='storage_onestore_v3_bytes.EntityProto.Kind',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GD_CONTACT', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GD_EVENT', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GD_MESSAGE', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2165,
  serialized_end=2217,
)
_sym_db.RegisterEnumDescriptor(_ENTITYPROTO_KIND)

_INDEX_PROPERTY_DIRECTION = _descriptor.EnumDescriptor(
  name='Direction',
  full_name='storage_onestore_v3_bytes.Index.Property.Direction',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DIRECTION_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ASCENDING', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DESCENDING', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2939,
  serialized_end=3008,
)
_sym_db.RegisterEnumDescriptor(_INDEX_PROPERTY_DIRECTION)

_INDEX_PROPERTY_MODE = _descriptor.EnumDescriptor(
  name='Mode',
  full_name='storage_onestore_v3_bytes.Index.Property.Mode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MODE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GEOSPATIAL', index=1, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ARRAY_CONTAINS', index=2, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=3010,
  serialized_end=3074,
)
_sym_db.RegisterEnumDescriptor(_INDEX_PROPERTY_MODE)

_INDEX_VERSION = _descriptor.EnumDescriptor(
  name='Version',
  full_name='storage_onestore_v3_bytes.Index.Version',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VERSION_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='V1', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='V2', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='V3', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=3076,
  serialized_end=3134,
)
_sym_db.RegisterEnumDescriptor(_INDEX_VERSION)

_COMPOSITEINDEX_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='storage_onestore_v3_bytes.CompositeIndex.State',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='WRITE_ONLY', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='READ_WRITE', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DELETED', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=3593,
  serialized_end=3656,
)
_sym_db.RegisterEnumDescriptor(_COMPOSITEINDEX_STATE)

_COMPOSITEINDEX_WORKFLOWSTATE = _descriptor.EnumDescriptor(
  name='WorkflowState',
  full_name='storage_onestore_v3_bytes.CompositeIndex.WorkflowState',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PENDING', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ACTIVE', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COMPLETED', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=3658,
  serialized_end=3713,
)
_sym_db.RegisterEnumDescriptor(_COMPOSITEINDEX_WORKFLOWSTATE)


_PROPERTYVALUE_POINTVALUE = _descriptor.Descriptor(
  name='PointValue',
  full_name='storage_onestore_v3_bytes.PropertyValue.PointValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='storage_onestore_v3_bytes.PropertyValue.PointValue.x', index=0,
      number=6, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='storage_onestore_v3_bytes.PropertyValue.PointValue.y', index=1,
      number=7, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
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
  serialized_start=403,
  serialized_end=437,
)

_PROPERTYVALUE_USERVALUE = _descriptor.Descriptor(
  name='UserValue',
  full_name='storage_onestore_v3_bytes.PropertyValue.UserValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='storage_onestore_v3_bytes.PropertyValue.UserValue.email', index=0,
      number=9, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auth_domain', full_name='storage_onestore_v3_bytes.PropertyValue.UserValue.auth_domain', index=1,
      number=10, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='storage_onestore_v3_bytes.PropertyValue.UserValue.nickname', index=2,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gaiaid', full_name='storage_onestore_v3_bytes.PropertyValue.UserValue.gaiaid', index=3,
      number=18, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='obfuscated_gaiaid', full_name='storage_onestore_v3_bytes.PropertyValue.UserValue.obfuscated_gaiaid', index=4,
      number=19, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='federated_identity', full_name='storage_onestore_v3_bytes.PropertyValue.UserValue.federated_identity', index=5,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='federated_provider', full_name='storage_onestore_v3_bytes.PropertyValue.UserValue.federated_provider', index=6,
      number=22, type=9, cpp_type=9, label=1,
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
  serialized_start=440,
  serialized_end=604,
)

_PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT = _descriptor.Descriptor(
  name='PathElement',
  full_name='storage_onestore_v3_bytes.PropertyValue.ReferenceValue.PathElement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='storage_onestore_v3_bytes.PropertyValue.ReferenceValue.PathElement.type', index=0,
      number=15, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='storage_onestore_v3_bytes.PropertyValue.ReferenceValue.PathElement.id', index=1,
      number=16, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='storage_onestore_v3_bytes.PropertyValue.ReferenceValue.PathElement.name', index=2,
      number=17, type=9, cpp_type=9, label=1,
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
  serialized_start=769,
  serialized_end=822,
)

_PROPERTYVALUE_REFERENCEVALUE = _descriptor.Descriptor(
  name='ReferenceValue',
  full_name='storage_onestore_v3_bytes.PropertyValue.ReferenceValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app', full_name='storage_onestore_v3_bytes.PropertyValue.ReferenceValue.app', index=0,
      number=13, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name_space', full_name='storage_onestore_v3_bytes.PropertyValue.ReferenceValue.name_space', index=1,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pathelement', full_name='storage_onestore_v3_bytes.PropertyValue.ReferenceValue.pathelement', index=2,
      number=14, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='database_id', full_name='storage_onestore_v3_bytes.PropertyValue.ReferenceValue.database_id', index=3,
      number=23, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=607,
  serialized_end=822,
)

_PROPERTYVALUE = _descriptor.Descriptor(
  name='PropertyValue',
  full_name='storage_onestore_v3_bytes.PropertyValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='int64Value', full_name='storage_onestore_v3_bytes.PropertyValue.int64Value', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='booleanValue', full_name='storage_onestore_v3_bytes.PropertyValue.booleanValue', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stringValue', full_name='storage_onestore_v3_bytes.PropertyValue.stringValue', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='doubleValue', full_name='storage_onestore_v3_bytes.PropertyValue.doubleValue', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pointvalue', full_name='storage_onestore_v3_bytes.PropertyValue.pointvalue', index=4,
      number=5, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uservalue', full_name='storage_onestore_v3_bytes.PropertyValue.uservalue', index=5,
      number=8, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='referencevalue', full_name='storage_onestore_v3_bytes.PropertyValue.referencevalue', index=6,
      number=12, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_PROPERTYVALUE_POINTVALUE, _PROPERTYVALUE_USERVALUE, _PROPERTYVALUE_REFERENCEVALUE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=822,
)


_PROPERTY = _descriptor.Descriptor(
  name='Property',
  full_name='storage_onestore_v3_bytes.Property',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='meaning', full_name='storage_onestore_v3_bytes.Property.meaning', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='meaning_uri', full_name='storage_onestore_v3_bytes.Property.meaning_uri', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='storage_onestore_v3_bytes.Property.name', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='storage_onestore_v3_bytes.Property.value', index=3,
      number=5, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='multiple', full_name='storage_onestore_v3_bytes.Property.multiple', index=4,
      number=4, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stashed', full_name='storage_onestore_v3_bytes.Property.stashed', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=-1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='computed', full_name='storage_onestore_v3_bytes.Property.computed', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PROPERTY_MEANING,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=825,
  serialized_end=1409,
)


_PATH_ELEMENT = _descriptor.Descriptor(
  name='Element',
  full_name='storage_onestore_v3_bytes.Path.Element',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='storage_onestore_v3_bytes.Path.Element.type', index=0,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='storage_onestore_v3_bytes.Path.Element.id', index=1,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='storage_onestore_v3_bytes.Path.Element.name', index=2,
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
  serialized_start=1477,
  serialized_end=1526,
)

_PATH = _descriptor.Descriptor(
  name='Path',
  full_name='storage_onestore_v3_bytes.Path',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='storage_onestore_v3_bytes.Path.element', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_PATH_ELEMENT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1411,
  serialized_end=1526,
)


_REFERENCE = _descriptor.Descriptor(
  name='Reference',
  full_name='storage_onestore_v3_bytes.Reference',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app', full_name='storage_onestore_v3_bytes.Reference.app', index=0,
      number=13, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name_space', full_name='storage_onestore_v3_bytes.Reference.name_space', index=1,
      number=20, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='path', full_name='storage_onestore_v3_bytes.Reference.path', index=2,
      number=14, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='database_id', full_name='storage_onestore_v3_bytes.Reference.database_id', index=3,
      number=23, type=9, cpp_type=9, label=1,
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
  serialized_start=1528,
  serialized_end=1640,
)


_USER = _descriptor.Descriptor(
  name='User',
  full_name='storage_onestore_v3_bytes.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='email', full_name='storage_onestore_v3_bytes.User.email', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auth_domain', full_name='storage_onestore_v3_bytes.User.auth_domain', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nickname', full_name='storage_onestore_v3_bytes.User.nickname', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='gaiaid', full_name='storage_onestore_v3_bytes.User.gaiaid', index=3,
      number=4, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='obfuscated_gaiaid', full_name='storage_onestore_v3_bytes.User.obfuscated_gaiaid', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='federated_identity', full_name='storage_onestore_v3_bytes.User.federated_identity', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='federated_provider', full_name='storage_onestore_v3_bytes.User.federated_provider', index=6,
      number=7, type=9, cpp_type=9, label=1,
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
  serialized_start=1643,
  serialized_end=1802,
)


_ENTITYPROTO = _descriptor.Descriptor(
  name='EntityProto',
  full_name='storage_onestore_v3_bytes.EntityProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='storage_onestore_v3_bytes.EntityProto.key', index=0,
      number=13, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entity_group', full_name='storage_onestore_v3_bytes.EntityProto.entity_group', index=1,
      number=16, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='owner', full_name='storage_onestore_v3_bytes.EntityProto.owner', index=2,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kind', full_name='storage_onestore_v3_bytes.EntityProto.kind', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kind_uri', full_name='storage_onestore_v3_bytes.EntityProto.kind_uri', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='property', full_name='storage_onestore_v3_bytes.EntityProto.property', index=5,
      number=14, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='raw_property', full_name='storage_onestore_v3_bytes.EntityProto.raw_property', index=6,
      number=15, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ENTITYPROTO_KIND,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1805,
  serialized_end=2217,
)


_ENTITYMETADATA = _descriptor.Descriptor(
  name='EntityMetadata',
  full_name='storage_onestore_v3_bytes.EntityMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='created_version', full_name='storage_onestore_v3_bytes.EntityMetadata.created_version', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='updated_version', full_name='storage_onestore_v3_bytes.EntityMetadata.updated_version', index=1,
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
  serialized_start=2219,
  serialized_end=2285,
)


_ENTITYSUMMARY_PROPERTYSUMMARY = _descriptor.Descriptor(
  name='PropertySummary',
  full_name='storage_onestore_v3_bytes.EntitySummary.PropertySummary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='storage_onestore_v3_bytes.EntitySummary.PropertySummary.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='property_type_for_stats', full_name='storage_onestore_v3_bytes.EntitySummary.PropertySummary.property_type_for_stats', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size_bytes', full_name='storage_onestore_v3_bytes.EntitySummary.PropertySummary.size_bytes', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  serialized_start=2391,
  serialized_end=2475,
)

_ENTITYSUMMARY = _descriptor.Descriptor(
  name='EntitySummary',
  full_name='storage_onestore_v3_bytes.EntitySummary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='large_raw_property', full_name='storage_onestore_v3_bytes.EntitySummary.large_raw_property', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_ENTITYSUMMARY_PROPERTYSUMMARY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2288,
  serialized_end=2475,
)


_COMPOSITEPROPERTY = _descriptor.Descriptor(
  name='CompositeProperty',
  full_name='storage_onestore_v3_bytes.CompositeProperty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index_id', full_name='storage_onestore_v3_bytes.CompositeProperty.index_id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='storage_onestore_v3_bytes.CompositeProperty.value', index=1,
      number=2, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=2477,
  serialized_end=2529,
)


_INDEX_PROPERTY = _descriptor.Descriptor(
  name='Property',
  full_name='storage_onestore_v3_bytes.Index.Property',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='storage_onestore_v3_bytes.Index.Property.name', index=0,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='direction', full_name='storage_onestore_v3_bytes.Index.Property.direction', index=1,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode', full_name='storage_onestore_v3_bytes.Index.Property.mode', index=2,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _INDEX_PROPERTY_DIRECTION,
    _INDEX_PROPERTY_MODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2738,
  serialized_end=3074,
)

_INDEX = _descriptor.Descriptor(
  name='Index',
  full_name='storage_onestore_v3_bytes.Index',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity_type', full_name='storage_onestore_v3_bytes.Index.entity_type', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ancestor', full_name='storage_onestore_v3_bytes.Index.ancestor', index=1,
      number=5, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parent', full_name='storage_onestore_v3_bytes.Index.parent', index=2,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='storage_onestore_v3_bytes.Index.version', index=3,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='property', full_name='storage_onestore_v3_bytes.Index.property', index=4,
      number=2, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_INDEX_PROPERTY, ],
  enum_types=[
    _INDEX_VERSION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2532,
  serialized_end=3134,
)


_COMPOSITEINDEX = _descriptor.Descriptor(
  name='CompositeIndex',
  full_name='storage_onestore_v3_bytes.CompositeIndex',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='storage_onestore_v3_bytes.CompositeIndex.app_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='database_id', full_name='storage_onestore_v3_bytes.CompositeIndex.database_id', index=1,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='storage_onestore_v3_bytes.CompositeIndex.id', index=2,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='definition', full_name='storage_onestore_v3_bytes.CompositeIndex.definition', index=3,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='storage_onestore_v3_bytes.CompositeIndex.state', index=4,
      number=4, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='workflow_state', full_name='storage_onestore_v3_bytes.CompositeIndex.workflow_state', index=5,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error_message', full_name='storage_onestore_v3_bytes.CompositeIndex.error_message', index=6,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='only_use_if_required', full_name='storage_onestore_v3_bytes.CompositeIndex.only_use_if_required', index=7,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='disabled_index', full_name='storage_onestore_v3_bytes.CompositeIndex.disabled_index', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_read_division_family', full_name='storage_onestore_v3_bytes.CompositeIndex.deprecated_read_division_family', index=9,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_write_division_family', full_name='storage_onestore_v3_bytes.CompositeIndex.deprecated_write_division_family', index=10,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _COMPOSITEINDEX_STATE,
    _COMPOSITEINDEX_WORKFLOWSTATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3137,
  serialized_end=3713,
)


_SEARCHINDEXENTRY = _descriptor.Descriptor(
  name='SearchIndexEntry',
  full_name='storage_onestore_v3_bytes.SearchIndexEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index_id', full_name='storage_onestore_v3_bytes.SearchIndexEntry.index_id', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='write_division_family', full_name='storage_onestore_v3_bytes.SearchIndexEntry.write_division_family', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fingerprint_1999', full_name='storage_onestore_v3_bytes.SearchIndexEntry.fingerprint_1999', index=2,
      number=3, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fingerprint_2011', full_name='storage_onestore_v3_bytes.SearchIndexEntry.fingerprint_2011', index=3,
      number=4, type=6, cpp_type=4, label=1,
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
  serialized_start=3715,
  serialized_end=3834,
)


_INDEXPOSTFIX_INDEXVALUE = _descriptor.Descriptor(
  name='IndexValue',
  full_name='storage_onestore_v3_bytes.IndexPostfix.IndexValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='property_name', full_name='storage_onestore_v3_bytes.IndexPostfix.IndexValue.property_name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='storage_onestore_v3_bytes.IndexPostfix.IndexValue.value', index=1,
      number=2, type=11, cpp_type=10, label=2,
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
  serialized_start=4025,
  serialized_end=4117,
)

_INDEXPOSTFIX = _descriptor.Descriptor(
  name='IndexPostfix',
  full_name='storage_onestore_v3_bytes.IndexPostfix',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index_value', full_name='storage_onestore_v3_bytes.IndexPostfix.index_value', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='key', full_name='storage_onestore_v3_bytes.IndexPostfix.key', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='before', full_name='storage_onestore_v3_bytes.IndexPostfix.before', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='before_ascending', full_name='storage_onestore_v3_bytes.IndexPostfix.before_ascending', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_INDEXPOSTFIX_INDEXVALUE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3837,
  serialized_end=4117,
)


_INDEXPOSITION = _descriptor.Descriptor(
  name='IndexPosition',
  full_name='storage_onestore_v3_bytes.IndexPosition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='storage_onestore_v3_bytes.IndexPosition.key', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='before', full_name='storage_onestore_v3_bytes.IndexPosition.before', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='before_ascending', full_name='storage_onestore_v3_bytes.IndexPosition.before_ascending', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=4119,
  serialized_end=4195,
)

_PROPERTYVALUE_POINTVALUE.containing_type = _PROPERTYVALUE
_PROPERTYVALUE_USERVALUE.containing_type = _PROPERTYVALUE
_PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT.containing_type = _PROPERTYVALUE_REFERENCEVALUE
_PROPERTYVALUE_REFERENCEVALUE.fields_by_name['pathelement'].message_type = _PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT
_PROPERTYVALUE_REFERENCEVALUE.containing_type = _PROPERTYVALUE
_PROPERTYVALUE.fields_by_name['pointvalue'].message_type = _PROPERTYVALUE_POINTVALUE
_PROPERTYVALUE.fields_by_name['uservalue'].message_type = _PROPERTYVALUE_USERVALUE
_PROPERTYVALUE.fields_by_name['referencevalue'].message_type = _PROPERTYVALUE_REFERENCEVALUE
_PROPERTY.fields_by_name['meaning'].enum_type = _PROPERTY_MEANING
_PROPERTY.fields_by_name['value'].message_type = _PROPERTYVALUE
_PROPERTY_MEANING.containing_type = _PROPERTY
_PATH_ELEMENT.containing_type = _PATH
_PATH.fields_by_name['element'].message_type = _PATH_ELEMENT
_REFERENCE.fields_by_name['path'].message_type = _PATH
_ENTITYPROTO.fields_by_name['key'].message_type = _REFERENCE
_ENTITYPROTO.fields_by_name['entity_group'].message_type = _PATH
_ENTITYPROTO.fields_by_name['owner'].message_type = _USER
_ENTITYPROTO.fields_by_name['kind'].enum_type = _ENTITYPROTO_KIND
_ENTITYPROTO.fields_by_name['property'].message_type = _PROPERTY
_ENTITYPROTO.fields_by_name['raw_property'].message_type = _PROPERTY
_ENTITYPROTO_KIND.containing_type = _ENTITYPROTO
_ENTITYSUMMARY_PROPERTYSUMMARY.containing_type = _ENTITYSUMMARY
_ENTITYSUMMARY.fields_by_name['large_raw_property'].message_type = _ENTITYSUMMARY_PROPERTYSUMMARY
_INDEX_PROPERTY.fields_by_name['direction'].enum_type = _INDEX_PROPERTY_DIRECTION
_INDEX_PROPERTY.fields_by_name['mode'].enum_type = _INDEX_PROPERTY_MODE
_INDEX_PROPERTY.containing_type = _INDEX
_INDEX_PROPERTY_DIRECTION.containing_type = _INDEX_PROPERTY
_INDEX_PROPERTY_MODE.containing_type = _INDEX_PROPERTY
_INDEX.fields_by_name['version'].enum_type = _INDEX_VERSION
_INDEX.fields_by_name['property'].message_type = _INDEX_PROPERTY
_INDEX_VERSION.containing_type = _INDEX
_COMPOSITEINDEX.fields_by_name['definition'].message_type = _INDEX
_COMPOSITEINDEX.fields_by_name['state'].enum_type = _COMPOSITEINDEX_STATE
_COMPOSITEINDEX.fields_by_name['workflow_state'].enum_type = _COMPOSITEINDEX_WORKFLOWSTATE
_COMPOSITEINDEX_STATE.containing_type = _COMPOSITEINDEX
_COMPOSITEINDEX_WORKFLOWSTATE.containing_type = _COMPOSITEINDEX
_INDEXPOSTFIX_INDEXVALUE.fields_by_name['value'].message_type = _PROPERTYVALUE
_INDEXPOSTFIX_INDEXVALUE.containing_type = _INDEXPOSTFIX
_INDEXPOSTFIX.fields_by_name['index_value'].message_type = _INDEXPOSTFIX_INDEXVALUE
_INDEXPOSTFIX.fields_by_name['key'].message_type = _REFERENCE
DESCRIPTOR.message_types_by_name['PropertyValue'] = _PROPERTYVALUE
DESCRIPTOR.message_types_by_name['Property'] = _PROPERTY
DESCRIPTOR.message_types_by_name['Path'] = _PATH
DESCRIPTOR.message_types_by_name['Reference'] = _REFERENCE
DESCRIPTOR.message_types_by_name['User'] = _USER
DESCRIPTOR.message_types_by_name['EntityProto'] = _ENTITYPROTO
DESCRIPTOR.message_types_by_name['EntityMetadata'] = _ENTITYMETADATA
DESCRIPTOR.message_types_by_name['EntitySummary'] = _ENTITYSUMMARY
DESCRIPTOR.message_types_by_name['CompositeProperty'] = _COMPOSITEPROPERTY
DESCRIPTOR.message_types_by_name['Index'] = _INDEX
DESCRIPTOR.message_types_by_name['CompositeIndex'] = _COMPOSITEINDEX
DESCRIPTOR.message_types_by_name['SearchIndexEntry'] = _SEARCHINDEXENTRY
DESCRIPTOR.message_types_by_name['IndexPostfix'] = _INDEXPOSTFIX
DESCRIPTOR.message_types_by_name['IndexPosition'] = _INDEXPOSITION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PropertyValue = _reflection.GeneratedProtocolMessageType('PropertyValue', (_message.Message,), {

  'PointValue' : _reflection.GeneratedProtocolMessageType('PointValue', (_message.Message,), {
    'DESCRIPTOR' : _PROPERTYVALUE_POINTVALUE,
    '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

    })
  ,

  'UserValue' : _reflection.GeneratedProtocolMessageType('UserValue', (_message.Message,), {
    'DESCRIPTOR' : _PROPERTYVALUE_USERVALUE,
    '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

    })
  ,

  'ReferenceValue' : _reflection.GeneratedProtocolMessageType('ReferenceValue', (_message.Message,), {

    'PathElement' : _reflection.GeneratedProtocolMessageType('PathElement', (_message.Message,), {
      'DESCRIPTOR' : _PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT,
      '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

      })
    ,
    'DESCRIPTOR' : _PROPERTYVALUE_REFERENCEVALUE,
    '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _PROPERTYVALUE,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(PropertyValue)
_sym_db.RegisterMessage(PropertyValue.PointValue)
_sym_db.RegisterMessage(PropertyValue.UserValue)
_sym_db.RegisterMessage(PropertyValue.ReferenceValue)
_sym_db.RegisterMessage(PropertyValue.ReferenceValue.PathElement)

Property = _reflection.GeneratedProtocolMessageType('Property', (_message.Message,), {
  'DESCRIPTOR' : _PROPERTY,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(Property)

Path = _reflection.GeneratedProtocolMessageType('Path', (_message.Message,), {

  'Element' : _reflection.GeneratedProtocolMessageType('Element', (_message.Message,), {
    'DESCRIPTOR' : _PATH_ELEMENT,
    '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _PATH,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(Path)
_sym_db.RegisterMessage(Path.Element)

Reference = _reflection.GeneratedProtocolMessageType('Reference', (_message.Message,), {
  'DESCRIPTOR' : _REFERENCE,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(Reference)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(User)

EntityProto = _reflection.GeneratedProtocolMessageType('EntityProto', (_message.Message,), {
  'DESCRIPTOR' : _ENTITYPROTO,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(EntityProto)

EntityMetadata = _reflection.GeneratedProtocolMessageType('EntityMetadata', (_message.Message,), {
  'DESCRIPTOR' : _ENTITYMETADATA,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(EntityMetadata)

EntitySummary = _reflection.GeneratedProtocolMessageType('EntitySummary', (_message.Message,), {

  'PropertySummary' : _reflection.GeneratedProtocolMessageType('PropertySummary', (_message.Message,), {
    'DESCRIPTOR' : _ENTITYSUMMARY_PROPERTYSUMMARY,
    '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _ENTITYSUMMARY,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(EntitySummary)
_sym_db.RegisterMessage(EntitySummary.PropertySummary)

CompositeProperty = _reflection.GeneratedProtocolMessageType('CompositeProperty', (_message.Message,), {
  'DESCRIPTOR' : _COMPOSITEPROPERTY,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(CompositeProperty)

Index = _reflection.GeneratedProtocolMessageType('Index', (_message.Message,), {

  'Property' : _reflection.GeneratedProtocolMessageType('Property', (_message.Message,), {
    'DESCRIPTOR' : _INDEX_PROPERTY,
    '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _INDEX,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(Index)
_sym_db.RegisterMessage(Index.Property)

CompositeIndex = _reflection.GeneratedProtocolMessageType('CompositeIndex', (_message.Message,), {
  'DESCRIPTOR' : _COMPOSITEINDEX,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(CompositeIndex)

SearchIndexEntry = _reflection.GeneratedProtocolMessageType('SearchIndexEntry', (_message.Message,), {
  'DESCRIPTOR' : _SEARCHINDEXENTRY,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(SearchIndexEntry)

IndexPostfix = _reflection.GeneratedProtocolMessageType('IndexPostfix', (_message.Message,), {

  'IndexValue' : _reflection.GeneratedProtocolMessageType('IndexValue', (_message.Message,), {
    'DESCRIPTOR' : _INDEXPOSTFIX_INDEXVALUE,
    '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _INDEXPOSTFIX,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(IndexPostfix)
_sym_db.RegisterMessage(IndexPostfix.IndexValue)

IndexPosition = _reflection.GeneratedProtocolMessageType('IndexPosition', (_message.Message,), {
  'DESCRIPTOR' : _INDEXPOSITION,
  '__module__' : 'google.appengine.datastore.entity_bytes_pb2'

  })
_sym_db.RegisterMessage(IndexPosition)


DESCRIPTOR._options = None
_COMPOSITEINDEX.fields_by_name['workflow_state']._options = None
_COMPOSITEINDEX.fields_by_name['error_message']._options = None
_COMPOSITEINDEX.fields_by_name['only_use_if_required']._options = None
_COMPOSITEINDEX.fields_by_name['disabled_index']._options = None

