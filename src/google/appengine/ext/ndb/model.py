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
















"""Model and Property classes and associated stuff.

A model class represents the structure of entities stored in the
datastore.  Applications define model classes to indicate the
structure of their entities, then instantiate those model classes
to create entities.

All model classes must inherit (directly or indirectly) from Model.
Through the magic of metaclasses, straightforward assignments in the
model class definition can be used to declare the model's structure::

  class Person(Model):
    name = StringProperty()
    age = IntegerProperty()

We can now create a Person entity and write it to Cloud Datastore::

  p = Person(name='Arthur Dent', age=42)
  k = p.put()

The return value from put() is a Key (see the documentation for
ndb/key.py), which can be used to retrieve the same entity later::

  p2 = k.get()
  p2 == p  # Returns True

To update an entity, simple change its attributes and write it back
(note that this doesn't change the key)::

  p2.name = 'Arthur Philip Dent'
  p2.put()

We can also delete an entity (by using the key)::

  k.delete()

The property definitions in the class body tell the system the names
and the types of the fields to be stored in Cloud Datastore, whether
they must be indexed, their default value, and more.

Many different Property types exist.  Most are indexed by default, the
exceptions indicated in the list below:

- StringProperty: a short text string, limited to 500 bytes

- TextProperty: an unlimited text string; unindexed

- BlobProperty: an unlimited byte string; unindexed

- IntegerProperty: a 64-bit signed integer

- FloatProperty: a double precision floating point number

- BooleanProperty: a bool value

- DateTimeProperty: a datetime object.  Note: App Engine always uses
  UTC as the timezone

- DateProperty: a date object

- TimeProperty: a time object

- GeoPtProperty: a geographical location, i.e. (latitude, longitude)

- KeyProperty: a Cloud Datastore Key value, optionally constrained to
  referring to a specific kind

- UserProperty: a User object (for backwards compatibility only)

- StructuredProperty: a field that is itself structured like an
  entity; see below for more details

- LocalStructuredProperty: like StructuredProperty but the on-disk
  representation is an opaque blob; unindexed

- ComputedProperty: a property whose value is computed from other
  properties by a user-defined function.  The property value is
  written to Cloud Datastore so that it can be used in queries, but the
  value from Cloud Datastore is not used when the entity is read back

- GenericProperty: a property whose type is not constrained; mostly
  used by the Expando class (see below) but also usable explicitly

- JsonProperty: a property whose value is any object that can be
  serialized using JSON; the value written to Cloud Datastore is a JSON
  representation of that object

- PickleProperty: a property whose value is any object that can be
  serialized using Python's pickle protocol; the value written to the
  Cloud Datastore is the pickled representation of that object, using the
  highest available pickle protocol

Most Property classes have similar constructor signatures.  They
accept several optional keyword arguments:

- name=<string>: the name used to store the property value in the
  datastore.  Unlike the following options, this may also be given as
  a positional argument

- indexed=<bool>: indicates whether the property should be indexed
  (allowing queries on this property's value)

- repeated=<bool>: indicates that this property can have multiple
  values in the same entity.

- write_empty_list<bool>: For repeated value properties, controls
  whether properties with no elements (the empty list) is
  written to Datastore. If true, written, if false, then nothing
  is written to Datastore.

- required=<bool>: indicates that this property must be given a value

- default=<value>: a default value if no explicit value is given

- choices=<list of values>: a list or tuple of allowable values

- validator=<function>: a general-purpose validation function.  It
  will be called with two arguments (prop, value) and should either
  return the validated value or raise an exception.  It is also
  allowed for the function to modify the value, but calling it again
  on the modified value should not modify the value further.  (For
  example: a validator that returns value.strip() or value.lower() is
  fine, but one that returns value + '$' is not.)

- verbose_name=<value>: A human readable name for this property.  This
  human readable name can be used for html form labels.

The repeated and required/default options are mutually exclusive: a
repeated property cannot be required nor can it specify a default
value (the default is always an empty list and an empty list is always
an allowed value), but a required property can have a default.

Some property types have additional arguments.  Some property types
do not support all options.

Repeated properties are always represented as Python lists; if there
is only one value, the list has only one element.  When a new list is
assigned to a repeated property, all elements of the list are
validated.  Since it is also possible to mutate lists in place,
repeated properties are re-validated before they are written to the
datastore.

No validation happens when an entity is read from Cloud Datastore;
however property values read that have the wrong type (e.g. a string
value for an IntegerProperty) are ignored.

For non-repeated properties, None is always a possible value, and no
validation is called when the value is set to None.  However for
required properties, writing the entity to Cloud Datastore requires
the value to be something other than None (and valid).

The StructuredProperty is different from most other properties; it
lets you define a sub-structure for your entities.  The substructure
itself is defined using a model class, and the attribute value is an
instance of that model class.  However it is not stored in the
datastore as a separate entity; instead, its attribute values are
included in the parent entity using a naming convention (the name of
the structured attribute followed by a dot followed by the name of the
subattribute).  For example::

  class Address(Model):
    street = StringProperty()
    city = StringProperty()

  class Person(Model):
    name = StringProperty()
    address = StructuredProperty(Address)

  p = Person(name='Harry Potter',
             address=Address(street='4 Privet Drive',
                             city='Little Whinging'))
  k.put()

This would write a single 'Person' entity with three attributes (as
you could verify using the Datastore Viewer in the Admin Console)::

  name = 'Harry Potter'
  address.street = '4 Privet Drive'
  address.city = 'Little Whinging'

Structured property types can be nested arbitrarily deep, but in a
hierarchy of nested structured property types, only one level can have
the repeated flag set.  It is fine to have multiple structured
properties referencing the same model class.

It is also fine to use the same model class both as a top-level entity
class and as for a structured property; however queries for the model
class will only return the top-level entities.

The LocalStructuredProperty works similar to StructuredProperty on the
Python side.  For example::

  class Address(Model):
    street = StringProperty()
    city = StringProperty()

  class Person(Model):
    name = StringProperty()
    address = LocalStructuredProperty(Address)

  p = Person(name='Harry Potter',
             address=Address(street='4 Privet Drive',
                             city='Little Whinging'))
  k.put()

However the data written to Cloud Datastore is different; it writes a
'Person' entity with a 'name' attribute as before and a single
'address' attribute whose value is a blob which encodes the Address
value (using the standard"protocol buffer" encoding).

Sometimes the set of properties is not known ahead of time.  In such
cases you can use the Expando class.  This is a Model subclass that
creates properties on the fly, both upon assignment and when loading
an entity from Cloud Datastore.  For example::

  class SuperPerson(Expando):
    name = StringProperty()
    superpower = StringProperty()

  razorgirl = SuperPerson(name='Molly Millions',
                          superpower='bionic eyes, razorblade hands',
                          rasta_name='Steppin\' Razor',
                          alt_name='Sally Shears')
  elastigirl = SuperPerson(name='Helen Parr',
                           superpower='stretchable body')
  elastigirl.max_stretch = 30  # Meters

You can inspect the properties of an expando instance using the
_properties attribute:

  >>> print razorgirl._properties.keys()
  ['rasta_name', 'name', 'superpower', 'alt_name']
  >>> print elastigirl._properties
  {'max_stretch': GenericProperty('max_stretch'),
   'name': StringProperty('name'),
   'superpower': StringProperty('superpower')}

Note: this property exists for plain Model instances too; it is just
not as interesting for those.

The Model class offers basic query support.  You can create a Query
object by calling the query() class method.  Iterating over a Query
object returns the entities matching the query one at a time.

Query objects are fully described in the docstring for query.py, but
there is one handy shortcut that is only available through
Model.query(): positional arguments are interpreted as filter
expressions which are combined through an AND operator.  For example::

  Person.query(Person.name == 'Harry Potter', Person.age >= 11)

is equivalent to::

  Person.query().filter(Person.name == 'Harry Potter', Person.age >= 11)

Keyword arguments passed to .query() are passed along to the Query()
constructor.

It is possible to query for field values of structured properties.  For
example::

  qry = Person.query(Person.address.city == 'London')

A number of top-level functions also live in this module:

- transaction() runs a function inside a transaction
- get_multi() reads multiple entities at once
- put_multi() writes multiple entities at once
- delete_multi() deletes multiple entities at once

All these have a corresponding ``*_async()`` variant as well.
The ``*_multi_async()`` functions return a list of Futures.

And finally these (without async variants):

- in_transaction() tests whether you are currently running in a transaction
- @transactional decorates functions that should be run in a transaction

There are many other interesting features.  For example, Model
subclasses may define pre-call and post-call hooks for most operations
(get, put, delete, allocate_ids), and Property classes may be
subclassed to suit various needs.  Documentation for writing a
Property subclass is in the docstring for the Property class.
"""

import collections
import copy
import datetime
import logging
import os
import zlib

from google.appengine.ext.ndb import key as key_module
from google.appengine.ext.ndb import utils
import six
from six.moves import map
import six.moves.cPickle as pickle

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.api import users
from google.appengine.datastore import datastore_query
from google.appengine.datastore import datastore_rpc
from google.appengine.datastore import entity_bytes_pb2 as entity_pb2



Key = key_module.Key


__all__ = ['Key', 'BlobKey', 'GeoPt', 'Rollback',
           'Index', 'IndexState', 'IndexProperty',
           'ModelAdapter', 'ModelAttribute',
           'ModelKey', 'MetaModel', 'Model', 'Expando',
           'transaction', 'transaction_async', 'in_transaction',
           'transactional', 'transactional_async', 'transactional_tasklet',
           'non_transactional',
           'get_multi', 'get_multi_async',
           'put_multi', 'put_multi_async',
           'delete_multi', 'delete_multi_async',
           'get_indexes', 'get_indexes_async',
           'make_connection',
          ]


BlobKey = datastore_types.BlobKey
GeoPt = datastore_types.GeoPt

Rollback = datastore_errors.Rollback


class KindError(datastore_errors.BadValueError):
  """Raised when an implementation for a kind can't be found.

  Also raised when the Kind is not an 8-bit string.
  """


class InvalidPropertyError(datastore_errors.Error):
  """Raised when a property is not applicable to a given use.

  For example, a property must exist and be indexed to be used in a query's
  projection or group by clause.
  """


BadProjectionError = InvalidPropertyError


class UnprojectedPropertyError(datastore_errors.Error):
  """Raised when getting a property value that's not in the projection."""


class ReadonlyPropertyError(datastore_errors.Error):
  """Raised when attempting to set a property value that is read-only."""


class ComputedPropertyError(ReadonlyPropertyError):
  """Raised when attempting to set a value to or delete a computed property."""



_MAX_LONG = key_module._MAX_LONG
_MAX_STRING_LENGTH = datastore_types._MAX_STRING_LENGTH


_DIR_MAP = {
    entity_pb2.Index.Property.ASCENDING: 'asc',
    entity_pb2.Index.Property.DESCENDING: 'desc',
}


_STATE_MAP = {
    entity_pb2.CompositeIndex.ERROR: 'error',
    entity_pb2.CompositeIndex.DELETED: 'deleting',
    entity_pb2.CompositeIndex.READ_WRITE: 'serving',
    entity_pb2.CompositeIndex.WRITE_ONLY: 'building',
}


class _NotEqualMixin(object):
  """Mix-in class that implements __ne__ in terms of __eq__."""

  def __ne__(self, other):
    """Implement self != other as not(self == other)."""
    eq = self.__eq__(other)
    if eq is NotImplemented:
      return NotImplemented
    return not eq


class _NestedCounter(object):
  """ A recursive counter for StructuredProperty deserialization.

  Deserialization has some complicated rules to handle StructuredPropertys
  that may or may not be empty. The simplest case is a leaf counter, where
  the counter will return the index of the repeated value that last had this
  leaf property written. When a non-leaf counter requested, this will return
  the max of all its leaf values. This is due to the fact that the next index
  that a full non-leaf property may be written to comes after all indices that
  have part of that property written (otherwise, a partial entity would be
  overwritten.

  Consider an evaluation of the following structure:
    class B(model.Model):
      c = model.IntegerProperty()
      d = model.IntegerProperty()

    class A(model.Model):
      b = model.StructuredProperty(B)

    class Foo(model.Model):
      # top-level model
      a = model.StructuredProperty(A, repeated=True)

    Foo(a=[A(b=None),
           A(b=B(c=1)),
           A(b=None),
           A(b=B(c=2, d=3))])

  This will result in a serialized structure:

  1) a.b   = None
  2) a.b.c = 1
  3) a.b.d = None
  4) a.b   = None
  5) a.b.c = 2
  6) a.b.d = 3

  The counter state should be the following:
     a | a.b | a.b.c | a.b.d
  0) -    -      -       -
  1) @1   1      -       -
  2) @2   @2     2       -
  3) @2   @2     2       2
  4) @3   @3     3       3
  5) @4   @4     4       3
  6) @4   @4     4       4

  Here, @ indicates that this counter value is actually a calculated value.
  It is equal to the MAX of its sub-counters.

  Counter values may get incremented multiple times while deserializing a
  property. This will happen if a child counter falls behind,
  for example in steps 2 and 3.

  During an increment of a parent node, all child nodes values are incremented
  to match that of the parent, for example in step 4.
  """

  def __init__(self):
    self.__counter = 0
    self.__sub_counters = collections.defaultdict(_NestedCounter)

  def get(self, parts=None):
    if parts:
      return self.__sub_counters[parts[0]].get(parts[1:])
    if self.__is_parent_node():
      return max(v.get() for v in six.itervalues(self.__sub_counters))
    return self.__counter

  def increment(self, parts=None):
    if parts:
      self.__make_parent_node()
      return self.__sub_counters[parts[0]].increment(parts[1:])
    if self.__is_parent_node():

      value = self.get() + 1
      self._set(value)
      return value
    self.__counter += 1
    return self.__counter

  def _set(self, value):
    """Updates all descendants to a specified value."""
    if self.__is_parent_node():
      for child in six.itervalues(self.__sub_counters):
        child._set(value)
    else:
      self.__counter = value

  def _absolute_counter(self):

    return self.__counter

  def __is_parent_node(self):
    return self.__counter == -1

  def __make_parent_node(self):
    self.__counter = -1


