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
"""Utilities related to rendering doubles into byte arrays which sort nicely.
"""

from __future__ import absolute_import
from __future__ import division

from __future__ import print_function

import array
import struct




def is_float_negative(value, encoded):
  if value == 0:
    return encoded[0] == 128
  return value < 0



def encode_double(value):
  """Encode a double into a sortable byte buffer."""

  encoded = array.array('B')
  encoded.fromstring(struct.pack('>d', value))
  if is_float_negative(value, encoded):


    encoded[0] ^= 0xFF
    encoded[1] ^= 0xFF
    encoded[2] ^= 0xFF
    encoded[3] ^= 0xFF
    encoded[4] ^= 0xFF
    encoded[5] ^= 0xFF
    encoded[6] ^= 0xFF
    encoded[7] ^= 0xFF
  else:

    encoded[0] ^= 0x80
  return encoded
