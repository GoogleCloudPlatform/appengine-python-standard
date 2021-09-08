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



"""Higher-level, semantic data types for the datastore.

These types are expected to be set as attributes of `Entities`.

Most of these types are based on XML elements from Atom and GData elements
from the `atom` and `gd` namespaces. For more information, see:

- http://www.atomenabled.org/developers/syndication/
- https://developers.google.com/gdata/docs/1.0/elements

The namespace schemas are:

- http://www.w3.org/2005/Atom
- http://schemas.google.com/g/2005
"""








import array
import base64
import binascii
import calendar
import datetime
import os
import re
import struct
import time
from xml.sax import saxutils

from google.appengine.api import cmp_compat
from google.appengine.api import datastore_errors
from google.appengine.api import full_app_id
from google.appengine.api import namespace_manager
from google.appengine.api import users
from google.appengine.datastore import datastore_pbs
from google.appengine.datastore import entity_v4_pb2
from google.appengine.datastore import sortable_pb_encoder
import six
from six.moves import range
from six.moves import urllib
from six.moves import zip

from google.appengine.datastore import entity_bytes_pb2 as entity_pb2









if datastore_pbs._CLOUD_DATASTORE_ENABLED:
  from google.appengine.datastore.datastore_pbs import googledatastore







_MAX_STRING_LENGTH = 1500











_MAX_LINK_PROPERTY_LENGTH = 2083




_MAX_RAW_PROPERTY_BYTES = 1048487







RESERVED_PROPERTY_NAME = re.compile('^__.*__$')







KEY_SPECIAL_PROPERTY = '__key__'
_KEY_SPECIAL_PROPERTY = KEY_SPECIAL_PROPERTY
_UNAPPLIED_LOG_TIMESTAMP_SPECIAL_PROPERTY = '__unapplied_log_timestamp_us__'
SCATTER_SPECIAL_PROPERTY = '__scatter__'
_SPECIAL_PROPERTIES = frozenset(
    [KEY_SPECIAL_PROPERTY,
     _UNAPPLIED_LOG_TIMESTAMP_SPECIAL_PROPERTY,
     SCATTER_SPECIAL_PROPERTY])







_NAMESPACE_SEPARATOR = '!'





_EMPTY_NAMESPACE_ID = 1


_EPOCH = datetime.datetime.utcfromtimestamp(0)


if six.PY2:
  _PREFERRED_NUM_TYPE = long
else:
  _PREFERRED_NUM_TYPE = int





class UtcTzinfo(datetime.tzinfo):
  def utcoffset(self, dt): return datetime.timedelta(0)
  def dst(self, dt): return datetime.timedelta(0)
  def tzname(self, dt): return 'UTC'
  def __repr__(self): return 'datastore_types.UTC'

UTC = UtcTzinfo()


def typename(obj):
  """Returns the type of obj as a string."""


  if hasattr(obj, '__class__'):
    return getattr(obj, '__class__').__name__
  else:
    return type(obj).__name__


def ValidateString(value,
                   name='unused',
                   exception=datastore_errors.BadValueError,
                   max_len=_MAX_STRING_LENGTH,
                   empty_ok=False):
  """Raises an exception if the value is not a valid string or a subclass thereof.

  A string is valid if it's not empty, no more than `_MAX_STRING_LENGTH` bytes,
  and not a Blob. The exception type can be specified with the exception
  argument; it defaults to `BadValueError`.

  Args:
    value: The value to validate.
    name: The name of this value; used in the exception message.
    exception: The type of exception to raise.
    max_len: The maximum allowed length, in bytes.
    empty_ok: Allow empty value.
  """
  if value is None and empty_ok:
    return
  if (
      not isinstance(value, (six.text_type, six.binary_type)) or
      isinstance(value, Blob)):
    raise exception('%s should be a string; received %s (a %s):' %
                    (name, value, typename(value)))
  if not value and not empty_ok:
    raise exception('%s must not be empty.' % name)




  conversion_kwargs = {}
  if six.PY3:
    conversion_kwargs = dict(errors='surrogatepass')
  if isinstance(value, six.text_type) and len(value.encode('utf-8', **conversion_kwargs)) > max_len:
    raise exception('%s must be under %d bytes.' % (name, max_len))
  if isinstance(value, str) and len(value) > max_len:
    raise exception('%s must be under %d bytes.' % (name, max_len))


def ValidateInteger(value,
                   name='unused',
                   exception=datastore_errors.BadValueError,
                   empty_ok=False,
                   zero_ok=False,
                   negative_ok=False):
  """Raises an exception if value is not a valid integer.

  An integer is valid if it's not negative or empty and is an integer
  (either `int` or `long`). The exception type raised can be specified
  with the exception argument; it defaults to `BadValueError`.

  Args:
    value: The value to validate.
    name: The name of this value; used in the exception message.
    exception: The type of exception to raise.
    empty_ok: Allow `None` value.
    zero_ok: Allow zero value.
    negative_ok: Allow negative value.
  """
  if value is None and empty_ok:
    return
  if not isinstance(value, six.integer_types):
    raise exception('%s should be an integer; received %s (a %s).' %
                    (name, value, typename(value)))
  if not value and not zero_ok:
    raise exception('%s must not be 0 (zero)' % name)
  if value < 0 and not negative_ok:
    raise exception('%s must not be negative.' % name)

def ResolveAppId(app):
  """Validates the application ID, providing a default.

  Args:
    app: The app ID argument value to be validated.

  Returns:
    The value of the app, or the substituted default. Always a non-empty string.

  Raises:
    `BadArgumentError` if the value is empty or not a string.
  """
  if app is None:
    app = full_app_id.get()
  ValidateString(app, 'app', datastore_errors.BadArgumentError)
  return app


def ResolveNamespace(namespace):
  """Validates the app namespace, providing a default.

  If the argument is `None`, `namespace_manager.get_namespace()` is substituted.

  Args:
    namespace: The namespace argument value to be validated.

  Returns:
    The value of namespace, or the substituted default. The empty string is used
    to denote the empty namespace.

  Raises:
    `BadArgumentError` if the value is not a string.
  """
  if namespace is None:
    namespace = namespace_manager.get_namespace()
  else:
    namespace_manager.validate_namespace(
        namespace, datastore_errors.BadArgumentError)
  return namespace


def EncodeAppIdNamespace(app_id, namespace):
  """Concatenates the application ID and namespace into a single string.

  This method is needed for XML and `datastore_file_stub`.

  Args:
    app_id: The application ID to encode.
    namespace: The namespace to encode.

  Returns:
    The string encoding for the `app_id`, namespace pair.
  """
  if not namespace:
    return app_id
  else:
    return app_id + _NAMESPACE_SEPARATOR + namespace


def DecodeAppIdNamespace(app_namespace_str):
  """Decodes `app_namespace_str` into an `(app_id, namespace)` pair.

  This method is the reverse of `EncodeAppIdNamespace` and is needed for
  `datastore_file_stub`.

  Args:
    app_namespace_str: An encoded `(app_id, namespace)` pair created by
      `EncodeAppIdNamespace`.

  Returns:
    `(app_id, namespace)` pair encoded in `app_namespace_str`.
  """
  sep = app_namespace_str.find(_NAMESPACE_SEPARATOR)
  if sep < 0:
    return (app_namespace_str, '')
  else:
    return (app_namespace_str[0:sep], app_namespace_str[sep + 1:])


def SetNamespace(proto, namespace):
  """Sets the namespace for a protocol buffer or clears the field.

  Args:
    proto: An `entity_pb2.Reference` to update
    namespace: The new namespace. `None` or an empty string will clear out the
        field.
  """
  if not namespace:
    proto.ClearField('name_space')
  else:
    proto.name_space = namespace


def PartitionString(value, separator):
  """Returns a 3-element tuple containing the part before the separator and the part after the separator.

  Equivalent to python2.5 `str.partition()`.

  Args:
    value: String to be partitioned.
    separator: Separator string.
  """
  index = value.find(separator)
  if index == -1:
    return (value, '', value[0:0])
  else:
    return (value[0:index], separator, value[index+len(separator):len(value)])