class IndexProperty(_NotEqualMixin):
  """Immutable object representing a single property in an index."""

  @utils.positional(1)
  def __new__(cls, name, direction):
    """Constructor."""
    obj = object.__new__(cls)
    obj.__name = name
    obj.__direction = direction
    return obj

  @property
  def name(self):
    """The property name being indexed, a string."""
    return self.__name

  @property
  def direction(self):
    """The direction in the index for this property, 'asc' or 'desc'."""
    return self.__direction

  def __repr__(self):
    """Return a string representation."""
    return '%s(name=%r, direction=%r)' % (self.__class__.__name__,
                                          self.name,
                                          self.direction)

  def __eq__(self, other):
    """Compare two index properties for equality."""
    if not isinstance(other, IndexProperty):
      return NotImplemented
    return self.name == other.name and self.direction == other.direction

  def __hash__(self):
    return hash((self.name, self.direction))


class Index(_NotEqualMixin):
  """Immutable object representing an index."""

  @utils.positional(1)
  def __new__(cls, kind, properties, ancestor):
    """Constructor."""
    obj = object.__new__(cls)
    obj.__kind = kind
    obj.__properties = properties
    obj.__ancestor = ancestor
    return obj

  @property
  def kind(self):
    """The kind being indexed, a string."""
    return self.__kind

  @property
  def properties(self):
    """A list of PropertyIndex objects giving the properties being indexed."""
    return self.__properties

  @property
  def ancestor(self):
    """Whether this is an ancestor index, a bool."""
    return self.__ancestor

  def __repr__(self):
    """Return a string representation."""
    parts = []
    parts.append('kind=%r' % self.kind)
    parts.append('properties=%r' % self.properties)
    parts.append('ancestor=%s' % self.ancestor)
    return '%s(%s)' % (self.__class__.__name__, ', '.join(parts))

  def __eq__(self, other):
    """Compare two indexes."""
    if not isinstance(other, Index):
      return NotImplemented
    return (self.kind == other.kind and
            self.properties == other.properties and
            self.ancestor == other.ancestor)

  def __hash__(self):
    return hash((self.kind, self.properties, self.ancestor))


class IndexState(_NotEqualMixin):
  """Immutable object representing and index and its state."""

  @utils.positional(1)
  def __new__(cls, definition, state, id):
    """Constructor."""
    obj = object.__new__(cls)
    obj.__definition = definition
    obj.__state = state
    obj.__id = id
    return obj

  @property
  def definition(self):
    """An Index object describing the index."""
    return self.__definition

  @property
  def state(self):
    """The index state, a string.

    Possible values are 'error', 'deleting', 'serving' or 'building'.
    """
    return self.__state

  @property
  def id(self):
    """The index ID, an integer."""
    return self.__id

  def __repr__(self):
    """Return a string representation."""
    parts = []
    parts.append('definition=%r' % self.definition)
    parts.append('state=%r' % self.state)
    parts.append('id=%d' % self.id)
    return '%s(%s)' % (self.__class__.__name__, ', '.join(parts))

  def __eq__(self, other):
    """Compare two index states."""
    if not isinstance(other, IndexState):
      return NotImplemented
    return (self.definition == other.definition and
            self.state == other.state and
            self.id == other.id)

  def __hash__(self):
    return hash((self.definition, self.state, self.id))


class ModelAdapter(datastore_rpc.AbstractAdapter):
  """Conversions between 'our' Key and Model classes and protobufs.

  This is needed to construct a Connection object, which in turn is
  needed to construct a Context object.

  See the base class docstring for more info about the signatures.
  """

  def __init__(self, default_model=None, id_resolver=None):
    """Constructor.

    Args:
      default_model: If an implementation for the kind cannot be found, use
        this model class.  If none is specified, an exception will be thrown
        (default).
      id_resolver: A datastore_pbs.IdResolver that can resolve
        application ids. This is only necessary when running on the Cloud
        Datastore v1 API.
    """


    try:
      super(ModelAdapter, self).__init__(id_resolver)
    except:
      pass
    self.default_model = default_model
    self.want_pbs = 0




  def __enter__(self):
    self.want_pbs += 1

  def __exit__(self, *unused_args):
    self.want_pbs -= 1

  def pb_to_key(self, pb):
    return Key(reference=pb)

  def key_to_pb(self, key):
    return key.reference()

  def pb_to_entity(self, pb):
    key = None
    kind = None
    if len(pb.key.path.element):
      key = Key(reference=pb.key)
      kind = key.kind()
    modelclass = Model._lookup_model(kind, self.default_model)
    entity = modelclass._from_pb(pb, key=key, set_key=False)
    if self.want_pbs:
      entity._orig_pb = pb
    return entity

  def entity_to_pb(self, ent):
    pb = ent._to_pb()
    return pb

  def pb_to_index(self, pb):
    index_def = pb.definition
    properties = [
        IndexProperty(name=prop.name, direction=_DIR_MAP[prop.direction])
        for prop in index_def.property
    ]
    index = Index(
        kind=index_def.entity_type,
        properties=properties,
        ancestor=bool(index_def.ancestor),
    )
    index_state = IndexState(
        definition=index,
        state=_STATE_MAP[pb.state],
        id=pb.id,
    )
    return index_state


def make_connection(config=None, default_model=None,
                    _api_version=datastore_rpc._DATASTORE_V3,
                    _id_resolver=None):
  """Create a new Connection object with the right adapter.

  Optionally you can pass in a datastore_rpc.Configuration object.
  """
  return datastore_rpc.Connection(
      adapter=ModelAdapter(default_model, id_resolver=_id_resolver),
      config=config,
      _api_version=_api_version)


class ModelAttribute(object):
  """A Base class signifying the presence of a _fix_up() method."""

  def _fix_up(self, cls, code_name):
    pass


class _BaseValue(_NotEqualMixin):
  """A marker object wrapping a 'base type' value.

  This is used to be able to tell whether ent._values[name] is a
  user value (i.e. of a type that the Python code understands) or a
  base value (i.e of a type that serialization understands).
  User values are unwrapped; base values are wrapped in a
  _BaseValue instance.
  """

  __slots__ = ['b_val']

  def __init__(self, b_val):
    """Constructor.  Argument is the base value to be wrapped."""
    assert b_val is not None, "Cannot wrap None"
    assert not isinstance(b_val, list), repr(b_val)
    self.b_val = b_val

  def __repr__(self):
    return '_BaseValue(%r)' % (self.b_val,)

  def __eq__(self, other):
    if not isinstance(other, _BaseValue):
      return NotImplemented
    return self.b_val == other.b_val

  def __hash__(self):
    raise TypeError('_BaseValue is not immutable')


