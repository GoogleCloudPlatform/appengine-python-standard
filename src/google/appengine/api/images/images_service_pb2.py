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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0google/appengine/api/images/images_service.proto\x12\x10google.appengine\"\xc8\x01\n\x12ImagesServiceError\"\xb1\x01\n\tErrorCode\x12\x15\n\x11UNSPECIFIED_ERROR\x10\x01\x12\x16\n\x12\x42\x41\x44_TRANSFORM_DATA\x10\x02\x12\r\n\tNOT_IMAGE\x10\x03\x12\x12\n\x0e\x42\x41\x44_IMAGE_DATA\x10\x04\x12\x13\n\x0fIMAGE_TOO_LARGE\x10\x05\x12\x14\n\x10INVALID_BLOB_KEY\x10\x06\x12\x11\n\rACCESS_DENIED\x10\x07\x12\x14\n\x10OBJECT_NOT_FOUND\x10\x08\"\x80\x01\n\x16ImagesServiceTransform\"f\n\x04Type\x12\n\n\x06RESIZE\x10\x01\x12\n\n\x06ROTATE\x10\x02\x12\x13\n\x0fHORIZONTAL_FLIP\x10\x03\x12\x11\n\rVERTICAL_FLIP\x10\x04\x12\x08\n\x04\x43ROP\x10\x05\x12\x14\n\x10IM_FEELING_LUCKY\x10\x06\"\x92\x04\n\tTransform\x12\r\n\x05width\x18\x01 \x01(\x05\x12\x0e\n\x06height\x18\x02 \x01(\x05\x12\x13\n\x0b\x63rop_to_fit\x18\x0b \x01(\x08\x12\x1a\n\rcrop_offset_x\x18\x0c \x01(\x02:\x03\x30.5\x12\x1a\n\rcrop_offset_y\x18\r \x01(\x02:\x03\x30.5\x12\x0e\n\x06rotate\x18\x03 \x01(\x05\x12\x17\n\x0fhorizontal_flip\x18\x04 \x01(\x08\x12\x15\n\rvertical_flip\x18\x05 \x01(\x08\x12\x13\n\x0b\x63rop_left_x\x18\x06 \x01(\x02\x12\x12\n\ncrop_top_y\x18\x07 \x01(\x02\x12\x17\n\x0c\x63rop_right_x\x18\x08 \x01(\x02:\x01\x31\x12\x18\n\rcrop_bottom_y\x18\t \x01(\x02:\x01\x31\x12\x12\n\nautolevels\x18\n \x01(\x08\x12\x15\n\rallow_stretch\x18\x0e \x01(\x08\x12\x1c\n\x14\x64\x65precated_width_set\x18\x65 \x01(\x08\x12\x1d\n\x15\x64\x65precated_height_set\x18\x66 \x01(\x08\x12$\n\x1c\x64\x65precated_crop_offset_x_set\x18p \x01(\x08\x12$\n\x1c\x64\x65precated_crop_offset_y_set\x18q \x01(\x08\x12#\n\x1b\x64\x65precated_crop_right_x_set\x18l \x01(\x08\x12$\n\x1c\x64\x65precated_crop_bottom_y_set\x18m \x01(\x08\"r\n\tImageData\x12\x13\n\x07\x63ontent\x18\x01 \x02(\x0c\x42\x02\x08\x01\x12\x10\n\x08\x62lob_key\x18\x02 \x01(\t\x12\r\n\x05width\x18\x03 \x01(\x05\x12\x0e\n\x06height\x18\x04 \x01(\x05\x12\x1f\n\x17\x64\x65precated_blob_key_set\x18\x66 \x01(\x08\"\xe5\x02\n\rInputSettings\x12]\n\x18\x63orrect_exif_orientation\x18\x01 \x01(\x0e\x32;.google.appengine.InputSettings.ORIENTATION_CORRECTION_TYPE\x12\x16\n\x0eparse_metadata\x18\x02 \x01(\x08\x12$\n\x1ctransparent_substitution_rgb\x18\x03 \x01(\x05\x12/\n\'deprecated_correct_exif_orientation_set\x18\x65 \x01(\x08\x12\x33\n+deprecated_transparent_substitution_rgb_set\x18g \x01(\x08\"Q\n\x1bORIENTATION_CORRECTION_TYPE\x12\x19\n\x15UNCHANGED_ORIENTATION\x10\x00\x12\x17\n\x13\x43ORRECT_ORIENTATION\x10\x01\"\x8a\x01\n\x0eOutputSettings\x12=\n\tmime_type\x18\x01 \x01(\x0e\x32*.google.appengine.OutputSettings.MIME_TYPE\x12\x0f\n\x07quality\x18\x02 \x01(\x05\"(\n\tMIME_TYPE\x12\x07\n\x03PNG\x10\x00\x12\x08\n\x04JPEG\x10\x01\x12\x08\n\x04WEBP\x10\x02\"\xd6\x01\n\x16ImagesTransformRequest\x12*\n\x05image\x18\x01 \x02(\x0b\x32\x1b.google.appengine.ImageData\x12.\n\ttransform\x18\x02 \x03(\x0b\x32\x1b.google.appengine.Transform\x12\x30\n\x06output\x18\x03 \x02(\x0b\x32 .google.appengine.OutputSettings\x12.\n\x05input\x18\x04 \x01(\x0b\x32\x1f.google.appengine.InputSettings\"^\n\x17ImagesTransformResponse\x12*\n\x05image\x18\x01 \x02(\x0b\x32\x1b.google.appengine.ImageData\x12\x17\n\x0fsource_metadata\x18\x02 \x01(\t\"\xa2\x02\n\x15\x43ompositeImageOptions\x12\x14\n\x0csource_index\x18\x01 \x02(\x05\x12\x10\n\x08x_offset\x18\x02 \x02(\x05\x12\x10\n\x08y_offset\x18\x03 \x02(\x05\x12\x0f\n\x07opacity\x18\x04 \x02(\x02\x12>\n\x06\x61nchor\x18\x05 \x02(\x0e\x32..google.appengine.CompositeImageOptions.ANCHOR\"~\n\x06\x41NCHOR\x12\x0c\n\x08TOP_LEFT\x10\x00\x12\x07\n\x03TOP\x10\x01\x12\r\n\tTOP_RIGHT\x10\x02\x12\x08\n\x04LEFT\x10\x03\x12\n\n\x06\x43\x45NTER\x10\x04\x12\t\n\x05RIGHT\x10\x05\x12\x0f\n\x0b\x42OTTOM_LEFT\x10\x06\x12\n\n\x06\x42OTTOM\x10\x07\x12\x10\n\x0c\x42OTTOM_RIGHT\x10\x08\"\x90\x01\n\x0cImagesCanvas\x12\r\n\x05width\x18\x01 \x02(\x05\x12\x0e\n\x06height\x18\x02 \x02(\x05\x12\x30\n\x06output\x18\x03 \x02(\x0b\x32 .google.appengine.OutputSettings\x12\x11\n\x05\x63olor\x18\x04 \x01(\x05:\x02-1\x12\x1c\n\x14\x64\x65precated_color_set\x18h \x01(\x08\"\xae\x01\n\x16ImagesCompositeRequest\x12*\n\x05image\x18\x01 \x03(\x0b\x32\x1b.google.appengine.ImageData\x12\x38\n\x07options\x18\x02 \x03(\x0b\x32\'.google.appengine.CompositeImageOptions\x12.\n\x06\x63\x61nvas\x18\x03 \x02(\x0b\x32\x1e.google.appengine.ImagesCanvas\"E\n\x17ImagesCompositeResponse\x12*\n\x05image\x18\x01 \x02(\x0b\x32\x1b.google.appengine.ImageData\"D\n\x16ImagesHistogramRequest\x12*\n\x05image\x18\x01 \x02(\x0b\x32\x1b.google.appengine.ImageData\";\n\x0fImagesHistogram\x12\x0b\n\x03red\x18\x01 \x03(\x05\x12\r\n\x05green\x18\x02 \x03(\x05\x12\x0c\n\x04\x62lue\x18\x03 \x03(\x05\"O\n\x17ImagesHistogramResponse\x12\x34\n\thistogram\x18\x01 \x02(\x0b\x32!.google.appengine.ImagesHistogram\"F\n\x17ImagesGetUrlBaseRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\t\x12\x19\n\x11\x63reate_secure_url\x18\x02 \x01(\x08\"\'\n\x18ImagesGetUrlBaseResponse\x12\x0b\n\x03url\x18\x01 \x02(\t\".\n\x1aImagesDeleteUrlBaseRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\t\"\x1d\n\x1bImagesDeleteUrlBaseResponseB5\n\x1f\x63om.google.appengine.api.imagesB\x0fImagesServicePb\x88\x01\x01')



