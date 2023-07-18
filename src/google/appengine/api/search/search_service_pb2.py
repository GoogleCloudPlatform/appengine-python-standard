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


from google.appengine.datastore import document_pb2 as google_dot_appengine_dot_datastore_dot_document__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0google/appengine/api/search/search_service.proto\x12\x10google.appengine\x1a)google/appengine/datastore/document.proto\"\xa8\x01\n\x12SearchServiceError\"\x91\x01\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x13\n\x0fINVALID_REQUEST\x10\x01\x12\x13\n\x0fTRANSIENT_ERROR\x10\x02\x12\x12\n\x0eINTERNAL_ERROR\x10\x03\x12\x15\n\x11PERMISSION_DENIED\x10\x04\x12\x0b\n\x07TIMEOUT\x10\x05\x12\x1a\n\x16\x43ONCURRENT_TRANSACTION\x10\x06\"{\n\rRequestStatus\x12<\n\x04\x63ode\x18\x01 \x01(\x0e\x32..google.appengine.SearchServiceError.ErrorCode\x12\x14\n\x0c\x65rror_detail\x18\x02 \x01(\t\x12\x16\n\x0e\x63\x61nonical_code\x18\x03 \x01(\x05\"\x8a\x03\n\tIndexSpec\x12\x0c\n\x04name\x18\x01 \x01(\t\x12J\n\x0b\x63onsistency\x18\x02 \x01(\x0e\x32\'.google.appengine.IndexSpec.Consistency:\x0cPER_DOCUMENT\x12\x11\n\tnamespace\x18\x03 \x01(\t\x12\x0f\n\x07version\x18\x04 \x01(\x05\x12:\n\x06source\x18\x05 \x01(\x0e\x32\".google.appengine.IndexSpec.Source:\x06SEARCH\x12\x38\n\x04mode\x18\x06 \x01(\x0e\x32 .google.appengine.IndexSpec.Mode:\x08PRIORITY\"+\n\x0b\x43onsistency\x12\n\n\x06GLOBAL\x10\x00\x12\x10\n\x0cPER_DOCUMENT\x10\x01\"6\n\x06Source\x12\n\n\x06SEARCH\x10\x00\x12\r\n\tDATASTORE\x10\x01\x12\x11\n\rCLOUD_STORAGE\x10\x02\"$\n\x04Mode\x12\x0c\n\x08PRIORITY\x10\x00\x12\x0e\n\nBACKGROUND\x10\x01\"\x8d\x03\n\rIndexMetadata\x12/\n\nindex_spec\x18\x01 \x01(\x0b\x32\x1b.google.appengine.IndexSpec\x12.\n\x05\x66ield\x18\x02 \x03(\x0b\x32\x1f.storage_onestore_v3.FieldTypes\x12\x38\n\x07storage\x18\x03 \x01(\x0b\x32\'.google.appengine.IndexMetadata.Storage\x12G\n\x0bindex_state\x18\x04 \x01(\x0e\x32*.google.appengine.IndexMetadata.IndexState:\x06\x41\x43TIVE\x12\x19\n\x11index_delete_time\x18\x05 \x01(\x03\x12\x15\n\nnum_shards\x18\x06 \x01(\x05:\x01\x31\x1a-\n\x07Storage\x12\x13\n\x0b\x61mount_used\x18\x01 \x01(\x03\x12\r\n\x05limit\x18\x02 \x01(\x03\"7\n\nIndexState\x12\n\n\x06\x41\x43TIVE\x10\x00\x12\x10\n\x0cSOFT_DELETED\x10\x01\x12\x0b\n\x07PURGING\x10\x02\"\x83\x02\n\x13IndexDocumentParams\x12/\n\x08\x64ocument\x18\x01 \x03(\x0b\x32\x1d.storage_onestore_v3.Document\x12U\n\tfreshness\x18\x02 \x01(\x0e\x32/.google.appengine.IndexDocumentParams.Freshness:\rSYNCHRONOUSLYB\x02\x18\x01\x12/\n\nindex_spec\x18\x03 \x01(\x0b\x32\x1b.google.appengine.IndexSpec\"3\n\tFreshness\x12\x11\n\rSYNCHRONOUSLY\x10\x00\x12\x13\n\x0fWHEN_CONVENIENT\x10\x01\"]\n\x14IndexDocumentRequest\x12\x35\n\x06params\x18\x01 \x01(\x0b\x32%.google.appengine.IndexDocumentParams\x12\x0e\n\x06\x61pp_id\x18\x03 \x01(\x0c\"`\n\x15IndexDocumentResponse\x12/\n\x06status\x18\x01 \x03(\x0b\x32\x1f.google.appengine.RequestStatus\x12\x0e\n\x06\x64oc_id\x18\x02 \x03(\t*\x06\x08\xe8\x07\x10\x90N\"W\n\x14\x44\x65leteDocumentParams\x12\x0e\n\x06\x64oc_id\x18\x01 \x03(\t\x12/\n\nindex_spec\x18\x02 \x01(\x0b\x32\x1b.google.appengine.IndexSpec\"_\n\x15\x44\x65leteDocumentRequest\x12\x36\n\x06params\x18\x01 \x01(\x0b\x32&.google.appengine.DeleteDocumentParams\x12\x0e\n\x06\x61pp_id\x18\x03 \x01(\x0c\"I\n\x16\x44\x65leteDocumentResponse\x12/\n\x06status\x18\x01 \x03(\x0b\x32\x1f.google.appengine.RequestStatus\"\xa4\x01\n\x13ListDocumentsParams\x12/\n\nindex_spec\x18\x01 \x01(\x0b\x32\x1b.google.appengine.IndexSpec\x12\x14\n\x0cstart_doc_id\x18\x02 \x01(\t\x12\x1f\n\x11include_start_doc\x18\x03 \x01(\x08:\x04true\x12\x12\n\x05limit\x18\x04 \x01(\x05:\x03\x31\x30\x30\x12\x11\n\tkeys_only\x18\x05 \x01(\x08\"]\n\x14ListDocumentsRequest\x12\x35\n\x06params\x18\x01 \x01(\x0b\x32%.google.appengine.ListDocumentsParams\x12\x0e\n\x06\x61pp_id\x18\x02 \x01(\x0c\"y\n\x15ListDocumentsResponse\x12/\n\x06status\x18\x01 \x01(\x0b\x32\x1f.google.appengine.RequestStatus\x12/\n\x08\x64ocument\x18\x02 \x03(\x0b\x32\x1d.storage_onestore_v3.Document\"D\n\x11\x44\x65leteIndexParams\x12/\n\nindex_spec\x18\x01 \x01(\x0b\x32\x1b.google.appengine.IndexSpec\"Y\n\x12\x44\x65leteIndexRequest\x12\x33\n\x06params\x18\x01 \x01(\x0b\x32#.google.appengine.DeleteIndexParams\x12\x0e\n\x06\x61pp_id\x18\x02 \x01(\x0c\"F\n\x13\x44\x65leteIndexResponse\x12/\n\x06status\x18\x01 \x01(\x0b\x32\x1f.google.appengine.RequestStatus\"J\n\x17\x43\x61ncelDeleteIndexParams\x12/\n\nindex_spec\x18\x01 \x01(\x0b\x32\x1b.google.appengine.IndexSpec\"e\n\x18\x43\x61ncelDeleteIndexRequest\x12\x39\n\x06params\x18\x01 \x01(\x0b\x32).google.appengine.CancelDeleteIndexParams\x12\x0e\n\x06\x61pp_id\x18\x02 \x01(\x0c\"L\n\x19\x43\x61ncelDeleteIndexResponse\x12/\n\x06status\x18\x01 \x01(\x0b\x32\x1f.google.appengine.RequestStatus\"\x8b\x02\n\x11ListIndexesParams\x12\x14\n\x0c\x66\x65tch_schema\x18\x01 \x01(\x08\x12\x11\n\x05limit\x18\x02 \x01(\x05:\x02\x32\x30\x12\x11\n\tnamespace\x18\x03 \x01(\t\x12\x18\n\x10start_index_name\x18\x04 \x01(\t\x12!\n\x13include_start_index\x18\x05 \x01(\x08:\x04true\x12\x19\n\x11index_name_prefix\x18\x06 \x01(\t\x12\x0e\n\x06offset\x18\x07 \x01(\x05\x12:\n\x06source\x18\x08 \x01(\x0e\x32\".google.appengine.IndexSpec.Source:\x06SEARCH\x12\x16\n\x0e\x61ll_namespaces\x18\t \x01(\x08\"Y\n\x12ListIndexesRequest\x12\x33\n\x06params\x18\x01 \x01(\x0b\x32#.google.appengine.ListIndexesParams\x12\x0e\n\x06\x61pp_id\x18\x03 \x01(\x0c\"\x7f\n\x13ListIndexesResponse\x12/\n\x06status\x18\x01 \x01(\x0b\x32\x1f.google.appengine.RequestStatus\x12\x37\n\x0eindex_metadata\x18\x02 \x03(\x0b\x32\x1f.google.appengine.IndexMetadata\"\x9e\x01\n\x12\x44\x65leteSchemaParams\x12:\n\x06source\x18\x01 \x01(\x0e\x32\".google.appengine.IndexSpec.Source:\x06SEARCH\x12/\n\nindex_spec\x18\x02 \x03(\x0b\x32\x1b.google.appengine.IndexSpec\x12\x1b\n\x13require_empty_index\x18\x03 \x01(\x08\"[\n\x13\x44\x65leteSchemaRequest\x12\x34\n\x06params\x18\x01 \x01(\x0b\x32$.google.appengine.DeleteSchemaParams\x12\x0e\n\x06\x61pp_id\x18\x03 \x01(\x0c\"G\n\x14\x44\x65leteSchemaResponse\x12/\n\x06status\x18\x01 \x03(\x0b\x32\x1f.google.appengine.RequestStatus\"}\n\x08SortSpec\x12\x17\n\x0fsort_expression\x18\x01 \x01(\t\x12\x1d\n\x0fsort_descending\x18\x02 \x01(\x08:\x04true\x12\x1a\n\x12\x64\x65\x66\x61ult_value_text\x18\x04 \x01(\t\x12\x1d\n\x15\x64\x65\x66\x61ult_value_numeric\x18\x05 \x01(\x01\"\xbd\x01\n\nScorerSpec\x12\x41\n\x06scorer\x18\x01 \x01(\x0e\x32#.google.appengine.ScorerSpec.Scorer:\x0cMATCH_SCORER\x12\x13\n\x05limit\x18\x02 \x01(\x05:\x04\x31\x30\x30\x30\x12\x1f\n\x17match_scorer_parameters\x18\t \x01(\t\"6\n\x06Scorer\x12\x1a\n\x16RESCORING_MATCH_SCORER\x10\x00\x12\x10\n\x0cMATCH_SCORER\x10\x02\"\x85\x01\n\tFieldSpec\x12\x0c\n\x04name\x18\x01 \x03(\t\x12:\n\nexpression\x18\x02 \x03(\n2&.google.appengine.FieldSpec.Expression\x1a.\n\nExpression\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nexpression\x18\x04 \x01(\t\"6\n\nFacetRange\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05start\x18\x02 \x01(\t\x12\x0b\n\x03\x65nd\x18\x03 \x01(\t\"o\n\x11\x46\x61\x63\x65tRequestParam\x12\x13\n\x0bvalue_limit\x18\x01 \x01(\x05\x12+\n\x05range\x18\x02 \x03(\x0b\x32\x1c.google.appengine.FacetRange\x12\x18\n\x10value_constraint\x18\x03 \x03(\t\"/\n\x14\x46\x61\x63\x65tAutoDetectParam\x12\x17\n\x0bvalue_limit\x18\x01 \x01(\x05:\x02\x31\x30\"Q\n\x0c\x46\x61\x63\x65tRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x33\n\x06params\x18\x02 \x01(\x0b\x32#.google.appengine.FacetRequestParam\"\x8b\x01\n\x0f\x46\x61\x63\x65tRefinement\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x36\n\x05range\x18\x03 \x01(\x0b\x32\'.google.appengine.FacetRefinement.Range\x1a#\n\x05Range\x12\r\n\x05start\x18\x01 \x01(\t\x12\x0b\n\x03\x65nd\x18\x02 \x01(\t\"\xd6\x06\n\x0cSearchParams\x12/\n\nindex_spec\x18\x01 \x01(\x0b\x32\x1b.google.appengine.IndexSpec\x12\r\n\x05query\x18\x02 \x01(\t\x12\x0e\n\x06\x63ursor\x18\x04 \x01(\t\x12\x0e\n\x06offset\x18\x0b \x01(\x05\x12\x44\n\x0b\x63ursor_type\x18\x05 \x01(\x0e\x32).google.appengine.SearchParams.CursorType:\x04NONE\x12\x11\n\x05limit\x18\x06 \x01(\x05:\x02\x32\x30\x12\x1e\n\x16matched_count_accuracy\x18\x07 \x01(\x05\x12-\n\tsort_spec\x18\x08 \x03(\x0b\x32\x1a.google.appengine.SortSpec\x12\x31\n\x0bscorer_spec\x18\t \x01(\x0b\x32\x1c.google.appengine.ScorerSpec\x12/\n\nfield_spec\x18\n \x01(\x0b\x32\x1b.google.appengine.FieldSpec\x12\x11\n\tkeys_only\x18\x0c \x01(\x08\x12H\n\x0cparsing_mode\x18\r \x01(\x0e\x32*.google.appengine.SearchParams.ParsingMode:\x06STRICT\x12$\n\x19\x61uto_discover_facet_count\x18\x0f \x01(\x05:\x01\x30\x12\x35\n\rinclude_facet\x18\x10 \x03(\x0b\x32\x1e.google.appengine.FacetRequest\x12;\n\x10\x66\x61\x63\x65t_refinement\x18\x11 \x03(\x0b\x32!.google.appengine.FacetRefinement\x12G\n\x17\x66\x61\x63\x65t_auto_detect_param\x18\x12 \x01(\x0b\x32&.google.appengine.FacetAutoDetectParam\x12\x19\n\x0b\x66\x61\x63\x65t_depth\x18\x13 \x01(\x05:\x04\x31\x30\x30\x30\x12#\n\x14\x65nable_query_rewrite\x18\x14 \x01(\x08:\x05\x66\x61lse\"2\n\nCursorType\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06SINGLE\x10\x01\x12\x0e\n\nPER_RESULT\x10\x02\"&\n\x0bParsingMode\x12\n\n\x06STRICT\x10\x00\x12\x0b\n\x07RELAXED\x10\x01\"O\n\rSearchRequest\x12.\n\x06params\x18\x01 \x01(\x0b\x32\x1e.google.appengine.SearchParams\x12\x0e\n\x06\x61pp_id\x18\x03 \x01(\x0c\"f\n\x10\x46\x61\x63\x65tResultValue\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05\x63ount\x18\x02 \x01(\x05\x12\x35\n\nrefinement\x18\x03 \x01(\x0b\x32!.google.appengine.FacetRefinement\"N\n\x0b\x46\x61\x63\x65tResult\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x31\n\x05value\x18\x02 \x03(\x0b\x32\".google.appengine.FacetResultValue\"\x8e\x01\n\x0cSearchResult\x12/\n\x08\x64ocument\x18\x01 \x01(\x0b\x32\x1d.storage_onestore_v3.Document\x12.\n\nexpression\x18\x04 \x03(\x0b\x32\x1a.storage_onestore_v3.Field\x12\r\n\x05score\x18\x02 \x03(\x01\x12\x0e\n\x06\x63ursor\x18\x03 \x01(\t\"\xea\x01\n\x0eSearchResponse\x12.\n\x06result\x18\x01 \x03(\x0b\x32\x1e.google.appengine.SearchResult\x12\x15\n\rmatched_count\x18\x02 \x01(\x03\x12/\n\x06status\x18\x03 \x01(\x0b\x32\x1f.google.appengine.RequestStatus\x12\x0e\n\x06\x63ursor\x18\x04 \x01(\t\x12\x33\n\x0c\x66\x61\x63\x65t_result\x18\x05 \x03(\x0b\x32\x1d.google.appengine.FacetResult\x12\x13\n\x0b\x64ocs_scored\x18\x06 \x01(\x05*\x06\x08\xe8\x07\x10\x90NB8\n%com.google.appengine.api.search.protoB\x0fSearchServicePb')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.appengine.api.search.search_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.google.appengine.api.search.protoB\017SearchServicePb'
  _INDEXDOCUMENTPARAMS.fields_by_name['freshness']._options = None
  _INDEXDOCUMENTPARAMS.fields_by_name['freshness']._serialized_options = b'\030\001'
  _globals['_SEARCHSERVICEERROR']._serialized_start=114
  _globals['_SEARCHSERVICEERROR']._serialized_end=282
  _globals['_SEARCHSERVICEERROR_ERRORCODE']._serialized_start=137
  _globals['_SEARCHSERVICEERROR_ERRORCODE']._serialized_end=282
  _globals['_REQUESTSTATUS']._serialized_start=284
  _globals['_REQUESTSTATUS']._serialized_end=407
  _globals['_INDEXSPEC']._serialized_start=410
  _globals['_INDEXSPEC']._serialized_end=804
  _globals['_INDEXSPEC_CONSISTENCY']._serialized_start=667
  _globals['_INDEXSPEC_CONSISTENCY']._serialized_end=710
  _globals['_INDEXSPEC_SOURCE']._serialized_start=712
  _globals['_INDEXSPEC_SOURCE']._serialized_end=766
  _globals['_INDEXSPEC_MODE']._serialized_start=768
  _globals['_INDEXSPEC_MODE']._serialized_end=804
  _globals['_INDEXMETADATA']._serialized_start=807
  _globals['_INDEXMETADATA']._serialized_end=1204
  _globals['_INDEXMETADATA_STORAGE']._serialized_start=1102
  _globals['_INDEXMETADATA_STORAGE']._serialized_end=1147
  _globals['_INDEXMETADATA_INDEXSTATE']._serialized_start=1149
  _globals['_INDEXMETADATA_INDEXSTATE']._serialized_end=1204
  _globals['_INDEXDOCUMENTPARAMS']._serialized_start=1207
  _globals['_INDEXDOCUMENTPARAMS']._serialized_end=1466
  _globals['_INDEXDOCUMENTPARAMS_FRESHNESS']._serialized_start=1415
  _globals['_INDEXDOCUMENTPARAMS_FRESHNESS']._serialized_end=1466
  _globals['_INDEXDOCUMENTREQUEST']._serialized_start=1468
  _globals['_INDEXDOCUMENTREQUEST']._serialized_end=1561
  _globals['_INDEXDOCUMENTRESPONSE']._serialized_start=1563
  _globals['_INDEXDOCUMENTRESPONSE']._serialized_end=1659
  _globals['_DELETEDOCUMENTPARAMS']._serialized_start=1661
  _globals['_DELETEDOCUMENTPARAMS']._serialized_end=1748
  _globals['_DELETEDOCUMENTREQUEST']._serialized_start=1750
  _globals['_DELETEDOCUMENTREQUEST']._serialized_end=1845
  _globals['_DELETEDOCUMENTRESPONSE']._serialized_start=1847
  _globals['_DELETEDOCUMENTRESPONSE']._serialized_end=1920
  _globals['_LISTDOCUMENTSPARAMS']._serialized_start=1923
  _globals['_LISTDOCUMENTSPARAMS']._serialized_end=2087
  _globals['_LISTDOCUMENTSREQUEST']._serialized_start=2089
  _globals['_LISTDOCUMENTSREQUEST']._serialized_end=2182
  _globals['_LISTDOCUMENTSRESPONSE']._serialized_start=2184
  _globals['_LISTDOCUMENTSRESPONSE']._serialized_end=2305
  _globals['_DELETEINDEXPARAMS']._serialized_start=2307
  _globals['_DELETEINDEXPARAMS']._serialized_end=2375
  _globals['_DELETEINDEXREQUEST']._serialized_start=2377
  _globals['_DELETEINDEXREQUEST']._serialized_end=2466
  _globals['_DELETEINDEXRESPONSE']._serialized_start=2468
  _globals['_DELETEINDEXRESPONSE']._serialized_end=2538
  _globals['_CANCELDELETEINDEXPARAMS']._serialized_start=2540
  _globals['_CANCELDELETEINDEXPARAMS']._serialized_end=2614
  _globals['_CANCELDELETEINDEXREQUEST']._serialized_start=2616
  _globals['_CANCELDELETEINDEXREQUEST']._serialized_end=2717
  _globals['_CANCELDELETEINDEXRESPONSE']._serialized_start=2719
  _globals['_CANCELDELETEINDEXRESPONSE']._serialized_end=2795
  _globals['_LISTINDEXESPARAMS']._serialized_start=2798
  _globals['_LISTINDEXESPARAMS']._serialized_end=3065
  _globals['_LISTINDEXESREQUEST']._serialized_start=3067
  _globals['_LISTINDEXESREQUEST']._serialized_end=3156
  _globals['_LISTINDEXESRESPONSE']._serialized_start=3158
  _globals['_LISTINDEXESRESPONSE']._serialized_end=3285
  _globals['_DELETESCHEMAPARAMS']._serialized_start=3288
  _globals['_DELETESCHEMAPARAMS']._serialized_end=3446
  _globals['_DELETESCHEMAREQUEST']._serialized_start=3448
  _globals['_DELETESCHEMAREQUEST']._serialized_end=3539
  _globals['_DELETESCHEMARESPONSE']._serialized_start=3541
  _globals['_DELETESCHEMARESPONSE']._serialized_end=3612
  _globals['_SORTSPEC']._serialized_start=3614
  _globals['_SORTSPEC']._serialized_end=3739
  _globals['_SCORERSPEC']._serialized_start=3742
  _globals['_SCORERSPEC']._serialized_end=3931
  _globals['_SCORERSPEC_SCORER']._serialized_start=3877
  _globals['_SCORERSPEC_SCORER']._serialized_end=3931
  _globals['_FIELDSPEC']._serialized_start=3934
  _globals['_FIELDSPEC']._serialized_end=4067
  _globals['_FIELDSPEC_EXPRESSION']._serialized_start=4021
  _globals['_FIELDSPEC_EXPRESSION']._serialized_end=4067
  _globals['_FACETRANGE']._serialized_start=4069
  _globals['_FACETRANGE']._serialized_end=4123
  _globals['_FACETREQUESTPARAM']._serialized_start=4125
  _globals['_FACETREQUESTPARAM']._serialized_end=4236
  _globals['_FACETAUTODETECTPARAM']._serialized_start=4238
  _globals['_FACETAUTODETECTPARAM']._serialized_end=4285
  _globals['_FACETREQUEST']._serialized_start=4287
  _globals['_FACETREQUEST']._serialized_end=4368
  _globals['_FACETREFINEMENT']._serialized_start=4371
  _globals['_FACETREFINEMENT']._serialized_end=4510
  _globals['_FACETREFINEMENT_RANGE']._serialized_start=4475
  _globals['_FACETREFINEMENT_RANGE']._serialized_end=4510
  _globals['_SEARCHPARAMS']._serialized_start=4513
  _globals['_SEARCHPARAMS']._serialized_end=5367
  _globals['_SEARCHPARAMS_CURSORTYPE']._serialized_start=5277
  _globals['_SEARCHPARAMS_CURSORTYPE']._serialized_end=5327
  _globals['_SEARCHPARAMS_PARSINGMODE']._serialized_start=5329
  _globals['_SEARCHPARAMS_PARSINGMODE']._serialized_end=5367
  _globals['_SEARCHREQUEST']._serialized_start=5369
  _globals['_SEARCHREQUEST']._serialized_end=5448
  _globals['_FACETRESULTVALUE']._serialized_start=5450
  _globals['_FACETRESULTVALUE']._serialized_end=5552
  _globals['_FACETRESULT']._serialized_start=5554
  _globals['_FACETRESULT']._serialized_end=5632
  _globals['_SEARCHRESULT']._serialized_start=5635
  _globals['_SEARCHRESULT']._serialized_end=5777
  _globals['_SEARCHRESPONSE']._serialized_start=5780
  _globals['_SEARCHRESPONSE']._serialized_end=6014
