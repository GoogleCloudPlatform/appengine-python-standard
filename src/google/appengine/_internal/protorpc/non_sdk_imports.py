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
"""Dynamically decide from where to import other non SDK Google modules.

All other protorpc code should import other non SDK modules from
this module. If necessary, add new imports here (in both places).
"""






try:
  from google.protobuf import descriptor
  normal_environment = True
except ImportError:

  from google.protobuf import descriptor

  normal_environment = False

if normal_environment:
  from google.protobuf import descriptor_pb2
  from google.protobuf import message
  from google.protobuf import reflection

else:
  from google.protobuf import message
  from google.protobuf import reflection
  from google.net.proto2.proto import descriptor_pb2

