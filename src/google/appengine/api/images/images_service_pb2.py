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
  name='google/appengine/api/images/images_service.proto',
  package='google.appengine',
  syntax='proto2',
  serialized_options=b'\n\037com.google.appengine.api.imagesB\017ImagesServicePb\210\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n0google/appengine/api/images/images_service.proto\x12\x10google.appengine\"\xc8\x01\n\x12ImagesServiceError\"\xb1\x01\n\tErrorCode\x12\x15\n\x11UNSPECIFIED_ERROR\x10\x01\x12\x16\n\x12\x42\x41\x44_TRANSFORM_DATA\x10\x02\x12\r\n\tNOT_IMAGE\x10\x03\x12\x12\n\x0e\x42\x41\x44_IMAGE_DATA\x10\x04\x12\x13\n\x0fIMAGE_TOO_LARGE\x10\x05\x12\x14\n\x10INVALID_BLOB_KEY\x10\x06\x12\x11\n\rACCESS_DENIED\x10\x07\x12\x14\n\x10OBJECT_NOT_FOUND\x10\x08\"\x80\x01\n\x16ImagesServiceTransform\"f\n\x04Type\x12\n\n\x06RESIZE\x10\x01\x12\n\n\x06ROTATE\x10\x02\x12\x13\n\x0fHORIZONTAL_FLIP\x10\x03\x12\x11\n\rVERTICAL_FLIP\x10\x04\x12\x08\n\x04\x43ROP\x10\x05\x12\x14\n\x10IM_FEELING_LUCKY\x10\x06\"\x92\x04\n\tTransform\x12\r\n\x05width\x18\x01 \x01(\x05\x12\x0e\n\x06height\x18\x02 \x01(\x05\x12\x13\n\x0b\x63rop_to_fit\x18\x0b \x01(\x08\x12\x1a\n\rcrop_offset_x\x18\x0c \x01(\x02:\x03\x30.5\x12\x1a\n\rcrop_offset_y\x18\r \x01(\x02:\x03\x30.5\x12\x0e\n\x06rotate\x18\x03 \x01(\x05\x12\x17\n\x0fhorizontal_flip\x18\x04 \x01(\x08\x12\x15\n\rvertical_flip\x18\x05 \x01(\x08\x12\x13\n\x0b\x63rop_left_x\x18\x06 \x01(\x02\x12\x12\n\ncrop_top_y\x18\x07 \x01(\x02\x12\x17\n\x0c\x63rop_right_x\x18\x08 \x01(\x02:\x01\x31\x12\x18\n\rcrop_bottom_y\x18\t \x01(\x02:\x01\x31\x12\x12\n\nautolevels\x18\n \x01(\x08\x12\x15\n\rallow_stretch\x18\x0e \x01(\x08\x12\x1c\n\x14\x64\x65precated_width_set\x18\x65 \x01(\x08\x12\x1d\n\x15\x64\x65precated_height_set\x18\x66 \x01(\x08\x12$\n\x1c\x64\x65precated_crop_offset_x_set\x18p \x01(\x08\x12$\n\x1c\x64\x65precated_crop_offset_y_set\x18q \x01(\x08\x12#\n\x1b\x64\x65precated_crop_right_x_set\x18l \x01(\x08\x12$\n\x1c\x64\x65precated_crop_bottom_y_set\x18m \x01(\x08\"r\n\tImageData\x12\x13\n\x07\x63ontent\x18\x01 \x02(\x0c\x42\x02\x08\x01\x12\x10\n\x08\x62lob_key\x18\x02 \x01(\t\x12\r\n\x05width\x18\x03 \x01(\x05\x12\x0e\n\x06height\x18\x04 \x01(\x05\x12\x1f\n\x17\x64\x65precated_blob_key_set\x18\x66 \x01(\x08\"\xe5\x02\n\rInputSettings\x12]\n\x18\x63orrect_exif_orientation\x18\x01 \x01(\x0e\x32;.google.appengine.InputSettings.ORIENTATION_CORRECTION_TYPE\x12\x16\n\x0eparse_metadata\x18\x02 \x01(\x08\x12$\n\x1ctransparent_substitution_rgb\x18\x03 \x01(\x05\x12/\n\'deprecated_correct_exif_orientation_set\x18\x65 \x01(\x08\x12\x33\n+deprecated_transparent_substitution_rgb_set\x18g \x01(\x08\"Q\n\x1bORIENTATION_CORRECTION_TYPE\x12\x19\n\x15UNCHANGED_ORIENTATION\x10\x00\x12\x17\n\x13\x43ORRECT_ORIENTATION\x10\x01\"\x8a\x01\n\x0eOutputSettings\x12=\n\tmime_type\x18\x01 \x01(\x0e\x32*.google.appengine.OutputSettings.MIME_TYPE\x12\x0f\n\x07quality\x18\x02 \x01(\x05\"(\n\tMIME_TYPE\x12\x07\n\x03PNG\x10\x00\x12\x08\n\x04JPEG\x10\x01\x12\x08\n\x04WEBP\x10\x02\"\xd6\x01\n\x16ImagesTransformRequest\x12*\n\x05image\x18\x01 \x02(\x0b\x32\x1b.google.appengine.ImageData\x12.\n\ttransform\x18\x02 \x03(\x0b\x32\x1b.google.appengine.Transform\x12\x30\n\x06output\x18\x03 \x02(\x0b\x32 .google.appengine.OutputSettings\x12.\n\x05input\x18\x04 \x01(\x0b\x32\x1f.google.appengine.InputSettings\"^\n\x17ImagesTransformResponse\x12*\n\x05image\x18\x01 \x02(\x0b\x32\x1b.google.appengine.ImageData\x12\x17\n\x0fsource_metadata\x18\x02 \x01(\t\"\xa2\x02\n\x15\x43ompositeImageOptions\x12\x14\n\x0csource_index\x18\x01 \x02(\x05\x12\x10\n\x08x_offset\x18\x02 \x02(\x05\x12\x10\n\x08y_offset\x18\x03 \x02(\x05\x12\x0f\n\x07opacity\x18\x04 \x02(\x02\x12>\n\x06\x61nchor\x18\x05 \x02(\x0e\x32..google.appengine.CompositeImageOptions.ANCHOR\"~\n\x06\x41NCHOR\x12\x0c\n\x08TOP_LEFT\x10\x00\x12\x07\n\x03TOP\x10\x01\x12\r\n\tTOP_RIGHT\x10\x02\x12\x08\n\x04LEFT\x10\x03\x12\n\n\x06\x43\x45NTER\x10\x04\x12\t\n\x05RIGHT\x10\x05\x12\x0f\n\x0b\x42OTTOM_LEFT\x10\x06\x12\n\n\x06\x42OTTOM\x10\x07\x12\x10\n\x0c\x42OTTOM_RIGHT\x10\x08\"\x90\x01\n\x0cImagesCanvas\x12\r\n\x05width\x18\x01 \x02(\x05\x12\x0e\n\x06height\x18\x02 \x02(\x05\x12\x30\n\x06output\x18\x03 \x02(\x0b\x32 .google.appengine.OutputSettings\x12\x11\n\x05\x63olor\x18\x04 \x01(\x05:\x02-1\x12\x1c\n\x14\x64\x65precated_color_set\x18h \x01(\x08\"\xae\x01\n\x16ImagesCompositeRequest\x12*\n\x05image\x18\x01 \x03(\x0b\x32\x1b.google.appengine.ImageData\x12\x38\n\x07options\x18\x02 \x03(\x0b\x32\'.google.appengine.CompositeImageOptions\x12.\n\x06\x63\x61nvas\x18\x03 \x02(\x0b\x32\x1e.google.appengine.ImagesCanvas\"E\n\x17ImagesCompositeResponse\x12*\n\x05image\x18\x01 \x02(\x0b\x32\x1b.google.appengine.ImageData\"D\n\x16ImagesHistogramRequest\x12*\n\x05image\x18\x01 \x02(\x0b\x32\x1b.google.appengine.ImageData\";\n\x0fImagesHistogram\x12\x0b\n\x03red\x18\x01 \x03(\x05\x12\r\n\x05green\x18\x02 \x03(\x05\x12\x0c\n\x04\x62lue\x18\x03 \x03(\x05\"O\n\x17ImagesHistogramResponse\x12\x34\n\thistogram\x18\x01 \x02(\x0b\x32!.google.appengine.ImagesHistogram\"F\n\x17ImagesGetUrlBaseRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\t\x12\x19\n\x11\x63reate_secure_url\x18\x02 \x01(\x08\"\'\n\x18ImagesGetUrlBaseResponse\x12\x0b\n\x03url\x18\x01 \x02(\t\".\n\x1aImagesDeleteUrlBaseRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\t\"\x1d\n\x1bImagesDeleteUrlBaseResponseB5\n\x1f\x63om.google.appengine.api.imagesB\x0fImagesServicePb\x88\x01\x01'
)



_IMAGESSERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='google.appengine.ImagesServiceError.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED_ERROR', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BAD_TRANSFORM_DATA', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NOT_IMAGE', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BAD_IMAGE_DATA', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='IMAGE_TOO_LARGE', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_BLOB_KEY', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ACCESS_DENIED', index=6, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OBJECT_NOT_FOUND', index=7, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=94,
  serialized_end=271,
)
_sym_db.RegisterEnumDescriptor(_IMAGESSERVICEERROR_ERRORCODE)

_IMAGESSERVICETRANSFORM_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='google.appengine.ImagesServiceTransform.Type',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RESIZE', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ROTATE', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HORIZONTAL_FLIP', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='VERTICAL_FLIP', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CROP', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='IM_FEELING_LUCKY', index=5, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=300,
  serialized_end=402,
)
_sym_db.RegisterEnumDescriptor(_IMAGESSERVICETRANSFORM_TYPE)

_INPUTSETTINGS_ORIENTATION_CORRECTION_TYPE = _descriptor.EnumDescriptor(
  name='ORIENTATION_CORRECTION_TYPE',
  full_name='google.appengine.InputSettings.ORIENTATION_CORRECTION_TYPE',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNCHANGED_ORIENTATION', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CORRECT_ORIENTATION', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1330,
  serialized_end=1411,
)
_sym_db.RegisterEnumDescriptor(_INPUTSETTINGS_ORIENTATION_CORRECTION_TYPE)