class Property(ModelAttribute):
  """A class describing a typed, persisted attribute of a Cloud Datastore entity.

  Not to be confused with Python's 'property' built-in.

  This is just a base class; there are specific subclasses that
  describe Properties of various types (and GenericProperty which
  describes a dynamically typed Property).

  All special Property attributes, even those considered 'public',
  have names starting with an underscore, because StructuredProperty
  uses the non-underscore attribute namespace to refer to nested
  Property names; this is essential for specifying queries on
  subproperties (see the module docstring).

  The Property class and its predefined subclasses allow easy
  subclassing using composable (or stackable) validation and
  conversion APIs.  These require some terminology definitions:

  - A 'user value' is a value such as would be set and accessed by the
    application code using standard attributes on the entity.

  - A 'base value' is a value such as would be serialized to
    and deserialized from Cloud Datastore.

  The values stored in ent._values[name] and accessed by
  _store_value() and _retrieve_value() can be either user values or
  base values.  To retrieve user values, use
  _get_user_value().  To retrieve base values, use
  _get_base_value().  In particular, _get_value() calls
  _get_user_value(), and _serialize() effectively calls
  _get_base_value().

  To store a user value, just call _store_value().  To store a
  base value, wrap the value in a _BaseValue() and then
  call _store_value().

  A Property subclass that wants to implement a specific
  transformation between user values and serialiazble values should
  implement two methods, _to_base_type() and _from_base_type().
  These should *NOT* call their super() method; super calls are taken
  care of by _call_to_base_type() and _call_from_base_type().
  This is what is meant by composable (or stackable) APIs.

  The API supports 'stacking' classes with ever more sophisticated
  user<-->base conversions: the user-->base conversion
  goes from more sophisticated to less sophisticated, while the
  base-->user conversion goes from less sophisticated to more
  sophisticated.  For example, see the relationship between
  BlobProperty, TextProperty and StringProperty.

  In addition to _to_base_type() and _from_base_type(), the
  _validate() method is also a composable API.

  The validation API distinguishes between 'lax' and 'strict' user
  values.  The set of lax values is a superset of the set of strict
  values.  The _validate() method takes a lax value and if necessary
  converts it to a strict value.  This means that when setting the
  property value, lax values are accepted, while when getting the
  property value, only strict values will be returned.  If no
  conversion is needed, _validate() may return None.  If the argument
  is outside the set of accepted lax values, _validate() should raise
  an exception, preferably TypeError or
  datastore_errors.BadValueError.

  Example/boilerplate:

  def _validate(self, value):
    'Lax user value to strict user value.'
    if not isinstance(value, <top type>):
      raise TypeError(...)  # Or datastore_errors.BadValueError(...).

  def _to_base_type(self, value):
    '(Strict) user value to base value.'
    if isinstance(value, <user type>):
      return <base type>(value)

  def _from_base_type(self, value):
    'base value to (strict) user value.'
    if not isinstance(value, <base type>):
      return <user type>(value)

  Things that _validate(), _to_base_type() and _from_base_type()
  do *not* need to handle:

  - None: They will not be called with None (and if they return None,
    this means that the value does not need conversion).

  - Repeated values: The infrastructure (_get_user_value() and
    _get_base_value()) takes care of calling
    _from_base_type() or _to_base_type() for each list item in a
    repeated value.

  - Wrapping values in _BaseValue(): The wrapping and unwrapping is
    taken care of by the infrastructure that calls the composable APIs.

  - Comparisons: The comparison operations call _to_base_type() on
    their operand.

  - Distinguishing between user and base values: the
    infrastructure guarantees that _from_base_type() will be called
    with an (unwrapped) base value, and that
    _to_base_type() will be called with a user value.

  - Returning the original value: if any of these return None, the
    original value is kept.  (Returning a differen value not equal to
    None will substitute the different value.)
  """



  _code_name = None
  _name = None
  _indexed = True
  _repeated = False
  _required = False
  _default = None
  _choices = None
  _validator = None
  _verbose_name = None
  _write_empty_list = False

  __creation_counter_global = 0

  _attributes = ['_name', '_indexed', '_repeated', '_required', '_default',
                 '_choices', '_validator', '_verbose_name',
                 '_write_empty_list']
  _positional = 1

  @utils.positional(1 + _positional)
  def __init__(self, name=None, indexed=None, repeated=None,
               required=None, default=None, choices=None, validator=None,
               verbose_name=None, write_empty_list=None):
    """Constructor.  For arguments see the module docstring."""
    if name is not None:
      if isinstance(name, six.text_type):
        name = six.ensure_binary(name)
      if not isinstance(name, six.binary_type):
        raise TypeError('Name %r is not a string' % (name,))
      if b'.' in name:
        raise ValueError('Name %r cannot contain period characters' % (name,))
      self._name = name
    if indexed is not None:
      self._indexed = indexed
    if repeated is not None:
      self._repeated = repeated
    if required is not None:
      self._required = required
    if default is not None:

      self._default = default
    if verbose_name is not None:
      self._verbose_name = verbose_name
    if write_empty_list is not None:
      self._write_empty_list = write_empty_list
    if self._repeated and (self._required or self._default is not None):
      raise ValueError('repeated is incompatible with required or default')
    if choices is not None:
      if not isinstance(choices, (list, tuple, set, frozenset)):
        raise TypeError('choices must be a list, tuple or set; received %r' %
                        choices)

      self._choices = frozenset(choices)
    if validator is not None:







      if not hasattr(validator, '__call__'):
        raise TypeError('validator must be callable or None; received %r' %
                        validator)
      self._validator = validator

    Property.__creation_counter_global += 1
    self._creation_counter = Property.__creation_counter_global

  def __repr__(self):
    """Return a compact unambiguous string representation of a property."""
    args = []
    cls = self.__class__
    for i, attr in enumerate(self._attributes):
      val = getattr(self, attr)
      if val is not getattr(cls, attr):
        if isinstance(val, type):
          s = val.__name__
        else:
          s = repr(val)
        if i >= cls._positional:
          if attr.startswith('_'):
            attr = attr[1:]
          s = '%s=%s' % (attr, s)
        args.append(s)
    s = '%s(%s)' % (self.__class__.__name__, ', '.join(args))
    return s

  def _datastore_type(self, value):
    """Internal hook used by property filters.

    Sometimes the low-level query interface needs a specific data type
    in order for the right filter to be constructed.  See _comparison().
    """
    return value

  def _comparison(self, op, value):
    """Internal helper for comparison operators.

    Args:
      op: The operator ('=', '<' etc.).

    Returns:
      A FilterNode instance representing the requested comparison.
    """

    if not self._indexed:
      raise datastore_errors.BadFilterError(
          'Cannot query for unindexed property %s' % self._name)
    from google.appengine.ext.ndb.query import FilterNode
    if value is not None:
      value = self._do_validate(value)
      value = self._call_to_base_type(value)
      value = self._datastore_type(value)
    return FilterNode(self._name, op, value)






  def __eq__(self, value):
    """Return a FilterNode instance representing the '=' comparison."""
    return self._comparison('=', value)

  def __ne__(self, value):
    """Return a FilterNode instance representing the '!=' comparison."""
    return self._comparison('!=', value)

  def __lt__(self, value):
    """Return a FilterNode instance representing the '<' comparison."""
    return self._comparison('<', value)

  def __le__(self, value):
    """Return a FilterNode instance representing the '<=' comparison."""
    return self._comparison('<=', value)

  def __gt__(self, value):
    """Return a FilterNode instance representing the '>' comparison."""
    return self._comparison('>', value)

  def __ge__(self, value):
    """Return a FilterNode instance representing the '>=' comparison."""
    return self._comparison('>=', value)


  def _IN(self, value):
    """Comparison operator for the 'in' comparison operator.

    The Python 'in' operator cannot be overloaded in the way we want
    to, so we define a method.  For example::

      Employee.query(Employee.rank.IN([4, 5, 6]))

    Note that the method is called ._IN() but may normally be invoked
    as .IN(); ._IN() is provided for the case you have a
    StructuredProperty with a model that has a Property named IN.
    """
    if not self._indexed:
      raise datastore_errors.BadFilterError(
          'Cannot query for unindexed property %s' % self._name)
    from google.appengine.ext.ndb.query import FilterNode
    if not isinstance(value, (list, tuple, set, frozenset)):
      raise datastore_errors.BadArgumentError(
          'Expected list, tuple or set, got %r' % (value,))
    values = []
    for val in value:
      if val is not None:
        val = self._do_validate(val)
        val = self._call_to_base_type(val)
        val = self._datastore_type(val)
      values.append(val)
    return FilterNode(self._name, 'in', values)
  IN = _IN

  def __neg__(self):
    """Return a descending sort order on this Property.

    For example::

      Employee.query().order(-Employee.rank)
    """
    return datastore_query.PropertyOrder(
        self._name, datastore_query.PropertyOrder.DESCENDING)

  def __pos__(self):
    """Return an ascending sort order on this Property.

    Note that this is redundant but provided for consistency with
    __neg__.  For example, the following two are equivalent::

      Employee.query().order(+Employee.rank)
      Employee.query().order(Employee.rank)
    """
    return datastore_query.PropertyOrder(self._name)

  def _do_validate(self, value):
    """Call all validations on the value.

    This calls the most derived _validate() method(s), then the custom
    validator function, and then checks the choices.  It returns the
    value, possibly modified in an idempotent way, or raises an
    exception.

    Note that this does not call all composable _validate() methods.
    It only calls _validate() methods up to but not including the
    first _to_base_type() method, when the MRO is traversed looking
    for _validate() and _to_base_type() methods.  (IOW if a class
    defines both _validate() and _to_base_type(), its _validate()
    is called and then the search is aborted.)

    Note that for a repeated Property this function should be called
    for each item in the list, not for the list as a whole.
    """
    if isinstance(value, _BaseValue):
      return value
    value = self._call_shallow_validation(value)
    if self._validator is not None:
      newvalue = self._validator(self, value)
      if newvalue is not None:
        value = newvalue
    if self._choices is not None:
      if value not in self._choices:
        raise datastore_errors.BadValueError(
            'Value %r for property %s is not an allowed choice' %
            (value, self._name))
    return value

  def _fix_up(self, cls, code_name):
    """Internal helper called to tell the property its name.

    This is called by _fix_up_properties() which is called by
    MetaModel when finishing the construction of a Model subclass.
    The name passed in is the name of the class attribute to which the
    Property is assigned (a.k.a. the code name).  Note that this means
    that each Property instance must be assigned to (at most) one
    class attribute.  E.g. to declare three strings, you must call
    StringProperty() three times, you cannot write

      foo = bar = baz = StringProperty()
    """
    self._code_name = code_name
    if self._name is None:
      self._name = six.ensure_binary(code_name)

  def _store_value(self, entity, value):
    """Internal helper to store a value in an entity for a Property.

    This assumes validation has already taken place.  For a repeated
    Property the value should be a list.
    """
    entity._values[self._name] = value

  def _set_value(self, entity, value):
    """Internal helper to set a value in an entity for a Property.

    This performs validation first.  For a repeated Property the value
    should be a list.
    """
    if entity._projection:
      raise ReadonlyPropertyError(
          'You cannot set property values of a projection entity')
    if self._repeated:
      if not isinstance(value, (list, tuple, set, frozenset)):
        raise datastore_errors.BadValueError('Expected list or tuple, got %r' %
                                             (value,))
      value = [self._do_validate(v) for v in value]
    else:
      if value is not None:
        value = self._do_validate(value)
    self._store_value(entity, value)

  def _has_value(self, entity, unused_rest=None):
    """Internal helper to ask if the entity has a value for this Property."""
    return self._name in entity._values

  def _retrieve_value(self, entity, default=None):
    """Internal helper to retrieve the value for this Property from an entity.

    This returns None if no value is set, or the default argument if
    given.  For a repeated Property this returns a list if a value is
    set, otherwise None.  No additional transformations are applied.
    """
    return entity._values.get(self._name, default)

  def _get_user_value(self, entity):
    """Return the user value for this property of the given entity.

    This implies removing the _BaseValue() wrapper if present, and
    if it is, calling all _from_base_type() methods, in the reverse
    method resolution order of the property's class.  It also handles
    default values and repeated properties.
    """
    return self._apply_to_values(entity, self._opt_call_from_base_type)

  def _get_base_value(self, entity):
    """Return the base value for this property of the given entity.

    This implies calling all _to_base_type() methods, in the method
    resolution order of the property's class, and adding a
    _BaseValue() wrapper, if one is not already present.  (If one
    is present, no work is done.)  It also handles default values and
    repeated properties.
    """
    return self._apply_to_values(entity, self._opt_call_to_base_type)


  def _get_base_value_unwrapped_as_list(self, entity):
    """Like _get_base_value(), but always returns a list.

    Returns:
      A new list of unwrapped base values.  For an unrepeated
      property, if the value is missing or None, returns [None]; for a
      repeated property, if the original value is missing or None or
      empty, returns [].
    """
    wrapped = self._get_base_value(entity)
    if self._repeated:
      if wrapped is None:
        return []
      assert isinstance(wrapped, list)
      return [w.b_val for w in wrapped]
    else:
      if wrapped is None:
        return [None]
      assert isinstance(wrapped, _BaseValue)
      return [wrapped.b_val]

  def _opt_call_from_base_type(self, value):
    """Call _from_base_type() if necessary.

    If the value is a _BaseValue instance, unwrap it and call all
    _from_base_type() methods.  Otherwise, return the value
    unchanged.
    """
    if isinstance(value, _BaseValue):
      value = self._call_from_base_type(value.b_val)
    return value

  def _value_to_repr(self, value):
    """Turn a value (base or not) into its repr().

    This exists so that property classes can override it separately.
    """



    val = self._opt_call_from_base_type(value)
    return repr(val)

  def _opt_call_to_base_type(self, value):
    """Call _to_base_type() if necessary.

    If the value is a _BaseValue instance, return it unchanged.
    Otherwise, call all _validate() and _to_base_type() methods and
    wrap it in a _BaseValue instance.
    """
    if not isinstance(value, _BaseValue):
      value = _BaseValue(self._call_to_base_type(value))
    return value

  def _call_from_base_type(self, value):
    """Call all _from_base_type() methods on the value.

    This calls the methods in the reverse method resolution order of
    the property's class.
    """
    methods = self._find_methods('_from_base_type', reverse=True)
    call = self._apply_list(methods)
    return call(value)

  def _call_to_base_type(self, value):
    """Call all _validate() and _to_base_type() methods on the value.

    This calls the methods in the method resolution order of the
    property's class.
    """
    methods = self._find_methods('_validate', '_to_base_type')
    call = self._apply_list(methods)
    return call(value)

  def _call_shallow_validation(self, value):
    """Call the initial set of _validate() methods.

    This is similar to _call_to_base_type() except it only calls
    those _validate() methods that can be called without needing to
    call _to_base_type().

    An example: suppose the class hierarchy is A -> B -> C ->
    Property, and suppose A defines _validate() only, but B and C
    define _validate() and _to_base_type().  The full list of
    methods called by _call_to_base_type() is::

      A._validate()
      B._validate()
      B._to_base_type()
      C._validate()
      C._to_base_type()

    This method will call A._validate() and B._validate() but not the
    others.
    """
    methods = []
    for method in self._find_methods('_validate', '_to_base_type'):
      if method.__name__ != '_validate':
        break
      methods.append(method)
    call = self._apply_list(methods)
    return call(value)

  @classmethod
  def _find_methods(cls, *names, **kwds):
    """Compute a list of composable methods.

    Because this is a common operation and the class hierarchy is
    static, the outcome is cached (assuming that for a particular list
    of names the reversed flag is either always on, or always off).

    Args:
      *names: One or more method names.
      reverse: Optional flag, default False; if True, the list is
        reversed.

    Returns:
      A list of callable class method objects.
    """
    reverse = kwds.pop('reverse', False)
    assert not kwds, repr(kwds)
    cache = cls.__dict__.get('_find_methods_cache')
    if cache:
      hit = cache.get(names)
      if hit is not None:
        return hit
    else:
      cls._find_methods_cache = cache = {}
    methods = []
    for c in cls.__mro__:
      for name in names:
        method = c.__dict__.get(name)
        if method is not None:
          methods.append(method)
    if reverse:
      methods.reverse()
    cache[names] = methods
    return methods

  def _apply_list(self, methods):
    """Return a single callable that applies a list of methods to a value.

    If a method returns None, the last value is kept; if it returns
    some other value, that replaces the last value.  Exceptions are
    not caught.
    """
    def call(value):
      for method in methods:
        newvalue = method(self, value)
        if newvalue is not None:
          value = newvalue
      return value
    return call

  def _apply_to_values(self, entity, function):
    """Apply a function to the property value/values of a given entity.

    This retrieves the property value, applies the function, and then
    stores the value back.  For a repeated property, the function is
    applied separately to each of the values in the list.  The
    resulting value or list of values is both stored back in the
    entity and returned from this method.
    """
    value = self._retrieve_value(entity, self._default)
    if self._repeated:
      if value is None:
        value = []
        self._store_value(entity, value)
      else:
        value[:] = list(map(function, value))
    else:
      if value is not None:
        newvalue = function(value)
        if newvalue is not None and newvalue is not value:
          self._store_value(entity, newvalue)
          value = newvalue
    return value

  def _get_value(self, entity):
    """Internal helper to get the value for this Property from an entity.

    For a repeated Property this initializes the value to an empty
    list if it is not set.
    """
    if entity._projection:




      if six.ensure_text(self._name) not in entity._projection:
        raise UnprojectedPropertyError(
            'Property %s is not in the projection' % (self._name,))
    return self._get_user_value(entity)

  def _delete_value(self, entity):
    """Internal helper to delete the value for this Property from an entity.

    Note that if no value exists this is a no-op; deleted values will
    not be serialized but requesting their value will return None (or
    an empty list in the case of a repeated Property).
    """
    if self._name in entity._values:
      del entity._values[self._name]

  def _is_initialized(self, entity):
    """Internal helper to ask if the entity has a value for this Property.

    This returns False if a value is stored but it is None.
    """
    return (not self._required or
            ((self._has_value(entity) or self._default is not None) and
             self._get_value(entity) is not None))

  def __get__(self, entity, unused_cls=None):
    """Descriptor protocol: get the value from the entity."""
    if entity is None:
      return self
    return self._get_value(entity)

  def __set__(self, entity, value):
    """Descriptor protocol: set the value on the entity."""
    self._set_value(entity, value)

  def __delete__(self, entity):
    """Descriptor protocol: delete the value from the entity."""
    self._delete_value(entity)

  def _serialize(self, entity, pb, prefix='', parent_repeated=False,
                 projection=None):
    """Internal helper to serialize this property to a protocol buffer.

    Subclasses may override this method.

    Args:
      entity: The entity, a Model (subclass) instance.
      pb: The protocol buffer, an EntityProto instance.
      prefix: Optional name prefix used for StructuredProperty
        (if present, must end in '.').
      parent_repeated: True if the parent (or an earlier ancestor)
        is a repeated Property.
      projection: A list or tuple of strings representing the projection for
        the model instance, or None if the instance is not a projection.
    """
    values = self._get_base_value_unwrapped_as_list(entity)
    name = six.ensure_text(prefix) + six.ensure_text(self._name)
    if projection and name not in projection:
      return

    if self._indexed:
      create_prop = lambda: pb.property.add()
    else:
      create_prop = lambda: pb.raw_property.add()

    if self._repeated and not values and self._write_empty_list:

      p = create_prop()
      p.name = name
      p.multiple = False
      p.meaning = entity_pb2.Property.EMPTY_LIST
      p.value.SetInParent()
    else:

      for val in values:
        p = create_prop()
        p.name = name
        p.multiple = self._repeated or parent_repeated
        p.value.SetInParent()
        v = p.value
        if val is not None:
          self._db_set_value(v, p, val)
          if projection:


            new_p = entity_pb2.Property()
            new_p.name = p.name
            new_p.meaning = entity_pb2.Property.INDEX_VALUE
            new_p.multiple = False
            new_p.value.CopyFrom(v)
            p.CopyFrom(new_p)

  def _deserialize(self, entity, p, unused_depth=1):
    """Internal helper to deserialize this property from a protocol buffer.

    Subclasses may override this method.

    Args:
      entity: The entity, a Model (subclass) instance.
      p: A Property Message object (a protocol buffer).
      depth: Optional nesting depth, default 1 (unused here, but used
        by some subclasses that override this method).
    """
    if p.meaning == entity_pb2.Property.EMPTY_LIST:
      self._store_value(entity, [])
      return

    val = self._db_get_value(p.value, p)
    if val is not None:
      val = _BaseValue(val)










    if self._repeated:
      if self._has_value(entity):
        value = self._retrieve_value(entity)
        assert isinstance(value, list), repr(value)
        value.append(val)
      else:

        value = [val]
    else:
      value = val
    self._store_value(entity, value)

  def _prepare_for_put(self, entity):
    pass

  def _check_property(self, rest=None, require_indexed=True):
    """Internal helper to check this property for specific requirements.

    Called by Model._check_properties().

    Args:
      rest: Optional subproperty to check, of the form 'name1.name2...nameN'.

    Raises:
      InvalidPropertyError if this property does not meet the given
      requirements or if a subproperty is specified.  (StructuredProperty
      overrides this method to handle subproperties.)
    """
    if require_indexed and not self._indexed:
      raise InvalidPropertyError('Property is unindexed %s' % self._name)
    if rest:
      raise InvalidPropertyError('Referencing subproperty %s.%s '
                                 'but %s is not a structured property' %
                                 (self._name, rest, self._name))

  def _get_for_dict(self, entity):
    """Retrieve the value like _get_value(), processed for _to_dict().

    Property subclasses can override this if they want the dictionary
    returned by entity._to_dict() to contain a different value.  The
    main use case is StructuredProperty and LocalStructuredProperty.

    NOTES::

    - If you override _get_for_dict() to return a different type, you
      must override _validate() to accept values of that type and
      convert them back to the original type.

    - If you override _get_for_dict(), you must handle repeated values
      and None correctly.  (See _StructuredGetForDictMixin for an
      example.)  However, _validate() does not need to handle these.
    """
    return self._get_value(entity)


def _validate_key(value, entity=None):
  if not isinstance(value, Key):

    raise datastore_errors.BadValueError('Expected Key, got %r' % value)
  if entity and entity.__class__ not in (Model, Expando):
    value_kind = six.ensure_str(value.kind(), encoding='utf-8')
    entity_kind = six.ensure_str(entity._get_kind(), encoding='utf-8')
    if value_kind != entity_kind:
      raise KindError(
          'Expected Key kind to be %s; received %s' % (entity_kind, value_kind))
  return value


