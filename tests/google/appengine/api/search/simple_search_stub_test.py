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
"""Tests for google.appengine.api.search.simple_search_stub."""

import base64
import bisect
import datetime
import hashlib
import math
import os

from absl import app
from absl import flags
import six
from six.moves import range
from six.moves import zip

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import module_testutil
from google.appengine.api import namespace_manager
from google.appengine.api.search import search
from google.appengine.api.search import search_service_pb2
from google.appengine.api.search import search_util
from google.appengine.api.search import simple_search_stub
from google.appengine.api.search.stub import simple_tokenizer
from google.appengine.api.search.stub import tokens as token_module
from google.appengine.runtime import apiproxy_errors
from google.appengine.datastore import document_pb2
from absl.testing import absltest


class ModuleInterfaceTest(module_testutil.ModuleInterfaceTest,
                          absltest.TestCase):
  """Test the module interface for consistency."""
  MODULE = simple_search_stub


class PostingTest(absltest.TestCase):

  def testInit(self):
    posting = simple_search_stub.Posting(doc_id='doc_id')
    self.assertEqual('doc_id', posting.doc_id)
    self.assertTrue(not posting.positions)

  def testAddPosition(self):
    posting = simple_search_stub.Posting(doc_id='doc_id')
    posting.AddPosition(10)
    self.assertEqual([10], posting.positions)
    posting.AddPosition(4)
    self.assertEqual([4, 10], posting.positions)
    posting.AddPosition(4)
    self.assertEqual([4, 10], posting.positions)
    posting.AddPosition(12)
    self.assertEqual([4, 10, 12], posting.positions)

  def testRemovePosition(self):
    posting = simple_search_stub.Posting(doc_id='doc_id')
    self.assertEqual([], posting.positions)
    posting.RemovePosition(3)
    self.assertEqual([], posting.positions)
    posting.AddPosition(3)
    posting.AddPosition(1)
    posting.AddPosition(2)
    self.assertEqual([1, 2, 3], posting.positions)
    posting.RemovePosition(2)
    self.assertEqual([1, 3], posting.positions)
    posting.RemovePosition(0)
    self.assertEqual([1, 3], posting.positions)

  def testCmp(self):
    posting1 = simple_search_stub.Posting(doc_id='doc_id1')
    posting2 = simple_search_stub.Posting(doc_id='doc_id2')
    posting3 = simple_search_stub.Posting(doc_id='doc_id3')
    self.assertTrue(posting1 < posting2 < posting3)
    posting2a = simple_search_stub.Posting(doc_id='doc_id2')
    posting2a.AddPosition(9)
    self.assertEqual(posting2, posting2a)


class DocumentStatisticsTest(absltest.TestCase):
  def setUp(self):
    self.doc_stats = simple_search_stub._DocumentStatistics()

  def testAddRemove(self):
    self.doc_stats.IncrementTermCount('abc')
    self.assertEqual(1, self.doc_stats.TermFrequency('abc'))

    self.doc_stats.IncrementTermCount('abc')
    self.assertEqual(2, self.doc_stats.TermFrequency('abc'))

    self.doc_stats.IncrementTermCount('efg')
    self.assertEqual(2, self.doc_stats.TermFrequency('abc'))
    self.assertEqual(1, self.doc_stats.TermFrequency('efg'))


class PostingListTest(absltest.TestCase):
  def setUp(self):
    self.posting_list = simple_search_stub.PostingList()

  def PositionsOfTokenInDoc(self, doc_id):
    """Returns all positions that some token occurs in doc for doc_id."""
    posting = simple_search_stub.Posting(doc_id=doc_id)
    pos = bisect.bisect_left(self.posting_list.postings, posting)
    if pos < len(self.posting_list.postings) and self.posting_list.postings[
        pos].doc_id == posting.doc_id:
      return self.posting_list.postings[pos].positions
    return []

  def testAddRemove(self):
    doc_id1 = 'pl_doc_id1'
    doc_id2 = 'pl_doc_id2'
    self.posting_list.Add(doc_id1, 0)
    self.posting_list.Add(doc_id1, 7)
    self.posting_list.Add(doc_id1, 5)
    self.posting_list.Add(doc_id2, 3)
    self.posting_list.Add(doc_id2, 1)
    self.assertEqual([0, 5, 7], self.PositionsOfTokenInDoc(doc_id1))
    self.assertEqual([1, 3], self.PositionsOfTokenInDoc(doc_id2))


class RamInvertedIndexTest(absltest.TestCase):

  def setUp(self):
    self.inverted_index = simple_search_stub.RamInvertedIndex(
        simple_tokenizer.SimpleTokenizer())

  def MakeDocument(self, doc_id, field_name, value):
    return self.MakeTypedDocument(doc_id, field_name,
                                  document_pb2.FieldValue.TEXT, value)

  def MakeTypedDocument(self, doc_id, field_name, field_type, value):
    doc = document_pb2.Document()
    doc.id = doc_id
    field = doc.field.add()
    field.name = field_name
    field_value = field.value
    field_value.type = field_type
    field_value.string_value = str(value)
    return doc

  def CheckTokenPosition(self, doc_id, token):
    postings = self.inverted_index.GetPostingsForToken(token)
    self.assertLen(postings, 1)
    self.assertEqual(doc_id, postings[0].doc_id)
    self.assertEqual([token.position], postings[0].positions)

  def testAddDocument(self):
    doc = self.MakeDocument('doc_id', 'field', 'a b c')
    self.inverted_index.AddDocument('doc_id', doc)
    tokens = [token_module.Token(chars='a', position=0),
              token_module.Token(chars='b', position=1),
              token_module.Token(chars='c', position=2)]
    for token in tokens:
      self.CheckTokenPosition('doc_id', token)
    self.assertEqual(1, self.inverted_index.document_count)

    self.inverted_index.RemoveDocument(doc)
    for token in tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    self.assertEqual(0, self.inverted_index.document_count)

  def testAddDocument_html(self):
    doc = self.MakeTypedDocument('doc_id', 'field',
                                 document_pb2.FieldValue.HTML,
                                 '<HTML>Hello World</HTML>')
    self.inverted_index.AddDocument('doc_id', doc)
    tokens = [token_module.Token(chars='hello', position=0),
              token_module.Token(chars='world', position=1)]
    for token in tokens:
      self.CheckTokenPosition('doc_id', token)
    self.assertEqual(1, self.inverted_index.document_count)

    self.inverted_index.RemoveDocument(doc)
    for token in tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    self.assertEqual(0, self.inverted_index.document_count)

  def testAddDocumentNumberField(self):
    doc = self.MakeTypedDocument('doc_id', 'field',
                                 document_pb2.FieldValue.NUMBER, 999.99)
    self.inverted_index.AddDocument('doc_id', doc)
    tokens = [token_module.Number(chars=999.99, position=0)]
    for token in tokens:
      self.CheckTokenPosition('doc_id', token)
    self.assertEqual(1, self.inverted_index.document_count)

    self.inverted_index.RemoveDocument(doc)
    for token in tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    self.assertEqual(0, self.inverted_index.document_count)

  def testAddDocumentGeoField(self):
    doc = document_pb2.Document()
    doc.id = 'doc_id'
    field = doc.field.add()
    field.name = 'field'
    field_value = field.value
    field_value.type = document_pb2.FieldValue.GEO
    geo = field_value.geo
    geo.lat = 33.87
    geo.lng = 151.21
    self.inverted_index.AddDocument('doc_id', doc)
    tokens = [token_module.GeoPoint(
        latitude=33.87, longitude=151.21, position=0)]
    for token in tokens:
      self.CheckTokenPosition('doc_id', token)
    self.assertEqual(1, self.inverted_index.document_count)

    self.inverted_index.RemoveDocument(doc)
    for token in tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    self.assertEqual(0, self.inverted_index.document_count)

  def testAddDocumentMultipleTokenOccurrences(self):
    doc = self.MakeDocument('doc_id', 'field', 'c a b a')
    self.inverted_index.AddDocument('doc_id', doc)
    tokens = [token_module.Token(chars='c', position=0),
              token_module.Token(chars='b', position=2)]
    a = token_module.Token(chars='a', position=1)
    for token in tokens:
      self.CheckTokenPosition('doc_id', token)
    self.assertEqual(1, self.inverted_index.document_count)

    postings = self.inverted_index.GetPostingsForToken(a)
    self.assertLen(postings, 1)
    self.assertEqual('doc_id', postings[0].doc_id)
    self.assertEqual([1, 3], postings[0].positions)

    self.inverted_index.RemoveDocument(doc)
    for token in tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    self.assertFalse(self.inverted_index.GetPostingsForToken(a))
    self.assertEqual(0, self.inverted_index.document_count)

  def testAddDocumentAtomField(self):
    doc = self.MakeTypedDocument('doc_id', 'field',
                                 document_pb2.FieldValue.ATOM, 'Foo Bar')
    self.inverted_index.AddDocument('doc_id', doc)
    tokens = [token_module.Token(chars='foo bar', position=0)]
    for token in tokens:
      self.CheckTokenPosition('doc_id', token)
    self.assertEqual(1, self.inverted_index.document_count)

    self.inverted_index.RemoveDocument(doc)
    for token in tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    self.assertEqual(0, self.inverted_index.document_count)

  def testAddDocumentUntokenizedPrefixField(self):
    doc = self.MakeTypedDocument('doc_id', 'field',
                                 document_pb2.FieldValue.UNTOKENIZED_PREFIX,
                                 'Foo Bar')
    self.inverted_index.AddDocument('doc_id', doc)
    prefixes = ['f', 'fo', 'foo', 'foo b', 'foo ba', 'foo bar']
    tokens = [token_module.Token(chars=word, position=0) for word in prefixes]
    restrict_field_tokens = [token.RestrictField('field') for token in tokens]
    self.assertEqual(1, self.inverted_index.document_count)

    for token in tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    for token in restrict_field_tokens:
      self.CheckTokenPosition('doc_id', token)


    self.inverted_index.RemoveDocument(doc)
    for token in restrict_field_tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    self.assertEqual(0, self.inverted_index.document_count)

  def testAddDocumentTokenizedPrefixField(self):
    doc = self.MakeTypedDocument('doc_id', 'field',
                                 document_pb2.FieldValue.TOKENIZED_PREFIX,
                                 'Foo Bar')
    self.inverted_index.AddDocument('doc_id', doc)
    prefixes = [['f', 'fo', 'foo'], ['b', 'ba', 'bar']]
    tokens = []
    for word, i in zip(prefixes, list(range(len(prefixes)))):
      tokens += [token_module.Token(chars=prefix, position=i)
                 for prefix in word]
    restrict_field_tokens = [token.RestrictField('field') for token in tokens]
    self.assertEqual(1, self.inverted_index.document_count)

    for token in tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    for token in restrict_field_tokens:
      self.CheckTokenPosition('doc_id', token)


    self.inverted_index.RemoveDocument(doc)
    for token in restrict_field_tokens:
      self.assertFalse(self.inverted_index.GetPostingsForToken(token))
    self.assertEqual(0, self.inverted_index.document_count)


