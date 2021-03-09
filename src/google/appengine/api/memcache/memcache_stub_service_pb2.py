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


from google.appengine.api import api_base_pb2 as google_dot_appengine_dot_api_dot_api__base__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/api/memcache/memcache_stub_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n!com.google.appengine.api.memcacheB\025MemcacheStubServicePb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n9google/appengine/api/memcache/memcache_stub_service.proto\x12\x10google.appengine\x1a#google/appengine/api/api_base.proto\"+\n\x11SetMaxSizeRequest\x12\x16\n\x0emax_size_bytes\x18\x01 \x02(\x03\"1\n\x19GetLruChainLengthResponse\x12\x14\n\x0c\x63hain_length\x18\x01 \x02(\x03\"2\n\x0fSetClockRequest\x12\x1f\n\x17\x63lock_time_milliseconds\x18\x01 \x02(\x03\"+\n\x13\x41\x64vanceClockRequest\x12\x14\n\x0cmilliseconds\x18\x01 \x02(\x03\"7\n\x14\x41\x64vanceClockResponse\x12\x1f\n\x17\x63lock_time_milliseconds\x18\x01 \x02(\x03\x42:\n!com.google.appengine.api.memcacheB\x15MemcacheStubServicePb'
  ,
  dependencies=[google_dot_appengine_dot_api_dot_api__base__pb2.DESCRIPTOR,])




_SETMAXSIZEREQUEST = _descriptor.Descriptor(
  name='SetMaxSizeRequest',
  full_name='google.appengine.SetMaxSizeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='max_size_bytes', full_name='google.appengine.SetMaxSizeRequest.max_size_bytes', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=116,
  serialized_end=159,
)


_GETLRUCHAINLENGTHRESPONSE = _descriptor.Descriptor(
  name='GetLruChainLengthResponse',
  full_name='google.appengine.GetLruChainLengthResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='chain_length', full_name='google.appengine.GetLruChainLengthResponse.chain_length', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=161,
  serialized_end=210,
)


_SETCLOCKREQUEST = _descriptor.Descriptor(
  name='SetClockRequest',
  full_name='google.appengine.SetClockRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clock_time_milliseconds', full_name='google.appengine.SetClockRequest.clock_time_milliseconds', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=212,
  serialized_end=262,
)


_ADVANCECLOCKREQUEST = _descriptor.Descriptor(
  name='AdvanceClockRequest',
  full_name='google.appengine.AdvanceClockRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='milliseconds', full_name='google.appengine.AdvanceClockRequest.milliseconds', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=264,
  serialized_end=307,
)


_ADVANCECLOCKRESPONSE = _descriptor.Descriptor(
  name='AdvanceClockResponse',
  full_name='google.appengine.AdvanceClockResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clock_time_milliseconds', full_name='google.appengine.AdvanceClockResponse.clock_time_milliseconds', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=309,
  serialized_end=364,
)

DESCRIPTOR.message_types_by_name['SetMaxSizeRequest'] = _SETMAXSIZEREQUEST
DESCRIPTOR.message_types_by_name['GetLruChainLengthResponse'] = _GETLRUCHAINLENGTHRESPONSE
DESCRIPTOR.message_types_by_name['SetClockRequest'] = _SETCLOCKREQUEST
DESCRIPTOR.message_types_by_name['AdvanceClockRequest'] = _ADVANCECLOCKREQUEST
DESCRIPTOR.message_types_by_name['AdvanceClockResponse'] = _ADVANCECLOCKRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SetMaxSizeRequest = _reflection.GeneratedProtocolMessageType('SetMaxSizeRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETMAXSIZEREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(SetMaxSizeRequest)

GetLruChainLengthResponse = _reflection.GeneratedProtocolMessageType('GetLruChainLengthResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETLRUCHAINLENGTHRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(GetLruChainLengthResponse)

SetClockRequest = _reflection.GeneratedProtocolMessageType('SetClockRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETCLOCKREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(SetClockRequest)

AdvanceClockRequest = _reflection.GeneratedProtocolMessageType('AdvanceClockRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADVANCECLOCKREQUEST,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(AdvanceClockRequest)

AdvanceClockResponse = _reflection.GeneratedProtocolMessageType('AdvanceClockResponse', (_message.Message,), {
  'DESCRIPTOR' : _ADVANCECLOCKRESPONSE,
  '__module__' : 'google.appengine.api.memcache.memcache_stub_service_pb2'

  })
_sym_db.RegisterMessage(AdvanceClockResponse)


DESCRIPTOR._options = None

