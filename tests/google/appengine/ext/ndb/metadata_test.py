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

















"""Tests for metadata.py."""

from google.appengine.api import namespace_manager
from absl.testing import absltest as unittest

from google.appengine.ext.ndb import context
from google.appengine.ext.ndb import metadata
from google.appengine.ext.ndb import model
from google.appengine.ext.ndb import tasklets
from google.appengine.ext.ndb import test_utils


class MetadataTests(test_utils.NDBTest):

  def setUp(self):
    super(MetadataTests, self).setUp()

    class Foo(model.Model):
      name = model.StringProperty()
      age = model.IntegerProperty()

    self.foo = Foo

    class Bar(model.Model):
      name = model.StringProperty()
      rate = model.IntegerProperty()

    self.bar = Bar

    class Ext(model.Expando):
      pass

    self.ext = Ext
    namespace_manager.set_namespace('')

    opts = context.ContextOptions(use_cache=True, use_memcache=True)
    tasklets.set_context(tasklets.make_context(config=opts))

  the_module = metadata

  def testGetNamespaces(self):
    self.assertEqual([], metadata.get_namespaces())
    self.foo().put()
    self.assertEqual([''], metadata.get_namespaces())
    self.assertEqual([], metadata.get_namespaces(None, ''))
    for ns in 'x', 'xyzzy', 'y', 'z':
      namespace_manager.set_namespace(ns)
      self.foo().put()
    self.assertEqual(
        ['', 'x', 'xyzzy', 'y', 'z'], metadata.get_namespaces())
    self.assertEqual(['x', 'xyzzy'], metadata.get_namespaces('x', 'y'))

  def testGetKinds(self):
    self.assertEqual([], metadata.get_kinds())
    self.foo().put()
    self.bar().put()
    self.ext().put()
    self.assertEqual(['Bar', 'Ext', 'Foo'], metadata.get_kinds())
    self.assertEqual(['Bar', 'Ext'], metadata.get_kinds('A', 'F'))
    self.assertEqual([], metadata.get_kinds(None, ''))
    namespace_manager.set_namespace('x')
    self.assertEqual([], metadata.get_kinds())
    self.foo().put()
    self.assertEqual(['Foo'], metadata.get_kinds())

  def testGetPropertiesOfKind(self):
    self.foo().put()
    self.assertEqual(['age', 'name'], metadata.get_properties_of_kind('Foo'))
    self.assertEqual(['age'], metadata.get_properties_of_kind('Foo', 'a', 'h'))
    self.assertEqual([], metadata.get_properties_of_kind('Foo', None, ''))
    e = self.ext()
    e.foo = 1
    e.bar = 2
    e.put()
    self.assertEqual(['bar', 'foo'], metadata.get_properties_of_kind('Ext'))
    namespace_manager.set_namespace('x')
    e = self.ext()
    e.one = 1
    e.two = 2
    e.put()
    self.assertEqual(['one', 'two'], metadata.get_properties_of_kind('Ext'))

  def testGetRepresentationsOfKind(self):
    e = self.ext()
    e.foo = 1
    e.bar = 'a'
    e.put()
    self.assertEqual({'foo': ['INT64'], 'bar': ['STRING']},
                     metadata.get_representations_of_kind('Ext'))
    self.assertEqual({'bar': ['STRING']},
                     metadata.get_representations_of_kind('Ext', 'a', 'e'))
    self.assertEqual({},
                     metadata.get_representations_of_kind('Ext', None, ''))
    f = self.ext()
    f.foo = 'x'
    f.bar = 2
    f.put()
    self.assertEqual({'foo': ['INT64', 'STRING'],
                      'bar': ['INT64', 'STRING']},
                     metadata.get_representations_of_kind('Ext'))

  def testDirectPropertyQueries(self):
    e = self.ext()
    e.foo = 1
    e.bar = 'a'
    e.put()
    f = self.foo(name='a', age=42)
    f.put()
    q = metadata.Property.query()
    res = q.fetch()
    expected = [
        ('Ext', 'bar'), ('Ext', 'foo'), ('Foo', 'age'), ('Foo', 'name')]
    actual = [(p.kind_name, p.property_name) for p in res]
    self.assertEqual(expected, actual)

  def testEntityGroup(self):
    """Test for EntityGroup class."""
    self.HRTest()
    foo_e = self.foo(age=11)
    foo_e.put()
    egfoo_k = metadata.EntityGroup.key_for_entity_group(foo_e.key)

    v1 = egfoo_k.get().version
    self.assertGreater(v1, 0)

    child_e = self.foo(age=22, parent=foo_e.key)
    child_e.put()
    self.assertEqual(egfoo_k,
                      metadata.EntityGroup.key_for_entity_group(child_e.key))

    self.assertGreater(egfoo_k.get().version, v1)

  def testGetEntityGroupVersion(self):
    """Test for get_entity_group_version function."""
    self.HRTest()
    foo_e = self.foo(age=11)
    foo_e.put()
    self.assertGreater(metadata.get_entity_group_version(foo_e.key), 0)


if __name__ == '__main__':
  unittest.main()