@cmp_compat.total_ordering_from_cmp
class Key(object):
  """The primary key for a datastore entity.

  A datastore `GUID`. A `Key` instance uniquely identifies an entity across all
  apps, and includes all information necessary to fetch the entity from the
  datastore with `Get()`.

  `Key` implements `__hash__`, and key instances are immutable, so Keys may be
  used in sets and as dictionary keys.
  """
  __reference = None

  def __init__(self, encoded=None):
    """Constructor. Creates a Key from a string.

    Args:
      # a base64-encoded primary key, generated by Key.__str__
      encoded: str
    """
    self._bytes = None
    if encoded is not None:
      if isinstance(encoded, bytes):
        pass
      elif isinstance(encoded, six.text_type):
        encoded = encoded.encode('utf-8')
      else:
        try:
          repr_encoded = repr(encoded)
        except:
          repr_encoded = "<couldn't encode>"
        raise datastore_errors.BadArgumentError(
          'Key() expects a string; received %s (a %s).' %
          (repr_encoded, typename(encoded)))
      try:

        modulo = len(encoded) % 4
        if modulo != 0:
          encoded += (b'=' * (4 - modulo))






        self._bytes = encoded
        encoded_pb = base64.urlsafe_b64decode(self._bytes)
        self.__reference = entity_pb2.Reference.FromString(encoded_pb)
        assert self.__reference.IsInitialized()


        self._bytes = self._bytes.rstrip(b'=')

      except (AssertionError, TypeError, binascii.Error) as e:
        raise datastore_errors.BadKeyError(
          'Invalid string key %s. Details: %s' % (encoded, e))
      except Exception as e:

        if (e.__class__.__name__ == 'ProtocolBufferDecodeError' or
            e.__class__.__name__ == 'DecodeError'):
          raise datastore_errors.BadKeyError('Invalid string key %s.' % encoded)
        else:
          raise
    else:

      self.__reference = entity_pb2.Reference()

  def to_path(self, _default_id=None, _decode=True, _fail=True):
    """Construct the "path" of this key as a list.

    Returns:
      A list [kind_1, id_or_name_1, ..., kind_n, id_or_name_n] of the key path.

    Raises:
      datastore_errors.BadKeyError if this key does not have a valid path.
    """







    path = []
    for path_element in self.__reference.path.element:
      path.append(path_element.type)
      if path_element.HasField('name'):
        path.append(path_element.name)
      elif path_element.HasField('id'):
        path.append(path_element.id)
      elif _default_id is not None:
        path.append(_default_id)
      else:
        raise datastore_errors.BadKeyError('Incomplete key found in to_path')
    return path

  @staticmethod
  def from_path(*args, **kwds):
    """Static method to construct a `Key` out of a "path" (`kind`, `id` or `name`, ...).

    This is useful when an application wants to use just the id or name portion
    of a key in, e.g., a URL, where the rest of the URL provides enough
    context to fill in the other properties. For example, the app id (always
    implicit), the entity kind, and possibly an ancestor key. Since ids and
    names are usually small, they're more attractive for use in end-user-visible
    URLs than the full string representation of a key.

    Args:
      kind: The entity kind (a str or unicode instance)
      id_or_name: The id (an int or long) or name (a str or unicode instance)
      parent: Optional parent `Key`; default `None`.
      namespace: Optional namespace to use otherwise namespace_manager's
        default namespace is used.

    Returns:
      A new `Key` instance whose `.kind()` and `.id()` or `.name()` methods
      return the *last* kind and id or name positional arguments passed.

    Raises:
      `BadArgumentError` for invalid arguments.
      `BadKeyError` if the parent key is incomplete.
    """

    parent = kwds.pop('parent', None)

    app_id = ResolveAppId(kwds.pop('_app', None))



    namespace = kwds.pop('namespace', None)


    if kwds:
      raise datastore_errors.BadArgumentError(
          'Excess keyword arguments ' + repr(kwds))


    if not args or len(args) % 2:
      raise datastore_errors.BadArgumentError(
          'A non-zero even number of positional arguments is required '
          '(kind, id or name, kind, id or name, ...); received %s' % repr(args))


    if parent is not None:
      if not isinstance(parent, Key):
        raise datastore_errors.BadArgumentError(
            'Expected None or a Key as parent; received %r (a %s).' %
            (parent, typename(parent)))
      if namespace is None:
        namespace = parent.namespace()
      if not parent.has_id_or_name():
        raise datastore_errors.BadKeyError(
            'The parent Key is incomplete.')
      if app_id != parent.app() or namespace != parent.namespace():
        raise datastore_errors.BadArgumentError(
            'The app/namespace arguments (%s/%s) should match '
            'parent.app/namespace() (%s/%s)' %
            (app_id, namespace, parent.app(), parent.namespace()))


    namespace = ResolveNamespace(namespace)


    key = Key()
    ref = key.__reference
    if parent is not None:
      ref.CopyFrom(parent.__reference)
    else:
      ref.app = app_id
      SetNamespace(ref, namespace)



    path = ref.path
    for i in range(0, len(args), 2):
      kind, id_or_name = args[i:i+2]
      if isinstance(kind, six.string_types):
        kind = kind.encode('utf-8')
      else:
        raise datastore_errors.BadArgumentError(
            'Expected a string kind as argument %d; received %r (a %s).' %
            (i + 1, kind, typename(kind)))
      elem = path.element.add()
      elem.type = kind
      if isinstance(id_or_name, six.integer_types):
        elem.id = id_or_name
      elif isinstance(id_or_name, six.string_types):
        ValidateString(id_or_name, 'name')
        elem.name = id_or_name.encode('utf-8')
      else:
        raise datastore_errors.BadArgumentError(
            'Expected an integer id or string name as argument %d; '
            'received %r (a %s).' % (i + 2, id_or_name, typename(id_or_name)))


    assert ref.IsInitialized()
    return key

  def app(self):
    """Returns this entity's app id, a string."""
    if self.__reference.app:
      return self.__reference.app
    else:
      return None

  def namespace(self):
    """Returns this entity's namespace, a string."""
    if self.__reference.HasField('name_space'):
      return self.__reference.name_space
    else:
      return ''



  def kind(self):
    """Returns this entity's kind, as a string."""
    if self.__reference.path.element:
      return self.__reference.path.element[-1].type
    else:
      return None

  def id(self):
    """Returns this entity's id, or None if it doesn't have one."""
    elems = self.__reference.path.element
    if elems and elems[-1].HasField('id') and elems[-1].id:
      return elems[-1].id
    else:
      return None

  def name(self):
    """Returns this entity's name, or None if it doesn't have one."""
    elems = self.__reference.path.element
    if elems and elems[-1].HasField('name') and elems[-1].name:
      return elems[-1].name
    else:
      return None

  def id_or_name(self):
    """Returns this entity's id or name, whichever it has, or None."""
    if self.id() is not None:
      return self.id()
    else:

      return self.name()

  def has_id_or_name(self):
    """Returns True if this entity has an id or name, False otherwise.
    """
    elems = self.__reference.path.element
    if elems:
      e = elems[-1]
      return bool(e.name or e.id)
    else:
      return False

  def parent(self):
    """Returns this entity's parent, as a Key. If this entity has no parent,
    returns None."""
    if len(self.__reference.path.element) > 1:
      parent = Key()
      parent.__reference.CopyFrom(self.__reference)
      del parent.__reference.path.element[-1]
      return parent
    else:
      return None

  def ToTagUri(self):
    """Returns a tag: URI for this entity for use in XML output.

    Foreign keys for entities may be represented in XML output as tag `URIs`.
    RFC 4151 describes the tag URI scheme. From http://taguri.org/:

      The tag algorithm lets people mint - create - identifiers that no one
      else using the same algorithm could ever mint. It is simple enough to do
      in your head, and the resulting identifiers can be easy to read, write,
      and remember. The identifiers conform to the URI (URL) Syntax.

    Tag URIs for entities use the app's auth domain and the date that the URI
     is generated. The namespace-specific part is `<kind>[<key>]`.

    For example, here is the tag URI for a Kitten with the key "Fluffy" in the
    catsinsinks app:

      tag:catsinsinks.googleapps.com,2006-08-29:Kitten[Fluffy]

    Raises a `BadKeyError` if this entity's key is incomplete.
    """
    if not self.has_id_or_name():
      raise datastore_errors.BadKeyError(
        'ToTagUri() called for an entity with an incomplete key.')

    return u'tag:%s.%s,%s:%s[%s]' % (

        saxutils.escape(EncodeAppIdNamespace(self.app(), self.namespace())),
        os.environ['AUTH_DOMAIN'],
        datetime.date.today().isoformat(),
        saxutils.escape(self.kind()),
        saxutils.escape(str(self)))

  ToXml = ToTagUri

  def entity_group(self):
    """Returns this key's entity group as a Key.

    Note that the returned Key will be incomplete if this Key is for a root
    entity and it is incomplete.
    """
    group = Key._FromPb(self.__reference)
    del group.__reference.path.element[1:]
    return group

  @staticmethod
  def _FromPb(pb):
    """Static factory method.

    Creates a Key from an entity_pb2.Reference.

    Not intended to be used by application developers. Enforced by hiding the
    entity_pb2 classes.

    Args:
      pb: entity_pb2.Reference

    Returns:
      A datastore_types.Key.
    """
    if not isinstance(pb, entity_pb2.Reference):
      raise datastore_errors.BadArgumentError(
          'Key constructor takes an entity_pb2.Reference; received %s (a %s).' %
          (pb, typename(pb)))

    key = Key()
    key.__reference = entity_pb2.Reference()
    key.__reference.CopyFrom(pb)
    return key

  def _ToPb(self):
    """Converts this Key to its protocol buffer representation.

    Not intended to be used by application developers. Enforced by hiding the
    entity_pb classes.e

    Returns:
      # The `Reference` `PB` representation of this Key
      entity_pb2.Reference
    """
    pb = entity_pb2.Reference()
    pb.CopyFrom(self.__reference)

    return pb

  def __str__(self):
    """Encodes this `Key` as an opaque string.

    Returns a string representation of this key, suitable for use in HTML,
    URLs, and other similar use cases. If the entity's key is incomplete,
    raises a `BadKeyError`.

    Unfortunately, this string encoding isn't particularly compact, and its
    length varies with the length of the path. If you want a shorter identifier
    and you know the kind and parent (if any) ahead of time, consider using just
    the entity's id or name.

    Returns:
      string
    """



    try:
      if self._bytes is not None:
        return self._bytes.decode('utf-8')
    except AttributeError:
      pass
    if (self.has_id_or_name()):
      encoded = base64.urlsafe_b64encode(self.__reference.SerializeToString())
      self._bytes = encoded.replace(b'=', b'')
    else:
      raise datastore_errors.BadKeyError(
        'Cannot string encode an incomplete key!\n%s' % self.__reference)
    return self._bytes.decode('utf-8')


  def __repr__(self):
    """Returns a Python string of the form `datastore_types.Key.from_path(...)` that can be used to recreate this key.

    Returns:
      String
    """
    args = []
    for elem in self.__reference.path.element:
      args.append(six.text_type(repr(elem.type)))
      if elem.HasField('name'):
        args.append(six.text_type(repr(elem.name)))
      else:
        args.append(repr(elem.id))

    args.append('_app=%r' % self.__reference.app)
    if self.__reference.HasField('name_space'):
      args.append('namespace=%r' % six.ensure_text(self.__reference.name_space))
    return u'datastore_types.Key.from_path(%s)' % ', '.join(args)

  def __cmp__(self, other):
    """Returns negative, zero, or positive when comparing two keys.

    TODO: for API v2, we should change this to make incomplete keys, ie
    keys without an id or name, not equal to any other keys.

    Args:
      other: Key to compare to.

    Returns:
      Negative if self is less than "other"
      Zero if "other" is equal to self
      Positive if self is greater than "other"
    """

    if not isinstance(other, Key):
      return -2

    self_args = [self.__reference.app, self.__reference.name_space]
    self_args += self.to_path(_default_id=0, _decode=False)

    other_args = [other.__reference.app, other.__reference.name_space]
    other_args += other.to_path(_default_id=0, _decode=False)

    for self_component, other_component in zip(self_args, other_args):
      comparison = cmp_compat.cmp(self_component, other_component)
      if comparison != 0:
        return comparison

    return cmp_compat.cmp(len(self_args), len(other_args))

  def __hash__(self):
    """Returns an integer hash of this key.

    Implements Python's hash protocol so that Keys may be used in sets and as
    dictionary keys.

    Returns:
      int
    """
    args = self.to_path(_default_id=0, _fail=False)
    args.append(self.__reference.app)
    return hash(type(args)) ^ hash(tuple(args))


