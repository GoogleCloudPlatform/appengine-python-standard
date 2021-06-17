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















"""Tests for key.py."""

import base64
import collections
import datetime
import os
import pickle
import sortedcontainers

from google.appengine.ext.ndb import key
from google.appengine.ext.ndb import model
from google.appengine.ext.ndb import tasklets
from google.appengine.ext.ndb import test_utils
import six
from six.moves import range
from six.moves import zip

from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.datastore import entity_bytes_pb2 as entity_pb2
from absl.testing import absltest as unittest


class KeyTests(test_utils.NDBTest):

  the_module = key

  def testShort(self):
    k0 = key.Key('Kind', None)
    self.assertEqual(k0.flat(), ('Kind', None))
    k1 = key.Key('Kind', 1)
    self.assertEqual(k1.flat(), ('Kind', 1))
    k2 = key.Key('Parent', 42, 'Kind', 1)
    self.assertEqual(k2.flat(), ('Parent', 42, 'Kind', 1))

  def testFlat(self):
    flat = ('Kind', 1)
    pairs = tuple((flat[i], flat[i + 1]) for i in range(0, len(flat), 2))
    k = key.Key(flat=flat)
    self.assertEqual(k.pairs(), pairs)
    self.assertEqual(k.flat(), flat)
    self.assertEqual(k.kind(), 'Kind')

  def testFlatLong(self):
    flat = ('Kind', 1, 'Subkind', 'foobar')
    pairs = tuple((flat[i], flat[i + 1]) for i in range(0, len(flat), 2))
    k = key.Key(flat=flat)
    self.assertEqual(k.pairs(), pairs)
    self.assertEqual(k.flat(), flat)
    self.assertEqual(k.kind(), 'Subkind')

  def testSerialized(self):
    flat = ['Kind', 1, 'Subkind', 'foobar']
    r = entity_pb2.Reference()
    r.app = 'ndb-test-app-id'
    e = r.path.element.add()
    e.type = flat[0]
    e.id = flat[1]
    e = r.path.element.add()
    e.type = flat[2]
    e.name = flat[3]
    serialized = r.SerializeToString()
    ref_bytes = six.ensure_binary(r.SerializeToString())
    urlsafe = base64.urlsafe_b64encode(ref_bytes).rstrip(b'=')

    k = key.Key(flat=flat)
    self.assertEqual(k.serialized(), serialized)
    self.assertEqual(k.urlsafe(), urlsafe)
    self.assertEqual(k.reference(), r)

    k = key.Key(urlsafe=urlsafe)
    self.assertEqual(k.serialized(), serialized)
    self.assertEqual(k.urlsafe(), urlsafe)
    self.assertEqual(k.reference(), r)

    k = key.Key(serialized=serialized)
    self.assertEqual(k.serialized(), serialized)
    self.assertEqual(k.urlsafe(), urlsafe)
    self.assertEqual(k.reference(), r)

    k = key.Key(reference=r)
    self.assertIsNot(k.reference(), r)
    self.assertEqual(k.serialized(), serialized)
    self.assertEqual(k.urlsafe(), urlsafe)
    self.assertEqual(k.reference(), r)

    k = key.Key(reference=r, app=r.app, namespace='')
    self.assertIsNot(k.reference(), r)
    self.assertEqual(k.serialized(), serialized)
    self.assertEqual(k.urlsafe(), urlsafe)
    self.assertEqual(k.reference(), r)

    k1 = key.Key('A', 1)
    self.assertEqual(k1.urlsafe(), b'ag9uZGItdGVzdC1hcHAtaWRyBwsSAUEYAQw')
    k2 = key.Key(urlsafe=k1.urlsafe())
    self.assertEqual(k1, k2)

  def testId(self):
    k1 = key.Key('Kind', 'foo', app='app1', namespace='ns1')
    self.assertEqual(k1.id(), 'foo')

    k2 = key.Key('Subkind', 42, parent=k1)
    self.assertEqual(k2.id(), 42)

    k3 = key.Key('Subkind', 'bar', parent=k2)
    self.assertEqual(k3.id(), 'bar')


    k4 = key.Key('Subkind', None, parent=k3)
    self.assertEqual(k4.id(), None)

  def testIdentity(self):
    test_kind, test_id = 'test-kind', 'test-id'
    k = key.Key(test_kind, test_id)

    with self.subTest(name='Kind'):
      self.assertEqual(k.kind(), test_kind)

    with self.subTest(name='ID'):
      self.assertEqual(k.id(), test_id)

  def testStringId(self):
    k1 = key.Key('Kind', 'foo', app='app1', namespace='ns1')
    self.assertEqual(k1.string_id(), 'foo')

    k2 = key.Key('Subkind', 'bar', parent=k1)
    self.assertEqual(k2.string_id(), 'bar')

    k3 = key.Key('Subkind', 42, parent=k2)
    self.assertEqual(k3.string_id(), None)


    k4 = key.Key('Subkind', None, parent=k3)
    self.assertEqual(k4.string_id(), None)

  def testIntegerId(self):
    k1 = key.Key('Kind', 42, app='app1', namespace='ns1')
    self.assertEqual(k1.integer_id(), 42)

    k2 = key.Key('Subkind', 43, parent=k1)
    self.assertEqual(k2.integer_id(), 43)

    k3 = key.Key('Subkind', 'foobar', parent=k2)
    self.assertEqual(k3.integer_id(), None)


    k4 = key.Key('Subkind', None, parent=k3)
    self.assertEqual(k4.integer_id(), None)

  def testParent(self):
    p = key.Key('Kind', 1, app='app1', namespace='ns1')
    self.assertEqual(p.parent(), None)

    k = key.Key('Subkind', 'foobar', parent=p)
    self.assertEqual(k.flat(), ('Kind', 1, 'Subkind', 'foobar'))
    self.assertEqual(k.parent(), p)

    k = key.Key(
        'Subkind', 'foobar', parent=p, app=p.app(), namespace=p.namespace())
    self.assertEqual(k.flat(), ('Kind', 1, 'Subkind', 'foobar'))
    self.assertEqual(k.parent(), p)

  def testRoot(self):
    p = key.Key('Kind', 1, app='app1', namespace='ns1')
    self.assertEqual(p.root(), p)

    k = key.Key('Subkind', 'foobar', parent=p)
    self.assertEqual(k.flat(), ('Kind', 1, 'Subkind', 'foobar'))
    self.assertEqual(k.root(), p)

    k2 = key.Key(
        'Subsubkind', 42, parent=k, app=p.app(), namespace=p.namespace())
    self.assertEqual(k2.flat(),
                     ('Kind', 1, 'Subkind', 'foobar', 'Subsubkind', 42))
    self.assertEqual(k2.root(), p)

  def testRepr_Inferior(self):
    k = key.Key('Kind', 1, 'Subkind', 'foobar')
    self.assertEqual(repr(k), "Key('Kind', 1, 'Subkind', 'foobar')")
    self.assertEqual(repr(k), str(k))

  def testRepr_Toplevel(self):
    k = key.Key('Kind', 1)
    self.assertEqual(repr(k), "Key('Kind', 1)")

  def testRepr_Incomplete(self):
    k = key.Key('Kind', None)
    self.assertEqual(repr(k), "Key('Kind', None)")

  def testRepr_UnicodeKind(self):
    k = key.Key(u'\u1234', 1)
    if six.PY2:
      self.assertEqual(repr(k), "Key('\\xe1\\x88\\xb4', 1)")
    else:
      self.assertEqual(repr(k), u"Key('\u1234', 1)")

  def testRepr_UnicodeId(self):
    k = key.Key('Kind', u'\u1234')
    if six.PY2:
      self.assertEqual(repr(k), "Key('Kind', '\\xe1\\x88\\xb4')")
    else:
      self.assertEqual(repr(k), u"Key('Kind', '\u1234')")

  def testRepr_App(self):
    k = key.Key('Kind', 1, app='foo')
    self.assertEqual(repr(k), "Key('Kind', 1, app='foo')")

  def testRepr_Namespace(self):
    k = key.Key('Kind', 1, namespace='foo')
    self.assertEqual(repr(k), "Key('Kind', 1, namespace='foo')")

  def testUnicode(self):
    flat_input = (u'Kind\u1234', 1, 'Subkind', u'foobar\u4321')
    flat = (six.ensure_str(flat_input[0]), flat_input[1], flat_input[2],
            six.ensure_str(flat_input[3]))
    pairs = tuple((flat[i], flat[i + 1]) for i in range(0, len(flat), 2))
    k = key.Key(flat=flat_input)
    self.assertEqual(k.pairs(), pairs)
    self.assertEqual(k.flat(), flat)

    r = k.reference()
    serialized = k.serialized()
    urlsafe = k.urlsafe()
    key.Key(urlsafe=urlsafe.decode('utf8'))
    key.Key(serialized=serialized.decode('utf8'))
    key.Key(reference=r)

    r = entity_pb2.Reference()
    r.app = 'ndb-test-app-id'
    e = r.path.element.add()
    e.type = flat[0]
    e.name = flat[3]
    k = key.Key(reference=r)
    self.assertEqual(k.reference(), r)

  def testHash(self):
    flat = ['Kind', 1, 'Subkind', 'foobar']
    pairs = [(flat[i], flat[i + 1]) for i in range(0, len(flat), 2)]
    k = key.Key(flat=flat)
    self.assertEqual(hash(k), hash(tuple(pairs)))

  def testOrdering(self):

    a = key.Key(app='app2', namespace='ns2', flat=('kind1', 1))
    b = key.Key(app='app2', namespace='ns1', flat=('kind1', 1))
    c = key.Key(app='app1', namespace='ns1', flat=('kind1', 1))
    d = key.Key(app='app1', namespace='ns1', flat=('kind1', 2))
    e = key.Key(app='app1', namespace='ns1', flat=('kind1', 'e'))
    f = key.Key(app='app1', namespace='ns1', flat=('kind1', 'f'))
    g = key.Key(app='app1', namespace='ns1', flat=('kind2', 'f', 'x', 1))
    h = key.Key(app='app1', namespace='ns1', flat=('kind2', 'f', 'x', 2))

    expected = [c, d, e, f, g, h, b, a]
    actual = sorted([a, b, c, d, e, f, g, h])
    self.assertEqual(actual, expected)

    for i in range(len(actual)):
      for j in range(len(actual)):
        self.assertEqual(actual[i] < actual[j], i < j)
        self.assertEqual(actual[i] <= actual[j], i <= j)
        self.assertEqual(actual[i] > actual[j], i > j)
        self.assertEqual(actual[i] >= actual[j], i >= j)
        self.assertEqual(actual[i] == actual[j], i == j)
        self.assertEqual(actual[i] != actual[j], i != j)

  def testUniqueIncomplete(self):
    p0 = None
    p1 = key.Key('bar', 1)
    for p in p0, p1:
      a = key.Key('foo', 0, parent=p)
      b = key.Key('foo', '', parent=p)
      c = key.Key('foo', None, parent=p)
      self.assertEqual(a, b)
      self.assertEqual(b, c)
      self.assertEqual(c, a)
      for x in a, b, c:
        self.assertEqual(x.id(), None)
        self.assertEqual(x.string_id(), None)
        self.assertEqual(x.integer_id(), None)
        self.assertEqual(x.pairs()[-1], ('foo', None))
        self.assertEqual(x.flat()[-1], None)
        self.assertEqual(x.urlsafe(), c.urlsafe())

  def testIncomplete(self):
    key.Key(flat=['Kind', None])
    self.assertRaises(
        datastore_errors.BadArgumentError,
        key.Key,
        flat=['Kind', None, 'Subkind', 1])
    self.assertRaises(TypeError, key.Key, flat=['Kind', ()])

  def testKindFromModel(self):

    class M(model.Model):
      pass

    class N(model.Model):

      @classmethod
      def _get_kind(cls):
        return 'NN'

    k = key.Key(M, 1)
    self.assertEqual(k, key.Key('M', 1))
    k = key.Key('X', 1, N, 2, 'Y', 3)
    self.assertEqual(k, key.Key('X', 1, 'NN', 2, 'Y', 3))

  def testKindFromBadValue(self):

    self.assertRaises(Exception, key.Key, 42, 42)

  def testDeleteHooksCalled(self):
    test = self
    self.pre_counter = 0
    self.post_counter = 0

    class HatStand(model.Model):

      @classmethod
      def _pre_delete_hook(cls, key):
        test.pre_counter += 1
        if test.pre_counter == 1:
          self.assertEqual(self.key, key)

      @classmethod
      def _post_delete_hook(cls, key, future):
        test.post_counter += 1
        self.assertEqual(self.key, key)
        self.assertIs(future.get_result(), None)

    furniture = HatStand()
    key = furniture.put()
    self.key = key
    self.assertEqual(self.pre_counter, 0, 'Pre delete hook called early')
    future = key.delete_async()
    self.assertEqual(self.pre_counter, 1, 'Pre delete hook not called')
    self.assertEqual(self.post_counter, 0, 'Post delete hook called early')
    future.get_result()
    self.assertEqual(self.post_counter, 1, 'Post delete hook not called')


    new_furniture = [HatStand() for _ in range(10)]
    keys = [furniture.put() for furniture in new_furniture]
    multi_future = model.delete_multi_async(keys)
    self.assertEqual(self.pre_counter, 11,
                     'Pre delete hooks not called on delete_multi')
    self.assertEqual(self.post_counter, 1,
                     'Post delete hooks called early on delete_multi')
    for fut, key in zip(multi_future, keys):
      self.key = key
      fut.get_result()
    self.assertEqual(self.post_counter, 11,
                     'Post delete hooks not called on delete_multi')

  def testNoDefaultDeleteCallback(self):

    ctx = tasklets.get_context()
    ctx.set_cache_policy(False)

    class EmptyModel(model.Model):
      pass

    entity = EmptyModel()
    entity.put()
    fut = entity.key.delete_async()
    self.assertFalse(fut._immediate_callbacks,
                     'Delete hook queued default no-op.')

  def testGetHooksCalled(self):
    test = self
    self.pre_counter = 0
    self.post_counter = 0

    class HatStand(model.Model):

      @classmethod
      def _pre_get_hook(cls, key):
        test.pre_counter += 1
        if test.pre_counter == 1:
          self.assertEqual(key, self.key)

      @classmethod
      def _post_get_hook(cls, key, future):
        test.post_counter += 1
        self.assertEqual(key, self.key)
        self.assertEqual(future.get_result(), self.entity)

    furniture = HatStand()
    self.entity = furniture
    key = furniture.put()
    self.key = key
    self.assertEqual(self.pre_counter, 0, 'Pre get hook called early')
    future = key.get_async()
    self.assertEqual(self.pre_counter, 1, 'Pre get hook not called')
    self.assertEqual(self.post_counter, 0, 'Post get hook called early')
    future.get_result()
    self.assertEqual(self.post_counter, 1, 'Post get hook not called')


    new_furniture = [HatStand() for _ in range(10)]
    keys = [furniture.put() for furniture in new_furniture]
    multi_future = model.get_multi_async(keys)
    self.assertEqual(self.pre_counter, 11,
                     'Pre get hooks not called on get_multi')
    self.assertEqual(self.post_counter, 1,
                     'Post get hooks called early on get_multi')
    for fut, key, entity in zip(multi_future, keys, new_furniture):
      self.key = key
      self.entity = entity
      fut.get_result()
    self.assertEqual(self.post_counter, 11,
                     'Post get hooks not called on get_multi')

  def testMonkeyPatchHooks(self):
    hook_attr_names = ('_pre_get_hook', '_post_get_hook', '_pre_delete_hook',
                       '_post_delete_hook')
    original_hooks = {}


    for name in hook_attr_names:
      original_hooks[name] = getattr(model.Model, name)

    self.pre_get_flag = False
    self.post_get_flag = False
    self.pre_delete_flag = False
    self.post_delete_flag = False


    class HatStand(model.Model):

      @classmethod
      def _pre_get_hook(cls, unused_key):
        self.pre_get_flag = True

      @classmethod
      def _post_get_hook(cls, unused_key, unused_future):
        self.post_get_flag = True

      @classmethod
      def _pre_delete_hook(cls, unused_key):
        self.pre_delete_flag = True

      @classmethod
      def _post_delete_hook(cls, unused_key, unused_future):
        self.post_delete_flag = True


    for name in hook_attr_names:
      hook = getattr(HatStand, name)
      setattr(model.Model, name, hook)

    try:
      key = HatStand().put()
      key.get()
      self.assertTrue(self.pre_get_flag,
                      'Pre get hook not called when model is monkey patched')
      self.assertTrue(self.post_get_flag,
                      'Post get hook not called when model is monkey patched')
      key.delete()
      self.assertTrue(
          self.pre_delete_flag,
          'Pre delete hook not called when model is monkey patched')
      self.assertTrue(
          self.post_delete_flag, 'Post delete hook not called when model '
          'is monkey patched')
    finally:

      for name in hook_attr_names:
        setattr(model.Model, name, original_hooks[name])

  def testPreHooksCannotCancelRPC(self):

    class Foo(model.Model):

      @classmethod
      def _pre_get_hook(cls, unused_key):
        raise tasklets.Return()

      @classmethod
      def _pre_delete_hook(cls, unused_key):
        raise tasklets.Return()

    entity = Foo()
    entity.put()
    self.assertRaises(tasklets.Return, entity.key.get)
    self.assertRaises(tasklets.Return, entity.key.delete)

  def testNoDefaultGetCallback(self):

    ctx = tasklets.get_context()
    ctx.set_cache_policy(False)

    class EmptyModel(model.Model):
      pass

    entity = EmptyModel()
    entity.put()
    fut = entity.key.get_async()
    self.assertFalse(fut._immediate_callbacks, 'Get hook queued default no-op.')

  def testFromOldKey(self):
    old_key = datastore_types.Key.from_path('TestKey', 1234)
    new_key = key.Key.from_old_key(old_key)
    self.assertEqual(str(old_key), six.ensure_text(new_key.urlsafe()))

    old_key2 = new_key.to_old_key()
    self.assertEqual(old_key, old_key2)



