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
"""Mixin to assert whether two images are equal."""

import io

import google
from PIL import Image
import six
from six.moves import range


class ImageComparisonMixin(object):

  def assert_images_are_equal(self, expected_bytes, actual_bytes):
    """Assert the images are equal pixel by pixel.

    The image comparison is pixel by pixel. In case both pixels are fully
    transparent then we consider them equal regardless of the color values.

    Note: metadata (EXIF, color profile) is not checked in this check.

    Args:
      expected_bytes: bytes representing the expected image
      actual_bytes: bytes representing the actual image
    """
    self.assertTrue(
        _images_are_equal(expected_bytes, actual_bytes),
        'Images differ:\nExpected:\n%r\nActual:\n%r' % (expected_bytes,
                                                        actual_bytes))


def _images_are_equal(bytes1, bytes2):
  """Check whether two images are equal byte by byte.

  The image comparison is pixel by pixel. In case both pixels are fully
  transparent then we consider them equal regardless of the color values.

  Note: metadata (EXIF, color profile) is not checked in this check.

  Args:
    bytes1: bytes representing the first image
    bytes2: bytes representing the second image

  Returns:
    True if the images are equal using above definition, False otherwise.
  """





  image1 = Image.open(io.BytesIO(bytes1)).convert('RGBA')
  image2 = Image.open(io.BytesIO(bytes2)).convert('RGBA')

  img1_bytes = _tobytes(image1)
  img2_bytes = _tobytes(image2)

  if len(img1_bytes) != len(img2_bytes):
    return False




  null_byte = b'\x00' [0]
  for i in range(len(img1_bytes) // 4):
    pos = 4 * i
    if img1_bytes[pos + 3] == null_byte and img2_bytes[pos + 3] == null_byte:
      continue

    if img1_bytes[pos:pos + 4] != img2_bytes[pos:pos + 4]:
      return False

  return True


def _tobytes(image):
  func = image.tostring if six.PY2 else image.tobytes
  return func('raw', 'RGBA')
