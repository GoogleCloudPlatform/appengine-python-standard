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

"""Unit test for the deferred module."""

import base64
import datetime
import operator
import os
import pickle

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import full_app_id
from google.appengine.api.taskqueue import taskqueue_stub
from google.appengine.ext import db
from google.appengine.ext import deferred
import six

from absl.testing import absltest




def setUpModule():


  os.environ["HTTP_HOST"] = "my-app.appspot.com"
  os.environ["DEFAULT_VERSION_HOSTNAME"] = "my-app.appspot.com"


def tearDownModule():
  del os.environ["HTTP_HOST"]
  del os.environ["DEFAULT_VERSION_HOSTNAME"]


calls = []


def SerializableFunction(a, b):
  calls.append(("SerializableFunction", a, b))
  return a + b


class SerializableClass(object):

  def __init__(self, a):
    calls.append(("SerializableClass", a))
    self.a = a

  def __call__(self, b):
    calls.append(("SerializableClass object", self.a, b))
    return self.a + b

  def Test(self, b):
    calls.append(("SerializableClass.Test", self.a, b))
    return self.a + b

  @classmethod
  def ClsTest(cls, a, b):
    calls.append(("SerializableClass.ClsTest", a, b))
    return a + b

  @staticmethod
  def DoesntWork(a, b):
    calls.append(("SerializableClass.DoesntWork", a, b))
    return a + b


class RetryCount(db.Model):
  count = db.IntegerProperty(required=True)


class SerializableRetryClass(object):

  def __init__(self):
    RetryCount(key_name="count", count=0).put()
    calls.append(("SerializableRetryClass",))

  def __call__(self, val):
    retry_count = RetryCount.get_by_key_name("count")
    if retry_count is None:
      retry_count = RetryCount(key_name="count", count=0)

    attempts = retry_count.count
    calls.append(("SerializableRetryClass object", attempts, val))
    if attempts == 0:
      retry_count.count += 1
      retry_count.put()
      raise deferred.SingularTaskFailure
    return val


def OuterFunction(a):

  def InnerFunction(b):
    return a + b

  return InnerFunction


def ClassGenerator(a):

  class Foo(object):

    def Bar(self, b):
      return a + b

  return Foo


def RecordCall(s):
  calls.append(("RecordCall", len(s)))


def ExecuteHandlerWithXSRF(task):
  """Execute the task with the correct headers to get past the XSRF protection.

  Args:
    task: A dict as returned from
      google.appengine.api.taskqueue.taskqueue_stub.QueryTasksResponseToDict

  Returns:
    The webapp.Response object.
  """
  wsgi_environ = {
      "HTTP_X_APPENGINE_TASKNAME": "taskname-goes-here",
      "SERVER_SOFTWARE": "Development/1.0: unittest",
  }
  return ExecuteHandler(task, wsgi_environ)


def ExecuteHandler(task, wsgi_environ_overrides):
  """Execute the task with the correct headers to get past the XSRF protection.

  Args:
    task: A dict as returned from
      google.appengine.api.taskqueue.taskqueue_stub.QueryTasksResponseToDict
    wsgi_environ_overrides: a dict containing keys to modify in the wsgi environ
      passed to the deferred webapp handler.

  Returns:
    response: a string containing body of the response
    status: HTTP status code of enum type http.HTTPStatus
    headers: a dict containing response headers
  """
  body = base64.b64decode(task["body"])
  body_file = six.BytesIO(body)
  wsgi_environ = {
      "wsgi.input": body_file,
      "CONTENT_LENGTH": len(body),
      "REQUEST_METHOD": "POST",
  }
  wsgi_environ.update(wsgi_environ_overrides)
  deferred_handler = deferred.Handler()
  return deferred_handler.post(wsgi_environ)


