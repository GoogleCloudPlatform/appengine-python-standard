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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-google/appengine/datastore/entity_bytes.proto\x12\x19storage_onestore_v3_bytes\"\xe9\x05\n\rPropertyValue\x12\x12\n\nint64Value\x18\x01 \x01(\x03\x12\x14\n\x0c\x62ooleanValue\x18\x02 \x01(\x08\x12\x13\n\x0bstringValue\x18\x03 \x01(\x0c\x12\x13\n\x0b\x64oubleValue\x18\x04 \x01(\x01\x12G\n\npointvalue\x18\x05 \x01(\n23.storage_onestore_v3_bytes.PropertyValue.PointValue\x12\x45\n\tuservalue\x18\x08 \x01(\n22.storage_onestore_v3_bytes.PropertyValue.UserValue\x12O\n\x0ereferencevalue\x18\x0c \x01(\n27.storage_onestore_v3_bytes.PropertyValue.ReferenceValue\x1a\"\n\nPointValue\x12\t\n\x01x\x18\x06 \x02(\x01\x12\t\n\x01y\x18\x07 \x02(\x01\x1a\xa4\x01\n\tUserValue\x12\r\n\x05\x65mail\x18\t \x02(\t\x12\x13\n\x0b\x61uth_domain\x18\n \x02(\t\x12\x10\n\x08nickname\x18\x0b \x01(\t\x12\x0e\n\x06gaiaid\x18\x12 \x02(\x03\x12\x19\n\x11obfuscated_gaiaid\x18\x13 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_identity\x18\x15 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_provider\x18\x16 \x01(\t\x1a\xd7\x01\n\x0eReferenceValue\x12\x0b\n\x03\x61pp\x18\r \x02(\t\x12\x12\n\nname_space\x18\x14 \x01(\t\x12X\n\x0bpathelement\x18\x0e \x03(\n2C.storage_onestore_v3_bytes.PropertyValue.ReferenceValue.PathElement\x12\x13\n\x0b\x64\x61tabase_id\x18\x17 \x01(\t\x1a\x35\n\x0bPathElement\x12\x0c\n\x04type\x18\x0f \x02(\t\x12\n\n\x02id\x18\x10 \x01(\x03\x12\x0c\n\x04name\x18\x11 \x01(\t\"\xc8\x04\n\x08Property\x12H\n\x07meaning\x18\x01 \x01(\x0e\x32+.storage_onestore_v3_bytes.Property.Meaning:\nNO_MEANING\x12\x13\n\x0bmeaning_uri\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x02(\t\x12\x37\n\x05value\x18\x05 \x02(\x0b\x32(.storage_onestore_v3_bytes.PropertyValue\x12\x10\n\x08multiple\x18\x04 \x02(\x08\x12\x13\n\x07stashed\x18\x06 \x01(\x05:\x02-1\x12\x17\n\x08\x63omputed\x18\x07 \x01(\x08:\x05\x66\x61lse\"\xd5\x02\n\x07Meaning\x12\x0e\n\nNO_MEANING\x10\x00\x12\x08\n\x04\x42LOB\x10\x0e\x12\x08\n\x04TEXT\x10\x0f\x12\x0e\n\nBYTESTRING\x10\x10\x12\x11\n\rATOM_CATEGORY\x10\x01\x12\r\n\tATOM_LINK\x10\x02\x12\x0e\n\nATOM_TITLE\x10\x03\x12\x10\n\x0c\x41TOM_CONTENT\x10\x04\x12\x10\n\x0c\x41TOM_SUMMARY\x10\x05\x12\x0f\n\x0b\x41TOM_AUTHOR\x10\x06\x12\x0b\n\x07GD_WHEN\x10\x07\x12\x0c\n\x08GD_EMAIL\x10\x08\x12\x10\n\x0cGEORSS_POINT\x10\t\x12\t\n\x05GD_IM\x10\n\x12\x12\n\x0eGD_PHONENUMBER\x10\x0b\x12\x14\n\x10GD_POSTALADDRESS\x10\x0c\x12\r\n\tGD_RATING\x10\r\x12\x0b\n\x07\x42LOBKEY\x10\x11\x12\x10\n\x0c\x45NTITY_PROTO\x10\x13\x12\x0e\n\nEMPTY_LIST\x10\x18\x12\x0f\n\x0bINDEX_VALUE\x10\x12\"s\n\x04Path\x12\x38\n\x07\x65lement\x18\x01 \x03(\n2\'.storage_onestore_v3_bytes.Path.Element\x1a\x31\n\x07\x45lement\x12\x0c\n\x04type\x18\x02 \x02(\t\x12\n\n\x02id\x18\x03 \x01(\x03\x12\x0c\n\x04name\x18\x04 \x01(\t\"p\n\tReference\x12\x0b\n\x03\x61pp\x18\r \x02(\t\x12\x12\n\nname_space\x18\x14 \x01(\t\x12-\n\x04path\x18\x0e \x02(\x0b\x32\x1f.storage_onestore_v3_bytes.Path\x12\x13\n\x0b\x64\x61tabase_id\x18\x17 \x01(\t\"\x9f\x01\n\x04User\x12\r\n\x05\x65mail\x18\x01 \x02(\t\x12\x13\n\x0b\x61uth_domain\x18\x02 \x02(\t\x12\x10\n\x08nickname\x18\x03 \x01(\t\x12\x0e\n\x06gaiaid\x18\x04 \x02(\x03\x12\x19\n\x11obfuscated_gaiaid\x18\x05 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_identity\x18\x06 \x01(\t\x12\x1a\n\x12\x66\x65\x64\x65rated_provider\x18\x07 \x01(\t\"\x9c\x03\n\x0b\x45ntityProto\x12\x31\n\x03key\x18\r \x02(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x35\n\x0c\x65ntity_group\x18\x10 \x02(\x0b\x32\x1f.storage_onestore_v3_bytes.Path\x12.\n\x05owner\x18\x11 \x01(\x0b\x32\x1f.storage_onestore_v3_bytes.User\x12\x39\n\x04kind\x18\x04 \x01(\x0e\x32+.storage_onestore_v3_bytes.EntityProto.Kind\x12\x10\n\x08kind_uri\x18\x05 \x01(\t\x12\x35\n\x08property\x18\x0e \x03(\x0b\x32#.storage_onestore_v3_bytes.Property\x12\x39\n\x0craw_property\x18\x0f \x03(\x0b\x32#.storage_onestore_v3_bytes.Property\"4\n\x04Kind\x12\x0e\n\nGD_CONTACT\x10\x01\x12\x0c\n\x08GD_EVENT\x10\x02\x12\x0e\n\nGD_MESSAGE\x10\x03\"B\n\x0e\x45ntityMetadata\x12\x17\n\x0f\x63reated_version\x18\x01 \x01(\x03\x12\x17\n\x0fupdated_version\x18\x02 \x01(\x03\"\xbb\x01\n\rEntitySummary\x12T\n\x12large_raw_property\x18\x01 \x03(\x0b\x32\x38.storage_onestore_v3_bytes.EntitySummary.PropertySummary\x1aT\n\x0fPropertySummary\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x1f\n\x17property_type_for_stats\x18\x02 \x01(\t\x12\x12\n\nsize_bytes\x18\x03 \x01(\x05\"4\n\x11\x43ompositeProperty\x12\x10\n\x08index_id\x18\x01 \x02(\x03\x12\r\n\x05value\x18\x02 \x03(\x0c\"\xda\x04\n\x05Index\x12\x13\n\x0b\x65ntity_type\x18\x01 \x02(\t\x12\x10\n\x08\x61ncestor\x18\x05 \x02(\x08\x12\x0e\n\x06parent\x18\x07 \x01(\x08\x12N\n\x07version\x18\x08 \x01(\x0e\x32(.storage_onestore_v3_bytes.Index.Version:\x13VERSION_UNSPECIFIED\x12;\n\x08property\x18\x02 \x03(\n2).storage_onestore_v3_bytes.Index.Property\x1a\xd0\x02\n\x08Property\x12\x0c\n\x04name\x18\x03 \x02(\t\x12]\n\tdirection\x18\x04 \x01(\x0e\x32\x33.storage_onestore_v3_bytes.Index.Property.Direction:\x15\x44IRECTION_UNSPECIFIED\x12N\n\x04mode\x18\x06 \x01(\x0e\x32..storage_onestore_v3_bytes.Index.Property.Mode:\x10MODE_UNSPECIFIED\"E\n\tDirection\x12\x19\n\x15\x44IRECTION_UNSPECIFIED\x10\x00\x12\r\n\tASCENDING\x10\x01\x12\x0e\n\nDESCENDING\x10\x02\"@\n\x04Mode\x12\x14\n\x10MODE_UNSPECIFIED\x10\x00\x12\x0e\n\nGEOSPATIAL\x10\x03\x12\x12\n\x0e\x41RRAY_CONTAINS\x10\x04\":\n\x07Version\x12\x17\n\x13VERSION_UNSPECIFIED\x10\x00\x12\x06\n\x02V1\x10\x01\x12\x06\n\x02V2\x10\x02\x12\x06\n\x02V3\x10\x03\"\xc0\x04\n\x0e\x43ompositeIndex\x12\x0e\n\x06\x61pp_id\x18\x01 \x02(\t\x12\x13\n\x0b\x64\x61tabase_id\x18\x0c \x01(\t\x12\n\n\x02id\x18\x02 \x02(\x03\x12\x34\n\ndefinition\x18\x03 \x02(\x0b\x32 .storage_onestore_v3_bytes.Index\x12>\n\x05state\x18\x04 \x02(\x0e\x32/.storage_onestore_v3_bytes.CompositeIndex.State\x12S\n\x0eworkflow_state\x18\n \x01(\x0e\x32\x37.storage_onestore_v3_bytes.CompositeIndex.WorkflowStateB\x02\x18\x01\x12\x19\n\rerror_message\x18\x0b \x01(\tB\x02\x18\x01\x12\'\n\x14only_use_if_required\x18\x06 \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12!\n\x0e\x64isabled_index\x18\t \x01(\x08:\x05\x66\x61lseB\x02\x18\x01\x12\'\n\x1f\x64\x65precated_read_division_family\x18\x07 \x03(\t\x12(\n deprecated_write_division_family\x18\x08 \x01(\t\"?\n\x05State\x12\x0e\n\nWRITE_ONLY\x10\x01\x12\x0e\n\nREAD_WRITE\x10\x02\x12\x0b\n\x07\x44\x45LETED\x10\x03\x12\t\n\x05\x45RROR\x10\x04\"7\n\rWorkflowState\x12\x0b\n\x07PENDING\x10\x01\x12\n\n\x06\x41\x43TIVE\x10\x02\x12\r\n\tCOMPLETED\x10\x03\"w\n\x10SearchIndexEntry\x12\x10\n\x08index_id\x18\x01 \x02(\x03\x12\x1d\n\x15write_division_family\x18\x02 \x02(\t\x12\x18\n\x10\x66ingerprint_1999\x18\x03 \x01(\x06\x12\x18\n\x10\x66ingerprint_2011\x18\x04 \x01(\x06\"\x98\x02\n\x0cIndexPostfix\x12G\n\x0bindex_value\x18\x01 \x03(\x0b\x32\x32.storage_onestore_v3_bytes.IndexPostfix.IndexValue\x12\x31\n\x03key\x18\x02 \x01(\x0b\x32$.storage_onestore_v3_bytes.Reference\x12\x14\n\x06\x62\x65\x66ore\x18\x03 \x01(\x08:\x04true\x12\x18\n\x10\x62\x65\x66ore_ascending\x18\x04 \x01(\x08\x1a\\\n\nIndexValue\x12\x15\n\rproperty_name\x18\x01 \x02(\t\x12\x37\n\x05value\x18\x02 \x02(\x0b\x32(.storage_onestore_v3_bytes.PropertyValue\"L\n\rIndexPosition\x12\x0b\n\x03key\x18\x01 \x01(\x0c\x12\x14\n\x06\x62\x65\x66ore\x18\x02 \x01(\x08:\x04true\x12\x18\n\x10\x62\x65\x66ore_ascending\x18\x03 \x01(\x08\x42\x45\n\x1e\x63om.google.storage.onestore.v3B\x0eOnestoreEntityZ\x13storage_onestore_v3')



