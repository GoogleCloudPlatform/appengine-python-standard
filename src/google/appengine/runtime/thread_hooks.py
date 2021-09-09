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
"""Helper module for hooking into thread module.

Thread_hooks module enables adding user provided hooks into threading module.
"""

import abc
import importlib
import multiprocessing.dummy
import threading

import contextvars
from google.appengine.runtime import request_environment
import six.moves._thread as thread


class ThreadHook(object):
  """ThreadHook provides an interface for pre/post work on thread creation."""
  __metaclass__ = abc.ABCMeta

  def __init__(self):
    """Called in spawning thread before start_new_thread to capture state."""
    pass

  @abc.abstractmethod
  def PreTarget(self):
    """Runs before the thread's target in the spawned thread."""
    pass

  @abc.abstractmethod
  def PostTarget(self):
    """Runs after the thread's target in the spawned thread.

        Note that threading.Thread.join() does not guarantee PostTarget runs
        before returning.
    """
    pass


class RequestEnvironmentThreadHook(ThreadHook):
  """Hook that clones and clears request environment on a new thread."""

  def __init__(self):
    self.cloner = request_environment.current_request.CloneRequestEnvironment()
    super(RequestEnvironmentThreadHook, self).__init__()

  def PreTarget(self):
    self.cloner()

  def PostTarget(self):
    request_environment.current_request.Clear()


def PatchStartNewThread(
    hooks, thread_module=thread, threading_module=threading):
  """Installs a start_new_thread replacement created by _MakeStartNewThread.

  Args:
    hooks: List of ThreadHook sub classes to instantiate and run before and
           after start_new_thread.
    thread_module: The thread module to override.
    threading_module: The threading module to override.

  """
  if not hooks:


    return
  thread_module.start_new_thread = _MakeStartNewThread(
      thread_module.start_new_thread, hooks)
  importlib.reload(threading_module)

  importlib.reload(multiprocessing.dummy)


def _MakeStartNewThread(base_start_new_thread, hooks):
  """Returns a replacement for start_new_thread that inherits environment.

  Returns a function with an interface that matches thread.start_new_thread
  where the new thread inherits the request environment of
  request_environment.current_request and cleans it up when it terminates.

  Args:
    base_start_new_thread: The thread.start_new_thread function to call to
        create a new thread.
    hooks: List of ThreadHook sub classes to instantiate and run before and
           after start_new_thread.

  Returns:
      A replacement for start_new_thread.
  """

  def StartNewThread(target, args, kw=None):
    """A replacement for thread.start_new_thread.

    A replacement for thread.start_new_thread that inherits RequestEnvironment
    state from its creator and cleans up that state when it terminates.

    Args:
      target: Target to run in the new thread.
      args:   Arguments to pass to the new thread.
      kw:     Keyword arguments to pass to the new thread.

    Returns:
      See thread.start_new_thread.
    """
    if kw is None:
      kw = {}
    hook_objs = []
    for hook_class in hooks:
      hook_objs.append(hook_class())
    def Run():
      try:
        for hook in hook_objs:
          hook.PreTarget()
        target(*args, **kw)
      finally:
        for hook in hook_objs:
          hook.PostTarget()
    ctx = contextvars.copy_context()
    return base_start_new_thread(ctx.run, (Run,))
  return StartNewThread
