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



"""
In-memory persistent stub for the Python datastore API. Gets, queries,
and searches are implemented as in-memory scans over all entities.

Stores entities across sessions as pickled proto bufs in a single file. On
startup, all entities are read from the file and loaded into memory. On
every `Put()`, the file is wiped and all entities are written from scratch.
Clients can also manually `Read()` and `Write()` the file themselves.
"""

import collections
import logging
import os
import struct
import tempfile
import threading
import weakref

import six
from six.moves import filter
from six.moves import map
import six.moves.cPickle as pickle

from google.appengine.api import apiproxy_stub
from google.appengine.api import cmp_compat
from google.appengine.api import datastore
from google.appengine.api import datastore_types
from google.appengine.datastore import datastore_pb
from google.appengine.datastore import datastore_stub_util
from google.appengine.runtime import apiproxy_errors
from google.protobuf import message
from google.appengine.datastore import entity_bytes_pb2 as entity_pb2
















datastore_pb.Query.__hash__ = lambda self: hash(self.SerializeToString())

logger = logging.getLogger('google.appengine.api.stubs.datastore')

if six.PY3:
  long = int


def _FinalElement(key):
  """Return final element of a key's path."""
  return key.path.element[-1]


class _StoredEntity(object):
  """Simple wrapper around an entity (and its metadata) stored by the stub.

  Public properties:
    record: The original `EntityRecord` that was stored by the stub.
    encoded_protobuf: Encoded binary representation of entity protobuf,
        including a special property that holds the pickled metadata object.
  """

  def __init__(self, record):
    """Creates a `_StoredEntity` object and store an entity.

    Args:
      record: The `EntityRecord` to store.
    """
    self.record = record






    entity = datastore_stub_util._ToStorageEntity(record)
    self.encoded_protobuf = entity.SerializeToString()


class KindPseudoKind(object):
  """Pseudo-kind for schema queries.

  Provides a Query method to perform the actual query.

  Public properties:
    name: The pseudo-kind name
  """
  name = '__kind__'

  def Query(self, query, filters, orders):
    """Perform a query on this pseudo-kind.

    Args:
      query: The original `datastore_pb.Query`.
      filters: The filters from query.
      orders: The orders from query.

    Returns:
      `(results, remaining_filters, remaining_orders)`.
      `results` is a list of `entity_pb2.EntityProto`.
      `remaining_filters` and `remaining_orders` are the filters and orders that
      should be applied in memory.
    """
    kind_range = datastore_stub_util.ParseKindQuery(query, filters, orders)
    app_namespace_str = datastore_types.EncodeAppIdNamespace(
        query.app, query.name_space)
    kinds = []


    for app_namespace, kind in self._stub._GetAllEntities():
      if app_namespace != app_namespace_str: continue
      if not kind_range.Contains(kind): continue
      kinds.append(
          datastore.Entity(
              self.name, name=kind, _app=query.app,
              namespace=query.name_space)._ToPb())

    return (kinds, [], [])


class PropertyPseudoKind(object):
  """Pseudo-kind for schema queries.

  Provides a Query method to perform the actual query.

  Public properties:
    name: The pseudo-kind name.
  """
  name = '__property__'

  def Query(self, query, filters, orders):
    """Perform a query on this pseudo-kind.

    Args:
      query: The original `datastore_pb.Query`.
      filters: The filters from query.
      orders: The orders from query.

    Returns:
      `(results, remaining_filters, remaining_orders)`.
      `results` is a list of `entity_pb2.EntityProto`.
      `remaining_filters` and `remaining_orders` are the filters and orders that
      should be applied in memory.
    """
    property_range = datastore_stub_util.ParsePropertyQuery(query, filters,
                                                            orders)
    keys_only = query.keys_only
    app_namespace_str = datastore_types.EncodeAppIdNamespace(
        query.app, query.name_space)

    properties = []
    if keys_only:
      usekey = '__property__keys'
    else:
      usekey = '__property__'

    entities = self._stub._GetAllEntities()
    for app_namespace, kind in entities:
      if app_namespace != app_namespace_str: continue

      app_kind = (app_namespace_str, kind)



      (start_cmp, end_cmp) = property_range.MapExtremes(
          lambda extreme, inclusive, is_end: cmp_compat.cmp(kind, extreme[0]))
      if not((start_cmp is None or start_cmp >= 0) and
             (end_cmp is None or end_cmp <= 0)):
        continue


      kind_properties = self._stub._GetSchemaCache(app_kind, usekey)
      if not kind_properties:
        kind_properties = []
        kind_key = datastore_types.Key.from_path(
            KindPseudoKind.name,
            kind,
            _app=query.app,
            namespace=query.name_space)

        props = collections.defaultdict(set)



        for entity in entities[app_kind].values():
          for prop in entity.record.entity.property:
            prop_name = prop.name

            if (prop_name in
                datastore_stub_util.GetInvisibleSpecialPropertyNames()):
              continue
            value_pb = prop.value
            props[prop_name].add(datastore_types.GetPropertyValueTag(value_pb))


        for prop in sorted(props):
          property_e = datastore.Entity(
              self.name,
              name=prop,
              parent=kind_key,
              _app=query.app,
              namespace=query.name_space)

          if not keys_only and props[prop]:
            property_e['property_representation'] = [
                datastore_stub_util._PROPERTY_TYPE_NAMES[tag]
                for tag in sorted(props[prop])]

          kind_properties.append(property_e._ToPb())

        self._stub._SetSchemaCache(app_kind, usekey, kind_properties)


      def InQuery(property_e):
        return property_range.Contains((kind,
                                        _FinalElement(property_e.key).name))

      properties += list(filter(InQuery, kind_properties))

    return (properties, [], [])


