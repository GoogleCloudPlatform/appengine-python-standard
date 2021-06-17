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


"""Tests for google.appengine.api.apiproxy_stub_map."""

from concurrent import futures
import threading
import traceback

import google

from absl import app
from six.moves import range

from google.appengine.api import apiproxy_rpc
from google.appengine.api import apiproxy_stub_map
from absl.testing import absltest




class APIProxyStubMapTest(absltest.TestCase):
  """Tests for API proxy stub map."""

  def setUp(self):
    super(APIProxyStubMapTest, self).setUp()
    self.stubmap = apiproxy_stub_map.APIProxyStubMap()

  def testCrudForHooks(self):
    """Tests for the precall stubs."""
    hooks = self.stubmap.GetPreCallHooks()
    order = []
    self.assertEmpty(hooks)

    def MakeFunction(number):
      def Result(service, call, request, response):
        order.append(number)
      return Result
    self.assertTrue(hooks.Append('a', MakeFunction(2)))
    self.assertTrue(hooks.Append('b', MakeFunction(3)))
    self.assertFalse(hooks.Append('b', MakeFunction(17)))
    self.assertLen(hooks, 2)
    self.assertTrue(hooks.Push('c', MakeFunction(1)))
    self.assertLen(hooks, 3)
    hooks.Call(None, None, None, None)
    self.assertEqual([1, 2, 3], order)
    hooks.Clear()
    self.assertEmpty(hooks)

  def testExtendedHookArgs(self):
    """Tests for extended 5-argument hooks."""
    for hooks in [self.stubmap.GetPreCallHooks(),
                  self.stubmap.GetPostCallHooks()]:
      rpc_args = []
      self.assertEmpty(hooks)

      def MakeFunction(extended):
        if extended:
          def Result(service, call, request, response, rpc):
            rpc_args.append(rpc)
          return Result
        else:
          def Result(service, call, request, response):
            rpc_args.append(None)
          return Result

      class BoundMethod:
        def WithRPC(self, service, call, request, response, rpc):
          rpc_args.append(rpc)
        def WithoutRPC(self, service, call, request, response):
          rpc_args.append(None)
      bound = BoundMethod()
      self.assertTrue(hooks.Append('a', MakeFunction(True)))
      self.assertTrue(hooks.Append('b', MakeFunction(False)))
      self.assertTrue(hooks.Append('c', bound.WithRPC))
      self.assertTrue(hooks.Append('d', bound.WithoutRPC))
      self.assertLen(hooks, 4)
      rpc_sentinel = "sentinel"
      hooks.Call(None, None, None, None, rpc_sentinel)
      self.assertEqual([rpc_sentinel, None, rpc_sentinel, None], rpc_args)

  def testSuperExtendedHookArgs(self):
    """Tests for extended 6-argument hooks."""
    hooks = self.stubmap.GetPostCallHooks()
    rpc_passed = '-RPC-'
    error_passed = '-ERR-'
    error_omitted = '-NOPE-'
    rpc_args = []
    self.assertEmpty(hooks)

    def MakeFunction(super_extended):
      if super_extended:
        def Result(service, call, request, response, rpc, error):
          rpc_args.append((rpc, error))
      else:
        def Result(service, call, request, response, rpc):
          rpc_args.append((rpc, error_omitted))
      return Result

    self.assertTrue(hooks.Append('a', MakeFunction(True)))
    self.assertTrue(hooks.Append('b', MakeFunction(False)))
    self.assertLen(hooks, 2)
    hooks.Call(None, None, None, None, rpc_passed)


    self.assertEqual([(rpc_passed, None),
                      (rpc_passed, error_omitted)], rpc_args)
    rpc_args = []
    hooks.Call(None, None, None, None, rpc_passed, error_passed)

    self.assertEqual([(rpc_passed, error_passed)], rpc_args)

  def testMakeSyncCall(self):
    """Makes sure that the hooks are executed in the right order."""
    calls = []

    def Pre(service, call, request, response):
      calls.append('pre')

    class Stub(object):
      def MakeSyncCall(self, service, call, request, response):
        calls.append('stub')

    def Post(service, call, request, response):
      calls.append('post')
    self.stubmap.GetPreCallHooks().Append('before', Pre)
    self.stubmap.RegisterStub('service1', Stub())
    self.stubmap.GetPostCallHooks().Append('after', Post)
    self.assertIsNone(self.stubmap.MakeSyncCall('service1', None, None, None))
    self.assertEqual(['pre', 'stub', 'post'], calls)

    calls = []
    self.stubmap.GetPreCallHooks().Clear()

    self.assertIsNone(apiproxy_stub_map.MakeSyncCall('service1', None,
                                                     None, None,
                                                     stubmap=self.stubmap))
    self.assertEqual(['stub', 'post'], calls)

  def testMakeSyncCallReturnValue(self):
    """Tests return value of MakeSyncCall.

    Tests that MakeSyncCall() correctly returns value returned by
    stub.MakeSyncCall() (if any) and calls hooks with correct request/response
    objects.
    """
    calls = []
    call_obj = object()
    request_obj = object()
    response_obj = object()
    response_obj_2 = object()

    def Pre(service, call, request, response):
      self.assertEqual('service1', service)
      self.assertEqual(call, call_obj)
      self.assertEqual(request, request_obj)
      self.assertEqual(response, response_obj)
      calls.append('pre')

    class Stub(object):
      def MakeSyncCall(innerself, service, call, request, response):
        calls.append('stub')
        self.assertEqual('service1', service)
        self.assertEqual(call, call_obj)
        self.assertEqual(request, request_obj)
        self.assertEqual(response, response_obj)
        return response_obj_2

    def Post(service, call, request, response):
      calls.append('post')
      self.assertEqual('service1', service)
      self.assertEqual(call, call_obj)
      self.assertEqual(request, request_obj)
      self.assertEqual(response, response_obj_2)
    self.stubmap.GetPreCallHooks().Append('before', Pre)
    self.stubmap.RegisterStub('service1', Stub())
    self.stubmap.GetPostCallHooks().Append('after', Post)
    self.assertEqual(
        response_obj_2,
        self.stubmap.MakeSyncCall('service1', call_obj, request_obj,
                                  response_obj))
    self.assertEqual(['pre', 'stub', 'post'], calls)

    calls = []
    self.stubmap.GetPreCallHooks().Clear()
    self.assertEqual(
        response_obj_2,
        self.stubmap.MakeSyncCall('service1', call_obj, request_obj,
                                  response_obj))
    self.assertEqual(['stub', 'post'], calls)

  def testMakeSyncCall_Exception(self):
    """Test end cases around rpcs that raise exceptions."""
    calls = []

    def Pre(service, call, request, response):
      calls.append('pre')

    class Stub(object):
      def MakeSyncCall(self, service, call, request, response):
        calls.append('stub')
        raise RuntimeError('stub')

    def Post4(service, call, request, response):
      calls.append('post4')
    def Post5(service, call, request, response, rpc):
      calls.append('post5')
    def Post6(service, call, request, response, rpc, error):
      calls.append('post6')
    self.stubmap.GetPreCallHooks().Append('before', Pre)
    self.stubmap.RegisterStub('service1', Stub())
    self.stubmap.GetPostCallHooks().Append('after4', Post4)
    self.stubmap.GetPostCallHooks().Append('after5', Post5)
    self.stubmap.GetPostCallHooks().Append('after6', Post6)
    self.assertRaises(RuntimeError,
                      self.stubmap.MakeSyncCall, 'service1', None, None, None)
    self.assertEqual(['pre', 'stub', 'post6'], calls)

  def testCopyStubMap(self):
    class Stub(object):
      pass

    self.stubmap.RegisterStub('service1', Stub())
    stubmap = self.stubmap._CopyStubMap()

    self.assertIn('service1', stubmap)
    self.assertLen(stubmap, 1)

    stubmap['service2'] = Stub()
    self.assertIsNone(self.stubmap.GetStub('service2'))