class ModelKey(Property):
  """Special property to store the Model key."""

  def __init__(self):
    super(ModelKey, self).__init__()
    self._name = '__key__'

  def _datastore_type(self, value):
    return datastore_types.Key(value.urlsafe())

  def _comparison(self, op, value):
    if value is not None:
      return super(ModelKey, self)._comparison(op, value)
    raise datastore_errors.BadValueError(
        "__key__ filter query can't be compared to None")



  def _validate(self, value):
    return _validate_key(value)

  def _set_value(self, entity, value):
    """Setter for key attribute."""
    if value is not None:
      value = _validate_key(value, entity=entity)
      value = entity._validate_key(value)
    entity._entity_key = value

  def _get_value(self, entity):
    """Getter for key attribute."""
    return entity._entity_key

  def _delete_value(self, entity):
    """Deleter for key attribute."""
    entity._entity_key = None


class BooleanProperty(Property):
  """A Property whose value is a Python bool."""


  def _validate(self, value):
    if not isinstance(value, bool):
      raise datastore_errors.BadValueError('Expected bool, got %r' %
                                           (value,))
    return value

  def _db_set_value(self, v, unused_p, value):
    if not isinstance(value, bool):
      raise TypeError('BooleanProperty %s can only be set to bool values; '
                      'received %r' % (self._name, value))
    v.booleanValue = value

  def _db_get_value(self, v, unused_p):
    if not v.HasField('booleanValue'):
      return None


    return bool(v.booleanValue)


class IntegerProperty(Property):
  """A Property whose value is a Python int or long (or bool)."""

  def _validate(self, value):
    if not isinstance(value, six.integer_types):
      raise datastore_errors.BadValueError('Expected integer, got %r' %
                                           (value,))
    return int(value)

  def _db_set_value(self, v, unused_p, value):
    if not isinstance(value, six.integer_types + (bool,)):
      raise TypeError('IntegerProperty %s can only be set to integer values; '
                      'received %r' % (self._name, value))
    v.int64Value = value

  def _db_get_value(self, v, unused_p):
    if not v.HasField('int64Value'):
      return None
    return int(v.int64Value)


class FloatProperty(Property):
  """A Property whose value is a Python float.

  Note: int, long and bool are also allowed.
  """

  def _validate(self, value):
    if not isinstance(value, six.integer_types + (float,)):
      raise datastore_errors.BadValueError('Expected float, got %r' %
                                           (value,))
    return float(value)

  def _db_set_value(self, v, unused_p, value):
    if not isinstance(value, six.integer_types + (bool, float)):
      raise TypeError('FloatProperty %s can only be set to integer or float '
                      'values; received %r' % (self._name, value))
    v.doubleValue = float(value)

  def _db_get_value(self, v, unused_p):
    if not v.HasField('doubleValue'):
      return None
    return v.doubleValue



_MEANING_URI_COMPRESSED = 'ZLIB'


class _CompressedValue(_NotEqualMixin):
  """A marker object wrapping compressed values."""

  __slots__ = ['z_val']

  def __init__(self, z_val):
    """Constructor.  Argument is a string returned by zlib.compress()."""
    assert isinstance(z_val, six.binary_type), repr(z_val)
    self.z_val = z_val

  def __repr__(self):
    return '_CompressedValue(%s)' % repr(self.z_val)

  def __eq__(self, other):
    if not isinstance(other, _CompressedValue):
      return NotImplemented
    return self.z_val == other.z_val

  def __hash__(self):
    raise TypeError('_CompressedValue is not immutable')


class BlobProperty(Property):
  """A Property whose value is a byte string.  It may be compressed."""

  _indexed = False
  _compressed = False

  _attributes = Property._attributes + ['_compressed']

  @utils.positional(1 + Property._positional)
  def __init__(self, name=None, compressed=False, **kwds):
    super(BlobProperty, self).__init__(name=name, **kwds)
    self._compressed = compressed
    if compressed and self._indexed:

      raise NotImplementedError('BlobProperty %s cannot be compressed and '
                                'indexed at the same time.' % self._name)

  def _value_to_repr(self, value):
    long_repr = super(BlobProperty, self)._value_to_repr(value)







    prefix = long_repr[0] if long_repr[0] != "'" else ''


    i = 2 if prefix else 1
    j = len(long_repr) - 1
    content = long_repr[i:j]

    if len(content) > _MAX_STRING_LENGTH:
      long_repr = "%s'%s...'" % (prefix, content[:_MAX_STRING_LENGTH])
    return long_repr

  def _validate(self, value):
    if not isinstance(value, six.binary_type):
      raise datastore_errors.BadValueError(
          'Expected %s, got %s' % (six.binary_type, type(value)))
    if (self._indexed and
        not isinstance(self, TextProperty) and
        len(value) > _MAX_STRING_LENGTH):
      raise datastore_errors.BadValueError(
          'Indexed value %s must be at most %d bytes' %
          (self._name, _MAX_STRING_LENGTH))

  def _to_base_type(self, value):
    if self._compressed:
      return _CompressedValue(zlib.compress(value))

  def _from_base_type(self, value):
    if isinstance(value, _CompressedValue):
      return zlib.decompress(value.z_val)

  def _datastore_type(self, value):


    return datastore_types.ByteString(value)

  def _db_set_value(self, v, p, value):
    if isinstance(value, _CompressedValue):
      self._db_set_compressed_meaning(p)
      value = value.z_val
    else:
      self._db_set_uncompressed_meaning(p)
    v.stringValue = value

  def _db_set_compressed_meaning(self, p):



    p.meaning_uri = _MEANING_URI_COMPRESSED
    p.meaning = entity_pb2.Property.BLOB

  def _db_set_uncompressed_meaning(self, p):
    if self._indexed:
      p.meaning = entity_pb2.Property.BYTESTRING
    else:
      p.meaning = entity_pb2.Property.BLOB

  def _db_get_value(self, v, p):
    if not v.HasField('stringValue'):
      return None
    value = v.stringValue
    if p.meaning_uri == _MEANING_URI_COMPRESSED:
      value = _CompressedValue(value)
    return value


class TextProperty(BlobProperty):
  """An unindexed Property whose value is a text string of unlimited length."""

  def _validate(self, value):
    if isinstance(value, six.binary_type):

      try:
        length = len(value)
        value = six.ensure_text(value)
      except UnicodeError:
        raise datastore_errors.BadValueError('Expected valid UTF-8, got %r' %
                                             (value,))
    elif isinstance(value, six.text_type):
      length = len(value.encode('utf-8'))
    else:
      raise datastore_errors.BadValueError('Expected string, got %r' %
                                           (value,))
    if self._indexed and length > _MAX_STRING_LENGTH:
      raise datastore_errors.BadValueError(
          'Indexed value %s must be at most %d bytes' %
          (self._name, _MAX_STRING_LENGTH))

  def _to_base_type(self, value):
    if isinstance(value, six.text_type):
      return value.encode('utf-8')

  def _from_base_type(self, value):
    if isinstance(value, six.binary_type):
      try:
        return six.text_type(value, 'utf-8')
      except UnicodeDecodeError:





        pass

  def _db_set_uncompressed_meaning(self, p):
    if not self._indexed:
      p.meaning = entity_pb2.Property.TEXT


class StringProperty(TextProperty):
  """An indexed Property whose value is a text string of limited length."""

  _indexed = True


class GeoPtProperty(Property):
  """A Property whose value is a GeoPt."""

  def _validate(self, value):
    if not isinstance(value, GeoPt):
      raise datastore_errors.BadValueError('Expected GeoPt, got %r' %
                                           (value,))

  def _db_set_value(self, v, p, value):
    if not isinstance(value, GeoPt):
      raise TypeError('GeoPtProperty %s can only be set to GeoPt values; '
                      'received %r' % (self._name, value))
    p.meaning = entity_pb2.Property.GEORSS_POINT
    pv = v.pointvalue
    pv.x = value.lat
    pv.y = value.lon

  def _db_get_value(self, v, unused_p):
    if not v.HasField('pointvalue'):
      return None
    pv = v.pointvalue
    return GeoPt(pv.x, pv.y)


def _unpack_user(v):
  """Internal helper to unpack a User value from a protocol buffer."""
  uv = v.uservalue
  email = six.ensure_text(uv.email)
  auth_domain = six.ensure_text(uv.auth_domain)
  obfuscated_gaiaid = six.ensure_text(uv.obfuscated_gaiaid)
  obfuscated_gaiaid = six.ensure_text(obfuscated_gaiaid)

  federated_identity = None
  if uv.HasField('federated_identity'):
    federated_identity = six.text_type(uv.federated_identity.decode('utf-8'))

  value = users.User(email=email,
                     _auth_domain=auth_domain,
                     _user_id=obfuscated_gaiaid,
                     federated_identity=federated_identity)
  return value


class PickleProperty(BlobProperty):
  """A Property whose value is any picklable Python object."""

  def _to_base_type(self, value):
    if os.environ.get('NDB_USE_CROSS_COMPATIBLE_PICKLE_PROTOCOL', False):
      protocol = 2
    else:
      protocol = pickle.HIGHEST_PROTOCOL
    return pickle.dumps(value, protocol)

  def _from_base_type(self, value):
    try:
      return pickle.loads(value)
    except UnicodeDecodeError:
      if int(os.environ.get('NDB_PY2_UNPICKLE_COMPAT', '0')):
        return pickle.loads(value, encoding='bytes')
      raise


class JsonProperty(BlobProperty):
  """A property whose value is any Json-encodable Python object."""

  _json_type = None

  @utils.positional(1 + BlobProperty._positional)
  def __init__(self, name=None, compressed=False, json_type=None, **kwds):
    super(JsonProperty, self).__init__(name=name, compressed=compressed, **kwds)
    self._json_type = json_type

  def _validate(self, value):
    if self._json_type is not None and not isinstance(value, self._json_type):
      raise TypeError('JSON property must be a %s' % self._json_type)



  def _to_base_type(self, value):
    try:
      import json
    except ImportError:
      import simplejson as json
    return six.ensure_binary(json.dumps(value, separators=(',', ':')))

  def _from_base_type(self, value):
    try:
      import json
    except ImportError:
      import simplejson as json
    return json.loads(value)


class UserProperty(Property):
  """A Property whose value is a User object.

  Note: this exists for backwards compatibility with existing
  Cloud Datastore schemas only; we do not recommend storing User objects
  directly in Cloud Datastore, but instead recommend storing the
  user.user_id() value.
  """

  _attributes = Property._attributes + ['_auto_current_user',
                                        '_auto_current_user_add']

  _auto_current_user = False
  _auto_current_user_add = False

  @utils.positional(1 + Property._positional)
  def __init__(self, name=None, auto_current_user=False,
               auto_current_user_add=False, **kwds):
    super(UserProperty, self).__init__(name=name, **kwds)

    if self._repeated:
      if auto_current_user:
        raise ValueError('UserProperty could use auto_current_user and be '
                         'repeated, but there would be no point.')
      elif auto_current_user_add:
        raise ValueError('UserProperty could use auto_current_user_add and be '
                         'repeated, but there would be no point.')
    self._auto_current_user = auto_current_user
    self._auto_current_user_add = auto_current_user_add

  def _validate(self, value):
    if not isinstance(value, users.User):
      raise datastore_errors.BadValueError('Expected User, got %r' %
                                           (value,))

  def _prepare_for_put(self, entity):
    if (self._auto_current_user or
        (self._auto_current_user_add and not self._has_value(entity))):
      value = users.get_current_user()
      if value is not None:
        self._store_value(entity, value)

  def _db_set_value(self, v, p, value):
    datastore_types.PackUser(p.name, value, v)

  def _db_get_value(self, v, unused_p):
    if not v.HasField('uservalue'):
      return None
    return _unpack_user(v)


class KeyProperty(Property):
  """A Property whose value is a Key object.

  Optional keyword argument: kind=<kind>, to require that keys
  assigned to this property always have the indicated kind.  May be a
  string or a Model subclass.
  """

  _attributes = Property._attributes + ['_kind']

  _kind = None

  @utils.positional(2 + Property._positional)
  def __init__(self, *args, **kwds):








    name = kind = None

    for arg in args:
      if isinstance(arg, six.string_types):
        if name is not None:
          raise TypeError('You can only specify one name')
        name = arg
      elif isinstance(arg, type) and issubclass(arg, Model):
        if kind is not None:
          raise TypeError('You can only specify one kind')
        kind = arg
      elif arg is not None:
        raise TypeError('Unexpected positional argument: %r' % (arg,))

    if name is None:
      name = kwds.pop('name', None)
    elif 'name' in kwds:
      raise TypeError('You can only specify name once')

    if kind is None:
      kind = kwds.pop('kind', None)
    elif 'kind' in kwds:
      raise TypeError('You can only specify kind once')

    if kind is not None:
      if isinstance(kind, type) and issubclass(kind, Model):
        kind = kind._get_kind()
      if isinstance(kind, (six.text_type, bytes)):
        kind = six.ensure_str(kind)
      if not isinstance(kind, str):
        raise TypeError('kind must be a Model class or a string')

    super(KeyProperty, self).__init__(name, **kwds)

    self._kind = kind

  def _datastore_type(self, value):
    return datastore_types.Key(value.urlsafe())

  def _validate(self, value):
    if not isinstance(value, Key):
      raise datastore_errors.BadValueError('Expected Key, got %r' % (value,))

    if not value.id():
      raise datastore_errors.BadValueError('Expected complete Key, got %r' %
                                           (value,))
    if self._kind is not None:
      if value.kind() != self._kind:
        raise datastore_errors.BadValueError(
            'Expected Key with kind=%r, got %r' % (self._kind, value))

  def _db_set_value(self, v, unused_p, value):
    if not isinstance(value, Key):
      raise TypeError('KeyProperty %s can only be set to Key values; '
                      'received %r' % (self._name, value))

    ref = value.reference()
    v.referencevalue.SetInParent()
    rv = v.referencevalue
    rv.app = ref.app
    if ref.HasField('name_space'):
      rv.name_space = ref.name_space
    for elem in ref.path.element:

      pe = rv.pathelement.add()
      if elem.HasField('type'):
        pe.type = elem.type
      if elem.HasField('id'):
        pe.id = elem.id
      elif elem.HasField('name'):
        pe.name = elem.name

  def _db_get_value(self, v, unused_p):
    if not v.HasField('referencevalue'):
      return None
    ref = entity_pb2.Reference()
    rv = v.referencevalue
    if rv.HasField('app'):
      ref.app = rv.app
    if rv.HasField('name_space'):
      ref.name_space = rv.name_space
    ref.path.SetInParent()
    path = ref.path
    for elem in rv.pathelement:

      e = path.element.add()
      if elem.HasField('type'):
        e.type = elem.type
      if elem.HasField('id'):
        e.id = elem.id
      elif elem.HasField('name'):
        e.name = elem.name
    return Key(reference=ref)


