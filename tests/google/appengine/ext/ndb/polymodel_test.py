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














"""Tests for polymodel.py.

See issue 35.  http://goo.gl/iHkCm
"""

import pickle

from google.appengine.ext.ndb import model
from google.appengine.ext.ndb import polymodel
from google.appengine.ext.ndb import query
from google.appengine.ext.ndb import test_utils

from google.appengine.api import datastore_types
from absl.testing import absltest as unittest


PolyModel = polymodel.PolyModel


class PolyModelTests(test_utils.NDBTest):

  def setUp(self):
    super(PolyModelTests, self).setUp()

  the_module = polymodel

  def testBasics(self):

    class Shoe(PolyModel):
      color = model.StringProperty()

    class Moccasin(Shoe):
      leather = model.StringProperty()

    class Sneaker(Shoe):
      pump = model.BooleanProperty()

    self.assertEqual(Shoe._class_name(), 'Shoe')
    self.assertEqual(Shoe._class_key(), ['Shoe'])
    self.assertEqual(Moccasin._class_name(), 'Moccasin')
    self.assertEqual(Moccasin._class_key(), ['Shoe', 'Moccasin'])
    self.assertEqual(Sneaker._class_name(), 'Sneaker')
    self.assertEqual(Sneaker._class_key(), ['Shoe', 'Sneaker'])

    s_key = model.Key('Shoe', 1)
    self.assertEqual(Shoe().put(), s_key)
    s = s_key.get()
    self.assertEqual(s._get_kind(), 'Shoe')
    self.assertEqual(s._class_key(), ['Shoe'])
    self.assertEqual(s.class_, ['Shoe'])

    m_key = model.Key('Shoe', 2)
    self.assertEqual(Moccasin(color='brown', leather='cattlehide').put(),
                     m_key)
    m = m_key.get()
    self.assertEqual(m._get_kind(), 'Shoe')
    self.assertEqual(m.class_, ['Shoe', 'Moccasin'])

    snkr_key = model.Key('Shoe', 3)
    self.assertEqual(Sneaker(color='red', pump=False).put(), snkr_key)
    snkr = snkr_key.get()
    self.assertEqual(snkr._get_kind(), 'Shoe')
    self.assertEqual(snkr.class_, ['Shoe', 'Sneaker'])

    self.assertEqual(Shoe.query().fetch(), [s, m, snkr])
    self.assertEqual(Shoe.query(Sneaker.pump == False).fetch(), [snkr])
    self.assertEqual(Moccasin.query().fetch(), [m])
    self.assertEqual(Sneaker.query().fetch(), [snkr])

  def testBlobKeyProperty(self):
    class MyModel(PolyModel):
      pass

    class MyDerivedModel(MyModel):
      image = model.BlobKeyProperty()

    test_blobkey = datastore_types.BlobKey('testkey123')
    m = MyDerivedModel()
    m.image = test_blobkey
    m.put()

    m = m.key.get()
    m.image = test_blobkey
    m.put()

    self.assertTrue(isinstance(m.image, datastore_types.BlobKey))
    self.assertEqual(str(m.image), str(test_blobkey))

  def testClassKeyProperty(self):

    class Animal(PolyModel):
      pass

    class Dog(Animal):
      pass
    fido = Dog()
    self.assertEqual(fido.class_, ['Animal', 'Dog'])
    self.assertRaises(TypeError, setattr, fido, 'class_', ['Animal', 'Dog'])

  def testPolyExpando(self):


    class Animal(PolyModel, model.Expando):
      pass

    class Mammal(Animal):
      pass
    cat = Mammal(name=b'Tom', naps=18, sound=b'purr')
    cat1 = cat.put().get()
    self.assertFalse(cat1 is cat)
    self.assertEqual(cat1, cat)
    self.assertEqual(cat1.name, b'Tom')
    self.assertEqual(cat1.naps, 18)
    self.assertEqual(cat1.sound, b'purr')

  def testExpandoPoly(self):



    class Animal(model.Expando, PolyModel):
      pass

    class Mammal(Animal):
      pass

    expected = Mammal(name=b'Tom', naps=18, sound=b'purr')
    actual = expected.put().get()

    self.assertIsNot(expected, actual)
    self.assertEqual(expected, actual)
    self.assertEqual(b'Tom', actual.name)
    self.assertEqual(18, actual.naps)
    self.assertEqual(b'purr', actual.sound)

  def testInheritance(self):

    class NamedThing(model.Model):
      name = model.StringProperty()

    class Animal(PolyModel, NamedThing):
      legs = model.IntegerProperty(default=4)

    class Canine(Animal):
      pass

    class Dog(Canine):
      breed = model.StringProperty(default='mutt')

    class Wolf(Canine):
      mythical = model.BooleanProperty(default=False)

    class Feline(Animal):
      sound = model.StringProperty()

    class Cat(Feline):
      naps = model.IntegerProperty()

    class Panther(Feline):
      pass

    class Monster(Dog, Cat):
      ancestry = model.StringProperty()

    class Ghoul(Monster, model.Expando):
      pass

    expected_k9 = Canine(name='Reynard')
    self.assertEqual(expected_k9.legs, 4)
    self.assertEqual(expected_k9._get_kind(), 'Animal')
    self.assertEqual(expected_k9._class_name(), 'Canine')
    self.assertEqual(expected_k9._class_key(), ['Animal', 'Canine'])

    expected_cat = Cat(name='Tom', naps=12, sound='purr')
    self.assertIsInstance(expected_cat, Cat)
    self.assertIsInstance(expected_cat, Feline)
    self.assertIsInstance(expected_cat, Animal)
    self.assertIsInstance(expected_cat, PolyModel)
    self.assertEqual(expected_cat.naps, 12)
    self.assertEqual(expected_cat.sound, 'purr')
    self.assertEqual(expected_cat.legs, 4)
    self.assertEqual(expected_cat._get_kind(), 'Animal')
    self.assertEqual(expected_cat._class_name(), 'Cat')
    self.assertEqual(expected_cat._class_key(), ['Animal', 'Feline', 'Cat'])

    expected_wolf = Wolf(name='Warg')
    self.assertEqual(expected_wolf._get_kind(), 'Animal')
    self.assertEqual(expected_wolf._class_name(), 'Wolf')
    self.assertEqual(
        expected_wolf._class_key(), ['Animal', 'Canine', 'Wolf'])
    self.assertRaises(AttributeError, lambda: expected_wolf.breed)

    expected_ghoul = Ghoul(name='Westminster', book=b'The Graveyard Book')
    self.assertEqual(expected_ghoul.ancestry, None)
    self.assertEqual(expected_ghoul._get_kind(), 'Animal')
    self.assertEqual(expected_ghoul._class_name(), 'Ghoul')
    self.assertEqual(
        expected_ghoul._class_key(),
        ['Animal', 'Feline', 'Cat', 'Canine', 'Dog', 'Monster', 'Ghoul'])

    actual_k9 = expected_k9.put().get()
    self.assertIsInstance(expected_k9, Canine)
    self.assertEqual(expected_k9.name, 'Reynard')
    self.assertEqual(expected_k9._get_kind(), 'Animal')
    self.assertEqual(expected_k9._class_name(), 'Canine')
    self.assertEqual(expected_k9._class_key(), ['Animal', 'Canine'])
    self.assertIsInstance(actual_k9, Canine)
    self.assertEqual(actual_k9.name, 'Reynard')
    self.assertEqual(actual_k9._get_kind(), 'Animal')
    self.assertEqual(actual_k9._class_name(), 'Canine')
    self.assertEqual(actual_k9._class_key(), ['Animal', 'Canine'])
    self.assertEqual(actual_k9, expected_k9)

    actual_cat = expected_cat.put().get()
    self.assertEqual(actual_cat, expected_cat)
    actual_wolf = expected_wolf.put().get()
    self.assertEqual(actual_wolf, expected_wolf)
    actual_ghoul = expected_ghoul.put().get()
    self.assertEqual(actual_ghoul, expected_ghoul)
    self.assertEqual(actual_ghoul.book, b'The Graveyard Book')

  def testPickling(self):


    global Animal, Dog


    class Animal(PolyModel):
      name = model.StringProperty()

    class Dog(Animal):
      breed = model.StringProperty()
    for proto in 0, 1, 2:
      fido = Dog(name='Fido', breed='chihuahua')
      s = pickle.dumps(fido, proto)
      fido1 = pickle.loads(s)
      self.assertEqual(fido1.name, 'Fido')
      self.assertEqual(fido1.breed, 'chihuahua')
      self.assertEqual(fido1.class_, ['Animal', 'Dog'])
      self.assertEqual(fido, fido1)

  def testClassNameOverride(self):

    class Animal(PolyModel):
      pass

    class Feline(Animal):
      pass

    class Cat(Feline):

      @classmethod
      def _class_name(cls):
        return 'Pussycat'
    tom = Cat()
    self.assertEqual(tom.class_, ['Animal', 'Feline', 'Pussycat'])
    tom.put()
    expected = [tom]
    actual = Cat.query().fetch()
    self.assertEqual(expected, actual)

  def testEdgeCases(self):

    self.assertEqual(PolyModel._get_kind(), 'PolyModel')

  def testMixins(self):
    class Mixin(object):
      pass

    class Entity(polymodel.PolyModel):
      pass

    class ChildEntity(Entity):
      pass

    class RightMixinEntity(Entity, Mixin):
      pass

    class LeftMixinEntity(Mixin, Entity):
      pass
    self.assertEqual(Entity._get_kind(), 'Entity')
    self.assertEqual(ChildEntity._get_kind(), 'Entity')
    self.assertEqual(RightMixinEntity._get_kind(), 'Entity')
    self.assertEqual(LeftMixinEntity._get_kind(), 'Entity')

  def testGql(self):

    class A(polymodel.PolyModel):
      pass

    class B(A):
      pass

    class C(A):
      pass
    b = B()
    b.put()
    c = C()
    c.put()
    self.assertEqual(query.gql('SELECT * FROM A').fetch(), [b, c])
    self.assertEqual(B.gql('').fetch(), [b])
    self.assertEqual(query.gql('SELECT * FROM B').fetch(), [b])

  def testQueryFilter(self):

    class Animal(PolyModel):
      pass

    class Cat(Animal):
      pass
    self.assertEqual(Animal.query().filters, None)
    self.assertNotEqual(Cat.query().filters, None)

  def testEqualityAfterPut(self):
    """ See https://github.com/GoogleCloudPlatform/appengine-python-standard/issues/89 """
    class Animal(PolyModel):
      pass

    a = Animal(id=1)
    b = Animal(id=1)
    a.put()

    self.assertEqual(a, b)