class _OverflowDateTime(_PREFERRED_NUM_TYPE):
  """Container for GD_WHEN values that don't fit into a datetime.datetime.

  This class only exists to safely round-trip GD_WHEN values that are too large
  to fit in a datetime.datetime instance e.g. that were created by Java
  applications. It should not be created directly.
  """
  pass

def _EmptyList(val):
  if val is not None:
    raise datastore_errors.BadValueError('value should be None.')
  return []

def _When(val):
  """Coverts a GD_WHEN value to the appropriate type."""
  try:
    return _EPOCH + datetime.timedelta(microseconds=val)
  except OverflowError:
    return _OverflowDateTime(val)










class Category(six.text_type):
  """A tag, ie a descriptive word or phrase. Entities may be tagged by users,
  and later returned by a queries for that tag. Tags can also be used for
  ranking results (frequency), photo captions, clustering, activity, etc.

  This is the Atom `category` element. In XML output, the tag is provided as
  the term attribute. See:
  http://www.atomenabled.org/developers/syndication/#category

  Raises `BadValueError` if tag is not a string or subtype.
  """
  TERM = 'user-tag'

  def __init__(self, tag):
    super(Category, self).__init__()
    ValidateString(tag, 'tag')

  def ToXml(self):
    return u'<category term="%s" label=%s />' % (Category.TERM,
                                                 saxutils.quoteattr(self))


class Link(six.text_type):
  """A fully qualified URL. Usually http: scheme, but may also be file:, ftp:,
  news:, among others.

  If you have email (`mailto:`) or instant messaging (`aim:`, `xmpp:`) links,
  consider using the `Email` or `IM` classes instead.

  This is the Atom `link` element. In XML output, the link is provided as the
  href attribute. See:
  http://www.atomenabled.org/developers/syndication/#link

  Raises `BadValueError` if link is not a fully qualified, well-formed URL.
  """
  def __init__(self, link):
    super(Link, self).__init__()
    ValidateString(link, 'link', max_len=_MAX_LINK_PROPERTY_LENGTH)

    scheme, domain, path, _, _, _ = urllib.parse.urlparse(link)
    if (not scheme or (scheme != 'file' and not domain) or
                      (scheme == 'file' and not path)):
      raise datastore_errors.BadValueError('Invalid URL: %s' % link)

  def ToXml(self):
    return u'<link href=%s />' % saxutils.quoteattr(self)


class Email(six.text_type):
  """An RFC2822 email address. Makes no attempt at validation.

  This is the `gd:email` element. In XML output, the email address is provided
  as the address attribute. See:
  https://developers.google.com/gdata/docs/1.0/elements#gdEmail

  Raises `BadValueError` if email is not a valid email address.
  """
  def __init__(self, email):
    super(Email, self).__init__()
    ValidateString(email, 'email')

  def ToXml(self):
    return u'<gd:email address=%s />' % saxutils.quoteattr(self)


