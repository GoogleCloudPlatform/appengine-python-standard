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


from google.appengine.base import capabilities_pb2 as google_dot_appengine_dot_base_dot_capabilities__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n:google/appengine/api/capabilities/capability_service.proto\x12\x10google.appengine\x1a(google/appengine/base/capabilities.proto\"E\n\x10IsEnabledRequest\x12\x0f\n\x07package\x18\x01 \x02(\t\x12\x12\n\ncapability\x18\x02 \x03(\t\x12\x0c\n\x04\x63\x61ll\x18\x03 \x03(\t\"\x9f\x02\n\x11IsEnabledResponse\x12I\n\x0esummary_status\x18\x01 \x01(\x0e\x32\x31.google.appengine.IsEnabledResponse.SummaryStatus\x12\x1c\n\x14time_until_scheduled\x18\x02 \x01(\x03\x12\x32\n\x06\x63onfig\x18\x03 \x03(\x0b\x32\".google.appengine.CapabilityConfig\"m\n\rSummaryStatus\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x14\n\x10SCHEDULED_FUTURE\x10\x02\x12\x11\n\rSCHEDULED_NOW\x10\x03\x12\x0c\n\x08\x44ISABLED\x10\x04\x12\x0b\n\x07UNKNOWN\x10\x05\x42?\n%com.google.appengine.api.capabilitiesB\x13\x43\x61pabilityServicePb\x88\x01\x01')



_ISENABLEDREQUEST = DESCRIPTOR.message_types_by_name['IsEnabledRequest']
_ISENABLEDRESPONSE = DESCRIPTOR.message_types_by_name['IsEnabledResponse']
_ISENABLEDRESPONSE_SUMMARYSTATUS = _ISENABLEDRESPONSE.enum_types_by_name['SummaryStatus']
IsEnabledRequest = _reflection.GeneratedProtocolMessageType('IsEnabledRequest', (_message.Message,), {
  'DESCRIPTOR' : _ISENABLEDREQUEST,
  '__module__' : 'google.appengine.api.capabilities.capability_service_pb2'

  })
_sym_db.RegisterMessage(IsEnabledRequest)

IsEnabledResponse = _reflection.GeneratedProtocolMessageType('IsEnabledResponse', (_message.Message,), {
  'DESCRIPTOR' : _ISENABLEDRESPONSE,
  '__module__' : 'google.appengine.api.capabilities.capability_service_pb2'

  })
_sym_db.RegisterMessage(IsEnabledResponse)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.google.appengine.api.capabilitiesB\023CapabilityServicePb\210\001\001'
  _ISENABLEDREQUEST._serialized_start=122
  _ISENABLEDREQUEST._serialized_end=191
  _ISENABLEDRESPONSE._serialized_start=194
  _ISENABLEDRESPONSE._serialized_end=481
  _ISENABLEDRESPONSE_SUMMARYSTATUS._serialized_start=372
  _ISENABLEDRESPONSE_SUMMARYSTATUS._serialized_end=481

