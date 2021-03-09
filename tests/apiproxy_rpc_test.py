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



"""Tests for google.appengine.api.apiproxy_rpc."""



from absl import app
from absl.testing import absltest
from google.appengine.api import apiproxy_rpc


class MockStub(object):
  """Mock apiproxy_stub."""

  def __init__(self, failure=None):
    self.failure = failure
    self.calls = []

  def MakeSyncCall(self, service, call, request, response):
    self.calls.append((service, call, request, response))

    if self.failure is not None:
      raise self.failure


def FakeCallback(stub):
  stub.calls.append('callback')


class ApiproxyRpcTest(absltest.TestCase):
  """Tests for RPC."""

  def testMakeCallSuccess(self):
    stub = MockStub()
    rpc = apiproxy_rpc.RPC(stub=stub)

    rpc.MakeCall('test', 'method', 'request', 'response')
    rpc.Wait()
    rpc.CheckSuccess()

    self.assertEquals([('test', 'method', 'request', 'response')],
                      stub.calls)

  def testMakeCallWithCallback(self):
    stub = MockStub()
    rpc = apiproxy_rpc.RPC(stub=stub)

    rpc.MakeCall('test', 'method', 'request', 'response',
                 lambda: FakeCallback(stub))
    rpc.Wait()
    rpc.CheckSuccess()

    self.assertEquals([('test', 'method', 'request', 'response'),
                       ('callback')],
                      stub.calls)

  def testMakeCallFailure(self):
    stub = MockStub(Exception())
    rpc = apiproxy_rpc.RPC(stub=stub)

    rpc.MakeCall('test', 'method', 'request', 'response')
    rpc.Wait()
    self.assertRaises(Exception, rpc.CheckSuccess)

  def testClone(self):
    """Test that Clone behaves appropriately."""
    stub = MockStub()
    deadline = 1.0
    rpc = apiproxy_rpc.RPC(stub=stub, deadline=deadline)


    rpc_clone = rpc.Clone()
    self.assertEqual(rpc_clone.deadline, rpc.deadline)
    self.assertNotEqual(rpc_clone.MakeCall, rpc.MakeCall)

  def testCloneAlreadyCalled(self):
    """Make sure we can't clone once we've started a call."""
    stub = MockStub()
    rpc = apiproxy_rpc.RPC(stub=stub)

    rpc.MakeCall('test', 'method', 'request', 'response')
    self.assertRaises(AssertionError, rpc.Clone)
    rpc.Wait()
    self.assertRaises(AssertionError, rpc.Clone)
    rpc.CheckSuccess()
    self.assertRaises(AssertionError, rpc.Clone)

    self.assertEquals([('test', 'method', 'request', 'response')],
                      stub.calls)


def main(unused_argv):
  absltest.main()


if __name__ == '__main__':
  absltest.main()
