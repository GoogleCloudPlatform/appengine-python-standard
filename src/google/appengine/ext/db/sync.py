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


"""Synchronization primitives backed by the datastore.

The Mutex class's interface matches the Python standard library's
threading.Lock class.

TODO: more here

TODO: use datastore caching, once we have a reusable library for it
"""









import datetime
import random
import time

from google.appengine.ext import db
from google.appengine.api import datastore


class Mutex(db.Model):
  """A mutex backed by the datastore."""
  LIFETIME = datetime.timedelta(milliseconds=20*1000)

  _held = db.BooleanProperty(required=True, default=False)
  _last_acquired = db.DateTimeProperty(required=True, auto_now=True)

  def acquire(self, blocking=True, retry_delay_ms=100):
    """Acquire this mutex. Fails if it's already held.

    Args:
      blocking: boolean. If True, blocks until the mutex can be acquired. If
      False, returns immediately.
      retry_delay_ms: integer. The desired delay between acquisition retries.
      Each actually delay is a random amount between half and twice this.

    Returns:
      True if the mutex was acquired, False otherwise.
    """
    if not self.is_saved():
      self.put()

    while True:
      mutex = db.run_in_transaction(self._acquire_or_fail)
      if mutex is not None:

        self._held = True
        self._last_acquired = mutex._last_acquired
        return True
      elif not blocking:
        return False
      else:
        retry_delay_s = float(retry_delay_ms) / 1000
        time.sleep(random.uniform(retry_delay_s / 2, retry_delay_s * 2))

  def release(self):
    """Releases the mutex. Raises db.BadRequestError if not currently held."""
    if not self.is_saved():
      raise db.BadRequestError("Can't release mutex that's not saved.")

    db.run_in_transaction(self._release_or_fail)


    self._held = False

  def is_held(self):
    """Returns true if the mutex is held, false otherwise.

    This takes expiration into account.
    """
    elapsed = datetime.datetime.now() - self._last_acquired
    return self._held and elapsed < Mutex.LIFETIME

  def _acquire_or_fail(self):
    """Acquires the given mutex.

    Intended to be run in a transaction.

    Returns:
      The mutex if it was acquired, otherwise None.
    """
    mutex = Mutex.get(self.key())
    if not mutex.is_held():
      mutex._held = True
      mutex.put()
      return mutex
    else:
      return None

  def _release_or_fail(self):
    """Releases the given mutex. Raises db.BadRequestError if it's held.

    Intended to be run in a transaction.

    Returns:
      Mutex
    """
    mutex = Mutex.get(self.key())
    if mutex.is_held():
      mutex._held = False
      mutex.put()
      return mutex
    else:
      raise db.BadRequestError("Can't release mutex that's not held.")


def acquire(mutexes, blocking=True):
  """Acquires the given mutexes.

  To prevent deadlocks, mutexes are acquired in order of the partial ordering
  defined by their keys.

  Args:
    mutexes: sequence of Mutex objects or keys
    blocking: boolean. If True, blocks until all mutexes can be acquired. If
      False, returns immediately.

  Returns:
    True if all mutexes were acquired, False otherwise.
  """

  mutexes = _to_mutexes(mutexes)
  mutexes.sort(key=lambda m: m.key())

  acquired = []

  try:
    for mutex in mutexes:
      if mutex.acquire(blocking=blocking):
        acquired.append(mutex)
      else:
        return False
  finally:
    if len(acquired) < len(mutexes):
      release(acquired)

  return True

def release(mutexes):
  """Releases the given mutexes.

  Mutexes are released according to the reverse of the partial ordering
  defined by their keys. This isn't strictly necessary to prevent deadlocks,
  but it's still a nice practice.

  Args:
    mutexes: sequence of Mutex objects or keys
  """
  mutexes = _to_mutexes(mutexes)
  mutexes.sort(key=lambda m: m.key(), reverse=True)

  for mutex in mutexes:
    mutex.release()


def _to_mutexes(mutexes_or_keys):
  """Normalizes and type checks the given sequence.

  Args:
    mutexes_or_keys: sequence of Mutex objects or keys

  Returns:
    list of Mutexes
  """
  mutexes = []

  for arg in mutexes_or_keys:
    if isinstance(arg, Mutex):
      mutexes.append(arg)
    elif isinstance(arg, db.Key):
      mutexes.append(Mutex.get(arg))
    else:
      raise db.BadArgumentError(
          'Expected a Mutex instance or key; received %s (a %s).' %
          (arg, datastore.typename(arg)))

  return mutexes
