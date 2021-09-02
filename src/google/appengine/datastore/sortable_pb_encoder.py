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
r"""An Encoder class for protocol buffers (PB) that preserves sorting characteristics.

This is used by `datastore_sqlite_stub` and `datastore_types` to match the
ordering semantics of the production datastore. Broadly, there are four
changes from regular PB encoding:

 - Strings are escaped and null terminated instead of length-prefixed. The
   escaping replaces `\x00` with `\x01\x01` and `\x01` with `\x01\x02`, thus
   preserving the ordering of the original string.
 - Variable length integers are encoded using a variable length encoding that
   preserves order. The first byte stores the absolute value if it's between
   -119 to 119, otherwise it stores the number of bytes that follow.
 - Numbers are stored big endian instead of little endian.
 - Negative doubles are entirely negated, while positive doubles have their sign
   bit flipped.

Warning:
  Due to the way nested Protocol Buffers are encoded, this encoder will NOT
  preserve sorting characteristics for embedded protocol buffers!
"""




import array
import struct
import six

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import symbol_database

_MAX_UNSIGNED_BYTE = 255


_MAX_LONG_BYTES = 8




_MAX_INLINE = (_MAX_UNSIGNED_BYTE - (2 * _MAX_LONG_BYTES)) // 2
_MIN_INLINE = -_MAX_INLINE
_OFFSET = 1 + 8
_POS_OFFSET = _OFFSET + _MAX_INLINE * 2


def ToBytes(arr):
  if six.PY2:
    return arr.tostring()
  else:
    return arr.tobytes()


def FromBytes(arr, b):
  if six.PY2:
    arr.fromstring(b)
  else:
    arr.frombytes(b)


def GetFieldNumber(field_tuple):
  """Get the field number from the tuple returned by `Message.ListFields`."""
  return field_tuple[0].number


_GROUP_START_WIRE_TYPE = 3
_GROUP_END_WIRE_TYPE = 4

_WIRE_TYPES = {
    descriptor.FieldDescriptor.TYPE_DOUBLE: 1,
    descriptor.FieldDescriptor.TYPE_FLOAT: 5,
    descriptor.FieldDescriptor.TYPE_INT64: 0,
    descriptor.FieldDescriptor.TYPE_UINT64: 0,
    descriptor.FieldDescriptor.TYPE_INT32: 0,
    descriptor.FieldDescriptor.TYPE_FIXED64: 1,
    descriptor.FieldDescriptor.TYPE_FIXED32: 5,
    descriptor.FieldDescriptor.TYPE_BOOL: 0,
    descriptor.FieldDescriptor.TYPE_STRING: 2,
    descriptor.FieldDescriptor.TYPE_MESSAGE: 2,
    descriptor.FieldDescriptor.TYPE_GROUP: 3,
    descriptor.FieldDescriptor.TYPE_BYTES: 3,
}


