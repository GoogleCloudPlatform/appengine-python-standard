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


"""Tests for google.appengine.api.background_thread.background_thread."""



import contextlib
import random
import threading
import google
import mock
import mox
import requests

from google.appengine.api import titanoboa_request_info
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import request_info
from google.appengine.api.background_thread import background_thread
from google.appengine.api.system import system_service_pb2
from google.appengine.api.system import system_stub
from google.appengine.runtime import apiproxy_errors
from google.appengine.runtime import background
from absl.testing import absltest


class BackgroundThreadExecutor(object):
  """Emulates worker executing background threads. For tests only."""

  def __init__(self, thread_join_timeout=3):
    self._event = threading.Event()
    self._queue = []
    self._keep_running = True
    self._thread = None
    self._timeout = thread_join_timeout

  def _Enqueue(self, request_id, target, args, kwargs):

    t = threading.Thread(
        target=

        background._pending_background_threads.EnqueueBackgroundThread,
        args=(request_id, target, args, kwargs))
    t.start()
    self._queue.append(request_id)
    self._event.set()
    t.join()

  def _Start(self):
    self._thread = threading.Thread(target=self._RunLoop)
    self._thread.start()

  def _Stop(self):
    self._keep_running = False
    self._event.set()
    self._thread.join(self._timeout)

  def _RunLoop(self):
    while self._keep_running:
      while self._queue:
        request_id = self._queue.pop(0)
        background._pending_background_threads.RunBackgroundThread(
            request_id)
      self._event.wait()
      self._event.clear()

  def HasBeenFinishedCorrectly(self):
    return self._thread and not self._thread.is_alive()

  def _StartBackgroundRequest(self, service, call, unused_request, response):
    assert (service, call) == ('system', 'StartBackgroundRequest')
    response.request_id = str(random.randint(1, 1000))
    return response

  @contextlib.contextmanager
  def ApplyPatchAndRun(self):
    with mock.patch.object(
        apiproxy_stub_map, 'MakeSyncCall', new=self._StartBackgroundRequest):
      with mock.patch.object(
          background, 'EnqueueBackgroundThread', new=self._Enqueue):
        self._Start()
        try:
          yield self
        finally:
          self._Stop()