@cmp_compat.total_ordering_from_cmp
class GeoPt(object):
  """A geographical point, specified by floating-point latitude and longitude
  coordinates. Often used to integrate with mapping sites like Google Maps.

  This is the `georss:point` element. In XML output, the coordinates are
  provided as the `lat` and `lon` attributes. See: http://georss.org/

  Serializes to `<lat>,<lon>`. Raises `BadValueError` if it's passed an invalid
  serialized string, or if `lat` and `lon` are not valid floating points in the
  ranges [-90, 90] and [-180, 180], respectively.
  """
  lat = None
  lon = None

  def __init__(self, lat, lon=None):
    if lon is None:

      try:
        split = lat.split(',')
        lat, lon = split
      except (AttributeError, ValueError):
        raise datastore_errors.BadValueError(
          'Expected a "lat,long" formatted string; received %s (a %s).' %
          (lat, typename(lat)))

    try:
      lat = float(lat)
      lon = float(lon)
      if abs(lat) > 90:
        raise datastore_errors.BadValueError(
          'Latitude must be between -90 and 90; received %f' % lat)
      if abs(lon) > 180:
        raise datastore_errors.BadValueError(
          'Longitude must be between -180 and 180; received %f' % lon)
    except (TypeError, ValueError):

      raise datastore_errors.BadValueError(
        'Expected floats for lat and long; received %s (a %s) and %s (a %s).' %
        (lat, typename(lat), lon, typename(lon)))

    self.lat = lat
    self.lon = lon

  def __cmp__(self, other):
    """Returns negative, zero, or positive when comparing two `GeoPts`."""

    if not isinstance(other, GeoPt):
      try:
        other = GeoPt(other)
      except datastore_errors.BadValueError:
        return NotImplemented


    lat_cmp = cmp_compat.cmp(self.lat, other.lat)
    if lat_cmp != 0:
      return lat_cmp
    else:
      return cmp_compat.cmp(self.lon, other.lon)

  def __hash__(self):
    """Returns an integer hash of this point.

    Implements Python's hash protocol so that `GeoPts` may be used in sets and
    as dictionary keys.

    Returns:
      int
    """
    return hash((self.lat, self.lon))

  def __repr__(self):
    """Returns a string of the form `datastore_types.GeoPt([lat], [lon])`.

    Returns:
      String
    """
    return 'datastore_types.GeoPt(%r, %r)' % (self.lat, self.lon)

  def __unicode__(self):
    return u'%s,%s' % (six.text_type(self.lat),
                       six.text_type(self.lon))

  __str__ = __unicode__

  def ToXml(self):
    return u'<georss:point>%s %s</georss:point>' % (six.text_type(
        self.lat), six.text_type(self.lon))


@cmp_compat.total_ordering_from_cmp
class IM(object):
  """An instant messaging handle. Includes both an address and its protocol.
  The protocol value is either a standard IM scheme or a URL identifying the
  IM network for the protocol. Possible values include:

    Value                           Description
    sip                             SIP/SIMPLE
    unknown                         Unknown or unspecified
    xmpp                            XMPP/Jabber
    http://aim.com/                 AIM
    http://icq.com/                 ICQ
    http://talk.google.com/         Google Talk
    http://messenger.msn.com/       MSN Messenger
    http://messenger.yahoo.com/     Yahoo Messenger
    http://sametime.com/            Lotus Sametime
    http://gadu-gadu.pl/            Gadu-Gadu

  This is the gd:im element. In XML output, the address and protocol are
  provided as the address and protocol attributes, respectively. See:
  https://developers.google.com/gdata/docs/1.0/elements#gdIm

  Serializes to `<protocol> <address>`. Raises `BadValueError` if tag is not a
  standard IM scheme or a URL.
  """
  PROTOCOLS = [ 'sip', 'unknown', 'xmpp' ]

  protocol = None
  address = None

  def __init__(self, protocol, address=None):
    if address is None:

      try:
        split = protocol.split(' ', 1)
        protocol, address = split
      except (AttributeError, ValueError):
        raise datastore_errors.BadValueError(
          'Expected string of format "protocol address"; received %s' %
          (protocol,))

    ValidateString(address, 'address')
    if protocol not in self.PROTOCOLS:

      Link(protocol)

    self.address = address
    self.protocol = protocol

  def __cmp__(self, other):
    """Returns negative, zero, or positive when comparing two `IM`s."""

    if not isinstance(other, IM):
      try:
        other = IM(other)
      except datastore_errors.BadValueError:
        return NotImplemented











    return cmp_compat.cmp((self.address, self.protocol),
                          (other.address, other.protocol))

  def __repr__(self):
    """Returns a string of the form `datastore_types.IM('address', 'protocol')`.

    Returns:
      string
    """
    return 'datastore_types.IM(%r, %r)' % (self.protocol, self.address)

  def __unicode__(self):
    return u'%s %s' % (self.protocol, self.address)

  __str__ = __unicode__

  def ToXml(self):
    return (u'<gd:im protocol=%s address=%s />' %
            (saxutils.quoteattr(self.protocol),
             saxutils.quoteattr(self.address)))

  def __len__(self):
    return len(six.text_type(self))


class PhoneNumber(six.text_type):
  """A human-readable phone number or address.

  No validation is performed. Phone numbers have many different formats -
  local, long distance, domestic, international, internal extension, TTY,
  VOIP, SMS, and alternative networks like Skype, XFire and Roger Wilco. They
  all have their own numbering and addressing formats.

  This is the `gd:phoneNumber` element. In XML output, the phone number is
  provided as the text of the element. See:
  https://developers.google.com/gdata/docs/1.0/elements#gdPhoneNumber

  Raises `BadValueError` if phone is not a string or subtype.
  """
  def __init__(self, phone):
    super(PhoneNumber, self).__init__()
    ValidateString(phone, 'phone')

  def ToXml(self):
    return u'<gd:phoneNumber>%s</gd:phoneNumber>' % saxutils.escape(self)


class PostalAddress(six.text_type):
  """A human-readable mailing address. Again, mailing address formats vary
  widely, so no validation is performed.

  This is the gd:postalAddress element. In XML output, the address is provided
  as the text of the element. See:
  https://developers.google.com/gdata/docs/1.0/elements#gdPostalAddress

  Raises `BadValueError` if address is not a string or subtype.
  """
  def __init__(self, address):
    super(PostalAddress, self).__init__()
    ValidateString(address, 'address')

  def ToXml(self):
    return u'<gd:postalAddress>%s</gd:postalAddress>' % saxutils.escape(self)


class Rating(_PREFERRED_NUM_TYPE):
  """A user-provided integer rating for a piece of content. Normalized to a
  0-100 scale.

  This is the gd:rating element. In XML output, the address is provided
  as the text of the element. See:
  https://developers.google.com/gdata/docs/1.0/elements#gdRating

  Serializes to the decimal string representation of the rating. Raises
  `BadValueError` if the rating is not an integer in the range [0, 100].
  """
  MIN = 0
  MAX = 100

  def __init__(self, rating):
    super(Rating, self).__init__()
    if isinstance(rating, float) or isinstance(rating, complex):

      raise datastore_errors.BadValueError(
        'Expected int or long; received %s (a %s).' %
        (rating, typename(rating)))

    try:
      if (_PREFERRED_NUM_TYPE(rating) < Rating.MIN
          or _PREFERRED_NUM_TYPE(rating) > Rating.MAX):
        raise datastore_errors.BadValueError()
    except ValueError:

      raise datastore_errors.BadValueError(
          'Expected int or long; received %s (a %s).' %
          (rating, typename(rating)))

  def ToXml(self):
    return (u'<gd:rating value="%d" min="%d" max="%d" />' %
            (self, Rating.MIN, Rating.MAX))


class Text(six.text_type):
  """A long string type.

  Strings of any length can be stored in the datastore using this
  type. It behaves identically to the Python unicode type, except for
  the constructor, which only accepts str and unicode arguments.
  """

  def __new__(cls, arg=None, encoding=None):
    """Constructor.

    We only accept unicode and str instances, the latter with encoding.

    Args:
      arg: optional unicode or str instance; default u''
      encoding: optional encoding; disallowed when `isinstance(arg, unicode)`,
                defaults to `ascii` when `isinstance(arg, str)`;
    """
    if arg is None:
      arg = u''
    if isinstance(arg, six.text_type):
      if encoding is not None:
        raise TypeError('Text() with a unicode argument '
                        'should not specify an encoding')
      return super(Text, cls).__new__(cls, arg)

    if isinstance(arg, bytes):
      if encoding is None:
        encoding = 'ascii'
      return super(Text, cls).__new__(cls, arg, encoding)

    raise TypeError('Text() argument should be str or unicode, not %s' %
                    type(arg).__name__)


class _BaseByteType(bytes):
  """A base class for datastore types that are encoded as bytes.

  This behaves identically to the Python bytes type, except for the
  constructor, which only accepts bytes arguments.
  """

  def __new__(cls, arg=None):
    """Constructor.

    We only accept bytes instances.

    Args:
      arg: optional bytes instance (default b'')
    """
    if arg is None:
      arg = b''

    if isinstance(arg, bytes):
      return super(_BaseByteType, cls).__new__(cls, arg)

    raise TypeError('%s() argument should be bytes instance, not %s' %
                    (cls.__name__, type(arg).__name__))

  def ToXml(self):
    """Output bytes as XML.

    Returns:
      Base64 encoded version of itself for safe insertion in to an XML document.
    """
    encoded = base64.urlsafe_b64encode(self).decode('utf-8')
    return saxutils.escape(encoded)

  if six.PY3:


    def __str__(self):
      return self.decode('utf-8')


