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



"""Tests for polymorphic Datstore models."""










import google
import mox
import os

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_file_stub
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from absl.testing import absltest


class PolyModelTest(absltest.TestCase):
  """Tests the PolyModel class and its metaclass."""

  def setUp(self):
    """Set up db test harness."""

    self.original_kind_map = dict(db._kind_map)


    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    stub = datastore_file_stub.DatastoreFileStub('test_app', '/dev/null',
                                                 '/dev/null')
    stub.Clear()
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    self.mox = mox.Mox()
    os.environ['APPLICATION_ID'] = 'test_app'

  def tearDown(self):
    """Clean up test harness."""
    db.PropertiedClass._kind_map = {}
    db.PropertiedClass._kind_map.update(self.original_kind_map)

  def CreateZoo(self):
    """Create a zoo of animals for testing."""

    class Animal(polymodel.PolyModel):
      name = db.StringProperty()
    class Canine(Animal): pass
    class Dog(Canine): pass
    class Wolf(Canine): pass
    class Feline(Animal): pass
    class Cat(Feline): pass
    class Panther(Feline): pass

    Animal(name='Generic').put()
    Dog(name='Cuomo').put()
    Wolf(name='Woody').put()
    Cat(name='Vespa').put()
    Panther(name='Jack').put()

    return {'Animal': Animal,
            'Canine': Canine,
            'Dog': Dog,
            'Wolf': Wolf,
            'Feline': Feline,
            'Cat': Cat,
            'Panther': Panther,
    }

  def testAssignmentToClassProperty(self):
    """Make sure assignment to _class fails.

    Even though this is a protected property, it's best to make sure that it is
    properly protected against illegal assignment.
    """
    zoo = self.CreateZoo()

    self.assertRaises(db.DerivedPropertyError,
                      zoo['Dog'],
                      **{'class': 'Some wicked class'})

  def testPolyModelDefinition(self):
    """Tests what happens when the polymorphic class itself is initialized."""
    self.assertFalse(hasattr(polymodel.PolyModel, '__root_class__'))
    self.assertIsInstance(polymodel.PolyModel._class, db.ListProperty)
    self.assertFalse(hasattr(polymodel.PolyModel,'__class_hierarchy__'))
    self.assertRaises(NotImplementedError, polymodel.PolyModel.class_key)

  def testInstantiatePolyModel(self):
    """Tests what happens when trying to construct PolyModel base class."""
    self.assertRaises(NotImplementedError, polymodel.PolyModel)

  def testPolymorphicRootDefinition(self):
    """Tests definition of a root polymorphic model."""
    class MyRoot(polymodel.PolyModel):
      pass

    self.assertEqual(MyRoot, MyRoot.__root_class__)
    self.assertEqual('MyRoot', MyRoot.kind())
    self.assertEqual([MyRoot], MyRoot.__class_hierarchy__)
    self.assertEqual(('MyRoot',), MyRoot.class_key())
    self.assertEqual('MyRoot', MyRoot.class_name())

  def testPolymorphicLeafDefinition(self):
    """Tests definition of a leaf (non-root) polymorphic model."""
    class MyRoot(polymodel.PolyModel):
      pass

    class MyLeaf(MyRoot):
      pass

    self.assertEqual(MyRoot, MyLeaf.__root_class__)
    self.assertEqual('MyRoot', MyLeaf.kind())
    self.assertEqual([MyRoot, MyLeaf], MyLeaf.__class_hierarchy__)
    self.assertEqual(('MyRoot', 'MyLeaf'), MyLeaf.class_key())
    self.assertEqual('MyLeaf', MyLeaf.class_name())

  def testClassName(self):
    """Tests that class_name is used in key definition."""
    class MyRoot(polymodel.PolyModel):
      @classmethod
      def class_name(self):
        return 'Alternate'

    self.assertEqual(MyRoot, MyRoot.__root_class__)
    self.assertEqual('MyRoot', MyRoot.kind())
    self.assertEqual([MyRoot], MyRoot.__class_hierarchy__)
    self.assertEqual(('Alternate',), MyRoot.class_key())
    self.assertEqual('Alternate', MyRoot.class_name())

  def testStorePolymorphicClasses(self):
    """Test storing and loading polymorphic classes."""
    class MyRoot(polymodel.PolyModel):
      pass

    class MyLeaf(MyRoot):
      pass

    for cls in [MyRoot, MyLeaf]:
      instance = cls()
      instance.put()

      reloaded = db.get(instance.key())
      self.assertEqual(cls, type(reloaded))
      self.assertEqual(reloaded.key(), instance.key())

  def testPolymorphicQuery(self):
    """Test for query on root class."""
    self.CreateZoo()

    for class_name, expected in (
        ('Animal', ['Generic', 'Cuomo', 'Woody', 'Vespa', 'Jack']),
        ('Feline', ['Vespa', 'Jack']),
        ('Canine', ['Cuomo', 'Woody']),
        ('Cat', ['Vespa']),
        ('Panther', ['Jack']),
        ('Dog', ['Cuomo']),
        ('Wolf', ['Woody'])):
      query = db.GqlQuery('SELECT * FROM Animal WHERE class = :1', class_name)
      self.assertEqual(set(expected), set(o.name for o in query))

  def testAll(self):
    """Test doing a query via class object."""
    classes = self.CreateZoo()

    for class_name, expected in (
        ('Animal', ['Generic', 'Cuomo', 'Woody', 'Vespa', 'Jack']),
        ('Feline', ['Vespa', 'Jack']),
        ('Canine', ['Cuomo', 'Woody']),
        ('Cat', ['Vespa']),
        ('Panther', ['Jack']),
        ('Dog', ['Cuomo']),
        ('Wolf', ['Woody'])):
      cls = classes[class_name]
      self.assertEqual(set(expected), set(o.name for o in cls.all()))

  def testAll_KeysOnly(self):
    """Test doing a query via class object returning only keys."""
    classes = self.CreateZoo()

    for class_name, expected in (
        ('Animal', ['Generic', 'Cuomo', 'Woody', 'Vespa', 'Jack']),
        ('Feline', ['Vespa', 'Jack']),
        ('Canine', ['Cuomo', 'Woody']),
        ('Cat', ['Vespa']),
        ('Panther', ['Jack']),
        ('Dog', ['Cuomo']),
        ('Wolf', ['Woody'])):
      cls = classes[class_name]
      keys = set(e.key() for e in cls.all())
      self.assertEqual(keys, set(cls.all(keys_only=True)))

  def testGql(self):
    """Test using GQL method."""
    classes = self.CreateZoo()

    for class_name, expected, gt in (
        ('Animal', ['Woody', 'Vespa'], 'K'),
        ('Feline', ['Vespa'], 'K'),
        ('Canine', ['Woody'], 'D')):
      cls = classes[class_name]

      query = 'WHERE name > :1'
      self.assertEqual(set(expected), set(o.name for o in cls.gql(query, gt)))

  def testGqlBlank(self):
    """Test an empty gql query"""
    classes = self.CreateZoo()

    self.assertEqual(
        set(['Jack', 'Vespa']), set(o.name for o in classes['Feline'].gql('')))

  def testGqlWithOrder(self):
    """Test using GQL method with an or clause."""
    classes = self.CreateZoo()

    for class_name, expected, gt in (
        ('Animal', ['Vespa', 'Woody'], 'K'),
        ('Feline', ['Vespa'], 'K'),
        ('Canine', ['Woody'], 'D')):
      cls = classes[class_name]

      query = 'WHERE name > :1 ORDER BY name'
      self.assertEqual(expected, [o.name for o in cls.gql(query, gt)])

  def testGqlWithIn(self):
    """Test using GQL method where it generates multiple queries."""
    classes = self.CreateZoo()

    for class_name, expected in (
        ('Animal', ['Woody', 'Vespa']),
        ('Feline', ['Vespa']),
        ('Canine', ['Woody'])):
      cls = classes[class_name]

      query = "WHERE name IN ('Woody', 'Vespa')"
      self.assertEqual(set(expected), set(o.name for o in cls.gql(query)))

  def testDefaultClass(self):
    """Tests that the root class is used when missing discriminator."""
    class MyRoot(polymodel.PolyModel):
      pass

    entity = datastore.Entity('MyRoot')
    datastore.Put(entity)

    (reloaded,) = list(MyRoot.all())
    self.assertIsInstance(reloaded, MyRoot)

    (reloaded,) = list(MyRoot.gql(''))
    self.assertIsInstance(reloaded, MyRoot)

  def testBadDiscriminator(self):
    """Tests what happens when discriminator is not mapped to a class."""
    class MyRoot(polymodel.PolyModel):
      pass

    entity = datastore.Entity('MyRoot')
    entity['class'] = ['MyRoot', 'NoSuchClass']
    datastore.Put(entity)

    self.assertRaises(db.KindError, list, MyRoot.all())

  def testMixin(self):
    """Tests that PolyModel plays nice as a mixin."""
    class FunctionalBase(db.Model):
      name = db.StringProperty()

    class PolyBase(FunctionalBase, polymodel.PolyModel):
      age = db.IntegerProperty()

    class PolyClass(PolyBase):
      number = db.IntegerProperty()

    poly_base = PolyBase(name='Vespa', age=5)
    poly_class = PolyClass(name='Jack', age=9)

    poly_base_key = poly_base.put()
    poly_class_key = poly_class.put()

    bases = tuple(PolyBase.all())
    classes = tuple(PolyClass.all())

    self.assertEqual(
        set([poly_base_key, poly_class_key]), set(e.key() for e in bases))
    self.assertEqual(set([poly_class_key]), set(e.key() for e in classes))

  def testAlternateMixinInheritanceOrders(self):
    """Tests different orders that PolyModel can be mixed in."""
    class FunctionalBase1(db.Model):
      b1 = db.StringProperty()
    class FunctionalBase2(db.Model):
      b2 = db.StringProperty()

    def reload_test(polymodel):
      instance = polymodel(b1='string1', b2='string2')
      instance.put()

      reloaded = db.get(instance.key())
      self.assertEqual('string1', reloaded.b1)
      self.assertEqual('string2', reloaded.b2)
      self.assertIsInstance(reloaded, polymodel)

    class PolyBase1(FunctionalBase1, polymodel.PolyModel): pass
    class PolySub1_1(FunctionalBase2, PolyBase1): pass
    class PolySub1_2(PolyBase1, FunctionalBase2): pass

    class PolyBase2(polymodel.PolyModel, FunctionalBase1): pass
    class PolySub2_1(FunctionalBase2, PolyBase2): pass
    class PolySub2_2(PolyBase2, FunctionalBase2): pass


    pb1 = PolyBase1().put()
    ps1_1 = PolySub1_1().put()
    ps1_2 = PolySub1_2().put()

    pb2 = PolyBase2().put()
    ps2_1 = PolySub2_1().put()
    ps2_2 = PolySub2_2().put()

    def keys(query):
      key_list = list([i.key() for i in query])
      return sorted(key_list)

    self.assertEqual(sorted([pb1, ps1_1, ps1_2]), keys(PolyBase1.all()))
    self.assertEqual(sorted([ps1_1]), keys(PolySub1_1.all()))
    self.assertEqual(sorted([ps1_2]), keys(PolySub1_2.all()))

    self.assertEqual(sorted([pb2, ps2_1, ps2_2]), keys(PolyBase2.all()))
    self.assertEqual(sorted([ps2_1]), keys(PolySub2_1.all()))
    self.assertEqual(sorted([ps2_2]), keys(PolySub2_2.all()))


    for cls in (PolySub1_1, PolySub1_2,
                PolySub2_1, PolySub2_2):
      reload_test(cls)

  def testMultiPolyModel(self):
    """Tests that class cannot inherit from PolyModel twice."""
    class Root1(polymodel.PolyModel):
      pass

    class Root2(polymodel.PolyModel):
      pass

    def create_multi_poly_model():
      class MultiPolyModel(Root1, Root2):
        pass
    self.assertRaises(db.ConfigurationError, create_multi_poly_model)

  def assertReverseMRO(self, cls):
    i = 0
    for c in reversed(cls.mro()):
      if issubclass(c, polymodel.PolyModel) and c != polymodel.PolyModel:
        self.assertEqual(c, cls.__class_hierarchy__[i])
        i += 1

  def testMultipleInheritance(self):
    """Tests that diamond inheritance functions properly"""
    class Root(polymodel.PolyModel):
      pass

    class Mixin1a(Root):
      pass

    class Mixin1b(Root):
      pass

    class Mixin1c(Root):
      pass

    class Mixin2a(Mixin1a, Mixin1b):
      pass

    class Mixin2b(Mixin1b, Mixin1a):
      pass

    class Mixin3a(Mixin2a, Mixin1c):
      pass


    self.assertEqual(Mixin2a.kind(), Root.kind())
    self.assertEqual(Mixin2b.kind(), Root.kind())
    self.assertEqual(Mixin3a.kind(), Root.kind())
    self.assertEqual(db._kind_map[Root.kind()], Root)

    self.assertReverseMRO(Mixin1a)
    self.assertReverseMRO(Mixin2a)
    self.assertReverseMRO(Mixin2b)
    self.assertReverseMRO(Mixin3a)

    def create_bad_order_mixin_1(self):
      class BadMixin(Mixin1a, Mixin2a):
        pass

    def create_bad_order_mixin_2(self):
      class BadMixin(Mixin2a, Mixin2b):
        pass

    self.assertRaises(TypeError, create_bad_order_mixin_1)
    self.assertRaises(TypeError, create_bad_order_mixin_2)

    def create_bad_root():
      class BadRoot(Mixin2a, polymodel.PolyModel):
        pass

    self.assertRaises(db.ConfigurationError, create_bad_root)

  def testPropertyNamedCls(self):
    """Tests whether it's okay to have a property named 'cls'."""



    class ModelWithClsField(polymodel.PolyModel):
      cls = db.StringProperty()
      prop = db.StringProperty()


    strange = ModelWithClsField(cls='foo', prop='bar')
    self.assertEqual('foo', strange.cls)
    self.assertEqual('bar', strange.prop)


    ModelWithClsField.__new__(ModelWithClsField, prop='bar')



    ModelWithClsField.__new__(ModelWithClsField, cls='foo', prop='bar')



    self.assertRaisesRegex(
        TypeError,
        'object.__new__\(\): not enough arguments',
        ModelWithClsField.__new__, cls=ModelWithClsField)


if __name__ == '__main__':
  absltest.main()