class Encoder(object):
  """Encodes protocol buffers in a form that sorts nicely."""

  @classmethod
  def EncodeMessage(cls, msg):
    encoder = cls()
    encoder.PutMessage(msg)
    return six.ensure_binary(ToBytes(encoder.Buffer()))

  def __init__(self):
    self.buf = array.array('B')
    return

  def Buffer(self):
    return self.buf

  def Put16(self, value):
    """Encode a fixed size 16 bit value in the buffer."""
    if value < 0 or value >= (1 << 16):
      raise message.EncodeError('u16 too big')
    self.buf.append((value >> 8) & 0xff)
    self.buf.append((value >> 0) & 0xff)
    return

  def Put32(self, value):
    """Encode a fixed size 32 bit value in the buffer."""
    if value < 0 or value >= (1 << 32):
      raise message.EncodeError('u32 too big')
    self.buf.append((value >> 24) & 0xff)
    self.buf.append((value >> 16) & 0xff)
    self.buf.append((value >> 8) & 0xff)
    self.buf.append((value >> 0) & 0xff)
    return

  def Put64(self, value):
    """Encode a fixed size 64 bit value in the buffer."""
    if value < 0 or value >= (1 << 64):
      raise message.EncodeError('u64 too big')
    self.buf.append((value >> 56) & 0xff)
    self.buf.append((value >> 48) & 0xff)
    self.buf.append((value >> 40) & 0xff)
    self.buf.append((value >> 32) & 0xff)
    self.buf.append((value >> 24) & 0xff)
    self.buf.append((value >> 16) & 0xff)
    self.buf.append((value >> 8) & 0xff)
    self.buf.append((value >> 0) & 0xff)
    return

  def _PutVarInt(self, value):
    """Encode a `varint` value in the buffer."""
    if value is None:
      self.buf.append(0)
      return

    if value >= _MIN_INLINE and value <= _MAX_INLINE:
      value = _OFFSET + (value - _MIN_INLINE)
      self.buf.append(value & 0xff)
      return

    negative = False

    if value < 0:
      value = _MIN_INLINE - value
      negative = True
    else:
      value = value - _MAX_INLINE

    length = 0
    w = value
    while w > 0:
      w >>= 8
      length += 1

    if negative:
      head = _OFFSET - length
    else:
      head = _POS_OFFSET + length
    self.buf.append(head & 0xff)

    for i in range(length - 1, -1, -1):
      b = value >> (i * 8)
      if negative:
        b = _MAX_UNSIGNED_BYTE - (b & 0xff)
      self.buf.append(b & 0xff)

  def PutVarInt32(self, value):
    """Encode a 32 bit `varint` value in the buffer."""
    if value >= 0x80000000 or value < -0x80000000:
      raise message.EncodeError('int32 too big')
    self._PutVarInt(value)

  def PutVarInt64(self, value):
    """Encode a 64 bit `varint` value in the buffer."""
    if value >= 0x8000000000000000 or value < -0x8000000000000000:
      raise message.EncodeError('int64 too big')
    self._PutVarInt(value)

  def PutVarUint64(self, value):
    """Encode a 64 bit unsigned `varint` value in the buffer."""
    if value < 0 or value >= 0x10000000000000000:
      raise message.EncodeError('uint64 too big')
    self._PutVarInt(value)

  def PutFloat(self, value):
    """Encode a floating point value in the buffer."""
    encoded = array.array('B')
    FromBytes(encoded, struct.pack('>f', value))
    if IsFloatNegative(value, encoded):


      encoded[0] ^= 0xFF
      encoded[1] ^= 0xFF
      encoded[2] ^= 0xFF
      encoded[3] ^= 0xFF
    else:

      encoded[0] ^= 0x80
    self.buf.extend(encoded)

  def PutDouble(self, value):
    """Encode a double value in the buffer."""
    encoded = array.array('B')
    FromBytes(encoded, struct.pack('>d', value))
    if IsFloatNegative(value, encoded):


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
    self.buf.extend(encoded)

  def PutPrefixedString(self, value):


    null_terminated = value.replace('\x01', '\x01\x02').replace(
        '\x00', '\x01\x01') + '\x00'
    FromBytes(self.buf, six.ensure_binary(null_terminated))

  def PutBytes(self, value):
    """Encode a byte array in the buffer."""
    null_terminated = value.replace(
        six.ensure_binary('\x01'), six.ensure_binary('\x01\x02')).replace(
            six.ensure_binary('\x00'),
            six.ensure_binary('\x01\x01')) + six.ensure_binary('\x00')
    FromBytes(self.buf, six.ensure_binary(null_terminated))

  def PutBoolean(self, v):
    """Encode a boolean value in the buffer."""
    if v:
      self.buf.append(1)
    else:
      self.buf.append(0)
    return

  def PutMessage(self, msg):
    """Encode a protocol buffer message on the buffer."""
    for field_descriptor, value in sorted(msg.ListFields(), key=GetFieldNumber):
      if field_descriptor.label == descriptor.FieldDescriptor.LABEL_REPEATED:
        self._OutputRepeatedValue(field_descriptor, value)
      else:
        self._PutScalarValue(field_descriptor, value)

  def _OutputRepeatedValue(self, field_descriptor, value):
    if field_descriptor.GetOptions().packed:
      raise NotImplementedError('Packed values not supported')
    for v in value:
      self._PutScalarValue(field_descriptor, v)

  def _PutFieldTag(self, field_descriptor):
    self.PutVarInt32((field_descriptor.number << 3)
                     | _WIRE_TYPES[field_descriptor.type])

  def _PutEndGroupTag(self, field_descriptor):
    self.PutVarInt32((field_descriptor.number << 3) | 4)

  def _PutScalarValue(self, field_descriptor, value):
    """Encode a scalar value onto the buffer."""
    self._PutFieldTag(field_descriptor)
    if field_descriptor.type == descriptor.FieldDescriptor.TYPE_DOUBLE:
      self.PutDouble(value)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_FLOAT:
      self.PutFloat(value)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_INT64:
      self.PutVarInt64(value)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_UINT64:
      self.PutVarUint64(value)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_INT32:
      self.PutVarInt32(value)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_FIXED64:
      self.Put64(value)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_FIXED32:
      self.Put32(value)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_BOOL:
      self.PutBoolean(value)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_STRING:
      self.PutPrefixedString(value)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_GROUP:
      self.PutMessage(value)
      self._PutEndGroupTag(field_descriptor)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_MESSAGE:
      encoded_bytes = self.EncodeMessage(value)
      self.PutBytes(encoded_bytes)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_BYTES:
      self.PutBytes(value)
    else:
      error_message = ('Unsupported field type. Name: %s Type: %d' %
                       (field_descriptor.full_name, field_descriptor.type))
      raise NotImplementedError(error_message)