class Blob(_BaseByteType):
  """A blob type, appropriate for storing binary data of any length.

  This behaves identically to the Python bytes type, except for the
  constructor, which only accepts bytes arguments.
  """

  def __new__(cls, *args, **kwargs):
    self = super(Blob, cls).__new__(cls, *args, **kwargs)
    self._meaning_uri = None
    return self

  @property
  def meaning_uri(self):
    return self._meaning_uri

  @meaning_uri.setter
  def meaning_uri(self, value):
    self._meaning_uri = value


class EmbeddedEntity(_BaseByteType):
  """A proto encoded `EntityProto`.

  This behaves identically to Blob, except for the
  constructor, which accepts a bytes or `EntityProto` argument.

  Can be decoded using `datastore.Entity.FromProto()`,
  `db.model_from_protobuf()`, or
  `ndb.LocalStructuredProperty`.
  """

  def __new__(cls, arg=None):
    """Constructor.

    Args:
      arg: Optional str or `EntityProto` instance (default `''`).
    """
    if isinstance(arg, entity_pb2.EntityProto):
      arg = arg.SerializePartialToString()
    return super(EmbeddedEntity, cls).__new__(cls, arg)


class ByteString(_BaseByteType):
  """A byte-string type, appropriate for storing short amounts of indexed data.

  This behaves identically to Blob, except it's used only for short, indexed
  byte strings.
  """
  pass


@cmp_compat.total_ordering_from_cmp
class BlobKey(object):
  """Key used to identify a blob in Blobstore.

  This object wraps a string that gets used internally by the Blobstore API
  to identify application blobs. The `BlobKey` corresponds to the entity name
  of the underlying `BlobReference` entity.

  This class is exposed in the API in both `google.appengine.ext.db` and
  `google.appengine.ext.blobstore`.
  """

  def __init__(self, blob_key):
    """Constructor.

    Used to convert a string to a `BlobKey`.  Normally used internally by
    Blobstore API.

    Args:
      blob_key:  Key name of `BlobReference` that this key belongs to.
    """
    ValidateString(blob_key, 'blob-key', empty_ok=True)
    self.__blob_key = blob_key

  def __str__(self):
    """Convert to string."""
    return six.ensure_str(self.__blob_key)

  def __repr__(self):
    """Returns a Python string of the form 'datastore_types.BlobKey(...)' that can be used to recreate this key.

    Returns:
      String
    """
    return 'datastore_types.%s(%r)' % (type(self).__name__, self.__blob_key)

  def __cmp__(self, other):


    if type(other) is type(self):
      return cmp_compat.cmp(str(self), str(other))
    elif isinstance(other, six.string_types):
      return cmp_compat.cmp(self.__blob_key, other)
    else:
      return NotImplemented

  def __hash__(self):
    return hash(self.__blob_key)

  def ToXml(self):
    return str(self)



_PROPERTY_MEANINGS = {



    Blob: entity_pb2.Property.BLOB,
    EmbeddedEntity: entity_pb2.Property.ENTITY_PROTO,
    ByteString: entity_pb2.Property.BYTESTRING,
    Text: entity_pb2.Property.TEXT,
    datetime.datetime: entity_pb2.Property.GD_WHEN,
    datetime.date: entity_pb2.Property.GD_WHEN,
    datetime.time: entity_pb2.Property.GD_WHEN,
    _OverflowDateTime: entity_pb2.Property.GD_WHEN,
    Category: entity_pb2.Property.ATOM_CATEGORY,
    Link: entity_pb2.Property.ATOM_LINK,
    Email: entity_pb2.Property.GD_EMAIL,
    GeoPt: entity_pb2.Property.GEORSS_POINT,
    IM: entity_pb2.Property.GD_IM,
    PhoneNumber: entity_pb2.Property.GD_PHONENUMBER,
    PostalAddress: entity_pb2.Property.GD_POSTALADDRESS,
    Rating: entity_pb2.Property.GD_RATING,
    BlobKey: entity_pb2.Property.BLOBKEY,
}


_PROPERTY_TYPES = frozenset([
    Blob,
    EmbeddedEntity,
    ByteString,
    bool,
    Category,
    datetime.datetime,
    _OverflowDateTime,
    Email,
    float,
    GeoPt,
    IM,
    int,
    Key,
    Link,
    _PREFERRED_NUM_TYPE,
    PhoneNumber,
    PostalAddress,
    Rating,
    str,
    Text,
    type(None),
    six.text_type,
    users.User,
    BlobKey,
    bytes,
])




_RAW_PROPERTY_TYPES = (Blob, Text, EmbeddedEntity)
_RAW_PROPERTY_MEANINGS = (entity_pb2.Property.BLOB, entity_pb2.Property.TEXT,
                          entity_pb2.Property.ENTITY_PROTO)


def ValidatePropertyInteger(name, value):
  """Raises an exception if the supplied integer is invalid.

  Args:
    name: Name of the property this is for.
    value: Integer value.

  Raises:
    `OverflowError` if the value does not fit within a signed `int64`.
  """
  if not (-0x8000000000000000 <= value <= 0x7fffffffffffffff):
    raise OverflowError('%d is out of bounds for int64' % value)


def ValidateStringLength(name, value, max_len):
  """Raises an exception if the supplied string is too long.

  Args:
    name: Name of the property this is for.
    value: String value.
    max_len: Maximum length the string may be.

  Raises:
    `OverflowError` if the value is larger than the maximum length.
  """

  if isinstance(value, six.text_type):
    value = value.encode('utf-8')

  if len(value) > max_len:
    raise datastore_errors.BadValueError(
      'Property %s is %d bytes long; it must be %d or less. '
      'Consider Text instead, which can store strings of any length.' %
      (name, len(value), max_len))


def ValidatePropertyString(name, value):
  """Validates the length of an indexed string property.

  Args:
    name: Name of the property this is for.
    value: String value.
  """
  ValidateStringLength(name, value, max_len=_MAX_STRING_LENGTH)


def ValidatePropertyLink(name, value):
  """Validates the length of an indexed `Link` property.

  Args:
    name: Name of the property this is for.
    value: String value.
  """
  ValidateStringLength(name, value, max_len=_MAX_LINK_PROPERTY_LENGTH)


def ValidatePropertyNothing(name, value):
  """No-op validation function.

  Args:
    name: Name of the property this is for.
    value: Not used.
  """
  pass


def ValidatePropertyKey(name, value):
  """Raises an exception if the supplied `datastore.Key` instance is invalid.

  Args:
    name: Name of the property this is for.
    value: A `datastore.Key` instance.

  Raises:
    `datastore_errors.BadValueError` if the value is invalid.
  """
  if not value.has_id_or_name():
    raise datastore_errors.BadValueError(
        'Incomplete key found for reference property %s.' % name)







_VALIDATE_PROPERTY_VALUES = {
    Blob: ValidatePropertyNothing,
    EmbeddedEntity: ValidatePropertyNothing,
    ByteString: ValidatePropertyNothing,
    bool: ValidatePropertyNothing,
    Category: ValidatePropertyNothing,
    datetime.datetime: ValidatePropertyNothing,
    _OverflowDateTime: ValidatePropertyInteger,
    Email: ValidatePropertyNothing,
    float: ValidatePropertyNothing,
    GeoPt: ValidatePropertyNothing,
    IM: ValidatePropertyNothing,
    int: ValidatePropertyInteger,
    Key: ValidatePropertyKey,
    Link: ValidatePropertyNothing,
    _PREFERRED_NUM_TYPE: ValidatePropertyInteger,
    PhoneNumber: ValidatePropertyNothing,
    PostalAddress: ValidatePropertyNothing,
    Rating: ValidatePropertyInteger,
    str: ValidatePropertyNothing,
    Text: ValidatePropertyNothing,
    type(None): ValidatePropertyNothing,
    six.text_type: ValidatePropertyNothing,
    bytes: ValidatePropertyNothing,
    users.User: ValidatePropertyNothing,
    BlobKey: ValidatePropertyNothing,
}










