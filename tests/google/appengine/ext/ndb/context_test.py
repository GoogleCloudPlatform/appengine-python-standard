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
















"""Tests for context.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import random
import socket
import threading
import unittest as real_unittest

from google.appengine.ext.ndb import context
from google.appengine.ext.ndb import eventloop
from google.appengine.ext.ndb import model
from google.appengine.ext.ndb import query
from google.appengine.ext.ndb import tasklets
from google.appengine.ext.ndb import test_utils
import six
from six.moves import range

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.datastore import datastore_pbs
from google.appengine.datastore import datastore_rpc
from google.appengine.runtime import apiproxy_errors
from absl.testing import absltest as unittest



STORED = True
NOT_STORED = False


class MyAutoBatcher(context.AutoBatcher):

  _log = []

  @classmethod
  def reset_log(cls):
    cls._log = []

  def __init__(self, todo_tasklet, limit):
    def wrap(todo, options):
      self.__class__._log.append((todo_tasklet.__name__, todo))
      return todo_tasklet(todo, options)
    super(MyAutoBatcher, self).__init__(wrap, limit)


class ContextTestMixin(object):

  the_module = context

  @tasklets.tasklet
  def create_entities(self, auto_id=False):
    key0 = model.Key(flat=['Foo', None])
    key1 = model.Key(flat=['Foo', 1])
    key2 = model.Key(flat=['Foo', 2])
    key3 = model.Key(flat=['Foo', 3])
    ent1 = model.Model(key=(key0 if auto_id else key1))
    ent2 = model.Model(key=(key0 if auto_id else key2))
    ent3 = model.Model(key=(key0 if auto_id else key3))
    fut1 = self.ctx.put(ent1)
    fut2 = self.ctx.put(ent2)
    fut3 = self.ctx.put(ent3)
    key1 = yield fut1
    key2 = yield fut2
    key3 = yield fut3
    raise tasklets.Return([key1, key2, key3])

  def make_bad_transaction(*arg, **kwargs):
    raise NotImplementedError

  def testContext_MultiRpc(self):



    config = datastore_rpc.Configuration(max_get_keys=3, max_put_entities=3)
    self.ctx._conn = self.MakeConnection(config=config,
                                         default_model=model.Expando)

    @tasklets.tasklet
    def foo():
      ents = [model.Expando() for _ in range(10)]
      futs = [self.ctx.put(ent) for ent in ents]
      keys = yield futs
      futs = [self.ctx.get(key) for key in keys]
      ents2 = yield futs
      self.assertEqual(ents2, ents)
      raise tasklets.Return(keys)
    keys = foo().get_result()
    self.assertEqual(len(keys), 10)

  def testContext_Cache(self):
    @tasklets.tasklet
    def foo():
      key1 = model.Key(flat=('Foo', 1))
      ent1 = model.Expando(key=key1, foo=42, bar='hello')
      key = yield self.ctx.put(ent1)
      self.assertTrue(key1 in self.ctx._cache)
      a = yield self.ctx.get(key1)
      b = yield self.ctx.get(key1)
      self.assertTrue(a is b)
      yield self.ctx.delete(key1)
      self.assertTrue(self.ctx._cache[key] is None)
      a = yield self.ctx.get(key1)
      self.assertTrue(a is None)
      self.ctx.clear_cache()
      self.assertEqual(self.ctx._cache, {})
    foo().check_success()

  def testContext_CacheMisses(self):



    ctx = self.ctx
    key = model.Key('Foo', 42)
    self.assertFalse(key in ctx._cache)
    ctx.get(key, use_datastore=False).wait()
    self.assertFalse(key in ctx._cache)
    ctx.get(key, use_memcache=False).wait()
    self.assertTrue(key in ctx._cache)
    self.assertEqual(ctx._cache[key], None)
    ctx.clear_cache()
    ctx.get(key).wait()
    self.assertTrue(key in ctx._cache)
    self.assertEqual(ctx._cache[key], None)

  def testContext_CachePolicy(self):
    def should_cache(unused_key):
      return False

    @tasklets.tasklet
    def foo():
      key1 = model.Key(flat=('Foo', 1))
      ent1 = model.Expando(key=key1, foo=42, bar='hello')
      key = yield self.ctx.put(ent1)
      self.assertTrue(key1 not in self.ctx._cache)
      a = yield self.ctx.get(key1)
      b = yield self.ctx.get(key1)
      self.assertTrue(a is not b)
      yield self.ctx.delete(key1)
      self.assertTrue(key not in self.ctx._cache)
      a = yield self.ctx.get(key1)
      self.assertTrue(a is None)
    self.ctx.set_cache_policy(should_cache)
    self.ctx.set_memcache_policy(False)
    foo().check_success()

  def testContext_CachePolicyDisabledLater(self):



    self.ctx.set_cache_policy(lambda unused_key: True)
    key1 = model.Key(flat=('Foo', 1))
    ent1 = model.Expando(key=key1)
    self.ctx.put(ent1).get_result()


    self.assertTrue(key1 in self.ctx._cache)
    self.assertEqual(self.ctx.get(key1).get_result(), ent1)


    self.ctx._cache[key1] = None
    self.assertEqual(self.ctx.get(key1).get_result(), None)


    self.ctx.set_cache_policy(lambda unused_key: False)
    self.assertEqual(self.ctx.get(key1).get_result(), ent1)

  def testContext_CacheQuery(self):
    @tasklets.tasklet
    def foo():
      key1 = model.Key(flat=('Foo', 1))
      key2 = model.Key(flat=('Foo', 2))
      ent1 = model.Expando(key=key1, foo=42, bar='hello')
      ent2 = model.Expando(key=key2, foo=1, bar='world')
      key1a, key2a = yield self.ctx.put(ent1), self.ctx.put(ent2)
      self.assertTrue(key1 in self.ctx._cache)
      self.assertTrue(key2 in self.ctx._cache)
      self.assertEqual(key1, key1a)
      self.assertEqual(key2, key2a)

      @tasklets.tasklet
      def callback(ent):
        return ent
      qry = query.Query(kind='Foo')
      results = yield self.ctx.map_query(qry, callback)
      self.assertEqual(results, [ent1, ent2])
      self.assertTrue(results[0] is self.ctx._cache[ent1.key])
      self.assertTrue(results[1] is self.ctx._cache[ent2.key])
    foo().check_success()

  def testContext_MapQuery(self):
    @tasklets.tasklet
    def callback(ent):
      return ent.key.flat()[-1]

    @tasklets.tasklet
    def foo():
      yield self.create_entities()
      qry = query.Query(kind='Foo')
      res = yield self.ctx.map_query(qry, callback)
      raise tasklets.Return(res)
    res = foo().get_result()
    self.assertEqual(set(res), set([1, 2, 3]))

  def testContext_MapQuery_NoCallback(self):
    @tasklets.tasklet
    def foo():
      yield self.create_entities()
      qry = query.Query(kind='Foo')
      res = yield self.ctx.map_query(qry, None)
      raise tasklets.Return(res)
    res = foo().get_result()
    self.assertEqual(len(res), 3)
    for i, ent in enumerate(res):
      self.assertTrue(isinstance(ent, model.Model))
      self.assertEqual(ent.key.flat(), ('Foo', i + 1))

  def testContext_MapQuery_NonTaskletCallback(self):
    def callback(ent):
      return ent.key.flat()[-1]

    @tasklets.tasklet
    def foo():
      yield self.create_entities()
      qry = query.Query(kind='Foo')
      res = yield self.ctx.map_query(qry, callback)
      raise tasklets.Return(res)
    res = foo().get_result()
    self.assertEqual(res, [1, 2, 3])

  def testContext_MapQuery_CustomFuture(self):
    mfut = tasklets.QueueFuture()

    @tasklets.tasklet
    def callback(ent):
      return ent.key.flat()[-1]

    @tasklets.tasklet
    def foo():
      yield self.create_entities()
      qry = query.Query(kind='Foo')
      res = yield self.ctx.map_query(qry, callback, merge_future=mfut)
      self.assertEqual(res, None)
      vals = set()
      for _ in range(3):
        val = yield mfut.getq()
        vals.add(val)
      fail = mfut.getq()
      self.assertRaises(EOFError, fail.get_result)
      raise tasklets.Return(vals)
    res = foo().get_result()
    self.assertEqual(res, set([1, 2, 3]))

  def testContext_MapQuery_KeysOnly(self):
    qo = query.QueryOptions(keys_only=True)

    @tasklets.tasklet
    def callback(key):
      return key.pairs()[-1]

    @tasklets.tasklet
    def foo():
      yield self.create_entities()
      qry = query.Query(kind='Foo')
      res = yield self.ctx.map_query(qry, callback, options=qo)
      raise tasklets.Return(res)
    res = foo().get_result()
    self.assertEqual(set(res), set([('Foo', 1), ('Foo', 2), ('Foo', 3)]))

  def testContext_MapQuery_Cursors(self):
    qo = query.QueryOptions(produce_cursors=True)

    @tasklets.tasklet
    def callback(ent):
      return ent.key.pairs()[-1]

    @tasklets.tasklet
    def foo():
      yield self.create_entities()
      qry = query.Query(kind='Foo')
      res = yield self.ctx.map_query(qry, callback, options=qo)
      raise tasklets.Return(res)
    res = foo().get_result()
    self.assertEqual(set(res), set([('Foo', 1), ('Foo', 2), ('Foo', 3)]))

  def testContext_IterQuery(self):
    @tasklets.tasklet
    def foo():
      yield self.create_entities()
      qry = query.Query(kind='Foo')
      it = self.ctx.iter_query(qry)
      res = []
      while True:
        try:
          ent = yield it.getq()
        except EOFError:
          break
        res.append(ent)
      raise tasklets.Return(res)
    res = foo().get_result()
    self.assertEqual(len(res), 3)
    for i, ent in enumerate(res):
      self.assertTrue(isinstance(ent, model.Model))
      self.assertEqual(ent.key.flat(), ('Foo', i + 1))

  def testContext_TransactionFailed(self):

    @tasklets.tasklet
    def foo():
      key = model.Key(flat=('Foo', 1))
      ent = model.Expando(key=key, bar=1)
      yield self.ctx.put(ent)

      @tasklets.tasklet
      def callback():
        ctx = tasklets.get_context()
        self.assertTrue(key not in ctx._cache)
        e = yield key.get_async()
        self.assertTrue(key in ctx._cache)
        e.bar = 2
        yield e.put_async()
      yield self.ctx.transaction(callback)
      self.assertEqual(self.ctx._cache[key].bar, 2)
    foo().check_success()

  def testContext_TransactionException(self):
    self.ExpectWarnings()
    key = model.Key('Foo', 1)

    @tasklets.tasklet
    def foo():
      ent = model.Expando(key=key, bar=1)

      @tasklets.tasklet
      def callback():
        yield ent.put_async()
        raise Exception('foo')
      yield self.ctx.transaction(callback)
    self.assertRaises(Exception, foo().check_success)
    self.assertEqual(key.get(), None)

  def testContext_TransactionRollback(self):
    self.ExpectWarnings()
    key = model.Key('Foo', 1)

    @tasklets.tasklet
    def foo():
      ent = model.Expando(key=key, bar=1)

      @tasklets.tasklet
      def callback():
        yield ent.put_async()
        raise model.Rollback()
      yield self.ctx.transaction(callback)
    foo().check_success()
    self.assertEqual(key.get(), None)

  def testContext_TransactionRollbackException(self):
    self.ExpectWarnings()
    key = model.Key('Foo', 1)

    class CustomException(Exception):
      pass

    @tasklets.tasklet
    def foo():
      ent = model.Expando(key=key, bar=1)

      @tasklets.tasklet
      def callback():
        yield ent.put_async()
        ctx = tasklets.get_context()
        ctx._conn.transaction

        (ctx._conn
         ._TransactionalConnection__transaction) = self.make_bad_transaction()
        raise CustomException()
      yield self.ctx.transaction(callback)
    try:
      foo().check_success()
      self.fail()
    except CustomException:
      pass

    self.assertEqual(key.get(), None)

  def testContext_TransactionCallBackTasklet(self):
    class Foo(model.Model):
      n = model.IntegerProperty()

    @tasklets.tasklet
    def inner_callback():
      self.assertTrue(tasklets.get_context().in_transaction())
      x = yield Foo.get_or_insert_async('x', n=0)
      x.n += 1
      yield x.put_async()
      raise tasklets.Return(x)


    x = self.ctx.transaction(inner_callback).get_result()
    self.assertEqual(x, Foo(n=1, id='x'))
    x.key.delete()


    def outer_callback():
      ctx = tasklets.get_context()
      self.assertTrue(ctx.in_transaction())
      f = ctx.transaction(
          inner_callback, propagation=context.TransactionOptions.MANDATORY)
      x = f.get_result()
      self.assertEqual(x, Foo(n=1, id='x'))
      return x
    x = self.ctx.transaction(outer_callback).get_result()
    x.key.delete()


    def outer_callback():
      ctx = tasklets.get_context()
      self.assertTrue(ctx.in_transaction())
      f = ctx.transaction(
          inner_callback, propagation=context.TransactionOptions.ALLOWED)
      x = f.get_result()
      self.assertEqual(x, Foo(n=1, id='x'))
      return x
    x = self.ctx.transaction(outer_callback).get_result()
    x.key.delete()

  def testTransaction_OnCommit(self):
    self.ExpectWarnings()

    class Counter(model.Model):
      count = model.IntegerProperty(default=0)

    @model.transactional
    def trans1(fail=False, bad=None):
      tasklets.get_context().call_on_commit(lambda: log.append('A'))
      c = key.get()
      c.count += 1
      c.put()
      if bad is not None:
        tasklets.get_context().call_on_commit(bad)
      tasklets.get_context().call_on_commit(lambda: log.append('B'))
      if fail:
        raise model.Rollback

    key = Counter().put()
    log = []
    trans1()
    self.assertEqual(key.get().count, 1)
    self.assertEqual(log, ['A', 'B'])

    key = Counter().put()
    log = []
    trans1(fail=True)
    self.assertEqual(key.get().count, 0)
    self.assertEqual(log, [])

    key = Counter().put()
    log = []
    self.assertRaises(ZeroDivisionError, trans1, bad=lambda: 1 / 0)
    self.assertEqual(key.get().count, 1)
    self.assertEqual(log, ['A'])

    key = Counter().put()
    log = []
    self.assertRaises(TypeError, trans1, bad=42)
    self.assertEqual(key.get().count, 1)
    self.assertEqual(log, ['A'])

    log = []
    tasklets.get_context().call_on_commit(lambda: log.append('C'))
    self.assertEqual(log, ['C'])

    log = []
    self.assertRaises(ZeroDivisionError,
                      tasklets.get_context().call_on_commit, lambda: 1 / 0)

    log = []
    self.assertRaises(TypeError, tasklets.get_context().call_on_commit, 42)

  def testDefaultContextTransaction(self):
    @tasklets.synctasklet
    def outer():
      ctx1 = tasklets.get_context()

      @tasklets.tasklet
      def inner():
        ctx2 = tasklets.get_context()
        self.assertTrue(ctx1 is not ctx2)
        self.assertTrue(isinstance(ctx2._conn,
                                   datastore_rpc.TransactionalConnection))
        return 42
      a = yield tasklets.get_context().transaction(inner)
      ctx1a = tasklets.get_context()
      self.assertTrue(ctx1 is ctx1a)
      raise tasklets.Return(a)
    b = outer()
    self.assertEqual(b, 42)

  def testExplicitTransactionClearsDefaultContext(self):
    old_ctx = tasklets.get_context()

    @tasklets.synctasklet
    def outer():
      ctx1 = tasklets.get_context()

      @tasklets.tasklet
      def inner():
        ctx = tasklets.get_context()
        self.assertTrue(ctx is not ctx1)
        key = model.Key('Account', 1)
        ent = yield key.get_async()
        self.assertTrue(tasklets.get_context() is ctx)
        self.assertTrue(ent is None)
        raise tasklets.Return(42)
      fut = ctx1.transaction(inner)
      self.assertEqual(tasklets.get_context(), ctx1)
      val = yield fut
      self.assertEqual(tasklets.get_context(), ctx1)
      raise tasklets.Return(val)
    val = outer()
    self.assertEqual(val, 42)
    self.assertTrue(tasklets.get_context() is old_ctx)

  def testKindError(self):
    self.ExpectWarnings()
    ctx = self.MakeContext()



    ctx.set_cache_policy(lambda unused_key: False)

    @tasklets.tasklet
    def foo():

      key1 = model.Key(flat=('ThisModelClassDoesntExist', 1))
      ent1 = model.Expando(key=key1, foo=42, bar='hello')
      yield ctx.put(ent1)
      yield ctx.get(key1)
    self.assertRaises(model.KindError, foo().check_success)

  def testAsyncInTransaction(self):

    class Bar(model.Model):
      name = model.StringProperty()

    bar = Bar(id='bar', name='bar')
    bar.put()

    @tasklets.tasklet
    def trans():
      bar = Bar.get_by_id('bar')
      bar.name = 'updated-bar'
      bar.put_async()
    model.transaction_async(trans).get_result()

    bar = bar.key.get()
    self.assertEqual(bar.name, 'updated-bar')

  def start_test_server(self):
    host = 'localhost'
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    for i in range(10):
      port = random.randrange(32768, 60000)
      try:
        s.bind((host, port))
        break
      except socket.error:
        continue
    else:
      self.fail('Could not find an unused port in 10 tries')
    s.listen(1)

    def run():
      c, addr = s.accept()
      s.close()
      c.recv(1000)
      c.send(b'HTTP/1.0 200 Ok\r\n\r\n')
      c.close()
    t = threading.Thread(target=run)
    t.setDaemon(True)
    t.start()
    return host, port

  def testUrlFetch(self):
    self.testbed.init_urlfetch_stub()
    host, port = self.start_test_server()
    fut = self.ctx.urlfetch('http://%s:%d' % (host, port))
    result = fut.get_result()
    self.assertEqual(result.status_code, 200)
    self.assertIsInstance(result.content, six.binary_type)

  def testDatastoreConnectionIsRestored(self):

    class TestData(model.Model):
      pass

    @tasklets.tasklet
    def txn():
      conn1 = datastore._GetConnection()
      self.assertIsInstance(
          conn1, datastore_rpc.TransactionalConnection)
      yield TestData().put_async()
      conn2 = datastore._GetConnection()
      self.assertEqual(conn1, conn2)

    @tasklets.synctasklet
    def many_txns():



      conn_a = datastore._GetConnection()
      ts = [model.transaction_async(txn) for i in range(100)]
      conn_b = datastore._GetConnection()
      self.assertEqual(conn_a, conn_b)
      yield ts
      conn_c = datastore._GetConnection()
      self.assertEqual(conn_b, conn_c)
    conn_before = datastore._GetConnection()
    many_txns()
    conn_after = datastore._GetConnection()
    self.assertEqual(conn_before, conn_after)


class ContextMemcacheTestMixin(object):

  def testContext_CacheMemcache(self):


    class Foo(model.Model):
      pass
    ctx = self.ctx
    ctx.set_cache_policy(False)
    ctx.set_memcache_policy(False)
    ent = Foo()
    key = ent.put()
    mkey = ctx._memcache_prefix + key.urlsafe()
    self.assertFalse(key in ctx._cache)
    self.assertEqual(None, memcache.get(mkey))
    ctx.set_memcache_policy(True)
    key.get()
    self.assertFalse(key in ctx._cache)
    self.assertNotEqual(None, memcache.get(mkey))
    eventloop.run()
    ctx.set_cache_policy(True)
    key.get()
    self.assertTrue(key in ctx._cache)

  def testContext_MemcacheMissingKind(self):
    ctx = self.MakeContext(default_model=None, auto_batcher_class=MyAutoBatcher)
    ctx.set_memcache_policy(False)
    ctx.set_cache_policy(False)

    class Foo(model.Model):
      foo = model.IntegerProperty()
      bar = model.StringProperty()

    key1 = model.Key(flat=('Foo', 1))
    ent1 = Foo(key=key1, foo=42, bar='hello')
    ctx.put(ent1).get_result()
    ctx.set_memcache_policy(True)
    ctx.get(key1).get_result()

    model.Model._reset_kind_map()
    self.assertRaises(model.KindError, ctx.get(key1).get_result)

    ctx = self.MakeContext(default_model=Foo, auto_batcher_class=MyAutoBatcher)
    ctx.set_memcache_policy(True)
    ctx.set_cache_policy(False)

    ent1_res = ctx.get(key1).get_result()
    self.assertEqual(ent1, ent1_res)

  def testContext_MemcachePolicy(self):
    badkeys = []

    def tracking_add_async(*args, **kwds):
      try:
        res = save_add_async(*args, **kwds)
        if badkeys and not res:
          res = badkeys
        track.append((args, kwds, res, None))
        return res
      except Exception as err:
        track.append((args, kwds, None, err))
        raise

    @tasklets.tasklet
    def foo():
      k1, k2 = yield self.ctx.put(ent1), self.ctx.put(ent2)
      self.assertEqual(k1, key1)
      self.assertEqual(k2, key2)

      yield (self.ctx.get(k1, use_cache=False),
             self.ctx.get(k2, use_cache=False))
      eventloop.run()
    key1 = model.Key('Foo', 1)
    key2 = model.Key('Foo', 2)
    ent1 = model.Expando(key=key1, foo=42, bar='hello')
    ent2 = model.Expando(key=key2, foo=1, bar='world')
    save_add_multi_async = self.ctx._memcache.add_multi_async
    try:
      self.ctx._memcache.add_multi_async = tracking_add_multi_async
      yield self.ctx._memcache.flush_all_async()

      track = []
      foo().check_success()
      self.assertEqual(len(track), 1)
      self.assertEqual(track[0][0],
                       ({key1.urlsafe(): ent1._to_pb(),
                         key2.urlsafe(): ent2._to_pb()},))
      self.assertEqual(track[0][1], {'key_prefix': self.ctx._memcache_prefix,
                                     'time': 0})
      yield self.ctx._memcache.flush_all_async()

      track = []
      self.ctx.set_memcache_policy(lambda unused_key: False)
      foo().check_success()
      self.assertEqual(len(track), 0)
      yield self.ctx._memcache.flush_all_async()

      track = []
      self.ctx.set_memcache_policy(lambda key: key == key1)
      foo().check_success()
      self.assertEqual(len(track), 1)
      self.assertEqual(track[0][0],
                       ({key1.urlsafe(): ent1._to_pb()},))
      self.assertEqual(track[0][1], {'key_prefix': self.ctx._memcache_prefix,
                                     'time': 0})
      yield self.ctx._memcache.flush_all_async()

      track = []
      self.ctx.set_memcache_policy(lambda unused_key: True)
      self.ctx.set_memcache_timeout_policy(lambda key: key.id())
      foo().check_success()
      self.assertEqual(len(track), 2)
      self.assertEqual(track[0][0],
                       ({key1.urlsafe(): ent1._to_pb()},))
      self.assertEqual(track[0][1], {'key_prefix': self.ctx._memcache_prefix,
                                     'time': 1})
      self.assertEqual(track[1][0],
                       ({key2.urlsafe(): ent2._to_pb()},))
      self.assertEqual(track[1][1], {'key_prefix': self.ctx._memcache_prefix,
                                     'time': 2})
      yield self.ctx._memcache.flush_all_async()

      track = []
      badkeys = [key2.urlsafe()]
      self.ctx.set_memcache_timeout_policy(lambda unused_key: 0)
      foo().check_success()
      self.assertEqual(len(track), 1)
      self.assertEqual(track[0][2], badkeys)
      yield self.ctx._memcache.flush_all_async()
    finally:
      self.ctx._memcache.add_multi_async = save_add_multi_async

  def testContext_Memcache(self):
    @tasklets.tasklet
    def foo():
      key1 = model.Key(flat=('Foo', 1))
      key2 = model.Key(flat=('Foo', 2))
      ent1 = model.Expando(key=key1, foo=42, bar='hello')
      ent2 = model.Expando(key=key2, foo=1, bar='world')
      self.ctx.set_memcache_policy(False)
      k1, k2 = yield self.ctx.put(ent1), self.ctx.put(ent2)
      self.ctx.set_memcache_policy(True)
      self.assertEqual(k1, key1)
      self.assertEqual(k2, key2)

      yield (self.ctx.get(k1, use_cache=False),
             self.ctx.get(k2, use_cache=False))
      eventloop.run()
      keys = [k1.urlsafe(), k2.urlsafe()]
      results = memcache.get_multi(keys, key_prefix=self.ctx._memcache_prefix)
      self.assertEqual(
          results,
          {key1.urlsafe():
               ent1._to_pb(set_key=False).SerializePartialToString(),
           key2.urlsafe():
               ent2._to_pb(set_key=False).SerializePartialToString(),
          })
    foo().check_success()

  def testContext_TransactionMemcache(self):
    class Foo(model.Model):
      name = model.StringProperty()

    foo1 = Foo(name='foo1')
    foo2 = Foo(name='foo2')
    key1 = foo1.put()
    key2 = foo2.put()
    skey1 = self.ctx._memcache_prefix + key1.urlsafe()
    skey2 = self.ctx._memcache_prefix + key2.urlsafe()


    self.assertEqual(memcache.get(skey1), None)
    self.assertEqual(memcache.get(skey2), None)


    self.ctx.clear_cache()


    def txn():
      ctx = tasklets.get_context()
      self.assertTrue(ctx is not self.ctx)
      f1 = key1.get()
      f2 = key1.get()
      f1.name += 'a'
      f1.put()


      self.assertEqual(memcache.get(skey1), context._LOCKED)
      self.assertEqual(memcache.get(skey2), None)
    self.ctx.transaction(txn).wait()


    self.assertEqual(memcache.get(skey1), None)
    self.assertEqual(memcache.get(skey2), None)


    self.ctx.clear_cache()


    f1 = key1.get()
    f2 = key2.get()
    eventloop.run()
    self.assertNotEqual(memcache.get(skey1), None)
    self.assertNotEqual(memcache.get(skey2), None)

  def testMemcachePolicy(self):

    class P(model.Model):
      pass

    class Q(model.Model):
      pass

    def policy(key): return key.kind() != 'P'
    self.ctx.set_cache_policy(policy)
    self.ctx.set_memcache_policy(policy)
    k1 = model.Key(P, 1)
    k2 = model.Key(Q, 1)
    f1 = self.ctx.get(k1)
    f2 = self.ctx.get(k2)
    self.assertTrue(f1.get_result() is None)
    self.assertTrue(f2.get_result() is None)

  def testMemcacheDeleteThenGet(self):

    self.ctx.set_cache_policy(False)
    self.ctx.set_datastore_policy(False)
    self.ctx.set_memcache_policy(True)

    class EmptyModel(model.Model):
      pass
    key = model.Key(EmptyModel, 1)


    del_fut = self.ctx.delete(key)
    del_fut.get_result()



    EmptyModel(key=key).put()


    get_fut = self.ctx.get(key)
    ent = get_fut.get_result()
    self.assertTrue(ent is not None,
                    'Memcache delete did block memcache set %r' % ent)

  def testMemcacheAPI(self):
    self.ExpectErrors()

    @tasklets.tasklet
    def foo():
      ctx = tasklets.get_context()
      k1 = 'k1'
      k2 = u'k2'
      vv = yield ctx.memcache_get(k1), ctx.memcache_get(k2)
      self.assertEqual(vv, [None, None])
      v1 = '24'
      v2 = 42
      vv = yield ctx.memcache_set(k1, v1), ctx.memcache_set(k2, v2)
      self.assertEqual(vv, [STORED, STORED])
      vv = yield ctx.memcache_get(k1), ctx.memcache_get(k2)
      self.assertEqual(vv, [v1, v2])
      vv = yield ctx.memcache_incr(k1), ctx.memcache_decr(k2)
      self.assertEqual(vv, [25, 41])
      vv = yield ctx.memcache_get(k1), ctx.memcache_get(k2)
      self.assertEqual(vv, ['25', 41])
      vv = yield ctx.memcache_incr(k1, -1), ctx.memcache_decr(k2, -1)
      self.assertEqual(vv, [24, 42])
      vv = yield ctx.memcache_get(k1), ctx.memcache_get(k2)
      self.assertEqual(vv, [v1, v2])
      vv = yield ctx.memcache_add(k1, 'a'), ctx.memcache_add(k2, 'b')
      self.assertEqual(vv, [NOT_STORED, NOT_STORED])
      vv = yield ctx.memcache_replace(k1, 'a'), ctx.memcache_replace(k2, 'b')
      self.assertEqual(vv, [STORED, STORED])
      vv = yield ctx.memcache_delete(k1), ctx.memcache_delete(k2)
      self.assertEqual(vv, [memcache.DELETE_SUCCESSFUL,
                            memcache.DELETE_SUCCESSFUL])
      vv = yield ctx.memcache_delete(k1), ctx.memcache_delete(k2)
      self.assertEqual(vv, [memcache.DELETE_ITEM_MISSING,
                            memcache.DELETE_ITEM_MISSING])
      vv = yield ctx.memcache_incr(k1), ctx.memcache_decr(k2)
      self.assertEqual(vv, [None, None])
      vv = yield ctx.memcache_replace(k1, 'a'), ctx.memcache_replace(k2, 'b')
      self.assertEqual(vv, [NOT_STORED, NOT_STORED])
      vv = yield ctx.memcache_add(k1, 'a'), ctx.memcache_add(k2, 'b')
      self.assertEqual(vv, [STORED, STORED])
      logging.warning('Following two errors are expected:')
      vv = yield ctx.memcache_incr(k1), ctx.memcache_decr(k2)
      self.assertEqual(vv, [None, None])

    foo().get_result()

  def testMemcacheCAS(self):
    @tasklets.tasklet
    def foo():
      c1 = self.MakeContext()
      c2 = self.MakeContext()
      k1 = u'k1'
      k2 = 'k2'
      yield c1.memcache_set(k1, 'a'), c1.memcache_set(k2, 'b')
      vv = yield c2.memcache_get(k1), c2.memcache_get(k2)
      self.assertEqual(vv, ['a', 'b'])
      vv = yield c1.memcache_gets(k1), c1.memcache_get(k2, for_cas=True)
      self.assertEqual(vv, ['a', 'b'])
      ffff = [c1.memcache_cas(k1, 'x'), c1.memcache_cas(k2, 'y'),
              c2.memcache_cas(k1, 'p'), c2.memcache_cas(k2, 'q')]
      vvvv = yield ffff
      self.assertEqual(vvvv, [STORED, STORED, NOT_STORED, NOT_STORED])

    foo().get_result()

  def testMemcacheErrors(self):


    save_create_rpc = memcache.create_rpc

    def fake_check_success(*args):
      raise apiproxy_errors.Error('fake error')

    def fake_create_rpc(*args, **kwds):
      rpc = save_create_rpc(*args, **kwds)
      rpc.check_success = fake_check_success
      return rpc
    try:
      memcache.create_rpc = fake_create_rpc
      val = self.ctx.memcache_get('key2').get_result()
      self.assertEqual(val, None)
      val = self.ctx.memcache_incr('key2').get_result()
      self.assertEqual(val, None)
      ok = self.ctx.memcache_set('key2', 'value2').get_result()
      self.assertFalse(ok)
      ok = self.ctx.memcache_delete('key2').get_result()
      self.assertEqual(ok, memcache.DELETE_NETWORK_FAILURE)
    finally:
      memcache.create_rpc = save_create_rpc

  def testMemcacheNamespaces(self):
    @tasklets.tasklet
    def foo():
      k1 = 'k1'
      k2 = 'k2'
      ns = u'ns'


      s1, s2 = yield (self.ctx.memcache_set(k1, 42, namespace=ns),
                      self.ctx.memcache_add(k2, 100, namespace=ns))
      self.assertEqual(s1, STORED)
      self.assertEqual(s2, STORED)


      v1n, v2n = yield (self.ctx.memcache_get(k1),
                        self.ctx.memcache_get(k2))
      self.assertEqual(v1n, None)
      self.assertEqual(v2n, None)


      v1, v2 = yield (self.ctx.memcache_get(k1, namespace=ns),
                      self.ctx.memcache_gets(k2, namespace=ns))
      self.assertEqual(v1, 42)
      self.assertEqual(v2, 100)


      s1, s2 = yield (self.ctx.memcache_replace(k1, v1 + 1, namespace=ns),
                      self.ctx.memcache_cas(k2, v2 + 1, namespace=ns))
      self.assertEqual(s1, STORED)
      self.assertEqual(s2, STORED)


      v1, v2 = yield (self.ctx.memcache_incr(k1, delta=10, namespace=ns),
                      self.ctx.memcache_decr(k2, delta=10, namespace=ns))
      self.assertEqual(v1, 53)
      self.assertEqual(v2, 91)


      s1, s2 = yield (self.ctx.memcache_delete(k1, namespace=ns),
                      self.ctx.memcache_delete(k2, namespace=ns))
      self.assertEqual(s1, memcache.DELETE_SUCCESSFUL)
      self.assertEqual(s2, memcache.DELETE_SUCCESSFUL)

    foo().check_success()

  def testMemcacheLocking(self):

    self.ctx.set_cache_policy(False)


    class EmptyModel(model.Model):
      pass
    key = model.Key(EmptyModel, 1)
    mkey = self.ctx._memcache_prefix + key.urlsafe()
    ent = EmptyModel(key=key)
    put_fut = self.ctx.put(ent)

    eventloop.run0()
    self.assertTrue(self.ctx._memcache_set_batcher._queues)
    eventloop.run0()
    self.assertTrue(self.ctx._memcache_set_batcher._running)
    while self.ctx._memcache_set_batcher._running:
      eventloop.run0()


    val = memcache.get(mkey)
    self.assertEqual(val, context._LOCKED)

    put_fut.check_success()

    val = memcache.get(mkey)
    self.assertEqual(val, None)

  def testMemcacheDefaultNamespaceBatching(self):
    self.ctx.set_datastore_policy(False)
    key = model.Key('Foo', 1)
    keyfut = key.get_async()
    mfut = self.ctx.memcache_get('bar')
    keyfut.check_success()
    mfut.check_success()
    log = MyAutoBatcher._log
    self.assertEqual(len(log), 1, log)

  def testMemcacheProtobufEncoding(self):


    class Employee(model.Model):
      _use_cache = False
    e = Employee()
    k = e.put(use_memcache=False)
    k.get(use_memcache=True)
    eventloop.run()
    ks = self.ctx._memcache_prefix + k.urlsafe()
    v = memcache.get(ks)
    self.assertIsInstance(v, six.binary_type)

  def testCorruptMemcache(self):

    self.ExpectWarnings()
    self.ctx.set_cache_policy(False)


    class EmptyModel(model.Model):
      pass
    ent = EmptyModel()
    key = ent.put()


    key.get()
    eventloop.run()


    mkey = self.ctx._memcache_prefix + key.urlsafe()
    self.assertEqual(memcache.get(mkey),
                     ent._to_pb(set_key=False).SerializePartialToString())


    memcache.set(mkey, b'ooby trap')


    self.assertEqual(ent, key.get())

  def testMemcacheRpcDeadline(self):


    orig_create_rpc = memcache.create_rpc

    def mock_create_rpc(deadline='invalid'):

      self.assertNotEqual(deadline, 'invalid')
      observed_deadlines.append(deadline)
      return orig_create_rpc(deadline=deadline)

    try:
      memcache.create_rpc = mock_create_rpc

      observed_deadlines = []
      self.ctx.memcache_get('a').get_result()
      self.assertEqual(observed_deadlines, [None])

      observed_deadlines = []
      self.ctx.memcache_get('a', deadline=1).get_result()
      self.assertEqual(observed_deadlines, [1])

      observed_deadlines = []
      self.ctx.memcache_gets('a', deadline=2).get_result()
      self.assertEqual(observed_deadlines, [2])

      observed_deadlines = []
      self.ctx.memcache_set('a', 'b', deadline=3).get_result()
      self.assertEqual(observed_deadlines, [3])

      observed_deadlines = []
      self.ctx.memcache_add('a', 'b', deadline=4).get_result()
      self.assertEqual(observed_deadlines, [4])

      observed_deadlines = []
      self.ctx.memcache_replace('a', 'b', deadline=5).get_result()
      self.assertEqual(observed_deadlines, [5])

      observed_deadlines = []
      self.ctx.memcache_cas('a', 'b', deadline=6).get_result()
      self.assertEqual(observed_deadlines, [6])

      observed_deadlines = []
      self.ctx.memcache_delete('a', deadline=7).get_result()
      self.assertEqual(observed_deadlines, [7])

      observed_deadlines = []
      self.ctx.memcache_incr('a', deadline=8).get_result()
      self.assertEqual(observed_deadlines, [8])

      observed_deadlines = []
      self.ctx.memcache_decr('a', deadline=9).get_result()
      self.assertEqual(observed_deadlines, [9])

    finally:
      memcache.create_rpc = orig_create_rpc

  def testMemcacheRpcDeadlineExceeded(self):

    orig_create_rpc = memcache.create_rpc

    def raise_deadline_error(*args):
      observed_raises.append('raise')
      raise apiproxy_errors.DeadlineExceededError('fake deadline')

    def mock_create_rpc(deadline='invalid'):

      self.assertNotEqual(deadline, 'invalid')
      observed_deadlines.append(deadline)
      rpc = orig_create_rpc(deadline=deadline)

      rpc.check_success = raise_deadline_error
      return rpc

    try:
      memcache.create_rpc = mock_create_rpc

      observed_deadlines = []

      observed_raises = []
      key = model.Key('Kind', 'id')
      ent = key.get(memcache_deadline=1)
      self.assertEqual(ent, None)

      self.assertEqual(observed_deadlines, [1] * 3)
      self.assertEqual(observed_raises, ['raise'] * 3)

    finally:
      memcache.create_rpc = orig_create_rpc

  def testTooBigForMemcache(self):
    self.ctx.set_memcache_policy(True)
    self.ctx.set_cache_policy(False)
    class Blobby(model.Model):
      blob = model.BlobProperty()
    small = Blobby(blob=b'x')
    huge = Blobby(blob=b'x' * 1000000)
    originals = [small, huge]
    keys = model.put_multi(originals)
    copies = model.get_multi(keys)
    self.assertEqual(copies, originals)
    memcache_copies = model.get_multi(keys, use_datastore=False)

    self.assertEqual(memcache_copies, [small, None])


    self.ExpectWarnings()
    Blobby._use_datastore = False
    small.key = model.Key(Blobby, "small")
    huge.key = model.Key(Blobby, "huge")

    fsmall = small.put_async()
    fhuge = huge.put_async()
    self.assertEqual(small.key, fsmall.get_result())
    self.assertRaises(ValueError, fhuge.get_result)
    self.assertEqual(small, small.key.get())
    self.assertEqual(None, huge.key.get())

  def testMemcacheAndContextCache(self):
    self.ctx.set_datastore_policy(True)
    self.ctx.set_cache_policy(False)
    self.ctx.set_memcache_policy(True)

    class EmptyModel(model.Model):
      pass
    key = EmptyModel().put()
    self.ctx.get(key).get_result()
    self.ctx.set_cache_policy(True)
    f1, f2 = self.ctx.get(key), self.ctx.get(key)
    e1, e2 = f1.get_result(), f2.get_result()
    self.assertTrue(e1 is e2)

  def testContext_NamespaceBonanza(self):


    def assertNone(expr):
      self.assertTrue(expr is None, repr(expr))

    def assertNotNone(expr):
      self.assertTrue(expr is not None, repr(expr))

    def assertLocked(expr):
      self.assertTrue(expr is context._LOCKED, repr(expr))

    def assertProtobuf(expr, ent):
      self.assertEqual(expr,
                       ent._to_pb(set_key=False).SerializePartialToString())

    class Foo(model.Model):
      pass
    k1 = model.Key(Foo, 1, namespace='a')
    k2 = model.Key(Foo, 2, namespace='b')
    mk1 = self.ctx._memcache_prefix + k1.urlsafe()
    mk2 = self.ctx._memcache_prefix + k2.urlsafe()
    e1 = Foo(key=k1)
    e2 = Foo(key=k2)
    self.ctx.set_cache_policy(False)
    self.ctx.set_memcache_policy(True)

    self.ctx.set_datastore_policy(False)


    k1 = self.ctx.put(e1).get_result()
    k2 = self.ctx.put(e2).get_result()

    assertNone(memcache.get(mk1, namespace=''))
    assertNone(memcache.get(mk2, namespace=''))

    assertProtobuf(memcache.get(mk1, namespace='a'), e1)
    assertNone(memcache.get(mk2, namespace='a'))

    assertNone(memcache.get(mk1, namespace='b'))
    assertProtobuf(memcache.get(mk2, namespace='b'), e2)

    memcache.flush_all()
    self.ctx.set_datastore_policy(True)


    k1_fut = self.ctx.put(e1)
    while not self.ctx._put_batcher._running:
      eventloop.run0()

    assertNone(memcache.get(mk1, namespace=''))
    assertNone(memcache.get(mk2, namespace=''))

    assertLocked(memcache.get(mk1, namespace='a'))
    assertNone(memcache.get(mk2, namespace='a'))
    self.assertEqual(k1_fut.get_result(), k1)

    k2_fut = self.ctx.put(e2)
    while not self.ctx._put_batcher._running:
      eventloop.run0()

    assertNone(memcache.get(mk1, namespace='b'))
    assertLocked(memcache.get(mk2, namespace='b'))

    self.assertEqual(k2_fut.get_result(), k2)

    memcache.flush_all()


    e1 = self.ctx.get(k1).get_result()
    e2 = self.ctx.get(k2).get_result()
    eventloop.run()

    assertNone(memcache.get(mk1, namespace=''))
    assertNone(memcache.get(mk2, namespace=''))

    assertProtobuf(memcache.get(mk1, namespace='a'), e1)
    assertNone(memcache.get(mk2, namespace='a'))

    assertNone(memcache.get(mk1, namespace='b'))
    assertProtobuf(memcache.get(mk2, namespace='b'), e2)

    self.ctx.set_datastore_policy(False)


    self.ctx.get(k1).get_result()
    self.ctx.get(k2).get_result()
    eventloop.run()

    assertNone(memcache.get(mk1, namespace=''))
    assertNone(memcache.get(mk2, namespace=''))

    assertNotNone(memcache.get(mk1, namespace='a'))
    assertNone(memcache.get(mk2, namespace='a'))

    assertNone(memcache.get(mk1, namespace='b'))
    assertNotNone(memcache.get(mk2, namespace='b'))

    self.ctx.set_datastore_policy(True)


    self.ctx.delete(k1).check_success()
    self.ctx.delete(k2).check_success()

    assertNone(memcache.get(mk1, namespace=''))
    assertNone(memcache.get(mk2, namespace=''))

    assertLocked(memcache.get(mk1, namespace='a'))
    assertNone(memcache.get(mk2, namespace='a'))

    assertNone(memcache.get(mk1, namespace='b'))
    assertLocked(memcache.get(mk2, namespace='b'))

    memcache.flush_all()


    self.ctx._clear_memcache([k1, k2]).check_success()

    assertNone(memcache.get(mk1, namespace=''))
    assertNone(memcache.get(mk2, namespace=''))

    assertNone(memcache.get(mk1, namespace='a'))
    assertNone(memcache.get(mk2, namespace='a'))

    assertNone(memcache.get(mk1, namespace='b'))
    assertNone(memcache.get(mk2, namespace='b'))

  def testContext_AutoBatcher_Get(self):
    @tasklets.tasklet
    def foo():
      key1 = model.Key(flat=['Foo', 1])
      key2 = model.Key(flat=['Foo', 2])
      key3 = model.Key(flat=['Foo', 3])
      fut1 = self.ctx.get(key1)
      fut2 = self.ctx.get(key2)
      fut3 = self.ctx.get(key3)
      ent1 = yield fut1
      ent2 = yield fut2
      ent3 = yield fut3
      raise tasklets.Return([ent1, ent2, ent3])
    ents = foo().get_result()
    self.assertEqual(ents, [None, None, None])
    log = MyAutoBatcher._log
    self.assertEqual(len(log), 4)
    name, todo = log[0]
    self.assertEqual(name, '_memcache_get_tasklet')
    self.assertEqual(len(todo), 3)
    name, todo = log[1]
    self.assertEqual(name, '_memcache_set_tasklet')
    self.assertEqual(len(todo), 3)
    name, todo = log[2]
    self.assertEqual(name, '_memcache_get_tasklet')
    self.assertEqual(len(todo), 3)
    name, todo = log[3]
    self.assertEqual(name, '_get_tasklet')
    self.assertEqual(len(todo), 3)

  def testContext_AutoBatcher_Put(self):
    keys = self.create_entities(True).get_result()
    self.assertEqual(len(keys), 3)
    self.assertTrue(None not in keys)
    log = MyAutoBatcher._log
    self.assertEqual(len(log), 2)
    name, todo = log[0]
    self.assertEqual(name, '_put_tasklet')
    self.assertEqual(len(todo), 3)
    name, todo = log[1]
    self.assertEqual(name, '_memcache_del_tasklet')
    self.assertEqual(len(todo), 3)

  def testContext_AutoBatcher_Delete(self):
    @tasklets.tasklet
    def foo():
      key1 = model.Key(flat=['Foo', 1])
      key2 = model.Key(flat=['Foo', 2])
      key3 = model.Key(flat=['Foo', 3])
      fut1 = self.ctx.delete(key1)
      fut2 = self.ctx.delete(key2)
      fut3 = self.ctx.delete(key3)
      yield fut1
      yield fut2
      yield fut3
    foo().check_success()
    self.assertEqual(len(MyAutoBatcher._log), 2)
    name, todo = MyAutoBatcher._log[0]
    self.assertEqual(name, '_memcache_set_tasklet')
    self.assertEqual(len(todo), 3)
    name, todo = MyAutoBatcher._log[1]
    self.assertEqual(name, '_delete_tasklet')
    self.assertEqual(len(todo), 3)

  def testContext_AutoBatcher_Limit(self):

    self.assertEqual(self.ctx._get_batcher._limit,
                     datastore_rpc.Connection.MAX_GET_KEYS)


    conn_config = context.ContextOptions(max_put_entities=3,
                                         max_memcache_items=7)
    conn = self.MakeConnection(config=conn_config,
                               default_model=model.Expando)
    real_config = context.ContextOptions(max_put_entities=25,
                                         max_memcache_items=100)
    self.ctx = self.MakeContext(
        conn=conn,
        auto_batcher_class=MyAutoBatcher,
        config=real_config)

    @tasklets.tasklet
    def foo():
      es = [model.Model(key=model.Key('Foo', None)) for _ in range(49)]
      fs = [self.ctx.put(e) for e in es]
      self.ctx.flush()
      ks = yield fs
      self.assertEqual(len(ks), 49)
      self.assertTrue(all(isinstance(k, model.Key) for k in ks))
    foo().get_result()
    self.assertEqual(len(MyAutoBatcher._log), 4)
    for name, todo in MyAutoBatcher._log[2:]:
      self.assertEqual(name, '_memcache_del_tasklet')
      self.assertTrue(len(todo) in (24, 25))
    for name, todo in MyAutoBatcher._log[:2]:
      self.assertEqual(name, '_put_tasklet')
      self.assertTrue(len(todo) in (24, 25))


class ContextTaskQueueTestMixin(object):

  def testContext_TransactionAddTask(self):
    self.ExpectWarnings()
    key = model.Key('Foo', 1)

    @tasklets.tasklet
    def foo():
      ent = model.Expando(key=key, bar=1)

      @tasklets.tasklet
      def callback():
        ctx = tasklets.get_context()
        yield ctx.put(ent)
        taskqueue.add(url='/', transactional=True)
      yield self.ctx.transaction(callback)
    foo().check_success()


class ContextV3Tests(ContextTestMixin,
                     ContextMemcacheTestMixin,
                     ContextTaskQueueTestMixin,
                     test_utils.NDBTest):
  """Context tests that use a Datastore V3 connection."""

  def setUp(self):
    super(ContextV3Tests, self).setUp()
    MyAutoBatcher.reset_log()
    self.ctx = self.MakeContext(default_model=model.Expando,
                                auto_batcher_class=MyAutoBatcher)
    tasklets.set_context(self.ctx)

  def make_bad_transaction(*arg, **kwargs):
    return datastore_rpc.datastore_pb.Transaction()

  def testContext_AutoBatcher_Errors(self):





    self.ExpectWarnings()

    class Blobby(model.Model):
      blob = model.BlobProperty()
    ent1 = Blobby()
    ent2 = Blobby(blob=b'x' * 2000000)
    fut1 = self.ctx.put(ent1)
    fut2 = self.ctx.put(ent2)
    err1 = fut1.get_exception()
    err2 = fut2.get_exception()
    self.assertTrue(isinstance(err1, apiproxy_errors.RequestTooLargeError))
    self.assertTrue(err1 is err2)

    fut1 = self.ctx.memcache_set('key1', 'x')
    fut2 = self.ctx.memcache_set('key2', 'x' * 1000001)
    err1 = fut1.get_exception()
    err2 = fut1.get_exception()
    self.assertTrue(isinstance(err1, ValueError))
    self.assertTrue(err1 is err2)


  def testContext_AllocateIds(self):

    @tasklets.tasklet
    def foo():
      key = model.Key(flat=('Foo', 1))
      lo_hi = yield self.ctx.allocate_ids(key, size=10)
      self.assertEqual(lo_hi, (1, 10))
      lo_hi = yield self.ctx.allocate_ids(key, max=20)
      self.assertEqual(lo_hi, (11, 20))
    foo().check_success()

  def MakeContext(self, *args, **kwargs):
    ctx = super(ContextV3Tests, self).MakeContext(*args, **kwargs)

    ctx.set_cache_policy(None)
    ctx.set_memcache_policy(None)
    return ctx


@real_unittest.skipUnless(datastore_pbs._CLOUD_DATASTORE_ENABLED,
                          'V1 must be supported to run V1 tests.')
class ContextV1Tests(ContextTestMixin,
                     test_utils.NDBCloudDatastoreV1Test):
  """Context tests that use a Cloud Datastore V1 connection.

  These tests run with memcache and taskqueue stubs available.
  """

  def setUp(self):
    super(ContextV1Tests, self).setUp()
    self.HRTest()
    MyAutoBatcher.reset_log()
    self.ctx = self.MakeContext(default_model=model.Expando,
                                auto_batcher_class=MyAutoBatcher)
    tasklets.set_context(self.ctx)

  def make_bad_transaction(*arg, **kwargs):
    return b''

  def testContext_AutoBatcher_Errors(self):


    pass

  def testContext_AllocateIds(self):

    pass

  def testContext_TransactionAddTask(self):

    def foo():
      taskqueue.add(url='/', transactional=True)
    self.assertRaises(ValueError, model.transaction, foo)

  def MakeContext(self, *args, **kwargs):
    ctx = super(ContextV1Tests, self).MakeContext(*args, **kwargs)


    ctx.set_cache_policy(None)
    return ctx


@real_unittest.skipUnless(datastore_pbs._CLOUD_DATASTORE_ENABLED,
                          'V1 must be supported to run V1 tests.')
class ContextV1WithRemoteAPITests(ContextV1Tests,
                                  ContextMemcacheTestMixin,
                                  ContextTaskQueueTestMixin):
  """Context tests that use a Cloud Datastore V1 connection.

  These tests run with memcache and taskqueue stubs available.
  """

  def setUp(self):

    super(ContextV1WithRemoteAPITests, self).setUp()
    self.testbed.init_memcache_stub()
    self.testbed.init_taskqueue_stub()

  def testContext_AutoBatcher_Errors(self):

    self.ExpectWarnings()

    class Blobby(model.Model):
      blob = model.BlobProperty()
    ent1 = Blobby()
    ent2 = Blobby(blob=b'x' * 2000000)
    fut1 = self.ctx.put(ent1)
    fut2 = self.ctx.put(ent2)
    err1 = fut1.get_exception()
    err2 = fut2.get_exception()
    self.assertTrue(isinstance(err1, datastore_errors.BadRequestError))
    self.assertTrue(err1 is err2)

    fut1 = self.ctx.memcache_set('key1', 'x')
    fut2 = self.ctx.memcache_set('key2', 'x' * 1000001)
    err1 = fut1.get_exception()
    err2 = fut1.get_exception()
    self.assertTrue(isinstance(err1, ValueError))
    self.assertTrue(err1 is err2)

  def MakeContext(self, *args, **kwargs):
    ctx = super(ContextV1WithRemoteAPITests, self).MakeContext(*args, **kwargs)

    ctx.set_memcache_policy(None)
    return ctx


class ContextFutureCachingTests(test_utils.NDBTest):


  def setUp(self):
    super(ContextFutureCachingTests, self).setUp()
    MyAutoBatcher.reset_log()
    config = context.ContextOptions(max_get_keys=1, max_memcache_items=1)
    self.ctx = self.MakeContext(default_model=model.Expando,
                                auto_batcher_class=MyAutoBatcher,
                                config=config)
    self.ctx.set_cache_policy(False)
    tasklets.set_context(self.ctx)

  def testGetFutureCachingOn(self):
    self.ctx.set_memcache_policy(False)

    class EmptyModel(model.Model):
      pass
    key = EmptyModel().put()
    MyAutoBatcher.reset_log()
    self.ctx.set_cache_policy(True)
    f1, f2 = self.ctx.get(key), self.ctx.get(key)
    self.assertFalse(f1 is f2, 'Context get futures are being cached, '
                               'instead of tasklets.')
    e1, e2 = f1.get_result(), f2.get_result()
    self.assertTrue(e1 is e2, 'Results of concurrent gets are not the same '
                              'with future caching on.')
    self.assertEqual(len(self.ctx._get_batcher._log), 1)
    self.assertFalse(f1 is self.ctx.get(key), 'Future cache persisted.')

  def testGetFutureCachingOff(self):
    self.ctx.set_memcache_policy(False)

    class EmptyModel(model.Model):
      pass
    key = EmptyModel().put()
    MyAutoBatcher.reset_log()
    f1, f2 = self.ctx.get(key), self.ctx.get(key)
    self.assertFalse(f1 is f2, 'Context get futures are being cached '
                               'with future caching off.')
    e1, e2 = f1.get_result(), f2.get_result()
    self.assertTrue(e1 is not e2, 'Results of concurrent gets are the same '
                                  'with future caching off.')
    self.assertEqual(len(self.ctx._get_batcher._log), 2)

  def testMemcacheGetFutureCaching(self):
    key = 'foo'
    f1 = self.ctx.memcache_get(key, use_cache=True)
    f2 = self.ctx.memcache_get(key, use_cache=True)
    self.assertTrue(f1 is f2,
                    'Context memcache get futures are not cached.')
    f3 = self.ctx.memcache_get(key)
    self.assertFalse(f1 is f3,
                     'Context memcache get futures are cached by default.')
    f1.check_success()
    f4 = self.ctx.memcache_get(key, use_cache=True)
    self.assertFalse(f1 is f4,
                     'Context memcache get future cached after result known.')

  def testMemcacheSetFutureCaching(self):
    key = 'foo'
    value = 'bar'
    f1 = self.ctx.memcache_set(key, value, use_cache=True)
    f2 = self.ctx.memcache_set(key, value, use_cache=True)
    self.assertTrue(f1 is f2,
                    'Context memcache get futures are not cached.')
    f3 = self.ctx.memcache_set(key, value)
    self.assertFalse(f1 is f3,
                     'Context memcache get futures are cached by default.')
    f1.check_success()
    f4 = self.ctx.memcache_set(key, value, use_cache=True)
    self.assertFalse(f1 is f4,
                     'Context memcache get future cached after result known.')

if __name__ == '__main__':
  unittest.main()
