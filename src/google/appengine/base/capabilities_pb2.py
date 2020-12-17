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




DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/base/capabilities.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n%com.google.appengine.api.capabilitiesB\016CapabilitiesPb\370\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n(google/appengine/base/capabilities.proto\x12\x10google.appengine\"\x86\x01\n\x14\x43\x61pabilityConfigList\x12\x32\n\x06\x63onfig\x18\x01 \x03(\x0b\x32\".google.appengine.CapabilityConfig\x12:\n\x0e\x64\x65\x66\x61ult_config\x18\x02 \x01(\x0b\x32\".google.appengine.CapabilityConfig\"\xa9\x02\n\x10\x43\x61pabilityConfig\x12\x0f\n\x07package\x18\x01 \x02(\t\x12\x12\n\ncapability\x18\x02 \x02(\t\x12\x42\n\x06status\x18\x03 \x01(\x0e\x32).google.appengine.CapabilityConfig.Status:\x07UNKNOWN\x12\x16\n\x0escheduled_time\x18\x07 \x01(\t\x12\x18\n\x10internal_message\x18\x04 \x01(\t\x12\x15\n\radmin_message\x18\x05 \x01(\t\x12\x15\n\rerror_message\x18\x06 \x01(\t\"L\n\x06Status\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\r\n\tSCHEDULED\x10\x02\x12\x0c\n\x08\x44ISABLED\x10\x03\x12\x0b\n\x07UNKNOWN\x10\x04\x42:\n%com.google.appengine.api.capabilitiesB\x0e\x43\x61pabilitiesPb\xf8\x01\x01'
)



_CAPABILITYCONFIG_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='google.appengine.CapabilityConfig.Status',
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
      name='SCHEDULED', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DISABLED', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=421,
  serialized_end=497,
)
_sym_db.RegisterEnumDescriptor(_CAPABILITYCONFIG_STATUS)


_CAPABILITYCONFIGLIST = _descriptor.Descriptor(
  name='CapabilityConfigList',
  full_name='google.appengine.CapabilityConfigList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='google.appengine.CapabilityConfigList.config', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='default_config', full_name='google.appengine.CapabilityConfigList.default_config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=63,
  serialized_end=197,
)


_CAPABILITYCONFIG = _descriptor.Descriptor(
  name='CapabilityConfig',
  full_name='google.appengine.CapabilityConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='package', full_name='google.appengine.CapabilityConfig.package', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='capability', full_name='google.appengine.CapabilityConfig.capability', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.appengine.CapabilityConfig.status', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=4,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scheduled_time', full_name='google.appengine.CapabilityConfig.scheduled_time', index=3,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='internal_message', full_name='google.appengine.CapabilityConfig.internal_message', index=4,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='admin_message', full_name='google.appengine.CapabilityConfig.admin_message', index=5,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error_message', full_name='google.appengine.CapabilityConfig.error_message', index=6,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CAPABILITYCONFIG_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=200,
  serialized_end=497,
)

_CAPABILITYCONFIGLIST.fields_by_name['config'].message_type = _CAPABILITYCONFIG
_CAPABILITYCONFIGLIST.fields_by_name['default_config'].message_type = _CAPABILITYCONFIG
_CAPABILITYCONFIG.fields_by_name['status'].enum_type = _CAPABILITYCONFIG_STATUS
_CAPABILITYCONFIG_STATUS.containing_type = _CAPABILITYCONFIG
DESCRIPTOR.message_types_by_name['CapabilityConfigList'] = _CAPABILITYCONFIGLIST
DESCRIPTOR.message_types_by_name['CapabilityConfig'] = _CAPABILITYCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CapabilityConfigList = _reflection.GeneratedProtocolMessageType('CapabilityConfigList', (_message.Message,), {
  'DESCRIPTOR' : _CAPABILITYCONFIGLIST,
  '__module__' : 'google.appengine.base.capabilities_pb2'

  })
_sym_db.RegisterMessage(CapabilityConfigList)

CapabilityConfig = _reflection.GeneratedProtocolMessageType('CapabilityConfig', (_message.Message,), {
  'DESCRIPTOR' : _CAPABILITYCONFIG,
  '__module__' : 'google.appengine.base.capabilities_pb2'

  })
_sym_db.RegisterMessage(CapabilityConfig)


DESCRIPTOR._options = None