_PROPERTY_TYPE_TO_INDEX_VALUE_TYPE = {
    six.text_type: bytes,
    Blob: bytes,
    EmbeddedEntity: bytes,
    ByteString: bytes,
    bool: bool,
    Category: bytes,
    datetime.datetime: _PREFERRED_NUM_TYPE,
    datetime.date: _PREFERRED_NUM_TYPE,
    datetime.time: _PREFERRED_NUM_TYPE,
    _OverflowDateTime: _PREFERRED_NUM_TYPE,
    Email: six.binary_type,
    float: float,
    GeoPt: GeoPt,
    IM: six.binary_type,
    int: _PREFERRED_NUM_TYPE,
    Key: Key,
    Link: six.binary_type,
    _PREFERRED_NUM_TYPE: _PREFERRED_NUM_TYPE,
    PhoneNumber: six.binary_type,
    PostalAddress: six.binary_type,
    Rating: _PREFERRED_NUM_TYPE,
    bytes: bytes,
    Text: bytes,
    type(None): type(None),
    users.User: users.User,
    BlobKey: bytes,
}
if six.PY2:


  _PROPERTY_TYPE_TO_INDEX_VALUE_TYPE[basestring] = bytes


assert set(_VALIDATE_PROPERTY_VALUES.keys()) == _PROPERTY_TYPES


def ValidateProperty(name, values, read_only=False):
  """Helper function for validating property values.

  Args:
    name: Name of the property this is for.
    value: Value for the property as a Python native type.
    read_only: Deprecated.

  Raises:
    `BadPropertyError` if the property name is invalid. `BadValueError` if the
    property did not validate correctly or the value was an empty list. Other
    exception types (like `OverflowError`) if the property value does not meet
    type-specific criteria.
  """
  ValidateString(name, 'property name', datastore_errors.BadPropertyError)

  values_type = type(values)


  if values_type is tuple:
    raise datastore_errors.BadValueError(
        'May not use tuple property value; property %s is %s.' %
        (name, repr(values)))


  if values_type is not list:
    values = [values]



  try:
    for v in values:
      prop_validator = _VALIDATE_PROPERTY_VALUES.get(v.__class__)
      if prop_validator is None:
        raise datastore_errors.BadValueError(
          'Unsupported type for property %s: %s' % (name, v.__class__))
      prop_validator(name, v)

  except (KeyError, ValueError, TypeError, IndexError, AttributeError) as msg:
    raise datastore_errors.BadValueError(
      'Error type checking values for property %s: %s' % (name, msg))





ValidateReadProperty = ValidateProperty



def PackBlob(name, value, pbvalue):
  """Packs a Blob property into a `entity_pb2.PropertyValue`.

  Args:
    name: The name of the property as a string.
    value: A Blob instance.
    pbvalue: The `entity_pbs.PropertyValue` to pack this value into.
  """
  pbvalue.stringValue = value


def PackString(name, value, pbvalue):
  """Packs a string-typed property into a entity_pb2.PropertyValue.

  Args:
    name: The name of the property as a string.
    value: A string, unicode, or string-like value instance.
    pbvalue: The entity_pb2.PropertyValue to pack this value into.
  """
  if isinstance(value, bytes):



    value.decode('ascii')
    pbvalue.stringValue = value
  else:
    pbvalue.stringValue = six.text_type(value).encode('utf-8')


def PackDatetime(name, value, pbvalue):
  """Packs a `datetime`-typed property into a `entity_pb2.PropertyValue`.

  Args:
    name: The name of the property as a string.
    value: A `datetime.datetime` instance.
    pbvalue: The `entity_pb2.PropertyValue` to pack this value into.
  """
  pbvalue.int64Value = DatetimeToTimestamp(value)


def DatetimeToTimestamp(value):
  """Converts a `datetime.datetime` to microseconds since the epoch, as a float.

  Args:
    value: `datetime.datetime`

  Returns:
    Value as a `long`.
  """
  if value.tzinfo:

    value = value.astimezone(UTC)
  return _PREFERRED_NUM_TYPE(
      calendar.timegm(value.timetuple()) * 1000000) + value.microsecond


def PackGeoPt(name, value, pbvalue):
  """Packs a `GeoPt` property into a `entity_pb2.PropertyValue`.

  Args:
    name: The name of the property as a string.
    value: A `GeoPt` instance.
    pbvalue: The `entity_pb2.PropertyValue` to pack this value into.
  """
  pbvalue.pointvalue.x = value.lat
  pbvalue.pointvalue.y = value.lon


def PackUser(name, value, pbvalue):
  """Packs a `User` property into a `entity_pb2.PropertyValue`.

  Args:
    name: The name of the property as a string.
    value: A `users.User` instance.
    pbvalue: The `entity_pb2.PropertyValue` to pack this value into.
  """
  pbvalue.uservalue.email = value.email().encode('utf-8')
  pbvalue.uservalue.auth_domain = value.auth_domain().encode('utf-8')
  pbvalue.uservalue.gaiaid = 0




  if value.user_id() is not None:
    pbvalue.uservalue.obfuscated_gaiaid = value.user_id().encode('utf-8')

  if value.federated_identity() is not None:
    pbvalue.uservalue.federated_identity = value.federated_identity().encode(
        'utf-8')

  if value.federated_provider() is not None:
    pbvalue.uservalue.federated_provider = value.federated_provider().encode(
        'utf-8')


def PackKey(name, value, pbvalue):
  """Packs a reference property into an `entity_pb2.PropertyValue`.

  Args:
    name: The name of the property as a string.
    value: A `Key` instance.
    pbvalue: The `entity_pb2.PropertyValue` to pack this value into.
  """
  ref = value._Key__reference
  pbvalue.referencevalue.app = ref.app
  SetNamespace(pbvalue.referencevalue, ref.name_space)
  for elem in ref.path.element:
    elementCopy = pbvalue.referencevalue.pathelement.add()
    datastore_pbs.copy_path_element(elem, elementCopy)


def PackBool(name, value, pbvalue):
  """Packs a boolean property into an `entity_pb2.PropertyValue`.

  Args:
    name: The name of the property as a string.
    value: A boolean instance.
    pbvalue: The `entity_pb2.PropertyValue` to pack this value into.
  """
  pbvalue.booleanValue = value


def PackInteger(name, value, pbvalue):
  """Packs an integer property into an `entity_pb2.PropertyValue`.

  Args:
    name: The name of the property as a string.
    value: An int or long instance.
    pbvalue: The `entity_pb2.PropertyValue` to pack this value into.
  """
  pbvalue.int64Value = value


def PackFloat(name, value, pbvalue):
  """Packs a float property into a `entity_pb2.PropertyValue`.

  Args:
    name: The name of the property as a string.
    value: A float instance.
    pbvalue: The `entity_pb2.PropertyValue` to pack this value into.
  """
  pbvalue.doubleValue = value







_PACK_PROPERTY_VALUES = {
    Blob: PackBlob,
    EmbeddedEntity: PackBlob,
    ByteString: PackBlob,
    bool: PackBool,
    Category: PackString,
    datetime.datetime: PackDatetime,
    _OverflowDateTime: PackInteger,
    Email: PackString,
    float: PackFloat,
    GeoPt: PackGeoPt,
    IM: PackString,
    int: PackInteger,
    Key: PackKey,
    Link: PackString,
    _PREFERRED_NUM_TYPE: PackInteger,
    PhoneNumber: PackString,
    PostalAddress: PackString,
    Rating: PackInteger,
    str: PackString,
    Text: PackString,
    type(None): lambda name, value, pbvalue: pbvalue.ClearField('stringValue'),
    six.text_type: PackString,
    users.User: PackUser,
    BlobKey: PackString,
    bytes: PackString,
}


assert set(_PACK_PROPERTY_VALUES.keys()) == _PROPERTY_TYPES