class SimpleIndexTest(absltest.TestCase):
  def setUp(self):
    self.index = simple_search_stub.SimpleIndex(
        self._MakeIndexSpec('unique_index',
                            search_service_pb2.IndexSpec.GLOBAL))

  def _MakeIndexSpec(self, index_name, consistency):
    index_spec = search_service_pb2.IndexSpec()
    index_spec.name = index_name
    index_spec.consistency = consistency
    return index_spec

  def _CreateDocument(self, doc_id, fields):
    """Returns a document_pb2.Document populated with id and fields."""
    doc = document_pb2.Document()
    search_util.AddFieldsToDocumentPb(doc_id, fields, doc)
    return doc

  def testTermFrequency(self):
    doc = self._CreateDocument('testid', [('foo', 'bar')])
    self.assertEqual(1, self.index._TermFrequency('bar', doc))
    doc = self._CreateDocument('testid', [('foo', 'bar bar')])
    self.assertEqual(2, self.index._TermFrequency('bar', doc))
    doc = self._CreateDocument('testid', [('foo', 'bar ' * 100)])
    self.assertEqual(100, self.index._TermFrequency('bar', doc))

    doc = self._CreateDocument('testid', [('foo', 'bar fuzz')])
    self.assertEqual(1, self.index._TermFrequency('bar', doc))
    doc = self._CreateDocument('testid', [('foo', 'bar fuzz ' * 100)])
    self.assertEqual(100, self.index._TermFrequency('bar', doc))

  def testAddRemoveDocuments(self):
    docs = [self._CreateDocument('testid', [('foo', 'bar')])]
    response = search_service_pb2.IndexDocumentResponse()
    self.index.IndexDocuments(docs, response)
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    response = search_service_pb2.DeleteDocumentResponse()
    self.index.DeleteDocuments(['testid'], response)
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)

  def testStatistics(self):
    doc = self._CreateDocument('testid', [('foo', 'bar')])
    docs = [doc]
    response = search_service_pb2.IndexDocumentResponse()
    self.index.IndexDocuments(docs, response)

    self.assertEqual(1, self.index.document_count)
    self.assertEqual(1, self.index._DocumentCountForTerm('bar'))
    tf = 1
    self.assertEqual(tf, self.index._TermFrequency('bar', doc))
    idf = math.log10(1)
    self.assertEqual(idf, self.index._InverseDocumentFrequency('bar'))
    self.assertEqual(
        tf * idf,
        self.index._ScoreDocument(document=doc, score=True, terms=['bar']))

  def testStatistics_largerDoc(self):
    doc = self._CreateDocument('testid', [('foo', 'foo bar ' * 1000)])
    docs = [doc]
    response = search_service_pb2.IndexDocumentResponse()
    self.index.IndexDocuments(docs, response)

    self.assertEqual(1, self.index.document_count)
    self.assertEqual(1, self.index._DocumentCountForTerm('bar'))
    tf = 1000
    self.assertEqual(tf, self.index._TermFrequency('bar', doc))
    idf = math.log10(1)
    self.assertEqual(idf, self.index._InverseDocumentFrequency('bar'))
    self.assertEqual(
        tf * idf,
        self.index._ScoreDocument(document=doc, score=True, terms=['bar']))