class NamespacePseudoKind(object):
  """Pseudo-kind for namespace queries.

  Provides a Query method to perform the actual query.

  Public properties:
    name: The pseudo-kind name.
  """
  name = '__namespace__'

  def Query(self, query, filters, orders):
    """Perform a query on this pseudo-kind.

    Args:
      query: The original `datastore_pb.Query`.
      filters: The filters from query.
      orders: The orders from query.

    Returns:
      `(results, remaining_filters, remaining_orders)`.
      `results` is a list of entity_pb2.EntityProto
      remaining_filters and remaining_orders are the filters and orders that
      should be applied in memory
    """
    namespace_range = datastore_stub_util.ParseNamespaceQuery(query, filters,
                                                              orders)
    app_str = query.app

    namespaces = set()

    for app_namespace, _ in self._stub._GetAllEntities():
      (app_id, namespace) = datastore_types.DecodeAppIdNamespace(app_namespace)
      if app_id == app_str and namespace_range.Contains(namespace):
        namespaces.add(namespace)

    namespace_entities = []
    for namespace in namespaces:
      if namespace:
        namespace_e = datastore.Entity(
            self.name, name=namespace, _app=query.app)
      else:
        namespace_e = datastore.Entity(
            self.name, id=datastore_types._EMPTY_NAMESPACE_ID, _app=query.app)
      namespace_entities.append(namespace_e._ToPb())
    return (namespace_entities, [], [])


