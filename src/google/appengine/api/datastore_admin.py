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



"""The Python datastore admin API for managing indices and schemas.
"""








from google.appengine.api import api_base_pb2
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_types
from google.appengine.datastore import datastore_pb
from google.appengine.runtime import apiproxy_errors


def GetIndices(_app=None):
  """Fetches all composite indices in the datastore for this app.

  Returns:
    list of entity_pb.CompositeIndex
  """


  resolved_app_id = datastore_types.ResolveAppId(_app)

  req = datastore_pb.GetIndicesRequest()
  req.app_id = resolved_app_id
  resp = datastore_pb.CompositeIndices()
  resp = _Call('GetIndices', req, resp)
  return resp.index


def CreateIndex(index):
  """Creates a new composite index in the datastore for this app.

  Args:
    index: entity_pb.CompositeIndex

  Returns:
    int, the id allocated to the index
  """
  resp = api_base_pb2.Integer64Proto()
  resp = _Call('CreateIndex', index, resp)
  return resp.value


def UpdateIndex(index):
  """Updates an index's status. The entire index definition must be present.

  Args:
    index: entity_pb.CompositeIndex
  """
  _Call('UpdateIndex', index, api_base_pb2.VoidProto())


def DeleteIndex(index):
  """Deletes an index. The entire index definition must be present.

  Args:
    index: entity_pb.CompositeIndex
  """
  _Call('DeleteIndex', index, api_base_pb2.VoidProto())


def _Call(call, req, resp):
  """Generic method for making a datastore API call.

  Args:
    call: string, the name of the RPC call
    req: the request PB. if the app_id field is not set, it defaults to the
      local app.
    resp: the response PB
  """
  if hasattr(req, 'app_id'):
    req.app_id = datastore_types.ResolveAppId(req.app_id)

  try:
    result = apiproxy_stub_map.MakeSyncCall('datastore_v3', call, req, resp)
    if result:
      return result
    return resp
  except apiproxy_errors.ApplicationError as err:
    raise datastore._ToDatastoreError(err)
