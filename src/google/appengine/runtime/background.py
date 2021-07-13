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


"""Background thread handler.

Provides a way to create new threads which are not bound to the creator's
request context and do not need to end before the creator request completes.
"""



import logging
import sys
import threading
import traceback

from google.appengine.runtime import request_environment
import six.moves._thread

BACKGROUND_REQUEST_ID = 'HTTP_X_APPENGINE_BACKGROUNDREQUEST'


class _BackgroundRequest(object):
  """A class for coordinating between a background thread and its creator.

  This facilitates swapping target, args and kwargs for thread_id between the
  background thread creator and the background thread.
  """

  def __init__(self):
    self._ready_condition = threading.Condition()
    self._callable_ready = False
    self._thread_id_ready = False

  def ProvideCallable(self, target, args, kwargs):
    """Sets the target and the args to be provided to this background request.

    Args:
      target: A callable for the background thread to execute.
      args: A tuple of positional args to be passed to target.
      kwargs: A dict of keyword args to be passed to target.

    Returns:
      The thread ID of the thread servicing this background request.
    """
    with self._ready_condition:
      self._target = target
      self._args = args
      self._kwargs = kwargs
      self._callable_ready = True
      self._ready_condition.notify()
      while not self._thread_id_ready:
        self._ready_condition.wait()
      return self._thread_id

  def WaitForCallable(self):
    """Sets the thread ID and returns the callable and args for this request.

    This will block until the request details have been set.

    Returns:
      A tuple (target, args, kwargs) where
        target: A callable for the background thread to execute.
        args: A tuple of positional args to be passed to target.
        kwargs: A dict of keyword args to be passed to target.
    """
    with self._ready_condition:
      self._thread_id = six.moves._thread.get_ident()
      self._thread_id_ready = True
      self._ready_condition.notify()
      while not self._callable_ready:
        self._ready_condition.wait()
      return self._target, self._args, self._kwargs


class _BackgroundRequestsContainer(object):
  """A container for storing pending background thread requests."""

  def __init__(self):
    self._requests = {}
    self._lock = threading.Lock()

  def _GetOrAddRequest(self, request_id):
    with self._lock:
      if request_id in self._requests:
        return self._requests[request_id]
      else:
        request = _BackgroundRequest()
        self._requests[request_id] = request
        return request

  def _RemoveRequest(self, request_id):
    with self._lock:
      del self._requests[request_id]

  def EnqueueBackgroundThread(self, request_id, target, args, kwargs):
    """Enqueues a new background thread request for a certain request ID.

    Args:
      request_id: A str containing the request ID for this background thread.
      target: A callable for the background thread to execute.
      args: A tuple of positional args to be passed to target.
      kwargs: A dict of keyword args to be passed to target.

    Returns:
      The thread_id of the background thread.
    """
    request = self._GetOrAddRequest(request_id)
    return request.ProvideCallable(target, args, kwargs)

  def RunBackgroundThread(self, request_id):
    """Runs the callable enqueued for the specified request ID."""
    request = self._GetOrAddRequest(request_id)
    target, args, kwargs = request.WaitForCallable()
    self._RemoveRequest(request_id)
    target(*args, **kwargs)

_pending_background_threads = _BackgroundRequestsContainer()


def EnqueueBackgroundThread(request_id, target, args, kwargs):
  """Enqueues a new background thread request for a certain request ID.

  Args:
    request_id: A str containing the request ID for this background thread.
    target: A callable for the background thread to execute.
    args: A tuple of positional args to be passed to target.
    kwargs: A dict of keyword args to be passed to target.

  Returns:
    The thread_id of the background thread.
  """
  return _pending_background_threads.EnqueueBackgroundThread(
      request_id, target, args, kwargs)


def _HandleNoInit(environ):
  """Handles a background request, skipping request initialization."""

  try:
    request_id = environ[BACKGROUND_REQUEST_ID]
    _pending_background_threads.RunBackgroundThread(request_id)

  except:
    exception = sys.exc_info()


    tb = exception[2].tb_next
    if tb:
      tb = tb.tb_next
    message = ''.join(traceback.format_exception(exception[0], exception[1],
                                                 tb))
    logging.error(message)
    return dict(error=1, response_code=500, message=message)

  return dict(error=0, response_code=200, message='OK')


def Handle(environ):
  """Handles a background request.

  This function is called by the runtime in response to an /_ah/background
  request.

  Args:
    environ: A dict containing the environ for this request (i.e. for
        os.environ).

  Returns:
    A dict containing:
      error: App Engine error code. 0 if completed successfully, 1 otherwise.
      response_code: The HTTP response code. 200 if completed successfully, 500
          otherwise.
      logs: A list of tuples (timestamp_usec, severity, message) of log
          entries.  timestamp_usec is a long, severity is int and message is
          str.  Severity levels are 0..4 for Debug, Info, Warning, Error,
          Critical.
  """
  request_environment.current_request.Init(sys.stderr, environ)
  try:
    response = _HandleNoInit(environ)
  finally:
    request_environment.current_request.Clear()
  return response


def App(environ, start_response):
  """Present Handle() as a WSGI app for Titanoboa."""




  response = _HandleNoInit(environ)
  start_response(str(response['response_code']) + ' ' + response['message'],
                 [('Content-Type', 'text/plain')])
  yield str(response).encode()