class SimpleSearchStubTest(absltest.TestCase):

  def setUp(self):
    """Set up simple search stub."""
    super(SimpleSearchStubTest, self).setUp()
    self.stub = simple_search_stub.SearchServiceStub()
    self.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    apiproxy_stub_map.apiproxy = self.apiproxy
    apiproxy_stub_map.apiproxy.RegisterStub('search', self.stub)

    filename = os.path.join(flags.FLAGS.test_tmpdir, 'search_stub_test_index')

    if os.path.exists(filename):
      os.remove(filename)

  def _AddDocumentToRequest(self, doc_id, fields, params):
    """Add a new document into IndexDocumentParams.

    Args:
      doc_id: The document id.
      fields: List of tuples of field name, value and optionally type.
      params: IndexDocumentParams proto to be stored.
    """
    search_util.AddFieldsToDocumentPb(doc_id, fields, params.document.add())

  def _MakeIndexSpec(self, index_name, consistency):
    index_spec = search_service_pb2.IndexSpec()
    index_spec.name = index_name
    index_spec.consistency = consistency
    return index_spec

  def _SetIndexSpec(self, index, index_spec_pb, namespace=None):
    if isinstance(index, six.string_types):
      index_spec_pb.name = index
      index_spec_pb.consistency = search_service_pb2.IndexSpec.GLOBAL
      if namespace:
        index_spec_pb.namespace = namespace
    else:
      index_spec_pb.MergeFrom(index)

  def _IndexDocument(self, index, doc_id, fields, namespace=None):
    """Make a call to IndexDocument.

    Args:
      index: The name or IndexSpec of the index to be stored.
      doc_id: The document id.
      fields: List of tuples of field name, value and optionally type.
      namespace: The namespace of the index where the document will be stored.
    Returns:
      A IndexDocumentResponse instance for the call.
    """
    request = search_service_pb2.IndexDocumentRequest()
    self._AddDocumentToRequest(doc_id, fields, request.params)
    self._SetIndexSpec(index, request.params.index_spec, namespace=namespace)
    response = search_service_pb2.IndexDocumentResponse()
    self.stub.MakeSyncCall('search', 'IndexDocument', request, response)
    return response

  def _DeleteDocument(self, index, doc_ids):
    """Make a call of DeleteDocument.

    Args:
      index: The name or IndexSpec of the index.
      doc_ids: A list of string which holds the doc ids to be deleted.
    Returns:
      A DeleteDocumentResponse instance for the call.
    """
    request = search_service_pb2.DeleteDocumentRequest()
    params = request.params
    params.SetInParent()
    for doc_id in doc_ids:
      params.doc_id.append(doc_id)
    self._SetIndexSpec(index, params.index_spec)
    response = search_service_pb2.DeleteDocumentResponse()
    self.stub.MakeSyncCall('search', 'DeleteDocument', request, response)
    return response

  def _ListIndexes(self, fetch_schema=False, limit=None, offset=None,
                   namespace=None, start_index_name=None,
                   include_start_index=None, index_name_prefix=None):
    """Make a call of ListIndexes.

    Args:
      fetch_schema: If True, returns the index schema in response.
      limit: If not None, the limit on how many indices to return.
      offset: If not None, the offset from the first result to return from.
      namespace: Indices in this namespace will be listed.
      start_index_name: The name of the first index to include.
      include_start_index: If false, start with the index after
      "start_index_name"
      index_name_prefix: Only include indices that start with the given prefix.

    Returns:
      A ListIndexesResponse instance populated by the call.
    """
    request = search_service_pb2.ListIndexesRequest()
    params = request.params
    params.SetInParent()
    if fetch_schema:
      params.fetch_schema = True
    if limit is not None:
      params.limit = limit
    if offset is not None:
      params.offset = offset
    if namespace is not None:
      params.namespace = namespace
    if start_index_name is not None:
      params.start_index_name = start_index_name
    if include_start_index is not None:
      params.include_start_index = include_start_index
    if index_name_prefix is not None:
      params.index_name_prefix = index_name_prefix
    response = search_service_pb2.ListIndexesResponse()
    self.stub.MakeSyncCall('search', 'ListIndexes', request, response)
    return response

  def _ListDocuments(self, index, start_doc_id=None, limit=None, ids_only=None,
                     include_start_doc=None, namespace=None):
    """Make a call of ListDocuments.

    Args:
      index: The name or IndexSpec of the index.
      start_doc_id: The doc id to start listing from.
      limit: The maximum number of documents to return.
      ids_only: If true, do not return fields, otherwise return fields.
      include_start_doc: Whether, to include the document matching
        start_doc_id.
      namespace: The namespace which the index is in.

    Returns:
      A ListDocumentsResponse instance for the call.
    """
    request = search_service_pb2.ListDocumentsRequest()
    params = request.params
    params.SetInParent()
    if namespace is not None:
      params.index_spec.namespace = namespace
    if start_doc_id is not None:
      params.start_doc_id = start_doc_id
    if limit is not None:
      params.limit = limit
    if ids_only is not None:
      params.keys_only = ids_only
    if include_start_doc is not None:
      params.include_start_doc = include_start_doc
    self._SetIndexSpec(index, params.index_spec)
    response = search_service_pb2.ListDocumentsResponse()
    self.stub.MakeSyncCall('search', 'ListDocuments', request, response)
    return response

  def _CreateSearchRequest(self, index, query, limit=None, offset=None,
                           cursor=None, cursor_type=None, scorer=None,
                           returned_fields=None, ids_only=None, namespace=None):
    """Creates a very simple SearchParams for the query for the test.

    Args:
      index: The name or IndexSpec of the index to search.
      query: The search query string.
      limit: The maximum number of documents to return.
      offset: The position to return documents from.
      cursor: The cursor to continue returning documents from.
      cursor_type: The type of cursor to return in results: NONE,
        PER_RESULT, or SINGLE (one per search result set).
      scorer: The scorer used to score documents.
      returned_fields: Fields to include in the returned documents.
      ids_only: If True, only the IDs of each document will be returned.
      namespace: The namespace to search in.
    Returns:
      A SearchParams which holds the index and query.
    """
    params = search_service_pb2.SearchParams()
    self._SetIndexSpec(index, params.index_spec, namespace=namespace)
    params.query = query
    if limit is not None:
      params.limit = limit
    if offset is not None:
      params.offset = offset
    if cursor is not None:
      params.cursor = cursor
    if cursor_type is not None:
      params.cursor_type = cursor_type
    if scorer:
      scorer_spec = params.scorer_spec
      scorer_spec.scorer = scorer
    if returned_fields:
      field_spec_pb = params.field_spec
      for field in returned_fields:
        field_spec_pb.name.append(field)
    if ids_only:
      params.keys_only = True
    return params

  def _Search(self, params):
    """Make a call of Search.

    Args:
      params: A SearchParams instance for the search spec.
    Returns:
      A SearchResponse instance for the call.
    """
    request = search_service_pb2.SearchRequest()
    request.params.CopyFrom(params)
    response = search_service_pb2.SearchResponse()
    self.stub.MakeSyncCall('search', 'Search', request, response)
    return response

  def testIndexDocument(self):
    response = self._IndexDocument('test_index', 'testid', [('foo', 'bar')])
    self.assertLen(response.status, 1)
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)

    response = self._Search(self._CreateSearchRequest('test_index', 'bar'))
    self.assertEqual(1, response.matched_count)

  def testIndexDocumentNoFields(self):
    response = self._IndexDocument('test_index', 'testid', [])
    self.assertEqual(search_service_pb2.SearchServiceError.INVALID_REQUEST,
                     response.status[0].code)

  def testIndexDocumentWithNoId(self):
    response = self._IndexDocument('test_index', None, [('foo', 'bar')])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    self.assertEqual(1, len(response.doc_id))
    self.assertTrue(response.doc_id[0])


    response = self._Search(self._CreateSearchRequest('test_index', 'bar'))
    self.assertEqual(1, response.matched_count)

  def testIndexDocumentWithEmptyId(self):
    response = self._IndexDocument('test_index', '', [('foo', 'bar')])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    self.assertEqual(1, len(response.doc_id))
    self.assertTrue(response.doc_id[0])


    response = self._Search(self._CreateSearchRequest('test_index', 'bar'))
    self.assertEqual(1, response.matched_count)

  def testIndexDocumentCaseInsensitive(self):
    response = self._IndexDocument('test_index', 'testid', [('foo', 'Bar')])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)

    response = self._Search(self._CreateSearchRequest('test_index', 'bar'))
    self.assertEqual(1, response.matched_count)
    response = self._Search(self._CreateSearchRequest('test_index', 'Bar'))
    self.assertEqual(1, response.matched_count)

  def testIndexDocumentCaseInsensitiveAtom(self):
    response = self._IndexDocument(
        'index', 'id0', [('atom', 'XyZzy', document_pb2.FieldValue.ATOM)])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)

    response = self._Search(self._CreateSearchRequest('index', 'xyzzy'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('id0', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest('index', 'atom:xyzzY'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('id0', response.result[0].document.id)

  def testIndexDocumentWithDifferentConsistency(self):
    index_spec = self._MakeIndexSpec('unique_index',
                                     search_service_pb2.IndexSpec.GLOBAL)
    response = self._IndexDocument(index_spec, 'testid', [('foo', 'bar')])
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)

    index_spec = self._MakeIndexSpec('unique_index',
                                     search_service_pb2.IndexSpec.PER_DOCUMENT)
    response = self._IndexDocument(index_spec, 'testid', [('foo', 'bar')])

    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    response = self._Search(self._CreateSearchRequest('unique_index', 'bar'))
    self.assertEqual(1, response.matched_count)

  def testIndexDocumentNumbers(self):
    response = self._IndexDocument(
        'test_index', 'testid',
        [('foo', '999.99', document_pb2.FieldValue.NUMBER)])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)

    response = self._Search(
        self._CreateSearchRequest('test_index', 'foo:999.99'))
    self.assertEqual(1, response.matched_count)

  def testIndexDocumentPrefixFields(self):
    response = self._IndexDocument(
        'test_index', 'untokenized_prefix_doc',
        [('uprefix', 'Quick Brown Fox',
          document_pb2.FieldValue.UNTOKENIZED_PREFIX)])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    response = self._IndexDocument(
        'test_index', 'tokenized_prefix_doc',
        [('tpf1', 'Foo Bar buzz', document_pb2.FieldValue.TOKENIZED_PREFIX)])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)

    response = self._Search(
        self._CreateSearchRequest('test_index', 'uprefix:"quick brown fox"'))
    self.assertEqual(1, response.matched_count)
    response = self._Search(
        self._CreateSearchRequest('test_index', 'uprefix:"quick bro"'))
    self.assertEqual(1, response.matched_count)
    response = self._Search(
        self._CreateSearchRequest('test_index', 'uprefix: qui'))
    self.assertEqual(1, response.matched_count)
    response = self._Search(
        self._CreateSearchRequest('test_index', 'uprefix: "qui bro"'))
    self.assertEqual(0, response.matched_count)
    response = self._Search(
        self._CreateSearchRequest('test_index', 'tpf1: fo'))
    self.assertEqual(1, response.matched_count)
    response = self._Search(
        self._CreateSearchRequest('test_index', 'tpf1: (fo ba bu)'))
    self.assertEqual(1, response.matched_count)
    response = self._Search(
        self._CreateSearchRequest('test_index', 'tpf1: "foo ba buzz"'))
    self.assertEqual(1, response.matched_count)

    response = self._Search(
        self._CreateSearchRequest('test_index', '"quick brown fox"'))
    self.assertEqual(0, response.matched_count)
    response = self._Search(
        self._CreateSearchRequest('test_index', '"foo"'))
    self.assertEqual(0, response.matched_count)

  def testMultipleIndexes(self):
    request = search_service_pb2.IndexDocumentRequest()
    self._AddDocumentToRequest('id1', [('foo', 'bar')], request.params)
    self._AddDocumentToRequest('id2', [('foo', 'baz')], request.params)
    index_spec = request.params.index_spec
    index_spec.name = 'test_index'
    index_spec.consistency = search_service_pb2.IndexSpec.GLOBAL
    response = search_service_pb2.IndexDocumentResponse()
    self.stub.MakeSyncCall('search', 'IndexDocument', request, response)
    self.assertEqual(2, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[1].code)

    response = self._Search(self._CreateSearchRequest('test_index', 'bar'))
    self.assertEqual(1, response.matched_count)
    response = self._Search(self._CreateSearchRequest('test_index', 'baz'))
    self.assertEqual(1, response.matched_count)

  def testIndexDocumentUpdate(self):
    response = self._IndexDocument('test_index', 'testid', [('foo', 'bar')])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    response = self._IndexDocument('test_index', 'testid', [('foo', 'baz')])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)

    response = self._Search(self._CreateSearchRequest('test_index', 'baz'))
    self.assertEqual(1, response.matched_count)
    response = self._Search(self._CreateSearchRequest('test_index', 'bar'))
    self.assertEqual(0, response.matched_count)

  def testDeleteDocument(self):
    self._IndexDocument('test_index', 'id1', [('foo', 'bar')])
    self._IndexDocument('test_index', 'id2', [('foo', 'baz')])
    self._IndexDocument('test_index', 'id3', [('foo', 'quox')])
    response = self._DeleteDocument('test_index', ['id1', 'id2'])
    self.assertEqual(2, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[1].code)

    response = self._Search(self._CreateSearchRequest('test_index', 'bar'))
    self.assertEqual(0, response.matched_count)
    response = self._Search(self._CreateSearchRequest('test_index', 'baz'))
    self.assertEqual(0, response.matched_count)

    response = self._Search(self._CreateSearchRequest('test_index', 'quox'))
    self.assertEqual(1, response.matched_count)

  def testDeleteDocumentDifferentConsistency(self):
    self._IndexDocument('test_index', 'id1', [('foo', 'bar')])
    index_spec = self._MakeIndexSpec('test_index',
                                     search_service_pb2.IndexSpec.PER_DOCUMENT)
    response = self._DeleteDocument(index_spec, ['id1'])
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    response = self._Search(self._CreateSearchRequest('test_index', 'bar'))
    self.assertEqual(0, response.matched_count)

  def testDeleteDocumentIndexDoesNotExist(self):
    response = self._DeleteDocument('test_index', ['id1'])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)
    self.assertEqual('Not found', response.status[0].error_detail)

  def CheckListIndexesResponse(self, response, names, metadata_list=None,
                               namespace_list=None):
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status.code)
    self.assertEqual(len(names), len(response.index_metadata))
    for i, name in enumerate(names):
      index_metadata = response.index_metadata[i]
      self.assertEqual(name, index_metadata.index_spec.name)
    if namespace_list:
      for i, ns in enumerate(namespace_list):
        index_metadata = response.index_metadata[i]
        self.assertEqual(ns, index_metadata.index_spec.namespace)
    if metadata_list:
      for i, metadata in enumerate(metadata_list):
        index_metadata = response.index_metadata[i]
        field_map = {}
        for field_types_pb in index_metadata.field:
          field_map[field_types_pb.name] = field_types_pb
        for field in metadata:
          field_types_pb = field_map[field.name]
          self.assertEqual(field.name, field_types_pb.name)
          self.assertEqual(field.type, field_types_pb.type)

  def testListIndexes(self):
    self.CheckListIndexesResponse(self._ListIndexes(), [])


    self._IndexDocument('test_index', 'testid', [])
    self.CheckListIndexesResponse(self._ListIndexes(), ['test_index'])

    self._IndexDocument('a', 'testid', [])
    self._IndexDocument('b', 'testid', [])
    self._IndexDocument('c0', 'testid', [])
    self._IndexDocument('cz', 'testid', [])
    self._IndexDocument('ca', 'testid', [])
    self._IndexDocument('d', 'testid', [])
    self._IndexDocument('Z', 'testid', [])
    self._IndexDocument('e', 'testid', [])
    self._IndexDocument('f', 'testid', [])
    self.CheckListIndexesResponse(self._ListIndexes(), [
        'Z', 'a', 'b', 'c0', 'ca', 'cz', 'd', 'e', 'f', 'test_index'])
    self.CheckListIndexesResponse(self._ListIndexes(limit=2), ['Z', 'a'])
    self.CheckListIndexesResponse(self._ListIndexes(limit=2, offset=1),
                                  ['a', 'b'])
    self.CheckListIndexesResponse(self._ListIndexes(
        start_index_name='ca', offset=1, limit=3), ['cz', 'd', 'e'])
    self.CheckListIndexesResponse(
        self._ListIndexes(
            start_index_name='ca', include_start_index=False,
            offset=1, limit=3),
        ['d', 'e', 'f'])
    self.CheckListIndexesResponse(
        self._ListIndexes(index_name_prefix='c'),
        ['c0', 'ca', 'cz'])
    self.CheckListIndexesResponse(
        self._ListIndexes(index_name_prefix='c', offset=1, limit=1), ['ca'])

  def testListIndexesWithMetadata(self):
    field1 = document_pb2.FieldTypes()
    field1.name = 'bar'
    field1.type.append(document_pb2.FieldValue.HTML)

    field2 = document_pb2.FieldTypes()
    field2.name = 'foo'
    field2.type.append(document_pb2.FieldValue.NUMBER)

    self._IndexDocument('test_index', 'testid',
                        [('bar', '<HTM></HTML>', document_pb2.FieldValue.HTML),
                         ('foo', '999.99', document_pb2.FieldValue.NUMBER)])
    self.CheckListIndexesResponse(self._ListIndexes(fetch_schema=True),
                                  names=['test_index'], metadata_list=
                                  [[field1, field2]])

  def testListIndexesWithStorage(self):
    self._IndexDocument('index1', 'doc1',
                        [('body', 'Lorem ipsum', document_pb2.FieldValue.TEXT)])
    response = self._ListIndexes()
    self.assertEqual(1, len(response.index_metadata))
    self.assertTrue(response.index_metadata[0].HasField('storage'))

  def testListIndexesWithStorageSize(self):
    long_body = 'The quick, brown fox jumps over the lazy dog.'
    self._IndexDocument('index1', 'doc1',
                        [('body', 'Hello world', document_pb2.FieldValue.TEXT)])
    self._IndexDocument('index1', 'doc2',
                        [('body', long_body, document_pb2.FieldValue.TEXT)])
    self._IndexDocument('index2', 'docA',
                        [('body', 'Hello world', document_pb2.FieldValue.TEXT)])
    response = self._ListIndexes()
    index1md = response.index_metadata[0]
    index2md = response.index_metadata[1]
    self.assertEqual('index1', index1md.index_spec.name)
    self.assertEqual('index2', index2md.index_spec.name)




    self.assertTrue(
        index1md.storage.amount_used > index2md.storage.amount_used +
        len(long_body))
    self.assertEqual(index1md.storage.limit, index2md.storage.limit)

  def testListIndexesWithAppId(self):
    """Tests that ListIndexes UI testing implementation doesn't crash."""
    request = search_service_pb2.ListIndexesRequest()
    request.params.SetInParent()
    request.app_id = b'app'
    response = search_service_pb2.ListIndexesResponse()
    try:
      self.stub.MakeSyncCall('search', 'ListIndexes', request, response)
    except apiproxy_errors.Error:

      pass

  def testListDocuments(self):

    self._IndexDocument('list_docs', 'doc1', [('foo', 'bar')])
    response = self._ListDocuments(index='list_docs')
    self.assertEqual(1, len(response.document))
    document = response.document[0]
    self.assertEqual('doc1', document.id)

    self._IndexDocument('list_docs', 'doc2', [('bar', 'foo')])
    response = self._ListDocuments(index='list_docs', limit=1)
    self.assertEqual(1, len(response.document))

    response = self._ListDocuments(index='list_docs', start_doc_id='doc1',
                                   limit=1)
    self.assertEqual(1, len(response.document))
    document = response.document[0]
    self.assertEqual('doc1', document.id)

    response = self._ListDocuments(index='list_docs', start_doc_id='doc1',
                                   limit=1, include_start_doc=False)
    self.assertTrue(len(response.document) <= 1)
    if len(response.document) == 1:
      document = response.document[0]
      self.assertFalse('doc1' == document.id)

    self._IndexDocument('list_docs', 'doc1', [('foo', 'bar')])
    response = self._ListDocuments(index='list_docs', start_doc_id='doc1',
                                   limit=1)
    self.assertEqual(1, len(response.document))
    document = response.document[0]
    self.assertEqual('doc1', document.id)
    self.assertEqual(1, len(document.field))

    response = self._ListDocuments(index='list_docs', start_doc_id='doc1',
                                   limit=1, ids_only=True)
    self.assertEqual(1, len(response.document))
    document = response.document[0]
    self.assertEqual('doc1', document.id)
    self.assertEqual(0, len(document.field))

    response = self._ListDocuments(index='i_do_not_exist')
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status.code)
    self.assertEqual(0, len(response.document))

  def testSearchWithAppId(self):
    """Tests that Search UI testing implementation doesn't crash."""
    request = search_service_pb2.SearchRequest()
    params = request.params
    params.SetInParent()
    index_spec = params.index_spec
    index_spec.name = '123'
    params.query = ''
    params.limit = 20
    request.app_id = b'app'

    while True:
      response = search_service_pb2.SearchResponse()
      try:
        self.stub.MakeSyncCall('search', 'Search', request, response)
        if response.matched_count <= (params.offset + len(response.result)):
          break
        self.assertEqual(len(response.result), params.limit)
        params.offset = params.offset + len(response.result)
      except apiproxy_errors.Error:

        pass
    self.assertEqual(response.matched_count,
                     params.offset + len(response.result))

  def testBasicSearch(self):

    document = document_pb2.Document()
    document.id = 'test_doc_id'
    document.language = 'en'
    new_field = document.field.add()
    new_field.name = 'field1'
    new_field.value.language = 'en'
    new_field.value.string_value = 'string value'
    new_field = document.field.add()
    new_field.name = 'field2'
    new_field.value.language = 'en'
    new_field.value.string_value = 'unmatchedcontent'
    new_field = document.field.add()
    new_field.name = 'numfield'
    new_field.value.type = document_pb2.FieldValue.NUMBER
    new_field.value.string_value = '100'

    index_request = search_service_pb2.IndexDocumentRequest()
    params = index_request.params
    params.document.add().CopyFrom(document)
    params.index_spec.name = 'test_index'
    params.index_spec.consistency = search_service_pb2.IndexSpec.GLOBAL
    index_response = search_service_pb2.IndexDocumentResponse()
    self.stub.MakeSyncCall(
        'search', 'IndexDocument', index_request, index_response)
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     index_response.status[0].code)


    response = self._Search(self._CreateSearchRequest('test_index', 'string'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual(1, len(response.result))
    expected = document_pb2.Document()
    expected.CopyFrom(document)
    expected.order_id = 0
    self.assertEqual(expected, response.result[0].document)


    response = self._Search(self._CreateSearchRequest('test_index', ''))
    self.assertEqual(1, response.matched_count)
    self.assertEqual(1, len(response.result))
    self.assertEqual(expected, response.result[0].document)


    response = self._Search(self._CreateSearchRequest('test_index', ' '))
    self.assertEqual(1, response.matched_count)
    self.assertEqual(1, len(response.result))
    self.assertEqual(expected, response.result[0].document)


    response = self._Search(
        self._CreateSearchRequest('test_index', 'field1:string'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual(1, len(response.result))
    self.assertEqual(expected, response.result[0].document)


    response = self._Search(self._CreateSearchRequest(
        'test_index', 'field1:string'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual(1, len(response.result))
    self.assertEqual(expected, response.result[0].document)


    response = self._Search(self._CreateSearchRequest('test_index', 'other'))
    self.assertEqual(0, response.matched_count)
    self.assertEqual(0, len(response.result))


    response = self._Search(
        self._CreateSearchRequest('test_index', 'nonexistenttoken OR string'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual(1, len(response.result))
    self.assertEqual(expected, response.result[0].document)


    response = self._Search(
        self._CreateSearchRequest('test_index', 'string AND value'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual(1, len(response.result))
    self.assertEqual(expected, response.result[0].document)


    response = self._Search(
        self._CreateSearchRequest('test_index', 'numfield:abc'))
    self.assertEqual(0, response.matched_count)
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status.code)


    response = self._Search(
        self._CreateSearchRequest('test_index', 'string', ids_only=True))
    self.assertEqual(1, response.matched_count)
    self.assertEqual(1, len(response.result))
    doc = response.result[0].document
    self.assertEqual('test_doc_id', doc.id)
    fields = doc.field
    self.assertEqual(0, len(fields))


    response = self._Search(
        self._CreateSearchRequest('test_index', 'string',
                                  returned_fields=['field2']))
    self.assertEqual(1, response.matched_count)
    self.assertEqual(1, len(response.result))
    doc = response.result[0].document
    self.assertEqual('test_doc_id', doc.id)
    fields = doc.field
    self.assertEqual(1, len(fields))
    field = fields[0]
    self.assertEqual('field2', field.name)
    self.assertEqual('unmatchedcontent', field.value.string_value)

  def testNestedSearch(self):
    document = document_pb2.Document()
    document.id = 'test_doc_id'
    document.language = 'en'
    new_field = document.field.add()
    new_field.name = 'field1'
    new_field.value.language = 'en'
    new_field.value.string_value = 'string value'
    new_field = document.field.add()
    new_field.name = 'field2'
    new_field.value.language = 'en'
    new_field.value.string_value = 'unmatchedcontent'

    index_request = search_service_pb2.IndexDocumentRequest()
    params = index_request.params
    params.document.add().CopyFrom(document)
    params.index_spec.name = 'test_index'
    params.index_spec.consistency = search_service_pb2.IndexSpec.GLOBAL
    index_response = search_service_pb2.IndexDocumentResponse()
    self.stub.MakeSyncCall(
        'search', 'IndexDocument', index_request, index_response)
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     index_response.status[0].code)

    response = self._Search(
        self._CreateSearchRequest(
            'test_index', 'field1:(nonexistenttoken OR string)'))
    self.assertEqual(1, response.matched_count)

    response = self._Search(
        self._CreateSearchRequest(
            'test_index', 'field1:(nonexistenttoken OR anotherbadone)'))
    self.assertEqual(0, response.matched_count)

    response = self._Search(
        self._CreateSearchRequest(
            'test_index', 'field1:(nonexistenttoken AND string)'))
    self.assertEqual(0, response.matched_count)

    response = self._Search(
        self._CreateSearchRequest(
            'test_index', 'field1:(value AND string)'))
    self.assertEqual(1, response.matched_count)

    response = self._Search(
        self._CreateSearchRequest(
            'test_index', 'field1:(nonexistenttoken OR (string AND value))'))
    self.assertEqual(1, response.matched_count)

  def testSearchNonExistentIndex(self):
    response = self._Search(
        self._CreateSearchRequest('index does not exist', 'hello world'))
    self.assertEqual(0, response.matched_count)
    self.assertEmpty(response.result)

  def testSearchOffset(self):
    id_list = []
    for i in range(10):
      new_id = 'id%d' % i
      id_list.append(new_id)
      self._IndexDocument('test_index', new_id, [('foo', 'bar')])

    response = self._Search(self._CreateSearchRequest('test_index', 'bar',
                                                      limit=10))
    self.assertEqual(10, response.matched_count)
    self.assertEqual(10, len(response.result))

    response = self._Search(self._CreateSearchRequest('test_index', 'bar',
                                                      offset=3, limit=5))
    self.assertEqual(10, response.matched_count)
    self.assertEqual(5, len(response.result))

    response = self._Search(self._CreateSearchRequest('test_index', 'bar',
                                                      offset=0, limit=5))
    self.assertEqual(10, response.matched_count)
    self.assertEqual(5, len(response.result))
    first_five = [result.document.id for result in response.result]

    response = self._Search(self._CreateSearchRequest('test_index', 'bar',
                                                      offset=5, limit=5))
    self.assertEqual(10, response.matched_count)
    self.assertEqual(5, len(response.result))
    second_five = [result.document.id for result in response.result]

    self.assertFalse([doc_id for doc_id in first_five if doc_id in second_five])

    response = self._Search(self._CreateSearchRequest('test_index', 'bar',
                                                      offset=10, limit=5))
    self.assertEqual(10, response.matched_count)
    self.assertEqual(0, len(response.result))


  def testSearchCursor(self):
    id_list = []
    for i in range(10):
      new_id = 'id+%d' % i
      id_list.append(new_id)
      self._IndexDocument('test_index', new_id, [('foo', 'bar')])

    response = self._Search(
        self._CreateSearchRequest('test_index', 'bar', limit=10))
    self.assertEqual(10, response.matched_count)
    self.assertEqual(10, len(response.result))

    response = self._Search(
        self._CreateSearchRequest(
            'test_index',
            'bar',
            limit=5,
            cursor_type=search_service_pb2.SearchParams.SINGLE))
    self.assertEqual(response.status.code,
                     search_service_pb2.SearchServiceError.OK)
    self.assertEqual(10, response.matched_count)
    self.assertEqual(5, len(response.result))
    first_five = [result.document.id for result in response.result]
    cursor = response.cursor
    self.assertTrue(cursor)

    response = self._Search(
        self._CreateSearchRequest(
            'test_index',
            'bar',
            limit=5,
            cursor=cursor,
            cursor_type=search_service_pb2.SearchParams.SINGLE))
    self.assertEqual(response.status.code,
                     search_service_pb2.SearchServiceError.OK,
                     response.status.error_detail)
    self.assertEqual(10, response.matched_count)
    self.assertEqual(5, len(response.result))
    second_five = [result.document.id for result in response.result]
    self.assertFalse(response.HasField('cursor'), response.cursor)
    self.assertFalse([doc_id for doc_id in first_five if doc_id in second_five])

    response = self._Search(
        self._CreateSearchRequest(
            'test_index',
            'bar',
            limit=10,
            cursor_type=search_service_pb2.SearchParams.PER_RESULT))
    self.assertEqual(response.status.code,
                     search_service_pb2.SearchServiceError.OK)
    self.assertEqual(10, response.matched_count)
    self.assertEqual(10, len(response.result))
    cursor9 = response.result[8].cursor
    cursor10 = response.result[9].cursor

    response = self._Search(
        self._CreateSearchRequest(
            'test_index',
            'bar',
            limit=10,
            cursor=cursor9,
            cursor_type=search_service_pb2.SearchParams.PER_RESULT))
    self.assertEqual(response.status.code,
                     search_service_pb2.SearchServiceError.OK)
    self.assertEqual(10, response.matched_count)
    self.assertEqual(1, len(response.result))
    self.assertEqual(cursor10, response.result[0].cursor)

  def testSearchSelected(self):
    id_list = []
    for i in range(10):
      new_id = 'id%d' % i
      id_list.append(new_id)
      self._IndexDocument('test_index', new_id, [('foo', 'bar')])

    response = self._Search(self._CreateSearchRequest('test_index', 'bar'))
    self.assertEqual(10, response.matched_count)
    self.assertEqual(10, len(response.result))

    params = self._CreateSearchRequest('test_index', 'bar', limit=5)
    response = self._Search(params)
    self.assertEqual(10, response.matched_count)
    self.assertEqual(5, len(response.result))

  def testSearchIndexDoesNotExist(self):
    response = self._Search(self._CreateSearchRequest('test_index', ''))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status.code)
    self.assertEqual("Index 'test_index' in namespace '' does not exist",
                     response.status.error_detail)

  def _GetFieldValue(self, document, field_name):
    """Get the field value for the field_name in the document.

    Args:
      document: a Document object
      field_name: a string of the field name

    Returns:
      a string of the specified field value.  None if not found.
    """
    for field in document.field:
      if field.name == field_name:
        return field.value.string_value
    return None

  def testSearchPhrase(self):
    response = self._IndexDocument('test_index', 'testid',
                                   [('foo', 'Lorem ipsum dolor sit amet')])
    self.assertEqual(1, len(response.status))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status[0].code)

    response = self._Search(self._CreateSearchRequest('test_index',
                                                      'ipsum lorem dolor'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('testid', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest('test_index',
                                                      'lorem ipsum dolor'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('testid', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest('test_index',
                                                      '"lorem ipsum" dolor'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('testid', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'foo:"lorem ipsum" dolor'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('testid', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest('test_index',
                                                      '"ipsum lorem" dolor'))
    self.assertFalse(response.result)


    response = self._Search(self._CreateSearchRequest('test_index',
                                                      '"ipsum dolor amet"'))
    self.assertFalse(response.result)


    response = self._Search(self._CreateSearchRequest('test_index',
                                                      '"foo bar hello world"'))
    self.assertFalse(response.result)


    response = self._Search(self._CreateSearchRequest('test_index', '""'))
    self.assertEqual(0, response.matched_count)

  def testSearchDateComparison(self):
    test_data = [
        ('0', 'ex why zee', datetime.date(2011, 5, 18)),
        ('1', 'one two three', datetime.date(2012, 5, 18)),
        ('2', 'three four five', datetime.date(2012, 2, 11)),
        ]

    for docid, text, date in test_data:
      response = self._IndexDocument(
          'test_index', docid,
          [('text', text, document_pb2.FieldValue.TEXT),
           ('date', str(date), document_pb2.FieldValue.DATE)])
      self.assertEqual(1, len(response.status))
      self.assertEqual(search_service_pb2.SearchServiceError.OK,
                       response.status[0].code)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'date = 2012-5-18'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('1', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'date > 2012-2-11'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('1', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'date < 2012-2-11'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('0', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'date <= 2012-2-11'))
    self.assertEqual(2, response.matched_count)
    for result in response.result:
      self.assertTrue(result.document.id in ('0', '2'))

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'date >= 2012-2-11'))
    self.assertEqual(2, response.matched_count)
    for result in response.result:
      self.assertTrue(result.document.id in ('1', '2'))

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'date != 2012-2-11'))
    self.assertEqual('!= comparison operator is not available',
                     response.status.error_detail)
    self.assertEqual(search_service_pb2.SearchServiceError.INVALID_REQUEST,
                     response.status.code)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'date > 2013-1-1'))
    self.assertEqual(0, response.matched_count)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'date < 2009-1-1'))
    self.assertEqual(0, response.matched_count)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'date = 2000-1-1'))
    self.assertEqual(0, response.matched_count)

  def testSearchNumberComparison(self):
    test_data = [
        ('0', 'ex why zee', 1),
        ('1', 'one two three', -20),
        ('2', 'three four five', 1000),
        ]

    for docid, text, num in test_data:
      response = self._IndexDocument(
          'test_index', docid,
          [('text', text, document_pb2.FieldValue.TEXT),
           ('num', str(num), document_pb2.FieldValue.NUMBER)])
      self.assertEqual(1, len(response.status))
      self.assertEqual(search_service_pb2.SearchServiceError.OK,
                       response.status[0].code)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'num = 1'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('0', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'num > 1'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('2', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'num < 1'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('1', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'num <= 1'))
    self.assertEqual(2, response.matched_count)
    for result in response.result:
      self.assertTrue(result.document.id in ('0', '1'))

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'num >= 1'))
    self.assertEqual(2, response.matched_count)
    for result in response.result:
      self.assertTrue(result.document.id in ('0', '2'))

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'num != 1'))
    self.assertEqual('!= comparison operator is not available',
                     response.status.error_detail)
    self.assertEqual(search_service_pb2.SearchServiceError.INVALID_REQUEST,
                     response.status.code)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'num > 1000'))
    self.assertEqual(0, response.matched_count)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'num < -100'))
    self.assertEqual(0, response.matched_count)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'num = -100'))
    self.assertEqual(0, response.matched_count)

  def testSearchNegation(self):
    self._IndexDocument('test_index', 'id1', [('foo', 'bar test')])
    self._IndexDocument('test_index', 'id2', [('foo', 'baz test')])

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'NOT foo:bar'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('id2', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest(
        'test_index', 'NOT foo:test'))
    self.assertEqual(0, response.matched_count)

  def testScoring(self):
    response = self._IndexDocument('test_index', 'testid1',
                                   [('foo', 'ipsum sit amet')])
    response = self._IndexDocument('test_index', 'testid2',
                                   [('foo', 'Lorem ipsum sit amet')])
    response = self._IndexDocument('test_index', 'testid3',
                                   [('foo', 'Lorem ipsum dolor sit amet')])
    response = self._IndexDocument(
        'test_index', 'testid4',
        [('foo', 'Lorem ipsum dolor dolor sit amet')])
    response = self._Search(
        self._CreateSearchRequest(
            'test_index',
            'ipsum lorem dolor',
            scorer=search_service_pb2.ScorerSpec.MATCH_SCORER))
    self.assertEqual(2, response.matched_count)
    results = response.result
    self.assertEqual('testid4', results[0].document.id)
    self.assertLen(results[0].score, 1)
    self.assertEqual('testid3', results[1].document.id)
    self.assertLen(results[1].score, 1)
    self.assertTrue(results[0].score[0] >= results[1].score[0])

  def testPersistence(self):
    filename = os.path.join(flags.FLAGS.test_tmpdir, 'search_stub_test_index')

    self.stub = simple_search_stub.SearchServiceStub(index_file=filename)
    self._IndexDocument('test_index_1', 'id_one', [('name', 'one')])
    self._IndexDocument('test_index_1', 'id_two', [('name', 'two')])
    self._IndexDocument('test_index_2', 'id_three', [('name', 'three')])
    self.stub.Write()
    del self.stub

    self.stub = simple_search_stub.SearchServiceStub(index_file=filename)
    self.CheckListIndexesResponse(
        self._ListIndexes(), ['test_index_1', 'test_index_2'])

    response = self._ListDocuments(index='test_index_1')
    self.assertEqual(2, len(response.document))

    response = self._ListDocuments(index='test_index_2')
    self.assertEqual(1, len(response.document))
    self.assertEqual('id_three', response.document[0].id)

  def testPersistenceWithErrors(self):
    filename = os.path.join(flags.FLAGS.test_tmpdir, 'search_stub_test_index')

    self.stub = simple_search_stub.SearchServiceStub(index_file=filename)
    self._IndexDocument('test_index_1', 'id_one', [('name', 'one')])
    self._IndexDocument('test_index_1', 'id_two', [('name', 'two')])
    self._IndexDocument('test_index_2', 'id_three', [('name', 'three')])
    self.stub.Write()
    del self.stub

    import stat

    os.chmod(filename, stat.S_IWUSR)


    simple_search_stub.SearchServiceStub(index_file=filename)

  def testPersistenceVersioning(self):
    filename = os.path.join(flags.FLAGS.test_tmpdir, 'search_stub_test_index')

    self.stub = simple_search_stub.SearchServiceStub(index_file=filename)
    self.stub._VERSION -= 1
    self._IndexDocument('test_index_1', 'id_one', [('name', 'one')])
    self._IndexDocument('test_index_1', 'id_two', [('name', 'two')])
    self._IndexDocument('test_index_2', 'id_three', [('name', 'three')])
    self.stub.Write()
    del self.stub

    self.stub = simple_search_stub.SearchServiceStub(index_file=filename)
    self.CheckListIndexesResponse(self._ListIndexes(), [])

    response = self._ListDocuments(index='test_index_1')
    self.assertEqual(0, len(response.document))

    response = self._ListDocuments(index='test_index_2')
    self.assertEqual(0, len(response.document))



    self.stub = simple_search_stub.SearchServiceStub(index_file=filename)
    self._IndexDocument('test_index_1', 'id_one', [('name', 'one')])
    self._IndexDocument('test_index_1', 'id_two', [('name', 'two')])
    self._IndexDocument('test_index_2', 'id_three', [('name', 'three')])



    import tempfile, pickle

    descriptor, tmp_filename = tempfile.mkstemp(dir=os.path.dirname(filename))
    tmpfile = os.fdopen(descriptor, 'wb')

    pickler = pickle.Pickler(tmpfile, protocol=1)
    pickler.fast = True



    index_spec = search_service_pb2.IndexSpec()
    self._SetIndexSpec('test_index_1', index_spec, namespace='test')
    pickler.dump({'test': self.stub._GetIndex(index_spec)})

    tmpfile.close()
    os.rename(tmp_filename, filename)

    del self.stub
    self.stub = simple_search_stub.SearchServiceStub(index_file=filename)
    self.CheckListIndexesResponse(self._ListIndexes(), [])


  def testDisablePersistence(self):
    filename = os.path.join(flags.FLAGS.test_tmpdir, 'search_stub_test_index')

    self.stub = simple_search_stub.SearchServiceStub(index_file='')
    self._IndexDocument('test_index_1', 'id_one', [('name', 'one')])
    self._IndexDocument('test_index_1', 'id_two', [('name', 'two')])
    self._IndexDocument('test_index_2', 'id_three', [('name', 'three')])
    self.stub.Write()

    self.assertFalse(os.path.exists(filename))

  def testNamespaceIsolation(self):
    self._IndexDocument(
        'index_1', 'id_one', [('name', 'one two three')], namespace='ns1')
    self._IndexDocument(
        'index_1', 'id_two', [('name', 'three four five')], namespace='ns1')
    self._IndexDocument(
        'index_1', 'id_three', [('name', 'five six seven')], namespace='ns1')
    self._IndexDocument(
        'index_1', 'id_four', [('name', 'one three five')], namespace='ns2')

    response = self._Search(
        self._CreateSearchRequest('index_1', 'three', namespace='ns1'))
    self.assertEqual(2, response.matched_count)
    for result in response.result:
      self.assertTrue(result.document.id in ['id_one', 'id_two'])

    response = self._Search(
        self._CreateSearchRequest('index_1', 'three', namespace='ns2'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('id_four', response.result[0].document.id)

  def testNamespacePersistence(self):
    filename = os.path.join(flags.FLAGS.test_tmpdir,
                            'search_stub_namespace_persistence')

    self.stub = simple_search_stub.SearchServiceStub(index_file=filename)
    self._IndexDocument('test_index_1', 'id_one', [('name', 'one')],
                        namespace='ns1')
    self._IndexDocument('test_index_2', 'id_two', [('name', 'two')],
                        namespace='ns1')
    self._IndexDocument('test_index_1', 'id_three', [('name', 'three')],
                        namespace='ns2')
    self._IndexDocument('test_index_default_namespace', 'id_four',
                        [('name', 'four')])
    self.stub.Write()
    del self.stub

    self.stub = simple_search_stub.SearchServiceStub(index_file=filename)
    self.CheckListIndexesResponse(
        self._ListIndexes(namespace='ns1'), ['test_index_1', 'test_index_2'],
        namespace_list=['ns1', 'ns1'])
    self.CheckListIndexesResponse(
        self._ListIndexes(namespace='ns2'), ['test_index_1'],
        namespace_list=['ns2'])
    self.CheckListIndexesResponse(
        self._ListIndexes(), ['test_index_default_namespace'],
        namespace_list=[''])

    response = self._ListDocuments(index='test_index_1', namespace='ns1')
    self.assertEqual(1, len(response.document))
    self.assertEqual('id_one', response.document[0].id)

    response = self._ListDocuments(index='test_index_1', namespace='ns2')
    self.assertEqual(1, len(response.document))
    self.assertEqual('id_three', response.document[0].id)

    response = self._ListDocuments(index='test_index_2', namespace='ns1')
    self.assertEqual(1, len(response.document))
    self.assertEqual('id_two', response.document[0].id)

  def testDefaultToGlobalNamespace(self):
    self._IndexDocument(
        'test_index', 'id_one', [('hello', 'world')], namespace=None)

    default_namespace = namespace_manager.get_namespace()
    response = self._Search(
        self._CreateSearchRequest(
            'test_index', 'world', namespace=default_namespace))
    self.assertEqual(1, response.matched_count)

  def testSearchNonexistentField(self):
    self._IndexDocument('test_index', 'id_one', [('hello', 'foo')])
    response = self._Search(self._CreateSearchRequest('test_index', 'foo:foo'))
    self.assertEqual(0, response.matched_count)

  def testSearchWithWrongConsistency(self):
    index_spec_1 = search_service_pb2.IndexSpec()
    index_spec_1.name = 'idx'
    index_spec_1.consistency = search_service_pb2.IndexSpec.GLOBAL

    index_spec_2 = search_service_pb2.IndexSpec()
    index_spec_2.name = 'idx'
    index_spec_2.consistency = search_service_pb2.IndexSpec.PER_DOCUMENT

    self._IndexDocument(index_spec_1, 'id1', [('field', 'value')])
    response = self._Search(
        self._CreateSearchRequest(index_spec_2, 'field:value'))
    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status.code)
    self.assertEqual(1, response.matched_count)

  def testMatchBadType(self):
    self._IndexDocument('test_index', 'id_one',
                        [('x', '7', document_pb2.FieldValue.TEXT)])

    response = self._Search(self._CreateSearchRequest('test_index', 'x:7'))
    self.assertEqual(1, response.matched_count)

  def testScoreWithoutAllTermsMatching(self):
    """Ensure that scoring works even when not all terms are found."""

    self._IndexDocument('test_index', 'id_one', [('field', 'test')])
    response = self._Search(
        self._CreateSearchRequest(
            'test_index',
            'test OR foo',
            scorer=search_service_pb2.ScorerSpec.MATCH_SCORER))

    self.assertEqual(search_service_pb2.SearchServiceError.OK,
                     response.status.code)
    self.assertEqual(1, response.matched_count)

  def testSnippets(self):
    self._IndexDocument('test_index', 'id1', [('text', """
             General relativity, or the general theory of relativity, is the
             geometric theory of gravitation published by Albert Einstein in
             1916 and the current description of gravitation in modern physics.
             General relativity generalises special relativity and Newton's law
             of universal gravitation, providing a unified description of
             gravity as a geometric property of space and time, or spacetime. In
             particular, the curvature of spacetime is directly related to the
             energy and momentum of whatever matter and radiation are present.
             The relation is specified by the Einstein field equations, a system
             of partial differential equations.
             """, document_pb2.FieldValue.TEXT)])

    req = self._CreateSearchRequest('test_index', 'property')
    field_spec = req.field_spec
    expr = field_spec.expression.add()
    expr.name = 'summary'
    expr.expression = 'snippet("property", text)'

    resp = self._Search(req)
    self.assertEqual(1, resp.matched_count)

    search_result = resp.result[0]
    self.assertEqual(1, len(search_result.expression))

    expression = search_result.expression[0]
    self.assertEqual('summary', expression.name)

    snippet = expression.value.string_value
    self.assertTrue(len(snippet) <= 160 + len('...<b></b>...'))
    self.assertTrue('<b>property</b>' in snippet)

  def _CheckSortOrder(
      self, sort_expr, expected_ids, default_text=None, default_numeric=None):
    req = self._CreateSearchRequest('test_index', 'common:yes')
    sort_spec = req.sort_spec.add()
    sort_spec.sort_expression = sort_expr
    sort_spec.sort_descending = False
    if default_numeric != None:
      sort_spec.default_value_numeric = default_numeric
    else:
      sort_spec.default_value_text = ''

    resp = self._Search(req)
    self.assertEqual(expected_ids,
                     [result.document.id for result in resp.result])

  def testSimpleSorting(self):
    self._IndexDocument('test_index', 'id1', [
        ('text', 'hello', document_pb2.FieldValue.TEXT),
        ('num', '9', document_pb2.FieldValue.NUMBER),
        ('date', '2000-1-1', document_pb2.FieldValue.DATE),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id2', [
        ('text', 'world', document_pb2.FieldValue.TEXT),
        ('num', '2', document_pb2.FieldValue.NUMBER),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id3', [
        ('text', 'test', document_pb2.FieldValue.TEXT),
        ('num', '12.1', document_pb2.FieldValue.NUMBER),
        ('date', '2012-12-21', document_pb2.FieldValue.DATE),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id4', [
        ('text', 'foo', document_pb2.FieldValue.TEXT),
        ('num', '-1', document_pb2.FieldValue.NUMBER),
        ('date', '2052-12-21', document_pb2.FieldValue.DATE),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id5', [
        ('text', 'bar', document_pb2.FieldValue.TEXT),
        ('date', '1985-12-21', document_pb2.FieldValue.DATE),
        ('common', 'yes'),
    ])

    self._CheckSortOrder(
        'text', ['id5', 'id4', 'id1', 'id3', 'id2'], default_text='')
    self._CheckSortOrder(
        'num', ['id4', 'id2', 'id5', 'id1', 'id3'], default_numeric=4)

    self._CheckSortOrder(
        'date', ['id5', 'id1', 'id2', 'id3', 'id4'],
        default_numeric=1322697600000)

  def testMultidimensionalSorting(self):
    self._IndexDocument('test_index', 'id1', [
        ('text', 'hello', document_pb2.FieldValue.TEXT),
        ('num', '9', document_pb2.FieldValue.NUMBER),
        ('date', '2000-1-1', document_pb2.FieldValue.DATE),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id2', [
        ('text', 'world', document_pb2.FieldValue.TEXT),
        ('num', '9', document_pb2.FieldValue.NUMBER),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id3', [
        ('text', 'test', document_pb2.FieldValue.TEXT),
        ('num', '9', document_pb2.FieldValue.NUMBER),
        ('date', '2012-12-21', document_pb2.FieldValue.DATE),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id4', [
        ('text', 'foo', document_pb2.FieldValue.TEXT),
        ('num', '1', document_pb2.FieldValue.NUMBER),
        ('date', '2052-12-21', document_pb2.FieldValue.DATE),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id5', [
        ('text', 'bar', document_pb2.FieldValue.TEXT),
        ('date', '1985-12-21', document_pb2.FieldValue.DATE),
        ('common', 'yes'),
    ])

    req = self._CreateSearchRequest('test_index', 'common:yes')
    sort_spec = req.sort_spec.add()
    sort_spec.sort_expression = 'num'
    sort_spec.sort_descending = False
    sort_spec.default_value_numeric = 3
    sort_spec = req.sort_spec.add()
    sort_spec.sort_expression = 'text'
    sort_spec.sort_descending = True
    sort_spec.default_value_text = ''

    resp = self._Search(req)
    self.assertEqual(['id4', 'id5', 'id2', 'id3', 'id1'],
                     [result.document.id for result in resp.result])

  def testSortOnExpression(self):
    self._IndexDocument('test_index', 'id1', [
        ('price', '90', document_pb2.FieldValue.NUMBER),
        ('repeat', 'test'),
        ('repeat', 'this'),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id2', [
        ('price', '10', document_pb2.FieldValue.NUMBER),
        ('shipping', '20', document_pb2.FieldValue.NUMBER),
        ('repeat', 'test'),
        ('common', 'yes'),
    ])
    self._IndexDocument('test_index', 'id3', [
        ('price', '100', document_pb2.FieldValue.NUMBER),
        ('shipping', '-20', document_pb2.FieldValue.NUMBER),
        ('common', 'yes'),
    ])

    self._CheckSortOrder(
        'price + shipping', ['id2', 'id3', 'id1'], default_numeric=100)
    self._CheckSortOrder(
        'price + 10 * shipping', ['id3', 'id1', 'id2'], default_numeric=100)


    req = self._CreateSearchRequest('test_index', 'common:yes')
    sort_spec = req.sort_spec.add()
    sort_spec.default_value_text = ''
    sort_spec.sort_expression = 'count(repeat)'
    resp = self._Search(req)
    self.assertEqual(
        'Failed to parse sort expression \'count(repeat)'
        '\': count() is not supported in sort expressions',
        resp.status.error_detail)
    self.assertEqual(search_service_pb2.SearchServiceError.INVALID_REQUEST,
                     resp.status.code)

  def testCjk(self):
    self._IndexDocument(
        'index', 'id0',
        [('f', u'\u308f\u305f\u3057 \u306f \u3046\u3043\u308b \u3067\u3059')])

    resp = self._Search(self._CreateSearchRequest('index', u'\u306f'))
    self.assertEqual(1, resp.matched_count)

    resp = self._Search(self._CreateSearchRequest('index', u'f:\u306f'))
    self.assertEqual(1, resp.matched_count)

  def testUnicode(self):
    paradox = u"""
    Russell's Paradox: <br/>
                       ∃ y∀ x(x∈ y ⇔ P(x)) <br/>
                       Let P(x)=~(x∈ x), x=y. <br/>
                       y∈ y ⇔ ~(y∈ y)
    """
    self._IndexDocument('index', 'id0', [('f', paradox)])

    resp = self._Search(self._CreateSearchRequest('index', 'Let'))
    self.assertEqual(1, resp.matched_count)
    req = self._CreateSearchRequest('index', 'Let', returned_fields=['f'])
    resp = self._Search(req)
    self.assertEqual(1, resp.matched_count)

  def testExpressions(self):
    self._IndexDocument('index', 'id0', [
        ('text', 'test text one two', document_pb2.FieldValue.TEXT),
        ('repeat', 'one', document_pb2.FieldValue.TEXT),
        ('repeat', 'two', document_pb2.FieldValue.TEXT),
        ('num1', '4', document_pb2.FieldValue.NUMBER),
        ('num2', '10.1', document_pb2.FieldValue.NUMBER),
        ('num3', '-4.5', document_pb2.FieldValue.NUMBER),
        ('num4', '-40', document_pb2.FieldValue.NUMBER),
    ])

    def CheckExpression(expression, expect_value, expect_type, cast=None):
      if cast is None:
        cast = lambda x: x

      req = self._CreateSearchRequest('index', 'text:text')
      field_spec = req.field_spec
      field_expr = field_spec.expression.add()
      field_expr.name = 'test'
      field_expr.expression = expression

      resp = self._Search(req)
      self.assertEqual(1, resp.matched_count)

      exprs = resp.result[0].expression
      self.assertEqual(1, len(exprs))

      expr = exprs[0]
      self.assertEqual('test', expr.name)
      self.assertEqual(expect_type, expr.value.type)
      self.assertEqual(expect_value, cast(expr.value.string_value),
                       'String value: %s' % expr.value.string_value)

    CheckExpression('text', 'test text one two', document_pb2.FieldValue.HTML)
    CheckExpression('1 + 2', 3, document_pb2.FieldValue.NUMBER, cast=float)
    CheckExpression(
        'num1 + num2', 14.1, document_pb2.FieldValue.NUMBER, cast=float)
    CheckExpression(
        'count(repeat)', 2, document_pb2.FieldValue.NUMBER, cast=float)

  def testMatchAtomFieldsExactly(self):
    self._IndexDocument('index', 'id0',
                        [('atom', 'just a test', document_pb2.FieldValue.ATOM)])
    self._IndexDocument('index', 'id1',
                        [('atom', 'test a just', document_pb2.FieldValue.ATOM)])
    self._IndexDocument('index', 'id2',
                        [('atom', 'test', document_pb2.FieldValue.ATOM)])

    response = self._Search(
        self._CreateSearchRequest('index', 'atom:"just a test"'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('id0', response.result[0].document.id)

    response = self._Search(
        self._CreateSearchRequest('index', 'atom:test'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('id2', response.result[0].document.id)

    response = self._Search(
        self._CreateSearchRequest('index', 'atom:just'))
    self.assertEqual(0, response.matched_count)

  def testCaseSensitiveFieldNames(self):
    self._IndexDocument(
        'index', 'id0', [
            ('Author', 'Will'),
            ('CONTENT', 'pass the test please'),
            ])
    self._IndexDocument(
        'index', 'id1', [
            ('author', 'Will'),
            ])

    response = self._Search(self._CreateSearchRequest('index', 'Author:Will'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('id0', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest('index', 'author:Will'))
    self.assertEqual(1, response.matched_count)
    self.assertEqual('id1', response.result[0].document.id)

    response = self._Search(self._CreateSearchRequest('index', 'aUTHOR:Will'))
    self.assertEqual(0, response.matched_count)

    response = self._Search(self._CreateSearchRequest('index', 'CONTENT:pass'))
    self.assertEqual(1, response.matched_count)

    response = self._Search(self._CreateSearchRequest('index', 'cONTENT:pass'))
    self.assertEqual(0, response.matched_count)

    response = self._Search(self._CreateSearchRequest('index', 'content:pass'))
    self.assertEqual(0, response.matched_count)

  def testSearchRepeatedFields(self):
    self._IndexDocument(
        'index', 'id0', [('test', 'stuff'), ('test', 'things')])

    response = self._Search(self._CreateSearchRequest('index', 'test:stuff'))
    self.assertEqual(1, response.matched_count)

    response = self._Search(self._CreateSearchRequest('index', 'test:things'))
    self.assertEqual(1, response.matched_count)

  def testSearchDocumentWithGeo(self):
    request = search_service_pb2.IndexDocumentRequest()

    doc = request.params.document.add()
    doc.id = 'doc_id'

    geo_field = doc.field.add()
    geo_field.name = 'field'
    geo_field_value = geo_field.value
    geo_field_value.type = document_pb2.FieldValue.GEO

    geo = geo_field_value.geo
    geo.lat = 33.87
    geo.lng = 151.21

    text_field = doc.field.add()
    text_field.name = 'textfield'
    text_field_value = text_field.value
    text_field_value.type = document_pb2.FieldValue.TEXT
    text_field_value.string_value = 'some text'

    self._SetIndexSpec('index', request.params.index_spec)
    response = search_service_pb2.IndexDocumentResponse()
    self.stub.MakeSyncCall('search', 'IndexDocument', request, response)

    search_response = self._Search(self._CreateSearchRequest('index', 'some'))
    self.assertEqual(1, search_response.matched_count)


    search_response = self._Search(
        self._CreateSearchRequest('index', 'field:71'))
    self.assertEqual(0, search_response.matched_count)

  def testDecodeCursor_invalidEncoding(self):
    self.assertRaises(
        simple_search_stub._InvalidCursorException,
        self.stub._DecodeCursor, 'this is invalid', 'bar')

  def testDecodeCursor_cursorHasNoSeparatorToken(self):
    self.assertRaises(simple_search_stub._InvalidCursorException,
                      self.stub._DecodeCursor,
                      base64.urlsafe_b64encode(b'this-has-no-separator'), 'bar')

  def testDecodeCursor_cursorDoesNotMatchQuery(self):
    self.assertRaises(simple_search_stub._InvalidCursorException,
                      self.stub._DecodeCursor,
                      base64.urlsafe_b64encode(b'this|wont match'),
                      'some query')

  def testDecodeCursor_cursorMatchesQuery(self):
    doc_id = '1234'
    query = b'query'
    doc_id_hash = hashlib.sha224(six.ensure_binary(doc_id) + query).hexdigest()
    cursor = base64.urlsafe_b64encode(
        six.ensure_binary(doc_id_hash) + b'|' + six.ensure_binary(doc_id))
    self.assertEqual(doc_id, self.stub._DecodeCursor(cursor, query))


def main(unused_argv):
  absltest.main()


if __name__ == '__main__':
  absltest.main(main)
