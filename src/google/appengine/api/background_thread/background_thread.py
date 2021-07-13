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


"""Background Threads API.

An API for creating background threads.

Background threads created using this API do not inherit the context of their
creator and do not need to end before the creator request completes.
"""



__all__ = ['start_new_background_thread',
           'BackgroundThread',
           'Error',
           'FrontendsNotSupported',
           'BackgroundThreadLimitReachedError',
          ]

import collections
import threading
import six

from google.appengine.api import apiproxy_stub_map
from google.appengine.api.system import system_service_pb2
from google.appengine.runtime import apiproxy_errors
from google.appengine.runtime import background


class Error(Exception):
  """Base exception class for this module."""


class FrontendsNotSupported(Error):
  """Error raised when a background thread is requested on a front end."""


class BackgroundThreadLimitReachedError(Error):
  """Error raised when no further active background threads can be created."""

ERROR_MAP = collections.defaultdict(lambda: Error, {
    system_service_pb2.SystemServiceError.BACKEND_REQUIRED:
    FrontendsNotSupported,
    system_service_pb2.SystemServiceError.LIMIT_REACHED:
    BackgroundThreadLimitReachedError,
})


def start_new_background_thread(target, args, kwargs=None):
  """Starts a new background thread.

  Creates a new background thread which will call target(*args, **kwargs).

  Args:
    target: A callable for the new thread to run.
    args: Position arguments to be passed to target.
    kwargs: Keyword arguments to be passed to target.

  Returns:
    The thread ID of the background thread.
  """

  if kwargs is None:
    kwargs = {}
  request = system_service_pb2.StartBackgroundRequestRequest()
  response = system_service_pb2.StartBackgroundRequestResponse()
  try:
    apiproxy_stub_map.MakeSyncCall('system', 'StartBackgroundRequest', request,
                                   response)
  except apiproxy_errors.ApplicationError as error:
    raise ERROR_MAP[error.application_error](error.error_detail)
  else:
    return background.EnqueueBackgroundThread(
        response.request_id,
        target,
        args,
        kwargs)


class BackgroundThread(threading.Thread):
  """A threading.Thread-like interface for background threads."""

  if six.PY2:

    def _bootstrap(self):
      self._Thread__bootstrap()

    @property
    def _initialized(self):
      return self._Thread__initialized

    @property
    def _started(self):
      return self._Thread__started

  else:

    def _bootstrap(self):
      try:
        super(BackgroundThread, self)._bootstrap()
      finally:


        if self._tstate_lock:
          self._tstate_lock.release()

    def _set_tstate_lock(self):
      """Use threading.Lock instead of calling _set_sentinel().

      Because it's not a real thread, _set_sentinel() will create a lock that
      will never be released automatically and moreover it will break such lock
      for real thread that executing this one.
      """
      self._tstate_lock = threading.Lock()
      self._tstate_lock.acquire()




  def start(self):
    """Starts this background thread."""
    if not self._initialized:
      raise RuntimeError('thread.__init__() not called')

    if self._started.is_set():
      raise RuntimeError('threads can only be started once')
    with threading._active_limbo_lock:
      threading._limbo[self] = self
    try:
      start_new_background_thread(self._bootstrap, ())
    except Exception:
      with threading._active_limbo_lock:
        del threading._limbo[self]
      raise
    self._started.wait()