class BackgroundThreadTest(absltest.TestCase):

  def setUp(self):
    self.mox = mox.Mox()
    self.mocked_get = mock.patch.object(requests, 'get')
    self.mocked_get.start()

  def tearDown(self):
    self.mox.UnsetStubs()
    self.mox.ResetAll()
    self.mocked_get.stop()

  def MakeResponsePopulator(self, request_id, start_real_thread=False):

    def PopulateResponse(unused_package, unused_call, unused_request, response):
      response.request_id = request_id
      if start_real_thread:
        threading.Thread(
            target=background._pending_background_threads.RunBackgroundThread,
            args=(request_id,)).start()

    return PopulateResponse

  def RunStartBackgroundThreadErrorTest(self, error, expected_exception):
    expected_request = system_service_pb2.StartBackgroundRequestRequest()
    empty_response = system_service_pb2.StartBackgroundRequestResponse()

    self.mox.StubOutWithMock(apiproxy_stub_map, 'MakeSyncCall')
    self.mox.StubOutWithMock(background, 'EnqueueBackgroundThread')

    apiproxy_stub_map.MakeSyncCall('system', 'StartBackgroundRequest',
                                   expected_request,
                                   empty_response).AndRaise(
                                       apiproxy_errors.ApplicationError(error))
    self.mox.ReplayAll()
    with self.assertRaises(expected_exception):
      background_thread.start_new_background_thread(target=1, args=2, kwargs=3)
    self.mox.VerifyAll()

  def RunBackgroundThreadErrorTest(self, error, expected_exception):
    expected_request = system_service_pb2.StartBackgroundRequestRequest()
    empty_response = system_service_pb2.StartBackgroundRequestResponse()

    self.mox.StubOutWithMock(apiproxy_stub_map, 'MakeSyncCall')
    self.mox.StubOutWithMock(background, 'EnqueueBackgroundThread')

    apiproxy_stub_map.MakeSyncCall('system', 'StartBackgroundRequest',
                                   expected_request,
                                   empty_response).AndRaise(
                                       apiproxy_errors.ApplicationError(error))
    self.mox.ReplayAll()

    with self.assertRaises(expected_exception):
      background_thread.BackgroundThread(target=1, args=2, kwargs=3).start()
    self.mox.VerifyAll()

  def testStartNewBackgroundThread(self):
    expected_request = system_service_pb2.StartBackgroundRequestRequest()
    empty_response = system_service_pb2.StartBackgroundRequestResponse()

    self.mox.StubOutWithMock(apiproxy_stub_map, 'MakeSyncCall')
    self.mox.StubOutWithMock(background, 'EnqueueBackgroundThread')

    apiproxy_stub_map.MakeSyncCall('system', 'StartBackgroundRequest',
                                   expected_request,
                                   empty_response).WithSideEffects(
                                       self.MakeResponsePopulator('foo'))
    background.EnqueueBackgroundThread('foo', 1, 2, 3).AndReturn(42)
    apiproxy_stub_map.MakeSyncCall('system', 'StartBackgroundRequest',
                                   expected_request,
                                   empty_response).WithSideEffects(
                                       self.MakeResponsePopulator('bar'))
    background.EnqueueBackgroundThread('bar', 4, 5, {}).AndReturn(43)
    self.mox.ReplayAll()

    self.assertEqual(42, background_thread.start_new_background_thread(1, 2, 3))
    self.assertEqual(43, background_thread.start_new_background_thread(4, 5))
    self.mox.VerifyAll()

  def testStartNewBackgroundThreadFrontendError(self):
    self.RunStartBackgroundThreadErrorTest(
        system_service_pb2.SystemServiceError.BACKEND_REQUIRED,
        background_thread.FrontendsNotSupported)

  def testStartNewBackgroundThreadBackgroundThreadLimitReachedError(self):
    self.RunStartBackgroundThreadErrorTest(
        system_service_pb2.SystemServiceError.LIMIT_REACHED,
        background_thread.BackgroundThreadLimitReachedError)

  def testStartNewBackgroundThreadInternalError(self):
    self.RunStartBackgroundThreadErrorTest(
        system_service_pb2.SystemServiceError.INTERNAL_ERROR,
        background_thread.Error)

  def testBackgroundThread(self):
    expected_request = system_service_pb2.StartBackgroundRequestRequest()
    empty_response = system_service_pb2.StartBackgroundRequestResponse()

    self.mox.StubOutWithMock(apiproxy_stub_map, 'MakeSyncCall')

    apiproxy_stub_map.MakeSyncCall('system', 'StartBackgroundRequest',
                                   expected_request,
                                   empty_response).WithSideEffects(
                                       self.MakeResponsePopulator('foo', True))
    apiproxy_stub_map.MakeSyncCall('system', 'StartBackgroundRequest',
                                   expected_request,
                                   empty_response).WithSideEffects(
                                       self.MakeResponsePopulator('bar', True))
    apiproxy_stub_map.MakeSyncCall('system', 'StartBackgroundRequest',
                                   expected_request,
                                   empty_response).WithSideEffects(
                                       self.MakeResponsePopulator('baz', True))
    self.mox.ReplayAll()

    s = set()

    def AddToSet(value, other_value=None):
      s.add(value)
      if other_value:
        s.add(other_value)

    thread = background_thread.BackgroundThread(target=AddToSet, args=(1,))
    thread.start()
    thread.join()
    self.assertEqual(s, set([1]))
    thread = background_thread.BackgroundThread(target=AddToSet, args=(2,),
                                                kwargs={'other_value': 3})
    thread.start()
    thread.join()
    self.assertEqual(s, set([1, 2, 3]))
    thread = background_thread.BackgroundThread(target=AddToSet, args=(4,),
                                                kwargs={'other_value': 5,
                                                        'fake': 6})
    thread.start()
    thread.join()
    self.assertEqual(s, set([1, 2, 3]))
    self.mox.VerifyAll()

  def testBackgroundThreadFrontendError(self):
    self.RunBackgroundThreadErrorTest(
        system_service_pb2.SystemServiceError.BACKEND_REQUIRED,
        background_thread.FrontendsNotSupported)

  def testBackgroundThreadBackgroundThreadLimitReachedError(self):
    self.RunBackgroundThreadErrorTest(
        system_service_pb2.SystemServiceError.LIMIT_REACHED,
        background_thread.BackgroundThreadLimitReachedError)

  def testBackgroundThreadInternalError(self):
    self.RunBackgroundThreadErrorTest(
        system_service_pb2.SystemServiceError.INTERNAL_ERROR,
        background_thread.Error)

  def testBackgroundThreadFinishing(self):
    """Tests that background thread can be joined correctly."""
    executor = BackgroundThreadExecutor()
    with executor.ApplyPatchAndRun():
      bg_thread = background_thread.BackgroundThread(target=lambda: True)
      bg_thread.start()
      bg_thread.join(3)
      self.assertFalse(bg_thread.is_alive())
    self.assertTrue(executor.HasBeenFinishedCorrectly())


class BackgroundThreadStubTest(absltest.TestCase):

  def setUp(self):
    super(BackgroundThreadStubTest, self).setUp()
    self.mocked_get = mock.patch.object(requests, 'get')
    self.mocked_random = mock.patch.object(
        random, 'randrange', return_value=255)
    self.mocked_get.start()
    self.mocked_random.start()
    self.request_data = titanoboa_request_info.LocalRequestInfo(
        'http://non-existing.address')
    self.stub = system_stub.SystemServiceStub(request_data=self.request_data)

  def tearDown(self):
    self.mocked_get.stop()
    self.mocked_random.stop()
    super(BackgroundThreadStubTest, self).tearDown()

  def testSuccess(self):
    response = system_service_pb2.StartBackgroundRequestResponse()
    self.stub._Dynamic_StartBackgroundRequest(None, response, 'request id')
    self.assertEqual('ff', response.request_id)

  def testAutoScalingFrontend(self):
    with mock.patch.object(
        self.request_data.get_dispatcher(),
        'send_background_request',
        side_effect=request_info.NotSupportedWithAutoScalingError()):
      with self.assertRaises(apiproxy_errors.ApplicationError) as e:
        self.stub._Dynamic_StartBackgroundRequest(None, None, 'request id')
      self.assertEqual(e.exception.application_error,
                       system_service_pb2.SystemServiceError.BACKEND_REQUIRED)

  def testLimitReached(self):
    with mock.patch.object(
        self.request_data.get_dispatcher(),
        'send_background_request',
        side_effect=request_info.BackgroundThreadLimitReachedError()):
      with self.assertRaises(apiproxy_errors.ApplicationError) as e:
        self.stub._Dynamic_StartBackgroundRequest(None, None, 'request id')
      self.assertEqual(e.exception.application_error,
                       system_service_pb2.SystemServiceError.LIMIT_REACHED)

if __name__ == '__main__':
  absltest.main()