class BarrierRPC(apiproxy_rpc.RPC):
  """Mock low-level RPC class for barrier test."""

  def __init__(self, stub):
    apiproxy_rpc.RPC.__init__(self, stub=stub)
    self._wait_for_future = None

  def _MakeCallImpl(self):

    self._wait_for_future = self.stub.Add(self.request, self)
    apiproxy_rpc.RPC._MakeCallImpl(self)

  def _SendRequest(self):

    if self._wait_for_future:
      futures.wait([self._wait_for_future])
    apiproxy_rpc.RPC._SendRequest(self)


class BarrierStub(object):
  """Mock stub for barrier test."""

  THREADSAFE = True

  def __init__(self):
    self.queue = []
    self.rpc_to_return = None

  def CreateRPC(self):
    return self.rpc_to_return or BarrierRPC(self)

  def SetRpcToReturn(self, rpc):
    """Which RPC should CreateRPC return?

    Args:
      rpc: This RPC will be returned by next CreateRPC call.
    """
    self.rpc_to_return = rpc

  def Add(self, order, rpc):
    if rpc is None:
      rpc = 0
    if order is None:
      order = 0
    self.queue.append((order, rpc))
    self.queue.sort(key=lambda entry: entry[0])


    wait_for_future = None
    for entry in self.queue:
      if entry[1] == rpc:
        break
      wait_for_future = entry[1].future
    return wait_for_future

  def MakeSyncCall(self, service, call, request, response):
    if call == 'error':
      raise ZeroDivisionError('booh')


