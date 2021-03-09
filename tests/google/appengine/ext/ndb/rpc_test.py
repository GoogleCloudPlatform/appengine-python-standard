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
















"""Some tests for datastore_rpc.py."""


from google.appengine.api import apiproxy_stub_map
from google.appengine.datastore import datastore_rpc
from absl.testing import absltest as unittest

from google.appengine.ext.ndb import model
from google.appengine.ext.ndb import test_utils


class PendingTests(test_utils.NDBTest):
  """Tests for the 'pending RPC' management."""

  def testBasicSetup1(self):
    ent = model.Expando()
    ent.foo = 'bar'
    rpc = self.conn.async_put(None, [ent])
    [key] = rpc.get_result()
    self.assertEqual(key, model.Key(flat=['Expando', 1]))

  def testBasicSetup2(self):
    key = model.Key(flat=['Expando', 1])
    rpc = self.conn.async_get(None, [key])
    [ent] = rpc.get_result()
    self.assertTrue(ent is None)

  def SetUpCallHooks(self):
    self.pre_args = []
    self.post_args = []
    apiproxy_stub_map.apiproxy.GetPreCallHooks().Append('test1',
                                                        self.PreCallHook)
    apiproxy_stub_map.apiproxy.GetPostCallHooks().Append('test1',
                                                         self.PostCallHook)

  def PreCallHook(self, service, call, request, response, rpc=None):
    self.pre_args.append((service, call, request, response, rpc))

  def PostCallHook(self, service, call, request, response,
                   rpc=None, error=None):
    self.post_args.append((service, call, request, response, rpc, error))

  def testCallHooks(self):
    self.SetUpCallHooks()
    key = model.Key(flat=['Expando', 1])
    rpc = self.conn.async_get(None, [key])
    self.assertEqual(len(self.pre_args), 1)
    self.assertEqual(self.post_args, [])
    [ent] = rpc.get_result()
    self.assertTrue(ent is None)
    self.assertEqual(len(self.pre_args), 1)
    self.assertEqual(len(self.post_args), 1)
    self.assertEqual(self.pre_args[0][:2], ('datastore_v3', 'Get'))
    self.assertEqual(self.post_args[0][:2], ('datastore_v3', 'Get'))

  def testCallHooks_Pending(self):
    self.SetUpCallHooks()
    key = model.Key(flat=['Expando', 1])
    rpc = self.conn.async_get(None, [key])
    self.conn.wait_for_all_pending_rpcs()
    self.assertEqual(rpc.state, 2)
    self.assertEqual(len(self.pre_args), 1)
    self.assertEqual(len(self.post_args), 1)
    self.assertEqual(self.conn.get_pending_rpcs(), set())

  def NastyCallback(self, rpc):
    rpc.get_result()
    key = model.Key(flat=['Expando', 1])
    self.conn.async_get(None, [key])

  def testCallHooks_Pending_CallbackAddsMore(self):
    self.SetUpCallHooks()
    conf = datastore_rpc.Configuration(on_completion=self.NastyCallback)
    key = model.Key(flat=['Expando', 1])
    self.conn.async_get(conf, [key])
    self.conn.wait_for_all_pending_rpcs()
    self.assertEqual(self.conn.get_pending_rpcs(), set())


if __name__ == '__main__':
  unittest.main()