class SerializationTest(absltest.TestCase):

  def setUp(self):
    calls[:] = []

  def testFunction(self):
    deferred.run(deferred.serialize(SerializableFunction, 1, 2))
    self.assertEqual(calls, [("SerializableFunction", 1, 2)])

  def testClass(self):
    deferred.run(deferred.serialize(SerializableClass, 1))
    self.assertEqual(calls, [("SerializableClass", 1)])

  def testCallableObject(self):
    data = deferred.serialize(SerializableClass(1), 2)
    self.assertEqual(calls, [("SerializableClass", 1)])
    deferred.run(data)
    self.assertEqual(calls, [("SerializableClass", 1),
                             ("SerializableClass object", 1, 2)])

  def testInstanceMethod(self):
    data = deferred.serialize(SerializableClass(1).Test, 2)
    self.assertEqual(calls, [("SerializableClass", 1)])
    deferred.run(data)
    self.assertEqual(calls, [("SerializableClass", 1),
                             ("SerializableClass.Test", 1, 2)])

  def testClassMethod(self):
    deferred.run(deferred.serialize(SerializableClass.ClsTest, 1, 2))
    self.assertEqual(calls, [("SerializableClass.ClsTest", 1, 2)])

  def testBuiltin(self):
    self.assertEqual(deferred.run(deferred.serialize(operator.add, 1, 2)), 3)
    now = datetime.datetime.now()
    self.assertEqual(
        deferred.run(deferred.serialize(now.isoformat)), now.isoformat())

  def testStaticMethod(self):
    if six.PY2:
      self.assertRaises(pickle.PicklingError, deferred.serialize,
                        SerializableClass.DoesntWork, 1, 2)
    else:
      deferred.run(deferred.serialize(SerializableClass.DoesntWork, 1, 2))
      self.assertEqual(calls, [("SerializableClass.DoesntWork", 1, 2)])

  def testLambda(self):
    expected_error = pickle.PicklingError if six.PY2 else AttributeError
    self.assertRaises(expected_error, deferred.serialize,
                      lambda a, b: a + b, 1, 2)

  def testNestedFunction(self):
    expected_error = pickle.PicklingError if six.PY2 else AttributeError
    self.assertRaises(expected_error, deferred.serialize,
                      OuterFunction(1), 2)

  def testNestedClass(self):
    expected_error = pickle.PicklingError if six.PY2 else AttributeError
    self.assertRaises(expected_error, deferred.serialize,
                      ClassGenerator(1), 2)


