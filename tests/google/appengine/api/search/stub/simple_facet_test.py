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
"""Tests for google.appengine.api.search.stub.simple_facet."""

import six

from google.appengine.api.search import search
from google.appengine.api.search import search_service_pb2
from google.appengine.api.search.stub import simple_facet
from google.appengine.datastore import document_pb2
from absl.testing import absltest


class _DocHolder(object):

  def __init__(self, document):
    self._document = document

  @property
  def document(self):
    return self._document


def _ConvertToProtoBuffDoc(doc):
  doc_pb = document_pb2.Document()
  search._CopyDocumentToProtocolBuffer(doc, doc_pb)



  return _DocHolder(doc_pb)


class SimpleFacetTest(absltest.TestCase):

  _DOC1 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc1', facets=[search.AtomFacet('genre', 'sci-fi'),
                             search.NumberFacet('rating', 3.5),
                             search.AtomFacet('type', 'movie'),
                             search.NumberFacet('year', 1995)]))
  _DOC2 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc2', facets=[search.AtomFacet('genre', 'fantasy'),
                             search.NumberFacet('rating', 2.0),
                             search.AtomFacet('type', 'movie'),
                             search.NumberFacet('year', 2003)]))
  _DOC3 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc3', facets=[search.AtomFacet('wine_type', 'red'),
                             search.AtomFacet('type', 'wine'),
                             search.NumberFacet('vintage', 1991)]))
  _DOC4 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc4', facets=[search.AtomFacet('genre', 'kids'),
                             search.AtomFacet('genre', 'fantasy'),
                             search.NumberFacet('rating', 1.5),
                             search.AtomFacet('type', 'movie'),
                             search.NumberFacet('year', 2000)]))
  _DOC5 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc5', facets=[search.AtomFacet('wine_type', 'white'),
                             search.AtomFacet('type', 'wine'),
                             search.NumberFacet('vintage', 1995)]))
  _DOC6 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc6', facets=[search.AtomFacet('wine_type', 'white'),
                             search.AtomFacet('type', 'wine'),
                             search.NumberFacet('vintage', 1898)]))
  _DOC7 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc7', facets=[search.AtomFacet('wine_type', 'white'),
                             search.AtomFacet('type', 'wine'),
                             search.NumberFacet('vintage', 1990)]))
  _DOC8 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc8', facets=[search.AtomFacet('wine_type', 'red'),
                             search.AtomFacet('type', 'wine'),
                             search.NumberFacet('vintage', 1988)]))
  _DOC9 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc9', facets=[search.AtomFacet('genre', 'fantasy'),
                             search.NumberFacet('rating', 4.0),
                             search.AtomFacet('type', 'movie'),
                             search.NumberFacet('year', 2010)]))
  _DOC10 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc10', facets=[search.AtomFacet('genre', 'fantasy'),
                              search.NumberFacet('rating', 3.9),
                              search.AtomFacet('type', 'movie'),
                              search.NumberFacet('year', 2011)]))
  _DOC11 = _ConvertToProtoBuffDoc(search.ScoredDocument(
      doc_id='doc11', facets=[search.AtomFacet('genre', 'sci-fi'),
                              search.NumberFacet('rating', 2.9),
                              search.AtomFacet('type', 'movie'),
                              search.NumberFacet('year', 2009)]))
  _RESULTS = [_DOC1, _DOC2, _DOC3, _DOC4, _DOC5,
              _DOC6, _DOC7, _DOC8, _DOC9, _DOC10, _DOC11]

  def _MakeSearchParams(self, refinement_pairs=None,
                        set_auto_discover_facet_count=None,
                        manual_facets=None,
                        depth=None):
    params = search_service_pb2.SearchParams()
    if refinement_pairs:
      for ref in refinement_pairs:
        ref_pb = params.facet_refinement.add()
        ref_pb.name = ref[0]
        if len(ref) == 2:
          ref_pb.value = str(ref[1])
        else:
          range_pb = ref_pb.range
          if ref[1] is not None:
            range_pb.start = str(ref[1])
          if ref[2] is not None:
            range_pb.end = str(ref[2])
    if set_auto_discover_facet_count:
      params.auto_discover_facet_count = set_auto_discover_facet_count
    if manual_facets:
      for manual_facet in manual_facets:
        manual_facet_pb = params.include_facet.add()
        if isinstance(manual_facet, six.string_types):
          manual_facet_pb.name = manual_facet
        else:
          manual_facet_pb.name = manual_facet['name']
          manual_facet_param_pb = manual_facet_pb.params
          if 'value_limit' in manual_facet:
            manual_facet_param_pb.value_limit = manual_facet['value_limit']
          if 'values' in manual_facet:
            for value in manual_facet['values']:
              manual_facet_param_pb.value_constraint.append(value)
          if 'ranges' in manual_facet:
            for r in manual_facet['ranges']:
              range_pb = manual_facet_param_pb.range.add()
              range_pb.name = r[0]
              if r[1] is not None:
                range_pb.start = str(r[1])
              if r[2] is not None:
                range_pb.end = str(r[2])
    if depth is not None:
      params.facet_depth = depth
    return params

  def _MakeFacetResult(self, name, values):
    result_pb = search_service_pb2.FacetResult()
    result_pb.name = name
    for value in values:
      value_pb = result_pb.value.add()
      if len(value) == 2:
        value_pb.name = value[0]
        value_pb.count = value[1]
        ref_pb = value_pb.refinement
        ref_pb.name = name
        ref_pb.value = str(value[0])
      elif len(value) == 4:
        value_pb.name = value[0]
        value_pb.count = value[1]
        ref_pb = value_pb.refinement
        ref_pb.name = name
        range_pb = ref_pb.range
        if value[2] is not None:
          range_pb.start = str(value[2])
        if value[3] is not None:
          range_pb.end = str(value[3])
      else:
        self.fail('Invalid test case.')
    return result_pb

  def testAutoDiscoverFacetsOnly(self):
    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(set_auto_discover_facet_count=10))
    expected_result = [
        self._MakeFacetResult('type', [('movie', 6), ('wine', 5)]),
        self._MakeFacetResult(
            'genre', [('fantasy', 4), ('sci-fi', 2), ('kids', 1)]),
        self._MakeFacetResult('wine_type', [('white', 3), ('red', 2)]),
        self._MakeFacetResult(
            'year', [('[1995.0,2011.0)', 6, '1995.0', '2011.0')]),
        self._MakeFacetResult('rating', [('[1.5,4.0)', 6, '1.5', '4.0')]),
        self._MakeFacetResult(
            'vintage', [('[1898.0,1995.0)', 5, '1898.0', '1995.0')])]
    actual_response = search_service_pb2.SearchResponse()
    facet_analyzer.FillFacetResponse(self._RESULTS, actual_response)
    self.assertCountEqual(expected_result, actual_response.facet_result)

    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(set_auto_discover_facet_count=2))
    expected_result = [
        self._MakeFacetResult('type', [('movie', 6), ('wine', 5)]),
        self._MakeFacetResult(
            'genre', [('fantasy', 4), ('sci-fi', 2), ('kids', 1)])]
    actual_response = search_service_pb2.SearchResponse()
    facet_analyzer.FillFacetResponse(self._RESULTS, actual_response)
    self.assertCountEqual(expected_result, actual_response.facet_result)

  def testManualFacetsWithNameOnly(self):
    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(manual_facets=['type', 'rating']))
    expected_result = [
        self._MakeFacetResult('type', [('movie', 6), ('wine', 5)]),
        self._MakeFacetResult('rating', [('[1.5,4.0)', 6, '1.5', '4.0')])]
    actual_response = search_service_pb2.SearchResponse()
    facet_analyzer.FillFacetResponse(self._RESULTS, actual_response)
    self.assertCountEqual(expected_result, actual_response.facet_result)

    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(manual_facets=['type', 'rating'],
                               set_auto_discover_facet_count=2))
    expected_result = [
        self._MakeFacetResult('type', [('movie', 6), ('wine', 5)]),
        self._MakeFacetResult(
            'genre', [('fantasy', 4), ('sci-fi', 2), ('kids', 1)]),
        self._MakeFacetResult(
            'year', [('[1995.0,2011.0)', 6, '1995.0', '2011.0')]),
        self._MakeFacetResult('rating', [('[1.5,4.0)', 6, '1.5', '4.0')])]
    actual_response = search_service_pb2.SearchResponse()
    facet_analyzer.FillFacetResponse(self._RESULTS, actual_response)
    self.assertCountEqual(expected_result, actual_response.facet_result)

  def testManualFacetsWithValueConstraint(self):
    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(
            manual_facets=[{'name': 'genre', 'values': ['sci-fi', 'fantasy']}]))
    expected_result = [
        self._MakeFacetResult('genre', [('fantasy', 4), ('sci-fi', 2)])]
    actual_response = search_service_pb2.SearchResponse()
    facet_analyzer.FillFacetResponse(self._RESULTS, actual_response)
    self.assertCountEqual(expected_result, actual_response.facet_result)

  def testManualFacetsWithValueLimit(self):
    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(
            manual_facets=[{'name': 'genre', 'value_limit': 1}]))
    expected_result = [
        self._MakeFacetResult('genre', [('fantasy', 4)])]
    actual_response = search_service_pb2.SearchResponse()
    facet_analyzer.FillFacetResponse(self._RESULTS, actual_response)
    self.assertCountEqual(expected_result, actual_response.facet_result)

  def testManualFacetsWithRange(self):
    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(
            manual_facets=[{'name': 'year', 'ranges':
                            [('pri-2000', None, 2000),
                             ('2000-2005', 2000, 2005),
                             ('post-2005', 2005, None)]}]))
    expected_result = [
        self._MakeFacetResult('year', [('post-2005', 3, '2005.0', None),
                                       ('2000-2005', 2, '2000.0', '2005.0'),
                                       ('pri-2000', 1, None, '2000.0')])]
    actual_response = search_service_pb2.SearchResponse()
    facet_analyzer.FillFacetResponse(self._RESULTS, actual_response)
    self.assertCountEqual(expected_result, actual_response.facet_result)

  def testRefineResults(self):
    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(refinement_pairs=[('type', 'wine')]))
    self.assertEqual([
        SimpleFacetTest._DOC3, SimpleFacetTest._DOC5, SimpleFacetTest._DOC6,
        SimpleFacetTest._DOC7, SimpleFacetTest._DOC8
    ], facet_analyzer.RefineResults(self._RESULTS))

    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(refinement_pairs=[('rating', 2.0, None)]))
    self.assertEqual([
        SimpleFacetTest._DOC1, SimpleFacetTest._DOC2, SimpleFacetTest._DOC9,
        SimpleFacetTest._DOC10, SimpleFacetTest._DOC11
    ], facet_analyzer.RefineResults(self._RESULTS))

    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(refinement_pairs=[('rating', 2.0, 3.5)]))
    self.assertEqual([SimpleFacetTest._DOC2, SimpleFacetTest._DOC11],
                     facet_analyzer.RefineResults(self._RESULTS))

    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(refinement_pairs=[('rating', None, 2.1)]))
    self.assertEqual([SimpleFacetTest._DOC2, SimpleFacetTest._DOC4],
                     facet_analyzer.RefineResults(self._RESULTS))

    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(refinement_pairs=[('type','movie'),
                                                 ('year', 2000)]))
    self.assertEqual([SimpleFacetTest._DOC4],
                     facet_analyzer.RefineResults(self._RESULTS))

    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(refinement_pairs=[('type', 'movie'),
                                                 ('year', 2000),
                                                 ('year', 1995)]))
    self.assertEqual([SimpleFacetTest._DOC1, SimpleFacetTest._DOC4],
                      facet_analyzer.RefineResults(self._RESULTS))

  def testFacetDepth(self):
    facet_analyzer = simple_facet.SimpleFacet(
        self._MakeSearchParams(set_auto_discover_facet_count=10, depth=1))
    expected_result = [
        self._MakeFacetResult('type', [('movie', 1)]),
        self._MakeFacetResult('genre', [('sci-fi', 1)]),
        self._MakeFacetResult(
            'year', [('[1995.0,1995.0)', 1, '1995.0', '1995.0')]),
        self._MakeFacetResult('rating', [('[3.5,3.5)', 1, '3.5', '3.5')])]
    actual_response = search_service_pb2.SearchResponse()
    facet_analyzer.FillFacetResponse(self._RESULTS, actual_response)
    self.assertCountEqual(expected_result, actual_response.facet_result)


if __name__ == '__main__':
  absltest.main()