_OUTPUTSETTINGS_MIME_TYPE = _descriptor.EnumDescriptor(
  name='MIME_TYPE',
  full_name='google.appengine.OutputSettings.MIME_TYPE',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PNG', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='JPEG', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WEBP', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1512,
  serialized_end=1552,
)
_sym_db.RegisterEnumDescriptor(_OUTPUTSETTINGS_MIME_TYPE)

_COMPOSITEIMAGEOPTIONS_ANCHOR = _descriptor.EnumDescriptor(
  name='ANCHOR',
  full_name='google.appengine.CompositeImageOptions.ANCHOR',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TOP_LEFT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TOP', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TOP_RIGHT', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LEFT', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CENTER', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RIGHT', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BOTTOM_LEFT', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BOTTOM', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BOTTOM_RIGHT', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2032,
  serialized_end=2158,
)
_sym_db.RegisterEnumDescriptor(_COMPOSITEIMAGEOPTIONS_ANCHOR)


_IMAGESSERVICEERROR = _descriptor.Descriptor(
  name='ImagesServiceError',
  full_name='google.appengine.ImagesServiceError',
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
    _IMAGESSERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=71,
  serialized_end=271,
)


_IMAGESSERVICETRANSFORM = _descriptor.Descriptor(
  name='ImagesServiceTransform',
  full_name='google.appengine.ImagesServiceTransform',
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
    _IMAGESSERVICETRANSFORM_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=274,
  serialized_end=402,
)