_IMAGESSERVICEERROR = DESCRIPTOR.message_types_by_name['ImagesServiceError']
_IMAGESSERVICETRANSFORM = DESCRIPTOR.message_types_by_name['ImagesServiceTransform']
_TRANSFORM = DESCRIPTOR.message_types_by_name['Transform']
_IMAGEDATA = DESCRIPTOR.message_types_by_name['ImageData']
_INPUTSETTINGS = DESCRIPTOR.message_types_by_name['InputSettings']
_OUTPUTSETTINGS = DESCRIPTOR.message_types_by_name['OutputSettings']
_IMAGESTRANSFORMREQUEST = DESCRIPTOR.message_types_by_name['ImagesTransformRequest']
_IMAGESTRANSFORMRESPONSE = DESCRIPTOR.message_types_by_name['ImagesTransformResponse']
_COMPOSITEIMAGEOPTIONS = DESCRIPTOR.message_types_by_name['CompositeImageOptions']
_IMAGESCANVAS = DESCRIPTOR.message_types_by_name['ImagesCanvas']
_IMAGESCOMPOSITEREQUEST = DESCRIPTOR.message_types_by_name['ImagesCompositeRequest']
_IMAGESCOMPOSITERESPONSE = DESCRIPTOR.message_types_by_name['ImagesCompositeResponse']
_IMAGESHISTOGRAMREQUEST = DESCRIPTOR.message_types_by_name['ImagesHistogramRequest']
_IMAGESHISTOGRAM = DESCRIPTOR.message_types_by_name['ImagesHistogram']
_IMAGESHISTOGRAMRESPONSE = DESCRIPTOR.message_types_by_name['ImagesHistogramResponse']
_IMAGESGETURLBASEREQUEST = DESCRIPTOR.message_types_by_name['ImagesGetUrlBaseRequest']
_IMAGESGETURLBASERESPONSE = DESCRIPTOR.message_types_by_name['ImagesGetUrlBaseResponse']
_IMAGESDELETEURLBASEREQUEST = DESCRIPTOR.message_types_by_name['ImagesDeleteUrlBaseRequest']
_IMAGESDELETEURLBASERESPONSE = DESCRIPTOR.message_types_by_name['ImagesDeleteUrlBaseResponse']
_IMAGESSERVICEERROR_ERRORCODE = _IMAGESSERVICEERROR.enum_types_by_name['ErrorCode']
_IMAGESSERVICETRANSFORM_TYPE = _IMAGESSERVICETRANSFORM.enum_types_by_name['Type']
_INPUTSETTINGS_ORIENTATION_CORRECTION_TYPE = _INPUTSETTINGS.enum_types_by_name['ORIENTATION_CORRECTION_TYPE']
_OUTPUTSETTINGS_MIME_TYPE = _OUTPUTSETTINGS.enum_types_by_name['MIME_TYPE']
_COMPOSITEIMAGEOPTIONS_ANCHOR = _COMPOSITEIMAGEOPTIONS.enum_types_by_name['ANCHOR']
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

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\037com.google.appengine.api.imagesB\017ImagesServicePb\210\001\001'
  _IMAGEDATA.fields_by_name['content']._options = None
  _IMAGEDATA.fields_by_name['content']._serialized_options = b'\010\001'
  _IMAGESSERVICEERROR._serialized_start=71
  _IMAGESSERVICEERROR._serialized_end=271
  _IMAGESSERVICEERROR_ERRORCODE._serialized_start=94
  _IMAGESSERVICEERROR_ERRORCODE._serialized_end=271
  _IMAGESSERVICETRANSFORM._serialized_start=274
  _IMAGESSERVICETRANSFORM._serialized_end=402
  _IMAGESSERVICETRANSFORM_TYPE._serialized_start=300
  _IMAGESSERVICETRANSFORM_TYPE._serialized_end=402
  _TRANSFORM._serialized_start=405
  _TRANSFORM._serialized_end=935
  _IMAGEDATA._serialized_start=937
  _IMAGEDATA._serialized_end=1051
  _INPUTSETTINGS._serialized_start=1054
  _INPUTSETTINGS._serialized_end=1411
  _INPUTSETTINGS_ORIENTATION_CORRECTION_TYPE._serialized_start=1330
  _INPUTSETTINGS_ORIENTATION_CORRECTION_TYPE._serialized_end=1411
  _OUTPUTSETTINGS._serialized_start=1414
  _OUTPUTSETTINGS._serialized_end=1552
  _OUTPUTSETTINGS_MIME_TYPE._serialized_start=1512
  _OUTPUTSETTINGS_MIME_TYPE._serialized_end=1552
  _IMAGESTRANSFORMREQUEST._serialized_start=1555
  _IMAGESTRANSFORMREQUEST._serialized_end=1769
  _IMAGESTRANSFORMRESPONSE._serialized_start=1771
  _IMAGESTRANSFORMRESPONSE._serialized_end=1865
  _COMPOSITEIMAGEOPTIONS._serialized_start=1868
  _COMPOSITEIMAGEOPTIONS._serialized_end=2158
  _COMPOSITEIMAGEOPTIONS_ANCHOR._serialized_start=2032
  _COMPOSITEIMAGEOPTIONS_ANCHOR._serialized_end=2158
  _IMAGESCANVAS._serialized_start=2161
  _IMAGESCANVAS._serialized_end=2305
  _IMAGESCOMPOSITEREQUEST._serialized_start=2308
  _IMAGESCOMPOSITEREQUEST._serialized_end=2482
  _IMAGESCOMPOSITERESPONSE._serialized_start=2484
  _IMAGESCOMPOSITERESPONSE._serialized_end=2553
  _IMAGESHISTOGRAMREQUEST._serialized_start=2555
  _IMAGESHISTOGRAMREQUEST._serialized_end=2623
  _IMAGESHISTOGRAM._serialized_start=2625
  _IMAGESHISTOGRAM._serialized_end=2684
  _IMAGESHISTOGRAMRESPONSE._serialized_start=2686
  _IMAGESHISTOGRAMRESPONSE._serialized_end=2765
  _IMAGESGETURLBASEREQUEST._serialized_start=2767
  _IMAGESGETURLBASEREQUEST._serialized_end=2837
  _IMAGESGETURLBASERESPONSE._serialized_start=2839
  _IMAGESGETURLBASERESPONSE._serialized_end=2878
  _IMAGESDELETEURLBASEREQUEST._serialized_start=2880
  _IMAGESDELETEURLBASEREQUEST._serialized_end=2926
  _IMAGESDELETEURLBASERESPONSE._serialized_start=2928
  _IMAGESDELETEURLBASERESPONSE._serialized_end=2957