class BlobKeyProperty(Property):
  """A Property whose value is a BlobKey object."""

  def _validate(self, value):
    if not isinstance(value, datastore_types.BlobKey):
      raise datastore_errors.BadValueError('Expected BlobKey, got %r' %
                                           (value,))

  def _db_set_value(self, v, p, value):
    if not isinstance(value, datastore_types.BlobKey):
      raise TypeError('BlobKeyProperty %s can only be set to BlobKey values; '
                      'received %r' % (self._name, value))
    p.meaning = entity_pb2.Property.BLOBKEY

    v.stringValue = six.ensure_binary(str(value))

  def _db_get_value(self, v, unused_p):
    if not v.HasField('stringValue'):
      return None
    return datastore_types.BlobKey(six.ensure_text(v.stringValue))



_EPOCH = datetime.datetime.utcfromtimestamp(0)


class DateTimeProperty(Property):
  """A Property whose value is a datetime object.

  Note: Unlike Django, auto_now_add can be overridden by setting the
  value before writing the entity.  And unlike classic db, auto_now
  does not supply a default value.  Also unlike classic db, when the
  entity is written, the property values are updated to match what
  was written.  Finally, beware that this also updates the value in
  the in-process cache, *and* that auto_now_add may interact weirdly
  with transaction retries (a retry of a property with auto_now_add
  set will reuse the value that was set on the first try).
  """

  _attributes = Property._attributes + ['_auto_now', '_auto_now_add']

  _auto_now = False
  _auto_now_add = False

  @utils.positional(1 + Property._positional)
  def __init__(self, name=None, auto_now=False, auto_now_add=False, **kwds):
    super(DateTimeProperty, self).__init__(name=name, **kwds)

    if self._repeated:
      if auto_now:
        raise ValueError('DateTimeProperty %s could use auto_now and be '
                         'repeated, but there would be no point.' % self._name)
      elif auto_now_add:
        raise ValueError('DateTimeProperty %s could use auto_now_add and be '
                         'repeated, but there would be no point.' % self._name)
    self._auto_now = auto_now
    self._auto_now_add = auto_now_add

  def _validate(self, value):
    if not isinstance(value, datetime.datetime):
      raise datastore_errors.BadValueError('Expected datetime, got %r' %
                                           (value,))

  def _now(self):
    return datetime.datetime.utcnow()

  def _prepare_for_put(self, entity):
    if (self._auto_now or
        (self._auto_now_add and not self._has_value(entity))):
      value = self._now()
      self._store_value(entity, value)

  def _db_set_value(self, v, p, value):
    if not isinstance(value, datetime.datetime):
      raise TypeError('DatetimeProperty %s can only be set to datetime values; '
                      'received %r' % (self._name, value))
    if value.tzinfo is not None:
      raise NotImplementedError('DatetimeProperty %s can only support UTC. '
                                'Please derive a new Property to support '
                                'alternative timezones.' % self._name)
    dt = value - _EPOCH
    ival = dt.microseconds + 1000000 * (dt.seconds + 24 * 3600 * dt.days)
    v.int64Value = ival
    p.meaning = entity_pb2.Property.GD_WHEN

  def _db_get_value(self, v, unused_p):
    if not v.HasField('int64Value'):
      return None
    ival = v.int64Value
    return _EPOCH + datetime.timedelta(microseconds=ival)


def _date_to_datetime(value):
  """Convert a date to a datetime for Cloud Datastore storage.

  Args:
    value: A datetime.date object.

  Returns:
    A datetime object with time set to 0:00.
  """
  if not isinstance(value, datetime.date):
    raise TypeError('Cannot convert to datetime expected date value; '
                    'received %s' % value)
  return datetime.datetime(value.year, value.month, value.day)


def _time_to_datetime(value):
  """Convert a time to a datetime for Cloud Datastore storage.

  Args:
    value: A datetime.time object.

  Returns:
    A datetime object with date set to 1970-01-01.
  """
  if not isinstance(value, datetime.time):
    raise TypeError('Cannot convert to datetime expected time value; '
                    'received %s' % value)
  return datetime.datetime(1970, 1, 1,
                           value.hour, value.minute, value.second,
                           value.microsecond)


class DateProperty(DateTimeProperty):
  """A Property whose value is a date object."""

  def _validate(self, value):
    if not isinstance(value, datetime.date):
      raise datastore_errors.BadValueError('Expected date, got %r' %
                                           (value,))

  def _to_base_type(self, value):
    assert isinstance(value, datetime.date), repr(value)
    return _date_to_datetime(value)

  def _from_base_type(self, value):
    assert isinstance(value, datetime.datetime), repr(value)
    return value.date()

  def _now(self):
    return datetime.datetime.utcnow().date()


class TimeProperty(DateTimeProperty):
  """A Property whose value is a time object."""

  def _validate(self, value):
    if not isinstance(value, datetime.time):
      raise datastore_errors.BadValueError('Expected time, got %r' %
                                           (value,))

  def _to_base_type(self, value):
    assert isinstance(value, datetime.time), repr(value)
    return _time_to_datetime(value)

  def _from_base_type(self, value):
    assert isinstance(value, datetime.datetime), repr(value)
    return value.time()

  def _now(self):
    return datetime.datetime.utcnow().time()


class _StructuredGetForDictMixin(Property):
  """Mixin class so *StructuredProperty can share _get_for_dict().

  The behavior here is that sub-entities are converted to dictionaries
  by calling to_dict() on them (also doing the right thing for
  repeated properties).

  NOTE: Even though the _validate() method in StructuredProperty and
  LocalStructuredProperty are identical, they cannot be moved into
  this shared base class.  The reason is subtle: _validate() is not a
  regular method, but treated specially by _call_to_base_type() and
  _call_shallow_validation(), and the class where it occurs matters
  if it also defines _to_base_type().
  """

  def _get_for_dict(self, entity):
    value = self._get_value(entity)
    if self._repeated:
      value = [v._to_dict() for v in value]
    elif value is not None:
      value = value._to_dict()
    return value


class StructuredProperty(_StructuredGetForDictMixin):
  """A Property whose value is itself an entity.

  The values of the sub-entity are indexed and can be queried.

  See the module docstring for details.
  """

  _modelclass = None

  _attributes = ['_modelclass'] + Property._attributes
  _positional = 1 + Property._positional

  @utils.positional(1 + _positional)
  def __init__(self, modelclass, name=None, **kwds):
    super(StructuredProperty, self).__init__(name=name, **kwds)
    if self._repeated:
      if modelclass._has_repeated:
        raise TypeError('This StructuredProperty cannot use repeated=True '
                        'because its model class (%s) contains repeated '
                        'properties (directly or indirectly).' %
                        modelclass.__name__)
    self._modelclass = modelclass

  def _get_value(self, entity):
    """Override _get_value() to *not* raise UnprojectedPropertyError."""
    value = self._get_user_value(entity)
    if value is None and entity._projection:

      return super(StructuredProperty, self)._get_value(entity)
    return value

  def __getattr__(self, attrname):
    """Dynamically get a subproperty."""

    prop = self._modelclass._properties.get(attrname)

    if prop is None or prop._code_name != attrname:

      for prop in self._modelclass._properties.values():
        if prop._code_name == attrname:
          break
      else:

        prop = None
    if prop is None:
      raise AttributeError('Model subclass %s has no attribute %s' %
                           (self._modelclass.__name__, attrname))
    prop_copy = copy.copy(prop)
    prop_copy._name = self._name + b'.' + prop_copy._name



    setattr(self, attrname, prop_copy)
    return prop_copy

  def _comparison(self, op, value):
    if op != '=':
      raise datastore_errors.BadFilterError(
          'StructuredProperty filter can only use ==')
    if not self._indexed:
      raise datastore_errors.BadFilterError(
          'Cannot query for unindexed StructuredProperty %s' % self._name)

    from google.appengine.ext.ndb.query import ConjunctionNode, PostFilterNode
    from google.appengine.ext.ndb.query import RepeatedStructuredPropertyPredicate
    if value is None:
      from google.appengine.ext.ndb.query import FilterNode
      return FilterNode(self._name, op, value)
    value = self._do_validate(value)
    value = self._call_to_base_type(value)
    filters = []
    match_keys = []

    for prop in six.itervalues(self._modelclass._properties):
      vals = prop._get_base_value_unwrapped_as_list(value)
      if prop._repeated:
        if vals:
          raise datastore_errors.BadFilterError(
              'Cannot query for non-empty repeated property %s' % prop._name)
        continue
      assert isinstance(vals, list) and len(vals) == 1, repr(vals)
      val = vals[0]
      if val is not None:
        altprop = getattr(self, prop._code_name)
        filt = altprop._comparison(op, val)
        filters.append(filt)
        match_keys.append(altprop._name)
    if not filters:
      raise datastore_errors.BadFilterError(
          'StructuredProperty filter without any values')
    if len(filters) == 1:
      return filters[0]
    if self._repeated:
      pb = value._to_pb(allow_partial=True)
      pred = RepeatedStructuredPropertyPredicate(
          match_keys, pb, self._name + b'.')
      filters.append(PostFilterNode(pred))
    return ConjunctionNode(*filters)

  def _IN(self, value):
    if not isinstance(value, (list, tuple, set, frozenset)):
      raise datastore_errors.BadArgumentError(
          'Expected list, tuple or set, got %r' % (value,))
    from google.appengine.ext.ndb.query import DisjunctionNode, FalseNode

    filters = [self._comparison('=', val) for val in value]
    if not filters:



      return FalseNode()
    else:
      return DisjunctionNode(*filters)
  IN = _IN

  def _validate(self, value):
    if isinstance(value, dict):

      return self._modelclass(**value)
    if not isinstance(value, self._modelclass):
      raise datastore_errors.BadValueError('Expected %s instance, got %r' %
                                           (self._modelclass.__name__, value))

  def _has_value(self, entity, rest=None):








    ok = super(StructuredProperty, self)._has_value(entity)
    if ok and rest:
      lst = self._get_base_value_unwrapped_as_list(entity)
      if len(lst) != 1:
        raise RuntimeError('Failed to retrieve sub-entity of StructuredProperty'
                           ' %s' % self._name)
      subent = lst[0]
      if subent is None:
        return True
      subprop = subent._properties.get(rest[0])
      if subprop is None:
        ok = False
      else:
        ok = subprop._has_value(subent, rest[1:])
    return ok

  def _serialize(self, entity, pb, prefix=b'', parent_repeated=False,
                 projection=None):

    values = self._get_base_value_unwrapped_as_list(entity)
    for value in values:
      if value is not None:

        for unused_name, prop in sorted(six.iteritems(value._properties)):
          prop._serialize(
              value,
              pb,
              prefix=prefix + self._name + b'.',
              parent_repeated=self._repeated or parent_repeated,
              projection=projection)
      else:

        super(StructuredProperty, self)._serialize(
            entity, pb, prefix=prefix, parent_repeated=parent_repeated,
            projection=projection)

  def _deserialize(self, entity, p, depth=1):
    if not self._repeated:
      subentity = self._retrieve_value(entity)
      if subentity is None:
        subentity = self._modelclass()
        self._store_value(entity, _BaseValue(subentity))
      cls = self._modelclass
      if isinstance(subentity, _BaseValue):


        subentity = subentity.b_val
      if not isinstance(subentity, cls):
        raise RuntimeError('Cannot deserialize StructuredProperty %s; value '
                           'retrieved not a %s instance %r' %
                           (self._name, cls.__name__, subentity))




      indexed = p.meaning_uri != _MEANING_URI_COMPRESSED
      prop = subentity._get_property_for(p, depth=depth, indexed=indexed)
      if prop is None:

        self._store_value(entity, None)
        return
      prop._deserialize(subentity, p, depth + 1)
      return



    name = p.name
    parts = name.split('.')
    if len(parts) <= depth:
      raise RuntimeError('StructuredProperty %s expected to find properties '
                         'separated by periods at a depth of %i; received %r' %
                         (self._name, depth, parts))
    next = parts[depth]
    rest = parts[depth + 1:]
    prop = self._modelclass._properties.get(next)
    prop_is_fake = False
    if prop is None:


      if rest:

        logging.warn('Skipping unknown structured subproperty (%s) '
                     'in repeated structured property (%s of %s)',
                     name, self._name, entity.__class__.__name__)
        return




      compressed = p.meaning_uri == _MEANING_URI_COMPRESSED
      prop = GenericProperty(next, compressed=compressed)
      prop._code_name = next
      prop_is_fake = True



    if not hasattr(entity, '_subentity_counter'):
      entity._subentity_counter = _NestedCounter()
    counter = entity._subentity_counter
    counter_path = parts[depth - 1:]
    next_index = counter.get(counter_path)
    subentity = None
    if self._has_value(entity):


      while next_index < self._get_value_size(entity):
        subentity = self._get_base_value_at_index(entity, next_index)
        if not isinstance(subentity, self._modelclass):
          raise TypeError('sub-entities must be instances '
                          'of their Model class.')
        if not prop._has_value(subentity, rest):
          break
        next_index = counter.increment(counter_path)
      else:
        subentity = None

    counter.increment(counter_path)
    if not subentity:


      subentity = self._modelclass()
      values = self._retrieve_value(entity, self._default)
      if values is None:
        self._store_value(entity, [])
        values = self._retrieve_value(entity, self._default)
      values.append(_BaseValue(subentity))
    if prop_is_fake:



      subentity._clone_properties()
      subentity._properties[six.ensure_text(prop._name)] = prop
    prop._deserialize(subentity, p, depth + 1)

  def _prepare_for_put(self, entity):
    values = self._get_base_value_unwrapped_as_list(entity)
    for value in values:
      if value is not None:
        value._prepare_for_put()

  def _check_property(self, rest=None, require_indexed=True):
    """Override for Property._check_property().

    Raises:
      InvalidPropertyError if no subproperty is specified or if something
      is wrong with the subproperty.
    """
    if not rest:
      raise InvalidPropertyError(
          'Structured property %s requires a subproperty' % self._name)
    self._modelclass._check_properties([rest], require_indexed=require_indexed)

  def _get_base_value_at_index(self, entity, index):
    assert self._repeated
    value = self._retrieve_value(entity, self._default)
    value[index] = self._opt_call_to_base_type(value[index])
    return value[index].b_val

  def _get_value_size(self, entity):
    values = self._retrieve_value(entity, self._default)
    if values is None:
      return 0
    return len(values)