def ToPropertyPb(name, values):
  """Creates type-specific `entity_pb2.PropertyValues`.

  Determines the type and meaning of the `PropertyValue` based on the Python
  type of the input value(s).

  NOTE: This function does not validate anything!

  Args:
    name: String or unicode; the property name.
    values: The values for this property, either a single one or a list of them.
      All values must be a supported type. Lists of values must all be of the
      same type.

  Returns:
    A list of `entity_pb2.Property` instances.
  """
  encoded_name = six.ensure_str(name)

  values_type = type(values)
  if values_type is list and len(values) == 0:

    pb = entity_pb2.Property()
    pb.meaning = entity_pb2.Property.EMPTY_LIST
    pb.name = encoded_name
    pb.multiple = False

    pb.value.ClearField('stringValue')
    return pb
  elif values_type is list:
    multiple = True
  else:
    multiple = False
    values = [values]

  pbs = []
  for v in values:
    pb = entity_pb2.Property()
    pb.name = encoded_name
    pb.multiple = multiple

    meaning = _PROPERTY_MEANINGS.get(v.__class__)
    if meaning is not None:
      pb.meaning = meaning

    if hasattr(v, 'meaning_uri') and v.meaning_uri:
      pb.meaning_uri = v.meaning_uri

    pack_prop = _PACK_PROPERTY_VALUES[v.__class__]
    pack_prop(name, v, pb.value)
    pbs.append(pb)

  if multiple:
    return pbs
  else:
    return pbs[0]


def FromReferenceProperty(value):
  """Converts a reference `PropertyValue` to a `Key`.

  Args:
    value: `entity_pb2.PropertyValue`

  Returns:
    `Key`

  Raises:
    `BadValueError` if the value is not a `PropertyValue`.
  """
  assert isinstance(value, entity_pb2.PropertyValue)
  assert value.HasField('referencevalue')
  ref = value.referencevalue

  key = Key()
  key_ref = key._Key__reference
  key_ref.app = ref.app
  SetNamespace(key_ref, ref.name_space)

  for pathelem in ref.pathelement:
    element = key_ref.path.element.add()
    datastore_pbs.copy_path_element(pathelem, element)

  return key









_PROPERTY_CONVERSIONS = {
    entity_pb2.Property.GD_WHEN: _When,
    entity_pb2.Property.ATOM_CATEGORY: Category,
    entity_pb2.Property.ATOM_LINK: Link,
    entity_pb2.Property.GD_EMAIL: Email,
    entity_pb2.Property.GD_IM: IM,
    entity_pb2.Property.GD_PHONENUMBER: PhoneNumber,
    entity_pb2.Property.GD_POSTALADDRESS: PostalAddress,
    entity_pb2.Property.GD_RATING: Rating,
    entity_pb2.Property.BLOB: Blob,
    entity_pb2.Property.ENTITY_PROTO: EmbeddedEntity,
    entity_pb2.Property.BYTESTRING: ByteString,
    entity_pb2.Property.TEXT: Text,
    entity_pb2.Property.BLOBKEY: BlobKey,
    entity_pb2.Property.EMPTY_LIST: _EmptyList,
}

_NON_UTF8_MEANINGS = frozenset(
    (entity_pb2.Property.BLOB, entity_pb2.Property.ENTITY_PROTO,
     entity_pb2.Property.BYTESTRING, entity_pb2.Property.INDEX_VALUE))


def FromPropertyPb(pb):
  """Converts a property `PB` to a python value.

  Args:
    pb: `entity_pb2.Property`

  Returns:
    The return type is determined by the type of the argument, such as
    `string`, `int`, `bool`, `double`, `users.User`, or one of the `atom` or
    `gd` types.
  """
  pbval = pb.value
  meaning = pb.meaning

  if pbval.HasField('stringValue'):
    value = pbval.stringValue
    if not pb.HasField('meaning') or meaning not in _NON_UTF8_MEANINGS:

      value = value.decode('utf-8')
  elif pbval.HasField('int64Value'):


    value = _PREFERRED_NUM_TYPE(pbval.int64Value)
  elif pbval.HasField('booleanValue'):


    value = bool(pbval.booleanValue)
  elif pbval.HasField('doubleValue'):
    value = pbval.doubleValue
  elif pbval.HasField('referencevalue'):
    value = FromReferenceProperty(pbval)
  elif pbval.HasField('pointvalue'):
    value = GeoPt(pbval.pointvalue.x, pbval.pointvalue.y)
  elif pbval.HasField('uservalue'):
    email = pbval.uservalue.email
    auth_domain = pbval.uservalue.auth_domain
    obfuscated_gaiaid = pbval.uservalue.obfuscated_gaiaid

    federated_identity = None
    if pbval.uservalue.HasField('federated_identity'):
      federated_identity = pbval.uservalue.federated_identity



    value = users.User(email=email,
                       _auth_domain=auth_domain,
                       _user_id=obfuscated_gaiaid,
                       federated_identity=federated_identity,
                       _strict_mode=False)
  else:
    value = None

  try:
    if pb.HasField('meaning') and meaning in _PROPERTY_CONVERSIONS:
      conversion = _PROPERTY_CONVERSIONS[meaning]
      value = conversion(value)
      if (meaning == entity_pb2.Property.BLOB and pb.HasField('meaning_uri')):
        value.meaning_uri = pb.meaning_uri
  except (KeyError, ValueError, IndexError, TypeError, AttributeError) as msg:
    raise datastore_errors.BadValueError(
      'Error converting pb: %s\nException was: %s' % (pb, msg))

  return value


def RestoreFromIndexValue(index_value, data_type):
  """Restores an index value to the correct datastore type.

  Projection queries return property values directly from a datastore index.
  These values are the native datastore values that can be one of the following:
  `str`, `bool`, `long`, `float`, `GeoPt`, `Key`, or `User`. This function
  restores the original value when the original type is known.

  This function returns the value type returned when decoding a normal entity,
  not necessarily of type `data_type`. For example, `data_type=int` returns a
  `long` instance.

  Args:
    index_value: The value returned by `FromPropertyPb` for the projected
      property.
    data_type: The type of the value originally given to `ToPropertyPb`.

  Returns:
    The restored property value.

  Raises:
    `datastore_errors.BadValueError` if the value cannot be restored.
  """
  raw_type = _PROPERTY_TYPE_TO_INDEX_VALUE_TYPE.get(data_type)
  if raw_type is None:
    raise datastore_errors.BadValueError(
        'Unsupported data type (%r)' % data_type)

  if index_value is None:
    return index_value



  if not isinstance(index_value, raw_type):
    raise datastore_errors.BadValueError(
        'Unsupported conversion. Expected %r got %r' %
        (type(index_value), raw_type))

  meaning = _PROPERTY_MEANINGS.get(data_type)


  if isinstance(index_value, bytes) and meaning not in _NON_UTF8_MEANINGS:
    index_value = six.text_type(index_value, 'utf-8')


  conv = _PROPERTY_CONVERSIONS.get(meaning)
  if not conv:
    return index_value

  try:
    value = conv(index_value)
  except (KeyError, ValueError, IndexError, TypeError, AttributeError) as msg:
    raise datastore_errors.BadValueError(
      'Error converting value: %r\nException was: %s' % (index_value, msg))
  return value


def PropertyTypeName(value):
  """Returns the type name of the given property value, as a string.

  Raises `BadValueError` if the value is not a valid property type.

  Args:
    value: Any valid property value.

  Returns:
    String.
  """
  if value.__class__ in _PROPERTY_MEANINGS:
    meaning = _PROPERTY_MEANINGS[value.__class__]
    name = entity_pb2.Property.Meaning.DESCRIPTOR.values_by_number[meaning].name
    return name.lower().replace('_', ':')
  elif isinstance(value, six.string_types):
    return 'string'
  elif isinstance(value, users.User):
    return 'user'
  elif isinstance(value, bool):
    return 'bool'
  elif isinstance(value, _PREFERRED_NUM_TYPE):
    return 'int'
  elif value is None:
    return 'null'
  else:
    return typename(value).lower()


_PROPERTY_TYPE_STRINGS = {
    'string': six.text_type,
    'bool': bool,
    'int': _PREFERRED_NUM_TYPE,
    'null': type(None),
    'float': float,
    'key': Key,
    'blob': Blob,
    'entity:proto': EmbeddedEntity,
    'bytestring': ByteString,
    'text': Text,
    'user': users.User,
    'atom:category': Category,
    'atom:link': Link,
    'gd:email': Email,
    'gd:when': datetime.datetime,
    'georss:point': GeoPt,
    'gd:im': IM,
    'gd:phonenumber': PhoneNumber,
    'gd:postaladdress': PostalAddress,
    'gd:rating': Rating,
    'blobkey': BlobKey,
}


