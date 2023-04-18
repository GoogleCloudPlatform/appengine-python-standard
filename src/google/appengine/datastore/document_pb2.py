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
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)google/appengine/datastore/document.proto\x12\x13storage_onestore_v3\"\xe9\x02\n\nFieldValue\x12?\n\x04type\x18\x01 \x01(\x0e\x32+.storage_onestore_v3.FieldValue.ContentType:\x04TEXT\x12\x14\n\x08language\x18\x02 \x01(\t:\x02\x65n\x12\x14\n\x0cstring_value\x18\x03 \x01(\t\x12\x30\n\x03geo\x18\x04 \x01(\n2#.storage_onestore_v3.FieldValue.Geo\x12\x14\n\x0cvector_value\x18\x07 \x03(\x01\x1a\x1f\n\x03Geo\x12\x0b\n\x03lat\x18\x05 \x01(\x01\x12\x0b\n\x03lng\x18\x06 \x01(\x01\"\x84\x01\n\x0b\x43ontentType\x12\x08\n\x04TEXT\x10\x00\x12\x08\n\x04HTML\x10\x01\x12\x08\n\x04\x41TOM\x10\x02\x12\x08\n\x04\x44\x41TE\x10\x03\x12\n\n\x06NUMBER\x10\x04\x12\x07\n\x03GEO\x10\x05\x12\x16\n\x12UNTOKENIZED_PREFIX\x10\x06\x12\x14\n\x10TOKENIZED_PREFIX\x10\x07\x12\n\n\x06VECTOR\x10\x08\"E\n\x05\x46ield\x12\x0c\n\x04name\x18\x01 \x01(\t\x12.\n\x05value\x18\x02 \x01(\x0b\x32\x1f.storage_onestore_v3.FieldValue\"U\n\nFieldTypes\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x39\n\x04type\x18\x02 \x03(\x0e\x32+.storage_onestore_v3.FieldValue.ContentType\"\x83\x01\n\x12IndexShardSettings\x12\x17\n\x0fprev_num_shards\x18\x01 \x03(\x05\x12\x15\n\nnum_shards\x18\x02 \x01(\x05:\x01\x31\x12$\n\x1cprev_num_shards_search_false\x18\x03 \x03(\x05\x12\x17\n\rlocal_replica\x18\x04 \x01(\t:\x00\"\xd1\x05\n\rIndexMetadata\x12-\n\x1eis_over_field_number_threshold\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x45\n\x14index_shard_settings\x18\x02 \x01(\x0b\x32\'.storage_onestore_v3.IndexShardSettings\x12J\n\x0bindex_state\x18\x03 \x01(\x0e\x32-.storage_onestore_v3.IndexMetadata.IndexState:\x06\x41\x43TIVE\x12\x19\n\x11index_delete_time\x18\x04 \x01(\x03\x12\x1c\n\x14max_index_size_bytes\x18\x05 \x01(\x03\x12Q\n\x10replica_deletion\x18\x06 \x03(\x0b\x32\x37.storage_onestore_v3.IndexMetadata.IndexDeletionDetails\x1a>\n\x0e\x44\x65letionStatus\x12\x14\n\x0cstarted_time\x18\x03 \x01(\x03\x12\x16\n\x0e\x63ompleted_time\x18\x04 \x01(\x03\x1a\xf8\x01\n\x14IndexDeletionDetails\x12\x14\n\x0creplica_name\x18\x01 \x01(\t\x12\x43\n\x08precheck\x18\x02 \x01(\x0b\x32\x31.storage_onestore_v3.IndexMetadata.DeletionStatus\x12\x41\n\x06st_bti\x18\x03 \x01(\x0b\x32\x31.storage_onestore_v3.IndexMetadata.DeletionStatus\x12\x42\n\x07ms_docs\x18\x04 \x01(\x0b\x32\x31.storage_onestore_v3.IndexMetadata.DeletionStatus\"7\n\nIndexState\x12\n\n\x06\x41\x43TIVE\x10\x00\x12\x10\n\x0cSOFT_DELETED\x10\x01\x12\x0b\n\x07PURGING\x10\x02\"\x88\x01\n\nFacetValue\x12?\n\x04type\x18\x01 \x01(\x0e\x32+.storage_onestore_v3.FacetValue.ContentType:\x04\x41TOM\x12\x14\n\x0cstring_value\x18\x03 \x01(\t\"#\n\x0b\x43ontentType\x12\x08\n\x04\x41TOM\x10\x02\x12\n\n\x06NUMBER\x10\x04\"E\n\x05\x46\x61\x63\x65t\x12\x0c\n\x04name\x18\x01 \x01(\t\x12.\n\x05value\x18\x02 \x01(\x0b\x32\x1f.storage_onestore_v3.FacetValue\"A\n\x10\x44ocumentMetadata\x12\x0f\n\x07version\x18\x01 \x01(\x03\x12\x1c\n\x14\x63ommitted_st_version\x18\x02 \x01(\x03\"\xe5\x02\n\x08\x44ocument\x12\n\n\x02id\x18\x01 \x01(\t\x12\x14\n\x08language\x18\x02 \x01(\t:\x02\x65n\x12)\n\x05\x66ield\x18\x03 \x03(\x0b\x32\x1a.storage_onestore_v3.Field\x12\x10\n\x08order_id\x18\x04 \x01(\x05\x12N\n\x0forder_id_source\x18\x06 \x01(\x0e\x32+.storage_onestore_v3.Document.OrderIdSource:\x08SUPPLIED\x12<\n\x07storage\x18\x05 \x01(\x0e\x32%.storage_onestore_v3.Document.Storage:\x04\x44ISK\x12)\n\x05\x66\x61\x63\x65t\x18\x08 \x03(\x0b\x32\x1a.storage_onestore_v3.Facet\",\n\rOrderIdSource\x12\r\n\tDEFAULTED\x10\x00\x12\x0c\n\x08SUPPLIED\x10\x01\"\x13\n\x07Storage\x12\x08\n\x04\x44ISK\x10\x00\x42\x34\n&com.google.google.appengine.api.searchB\nDocumentPb')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.appengine.datastore.document_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n&com.google.google.appengine.api.searchB\nDocumentPb'
  _globals['_FIELDVALUE']._serialized_start=67
  _globals['_FIELDVALUE']._serialized_end=428
  _globals['_FIELDVALUE_GEO']._serialized_start=262
  _globals['_FIELDVALUE_GEO']._serialized_end=293
  _globals['_FIELDVALUE_CONTENTTYPE']._serialized_start=296
  _globals['_FIELDVALUE_CONTENTTYPE']._serialized_end=428
  _globals['_FIELD']._serialized_start=430
  _globals['_FIELD']._serialized_end=499
  _globals['_FIELDTYPES']._serialized_start=501
  _globals['_FIELDTYPES']._serialized_end=586
  _globals['_INDEXSHARDSETTINGS']._serialized_start=589
  _globals['_INDEXSHARDSETTINGS']._serialized_end=720
  _globals['_INDEXMETADATA']._serialized_start=723
  _globals['_INDEXMETADATA']._serialized_end=1444
  _globals['_INDEXMETADATA_DELETIONSTATUS']._serialized_start=1074
  _globals['_INDEXMETADATA_DELETIONSTATUS']._serialized_end=1136
  _globals['_INDEXMETADATA_INDEXDELETIONDETAILS']._serialized_start=1139
  _globals['_INDEXMETADATA_INDEXDELETIONDETAILS']._serialized_end=1387
  _globals['_INDEXMETADATA_INDEXSTATE']._serialized_start=1389
  _globals['_INDEXMETADATA_INDEXSTATE']._serialized_end=1444
  _globals['_FACETVALUE']._serialized_start=1447
  _globals['_FACETVALUE']._serialized_end=1583
  _globals['_FACETVALUE_CONTENTTYPE']._serialized_start=1548
  _globals['_FACETVALUE_CONTENTTYPE']._serialized_end=1583
  _globals['_FACET']._serialized_start=1585
  _globals['_FACET']._serialized_end=1654
  _globals['_DOCUMENTMETADATA']._serialized_start=1656
  _globals['_DOCUMENTMETADATA']._serialized_end=1721
  _globals['_DOCUMENT']._serialized_start=1724
  _globals['_DOCUMENT']._serialized_end=2081
  _globals['_DOCUMENT_ORDERIDSOURCE']._serialized_start=2016
  _globals['_DOCUMENT_ORDERIDSOURCE']._serialized_end=2060
  _globals['_DOCUMENT_STORAGE']._serialized_start=2062
  _globals['_DOCUMENT_STORAGE']._serialized_end=2081