class LocalStructuredProperty(_StructuredGetForDictMixin, BlobProperty):
  """Substructure that is serialized to an opaque blob.

  This looks like StructuredProperty on the Python side, but is
  written like a BlobProperty in Cloud Datastore.  It is not indexed
  and you cannot query for subproperties.  On the other hand, the
  on-disk representation is more efficient and can be made even more
  efficient by passing compressed=True, which compresses the blob
  data using gzip.
  """

  _indexed = False
  _modelclass = None
  _keep_keys = False

  _attributes = ['_modelclass'] + BlobProperty._attributes + ['_keep_keys']
  _positional = 1 + BlobProperty._positional

  @utils.positional(1 + _positional)
  def __init__(self, modelclass,
               name=None, compressed=False, keep_keys=False,
               **kwds):
    super(LocalStructuredProperty, self).__init__(name=name,
                                                  compressed=compressed,
                                                  **kwds)
    if self._indexed:
      raise NotImplementedError('Cannot index LocalStructuredProperty %s.' %
                                self._name)
    self._modelclass = modelclass
    self._keep_keys = keep_keys

  def _validate(self, value):
    if isinstance(value, dict):

      return self._modelclass(**value)
    if not isinstance(value, self._modelclass):
      raise datastore_errors.BadValueError('Expected %s instance, got %r' %
                                           (self._modelclass.__name__, value))

  def _to_base_type(self, value):
    if isinstance(value, self._modelclass):
      pb = value._to_pb(set_key=self._keep_keys)
      return pb.SerializePartialToString()

  def _from_base_type(self, value):
    if not isinstance(value, self._modelclass):
      pb = entity_pb2.EntityProto()
      pb.MergeFromString(value)
      if not self._keep_keys:
        pb.ClearField('key')
      return self._modelclass._from_pb(pb)

  def _prepare_for_put(self, entity):




    value = self._get_user_value(entity)
    if value is not None:
      if self._repeated:
        for subent in value:
          if subent is not None:
            subent._prepare_for_put()
      else:
        value._prepare_for_put()

  def _db_set_uncompressed_meaning(self, p):
    p.meaning = entity_pb2.Property.ENTITY_PROTO


class GenericProperty(Property):
  """A Property whose value can be (almost) any basic type.

  This is mainly used for Expando and for orphans (values present in
  Cloud Datastore but not represented in the Model subclass) but can
  also be used explicitly for properties with dynamically-typed
  values.

  This supports compressed=True, which is only effective for str
  values (not for unicode), and implies indexed=False.
  """

  _compressed = False

  _attributes = Property._attributes + ['_compressed']

  @utils.positional(1 + Property._positional)
  def __init__(self, name=None, compressed=False, **kwds):
    if compressed:
      kwds.setdefault('indexed', False)
    super(GenericProperty, self).__init__(name=name, **kwds)
    self._compressed = compressed
    if compressed and self._indexed:

      raise NotImplementedError('GenericProperty %s cannot be compressed and '
                                'indexed at the same time.' % self._name)

  def _to_base_type(self, value):
    if self._compressed and isinstance(value, six.binary_type):
      return _CompressedValue(zlib.compress(value))

  def _from_base_type(self, value):
    if isinstance(value, _CompressedValue):
      return zlib.decompress(value.z_val)

  def _validate(self, value):
    if self._indexed:
      if isinstance(value, six.text_type):
        value = value.encode('utf-8')
      if (isinstance(value, (six.text_type, six.binary_type)) and
          len(value) > _MAX_STRING_LENGTH):
        raise datastore_errors.BadValueError(
            'Indexed value %s must be at most %d bytes' %
            (self._name, _MAX_STRING_LENGTH))

  def _db_get_value(self, v, p):




    if v.HasField('stringValue'):
      sval = v.stringValue
      meaning = p.meaning
      if meaning == entity_pb2.Property.BLOBKEY:
        sval = BlobKey(sval)
      elif meaning == entity_pb2.Property.BLOB:
        if p.meaning_uri == _MEANING_URI_COMPRESSED:
          sval = _CompressedValue(sval)
      elif meaning == entity_pb2.Property.ENTITY_PROTO:

        pb = entity_pb2.EntityProto()
        pb.MergeFromString(sval)
        modelclass = Expando
        if len(pb.key.path.element):
          kind = six.ensure_str(pb.key.path.element[-1].type)
          modelclass = Model._kind_map.get(kind, modelclass)
        sval = modelclass._from_pb(pb)
      elif meaning != entity_pb2.Property.BYTESTRING:
        try:
          sval.decode('ascii')

        except UnicodeDecodeError:
          try:
            sval = six.text_type(sval.decode('utf-8'))
          except UnicodeDecodeError:
            pass
      return sval
    elif v.HasField('int64Value'):
      ival = v.int64Value
      if p.meaning == entity_pb2.Property.GD_WHEN:
        return _EPOCH + datetime.timedelta(microseconds=ival)
      return ival
    elif v.HasField('booleanValue'):


      return bool(v.booleanValue)
    elif v.HasField('doubleValue'):
      return v.doubleValue
    elif v.HasField('referencevalue'):
      rv = v.referencevalue
      app = rv.app
      namespace = rv.name_space
      pairs = [(elem.type, elem.id or elem.name) for elem in rv.pathelement]
      return Key(pairs=pairs, app=app, namespace=namespace)
    elif v.HasField('pointvalue'):
      pv = v.pointvalue
      return GeoPt(pv.x, pv.y)
    elif v.HasField('uservalue'):
      return _unpack_user(v)
    else:

      return None

  def _db_set_value(self, v, p, value):

    if isinstance(value, six.binary_type):
      v.stringValue = value


    elif isinstance(value, six.text_type):
      v.stringValue = six.ensure_binary(value)
      if not self._indexed:
        p.meaning = entity_pb2.Property.TEXT
    elif isinstance(value, bool):
      v.booleanValue = value
    elif isinstance(value, six.integer_types):

      if not (-_MAX_LONG <= value < _MAX_LONG):
        raise TypeError('Property %s can only accept 64-bit integers; '
                        'received %s' % (self._name, value))
      v.int64Value = value
    elif isinstance(value, float):
      v.doubleValue = value
    elif isinstance(value, Key):

      ref = value.reference()
      rv = v.referencevalue
      rv.app = ref.app
      if ref.HasField('name_space'):
        rv.name_space = ref.name_space
      for elem in ref.path.element:

        pe = rv.pathelement.add()
        if elem.HasField('type'):
          pe.type = elem.type
        if elem.HasField('id'):
          pe.id = elem.id
        elif elem.HasField('name'):
          pe.name = elem.name
    elif isinstance(value, datetime.datetime):
      if value.tzinfo is not None:
        raise NotImplementedError('Property %s can only support the UTC. '
                                  'Please derive a new Property to support '
                                  'alternative timezones.' % self._name)
      dt = value - _EPOCH
      ival = dt.microseconds + 1000000 * (dt.seconds + 24 * 3600 * dt.days)
      v.int64Value = ival
      p.meaning = entity_pb2.Property.GD_WHEN
    elif isinstance(value, GeoPt):
      p.meaning = entity_pb2.Property.GEORSS_POINT
      pv = v.pointvalue
      pv.x = value.lat
      pv.y = value.lon
    elif isinstance(value, users.User):
      datastore_types.PackUser(p.name, value, v)
    elif isinstance(value, BlobKey):
      v.stringValue = six.ensure_binary(str(value))
      p.meaning = entity_pb2.Property.BLOBKEY
    elif isinstance(value, Model):
      set_key = value._key is not None
      pb = value._to_pb(set_key=set_key)
      value = pb.SerializePartialToString()
      v.stringValue = value
      p.meaning = entity_pb2.Property.ENTITY_PROTO
    elif isinstance(value, _CompressedValue):
      value = value.z_val
      v.stringValue = value
      p.meaning_uri = _MEANING_URI_COMPRESSED
      p.meaning = entity_pb2.Property.BLOB
    else:
      raise NotImplementedError('Property %s does not support %s types.' %
                                (self._name, type(value)))


class ComputedProperty(GenericProperty):
  """A Property whose value is determined by a user-supplied function.

  Computed properties cannot be set directly, but are instead generated by a
  function when required. They are useful to provide fields in Cloud Datastore
  that can be used for filtering or sorting without having to manually set the
  value in code - for example, sorting on the length of a BlobProperty, or
  using an equality filter to check if another field is not empty.

  ComputedProperty can be declared as a regular property, passing a function as
  the first argument, or it can be used as a decorator for the function that
  does the calculation.

  Example:

  >>> class DatastoreFile(Model):
  ...   name = StringProperty()
  ...   name_lower = ComputedProperty(lambda self: self.name.lower())
  ...
  ...   data = BlobProperty()
  ...
  ...   @ComputedProperty
  ...   def size(self):
  ...     return len(self.data)
  ...
  ...   def _compute_hash(self):
  ...     return hashlib.sha1(self.data).hexdigest()
  ...   hash = ComputedProperty(_compute_hash, name='sha1')
  """

  def __init__(self, func, name=None, indexed=None,
               repeated=None, verbose_name=None):
    """Constructor.

    Args:
      func: A function that takes one argument, the model instance, and returns
            a calculated value.
    """
    super(ComputedProperty, self).__init__(name=name, indexed=indexed,
                                           repeated=repeated,
                                           verbose_name=verbose_name)
    self._func = func

  def _set_value(self, entity, value):
    raise ComputedPropertyError("Cannot assign to a ComputedProperty")

  def _delete_value(self, entity):
    raise ComputedPropertyError("Cannot delete a ComputedProperty")

  def _get_value(self, entity):











    if entity._projection and six.ensure_text(self._name) in entity._projection:
      return super(ComputedProperty, self)._get_value(entity)

    value = self._func(entity)
    self._store_value(entity, value)
    return value

  def _prepare_for_put(self, entity):
    self._get_value(entity)


class MetaModel(type):
  """Metaclass for Model.

  This exists to fix up the properties -- they need to know their name.
  This is accomplished by calling the class's _fix_properties() method.
  """

  def __init__(cls, name, bases, classdict):
    super(MetaModel, cls).__init__(name, bases, classdict)
    cls._fix_up_properties()

  def __repr__(cls):
    props = []
    for _, prop in sorted(six.iteritems(cls._properties)):
      props.append('%s=%r' % (prop._code_name, prop))
    return '%s<%s>' % (cls.__name__, ', '.join(props))