_TRANSFORM = _descriptor.Descriptor(
  name='Transform',
  full_name='google.appengine.Transform',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='width', full_name='google.appengine.Transform.width', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='google.appengine.Transform.height', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crop_to_fit', full_name='google.appengine.Transform.crop_to_fit', index=2,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crop_offset_x', full_name='google.appengine.Transform.crop_offset_x', index=3,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crop_offset_y', full_name='google.appengine.Transform.crop_offset_y', index=4,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rotate', full_name='google.appengine.Transform.rotate', index=5,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='horizontal_flip', full_name='google.appengine.Transform.horizontal_flip', index=6,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vertical_flip', full_name='google.appengine.Transform.vertical_flip', index=7,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crop_left_x', full_name='google.appengine.Transform.crop_left_x', index=8,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crop_top_y', full_name='google.appengine.Transform.crop_top_y', index=9,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crop_right_x', full_name='google.appengine.Transform.crop_right_x', index=10,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crop_bottom_y', full_name='google.appengine.Transform.crop_bottom_y', index=11,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='autolevels', full_name='google.appengine.Transform.autolevels', index=12,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='allow_stretch', full_name='google.appengine.Transform.allow_stretch', index=13,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_width_set', full_name='google.appengine.Transform.deprecated_width_set', index=14,
      number=101, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_height_set', full_name='google.appengine.Transform.deprecated_height_set', index=15,
      number=102, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_crop_offset_x_set', full_name='google.appengine.Transform.deprecated_crop_offset_x_set', index=16,
      number=112, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_crop_offset_y_set', full_name='google.appengine.Transform.deprecated_crop_offset_y_set', index=17,
      number=113, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_crop_right_x_set', full_name='google.appengine.Transform.deprecated_crop_right_x_set', index=18,
      number=108, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_crop_bottom_y_set', full_name='google.appengine.Transform.deprecated_crop_bottom_y_set', index=19,
      number=109, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=405,
  serialized_end=935,
)


_IMAGEDATA = _descriptor.Descriptor(
  name='ImageData',
  full_name='google.appengine.ImageData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='content', full_name='google.appengine.ImageData.content', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='google.appengine.ImageData.blob_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='width', full_name='google.appengine.ImageData.width', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='google.appengine.ImageData.height', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_blob_key_set', full_name='google.appengine.ImageData.deprecated_blob_key_set', index=4,
      number=102, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=937,
  serialized_end=1051,
)


_INPUTSETTINGS = _descriptor.Descriptor(
  name='InputSettings',
  full_name='google.appengine.InputSettings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='correct_exif_orientation', full_name='google.appengine.InputSettings.correct_exif_orientation', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parse_metadata', full_name='google.appengine.InputSettings.parse_metadata', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transparent_substitution_rgb', full_name='google.appengine.InputSettings.transparent_substitution_rgb', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_correct_exif_orientation_set', full_name='google.appengine.InputSettings.deprecated_correct_exif_orientation_set', index=3,
      number=101, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_transparent_substitution_rgb_set', full_name='google.appengine.InputSettings.deprecated_transparent_substitution_rgb_set', index=4,
      number=103, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _INPUTSETTINGS_ORIENTATION_CORRECTION_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1054,
  serialized_end=1411,
)


_OUTPUTSETTINGS = _descriptor.Descriptor(
  name='OutputSettings',
  full_name='google.appengine.OutputSettings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mime_type', full_name='google.appengine.OutputSettings.mime_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='quality', full_name='google.appengine.OutputSettings.quality', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _OUTPUTSETTINGS_MIME_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1414,
  serialized_end=1552,
)


_IMAGESTRANSFORMREQUEST = _descriptor.Descriptor(
  name='ImagesTransformRequest',
  full_name='google.appengine.ImagesTransformRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='google.appengine.ImagesTransformRequest.image', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transform', full_name='google.appengine.ImagesTransformRequest.transform', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='output', full_name='google.appengine.ImagesTransformRequest.output', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='input', full_name='google.appengine.ImagesTransformRequest.input', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=1555,
  serialized_end=1769,
)


_IMAGESTRANSFORMRESPONSE = _descriptor.Descriptor(
  name='ImagesTransformResponse',
  full_name='google.appengine.ImagesTransformResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='google.appengine.ImagesTransformResponse.image', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source_metadata', full_name='google.appengine.ImagesTransformResponse.source_metadata', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=1771,
  serialized_end=1865,
)


_COMPOSITEIMAGEOPTIONS = _descriptor.Descriptor(
  name='CompositeImageOptions',
  full_name='google.appengine.CompositeImageOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='source_index', full_name='google.appengine.CompositeImageOptions.source_index', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='x_offset', full_name='google.appengine.CompositeImageOptions.x_offset', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y_offset', full_name='google.appengine.CompositeImageOptions.y_offset', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='opacity', full_name='google.appengine.CompositeImageOptions.opacity', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='anchor', full_name='google.appengine.CompositeImageOptions.anchor', index=4,
      number=5, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _COMPOSITEIMAGEOPTIONS_ANCHOR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1868,
  serialized_end=2158,
)


