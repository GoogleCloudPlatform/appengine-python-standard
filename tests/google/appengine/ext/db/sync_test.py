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



"""Tests for google.appengine.ext.db.sync."""




from google.appengine.tools import os_compat

import datetime
import threading

from google.appengine.api import datastore_base_testutil
from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import db
from google.appengine.ext.db import sync
from absl.testing import absltest








class MutexTest(datastore_base_testutil.IdTestMixin, absltest.TestCase):
  """Unit tests for the Mutex class."""

  class RecordingMutex(sync.Mutex):
    """Records the timestamp of each acquire() call."""


    acquire_attempts = {}
    release_attempts = {}

    @classmethod
    def clear_attempts(cls):
      """Clears the acquire_attempts dict."""
      cls.acquire_attempts.clear()
      cls.release_attempts.clear()

    def _acquire_or_fail(self):
      self.acquire_attempts[datetime.datetime.now()] = self.key()
      return super(MutexTest.RecordingMutex, self)._acquire_or_fail()

    def _release_or_fail(self):
      self.release_attempts[datetime.datetime.now()] = self.key()
      return super(MutexTest.RecordingMutex, self)._release_or_fail()

  def setUp(self):
    super(MutexTest, self).setUp()

    self.apiproxy.GetStub('datastore_v3').SetAutoIdPolicy(
        datastore_stub_util.SEQUENTIAL)
    self.RecordingMutex.clear_attempts()

  def testAcquireAndRelease(self):
    mutex = sync.Mutex()
    mutex.put()
    self.assertTrue(mutex.acquire())
    mutex.release()
    self.assertEqual(False, mutex._held)

  def testLastAcquiredTimestamp(self):
    mutex = sync.Mutex()
    mutex.put()
    self.assertEqual(False, mutex._held)
    orig_last_acquired = mutex._last_acquired

    self.assertTrue(mutex.acquire())
    self.assertEqual(True, mutex._held)
    self.assertNotEqual(orig_last_acquired, mutex._last_acquired)



    elapsed = datetime.datetime.now() - mutex._last_acquired
    self.assertLess(elapsed.seconds, 2)

    mutex.release()

  def testReleaseUnheld(self):
    mutex = sync.Mutex()
    self.assertRaises(db.BadRequestError, mutex.release)

    self.assertTrue(mutex.acquire())
    mutex.release()
    self.assertRaises(db.BadRequestError, mutex.release)

  def testIsHeld(self):
    mutex = sync.Mutex()
    self.assertFalse(mutex.is_held())
    mutex.put()
    self.assertFalse(mutex.is_held())

    self.assertTrue(mutex.acquire())
    self.assertTrue(mutex.is_held())
    mutex.release()
    self.assertFalse(mutex.is_held())

    self.assertTrue(mutex.acquire())
    mutex._last_acquired -= sync.Mutex.LIFETIME
    self.assertFalse(mutex.is_held())

  def testNonBlocking(self):
    mutex = self.RecordingMutex()
    self.assertTrue(mutex.acquire())
    self.assertEqual(1, len(self.RecordingMutex.acquire_attempts))

    self.assertFalse(mutex.acquire(blocking=False))
    self.assertTrue(mutex.is_held())
    self.assertEqual(2, len(self.RecordingMutex.acquire_attempts))

    mutex.release()
    self.assertFalse(mutex.is_held())
    self.assertTrue(mutex.acquire(blocking=False))
    self.assertTrue(mutex.is_held())
    self.assertEqual(3, len(self.RecordingMutex.acquire_attempts))

  class RetryingMutex(RecordingMutex):
    """Reports that it's held to make acquire() retry."""
    TRIES = 5

    def is_held(self):
      if len(self.acquire_attempts) < self.TRIES:
        return True
      else:
        return super(MutexTest.RetryingMutex, self).is_held()

  def testBlocking(self):
    mutex = self.RetryingMutex()
    self.assertTrue(mutex.acquire(blocking=True, retry_delay_ms=10))

    self.assertEqual(self.RetryingMutex.TRIES, len(mutex.acquire_attempts))
    timestamps = sorted(mutex.acquire_attempts.keys())
    for start, end in zip(timestamps[:-1], timestamps[1:]):
      delay = end - start
      self.assertGreaterEqual(delay.microseconds, 5000)



      self.assertLessEqual(delay.microseconds, 50000 * 9)

  def testContention(self):
    """Use threads to test that a mutex can only have one owner at a time."""
    mutex = sync.Mutex()
    self.assertTrue(mutex.acquire())

    started = threading.Event()
    acquired = threading.Event()

    def try_to_acquire():
      started.set()
      mutex.acquire()
      acquired.set()

    thread = threading.Thread(target=try_to_acquire)
    thread.start()
    started.wait()
    acquired.wait(1)
    self.assertFalse(acquired.isSet())

    mutex.release()
    acquired.wait(1)
    self.assertTrue(acquired.isSet())

    thread.join()

  def AssertAllHeld(self, mutexes, held):
    """Asserts that all of the mutexes are either held or not.

    Args:
      mutexes: sequence of Mutex
      held: boolean
    """
    for mutex in mutexes:
      self.assertEqual(held, mutex.is_held())

  def testAcquireAndReleaseMultipleBlocking(self):
    """Test sync.acquire() and sync.release() with multiple mutexes.

    They should always be acquired in the same partial ordering, by key.
    """
    mutexes = [self.RecordingMutex(),
               self.RecordingMutex(),
               self.RecordingMutex()]

    for mutex in mutexes:

      db.put(mutex)

    keys = [m.key() for m in mutexes]
    self.assertGreater(keys[1], keys[0])
    self.assertGreater(keys[2], keys[1])

    self.assertTrue(sync.acquire(reversed(mutexes)))
    self.AssertAllHeld(mutexes, True)


    acquires = sorted(self.RecordingMutex.acquire_attempts.items())
    self.assertListEqual(keys, [key for time, key in acquires])

    sync.release(mutexes)
    self.AssertAllHeld(mutexes, False)


    releases = sorted(self.RecordingMutex.release_attempts.items())
    self.assertListEqual(list(reversed(keys)), [key for time, key in releases])


    self.assertTrue(sync.acquire(keys))
    self.AssertAllHeld(db.get(keys), True)
    sync.release(keys)
    self.AssertAllHeld(db.get(keys), False)

  def testAcquireAndReleaseMultipleNonBlocking(self):
    """Test non-blocking sync.acquire() and release() with multiple mutexes."""
    mutexes = [self.RecordingMutex(),
               self.RecordingMutex(),
               self.RecordingMutex()]

    for mutex in mutexes:
      db.put(mutex)

    self.assertTrue(sync.acquire(mutexes, blocking=False))
    self.AssertAllHeld(mutexes, True)
    sync.release(mutexes)
    self.AssertAllHeld(mutexes, False)


    mutexes[2].acquire()
    self.RecordingMutex.clear_attempts()

    self.assertFalse(sync.acquire(reversed(mutexes), blocking=False))
    self.AssertAllHeld(mutexes[:2], False)



    releases = sorted(self.RecordingMutex.release_attempts.items())
    self.assertListEqual([mutexes[1].key(), mutexes[0].key()],
                         [key for time, key in releases])


    last_acquire = max(self.RecordingMutex.acquire_attempts.keys())
    for release in self.RecordingMutex.release_attempts.keys():
      self.assertGreater(release, last_acquire)

  class ExceptionMutex(sync.Mutex):
    """Raises BadRequestError on acquire()."""
    def acquire(self, blocking=True):
      raise db.BadRequestError()

    @classmethod
    def kind(cls):
      """Override the kind so that the key comes after RecordingMutexes."""
      return 'ZExceptionMutex'

  def testReleaseOnExceptionInMultipleAcquire(self):
    """If an acquire hits an exception, the other mutexes should be released."""
    mutexes = [self.RecordingMutex(), self.ExceptionMutex()]
    for mutex in mutexes:
      mutex.put()

    self.assertRaises(db.BadRequestError, sync.acquire, mutexes)
    self.AssertAllHeld(mutexes, False)
    self.assertEqual(1, len(self.RecordingMutex.acquire_attempts))
    self.assertEqual(1, len(self.RecordingMutex.release_attempts))


if __name__ == '__main__':
  absltest.main()
