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
  name='google/appengine/api/mail_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n\035com.google.appengine.api.mailB\rMailServicePb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\'google/appengine/api/mail_service.proto\x12\x10google.appengine\"\xb4\x01\n\x10MailServiceError\"\x9f\x01\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x12\n\x0eINTERNAL_ERROR\x10\x01\x12\x0f\n\x0b\x42\x41\x44_REQUEST\x10\x02\x12\x17\n\x13UNAUTHORIZED_SENDER\x10\x03\x12\x1b\n\x17INVALID_ATTACHMENT_TYPE\x10\x04\x12\x17\n\x13INVALID_HEADER_NAME\x10\x05\x12\x16\n\x12INVALID_CONTENT_ID\x10\x06\"i\n\x0eMailAttachment\x12\x10\n\x08\x46ileName\x18\x01 \x02(\t\x12\x0c\n\x04\x44\x61ta\x18\x02 \x02(\x0c\x12\x11\n\tContentID\x18\x03 \x01(\t\x12$\n\x18\x44\x45PRECATED_ContentID_set\x18\r \x01(\x08\x42\x02\x18\x01\")\n\nMailHeader\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\t\"\x81\x02\n\x0bMailMessage\x12\x0e\n\x06Sender\x18\x01 \x02(\t\x12\x0f\n\x07ReplyTo\x18\x02 \x01(\t\x12\n\n\x02To\x18\x03 \x03(\t\x12\n\n\x02\x43\x63\x18\x04 \x03(\t\x12\x0b\n\x03\x42\x63\x63\x18\x05 \x03(\t\x12\x0f\n\x07Subject\x18\x06 \x02(\t\x12\x10\n\x08TextBody\x18\x07 \x01(\t\x12\x10\n\x08HtmlBody\x18\x08 \x01(\t\x12\x13\n\x0b\x41mpHtmlBody\x18\x0b \x01(\t\x12\x34\n\nAttachment\x18\t \x03(\x0b\x32 .google.appengine.MailAttachment\x12,\n\x06Header\x18\n \x03(\x0b\x32\x1c.google.appengine.MailHeaderB.\n\x1d\x63om.google.appengine.api.mailB\rMailServicePb'
)



_MAILSERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.MailServiceError.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INTERNAL_ERROR', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BAD_REQUEST', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNAUTHORIZED_SENDER', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_ATTACHMENT_TYPE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_HEADER_NAME', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_CONTENT_ID', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=83,
  serialized_end=242,
)
_sym_db.RegisterEnumDescriptor(_MAILSERVICEERROR_ERRORCODE)


_MAILSERVICEERROR = _descriptor.Descriptor(
  name='MailServiceError',
  full_name='google.appengine.MailServiceError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MAILSERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=242,
)


_MAILATTACHMENT = _descriptor.Descriptor(
  name='MailAttachment',
  full_name='google.appengine.MailAttachment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='FileName', full_name='google.appengine.MailAttachment.FileName', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Data', full_name='google.appengine.MailAttachment.Data', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ContentID', full_name='google.appengine.MailAttachment.ContentID', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='DEPRECATED_ContentID_set', full_name='google.appengine.MailAttachment.DEPRECATED_ContentID_set', index=3,
      number=13, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=244,
  serialized_end=349,
)


_MAILHEADER = _descriptor.Descriptor(
  name='MailHeader',
  full_name='google.appengine.MailHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='google.appengine.MailHeader.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='google.appengine.MailHeader.value', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=351,
  serialized_end=392,
)


_MAILMESSAGE = _descriptor.Descriptor(
  name='MailMessage',
  full_name='google.appengine.MailMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Sender', full_name='google.appengine.MailMessage.Sender', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ReplyTo', full_name='google.appengine.MailMessage.ReplyTo', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='To', full_name='google.appengine.MailMessage.To', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Cc', full_name='google.appengine.MailMessage.Cc', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Bcc', full_name='google.appengine.MailMessage.Bcc', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Subject', full_name='google.appengine.MailMessage.Subject', index=5,
      number=6, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='TextBody', full_name='google.appengine.MailMessage.TextBody', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='HtmlBody', full_name='google.appengine.MailMessage.HtmlBody', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='AmpHtmlBody', full_name='google.appengine.MailMessage.AmpHtmlBody', index=8,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Attachment', full_name='google.appengine.MailMessage.Attachment', index=9,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Header', full_name='google.appengine.MailMessage.Header', index=10,
      number=10, type=11, cpp_type=10, label=3,
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
  serialized_start=395,
  serialized_end=652,
)

_MAILSERVICEERROR_ERRORCODE.containing_type = _MAILSERVICEERROR
_MAILMESSAGE.fields_by_name['Attachment'].message_type = _MAILATTACHMENT
_MAILMESSAGE.fields_by_name['Header'].message_type = _MAILHEADER
DESCRIPTOR.message_types_by_name['MailServiceError'] = _MAILSERVICEERROR
DESCRIPTOR.message_types_by_name['MailAttachment'] = _MAILATTACHMENT
DESCRIPTOR.message_types_by_name['MailHeader'] = _MAILHEADER
DESCRIPTOR.message_types_by_name['MailMessage'] = _MAILMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MailServiceError = _reflection.GeneratedProtocolMessageType('MailServiceError', (_message.Message,), {
  'DESCRIPTOR' : _MAILSERVICEERROR,
  '__module__' : 'google.appengine.api.mail_service_pb2'

  })
_sym_db.RegisterMessage(MailServiceError)

MailAttachment = _reflection.GeneratedProtocolMessageType('MailAttachment', (_message.Message,), {
  'DESCRIPTOR' : _MAILATTACHMENT,
  '__module__' : 'google.appengine.api.mail_service_pb2'

  })
_sym_db.RegisterMessage(MailAttachment)

MailHeader = _reflection.GeneratedProtocolMessageType('MailHeader', (_message.Message,), {
  'DESCRIPTOR' : _MAILHEADER,
  '__module__' : 'google.appengine.api.mail_service_pb2'

  })
_sym_db.RegisterMessage(MailHeader)

MailMessage = _reflection.GeneratedProtocolMessageType('MailMessage', (_message.Message,), {
  'DESCRIPTOR' : _MAILMESSAGE,
  '__module__' : 'google.appengine.api.mail_service_pb2'

  })
_sym_db.RegisterMessage(MailMessage)


DESCRIPTOR._options = None
_MAILATTACHMENT.fields_by_name['DEPRECATED_ContentID_set']._options = None