class Decoder(object):
  """Decoder that decodes a bytes buffer into a protocol buffer message."""

  def __init__(self, buf, idx=0, limit=None):
    self.buf = buf
    self.idx = idx
    self.limit = limit or len(buf)

  @classmethod
  def DecodeMessage(cls, prototype, buf, idx=0, limit=None):
    return cls(buf, idx, limit).GetMessage(prototype)

  def _Avail(self):
    return self.limit - self.idx

  def _Buffer(self):
    return self.buf

  def _Pos(self):
    return self.idx

  def _Skip(self, n):
    if self.idx + n > self.limit:
      raise message.DecodeError('truncated')
    self.idx += n
    return

  def Get8(self):
    """Get the next 8 bits from the buffer."""
    if self.idx >= self.limit:
      raise message.DecodeError('truncated')
    c = self.buf[self.idx]
    self.idx += 1
    return c

  def Get16(self):
    """Get the next 16 bits from the buffer."""
    if self.idx + 2 > self.limit:
      raise message.DecodeError('truncated')
    c = self.buf[self.idx]
    d = self.buf[self.idx + 1]
    self.idx += 2
    return (c << 8) | d

  def Get32(self):
    """Get the next 32 bits from the buffer."""
    if self.idx + 4 > self.limit:
      raise message.DecodeError('truncated')
    c = int(self.buf[self.idx])
    d = self.buf[self.idx + 1]
    e = self.buf[self.idx + 2]
    f = self.buf[self.idx + 3]
    self.idx += 4
    return (c << 24) | (d << 16) | (e << 8) | f

  def Get64(self):
    """Get the next 64 bits from the buffer."""
    if self.idx + 8 > self.limit:
      raise message.DecodeError('truncated')
    c = int(self.buf[self.idx])
    d = int(self.buf[self.idx + 1])
    e = int(self.buf[self.idx + 2])
    f = int(self.buf[self.idx + 3])
    g = int(self.buf[self.idx + 4])
    h = self.buf[self.idx + 5]
    i = self.buf[self.idx + 6]
    j = self.buf[self.idx + 7]
    self.idx += 8
    return ((c << 56) | (d << 48) | (e << 40) | (f << 32) | (g << 24)
            | (h << 16) | (i << 8) | j)

  def GetVarInt64(self):
    """Decode the next bits as a `varint`."""
    b = self.Get8()
    if b >= _OFFSET and b <= _POS_OFFSET:
      return b - _OFFSET + _MIN_INLINE
    if b == 0:
      return None

    if b < _OFFSET:
      negative = True
      num_bytes = _OFFSET - b
    else:
      negative = False
      num_bytes = b - _POS_OFFSET

    ret = 0
    for _ in range(num_bytes):
      b = self.Get8()
      if negative:
        b = _MAX_UNSIGNED_BYTE - b
      ret = ret << 8 | b

    if negative:
      return _MIN_INLINE - ret
    else:
      return ret + _MAX_INLINE

  def GetVarInt32(self):
    """Decode the next bits as a `varint` and check it's a 32 bit value."""
    result = self.GetVarInt64()
    if result >= 0x80000000 or result < -0x80000000:
      raise message.DecodeError('corrupted')
    return result

  def GetVarUint64(self):
    """Decode the next bits as a `varint` and check it's non-negative value."""
    result = self.GetVarInt64()
    if result < 0:
      raise message.DecodeError('corrupted')
    return result

  def GetFloat(self):
    """Decode the next bits as a floating point value."""
    if self.idx + 4 > self.limit:
      raise message.DecodeError('truncated')
    a = self.buf[self.idx:self.idx + 4]
    self.idx += 4
    if a[0] & 0x80:

      a[0] ^= 0x80
    else:

      a = [x ^ 0xFF for x in a]
    return struct.unpack('>f', ToBytes(array.array('B', a)))[0]

  def GetDouble(self):
    """Decode the next bits as a double value."""
    if self.idx + 8 > self.limit:
      raise message.DecodeError('truncated')
    a = self.buf[self.idx:self.idx + 8]
    self.idx += 8
    if a[0] & 0x80:

      a[0] ^= 0x80
    else:

      a = [x ^ 0xFF for x in a]
    return struct.unpack('>d', ToBytes(array.array('B', a)))[0]

  def GetPrefixedString(self):
    end_idx = self.idx
    while self.buf[end_idx] != 0:
      end_idx += 1

    data = ToBytes(array.array('B', self.buf[self.idx:end_idx]))
    self.idx = end_idx + 1
    return data.replace(
        six.ensure_binary('\x01\x01'), six.ensure_binary('\x00')).replace(
            six.ensure_binary('\x01\x02'), six.ensure_binary('\x01'))

  def GetBoolean(self):
    """Decode the next bits as a boolean value."""
    b = self.Get8()
    if b != 0 and b != 1:
      raise message.DecodeError('corrupted')
    return b

  def _GetNumAndWireType(self):
    tt = self.GetVarInt32()
    return tt >> 3, tt & 7

  def _GetValue(self, field_descriptor, wire_type):
    """Get the next encoded value based on the field information."""
    if field_descriptor.type == descriptor.FieldDescriptor.TYPE_DOUBLE:
      return self.GetDouble()
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_FLOAT:
      return self.GetFloat()
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_INT64:
      return self.GetVarInt64()
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_UINT64:
      return self.GetVarUint64()
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_INT32:
      return self.GetVarInt32()
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_FIXED64:
      return self.Get64()
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_FIXED32:
      return self.Get32()
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_BOOL:
      return self.GetBoolean()
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_STRING:
      return six.ensure_text(self.GetPrefixedString())
    elif field_descriptor.type in (descriptor.FieldDescriptor.TYPE_GROUP,
                                   descriptor.FieldDescriptor.TYPE_MESSAGE):
      prototype = _GetPrototype(field_descriptor)
      if wire_type == _GROUP_START_WIRE_TYPE:
        return self.GetMessage(prototype)
      else:
        arr = array.array('B')
        FromBytes(arr, self.GetPrefixedString())
        sub_decoder = Decoder(arr, 0, len(arr))
        return sub_decoder.GetMessage(prototype)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_BYTES:
      return self.GetPrefixedString()
    else:
      error_message = ('Unsupported field type. Name: %s Type: %d' %
                       (field_descriptor.full_name, field_descriptor.type))
      raise NotImplementedError(error_message)

  def GetMessage(self, prototype):
    """Decode a message.

    Args:
      prototype: The prototype of the protocol buffer message.

    Returns:
      The decoded message.
    """

    msg = prototype()
    message_descriptor = prototype.DESCRIPTOR

    while self._Avail() > 0:
      number, wire_type = self._GetNumAndWireType()
      if wire_type == _GROUP_END_WIRE_TYPE:
        break
      field_descriptor = message_descriptor.fields_by_number[number]
      if field_descriptor.GetOptions().packed:
        raise NotImplementedError('Packed values not supported.')
      value = self._GetValue(field_descriptor, wire_type)

      if field_descriptor.label == descriptor.FieldDescriptor.LABEL_REPEATED:
        getattr(msg, field_descriptor.name).append(value)
      else:
        setattr(msg, field_descriptor.name, value)

    return msg


def _GetPrototype(field_descriptor):
  return symbol_database.Default().GetPrototype(field_descriptor.message_type)


def IsFloatNegative(value, encoded):
  if value == 0:
    return encoded[0] == 128
  return value < 0


def EncodeDouble(value):
  """Encode a double into a sortable byte buffer."""

  encoded = array.array('B')
  FromBytes(encoded, struct.pack('>d', value))
  if IsFloatNegative(value, encoded):


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
