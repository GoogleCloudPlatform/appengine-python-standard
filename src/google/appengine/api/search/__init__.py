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


"""Search API module."""

from google.appengine.api.search.search import AtomFacet
from google.appengine.api.search.search import AtomField
from google.appengine.api.search.search import Cursor
from google.appengine.api.search.search import DateField
from google.appengine.api.search.search import DeleteError
from google.appengine.api.search.search import DeleteResult
from google.appengine.api.search.search import Document
from google.appengine.api.search.search import DOCUMENT_ID_FIELD_NAME
from google.appengine.api.search.search import Error
from google.appengine.api.search.search import ExpressionError
from google.appengine.api.search.search import Facet
from google.appengine.api.search.search import FacetOptions
from google.appengine.api.search.search import FacetRange
from google.appengine.api.search.search import FacetRefinement
from google.appengine.api.search.search import FacetRequest
from google.appengine.api.search.search import FacetResult
from google.appengine.api.search.search import FacetResultValue
from google.appengine.api.search.search import Field
from google.appengine.api.search.search import FieldExpression
from google.appengine.api.search.search import GeoField
from google.appengine.api.search.search import GeoPoint
from google.appengine.api.search.search import get_indexes
from google.appengine.api.search.search import get_indexes_async
from google.appengine.api.search.search import GetResponse
from google.appengine.api.search.search import HtmlField
from google.appengine.api.search.search import Index
from google.appengine.api.search.search import InternalError
from google.appengine.api.search.search import InvalidRequest
from google.appengine.api.search.search import LANGUAGE_FIELD_NAME
from google.appengine.api.search.search import MatchScorer
from google.appengine.api.search.search import MAXIMUM_DEPTH_FOR_FACETED_SEARCH
from google.appengine.api.search.search import MAXIMUM_DOCUMENT_ID_LENGTH
from google.appengine.api.search.search import MAXIMUM_DOCUMENTS_PER_PUT_REQUEST
from google.appengine.api.search.search import MAXIMUM_DOCUMENTS_RETURNED_PER_SEARCH
from google.appengine.api.search.search import MAXIMUM_EXPRESSION_LENGTH
from google.appengine.api.search.search import MAXIMUM_FACET_VALUES_TO_RETURN
from google.appengine.api.search.search import MAXIMUM_FACETS_TO_RETURN
from google.appengine.api.search.search import MAXIMUM_FIELD_ATOM_LENGTH
from google.appengine.api.search.search import MAXIMUM_FIELD_NAME_LENGTH
from google.appengine.api.search.search import MAXIMUM_FIELD_PREFIX_LENGTH
from google.appengine.api.search.search import MAXIMUM_FIELD_VALUE_LENGTH
from google.appengine.api.search.search import MAXIMUM_FIELDS_RETURNED_PER_SEARCH
from google.appengine.api.search.search import MAXIMUM_GET_INDEXES_OFFSET
from google.appengine.api.search.search import MAXIMUM_INDEX_NAME_LENGTH
from google.appengine.api.search.search import MAXIMUM_INDEXES_RETURNED_PER_GET_REQUEST
from google.appengine.api.search.search import MAXIMUM_NUMBER_FOUND_ACCURACY
from google.appengine.api.search.search import MAXIMUM_QUERY_LENGTH
from google.appengine.api.search.search import MAXIMUM_SEARCH_OFFSET
from google.appengine.api.search.search import MAXIMUM_SORTED_DOCUMENTS
from google.appengine.api.search.search import NumberFacet
from google.appengine.api.search.search import NumberField
from google.appengine.api.search.search import OperationResult
from google.appengine.api.search.search import PutError
from google.appengine.api.search.search import PutResult
from google.appengine.api.search.search import Query
from google.appengine.api.search.search import QueryError
from google.appengine.api.search.search import QueryOptions
from google.appengine.api.search.search import RANK_FIELD_NAME
from google.appengine.api.search.search import RescoringMatchScorer
from google.appengine.api.search.search import SCORE_FIELD_NAME
from google.appengine.api.search.search import ScoredDocument
from google.appengine.api.search.search import SearchResults
from google.appengine.api.search.search import SortExpression
from google.appengine.api.search.search import SortOptions
from google.appengine.api.search.search import TextField
from google.appengine.api.search.search import TIMESTAMP_FIELD_NAME
from google.appengine.api.search.search import TokenizedPrefixField
from google.appengine.api.search.search import TransientError
from google.appengine.api.search.search import UntokenizedPrefixField
from google.appengine.api.search.search import VECTOR_FIELD_MAX_SIZE
from google.appengine.api.search.search import VectorField