_IMAGESCANVAS = _descriptor.Descriptor(
  name='ImagesCanvas',
  full_name='google.appengine.ImagesCanvas',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='width', full_name='google.appengine.ImagesCanvas.width', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='google.appengine.ImagesCanvas.height', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='output', full_name='google.appengine.ImagesCanvas.output', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='color', full_name='google.appengine.ImagesCanvas.color', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=-1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deprecated_color_set', full_name='google.appengine.ImagesCanvas.deprecated_color_set', index=4,
      number=104, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=2161,
  serialized_end=2305,
)


_IMAGESCOMPOSITEREQUEST = _descriptor.Descriptor(
  name='ImagesCompositeRequest',
  full_name='google.appengine.ImagesCompositeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='google.appengine.ImagesCompositeRequest.image', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='options', full_name='google.appengine.ImagesCompositeRequest.options', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='canvas', full_name='google.appengine.ImagesCompositeRequest.canvas', index=2,
      number=3, type=11, cpp_type=10, label=2,
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
  serialized_start=2308,
  serialized_end=2482,
)


_IMAGESCOMPOSITERESPONSE = _descriptor.Descriptor(
  name='ImagesCompositeResponse',
  full_name='google.appengine.ImagesCompositeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='google.appengine.ImagesCompositeResponse.image', index=0,
      number=1, type=11, cpp_type=10, label=2,
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
  serialized_start=2484,
  serialized_end=2553,
)


_IMAGESHISTOGRAMREQUEST = _descriptor.Descriptor(
  name='ImagesHistogramRequest',
  full_name='google.appengine.ImagesHistogramRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='google.appengine.ImagesHistogramRequest.image', index=0,
      number=1, type=11, cpp_type=10, label=2,
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
  serialized_start=2555,
  serialized_end=2623,
)


_IMAGESHISTOGRAM = _descriptor.Descriptor(
  name='ImagesHistogram',
  full_name='google.appengine.ImagesHistogram',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='red', full_name='google.appengine.ImagesHistogram.red', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='green', full_name='google.appengine.ImagesHistogram.green', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='blue', full_name='google.appengine.ImagesHistogram.blue', index=2,
      number=3, type=5, cpp_type=1, label=3,
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
  serialized_start=2625,
  serialized_end=2684,
)


_IMAGESHISTOGRAMRESPONSE = _descriptor.Descriptor(
  name='ImagesHistogramResponse',
  full_name='google.appengine.ImagesHistogramResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='histogram', full_name='google.appengine.ImagesHistogramResponse.histogram', index=0,
      number=1, type=11, cpp_type=10, label=2,
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
  serialized_start=2686,
  serialized_end=2765,
)


_IMAGESGETURLBASEREQUEST = _descriptor.Descriptor(
  name='ImagesGetUrlBaseRequest',
  full_name='google.appengine.ImagesGetUrlBaseRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='google.appengine.ImagesGetUrlBaseRequest.blob_key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='create_secure_url', full_name='google.appengine.ImagesGetUrlBaseRequest.create_secure_url', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=2767,
  serialized_end=2837,
)


_IMAGESGETURLBASERESPONSE = _descriptor.Descriptor(
  name='ImagesGetUrlBaseResponse',
  full_name='google.appengine.ImagesGetUrlBaseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='url', full_name='google.appengine.ImagesGetUrlBaseResponse.url', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  serialized_start=2839,
  serialized_end=2878,
)


_IMAGESDELETEURLBASEREQUEST = _descriptor.Descriptor(
  name='ImagesDeleteUrlBaseRequest',
  full_name='google.appengine.ImagesDeleteUrlBaseRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='google.appengine.ImagesDeleteUrlBaseRequest.blob_key', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  serialized_start=2880,
  serialized_end=2926,
)


_IMAGESDELETEURLBASERESPONSE = _descriptor.Descriptor(
  name='ImagesDeleteUrlBaseResponse',
  full_name='google.appengine.ImagesDeleteUrlBaseResponse',
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
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2928,
  serialized_end=2957,
)

