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


"""Callbacks the runtime invokes when requests end."""



import os



REQUEST_ID_KEY = 'HTTP_X_CLOUD_TRACE_CONTEXT'
_callback_storage = {}


def SetRequestEndCallback(callback):
  """Stores a callback by the request ID.

  The request ID currently uses the cloud trace ID.

  Args:
    callback: A zero-argument callable whose return value is unused.
  """
  req_id = GetRequestId()




  if req_id:
    _callback_storage.setdefault(req_id, []).append(callback)


def InvokeCallbacks():
  """Invokes the callbacks associated with the current request ID."""

  req_id = GetRequestId()
  if req_id in _callback_storage:
    for callback in _callback_storage[req_id]:
      callback(req_id)

    del _callback_storage[req_id]


def GetRequestId():
  """Returns a unique ID using the cloud trace ID."""
  if REQUEST_ID_KEY in os.environ:
    return os.environ[REQUEST_ID_KEY]
  else:
    return None

