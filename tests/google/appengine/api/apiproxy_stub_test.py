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


"""Tests for google.appengine.api.apiproxy_stub."""



import random

from google.appengine.api import apiproxy_stub
from google.appengine.runtime import apiproxy_errors
from absl.testing import absltest


class FakePB(object):
  def __init__(self, byte_size=10):
    self.__byte_size = byte_size

  def IsInitialized(self, messages):
    return True

  def ByteSize(self):
    return self.__byte_size


class UninitializedPB(object):
  def IsInitialized(self, messages):
    return False

  def ByteSize(self):
    return 42


class FakeStub(apiproxy_stub.APIProxyStub):
  """A fake stub for testing."""

  def __init__(self,
               service_name='fake',
               max_request_size=apiproxy_stub.MAX_REQUEST_SIZE):
    super(FakeStub, self).__init__(service_name,
                                   max_request_size=max_request_size)
    self.calls = []

  def _Dynamic_method1(self, request, response):
    self.calls.append(('method1', request, response))

  def _Dynamic_method2(self, request, response):
    self.calls.append(('method2', request, response))


class APIProxyStubTest(absltest.TestCase):
  """Tests for API proxy stub."""

  def setUp(self):
    self.stub = FakeStub()

  def testMakeCallAsync(self):
    """Tests making calls asynchronously."""
    rpc1 = self.stub.CreateRPC()
    request1 = FakePB()
    response1 = FakePB()
    rpc1.MakeCall('fake', 'method1', request1, response1)

    rpc2 = self.stub.CreateRPC()
    request2 = FakePB()
    response2 = FakePB()
    rpc2.MakeCall('fake', 'method2', request2, response2)

    rpc1.Wait()
    rpc1.CheckSuccess()

    rpc2.Wait()
    rpc2.CheckSuccess()

    self.assertSameElements([('method1', request1, response1),
                             ('method2', request2, response2)],
                            self.stub.calls)

  def testMakeSyncCall(self):
    """Tests making calls to stub."""
    request1 = FakePB()
    response1 = FakePB()
    self.stub.MakeSyncCall('fake', 'method1', request1, response1)

    request2 = FakePB()
    response2 = FakePB()
    self.stub.MakeSyncCall('fake', 'method2', request2, response2)

    self.assertEquals([('method1', request1, response1),
                       ('method2', request2, response2)],
                      self.stub.calls)

  def testUnitializedPB(self):
    """Tests response to un-unitialized request buffer."""
    self.assertRaises(AssertionError,
                      self.stub.MakeSyncCall,
                      'fake',
                      'method1',
                      UninitializedPB(),
                      FakePB())

  def testMissingMethod(self):
    """Test when unknown method is called."""
    self.assertRaises(AttributeError,
                      self.stub.MakeSyncCall,
                      'fake',
                      'no_such_method',
                      FakePB(),
                      FakePB())

  def testWrongService(self):
    """Tests response to un-unitialized request buffer."""
    self.assertRaises(AssertionError,
                      self.stub.MakeSyncCall,
                      'wrong',
                      'method1',
                      FakePB(),
                      FakePB())

  def testRequestTooLarge(self):
    """Tests we error when the request PB is too large."""
    stub = FakeStub(max_request_size=5)
    self.assertRaises(apiproxy_errors.RequestTooLargeError,
                      stub.MakeSyncCall,
                      'fake',
                      'method1',
                      FakePB(byte_size=6),
                      FakePB())

  def testAlternateServiceName(self):
    """Tests ability to use different service name."""
    self.stub = FakeStub('alternate')
    self.assertRaises(AssertionError,
                      self.stub.MakeSyncCall,
                      'fake',
                      'method1',
                      FakePB(),
                      FakePB())

    request1 = FakePB()
    response1 = FakePB()
    self.stub.MakeSyncCall('alternate', 'method1', request1, response1)

    request2 = FakePB()
    response2 = FakePB()
    self.stub.MakeSyncCall('alternate', 'method2', request2, response2)

    self.assertEquals([('method1', request1, response1),
                       ('method2', request2, response2)],
                      self.stub.calls)

  def testSetError(self):
    """Tests ability to set stub to always raise and error."""
    request1 = FakePB()
    response1 = FakePB()
    error = apiproxy_errors.OverQuotaError()
    self.stub.SetError(error)
    self.assertRaises(apiproxy_errors.OverQuotaError, self.stub.MakeSyncCall,
        'fake', 'method1', request1, response1)

  def testSetErrorNone(self):
    """Test what happens when setting error to None."""
    request1 = FakePB()
    response1 = FakePB()
    error = apiproxy_errors.OverQuotaError()
    self.stub.SetError(error)
    self.stub.SetError(None)
    self.stub.MakeSyncCall('fake', 'method1', request1, response1)

  def testSetErrorRateZero(self):
    """Test setting the error rate to Zero."""
    request1 = FakePB()
    response1 = FakePB()
    error = apiproxy_errors.OverQuotaError()
    self.stub.SetError(error, error_rate=0)
    self.stub.MakeSyncCall('fake', 'method1', request1, response1)

  def testSetMethodError(self):
    """Test setting an error for a method."""
    request1 = FakePB()
    response1 = FakePB()
    error = apiproxy_errors.OverQuotaError()
    self.stub.SetError(error, method='method1')
    self.assertRaises(apiproxy_errors.OverQuotaError, self.stub.MakeSyncCall,
        'fake', 'method1', request1, response1)

  def testSetMethodRandomError(self):
    """Test setting random rates for a method."""
    request1 = FakePB()
    response1 = FakePB()
    error = apiproxy_errors.OverQuotaError()
    self.stub.SetError(error, method='method1', error_rate=0.5)
    old_random = random.random

    def FakeRandom():
      yield 0.50
      yield 0.51
    try:
      fakeRandom = FakeRandom()
      random.random = lambda: next(fakeRandom)
      self.assertRaises(
          apiproxy_errors.OverQuotaError,
          self.stub.MakeSyncCall,
          'fake',
          'method1',
          request1,
          response1)
      self.stub.MakeSyncCall('fake', 'method1', request1, response1)
    finally:
      random.random = old_random

  def testSetNonApiProxyError(self):
    """Tests anything other than an api proxy error as a condition fails."""
    self.assertRaises(AssertionError, self.stub.SetError, TypeError())
    self.assertRaises(AssertionError, self.stub.SetError, TypeError)
    self.assertRaises(AssertionError, self.stub.SetError, 'whatever')


if __name__ == '__main__':
  absltest.main()
