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



"""The Python datastore protocol buffer definition (old name)."""











from google.appengine.api.api_base_pb2 import Integer64Proto
from google.appengine.api.api_base_pb2 import StringProto
from google.appengine.api.api_base_pb2 import VoidProto
from google.appengine.datastore import datastore_v3_bytes_pb2 as datastore_v3_pb2
from google.appengine.datastore.datastore_v3_bytes_pb2 import *
from google.appengine.datastore.action_pb2 import Action
from google.appengine.datastore.entity_bytes_pb2 import CompositeIndex
from google.appengine.datastore.entity_bytes_pb2 import EntityProto
from google.appengine.datastore.entity_bytes_pb2 import Index
from google.appengine.datastore.entity_bytes_pb2 import Path
from google.appengine.datastore.entity_bytes_pb2 import Property
from google.appengine.datastore.entity_bytes_pb2 import PropertyValue
from google.appengine.datastore.entity_bytes_pb2 import Reference
from google.appengine.datastore.snapshot_pb2 import Snapshot