class BarrierTest(absltest.TestCase):
  """Tests specific for wait_any() and wait_all()."""

  def setUp(self):
    super(BarrierTest, self).setUp()
    self.stubmap = apiproxy_stub_map.APIProxyStubMap()
    self.stub = BarrierStub()
    self.stubmap.RegisterStub('barrier', self.stub)

  def testWaitAll(self):
    """Test UserRPC.wait_all()."""
    rpcs = []
    calls = []
    for i in range(5):
      def _Callback(arg=i):
        calls.append(arg)
      rpc = apiproxy_stub_map.UserRPC('barrier', callback=_Callback,
                                      stubmap=self.stubmap)
      rpc.make_call('call', i, None)
      rpcs.append(rpc)
    apiproxy_stub_map.UserRPC.wait_all([rpcs[3], rpcs[2], rpcs[1]])
    self.assertCountEqual(calls, [1, 2, 3])
    calls = []
    apiproxy_stub_map.UserRPC.wait_all(rpcs)
    self.assertCountEqual(calls, [0, 4])

    apiproxy_stub_map.UserRPC.wait_all([])

  def testWaitAny(self):
    """Test UserRPC.wait_any()."""
    rpcs = []
    calls = []

    for i in range(5):
      def _Callback(arg=i):
        calls.append(arg)
      rpc = apiproxy_stub_map.UserRPC('barrier', callback=_Callback,
                                      stubmap=self.stubmap)
      rpc.make_call('call', i, None)
      rpcs.append(rpc)


    wait_for_rpcs = [rpcs[3], rpcs[2], rpcs[1]]
    rpc = apiproxy_stub_map.UserRPC.wait_any(wait_for_rpcs)

    self.assertIn(rpc, wait_for_rpcs)
    self.assertLen(calls, 1)
    first_call = calls[0]
    self.assertEqual(rpc, rpcs[first_call])


    calls = []
    rpc = apiproxy_stub_map.UserRPC.wait_any([rpcs[0]])
    self.assertEqual(rpc, rpcs[0])
    self.assertEqual(calls, [0])



    calls = []
    rpcs = set(rpcs)
    while rpcs:
      rpc = apiproxy_stub_map.UserRPC.wait_any(rpcs)
      rpcs.remove(rpc)
    expected_calls = [1, 2, 3, 4]
    expected_calls.remove(first_call)
    self.assertCountEqual(calls, expected_calls)

    rpc = apiproxy_stub_map.UserRPC.wait_any([])
    self.assertIsNone(rpc)

  def testNoNestedCallbacks(self):
    """Test that callbacks will never be nested inside each other."""
    rpcs = []
    calls = []
    for i in range(5):
      def _Callback(arg=i):
        calls.append(arg+100)
        other_rpc = apiproxy_stub_map.UserRPC('barrier', stubmap=self.stubmap)
        other_rpc.make_call('call', arg, None)
        other_rpc.wait()
        calls.append(arg+200)
      rpc = apiproxy_stub_map.UserRPC('barrier', callback=_Callback,
                                      stubmap=self.stubmap)
      rpc.make_call('call', i, None)
      rpcs.append(rpc)
    apiproxy_stub_map.UserRPC.wait_all([rpcs[1]])
    self.assertCountEqual(calls, [101, 201])
    calls = []
    apiproxy_stub_map.UserRPC.wait_all(rpcs[:3])
    self.assertCountEqual(calls, [100, 200, 102, 202])
    calls = []
    apiproxy_stub_map.UserRPC.wait_all(rpcs)
    self.assertCountEqual(calls, [103, 203, 104, 204])

  def testCheckSuccess(self):
    """Test that check_success() doesn't raise InterruptedError."""
    rpc1 = apiproxy_stub_map.UserRPC('barrier', stubmap=self.stubmap)
    rpc1.make_call('call', 42, None)
    rpc = apiproxy_stub_map.UserRPC.wait_any([rpc1])
    self.assertIs(rpc1, rpc)
    rpc.check_success()


  def testCheckSuccess_Exception(self):
    """Test that check_success() doesn't overwrite low-level exceptions."""
    rpc1 = apiproxy_stub_map.UserRPC('barrier', stubmap=self.stubmap)
    rpc1.make_call('error', 42, None)
    rpc = apiproxy_stub_map.UserRPC.wait_any([rpc1])
    self.assertIs(rpc1, rpc)
    self.assertRaises(ZeroDivisionError, rpc.check_success)

  def testMultiThreadedWait(self):
    """Test that UserRpc() works in presence of multiple threads."""


    exceptions = []

    calls = []
    some_random_number = 42

    def Call(request):
      try:
        barrier_rpc = TestRpc(self.stub)
        self.stub.SetRpcToReturn(barrier_rpc)
        rpc1 = apiproxy_stub_map.UserRPC('barrier', stubmap=self.stubmap)
        rpc1.make_call('call', request, None)
        rpc = apiproxy_stub_map.UserRPC.wait_any([rpc1])
        self.assertIs(rpc1, rpc)
        rpc.check_success()
      except:
        exceptions.append(traceback.format_exc())

    class TestRpc(BarrierRPC):
      """Overrides BarrierRPC _SendRequest() to simulate race condition.

      When first RPC calls _SendRequest() it issues another RPC using thread.
      """

      def _SendRequest(self, *args, **kwargs):



        if not calls:
          calls.append(1)




          t = threading.Thread(target=Call, args=(some_random_number - 1,))
          t.setDaemon(True)
          t.start()
          t.join()
        else:
          calls.append(2)
        super(TestRpc, self)._SendRequest(*args, **kwargs)

    Call(some_random_number)
    self.assertEqual([1, 2], calls)
    self.assertEqual([], exceptions, '\n'.join(exceptions))