class Model(six.with_metaclass(MetaModel, _NotEqualMixin)):
  """A class describing Cloud Datastore entities.

  Model instances are usually called entities.  All model classes
  inheriting from Model automatically have MetaModel as their
  metaclass, so that the properties are fixed up properly after the
  class once the class is defined.

  Because of this, you cannot use the same Property object to describe
  multiple properties -- you must create separate Property objects for
  each property.  E.g. this does not work::

    wrong_prop = StringProperty()
    class Wrong(Model):
      wrong1 = wrong_prop
      wrong2 = wrong_prop

  The kind is normally equal to the class name (exclusive of the
  module name or any other parent scope).  To override the kind,
  define a class method named _get_kind(), as follows::

    class MyModel(Model):
      @classmethod
      def _get_kind(cls):
        return 'AnotherKind'
  """


  _properties = None
  _has_repeated = False
  _kind_map = {}


  _entity_key = None
  _values = None
  _projection = ()


  _key = ModelKey()
  key = _key

  def __init__(*args, **kwds):
    """Creates a new instance of this model (a.k.a. an entity).

    The new entity must be written to Cloud Datastore using an explicit
    call to .put().

    Keyword Args:
      key: Key instance for this model. If key is used, id and parent must
        be None.
      id: Key id for this model. If id is used, key must be None.
      parent: Key instance for the parent model or None for a top-level one.
        If parent is used, key must be None.
      namespace: Optional namespace.
      app: Optional app ID.
      **kwds: Keyword arguments mapping to properties of this model.

    Note: you cannot define a property named key; the .key attribute
    always refers to the entity's key.  But you can define properties
    named id or parent.  Values for the latter cannot be passed
    through the constructor, but can be assigned to entity attributes
    after the entity has been created.
    """
    if len(args) > 1:
      raise TypeError('Model constructor takes no positional arguments.')


    (self,) = args
    get_arg = self.__get_arg
    key = get_arg(kwds, 'key')
    id = get_arg(kwds, 'id')
    app = get_arg(kwds, 'app')
    namespace = get_arg(kwds, 'namespace')
    parent = get_arg(kwds, 'parent')
    projection = get_arg(kwds, 'projection')
    if key is not None:
      if (id is not None or parent is not None or
          app is not None or namespace is not None):
        raise datastore_errors.BadArgumentError(
            'Model constructor given key= does not accept '
            'id=, app=, namespace=, or parent=.')
      self._key = _validate_key(key, entity=self)
    elif (id is not None or parent is not None or
          app is not None or namespace is not None):
      self._key = Key(self._get_kind(), id,
                      parent=parent, app=app, namespace=namespace)
    self._values = {}
    self._set_attributes(kwds)

    if projection:
      self._set_projection(projection)

  @classmethod
  def __get_arg(cls, kwds, kwd):
    """Internal helper method to parse keywords that may be property names."""
    alt_kwd = '_' + kwd
    if alt_kwd in kwds:
      return kwds.pop(alt_kwd)
    if kwd in kwds:
      obj = getattr(cls, kwd, None)
      if not isinstance(obj, Property) or isinstance(obj, ModelKey):
        return kwds.pop(kwd)
    return None

  def __getstate__(self):
    return self._to_pb().SerializeToString()

  def __setstate__(self, serialized_pb):
    pb = entity_pb2.EntityProto.FromString(serialized_pb)
    self.__init__()
    self.__class__._from_pb(pb, set_key=False, ent=self)

  def _populate(self, **kwds):
    """Populate an instance from keyword arguments.

    Each keyword argument will be used to set a corresponding
    property.  Keywords must refer to valid property name.  This is
    similar to passing keyword arguments to the Model constructor,
    except that no provisions for key, id or parent are made.
    """
    self._set_attributes(kwds)
  populate = _populate

  def _set_attributes(self, kwds):
    """Internal helper to set attributes from keyword arguments.

    Expando overrides this.
    """
    cls = self.__class__
    for name, value in six.iteritems(kwds):
      prop = getattr(cls, name)
      if not isinstance(prop, Property):
        raise TypeError('Cannot set non-property %s' % name)
      prop._set_value(self, value)

  def _find_uninitialized(self):
    """Internal helper to find uninitialized properties.

    Returns:
      A set of property names.
    """
    return set(name for name, prop in six.iteritems(self._properties)
               if not prop._is_initialized(self))

  def _check_initialized(self):
    """Internal helper to check for uninitialized properties.

    Raises:
      BadValueError if it finds any.
    """
    baddies = self._find_uninitialized()
    if baddies:
      raise datastore_errors.BadValueError(
          'Entity has uninitialized properties: %s' % ', '.join(baddies))

  def __repr__(self):
    """Return an unambiguous string representation of an entity."""
    args = []
    for prop in six.itervalues(self._properties):
      if prop._has_value(self):
        val = prop._retrieve_value(self)
        if val is None:
          rep = 'None'
        elif prop._repeated:
          reprs = [prop._value_to_repr(v) for v in val]
          if reprs:
            reprs[0] = '[' + reprs[0]
            reprs[-1] = reprs[-1] + ']'
            rep = ', '.join(reprs)
          else:
            rep = '[]'
        else:
          rep = prop._value_to_repr(val)
        args.append('%s=%s' % (prop._code_name, rep))
    args.sort()
    if self._key is not None:
      args.insert(0, 'key=%r' % self._key)
    if self._projection:
      args.append('_projection=%r' % (self._projection,))
    s = '%s(%s)' % (self.__class__.__name__, ', '.join(args))
    return s

  @classmethod
  def _get_kind(cls):
    """Return the kind name for this class.

    This defaults to cls.__name__; users may overrid this to give a
    class a different on-disk name than its class name.
    """
    return cls.__name__

  @classmethod
  def _class_name(cls):
    """A hook for polymodel to override.

    For regular models and expandos this is just an alias for
    _get_kind().  For PolyModel subclasses, it returns the class name
    (as set in the 'class' attribute thereof), whereas _get_kind()
    returns the kind (the class name of the root class of a specific
    PolyModel hierarchy).
    """
    return cls._get_kind()

  @classmethod
  def _default_filters(cls):
    """Return an iterable of filters that are always to be applied.

    This is used by PolyModel to quietly insert a filter for the
    current class name.
    """
    return ()

  @classmethod
  def _reset_kind_map(cls):
    """Clear the kind map.  Useful for testing."""

    keep = {}
    for name, value in six.iteritems(cls._kind_map):
      if name.startswith('__') and name.endswith('__'):
        keep[name] = value
    cls._kind_map.clear()
    cls._kind_map.update(keep)

  @classmethod
  def _lookup_model(cls, kind, default_model=None):
    """Get the model class for the kind.

    Args:
      kind: A string representing the name of the kind to lookup.
      default_model: The model class to use if the kind can't be found.

    Returns:
      The model class for the requested kind.
    Raises:
      KindError: The kind was not found and no default_model was provided.
    """
    modelclass = cls._kind_map.get(kind, default_model)
    if modelclass is None:
      raise KindError(
          "No model class found for kind '%s'. Did you forget to import it?" %
          kind)
    return modelclass

  def _has_complete_key(self):
    """Return whether this entity has a complete key."""
    return self._key is not None and self._key.id() is not None
  has_complete_key = _has_complete_key

  def __hash__(self):
    """Dummy hash function.

    Raises:
      Always TypeError to emphasize that entities are mutable.
    """
    raise TypeError('Model is not immutable')



  def __eq__(self, other):
    """Compare two entities of the same class for equality."""
    if other.__class__ is not self.__class__:
      return NotImplemented
    if self._key != other._key:


      return False
    return self._equivalent(other)

  def _equivalent(self, other):
    """Compare two entities of the same class, excluding keys."""
    if other.__class__ is not self.__class__:
      raise NotImplementedError('Cannot compare different model classes. '
                                '%s is not %s' % (self.__class__.__name__,
                                                  other.__class_.__name__))
    if set(self._projection) != set(other._projection):
      return False

    if len(self._properties) != len(other._properties):
      return False
    my_prop_names = set(six.iterkeys(self._properties))
    their_prop_names = set(six.iterkeys(other._properties))
    if my_prop_names != their_prop_names:
      return False
    if self._projection:
      my_prop_names = set(self._projection)
    for name in my_prop_names:
      name = six.ensure_text(name)
      if '.' in name:
        name, _ = name.split('.', 1)
      my_value = self._properties[name]._get_value(self)
      their_value = other._properties[name]._get_value(other)
      if my_value != their_value:
        return False
    return True

  def _to_pb(self, pb=None, allow_partial=False, set_key=True):
    """Internal helper to turn an entity into an EntityProto protobuf."""
    if not allow_partial:
      self._check_initialized()
    if pb is None:
      pb = entity_pb2.EntityProto()

    if set_key:

      self._key_to_pb(pb)

    for unused_name, prop in sorted(six.iteritems(self._properties)):
      prop._serialize(self, pb, projection=self._projection)

    return pb

  def _key_to_pb(self, pb):
    """Internal helper to copy the key into a protobuf."""
    key = self._key
    if key is None:
      pairs = [(self._get_kind(), None)]
      ref = key_module._ReferenceFromPairs(pairs, reference=pb.key)
    else:
      ref = key.reference()
      pb.key.CopyFrom(ref)
    pb.entity_group.SetInParent()
    group = pb.entity_group


    if key is not None and key.id():
      elem = ref.path.element[0]
      if elem.id or elem.name:
        group.element.add().CopyFrom(elem)

  @classmethod
  def _from_pb(cls, pb, set_key=True, ent=None, key=None):
    """Internal helper to create an entity from an EntityProto protobuf."""
    if not isinstance(pb, entity_pb2.EntityProto):
      raise TypeError('pb must be a EntityProto; received %r' % pb)
    if ent is None:
      ent = cls()


    if key is None and len(pb.key.path.element):
      key = Key(reference=pb.key)

    if key is not None and (set_key or key.id() or key.parent()):
      ent._key = key




    _property_map = {}
    projection = []
    for indexed, plist in ((True, pb.property), (False, pb.raw_property)):
      for p in plist:
        prop_name = six.ensure_text(p.name)
        if p.meaning == entity_pb2.Property.INDEX_VALUE:
          projection.append(prop_name)
        property_map_key = (prop_name, indexed)
        if property_map_key not in _property_map:
          _property_map[property_map_key] = ent._get_property_for(p, indexed)
        _property_map[property_map_key]._deserialize(ent, p)

    ent._set_projection(projection)
    return ent

  def _set_projection(self, projection):
    by_prefix = {}
    for propname in projection:
      if '.' in propname:
        head, tail = propname.split('.', 1)
        if head in by_prefix:
          by_prefix[head].append(tail)
        else:
          by_prefix[head] = [tail]
    self._projection = tuple(projection)
    for propname, proj in six.iteritems(by_prefix):
      prop = self._properties.get(propname)
      subval = prop._get_base_value_unwrapped_as_list(self)
      for item in subval:
        assert item is not None
        item._set_projection(proj)

  def _get_property_for(self, p, indexed=True, depth=0):
    """Internal helper to get the Property for a protobuf-level property."""
    parts = p.name.split('.')
    if len(parts) <= depth:






      return None
    next = parts[depth]
    prop = self._properties.get(next)
    if prop is None:
      prop = self._fake_property(p, next, indexed)
    return prop

  def _clone_properties(self):
    """Internal helper to clone self._properties if necessary."""
    cls = self.__class__
    if self._properties is cls._properties:
      self._properties = dict(cls._properties)

  def _fake_property(self, p, next, indexed=True):
    """Internal helper to create a fake Property."""
    self._clone_properties()
    if p.name != next and not p.name.endswith('.' + next):
      prop = StructuredProperty(Expando, next)
      prop._store_value(self, _BaseValue(Expando()))
    else:
      compressed = p.meaning_uri == _MEANING_URI_COMPRESSED
      prop = GenericProperty(
          next, repeated=p.multiple, indexed=indexed, compressed=compressed)
    prop._code_name = next
    self._properties[prop._name.decode('utf-8')] = prop
    return prop

  @utils.positional(1)
  def _to_dict(self, include=None, exclude=None):
    """Return a dict containing the entity's property values.

    Args:
      include: Optional set of property names to include, default all.
      exclude: Optional set of property names to skip, default none.
        A name contained in both include and exclude is excluded.
    """
    if (include is not None and
        not isinstance(include, (list, tuple, set, frozenset))):
      raise TypeError('include should be a list, tuple or set')
    if (exclude is not None and
        not isinstance(exclude, (list, tuple, set, frozenset))):
      raise TypeError('exclude should be a list, tuple or set')
    values = {}
    for prop in six.itervalues(self._properties):
      name = prop._code_name
      if include is not None and name not in include:
        continue
      if exclude is not None and name in exclude:
        continue
      try:
        values[name] = prop._get_for_dict(self)
      except UnprojectedPropertyError:
        pass
    return values
  to_dict = _to_dict

  @classmethod
  def _fix_up_properties(cls):
    """Fix up the properties by calling their _fix_up() method.

    Note: This is called by MetaModel, but may also be called manually
    after dynamically updating a model class.
    """

    kind = cls._get_kind()
    if not isinstance(kind, (six.text_type, six.binary_type)):
      raise KindError('Class %s defines a _get_kind() method that returns '
                      'a non-string (%r)' % (cls.__name__, kind))
    if six.PY2 and not isinstance(kind, six.binary_type):
      try:
        kind = kind.encode('ascii')
      except UnicodeEncodeError:
        raise KindError('Class %s defines a _get_kind() method that returns '
                        'a Unicode string (%r); please encode using utf-8' %
                        (cls.__name__, kind))
    cls._properties = {}
    if cls.__module__ == __name__:
      return
    for name in set(dir(cls)):
      attr = getattr(cls, name, None)
      if isinstance(attr, ModelAttribute) and not isinstance(attr, ModelKey):
        if name.startswith('_'):
          raise TypeError('ModelAttribute %s cannot begin with an underscore '
                          'character. _ prefixed attributes are reserved for '
                          'temporary Model instance values.' % name)
        attr._fix_up(cls, name)
        if isinstance(attr, Property):
          if (attr._repeated or
              (isinstance(attr, StructuredProperty) and
               attr._modelclass._has_repeated)):
            cls._has_repeated = True
          cls._properties[six.ensure_text(attr._name)] = attr
    cls._update_kind_map()

  @classmethod
  def _update_kind_map(cls):
    """Update the kind map to include this class."""
    k = cls._get_kind()
    cls._kind_map[k] = cls

  def _prepare_for_put(self):
    if self._properties:
      for _, prop in sorted(six.iteritems(self._properties)):
        prop._prepare_for_put(self)

  @classmethod
  def _check_properties(cls, property_names, require_indexed=True):
    """Internal helper to check the given properties exist and meet specified
    requirements.

    Called from query.py.

    Args:
      property_names: List or tuple of property names -- each being a string,
        possibly containing dots (to address subproperties of structured
        properties).

    Raises:
      InvalidPropertyError if one of the properties is invalid.
      AssertionError if the argument is not a list or tuple of strings.
    """
    assert isinstance(property_names, (list, tuple)), repr(property_names)
    for name in property_names:
      assert isinstance(name, (six.text_type, six.binary_type)), repr(name)
      name = six.ensure_text(name)
      if '.' in name:
        name, rest = name.split('.', 1)
      else:
        rest = None
      prop = cls._properties.get(name)
      if prop is None:
        cls._unknown_property(name)
      else:
        prop._check_property(rest, require_indexed=require_indexed)

  @classmethod
  def _unknown_property(cls, name):
    """Internal helper to raise an exception for an unknown property name.

    This is called by _check_properties().  It is overridden by
    Expando, where this is a no-op.

    Raises:
      InvalidPropertyError.
    """
    raise InvalidPropertyError('Unknown property %s' % name)

  def _validate_key(self, key):
    """Validation for _key attribute (designed to be overridden).

    Args:
      key: Proposed Key to use for entity.

    Returns:
      A valid key.
    """
    return key




  @classmethod
  def _query(cls, *args, **kwds):
    """Create a Query object for this class.

    Args:
      distinct: Optional bool, short hand for group_by = projection.
      *args: Used to apply an initial filter
      **kwds: are passed to the Query() constructor.

    Returns:
      A Query object.
    """

    if 'distinct' in kwds:
      if 'group_by' in kwds:
        raise TypeError(
            'cannot use distinct= and group_by= at the same time')
      projection = kwds.get('projection')
      if not projection:
        raise TypeError(
            'cannot use distinct= without projection=')
      if kwds.pop('distinct'):
        kwds['group_by'] = projection


    from google.appengine.ext.ndb.query import Query
    qry = Query(kind=cls._get_kind(), **kwds)
    qry = qry.filter(*cls._default_filters())
    qry = qry.filter(*args)
    return qry
  query = _query

  @classmethod
  def _gql(cls, query_string, *args, **kwds):
    """Run a GQL query."""
    from google.appengine.ext.ndb.query import gql
    return gql('SELECT * FROM %s %s' % (cls._class_name(), query_string),
               *args, **kwds)
  gql = _gql

  def _put(self, **ctx_options):
    """Write this entity to Cloud Datastore.

    If the operation creates or completes a key, the entity's key
    attribute is set to the new, complete key.

    Returns:
      The key for the entity.  This is always a complete key.
    """
    return self._put_async(**ctx_options).get_result()
  put = _put

  def _put_async(self, **ctx_options):
    """Write this entity to Cloud Datastore.

    This is the asynchronous version of Model._put().
    """
    if self._projection:
      raise datastore_errors.BadRequestError('Cannot put a partial entity')
    from google.appengine.ext.ndb import tasklets
    ctx = tasklets.get_context()
    self._prepare_for_put()
    if self._key is None:
      self._key = Key(self._get_kind(), None)
    self._pre_put_hook()
    fut = ctx.put(self, **ctx_options)
    post_hook = self._post_put_hook
    if not self._is_default_hook(Model._default_post_put_hook, post_hook):
      fut.add_immediate_callback(post_hook, fut)
    return fut
  put_async = _put_async

  @classmethod
  def _get_or_insert(*args, **kwds):
    """Transactionally retrieves an existing entity or creates a new one.

    Positional Args:
      name: Key name to retrieve or create.

    Keyword Args:
      namespace: Optional namespace.
      app: Optional app ID.
      parent: Parent entity key, if any.
      context_options: ContextOptions object (not keyword args!) or None.
      **kwds: Keyword arguments to pass to the constructor of the model class
        if an instance for the specified key name does not already exist. If
        an instance with the supplied key_name and parent already exists,
        these arguments will be discarded.

    Returns:
      Existing instance of Model class with the specified key name and parent
      or a new one that has just been created.
    """
    cls, args = args[0], args[1:]
    return cls._get_or_insert_async(*args, **kwds).get_result()
  get_or_insert = _get_or_insert

  @classmethod
  def _get_or_insert_async(*args, **kwds):
    """Transactionally retrieves an existing entity or creates a new one.

    This is the asynchronous version of Model._get_or_insert().
    """


    from google.appengine.ext.ndb import tasklets
    cls, name = args
    get_arg = cls.__get_arg
    app = get_arg(kwds, 'app')
    namespace = get_arg(kwds, 'namespace')
    parent = get_arg(kwds, 'parent')
    context_options = get_arg(kwds, 'context_options')


    if not isinstance(name, six.string_types):
      raise TypeError('name must be a string; received %r' % name)
    elif not name:
      raise ValueError('name cannot be an empty string.')
    key = Key(cls, name, app=app, namespace=namespace, parent=parent)

    @tasklets.tasklet
    def internal_tasklet():
      @tasklets.tasklet
      def txn():
        ent = yield key.get_async(options=context_options)
        if ent is None:
          ent = cls(**kwds)
          ent._key = key
          yield ent.put_async(options=context_options)
        raise tasklets.Return(ent)
      if in_transaction():

        ent = yield txn()
      else:

        ent = yield key.get_async(options=context_options)
        if ent is None:

          ent = yield transaction_async(txn)
      raise tasklets.Return(ent)

    return internal_tasklet()

  get_or_insert_async = _get_or_insert_async

  @classmethod
  def _allocate_ids(cls, size=None, max=None, parent=None, **ctx_options):
    """Allocates a range of key IDs for this model class.

    Args:
      size: Number of IDs to allocate. Either size or max can be specified,
        not both.
      max: Maximum ID to allocate. Either size or max can be specified,
        not both.
      parent: Parent key for which the IDs will be allocated.
      **ctx_options: Context options.

    Returns:
      A tuple with (start, end) for the allocated range, inclusive.
    """
    return cls._allocate_ids_async(size=size, max=max, parent=parent,
                                   **ctx_options).get_result()
  allocate_ids = _allocate_ids

  @classmethod
  def _allocate_ids_async(cls, size=None, max=None, parent=None,
                          **ctx_options):
    """Allocates a range of key IDs for this model class.

    This is the asynchronous version of Model._allocate_ids().
    """
    from google.appengine.ext.ndb import tasklets
    ctx = tasklets.get_context()
    cls._pre_allocate_ids_hook(size, max, parent)
    key = Key(cls._get_kind(), None, parent=parent)
    fut = ctx.allocate_ids(key, size=size, max=max, **ctx_options)
    post_hook = cls._post_allocate_ids_hook
    if not cls._is_default_hook(Model._default_post_allocate_ids_hook,
                                post_hook):
      fut.add_immediate_callback(post_hook, size, max, parent, fut)
    return fut
  allocate_ids_async = _allocate_ids_async

  @classmethod
  @utils.positional(3)
  def _get_by_id(cls, id, parent=None, **ctx_options):
    """Returns an instance of Model class by ID.

    This is really just a shorthand for Key(cls, id, ...).get().

    Args:
      id: A string or integer key ID.
      parent: Optional parent key of the model to get.
      namespace: Optional namespace.
      app: Optional app ID.
      **ctx_options: Context options.

    Returns:
      A model instance or None if not found.
    """
    return cls._get_by_id_async(id, parent=parent, **ctx_options).get_result()
  get_by_id = _get_by_id

  @classmethod
  @utils.positional(3)
  def _get_by_id_async(cls, id, parent=None, app=None, namespace=None,
                       **ctx_options):
    """Returns an instance of Model class by ID (and app, namespace).

    This is the asynchronous version of Model._get_by_id().
    """
    key = Key(cls._get_kind(), id, parent=parent, app=app, namespace=namespace)
    return key.get_async(**ctx_options)
  get_by_id_async = _get_by_id_async














  @classmethod
  def _pre_allocate_ids_hook(cls, size, max, parent):
    pass
  _default_pre_allocate_ids_hook = _pre_allocate_ids_hook

  @classmethod
  def _post_allocate_ids_hook(cls, size, max, parent, future):
    pass
  _default_post_allocate_ids_hook = _post_allocate_ids_hook

  @classmethod
  def _pre_delete_hook(cls, key):
    pass
  _default_pre_delete_hook = _pre_delete_hook

  @classmethod
  def _post_delete_hook(cls, key, future):
    pass
  _default_post_delete_hook = _post_delete_hook

  @classmethod
  def _pre_get_hook(cls, key):
    pass
  _default_pre_get_hook = _pre_get_hook

  @classmethod
  def _post_get_hook(cls, key, future):
    pass
  _default_post_get_hook = _post_get_hook

  def _pre_put_hook(self):
    pass
  _default_pre_put_hook = _pre_put_hook

  def _post_put_hook(self, future):
    pass
  _default_post_put_hook = _post_put_hook

  @staticmethod
  def _is_default_hook(default_hook, hook):
    """Checks whether a specific hook is in its default state.

    Args:
      default_hook: Callable specified by ndb internally (do not override).
      hook: The hook defined by a model class using _post_*_hook.

    Raises:
      TypeError if either the default hook or the tested hook are not callable.
    """
    if not hasattr(default_hook, '__call__'):
      raise TypeError('Default hooks for ndb.model.Model must be callable')
    if not hasattr(hook, '__call__'):
      raise TypeError('Hooks must be callable')





    if hasattr(default_hook, '__func__'):
      default_hook = default_hook.__func__
    if hasattr(hook, '__func__'):
      hook = hook.__func__

    return default_hook is hook


