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
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database


_sym_db = _symbol_database.Default()


from google.appengine.base import capabilities_pb2 as google_dot_appengine_dot_base_dot_capabilities__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/api/capabilities/capability_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n%com.google.appengine.api.capabilitiesB\023CapabilityServicePb\210\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n:google/appengine/api/capabilities/capability_service.proto\x12\x10google.appengine\x1a(google/appengine/base/capabilities.proto\"E\n\x10IsEnabledRequest\x12\x0f\n\x07package\x18\x01 \x02(\t\x12\x12\n\ncapability\x18\x02 \x03(\t\x12\x0c\n\x04\x63\x61ll\x18\x03 \x03(\t\"\x9f\x02\n\x11IsEnabledResponse\x12I\n\x0esummary_status\x18\x01 \x01(\x0e\x32\x31.google.appengine.IsEnabledResponse.SummaryStatus\x12\x1c\n\x14time_until_scheduled\x18\x02 \x01(\x03\x12\x32\n\x06\x63onfig\x18\x03 \x03(\x0b\x32\".google.appengine.CapabilityConfig\"m\n\rSummaryStatus\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x14\n\x10SCHEDULED_FUTURE\x10\x02\x12\x11\n\rSCHEDULED_NOW\x10\x03\x12\x0c\n\x08\x44ISABLED\x10\x04\x12\x0b\n\x07UNKNOWN\x10\x05\x42?\n%com.google.appengine.api.capabilitiesB\x13\x43\x61pabilityServicePb\x88\x01\x01'
  ,
  dependencies=[google_dot_appengine_dot_base_dot_capabilities__pb2.DESCRIPTOR,])



_ISENABLEDRESPONSE_SUMMARYSTATUS = _descriptor.EnumDescriptor(
  name='SummaryStatus',
  full_name='google.appengine.IsEnabledResponse.SummaryStatus',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DEFAULT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ENABLED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SCHEDULED_FUTURE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SCHEDULED_NOW', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DISABLED', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=372,
  serialized_end=481,
)
_sym_db.RegisterEnumDescriptor(_ISENABLEDRESPONSE_SUMMARYSTATUS)


_ISENABLEDREQUEST = _descriptor.Descriptor(
  name='IsEnabledRequest',
  full_name='google.appengine.IsEnabledRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='package', full_name='google.appengine.IsEnabledRequest.package', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='capability', full_name='google.appengine.IsEnabledRequest.capability', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='call', full_name='google.appengine.IsEnabledRequest.call', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=191,
)


_ISENABLEDRESPONSE = _descriptor.Descriptor(
  name='IsEnabledResponse',
  full_name='google.appengine.IsEnabledResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='summary_status', full_name='google.appengine.IsEnabledResponse.summary_status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time_until_scheduled', full_name='google.appengine.IsEnabledResponse.time_until_scheduled', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='config', full_name='google.appengine.IsEnabledResponse.config', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ISENABLEDRESPONSE_SUMMARYSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=481,
)

_ISENABLEDRESPONSE.fields_by_name['summary_status'].enum_type = _ISENABLEDRESPONSE_SUMMARYSTATUS
_ISENABLEDRESPONSE.fields_by_name['config'].message_type = google_dot_appengine_dot_base_dot_capabilities__pb2._CAPABILITYCONFIG
_ISENABLEDRESPONSE_SUMMARYSTATUS.containing_type = _ISENABLEDRESPONSE
DESCRIPTOR.message_types_by_name['IsEnabledRequest'] = _ISENABLEDREQUEST
DESCRIPTOR.message_types_by_name['IsEnabledResponse'] = _ISENABLEDRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

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


DESCRIPTOR._options = None