TOM_PB2 = """\
key {
  app: "ndb-test-app-id"
  path {
    Element {
      type: "Animal"
    }
  }
}
property {
  name: "class"
  multiple: true
  value {
    stringValue: "Animal"
  }
}
property {
  name: "class"
  multiple: true
  value {
    stringValue: "Feline"
  }
}
property {
  name: "class"
  multiple: true
  value {
    stringValue: "Cat"
  }
}
property {
  name: "name"
  multiple: false
  value {
    stringValue: "Tom"
  }
}
property {
  name: "purr"
  multiple: false
  value {
    stringValue: "loud"
  }
}
property {
  name: "whiskers"
  multiple: false
  value {
    booleanValue: true
  }
}
entity_group {
}
"""

TOM_PB1 = """\
key <
  app: "ndb-test-app-id"
  path <
    Element {
      type: "Animal"
    }
  >
>
entity_group <
>
property <
  name: "class"
  value <
    stringValue: "Animal"
  >
  multiple: true
>
property <
  name: "class"
  value <
    stringValue: "Feline"
  >
  multiple: true
>
property <
  name: "class"
  value <
    stringValue: "Cat"
  >
  multiple: true
>
property <
  name: "name"
  value <
    stringValue: "Tom"
  >
  multiple: false
>
property <
  name: "purr"
  value <
    stringValue: "loud"
  >
  multiple: false
>
property <
  name: "whiskers"
  value <
    booleanValue: true
  >
  multiple: false
>
"""


class CompatibilityTests(test_utils.NDBTest):

  def testCompatibility(self):
    class Animal(PolyModel):
      name = model.StringProperty()

    class Feline(Animal):
      whiskers = model.BooleanProperty()

    class Cat(Feline):
      purr = model.StringProperty()
    tom = Cat(name='Tom', purr='loud', whiskers=True)
    tom._prepare_for_put()
    try:
      self.assertEqual(str(tom._to_pb()), TOM_PB2)
    except AssertionError:


      self.assertEqual(str(tom._to_pb()), TOM_PB1)


if __name__ == '__main__':
  unittest.main()
