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



"""Tests for google.appengine.ext.db.metadata."""



import os

from absl.testing import absltest
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_file_stub
from google.appengine.api import namespace_manager
from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import db
from google.appengine.ext.db import metadata


class TestModel(db.Model):
  x = db.IntegerProperty()


class MetadataTest(absltest.TestCase):

  NAMESPACES = ('ns1', 'fun', '')

  def setUp(self):
    """Setup test infrastructure."""
    super(MetadataTest, self).setUp()

    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.datastore_stub = datastore_file_stub.DatastoreFileStub('test_app',
                                                                None, None)
    self.datastore_stub.Clear()
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', self.datastore_stub)
    os.environ['APPLICATION_ID'] = 'test_app'

    self.PopulateEntities()

  def PopulateEntities(self):
    """Insert entities for metadata queries into the datastore."""

    for ns in MetadataTest.NAMESPACES:
      namespace_manager.set_namespace(ns)
      foo_e = datastore.Entity('Foo')
      foo_e['num'] = 1
      foo_e['data'] = None
      datastore.Put(foo_e)
      bar_e = datastore.Entity('Bar', unindexed_properties=['data'])
      bar_e['str'] = 'yeah'
      bar_e['data'] = 'gasp!'
      datastore.Put(bar_e)
      baz1_e = datastore.Entity('Baz')
      baz1_e['fun'] = True
      datastore.Put(baz1_e)
      baz2_e = datastore.Entity('Baz')
      baz2_e['fun'] = 'string'
      datastore.Put(baz2_e)

    namespace_manager.set_namespace('')

  def testNamespace(self):
    """Test model for __namespace__."""
    namespaces = metadata.Namespace.all().fetch(100)
    self.assertEqual('', namespaces[0].namespace_name)
    self.assertEqual('fun', namespaces[1].namespace_name)
    self.assertEqual('ns1', namespaces[2].namespace_name)
    self.assertEqual(3, len(namespaces))

    self.assertEqual('',
                     metadata.Namespace.key_to_namespace(namespaces[0].key()))
    self.assertEqual('fun',
                     metadata.Namespace.key_to_namespace(namespaces[1].key()))

    namespaces = (metadata.Namespace.all()
                  .filter('__key__ =', metadata.Namespace.key_for_namespace(''))
                  .fetch(100))
    self.assertEqual('', namespaces[0].namespace_name)
    self.assertEqual(metadata.Namespace.EMPTY_NAMESPACE_ID,
                     namespaces[0].key().id())
    self.assertEqual(1, len(namespaces))

    query = metadata.Namespace.all()
    query.filter('__key__ =', metadata.Namespace.key_for_namespace('ns1'))
    namespaces = query.fetch(100)
    self.assertEqual('ns1', namespaces[0].namespace_name)
    self.assertEqual('ns1', namespaces[0].key().name())
    self.assertEqual(1, len(namespaces))

    query = metadata.Namespace.all()
    query.filter('__key__ >', metadata.Namespace.key_for_namespace(''))
    namespaces = query.fetch(100)
    self.assertEqual('fun', namespaces[0].namespace_name)
    self.assertEqual('ns1', namespaces[1].namespace_name)
    self.assertEqual(2, len(namespaces))

  def testGetNamespaces(self):
    """Test for get_namespaces."""
    self.assertEqual(['', 'fun', 'ns1'], metadata.get_namespaces())
    self.assertEqual(['fun', 'ns1'], metadata.get_namespaces('a'))
    self.assertEqual(['', 'fun'], metadata.get_namespaces('', 'g'))
    self.assertEqual(['fun'], metadata.get_namespaces('f', 'g'))
    self.assertEqual([], metadata.get_namespaces('f', ''))

  def testKind(self):
    """Test model for __kind__."""
    kinds = metadata.Kind.all().fetch(100)
    self.assertEqual('Bar', kinds[0].kind_name)
    self.assertEqual('Baz', kinds[1].kind_name)
    self.assertEqual('Foo', kinds[2].kind_name)
    self.assertEqual(3, len(kinds))

    self.assertEqual('Bar', metadata.Kind.key_to_kind(kinds[0].key()))
    self.assertEqual('Baz', metadata.Kind.key_to_kind(kinds[1].key()))

    query = metadata.Kind.all()
    query.filter('__key__ =', metadata.Kind.key_for_kind('Baz'))
    kinds = query.fetch(100)
    self.assertEqual('Baz', kinds[0].kind_name)
    self.assertEqual('Baz', kinds[0].key().name())
    self.assertEqual(1, len(kinds))

    query = metadata.Kind.all()
    query.filter('__key__ >', metadata.Kind.key_for_kind('Bar'))
    kinds = query.fetch(100)
    self.assertEqual('Baz', kinds[0].kind_name)
    self.assertEqual('Foo', kinds[1].kind_name)
    self.assertEqual(2, len(kinds))

  def testGetKinds(self):
    """Test for get_kinds."""
    self.assertEqual(['Bar', 'Baz', 'Foo'], metadata.get_kinds())
    self.assertEqual(['Baz', 'Foo'], metadata.get_kinds('Bat'))
    self.assertEqual(['Bar', 'Baz'], metadata.get_kinds('', 'C'))
    self.assertEqual([], metadata.get_kinds('A', ''))

  def testProperty(self):
    """Test model for __property__."""
    properties = metadata.Property.all().fetch(100)

    self.assertEqual('Bar', properties[0].kind_name)
    self.assertEqual('str', properties[0].property_name)
    self.assertEqual(['STRING'], properties[0].property_representation)
    self.assertEqual('Baz', properties[1].kind_name)
    self.assertEqual('fun', properties[1].property_name)
    self.assertEqual(['BOOLEAN', 'STRING'],
                     properties[1].property_representation)
    self.assertEqual('Foo', properties[2].kind_name)
    self.assertEqual('data', properties[2].property_name)
    self.assertEqual(['NULL'], properties[2].property_representation)
    self.assertEqual('Foo', properties[3].kind_name)
    self.assertEqual('num', properties[3].property_name)
    self.assertEqual(['INT64'], properties[3].property_representation)
    self.assertEqual(4, len(properties))

    self.assertEqual('Baz', metadata.Property.key_to_kind(properties[1].key()))
    self.assertEqual('fun',
                     metadata.Property.key_to_property(properties[1].key()))

    query = metadata.Property.all()
    query.ancestor(metadata.Property.key_for_kind('Bar'))
    properties = query.fetch(100)
    self.assertEqual('Bar', properties[0].kind_name)
    self.assertEqual('str', properties[0].property_name)
    self.assertEqual(1, len(properties))

    query = metadata.Property.all(keys_only=True)
    query.filter('__key__ >', metadata.Property.key_for_property('Foo', 'data'))
    properties = query.fetch(100)
    self.assertEqual('Foo', metadata.Property.key_to_kind(properties[0]))
    self.assertEqual('num', metadata.Property.key_to_property(properties[0]))
    self.assertEqual(1, len(properties))


    key1 = metadata.Property.key_for_kind('Baz')
    key2 = metadata.Property.key_for_property('Bat', 'x')
    self.assertEqual('Baz', metadata.Property.key_to_kind(key1))
    self.assertEqual('Bat', metadata.Property.key_to_kind(key2))
    self.assertEqual(None, metadata.Property.key_to_property(key1))
    self.assertEqual('x', metadata.Property.key_to_property(key2))

  def testGetPropertiesOf(self):
    """Test for get_properties_of_kind."""
    self.assertEqual(['str'], metadata.get_properties_of_kind('Bar'))
    self.assertEqual([], metadata.get_properties_of_kind('Baz', 'g'))
    self.assertEqual(['data'],
                     metadata.get_properties_of_kind('Foo', None, 'e'))
    self.assertEqual(['data'], metadata.get_properties_of_kind('Foo', '', 'e'))
    self.assertEqual([], metadata.get_properties_of_kind('Foo', None, ''))

  def testGetRepresentationsOf(self):
    """Test for get_representations_of_kind."""
    self.assertEqual({'str': ['STRING']},
                     metadata.get_representations_of_kind('Bar'))
    self.assertEqual({}, metadata.get_representations_of_kind('Baz', 'g'))
    self.assertEqual({'data': ['NULL']},
                     metadata.get_representations_of_kind('Foo', None, 'e'))
    self.assertEqual({
        'data': ['NULL'],
        'num': ['INT64']
    }, metadata.get_representations_of_kind('Foo', 'a', 'z'))
    self.assertEqual({
        'data': ['NULL'],
        'num': ['INT64']
    }, metadata.get_representations_of_kind('Foo', '', 'z'))
    self.assertEqual({}, metadata.get_representations_of_kind('Foo', None, ''))

  def testEntityGroup(self):
    """Test for EntityGroup class."""

    self.datastore_stub.SetConsistencyPolicy(
        datastore_stub_util.PseudoRandomHRConsistencyPolicy())
    foo_e = TestModel(x=11)
    foo_e.put()
    child_e = TestModel(x=22, parent=foo_e)
    child_e.put()

    egfoo_k = metadata.EntityGroup.key_for_entity(foo_e.key())
    self.assertEqual(egfoo_k, metadata.EntityGroup.key_for_entity(foo_e))
    self.assertEqual(egfoo_k, metadata.EntityGroup.key_for_entity(child_e))

    self.assertGreater(db.get(egfoo_k).version, 0)

  def testGetEntityGroupVersion(self):
    """Test for get_entity_group_version function."""

    self.datastore_stub.SetConsistencyPolicy(
        datastore_stub_util.PseudoRandomHRConsistencyPolicy())
    foo_e = TestModel(x=11)
    foo_e.put()

    v1 = metadata.get_entity_group_version(foo_e)
    self.assertGreater(v1, 0)
    self.assertEqual(v1, metadata.get_entity_group_version(foo_e.key()))


if __name__ == '__main__':
  absltest.main()