Snapshot = collections.namedtuple('Snapshot', ['snapshot_key', 'created_on'])


class KeyPickleTests(test_utils.NDBTest):
  """Tests for key pickling."""

  def setUp(self):
    super(KeyPickleTests, self).setUp()
    self.keys = [
        key.Key(flat=['Kind', 1]),
        key.Key(flat=['Kind', 1, 'Subkind', 'foobar']),
        key.Key(
            flat=['Kind', 1, 'Subkind', 'foobar'],
            namespace='ns',
            app='a-different-app')
    ]



    self.pkeys = [
        [
            b"ccopy_reg\n_reconstructor\np0\n(cgoogle.appengine.ext.ndb.key\nKey\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n((dp5\nS'namespace'\np6\nS''\np7\nsS'app'\np8\nS'ndb-test-app-id'\np9\nsS'pairs'\np10\n(lp11\n(S'Kind'\np12\nI1\ntp13\nastp14\nb.",
            b"ccopy_reg\n_reconstructor\np0\n(cgoogle.appengine.ext.ndb.key\nKey\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n((dp5\nS'namespace'\np6\nS''\np7\nsS'app'\np8\nS'ndb-test-app-id'\np9\nsS'pairs'\np10\n(lp11\n(S'Kind'\np12\nI1\ntp13\na(S'Subkind'\np14\nS'foobar'\np15\ntp16\nastp17\nb.",
            b"ccopy_reg\n_reconstructor\np0\n(cgoogle.appengine.ext.ndb.key\nKey\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n((dp5\nS'namespace'\np6\nS'ns'\np7\nsS'app'\np8\nS'a-different-app'\np9\nsS'pairs'\np9\n(lp10\n(S'Kind'\np11\nI1\ntp12\na(S'Subkind'\np13\nS'foobar'\np14\ntp15\nastp16\nb."
        ],
        [
            b"ccopy_reg\n_reconstructor\np0\n(cgoogle.appengine.ext.ndb.key\nKey\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n((dp5\nS'app'\np6\nS'ndb-test-app-id'\np7\nsS'pairs'\np8\n((S'Kind'\np9\nI1\ntp10\ntp11\nsS'namespace'\np12\nS''\np13\nstp14\nb.",
            b"ccopy_reg\n_reconstructor\np0\n(cgoogle.appengine.ext.ndb.key\nKey\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n((dp5\nS'app'\np6\nS'ndb-test-app-id'\np7\nsS'pairs'\np8\n((S'Kind'\np9\nI1\ntp10\n(S'Subkind'\np11\nS'foobar'\np12\ntp13\ntp14\nsS'namespace'\np15\nS''\np16\nstp17\nb.",
            b"ccopy_reg\n_reconstructor\np0\n(cgoogle.appengine.ext.ndb.key\nKey\np1\nc__builtin__\nobject\np2\nNtp3\nRp4\n((dp5\nS'app'\np6\nS'a-different-app'\np7\nsS'pairs'\np8\n((S'Kind'\np9\nI1\ntp10\n(S'Subkind'\np11\nS'foobar'\np12\ntp13\ntp14\nsS'namespace'\np15\nS'ns'\np16\nstp17\nb."
        ]
    ]

  def _Unpickle(self, s):
    if six.PY2:
      return pickle.loads(s)
    else:
      return pickle.loads(s, encoding='bytes')

  def testPickleBackwardsCompatibility(self):
    for pkey_list in self.pkeys:
      for expected, pkey in zip(self.keys, pkey_list):
        expected.app()
        actual = self._Unpickle(pkey)
        self.assertEqual(expected, actual)

  def testPickleForwardCompatibility(self):
    os.environ['NDB_PY2_UNPICKLE_COMPAT'] = '1'
    self.addCleanup(os.unsetenv, 'NDB_PY2_UNPICKLE_COMPAT')
    expected = sortedcontainers.SortedSet([
        Snapshot(
            snapshot_key=key.Key('Kind', 1, 'Subkind', 'foobar', app='test'),
            created_on=datetime.datetime(2020, 8, 25, 18, 28, 27, 66651))
    ])
    py2_pickle = b'\x80\x02csortedcontainers.sortedset\nSortedSet\nq\x00c__builtin__\nset\nq\x01]q\x02cgoogle.appengine.ext.ndb.key_test\nSnapshot\nq\x03cgoogle.appengine.ext.ndb.key\nKey\nq\x04}q\x05(U\x05pairsq\x06U\x04Kindq\x07K\x01\x86q\x08U\x07Subkindq\tU\x06foobarq\n\x86q\x0b\x86q\x0cU\tnamespaceq\rU\x00q\x0eU\x03appq\x0fU\x04testq\x10u\x85q\x11\x81q\x12}q\x13(h\x06h\x0ch\rh\x0eh\x0fh\x10u\x85q\x14bcdatetime\ndatetime\nq\x15U\n\x07\xe4\x08\x19\x12\x1c\x1b\x01\x04[q\x16\x85q\x17Rq\x18\x86q\x19\x81q\x1aa\x85q\x1bRq\x1cN\x86q\x1dRq\x1e.'
    actual = self._Unpickle(six.ensure_binary(py2_pickle))
    self.assertEqual(expected, actual)

  def testPy2PickleSetState(self):

    pickle_bytes = b'\x80\x02cgoogle.appengine.ext.ndb.key\nKey\nq\x00}q\x01(U\x09namespaceq\x02U\x00q\x03U\x03appq\x04U\x0ds~some-app-idq\x05U\x05pairsq\x06U\x05Classq\x07U\x02idq\x08\x86q\x09\x85q\nu\x85q\x0b\x81q\x0c}q\x0d(h\x02h\x03h\x04h\x05h\x06h\nu\x85q\x0eb.'

    expected = key.Key('Class', 'id', app='s~some-app-id')

    actual = pickle.loads(pickle_bytes)
    self.assertEqual(expected.__getstate__()[0]['pairs'],
                     actual.__getstate__()[0]['pairs'])




  def testConsistentPickleBehaviour(self):
    k = key.Key('Kind', 'foo', app='app1', namespace='ns1')
    k.__setstate__(
        ({'pairs': (('Kind', 'foo'),), 'app': 'app1', 'namespace': 'ns1'},)
    )
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
      self.assertEqual(k, self._Unpickle(pickle.dumps(k, protocol)))

  def testPickling(self):
    for k in self.keys:
      for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
        self.assertEqual(k, self._Unpickle(pickle.dumps(k, protocol)))


def _bytes2str(bytestring):
  """Helper method for debugging pickle.dumps output."""
  return ''.join(_human_readable_byte(x) for x in bytestring)


def _human_readable_byte(c):
  if isinstance(c, str):
    c = ord(c)
  if c == 10:
    return '\\n'
  if c > 21 and c < 127:
    return chr(c)
  else:
    return '\\x{:02x}'.format(c)


if __name__ == '__main__':
  unittest.main()
