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
    'google/appengine/datastore/entity_bytes.proto'
)


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-google/appengine/datastore/entity_bytes.proto\x12\x19storage_onestore_v3_bytes\"\xe9\x05\n\rPropertyValue\x12\x12\n\nint64Value\x18\x01 \x01(\x03\x12\x14\n\x0c\x62ooleanValue\x18\x02 \x01(\x08\x12\x13\n\x0bstringValue\x18\x03 \x01(\x0c\x12\x13\n\x0b\x64oubleValue\x18\x04 \x01(\x01\x12G\n\npointvalue\x18\x05 \x01(\n23.storage_onestore_v3_bytes.PropertyValue.PointValue\x12\x45\n\tuservalue\x18\x08 \x01(\n22.storage_onestore_v3_bytes.PropertyValue.UserValue\x12O\n\x0ereferencevalue\x18\x0c \x01(\n27.storage_onestore_v3_bytes.PropertyValue.ReferenceValue\x1a\"\n\nPointValue\x12\t\n\x01x\x18\x06 \x01(\x01\x12\t\n\x01y\x18\x07 \x01(\x01\x1a\xa4\x01\n\tUserValue\x12\r\n\x05\x65mail\x18\t \x01(\t\x12\x13\n\x0b\x61uth_domain\x18\n \x01(\t\x12\x10\n\x08nickname\x18\x0b \x01(\t\x12\x0e\n\x06gaiaid\x18\x12 \x01(\x03\x12\x19\n\x11obfuscated_gaiaid\x18\x13 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_identity\x18\x15 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_provider\x18\x16 \x01(\t\x1a\xd7\x01\n\x0eReferenceValue\x12\x0b\n\x03\x61pp\x18\r \x01(\t\x12\x12\n\nname_space\x18\x14 \x01(\t\x12X\n\x0bpathelement\x18\x0e \x03(\n2C.storage_onestore_v3_bytes.PropertyValue.ReferenceValue.PathElement\x12\x13\n\x0b\x64\x61tabase_id\x18\x17 \x01(\t\x1a\x35\n\x0bPathElement\x12\x0c\n\x04type\x18\x0f \x01(\t\x12\n\n\x02id\x18\x10 \x01(\x03\x12\x0c\n\x04name\x18\x11 \x01(\t\"\xd6\x05\n\x08Property\x12H\n\x07meaning\x18\x01 \x01(\x0e\x32+.storage_onestore_v3_bytes.Property.Meaning:\nNO_MEANING\x12\x13\n\x0bmeaning_uri\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x37\n\x05value\x18\x05 \x01(\x0b\x32(.storage_onestore_v3_bytes.PropertyValue\x12\x10\n\x08multiple\x18\x04 \x01(\x08\x12\x13\n\x07stashed\x18\x06 \x01(\x05:\x02-1\x12\x17\n\x08\x63omputed\x18\x07 \x01(\x08:\x05\x66\x61lse\"\xe3\x03\n\x07Meaning\x12\x0e\n\nNO_MEANING\x10\x00\x12\x08\n\x04\x42LOB\x10\x0e\x12\x08\n\x04TEXT\x10\x0f\x12\x0e\n\nBYTESTRING\x10\x10\x12\x11\n\rATOM_CATEGORY\x10\x01\x12\r\n\tATOM_LINK\x10\x02\x12\x0e\n\nATOM_TITLE\x10\x03\x12\x10\n\x0c\x41TOM_CONTENT\x10\x04\x12\x10\n\x0c\x41TOM_SUMMARY\x10\x05\x12\x0f\n\x0b\x41TOM_AUTHOR\x10\x06\x12\x0b\n\x07GD_WHEN\x10\x07\x12\x0c\n\x08GD_EMAIL\x10\x08\x12\x10\n\x0cGEORSS_POINT\x10\t\x12\t\n\x05GD_IM\x10\n\x12\x12\n\x0eGD_PHONENUMBER\x10\x0b\x12\x14\n\x10GD_POSTALADDRESS\x10\x0c\x12\r\n\tGD_RATING\x10\r\x12\x0b\n\x07\x42LOBKEY\x10\x11\x12\x10\n\x0c\x45NTITY_PROTO\x10\x13\x12\x0e\n\nEMPTY_LIST\x10\x18\x12\x0f\n\x0bINDEX_VALUE\x10\x12\x12\n\n\x06VECTOR\x10\x1f\x12\x0e\n\nDECIMAL128\x10 \x12\x16\n\x12\x42YTES_WITH_SUBTYPE\x10!\x12\r\n\tOBJECT_ID\x10\"\x12\t\n\x05REGEX\x10#\x12\t\n\x05INT32\x10$\x12\x15\n\x11REQUEST_TIMESTAMP\x10%\x12\r\n\tMIN_VALUE\x10&\x12\r\n\tMAX_VALUE\x10\'\"s\n\x04Path\x12\x38\n\x07\x65lement\x18\x01 \x03(\n2\'.storage_onestore_v3_bytes.Path.Element\x1a\x31\n\x07\x45lement\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\x03\x12\x0c\n\x04name\x18\x04 \x01(\t\"p\n\tReference\x12\x0b\n\x03\x61pp\x18\r \x01(\t\x12\x12\n\nname_space\x18\x14 \x01(\t\x12-\n\x04path\x18\x0e \x01(\x0b\x32\x1f.storage_onestore_v3_bytes.Path\x12\x13\n\x0b\x64\x61tabase_id\x18\x17 \x01(\t\"\x9f\x01\n\x04User\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x13\n\x0b\x61uth_domain\x18\x02 \x01(\t\x12\x10\n\x08nickname\x18\x03 \x01(\t\x12\x0e\n\x06gaiaid\x18\x04 \x01(\x03\x12\x19\n\x11obfuscated_gaiaid\x18\x05 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_identity\x18\x06 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_provider\x18\x07 \x01(\t\"\x9c\x03\n\x0b\x45ntityProto\x12\x31\n\x03key\x18\r \x01(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x35\n\x0c\x65ntity_group\x18\x10 \x01(\x0b\x32\x1f.storage_onestore_v3_bytes.Path\x12.\n\x05owner\x18\x11 \x01(\x0b\x32\x1f.storage_onestore_v3_bytes.User\x12\x39\n\x04kind\x18\x04 \x01(\x0e\x32+.storage_onestore_v3_bytes.EntityProto.Kind\x12\x10\n\x08kind_uri\x18\x05 \x01(\t\x12\x35\n\x08property\x18\x0e \x03(\x0b\x32#.storage_onestore_v3_bytes.Property\x12\x39\n\x0craw_property\x18\x0f \x03(\x0b\x32#.storage_onestore_v3_bytes.Property\"4\n\x04Kind\x12\x0e\n\nGD_CONTACT\x10\x01\x12\x0c\n\x08GD_EVENT\x10\x02\x12\x0e\n\nGD_MESSAGE\x10\x03\"B\n\x0e\x45ntityMetadata\x12\x17\n\x0f\x63reated_version\x18\x01 \x01(\x03\x12\x17\n\x0fupdated_version\x18\x02 \x01(\x03\"\xbb\x01\n\rEntitySummary\x12T\n\x12large_raw_property\x18\x01 \x03(\x0b\x32\x38.storage_onestore_v3_bytes.EntitySummary.PropertySummary\x1aT\n\x0fPropertySummary\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1f\n\x17property_type_for_stats\x18\x02 \x01(\t\x12\x12\n\nsize_bytes\x18\x03 \x01(\x05\"4\n\x11\x43ompositeProperty\x12\x10\n\x08index_id\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x03(\x0c\"\xe6\x04\n\x05Index\x12\x13\n\x0b\x65ntity_type\x18\x01 \x01(\t\x12\x10\n\x08\x61ncestor\x18\x05 \x01(\x08\x12\x0e\n\x06parent\x18\x07 \x01(\x08\x12N\n\x07version\x18\x08 \x01(\x0e\x32(.storage_onestore_v3_bytes.Index.Version:\x13VERSION_UNSPECIFIED\x12;\n\x08property\x18\x02 \x03(\n2).storage_onestore_v3_bytes.Index.Property\x1a\xdc\x02\n\x08Property\x12\x0c\n\x04name\x18\x03 \x01(\t\x12]\n\tdirection\x18\x04 \x01(\x0e\x32\x33.storage_onestore_v3_bytes.Index.Property.Direction:\x15\x44IRECTION_UNSPECIFIED\x12N\n\x04mode\x18\x06 \x01(\x0e\x32..storage_onestore_v3_bytes.Index.Property.Mode:\x10MODE_UNSPECIFIED\"E\n\tDirection\x12\x19\n\x15\x44IRECTION_UNSPECIFIED\x10\x00\x12\r\n\tASCENDING\x10\x01\x12\x0e\n\nDESCENDING\x10\x02\"L\n\x04Mode\x12\x14\n\x10MODE_UNSPECIFIED\x10\x00\x12\x0e\n\nGEOSPATIAL\x10\x03\x12\x12\n\x0e\x41RRAY_CONTAINS\x10\x04\x12\n\n\x06VECTOR\x10\x05\":\n\x07Version\x12\x17\n\x13VERSION_UNSPECIFIED\x10\x00\x12\x06\n\x02V1\x10\x01\x12\x06\n\x02V2\x10\x02\x12\x06\n\x02V3\x10\x03\"\xc0\x04\n\x0e\x43ompositeIndex\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x61tabase_id\x18\x0c \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x03\x12\x34\n\ndefinition\x18\x03 \x01(\x0b\x32 .storage_onestore_v3_bytes.Index\x12>\n\x05state\x18\x04 \x01(\x0e\x32/.storage_onestore_v3_bytes.CompositeIndex.State\x12S\n\x0eworkflow_state\x18\n \x01(\x0e\x32\x37.storage_onestore_v3_bytes.CompositeIndex.WorkflowStateB\x02\x18\x01\x12\x19\n\rerror_message\x18\x0b \x01(\tB\x02\x18\x01\x12\'\n\x14only_use_if_optional\x18\x06 \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12!\n\x0e\x64isabled_index\x18\t \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12\'\n\x1f\x64\x65precated_read_division_family\x18\x07 \x03(\t\x12(\n deprecated_write_division_family\x18\x08 \x01(\t\"?\n\x05State\x12\x0e\n\nWRITE_ONLY\x10\x01\x12\x0e\n\nREAD_WRITE\x10\x02\x12\x0b\n\x07\x44\x45LETED\x10\x03\x12\t\n\x05\x45RROR\x10\x04\"7\n\rWorkflowState\x12\x0b\n\x07PENDING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x12\r\n\tCOMPLETED\x10\x03\"w\n\x10SearchIndexEntry\x12\x10\n\x08index_id\x18\x01 \x01(\x03\x12\x1d\n\x15write_division_family\x18\x02 \x01(\t\x12\x18\n\x10\x66ingerprint_1999\x18\x03 \x01(\x06\x12\x18\n\x10\x66ingerprint_2011\x18\x04 \x01(\x06\"\x98\x02\n\x0cIndexPostfix\x12G\n\x0bindex_value\x18\x01 \x03(\x0b\x32\x32.storage_onestore_v3_bytes.IndexPostfix.IndexValue\x12\x31\n\x03key\x18\x02 \x01(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x14\n\x06\x62\x65\x66ore\x18\x03 \x01(\x08:\x04true\x12\x18\n\x10\x62\x65\x66ore_ascending\x18\x04 \x01(\x08\x1a\\\n\nIndexValue\x12\x15\n\rproperty_name\x18\x01 \x01(\t\x12\x37\n\x05value\x18\x02 \x01(\x0b\x32(.storage_onestore_v3_bytes.PropertyValue\"L\n\rIndexPosition\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\x14\n\x06\x62\x65\x66ore\x18\x02 \x01(\x08:\x04true\x12\x18\n\x10\x62\x65\x66ore_ascending\x18\x03 \x01(\x08\x42\x45\n\x1e\x63om.google.storage.onestore.v3B\x0eOnestoreEntityZ\x13storage_onestore_v3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.appengine.datastore.entity_bytes_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\036com.google.storage.onestore.v3B\016OnestoreEntityZ\023storage_onestore_v3'
  _globals['_COMPOSITEINDEX'].fields_by_name['workflow_state']._loaded_options = None
  _globals['_COMPOSITEINDEX'].fields_by_name['workflow_state']._serialized_options = b'\030\001'
  _globals['_COMPOSITEINDEX'].fields_by_name['error_message']._loaded_options = None
  _globals['_COMPOSITEINDEX'].fields_by_name['error_message']._serialized_options = b'\030\001'
  _globals['_COMPOSITEINDEX'].fields_by_name['only_use_if_optional']._loaded_options = None
  _globals['_COMPOSITEINDEX'].fields_by_name['only_use_if_optional']._serialized_options = b'\030\001'
  _globals['_COMPOSITEINDEX'].fields_by_name['disabled_index']._loaded_options = None
  _globals['_COMPOSITEINDEX'].fields_by_name['disabled_index']._serialized_options = b'\030\001'
  _globals['_PROPERTYVALUE']._serialized_start=77
  _globals['_PROPERTYVALUE']._serialized_end=822
  _globals['_PROPERTYVALUE_POINTVALUE']._serialized_start=403
  _globals['_PROPERTYVALUE_POINTVALUE']._serialized_end=437
  _globals['_PROPERTYVALUE_USERVALUE']._serialized_start=440
  _globals['_PROPERTYVALUE_USERVALUE']._serialized_end=604
  _globals['_PROPERTYVALUE_REFERENCEVALUE']._serialized_start=607
  _globals['_PROPERTYVALUE_REFERENCEVALUE']._serialized_end=822
  _globals['_PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT']._serialized_start=769
  _globals['_PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT']._serialized_end=822
  _globals['_PROPERTY']._serialized_start=825
  _globals['_PROPERTY']._serialized_end=1551
  _globals['_PROPERTY_MEANING']._serialized_start=1068
  _globals['_PROPERTY_MEANING']._serialized_end=1551
  _globals['_PATH']._serialized_start=1553
  _globals['_PATH']._serialized_end=1668
  _globals['_PATH_ELEMENT']._serialized_start=1619
  _globals['_PATH_ELEMENT']._serialized_end=1668
  _globals['_REFERENCE']._serialized_start=1670
  _globals['_REFERENCE']._serialized_end=1782
  _globals['_USER']._serialized_start=1785
  _globals['_USER']._serialized_end=1944
  _globals['_ENTITYPROTO']._serialized_start=1947
  _globals['_ENTITYPROTO']._serialized_end=2359
  _globals['_ENTITYPROTO_KIND']._serialized_start=2307
  _globals['_ENTITYPROTO_KIND']._serialized_end=2359
  _globals['_ENTITYMETADATA']._serialized_start=2361
  _globals['_ENTITYMETADATA']._serialized_end=2427
  _globals['_ENTITYSUMMARY']._serialized_start=2430
  _globals['_ENTITYSUMMARY']._serialized_end=2617
  _globals['_ENTITYSUMMARY_PROPERTYSUMMARY']._serialized_start=2533
  _globals['_ENTITYSUMMARY_PROPERTYSUMMARY']._serialized_end=2617
  _globals['_COMPOSITEPROPERTY']._serialized_start=2619
  _globals['_COMPOSITEPROPERTY']._serialized_end=2671
  _globals['_INDEX']._serialized_start=2674
  _globals['_INDEX']._serialized_end=3288
  _globals['_INDEX_PROPERTY']._serialized_start=2880
  _globals['_INDEX_PROPERTY']._serialized_end=3228
  _globals['_INDEX_PROPERTY_DIRECTION']._serialized_start=3081
  _globals['_INDEX_PROPERTY_DIRECTION']._serialized_end=3150
  _globals['_INDEX_PROPERTY_MODE']._serialized_start=3152
  _globals['_INDEX_PROPERTY_MODE']._serialized_end=3228
  _globals['_INDEX_VERSION']._serialized_start=3230
  _globals['_INDEX_VERSION']._serialized_end=3288
  _globals['_COMPOSITEINDEX']._serialized_start=3291
  _globals['_COMPOSITEINDEX']._serialized_end=3867
  _globals['_COMPOSITEINDEX_STATE']._serialized_start=3747
  _globals['_COMPOSITEINDEX_STATE']._serialized_end=3810
  _globals['_COMPOSITEINDEX_WORKFLOWSTATE']._serialized_start=3812
  _globals['_COMPOSITEINDEX_WORKFLOWSTATE']._serialized_end=3867
  _globals['_SEARCHINDEXENTRY']._serialized_start=3869
  _globals['_SEARCHINDEXENTRY']._serialized_end=3988
  _globals['_INDEXPOSTFIX']._serialized_start=3991
  _globals['_INDEXPOSTFIX']._serialized_end=4271
  _globals['_INDEXPOSTFIX_INDEXVALUE']._serialized_start=4179
  _globals['_INDEXPOSTFIX_INDEXVALUE']._serialized_end=4271
  _globals['_INDEXPOSITION']._serialized_start=4273
  _globals['_INDEXPOSITION']._serialized_end=4349