class DatastoreFileStub(datastore_stub_util.BaseDatastore,
                        apiproxy_stub.APIProxyStub,
                        datastore_stub_util.DatastoreStub):
  """Persistent stub for the Python datastore API.

  Stores all entities in memory, and persists them to a file as pickled
  protocol buffers. A `DatastoreFileStub` instance handles a single app's data
  and is backed by files on disk.
  """

  def __init__(self,
               app_id,
               datastore_file,
               history_file=None,
               require_indexes=False,
               service_name='datastore_v3',
               trusted=False,
               consistency_policy=None,
               save_changes=True,
               root_path=None,
               use_atexit=True,
               auto_id_policy=datastore_stub_util.SEQUENTIAL):
    """Constructor.

    Initializes and loads the datastore from the backing files, if they exist.

    Args:
      app_id: String
      datastore_file: String. Stores all entities across sessions. Use `None`
          not to use a file.
      history_file: DEPRECATE`. No-op.
      require_indexes: Bool. Default is `False`. If `True`, composite indexes
          must exist in `index.yaml` for queries that need them.
      service_name: Service name is expected for all calls.
      trusted: Bool. Default is `False`. If `True`, this stub allows an app to
        access the data of another app.
      consistency_policy: The consistency policy to use or `None` to use the
        default. Consistency policies can be found in
        `datastore_stub_util.*ConsistencyPolicy`.
      save_changes: Bool. Default is `True`. If this stub should modify
        `datastore_file` when entities are changed.
      root_path: String. The root path of the app.
      use_atexit: Bool. Indicates if the stub should save itself atexit.
      auto_id_policy: Enum. `datastore_stub_util.SEQUENTIAL` or `.SCATTERED`.
    """





    self.__datastore_file = datastore_file
    self.__save_changes = save_changes








    self.__entities_by_kind = collections.defaultdict(dict)
    self.__entities_by_group = collections.defaultdict(dict)
    self.__entities_lock = threading.Lock()




    self.__schema_cache = {}

    self.__id_counters = {
        datastore_stub_util.SEQUENTIAL: long(1),
        datastore_stub_util.SCATTERED: long(1)
    }
    self.__id_lock = threading.Lock()

    self.__file_lock = threading.Lock()

    datastore_stub_util.BaseDatastore.__init__(
        self, require_indexes, consistency_policy,
        use_atexit and self.__IsSaveable(), auto_id_policy)
    apiproxy_stub.APIProxyStub.__init__(self, service_name)
    datastore_stub_util.DatastoreStub.__init__(self, weakref.proxy(self),
                                               app_id, trusted, root_path)


    self._RegisterPseudoKind(KindPseudoKind())
    self._RegisterPseudoKind(PropertyPseudoKind())
    self._RegisterPseudoKind(NamespacePseudoKind())
    self._RegisterPseudoKind(datastore_stub_util.EntityGroupPseudoKind())

    self.Read()

  def Clear(self):
    """Clears the datastore by deleting all currently stored entities and queries.
    """
    self.__entities_lock.acquire()
    try:
      datastore_stub_util.BaseDatastore.Clear(self)
      datastore_stub_util.DatastoreStub.Clear(self)

      self.__entities_by_kind = collections.defaultdict(dict)
      self.__entities_by_group = collections.defaultdict(dict)
      self.__schema_cache = {}
    finally:
      self.__entities_lock.release()

  def _GetAllEntities(self):
    """Get all entities.

    Returns:
      Map from kind to `_StoredEntity()` list. Do not modify directly.
    """
    return self.__entities_by_kind

  def _GetEntityLocation(self, key):
    """Get keys to self.__entities_by_* from the given key.

    Example usage:
      app_kind, eg_k, k = self._GetEntityLocation(key)
      self.__entities_by_kind[app_kind][k]
      self.__entities_by_entity_group[eg_k][k]

    Args:
      key: entity_pb2.Reference

    Returns:
      Tuple (by_kind key, by_entity_group key, entity key)
    """
    app_ns = datastore_types.EncodeAppIdNamespace(key.app, key.name_space)
    kind = _FinalElement(key).type
    entity_group = datastore_stub_util._GetEntityGroup(key)
    eg_k = datastore_types.ReferenceToKeyValue(entity_group)
    k = datastore_types.ReferenceToKeyValue(key)

    return ((app_ns, kind), eg_k, k)

  def _StoreRecord(self, record, insert=False):
    """ Store the given entity record.

    Any needed locking should be managed by the caller.

    Args:
      record: The `EntityRecord` to store.
      insert: If we should check for existence.
    """
    app_kind, eg_k, k = self._GetEntityLocation(record.entity.key)

    assert not insert or k not in self.__entities_by_kind[app_kind]

    stored_entity = _StoredEntity(record)
    self.__entities_by_kind[app_kind][k] = stored_entity
    self.__entities_by_group[eg_k][k] = stored_entity


    if app_kind in self.__schema_cache:
      del self.__schema_cache[app_kind]

  READ_PB_EXCEPTIONS = (message.DecodeError, LookupError, TypeError, ValueError)
  READ_ERROR_MSG = ('Data in %s is corrupt or a different version. '
                    'Try running with the --clear_datastore flag.\n%r')
  READ_PY250_MSG = ('Are you using FloatProperty and/or GeoPtProperty? '
                    'Unfortunately loading float values from the datastore '
                    'file does not work with Python 2.5.0. '
                    'Please upgrade to a newer Python 2.5 release or use '
                    'the --clear_datastore flag.\n')

  def Read(self):
    """Reads the datastore and history files into memory.

    The in-memory query history is cleared, but the datastore is *not*
    cleared; the entities in the files are merged into the entities in memory.
    If you want them to overwrite the in-memory datastore, call `Clear()` before
    calling `Read()`.

    If the datastore file contains an entity with the same app name, kind, and
    key as an entity already in the datastore, the entity from the file
    overwrites the entity in the datastore.

    Also sets each `ID` counter to one greater than the highest `ID` allocated
    so far in that counter's `ID` space.
    """
    if self.__datastore_file and self.__datastore_file != '/dev/null':
      entities = self.__ReadPickled(self.__datastore_file)
      if entities and isinstance(entities[-1], six.integer_types):
        self._commit_timestamp = int(entities.pop())
      for encoded_entity in entities:
        try:
          entity = entity_pb2.EntityProto.FromString(encoded_entity)
          record = datastore_stub_util._FromStorageEntity(entity)
        except self.READ_PB_EXCEPTIONS as e:
          raise apiproxy_errors.ApplicationError(
              datastore_pb.Error.INTERNAL_ERROR,
              self.READ_ERROR_MSG % (self.__datastore_file, e))
        except struct.error as e:
          raise

        self._StoreRecord(record)

        last_path = _FinalElement(entity.key)
        if last_path.id:
          self._SetMaxId(last_path.id)

  def Write(self):
    """Writes out the datastore and history files.

    Important: If the files already exist, this method overwrites them.
    """
    super(DatastoreFileStub, self).Write()
    self.__WriteDatastore()

  def __IsSaveable(self):
    return (self.__datastore_file and self.__datastore_file != '/dev/null' and
            self.__save_changes)

  def __WriteDatastore(self):
    """Writes out the datastore file.

    Be careful: If the file already exists, this method overwrites it!
    """
    if self.__IsSaveable():
      encoded = []
      for kind_dict in self.__entities_by_kind.values():
        encoded.extend(entity.encoded_protobuf for entity in kind_dict.values())
      encoded.append(self._GetReadTimestamp())

      self.__WritePickled(encoded, self.__datastore_file)

  def __ReadPickled(self, filename):
    """Reads a pickled object from the given file and returns it.
    """
    self.__file_lock.acquire()

    try:
      try:
        if (filename and
            filename != '/dev/null' and
            os.path.isfile(filename) and
            os.stat(filename).st_size > 0):
          pickle_kwargs = {}
          if six.PY3:

            pickle_kwargs['encoding'] = 'bytes'
          return pickle.load(open(filename, 'rb'), **pickle_kwargs)
        else:
          logger.warning('Could not read datastore data from %s', filename)
      except (AttributeError, LookupError, ImportError, NameError, TypeError,
              ValueError, struct.error, pickle.PickleError) as e:


        raise apiproxy_errors.ApplicationError(
            datastore_pb.Error.INTERNAL_ERROR,
            'Could not read data from %s. Try running with the '
            '--clear_datastore flag. Cause:\n%r' % (filename, e))
    finally:
      self.__file_lock.release()

    return []

  def __WritePickled(self, obj, filename):
    """Pickles the object and writes it to the given file.
    """
    if not filename or filename == '/dev/null' or not obj:
      return


    descriptor, tmp_filename = tempfile.mkstemp(dir=os.path.dirname(filename))
    tmpfile = os.fdopen(descriptor, 'wb')





    pickler = pickle.Pickler(tmpfile, protocol=1)
    pickler.fast = True
    pickler.dump(obj)

    tmpfile.close()

    self.__file_lock.acquire()
    try:
      try:

        os.rename(tmp_filename, filename)
      except OSError:

        try:
          os.remove(filename)
        except:
          pass
        os.rename(tmp_filename, filename)
    finally:
      self.__file_lock.release()

  def MakeSyncCall(self, service, call, request, response, request_id=None):
    """The main RPC entry point. Service must be datastore_v3."""
    self.assertPbIsInitialized(request)
    super(DatastoreFileStub, self).MakeSyncCall(service,
                                                call,
                                                request,
                                                response,
                                                request_id)
    self.assertPbIsInitialized(response)

  def assertPbIsInitialized(self, pb):
    """Raises an exception if the given `PB` is not initialized and valid."""
    explanation = []

    pb.SerializeToString()

  def _GetSchemaCache(self, kind, usekey):
    if kind in self.__schema_cache and usekey in self.__schema_cache[kind]:
      return self.__schema_cache[kind][usekey]
    else:
      return None

  def _SetSchemaCache(self, kind, usekey, value):
    if kind not in self.__schema_cache:
      self.__schema_cache[kind] = {}
    self.__schema_cache[kind][usekey] = value



  def _Put(self, record, insert):
    record = datastore_stub_util.StoreRecord(record)

    self.__entities_lock.acquire()
    try:
      self._StoreRecord(record, insert)
    finally:
      self.__entities_lock.release()

  def _Get(self, key):
    app_kind, _, k = self._GetEntityLocation(key)


    try:
      stored_entity = self.__entities_by_kind[app_kind][k]
      return datastore_stub_util.LoadRecord(stored_entity.record)

    except KeyError:
      pass

  def _Delete(self, key):
    app_kind, eg_k, k = self._GetEntityLocation(key)

    self.__entities_lock.acquire()
    try:
      del self.__entities_by_kind[app_kind][k]
      del self.__entities_by_group[eg_k][k]
      if not self.__entities_by_kind[app_kind]:

        del self.__entities_by_kind[app_kind]
      if not self.__entities_by_group[eg_k]:
        del self.__entities_by_group[eg_k]

      del self.__schema_cache[app_kind]
    except KeyError:

      pass
    finally:
      self.__entities_lock.release()

  def _GetEntitiesInEntityGroup(self, entity_group):
    eg_k = datastore_types.ReferenceToKeyValue(entity_group)
    return dict((k, e.record)
                for (k, e) in six.iteritems(self.__entities_by_group[eg_k]))

  def _GetQueryCursor(self, query, filters, orders, index_list):
    app_id = query.app
    namespace = query.name_space

    pseudo_kind = None
    if query.HasField('kind') and query.kind in self._pseudo_kinds:
      pseudo_kind = self._pseudo_kinds[query.kind]




    self.__entities_lock.acquire()
    try:
      app_ns = datastore_types.EncodeAppIdNamespace(app_id, namespace)
      if pseudo_kind:

        (results, filters, orders) = pseudo_kind.Query(query, filters, orders)
        results = list(map(datastore_stub_util.EntityRecord, results))
      elif query.HasField('kind'):
        stored_entities = list(
            self.__entities_by_kind[app_ns, query.kind].values())
        results = [stored_entity.record for stored_entity in stored_entities]
      else:
        results = []
        for (cur_app_ns, _), entities in six.iteritems(self.__entities_by_kind):
          if cur_app_ns == app_ns:
            results.extend(entity.record for entity in six.itervalues(entities))
    except KeyError:
      results = []
    finally:
      self.__entities_lock.release()

    return datastore_stub_util._ExecuteQuery(results, query, filters, orders,
                                             index_list)

  def _SetIdCounter(self, id_space, value):
    """Sets the `ID` counter for id_space to value."""
    self.__id_counters[id_space] = value

  def _IdCounter(self, id_space):
    """Returns current value of `ID` counter for id_space."""
    return self.__id_counters[id_space]

  def _SetMaxId(self, max_id):
    """Infers `ID` space and advance corresponding counter."""
    count, id_space = datastore_stub_util.IdToCounter(max_id)
    if count >= self._IdCounter(id_space):
      self._SetIdCounter(id_space, count + 1)

  def _AllocateSequentialIds(self, reference, size=1, max_id=None):
    datastore_stub_util.Check(not (size and max_id),
                              'Both size and max cannot be set.')

    self.__id_lock.acquire()
    try:
      id_space = datastore_stub_util.SEQUENTIAL
      start = self._IdCounter(id_space)
      if size:
        datastore_stub_util.Check(size > 0, 'Size must be greater than 0.')
        self._SetIdCounter(id_space, start + size)
      elif max_id:
        datastore_stub_util.Check(max_id >=0,
                                  'Max must be greater than or equal to 0.')
        self._SetIdCounter(id_space, max(start, max_id + 1))
      end = self._IdCounter(id_space) - 1
    finally:
      self.__id_lock.release()

    return (start, end)

  def _AllocateIds(self, keys):
    self.__id_lock.acquire()
    full_keys = []
    try:
      for key in keys:
        last_element = _FinalElement(key)

        if last_element.id or last_element.HasField('name'):
          for el in key.path.element:
            if el.HasField('id'):
              self._SetMaxId(el.id)

        else:
          id_space = datastore_stub_util.SCATTERED
          count = self._IdCounter(id_space)
          last_element.id = datastore_stub_util.ToScatteredId(count)
          self._SetIdCounter(id_space, count + 1)
          full_keys.append(key)
    finally:
      self.__id_lock.release()

    return full_keys