class WaitCancellerTest(absltest.TestCase):
  """Tests for WaitCanceller functionality with wait_any()."""

  def setUp(self):
    super(WaitCancellerTest, self).setUp()
    self.stubmap = apiproxy_stub_map.APIProxyStubMap()
    self.stub = BarrierStub()
    self.stubmap.RegisterStub('barrier', self.stub)

  def testWaitAny_JustCanceller(self):
    """Calling wait_any() on just the wait_canceller should return it."""
    wait_canceller = apiproxy_stub_map.WaitCanceller()
    wait_canceller.cancel()
    finished_rpc = apiproxy_stub_map.UserRPC.wait_any([wait_canceller])
    self.assertEqual(wait_canceller, finished_rpc)

    finished_rpc = apiproxy_stub_map.UserRPC.wait_any([wait_canceller])
    self.assertEqual(wait_canceller, finished_rpc)

  def testCancelCalledTwice(self):
    """Calling cancel() multiple times doesn't cause a crash."""
    wait_canceller = apiproxy_stub_map.WaitCanceller()
    wait_canceller.cancel()
    wait_canceller.cancel()
    finished_rpc = apiproxy_stub_map.UserRPC.wait_any([wait_canceller])
    self.assertEqual(wait_canceller, finished_rpc)

  def testWaitAny_CancellerFinishesFirst(self):
    """Wait on a cancelled canceller and a blocked RPC returns canceller."""

    blocking_event = threading.Event()

    class BlockingRPC(BarrierRPC):
      """RPC that blocks until blocking_event."""

      def _SendRequest(self, *args, **kwargs):
        blocking_event.wait()
        super(BlockingRPC, self)._SendRequest(*args, **kwargs)

    blocking_rpc = BlockingRPC(self.stub)
    self.stub.SetRpcToReturn(blocking_rpc)
    rpc = apiproxy_stub_map.UserRPC('barrier', stubmap=self.stubmap)
    rpc.make_call('call', 0, None)

    wait_canceller = apiproxy_stub_map.WaitCanceller()
    wait_canceller.cancel()
    finished_rpc = apiproxy_stub_map.UserRPC.wait_any([rpc, wait_canceller])
    self.assertEqual(wait_canceller, finished_rpc)

    finished_rpc = apiproxy_stub_map.UserRPC.wait_any([wait_canceller, rpc])
    self.assertEqual(wait_canceller, finished_rpc)
    blocking_event.set()

  def testWaitAny_RpcFinishesFirst(self):
    """Wait on a cancelled canceller and finished RPC should return the RPC."""
    rpc_finished = threading.Event()

    class TestRPC(BarrierRPC):
      """RPC that blocks until blocking_event."""

      def _SendRequest(self, *args, **kwargs):
        super(TestRPC, self)._SendRequest(*args, **kwargs)
        rpc_finished.set()

    blocking_rpc = TestRPC(self.stub)
    self.stub.SetRpcToReturn(blocking_rpc)
    rpc = apiproxy_stub_map.UserRPC('barrier', stubmap=self.stubmap)
    rpc.make_call('call', 0, None)

    rpc_finished.wait()
    wait_canceller = apiproxy_stub_map.WaitCanceller()
    wait_canceller.cancel()

    finished_rpc = apiproxy_stub_map.UserRPC.wait_any([rpc, wait_canceller])
    self.assertEqual(rpc, finished_rpc)

    finished_rpc = apiproxy_stub_map.UserRPC.wait_any([wait_canceller, rpc])
    self.assertEqual(rpc, finished_rpc)


def main(unused_argv):
  absltest.main()


if __name__ == '__main__':
  absltest.main(main)