_IMAGESSERVICEERROR_ERRORCODE.containing_type = _IMAGESSERVICEERROR
_IMAGESSERVICETRANSFORM_TYPE.containing_type = _IMAGESSERVICETRANSFORM
_INPUTSETTINGS.fields_by_name['correct_exif_orientation'].enum_type = _INPUTSETTINGS_ORIENTATION_CORRECTION_TYPE
_INPUTSETTINGS_ORIENTATION_CORRECTION_TYPE.containing_type = _INPUTSETTINGS
_OUTPUTSETTINGS.fields_by_name['mime_type'].enum_type = _OUTPUTSETTINGS_MIME_TYPE
_OUTPUTSETTINGS_MIME_TYPE.containing_type = _OUTPUTSETTINGS
_IMAGESTRANSFORMREQUEST.fields_by_name['image'].message_type = _IMAGEDATA
_IMAGESTRANSFORMREQUEST.fields_by_name['transform'].message_type = _TRANSFORM
_IMAGESTRANSFORMREQUEST.fields_by_name['output'].message_type = _OUTPUTSETTINGS
_IMAGESTRANSFORMREQUEST.fields_by_name['input'].message_type = _INPUTSETTINGS
_IMAGESTRANSFORMRESPONSE.fields_by_name['image'].message_type = _IMAGEDATA
_COMPOSITEIMAGEOPTIONS.fields_by_name['anchor'].enum_type = _COMPOSITEIMAGEOPTIONS_ANCHOR
_COMPOSITEIMAGEOPTIONS_ANCHOR.containing_type = _COMPOSITEIMAGEOPTIONS
_IMAGESCANVAS.fields_by_name['output'].message_type = _OUTPUTSETTINGS
_IMAGESCOMPOSITEREQUEST.fields_by_name['image'].message_type = _IMAGEDATA
_IMAGESCOMPOSITEREQUEST.fields_by_name['options'].message_type = _COMPOSITEIMAGEOPTIONS
_IMAGESCOMPOSITEREQUEST.fields_by_name['canvas'].message_type = _IMAGESCANVAS
_IMAGESCOMPOSITERESPONSE.fields_by_name['image'].message_type = _IMAGEDATA
_IMAGESHISTOGRAMREQUEST.fields_by_name['image'].message_type = _IMAGEDATA
_IMAGESHISTOGRAMRESPONSE.fields_by_name['histogram'].message_type = _IMAGESHISTOGRAM
DESCRIPTOR.message_types_by_name['ImagesServiceError'] = _IMAGESSERVICEERROR
DESCRIPTOR.message_types_by_name['ImagesServiceTransform'] = _IMAGESSERVICETRANSFORM
DESCRIPTOR.message_types_by_name['Transform'] = _TRANSFORM
DESCRIPTOR.message_types_by_name['ImageData'] = _IMAGEDATA
DESCRIPTOR.message_types_by_name['InputSettings'] = _INPUTSETTINGS
DESCRIPTOR.message_types_by_name['OutputSettings'] = _OUTPUTSETTINGS
DESCRIPTOR.message_types_by_name['ImagesTransformRequest'] = _IMAGESTRANSFORMREQUEST
DESCRIPTOR.message_types_by_name['ImagesTransformResponse'] = _IMAGESTRANSFORMRESPONSE
DESCRIPTOR.message_types_by_name['CompositeImageOptions'] = _COMPOSITEIMAGEOPTIONS
DESCRIPTOR.message_types_by_name['ImagesCanvas'] = _IMAGESCANVAS
DESCRIPTOR.message_types_by_name['ImagesCompositeRequest'] = _IMAGESCOMPOSITEREQUEST
DESCRIPTOR.message_types_by_name['ImagesCompositeResponse'] = _IMAGESCOMPOSITERESPONSE
DESCRIPTOR.message_types_by_name['ImagesHistogramRequest'] = _IMAGESHISTOGRAMREQUEST
DESCRIPTOR.message_types_by_name['ImagesHistogram'] = _IMAGESHISTOGRAM
DESCRIPTOR.message_types_by_name['ImagesHistogramResponse'] = _IMAGESHISTOGRAMRESPONSE
DESCRIPTOR.message_types_by_name['ImagesGetUrlBaseRequest'] = _IMAGESGETURLBASEREQUEST
DESCRIPTOR.message_types_by_name['ImagesGetUrlBaseResponse'] = _IMAGESGETURLBASERESPONSE
DESCRIPTOR.message_types_by_name['ImagesDeleteUrlBaseRequest'] = _IMAGESDELETEURLBASEREQUEST
DESCRIPTOR.message_types_by_name['ImagesDeleteUrlBaseResponse'] = _IMAGESDELETEURLBASERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ImagesServiceError = _reflection.GeneratedProtocolMessageType('ImagesServiceError', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESSERVICEERROR,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesServiceError)

