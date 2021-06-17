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


"""Tests for google.appengine.ext.db.stats."""

import datetime

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_file_stub
from google.appengine.api import full_app_id
from google.appengine.datastore import datastore_stub_util
from google.appengine.ext.db import stats

from absl.testing import absltest


class StatsTest(absltest.TestCase):

  def setUp(self):
    """Setup test infrastructure."""
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.datastore_stub = datastore_file_stub.DatastoreFileStub('test_app',
                                                                '/dev/null',
                                                                '/dev/null')
    self.datastore_stub.Clear()
    self.datastore_stub.SetAutoIdPolicy(datastore_stub_util.SEQUENTIAL)
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', self.datastore_stub)
    full_app_id.put('test_app')

    self.PopulateStatEntities()

  def PopulateStatEntities(self):
    """Insert stat entities into the datastore."""

    self.CreateStatEntity(stats.GlobalStat.STORED_KIND_NAME,
        has_entity_bytes=True,
        has_builtin_index_stats=True,
        has_composite_index_stats=True)


    self.CreateStatEntity(stats.NamespaceStat.STORED_KIND_NAME,
        subject_namespace='name-space',
        has_entity_bytes=True,
        has_builtin_index_stats=True,
        has_composite_index_stats=True)


    self.CreateStatEntity(stats.KindStat.STORED_KIND_NAME, 'foo',
        has_entity_bytes=True,
        has_builtin_index_stats=True,
        has_composite_index_stats=True)
    self.CreateStatEntity(stats.KindStat.STORED_KIND_NAME, 'foo2',
        has_entity_bytes=True,
        has_builtin_index_stats=True,
        has_composite_index_stats=True)


    self.CreateStatEntity(stats.KindRootEntityStat.STORED_KIND_NAME, 'foo3',
                          has_entity_bytes=True)
    self.CreateStatEntity(stats.KindRootEntityStat.STORED_KIND_NAME, 'foo4',
                          has_entity_bytes=True)


    self.CreateStatEntity(stats.KindNonRootEntityStat.STORED_KIND_NAME, 'foo5',
                          has_entity_bytes=True)
    self.CreateStatEntity(stats.KindNonRootEntityStat.STORED_KIND_NAME, 'foo6',
                          has_entity_bytes=True)


    self.CreateStatEntity(stats.PropertyTypeStat.STORED_KIND_NAME,
        property_type='pt1',
        has_entity_bytes=True,
        has_builtin_index_stats=True)
    self.CreateStatEntity(stats.PropertyTypeStat.STORED_KIND_NAME,
        property_type='pt2',
        has_entity_bytes=True,
        has_builtin_index_stats=True)


    self.CreateStatEntity(stats.KindPropertyTypeStat.STORED_KIND_NAME,
        kind_name='foo1',
        property_type='pt1',
        has_entity_bytes=True,
        has_builtin_index_stats=True)
    self.CreateStatEntity(stats.KindPropertyTypeStat.STORED_KIND_NAME,
        kind_name='foo1',
        property_type='pt2',
        has_entity_bytes=True,
        has_builtin_index_stats=True)
    self.CreateStatEntity(stats.KindPropertyTypeStat.STORED_KIND_NAME,
        kind_name='foo2',
        property_type='pt2',
        has_entity_bytes=True,
        has_builtin_index_stats=True)


    self.CreateStatEntity(stats.KindPropertyNameStat.STORED_KIND_NAME,
        kind_name='foo11',
        property_name='pn1',
        has_entity_bytes=True,
        has_builtin_index_stats=True)
    self.CreateStatEntity(stats.KindPropertyNameStat.STORED_KIND_NAME,
        kind_name='foo11',
        property_name='pn2',
        has_entity_bytes=True,
        has_builtin_index_stats=True)
    self.CreateStatEntity(stats.KindPropertyNameStat.STORED_KIND_NAME,
        kind_name='foo21',
        property_name='pn2',
        has_entity_bytes=True,
        has_builtin_index_stats=True)


    self.CreateStatEntity(
        stats.KindPropertyNamePropertyTypeStat.STORED_KIND_NAME,
        kind_name='foo12',
        property_type='pt1',
        property_name='pn1',
        has_entity_bytes=True,
        has_builtin_index_stats=True)

    self.CreateStatEntity(
        stats.KindPropertyNamePropertyTypeStat.STORED_KIND_NAME,
        kind_name='foo12',
        property_type='pt2',
        property_name='pn2',
        has_entity_bytes=True,
        has_builtin_index_stats=True)

    self.CreateStatEntity(
        stats.KindPropertyNamePropertyTypeStat.STORED_KIND_NAME,
        kind_name='foo22',
        property_type='pt2',
        property_name='pn2',
        has_entity_bytes=True,
        has_builtin_index_stats=True)


    self.CreateStatEntity(
        stats.KindCompositeIndexStat.STORED_KIND_NAME,
        kind_name='foo12',
        composite_index_id=1)
    self.CreateStatEntity(
        stats.KindCompositeIndexStat.STORED_KIND_NAME,
        kind_name='foo12',
        composite_index_id=2)
    self.CreateStatEntity(
        stats.KindCompositeIndexStat.STORED_KIND_NAME,
        kind_name='foo22',
        composite_index_id=3)

  def CreateStatEntity(self,
                       kind,
                       kind_name=None,
                       property_type=None,
                       property_name=None,
                       subject_namespace=None,
                       composite_index_id=None,
                       has_entity_bytes=None,
                       has_builtin_index_stats=None,
                       has_composite_index_stats=None):
    """Create a single Statistic datastore entity.

    Args:
      kind: The name of the kind to store.
      kind_name: The value of the 'kind_name' property to set on the entity.
      property_type: The value of the 'property_type' property to set on the
        entity.
      property_name: The value of the 'property_name' property to set on the
        entity.
      subject_namespace: The namespace for NamespaceStat entities.
      composite_index_id: The index id of composite index.
      has_entity_bytes: The stat has the entity_bytes property.
      has_builtin_index_stats: The stat entity has builtin_index_bytes and
        builtin_index_count.
      has_composite_index_stats: The stat entity has composite_index_bytes and
        composite_index_count.
    """
    stat = datastore.Entity(kind)
    stat['bytes'] = 4
    stat['count'] = 2
    stat['timestamp'] = datetime.datetime.utcfromtimestamp(40)
    if has_entity_bytes:
      stat['entity_bytes'] = 2
    if has_builtin_index_stats:
      stat['builtin_index_count'] = 3
      stat['builtin_index_bytes'] = 1
    if has_composite_index_stats:
      stat['composite_index_count'] = 2
      stat['composite_index_bytes'] = 1
    if kind_name is not None:
      stat['kind_name'] = kind_name
    if property_type is not None:
      stat['property_type'] = property_type
    if property_name is not None:
      stat['property_name'] = property_name
    if subject_namespace is not None:
      stat['subject_namespace'] = subject_namespace
    if composite_index_id is not None:
      stat['index_id'] = composite_index_id
    datastore.Put(stat)

  def testGlobalStat(self):
    """Test fetching the global stat singleton."""
    res = stats.GlobalStat.all().fetch(100)
    self.assertEqual(1, len(res))
    self.assertEqual(4, res[0].bytes)
    self.assertEqual(2, res[0].entity_bytes)
    self.assertEqual(3, res[0].builtin_index_count)
    self.assertEqual(1, res[0].builtin_index_bytes)
    self.assertEqual(2, res[0].composite_index_count)
    self.assertEqual(1, res[0].composite_index_bytes)

  def testNamespaceStat(self):
    """Test fetching the global stat singleton."""
    res = stats.NamespaceStat.all().fetch(100)
    self.assertEqual(1, len(res))
    self.assertEqual(4, res[0].bytes)
    self.assertEqual('name-space', res[0].subject_namespace)
    self.assertEqual(2, res[0].entity_bytes)
    self.assertEqual(3, res[0].builtin_index_count)
    self.assertEqual(1, res[0].builtin_index_bytes)
    self.assertEqual(2, res[0].composite_index_count)
    self.assertEqual(1, res[0].composite_index_bytes)

  def testKindStat(self):
    """Test fetching the Kind stats."""
    res = stats.KindStat.all().fetch(100)
    self.assertEqual(2, len(res))
    self.assertEqual('foo', res[0].kind_name)
    self.assertEqual('foo2', res[1].kind_name)
    self.assertEqual(2, res[0].entity_bytes)
    self.assertEqual(3, res[0].builtin_index_count)
    self.assertEqual(1, res[0].builtin_index_bytes)
    self.assertEqual(2, res[0].composite_index_count)
    self.assertEqual(1, res[0].composite_index_bytes)

  def testKindRootEntityStat(self):
    """Test fetching the Kind root entity stats."""
    res = stats.KindRootEntityStat.all().fetch(100)
    self.assertEqual(2, len(res))
    self.assertEqual('foo3', res[0].kind_name)
    self.assertEqual('foo4', res[1].kind_name)
    self.assertEqual(2, res[0].entity_bytes)

  def testKindNonRootEntityStat(self):
    """Test fetching the Kind non-root entity stats."""
    res = stats.KindNonRootEntityStat.all().fetch(100)
    self.assertEqual(2, len(res))
    self.assertEqual('foo5', res[0].kind_name)
    self.assertEqual('foo6', res[1].kind_name)
    self.assertEqual(2, res[0].entity_bytes)

  def testPropertyTypeStat(self):
    """Test fetching the property type stats."""
    res = stats.PropertyTypeStat.all().fetch(100)
    self.assertEqual(2, len(res))
    self.assertEqual('pt1', res[0].property_type)
    self.assertEqual('pt2', res[1].property_type)
    self.assertEqual(2, res[0].entity_bytes)
    self.assertEqual(3, res[0].builtin_index_count)
    self.assertEqual(1, res[0].builtin_index_bytes)

  def testKindPropertyTypeStat(self):
    """Test fetching the (kind, property type) stats."""
    res = stats.KindPropertyTypeStat.all().fetch(100)
    self.assertEqual(3, len(res))
    self.assertEqual('foo1', res[0].kind_name)
    self.assertEqual('pt1', res[0].property_type)
    self.assertEqual('foo1', res[1].kind_name)
    self.assertEqual('pt2', res[1].property_type)
    self.assertEqual('foo2', res[2].kind_name)
    self.assertEqual('pt2', res[2].property_type)
    self.assertEqual(2, res[0].entity_bytes)
    self.assertEqual(3, res[0].builtin_index_count)
    self.assertEqual(1, res[0].builtin_index_bytes)

    query = stats.KindPropertyTypeStat.all().filter('kind_name =', 'foo2')
    res = query.fetch(100)
    self.assertEqual(1, len(res))
    self.assertEqual('foo2', res[0].kind_name)

  def testKindPropertyNameStat(self):
    """Test fetching the (kind, property name) type stats."""
    res = stats.KindPropertyNameStat.all().fetch(100)
    self.assertEqual(3, len(res))
    self.assertEqual('foo11', res[0].kind_name)
    self.assertEqual('pn1', res[0].property_name)
    self.assertEqual('foo11', res[1].kind_name)
    self.assertEqual('pn2', res[1].property_name)
    self.assertEqual('foo21', res[2].kind_name)
    self.assertEqual('pn2', res[2].property_name)
    self.assertEqual(2, res[0].entity_bytes)
    self.assertEqual(3, res[0].builtin_index_count)
    self.assertEqual(1, res[0].builtin_index_bytes)

    query = stats.KindPropertyNameStat.all().filter('kind_name =', 'foo21')
    res = query.fetch(100)
    self.assertEqual(1, len(res))
    self.assertEqual('foo21', res[0].kind_name)

  def testKindPropertyNamePropertyTypeStat(self):
    """Test fetching the (kind, property name, property type) stats."""
    res = stats.KindPropertyNamePropertyTypeStat.all().fetch(100)
    self.assertEqual(3, len(res))
    self.assertEqual('foo12', res[0].kind_name)
    self.assertEqual('pn1', res[0].property_name)
    self.assertEqual('pt1', res[0].property_type)
    self.assertEqual('foo12', res[1].kind_name)
    self.assertEqual('pn2', res[1].property_name)
    self.assertEqual('pt2', res[1].property_type)
    self.assertEqual('foo22', res[2].kind_name)
    self.assertEqual('pn2', res[2].property_name)
    self.assertEqual('pt2', res[2].property_type)
    self.assertEqual(2, res[0].entity_bytes)
    self.assertEqual(3, res[0].builtin_index_count)
    self.assertEqual(1, res[0].builtin_index_bytes)

    query = stats.KindPropertyNamePropertyTypeStat.all()
    query.filter('kind_name =', 'foo22')
    res = query.fetch(100)
    self.assertEqual(1, len(res))
    self.assertEqual('foo22', res[0].kind_name)

  def testKindCompositeIndex(self):
    """Test fetching the (kind, composite index id) stats."""
    res = stats.KindCompositeIndexStat.all().fetch(100)
    self.assertEqual(3, len(res))
    self.assertEqual('foo12', res[0].kind_name)
    self.assertEqual(1, res[0].index_id)
    self.assertEqual('foo12', res[1].kind_name)
    self.assertEqual(2, res[1].index_id)
    self.assertEqual('foo22', res[2].kind_name)
    self.assertEqual(3, res[2].index_id)
    self.assertEqual(4, res[0].bytes)
    self.assertEqual(2, res[0].count)


if __name__ == '__main__':
  absltest.main()