class DeferredTest(absltest.TestCase):

  def setUp(self):
    calls[:] = []

    full_app_id.put("test_app")
    os.environ["USER_IS_ADMIN"] = "1"


    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    stub = datastore_file_stub.DatastoreFileStub(
        "test_app", "/dev/null", "/dev/null", require_indexes=True)
    apiproxy_stub_map.apiproxy.RegisterStub("datastore_v3", stub)


    self.task_queue = taskqueue_stub.TaskQueueServiceStub()
    apiproxy_stub_map.apiproxy.RegisterStub("taskqueue", self.task_queue)

  def testDefer(self):
    deferred.defer(SerializableClass(4), 4)
    task1 = deferred.defer(
        SerializableClass(5), 2, _name="foo", _countdown=10, _target="backend")
    tasks = self.task_queue.GetTasks("default")
    self.assertLen(tasks, 2)
    self.assertEqual(deferred.run(base64.b64decode(tasks[0]["body"])), 8)
    self.assertEqual(tasks[0]["url"], "/_ah/queue/deferred")
    self.assertEqual(deferred.run(base64.b64decode(tasks[1]["body"])), 7)
    self.assertEqual(tasks[1]["name"], "foo")
    self.assertEqual(tasks[0]["name"], "task1")
    self.assertEqual(tasks[1]["name"], task1.name)

    self.assertTrue(task1.headers["Host"].startswith("backend."))

  def testDeferHeaders(self):
    task = deferred.defer(
        SerializableClass(5), 2, _headers={"X-AppEngine-Fail-Fast": "true"})
    tasks = self.task_queue.GetTasks("default")
    self.assertLen(tasks, 1)
    self.assertEqual(deferred.run(base64.b64decode(tasks[0]["body"])), 7)
    self.assertEqual(tasks[0]["url"], "/_ah/queue/deferred")
    self.assertEqual(tasks[0]["name"], "task1")
    self.assertIn("X-AppEngine-Fail-Fast", task.headers)
    self.assertEqual("true", task.headers["X-AppEngine-Fail-Fast"])

  def testDeferHeadersOverwriting(self):
    task = deferred.defer(
        SerializableClass(5), 2, _headers={"Content-Type": "text/plain"})
    tasks = self.task_queue.GetTasks("default")
    self.assertLen(tasks, 1)
    self.assertEqual(deferred.run(base64.b64decode(tasks[0]["body"])), 7)
    self.assertEqual(tasks[0]["url"], "/_ah/queue/deferred")
    self.assertEqual(tasks[0]["name"], "task1")
    self.assertEqual("text/plain", task.headers["Content-Type"])

  def testHandler(self):
    deferred.defer(SerializableClass(4), 4)
    tasks = self.task_queue.GetTasks("default")
    self.assertLen(tasks, 1)

    response = ExecuteHandlerWithXSRF(tasks[0])

    self.assertEqual(response[1].value, 200)
    self.assertEqual(calls, [("SerializableClass", 4),
                             ("SerializableClass object", 4, 4)])

  def testHandlerWithSingularFailure(self):
    deferred.defer(SerializableRetryClass(), 4)
    tasks = self.task_queue.GetTasks("default")
    self.assertLen(tasks, 1)

    response = ExecuteHandlerWithXSRF(tasks[0])
    self.assertEqual(response[1].value, 408)
    self.assertEqual(calls, [("SerializableRetryClass",),
                             ("SerializableRetryClass object", 0, 4)])

    response = ExecuteHandlerWithXSRF(tasks[0])
    self.assertEqual(response[1].value, 200)
    self.assertEqual(calls, [("SerializableRetryClass",),
                             ("SerializableRetryClass object", 0, 4),
                             ("SerializableRetryClass object", 1, 4)])

  def testXSRFHeaderCheckInDevAppserver(self):
    deferred.defer(SerializableClass(4), 4)
    tasks = self.task_queue.GetTasks("default")
    self.assertLen(tasks, 1)

    extra_wsgi_environ = {}
    response = ExecuteHandler(tasks[0], extra_wsgi_environ)
    self.assertEqual(response[1].value, 403)
    self.assertEqual(calls, [("SerializableClass", 4)])


    extra_wsgi_environ["SERVER_SOFTWARE"] = "Development/1.0"
    response = ExecuteHandler(tasks[0], extra_wsgi_environ)
    self.assertEqual(response[1].value, 403)
    self.assertEqual(calls, [("SerializableClass", 4)])


    extra_wsgi_environ["HTTP_X_APPENGINE_TASKNAME"] = "taskname-goes-here"
    response = ExecuteHandler(tasks[0], extra_wsgi_environ)
    self.assertEqual(response[1].value, 200)
    self.assertEqual(calls, [("SerializableClass", 4),
                             ("SerializableClass object", 4, 4)])

  def testXSRFHeaderCheckInProduction(self):
    deferred.defer(SerializableClass(4), 4)
    tasks = self.task_queue.GetTasks("default")
    self.assertLen(tasks, 1)

    extra_wsgi_environ = {}
    response = ExecuteHandler(tasks[0], extra_wsgi_environ)
    self.assertEqual(response[1].value, 403)
    self.assertEqual(calls, [("SerializableClass", 4)])


    extra_wsgi_environ["SERVER_SOFTWARE"] = "Google App Engine/0.0.0"
    response = ExecuteHandler(tasks[0], extra_wsgi_environ)
    self.assertEqual(response[1].value, 403)
    self.assertEqual(calls, [("SerializableClass", 4)])


    extra_wsgi_environ["HTTP_X_APPENGINE_TASKNAME"] = "taskname-goes-here"
    response = ExecuteHandler(tasks[0], extra_wsgi_environ)
    self.assertEqual(response[1].value, 403)
    self.assertEqual(calls, [("SerializableClass", 4)])


    extra_wsgi_environ["REMOTE_ADDR"] = "192.168.0.1"
    response = ExecuteHandler(tasks[0], extra_wsgi_environ)
    self.assertEqual(response[1].value, 403)
    self.assertEqual(calls, [("SerializableClass", 4)])


    extra_wsgi_environ["REMOTE_ADDR"] = "0.1.0.2"
    response = ExecuteHandler(tasks[0], extra_wsgi_environ)
    self.assertEqual(response[1].value, 200)
    self.assertEqual(calls, [("SerializableClass", 4),
                             ("SerializableClass object", 4, 4)])

  def testOversize(self):
    deferred.defer(RecordCall, "x" * taskqueue_stub.MAX_PUSH_TASK_SIZE_BYTES)
    tasks = self.task_queue.GetTasks("default")
    self.assertLen(tasks, 1)

    obj = pickle.loads(base64.b64decode(tasks[0]["body"]))
    self.assertIsInstance(obj, tuple)
    self.assertEqual(obj[0], deferred.run_from_datastore)
    key = obj[1][0]
    self.assertIsInstance(key, str)
    entity = deferred.deferred._DeferredTaskEntity.get(key)
    self.assertNotEqual(entity, None)

    response = ExecuteHandlerWithXSRF(tasks[0])
    self.assertEqual(response[1].value, 200)
    self.assertEqual(calls,
                     [("RecordCall", taskqueue_stub.MAX_PUSH_TASK_SIZE_BYTES)])

    self.assertEqual(deferred.deferred._DeferredTaskEntity.get(key), None)


if __name__ == "__main__":
  absltest.main()