class Expando(Model):
  """Model subclass to support dynamic Property names and types.

  See the module docstring for details.
  """



  _default_indexed = True


  _write_empty_list_for_dynamic_properties = None

  def _set_attributes(self, kwds):
    for name, value in six.iteritems(kwds):
      setattr(self, name, value)

  @classmethod
  def _unknown_property(cls, name):

    pass

  def __getattr__(self, name):
    if name.startswith('_'):
      return super(Expando, self).__getattr__(name)
    prop = self._properties.get(six.ensure_text(name))
    if prop is None:
      return super(Expando, self).__getattribute__(name)
    return prop._get_value(self)

  def __setattr__(self, name, value):
    if (name.startswith('_') or
        isinstance(getattr(self.__class__, name, None), (Property, property))):
      return super(Expando, self).__setattr__(name, value)

    self._clone_properties()
    if isinstance(value, Model):
      prop = StructuredProperty(Model, name)
    elif isinstance(value, dict):
      prop = StructuredProperty(Expando, name)
    else:

      prop = GenericProperty(
          name, repeated=isinstance(value, list),
          indexed=self._default_indexed,
          write_empty_list=self._write_empty_list_for_dynamic_properties)
    prop._code_name = name
    self._properties[six.ensure_text(name)] = prop
    prop._set_value(self, value)

  def __delattr__(self, name):
    if (name.startswith('_') or
        isinstance(getattr(self.__class__, name, None), (Property, property))):
      return super(Expando, self).__delattr__(name)
    prop_name = six.ensure_text(name)
    prop = self._properties.get(prop_name)
    if not isinstance(prop, Property):
      raise TypeError('Model properties must be Property instances; not %r' %
                      prop)
    prop._delete_value(self)
    if prop_name in self.__class__._properties:
      raise RuntimeError('Property %s still in the list of properties for the '
                         'base class.' % name)
    del self._properties[prop_name]


@utils.positional(1)
def transaction(callback, **ctx_options):
  """Run a callback in a transaction.

  Args:
    callback: A function or tasklet to be called.
    **ctx_options: Transaction options.

  Useful options include:
    retries=N: Retry up to N times (i.e. try up to N+1 times)
    propagation=<flag>: Determines how an existing transaction should be
      propagated, where <flag> can be one of the following:
      TransactionOptions.NESTED: Start a nested transaction (this is the
        default; but actual nested transactions are not yet implemented,
        so effectively you can only use this outside an existing transaction).
      TransactionOptions.MANDATORY: A transaction must already be in progress.
      TransactionOptions.ALLOWED: If a transaction is in progress, join it.
      TransactionOptions.INDEPENDENT: Always start a new parallel transaction.
    xg=True: On the High Replication Datastore, enable cross-group
      transactions, i.e. allow writing to up to 5 entity groups.
    read_only=True: Indicates a transaction will not do any writes, which
      potentially allows for more throughput.

  WARNING: Using anything other than NESTED for the propagation flag
  can have strange consequences.  When using ALLOWED or MANDATORY, if
  an exception is raised, the transaction is likely not safe to
  commit.  When using INDEPENDENT it is not generally safe to return
  values read to the caller (as they were not read in the caller's
  transaction).

  Returns:
    Whatever callback() returns.

  Raises:
    Whatever callback() raises; datastore_errors.TransactionFailedError
    if the transaction failed.

  Note:
    To pass arguments to a callback function, use a lambda, e.g.
      def my_callback(key, inc):
        ...
      transaction(lambda: my_callback(Key(...), 1))
  """
  fut = transaction_async(callback, **ctx_options)
  return fut.get_result()


@utils.positional(1)
def transaction_async(callback, **ctx_options):
  """Run a callback in a transaction.

  This is the asynchronous version of transaction().
  """
  from google.appengine.ext.ndb import tasklets
  return tasklets.get_context().transaction(callback, **ctx_options)


def in_transaction():
  """Return whether a transaction is currently active."""
  from google.appengine.ext.ndb import tasklets
  return tasklets.get_context().in_transaction()


@utils.decorator
def transactional(func, args, kwds, **options):
  """Decorator to make a function automatically run in a transaction.

  Args:
    **ctx_options: Transaction options (see transaction(), but propagation
      default to TransactionOptions.ALLOWED).

  This supports two forms:

  (1) Vanilla:
      @transactional
      def callback(arg):
        ...

  (2) With options:
      @transactional(retries=1)
      def callback(arg):
        ...
  """
  return transactional_async.wrapped_decorator(
      func, args, kwds, **options).get_result()


@utils.decorator
def transactional_async(func, args, kwds, **options):
  """The async version of @ndb.transaction."""
  options.setdefault('propagation', datastore_rpc.TransactionOptions.ALLOWED)
  if args or kwds:
    return transaction_async(lambda: func(*args, **kwds), **options)
  return transaction_async(func, **options)


@utils.decorator
def transactional_tasklet(func, args, kwds, **options):
  """The async version of @ndb.transaction.

  Will return the result of the wrapped function as a Future.
  """
  from google.appengine.ext.ndb import tasklets
  func = tasklets.tasklet(func)
  return transactional_async.wrapped_decorator(func, args, kwds, **options)


@utils.decorator
def non_transactional(func, args, kwds, allow_existing=True):
  """A decorator that ensures a function is run outside a transaction.

  If there is an existing transaction (and allow_existing=True), the
  existing transaction is paused while the function is executed.

  Args:
    allow_existing: If false, throw an exception if called from within
      a transaction.  If true, temporarily re-establish the
      previous non-transactional context.  Defaults to True.

  This supports two forms, similar to transactional().

  Returns:
    A wrapper for the decorated function that ensures it runs outside a
    transaction.
  """
  from google.appengine.ext.ndb import tasklets
  ctx = tasklets.get_context()
  if not ctx.in_transaction():
    return func(*args, **kwds)
  if not allow_existing:
    raise datastore_errors.BadRequestError(
        '%s cannot be called within a transaction.' % func.__name__)
  save_ctx = ctx
  while ctx.in_transaction():
    ctx = ctx._parent_context
    if ctx is None:
      raise datastore_errors.BadRequestError(
          'Context without non-transactional ancestor')
  save_ds_conn = datastore._GetConnection()
  try:
    if hasattr(save_ctx, '_old_ds_conn'):
      datastore._SetConnection(save_ctx._old_ds_conn)
    tasklets.set_context(ctx)
    return func(*args, **kwds)
  finally:
    tasklets.set_context(save_ctx)
    datastore._SetConnection(save_ds_conn)


def get_multi_async(keys, **ctx_options):
  """Fetches a sequence of keys.

  Args:
    keys: A sequence of keys.
    **ctx_options: Context options.

  Returns:
    A list of futures.
  """
  return [key.get_async(**ctx_options) for key in keys]


def get_multi(keys, **ctx_options):
  """Fetches a sequence of keys.

  Args:
    keys: A sequence of keys.
    **ctx_options: Context options.

  Returns:
    A list whose items are either a Model instance or None if the key wasn't
    found.
  """
  return [future.get_result()
          for future in get_multi_async(keys, **ctx_options)]


def put_multi_async(entities, **ctx_options):
  """Stores a sequence of Model instances.

  Args:
    entities: A sequence of Model instances.
    **ctx_options: Context options.

  Returns:
    A list of futures.
  """
  return [entity.put_async(**ctx_options) for entity in entities]


def put_multi(entities, **ctx_options):
  """Stores a sequence of Model instances.

  Args:
    entities: A sequence of Model instances.
    **ctx_options: Context options.

  Returns:
    A list with the stored keys.
  """
  return [future.get_result()
          for future in put_multi_async(entities, **ctx_options)]


def delete_multi_async(keys, **ctx_options):
  """Deletes a sequence of keys.

  Args:
    keys: A sequence of keys.
    **ctx_options: Context options.

  Returns:
    A list of futures.
  """
  return [key.delete_async(**ctx_options) for key in keys]


def delete_multi(keys, **ctx_options):
  """Deletes a sequence of keys.

  Args:
    keys: A sequence of keys.
    **ctx_options: Context options.

  Returns:
    A list whose items are all None, one per deleted key.
  """
  return [future.get_result()
          for future in delete_multi_async(keys, **ctx_options)]


def get_indexes_async(**ctx_options):
  """Get a data structure representing the configured indexes.

  Args:
    **ctx_options: Context options.

  Returns:
    A future.
  """
  from google.appengine.ext.ndb import tasklets
  ctx = tasklets.get_context()
  return ctx.get_indexes(**ctx_options)


def get_indexes(**ctx_options):
  """Get a data structure representing the configured indexes.

  Args:
    **ctx_options: Context options.

  Returns:
    A list of Index objects.
  """
  return get_indexes_async(**ctx_options).get_result()



for _name, _object in list(globals().items()):
  if ((_name.endswith('Property') and issubclass(_object, Property)) or
      (_name.endswith('Error') and issubclass(_object, Exception))):
    __all__.append(_name)