def FromPropertyTypeName(type_name):
  """Returns the python type given a type name.

  Args:
    type_name: A string representation of a datastore type name.

  Returns:
    A Python type.
  """
  return _PROPERTY_TYPE_STRINGS[type_name]


def PropertyValueFromString(type_,
                            value_string,
                            _auth_domain=None):
  """Returns an instance of a property value given a type and string value.

  The reverse of this method is just `str()` and `type()` of the Python value.

  Note that this does *not* support non-UTC offsets in ISO 8601-formatted
  datetime strings, e.g., the `-08:00` suffix in `2002-12-25 00:00:00-08:00`.
  It only supports `-00:00` and `+00:00` suffixes, which are UTC.

  Args:
    type_: A Python class.
    value_string: A string representation of the value of the property.

  Returns:
    An instance of `type`.

  Raises:
    `ValueError` if `type_` is datetime and `value_string` has a timezone
    offset.
  """
  if type_ == datetime.datetime:
    value_string = value_string.strip()

    if value_string[-6] in ('+', '-'):
      if value_string[-5:] == '00:00':
        value_string = value_string[:-6]
      else:

        raise ValueError('Non-UTC offsets in datetimes are not supported.')


    split = value_string.split('.')
    iso_date = split[0]
    microseconds = 0
    if len(split) > 1:
      microseconds = int(split[1])



    time_struct = time.strptime(iso_date, '%Y-%m-%d %H:%M:%S')[0:6]
    value = datetime.datetime(*(time_struct + (microseconds,)))
    return value
  elif type_ == Rating:

    return Rating(int(value_string))
  elif type_ == bool:
    return value_string == 'True'
  elif type_ == users.User:
    return users.User(value_string, _auth_domain)
  elif type_ == type(None):
    return None
  elif type_ in (Blob, EmbeddedEntity, ByteString):
    return type_(value_string.encode('utf-8'))
  return type_(value_string)


def ReferenceToKeyValue(key, id_resolver=None):
  """Converts a key into a comparable hashable `key` value.

  Args:
    key: The `entity_pb2.Reference` or `googledatastore.Key` from which to
        construct the key value.
    id_resolver: An optional `datastore_pbs.IdResolver`. Only necessary for
        `googledatastore.Key` values.
  Returns:
    A comparable and hashable representation of the given key that is
    compatible with one derived from a key property value.
  """
  if (datastore_pbs._CLOUD_DATASTORE_ENABLED
      and isinstance(key, googledatastore.Key)):
    v1_key = key
    key = entity_pb2.Reference()
    datastore_pbs.get_entity_converter(id_resolver).v1_to_v3_reference(v1_key,
                                                                       key)
  elif isinstance(key, entity_v4_pb2.Key):
    v4_key = key
    key = entity_pb2.Reference()
    datastore_pbs.get_entity_converter().v4_to_v3_reference(v4_key, key)

  if isinstance(key, entity_pb2.Reference):
    element_list = key.path.element
  elif isinstance(key, entity_pb2.PropertyValue.ReferenceValue):
    element_list = key.pathelement
  else:
    raise datastore_errors.BadArgumentError(
        'key arg expected to be entity_pb2.Reference or googledatastore.Key (%r)'
        % (key,))

  result = [
      entity_pb2.PropertyValue.REFERENCEVALUE_FIELD_NUMBER, key.app,
      key.name_space
  ]
  for element in element_list:
    result.append(element.type)
    if element.HasField('name'):
      result.append(element.name)
    else:
      result.append(element.id)
  return tuple(result)




def _isFloatNegative(value, encoded):
  if value == 0:
    return encoded[0] == 128
  return value < 0



def _encodeDoubleSortably(value):
  """Encode a double into a sortable byte buffer."""

  encoded = array.array('B')
  encoded.fromstring(struct.pack('>d', value))
  if _isFloatNegative(value, encoded):


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


def PropertyValueToKeyValue(prop_value):
  """Converts an `entity_pb2.PropertyValue` into a comparable hashable `key` value.

  The values produces by this function mimic the native ordering of the
  datastore and uniquely identify the given `PropertyValue`.

  Args:
    prop_value: The `entity_pb2.PropertyValue` from which to construct the key
      value.

  Returns:
    A comparable and hashable representation of the given property value.
  """
  if not isinstance(prop_value, entity_pb2.PropertyValue):
    raise datastore_errors.BadArgumentError(
        'prop_value arg expected to be entity_pb2.PropertyValue (%r)' %
        (prop_value,))



  if prop_value.HasField('stringValue'):
    return (entity_pb2.PropertyValue.STRINGVALUE_FIELD_NUMBER,
            prop_value.stringValue)
  if prop_value.HasField('int64Value'):
    return (entity_pb2.PropertyValue.INT64VALUE_FIELD_NUMBER,
            prop_value.int64Value)
  if prop_value.HasField('booleanValue'):
    return (entity_pb2.PropertyValue.BOOLEANVALUE_FIELD_NUMBER,
            prop_value.booleanValue)
  if prop_value.HasField('doubleValue'):

    return (entity_pb2.PropertyValue.DOUBLEVALUE_FIELD_NUMBER,
            tuple(sortable_pb_encoder.EncodeDouble(prop_value.doubleValue)))
  if prop_value.HasField('pointvalue'):
    return (entity_pb2.PropertyValue.POINTVALUE_FIELD_NUMBER,
            prop_value.pointvalue.x, prop_value.pointvalue.y)
  if prop_value.HasField('referencevalue'):
    return ReferenceToKeyValue(prop_value.referencevalue)
  if prop_value.HasField('uservalue'):
    result = []
    uservalue = prop_value.uservalue
    if uservalue.HasField('email'):
      result.append((entity_pb2.PropertyValue.UserValue.EMAIL_FIELD_NUMBER,
                     uservalue.email))
    if uservalue.HasField('auth_domain'):
      result.append(
          (entity_pb2.PropertyValue.UserValue.AUTH_DOMAIN_FIELD_NUMBER,
           uservalue.auth_domain))
    if uservalue.HasField('nickname'):
      result.append((entity_pb2.PropertyValue.UserValue.NICKNAME_FIELD_NUMBER,
                     uservalue.nickname))
    if uservalue.HasField('gaiaid'):
      result.append((entity_pb2.PropertyValue.UserValue.GAIAID_FIELD_NUMBER,
                     uservalue.gaiaid))
    if uservalue.HasField('obfuscated_gaiaid'):
      result.append(
          (entity_pb2.PropertyValue.UserValue.OBFUSCATED_GAIAID_FIELD_NUMBER,
           uservalue.obfuscated_gaiaid))
    if uservalue.HasField('federated_identity'):
      result.append(
          (entity_pb2.PropertyValue.UserValue.FEDERATED_IDENTITY_FIELD_NUMBER,
           uservalue.federated_identity))
    if uservalue.HasField('federated_provider'):
      result.append(
          (entity_pb2.PropertyValue.UserValue.FEDERATED_PROVIDER_FIELD_NUMBER,
           uservalue.federated_provider))
    result.sort()
    return (entity_pb2.PropertyValue.USERVALUE_FIELD_NUMBER, tuple(result))
  return ()


def GetPropertyValueTag(value_pb):
  """Returns the tag constant associated with the given `entity_pb2.PropertyValue`."""
  if value_pb.HasField('booleanValue'):
    return entity_pb2.PropertyValue.BOOLEANVALUE_FIELD_NUMBER
  elif value_pb.HasField('doubleValue'):
    return entity_pb2.PropertyValue.DOUBLEVALUE_FIELD_NUMBER
  elif value_pb.HasField('int64Value'):
    return entity_pb2.PropertyValue.INT64VALUE_FIELD_NUMBER
  elif value_pb.HasField('pointvalue'):
    return entity_pb2.PropertyValue.POINTVALUE_FIELD_NUMBER
  elif value_pb.HasField('referencevalue'):
    return entity_pb2.PropertyValue.REFERENCEVALUE_FIELD_NUMBER
  elif value_pb.HasField('stringValue'):
    return entity_pb2.PropertyValue.STRINGVALUE_FIELD_NUMBER
  elif value_pb.HasField('uservalue'):
    return entity_pb2.PropertyValue.USERVALUE_FIELD_NUMBER
  else:
    return 0