ImagesServiceTransform = _reflection.GeneratedProtocolMessageType('ImagesServiceTransform', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESSERVICETRANSFORM,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesServiceTransform)

Transform = _reflection.GeneratedProtocolMessageType('Transform', (_message.Message,), {
  'DESCRIPTOR' : _TRANSFORM,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(Transform)

ImageData = _reflection.GeneratedProtocolMessageType('ImageData', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEDATA,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImageData)

InputSettings = _reflection.GeneratedProtocolMessageType('InputSettings', (_message.Message,), {
  'DESCRIPTOR' : _INPUTSETTINGS,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(InputSettings)

OutputSettings = _reflection.GeneratedProtocolMessageType('OutputSettings', (_message.Message,), {
  'DESCRIPTOR' : _OUTPUTSETTINGS,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(OutputSettings)

ImagesTransformRequest = _reflection.GeneratedProtocolMessageType('ImagesTransformRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESTRANSFORMREQUEST,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesTransformRequest)

ImagesTransformResponse = _reflection.GeneratedProtocolMessageType('ImagesTransformResponse', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESTRANSFORMRESPONSE,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesTransformResponse)

CompositeImageOptions = _reflection.GeneratedProtocolMessageType('CompositeImageOptions', (_message.Message,), {
  'DESCRIPTOR' : _COMPOSITEIMAGEOPTIONS,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(CompositeImageOptions)

ImagesCanvas = _reflection.GeneratedProtocolMessageType('ImagesCanvas', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESCANVAS,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesCanvas)

ImagesCompositeRequest = _reflection.GeneratedProtocolMessageType('ImagesCompositeRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESCOMPOSITEREQUEST,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesCompositeRequest)

ImagesCompositeResponse = _reflection.GeneratedProtocolMessageType('ImagesCompositeResponse', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESCOMPOSITERESPONSE,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesCompositeResponse)

ImagesHistogramRequest = _reflection.GeneratedProtocolMessageType('ImagesHistogramRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESHISTOGRAMREQUEST,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesHistogramRequest)

ImagesHistogram = _reflection.GeneratedProtocolMessageType('ImagesHistogram', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESHISTOGRAM,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesHistogram)

ImagesHistogramResponse = _reflection.GeneratedProtocolMessageType('ImagesHistogramResponse', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESHISTOGRAMRESPONSE,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesHistogramResponse)

ImagesGetUrlBaseRequest = _reflection.GeneratedProtocolMessageType('ImagesGetUrlBaseRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESGETURLBASEREQUEST,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesGetUrlBaseRequest)

ImagesGetUrlBaseResponse = _reflection.GeneratedProtocolMessageType('ImagesGetUrlBaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESGETURLBASERESPONSE,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesGetUrlBaseResponse)

ImagesDeleteUrlBaseRequest = _reflection.GeneratedProtocolMessageType('ImagesDeleteUrlBaseRequest', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESDELETEURLBASEREQUEST,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesDeleteUrlBaseRequest)

ImagesDeleteUrlBaseResponse = _reflection.GeneratedProtocolMessageType('ImagesDeleteUrlBaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _IMAGESDELETEURLBASERESPONSE,
  '__module__' : 'google.appengine.api.images.images_service_pb2'

  })
_sym_db.RegisterMessage(ImagesDeleteUrlBaseResponse)


DESCRIPTOR._options = None
_IMAGEDATA.fields_by_name['content']._options = None