_PROPERTYVALUE = DESCRIPTOR.message_types_by_name['PropertyValue']
_PROPERTYVALUE_POINTVALUE = _PROPERTYVALUE.nested_types_by_name['PointValue']
_PROPERTYVALUE_USERVALUE = _PROPERTYVALUE.nested_types_by_name['UserValue']
_PROPERTYVALUE_REFERENCEVALUE = _PROPERTYVALUE.nested_types_by_name['ReferenceValue']
_PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT = _PROPERTYVALUE_REFERENCEVALUE.nested_types_by_name['PathElement']
_PROPERTY = DESCRIPTOR.message_types_by_name['Property']
_PATH = DESCRIPTOR.message_types_by_name['Path']
_PATH_ELEMENT = _PATH.nested_types_by_name['Element']
_REFERENCE = DESCRIPTOR.message_types_by_name['Reference']
_USER = DESCRIPTOR.message_types_by_name['User']
_ENTITYPROTO = DESCRIPTOR.message_types_by_name['EntityProto']
_ENTITYMETADATA = DESCRIPTOR.message_types_by_name['EntityMetadata']
_ENTITYSUMMARY = DESCRIPTOR.message_types_by_name['EntitySummary']
_ENTITYSUMMARY_PROPERTYSUMMARY = _ENTITYSUMMARY.nested_types_by_name['PropertySummary']
_COMPOSITEPROPERTY = DESCRIPTOR.message_types_by_name['CompositeProperty']
_INDEX = DESCRIPTOR.message_types_by_name['Index']
_INDEX_PROPERTY = _INDEX.nested_types_by_name['Property']
_COMPOSITEINDEX = DESCRIPTOR.message_types_by_name['CompositeIndex']
_SEARCHINDEXENTRY = DESCRIPTOR.message_types_by_name['SearchIndexEntry']
_INDEXPOSTFIX = DESCRIPTOR.message_types_by_name['IndexPostfix']
_INDEXPOSTFIX_INDEXVALUE = _INDEXPOSTFIX.nested_types_by_name['IndexValue']
_INDEXPOSITION = DESCRIPTOR.message_types_by_name['IndexPosition']
_PROPERTY_MEANING = _PROPERTY.enum_types_by_name['Meaning']
_ENTITYPROTO_KIND = _ENTITYPROTO.enum_types_by_name['Kind']
_INDEX_PROPERTY_DIRECTION = _INDEX_PROPERTY.enum_types_by_name['Direction']
_INDEX_PROPERTY_MODE = _INDEX_PROPERTY.enum_types_by_name['Mode']
_INDEX_VERSION = _INDEX.enum_types_by_name['Version']
_COMPOSITEINDEX_STATE = _COMPOSITEINDEX.enum_types_by_name['State']
_COMPOSITEINDEX_WORKFLOWSTATE = _COMPOSITEINDEX.enum_types_by_name['WorkflowState']
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

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.google.storage.onestore.v3B\016OnestoreEntityZ\023storage_onestore_v3'
  _COMPOSITEINDEX.fields_by_name['workflow_state']._options = None
  _COMPOSITEINDEX.fields_by_name['workflow_state']._serialized_options = b'\030\001'
  _COMPOSITEINDEX.fields_by_name['error_message']._options = None
  _COMPOSITEINDEX.fields_by_name['error_message']._serialized_options = b'\030\001'
  _COMPOSITEINDEX.fields_by_name['only_use_if_required']._options = None
  _COMPOSITEINDEX.fields_by_name['only_use_if_required']._serialized_options = b'\030\001'
  _COMPOSITEINDEX.fields_by_name['disabled_index']._options = None
  _COMPOSITEINDEX.fields_by_name['disabled_index']._serialized_options = b'\030\001'
  _PROPERTYVALUE._serialized_start=77
  _PROPERTYVALUE._serialized_end=822
  _PROPERTYVALUE_POINTVALUE._serialized_start=403
  _PROPERTYVALUE_POINTVALUE._serialized_end=437
  _PROPERTYVALUE_USERVALUE._serialized_start=440
  _PROPERTYVALUE_USERVALUE._serialized_end=604
  _PROPERTYVALUE_REFERENCEVALUE._serialized_start=607
  _PROPERTYVALUE_REFERENCEVALUE._serialized_end=822
  _PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT._serialized_start=769
  _PROPERTYVALUE_REFERENCEVALUE_PATHELEMENT._serialized_end=822
  _PROPERTY._serialized_start=825
  _PROPERTY._serialized_end=1409
  _PROPERTY_MEANING._serialized_start=1068
  _PROPERTY_MEANING._serialized_end=1409
  _PATH._serialized_start=1411
  _PATH._serialized_end=1526
  _PATH_ELEMENT._serialized_start=1477
  _PATH_ELEMENT._serialized_end=1526
  _REFERENCE._serialized_start=1528
  _REFERENCE._serialized_end=1640
  _USER._serialized_start=1643
  _USER._serialized_end=1802
  _ENTITYPROTO._serialized_start=1805
  _ENTITYPROTO._serialized_end=2217
  _ENTITYPROTO_KIND._serialized_start=2165
  _ENTITYPROTO_KIND._serialized_end=2217
  _ENTITYMETADATA._serialized_start=2219
  _ENTITYMETADATA._serialized_end=2285
  _ENTITYSUMMARY._serialized_start=2288
  _ENTITYSUMMARY._serialized_end=2475
  _ENTITYSUMMARY_PROPERTYSUMMARY._serialized_start=2391
  _ENTITYSUMMARY_PROPERTYSUMMARY._serialized_end=2475
  _COMPOSITEPROPERTY._serialized_start=2477
  _COMPOSITEPROPERTY._serialized_end=2529
  _INDEX._serialized_start=2532
  _INDEX._serialized_end=3134
  _INDEX_PROPERTY._serialized_start=2738
  _INDEX_PROPERTY._serialized_end=3074
  _INDEX_PROPERTY_DIRECTION._serialized_start=2939
  _INDEX_PROPERTY_DIRECTION._serialized_end=3008
  _INDEX_PROPERTY_MODE._serialized_start=3010
  _INDEX_PROPERTY_MODE._serialized_end=3074
  _INDEX_VERSION._serialized_start=3076
  _INDEX_VERSION._serialized_end=3134
  _COMPOSITEINDEX._serialized_start=3137
  _COMPOSITEINDEX._serialized_end=3713
  _COMPOSITEINDEX_STATE._serialized_start=3593
  _COMPOSITEINDEX_STATE._serialized_end=3656
  _COMPOSITEINDEX_WORKFLOWSTATE._serialized_start=3658
  _COMPOSITEINDEX_WORKFLOWSTATE._serialized_end=3713
  _SEARCHINDEXENTRY._serialized_start=3715
  _SEARCHINDEXENTRY._serialized_end=3834
  _INDEXPOSTFIX._serialized_start=3837
  _INDEXPOSTFIX._serialized_end=4117
  _INDEXPOSTFIX_INDEXVALUE._serialized_start=4025
  _INDEXPOSTFIX_INDEXVALUE._serialized_end=4117
  _INDEXPOSITION._serialized_start=4119
  _INDEXPOSITION._serialized_end=4195

