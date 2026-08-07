# Copyright 2026 Google LLC
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

import datetime
import http
import os
import time
import unittest
from unittest import mock
from google.appengine.api.taskqueue import cloudtask
from google.appengine.api.taskqueue import taskqueue
from google.appengine.api.taskqueue import taskqueue_service_bytes_pb2 as taskqueue_service_pb2
from google.rpc import code_pb2


class CloudtaskTest(unittest.TestCase):

  def setUp(self):
    super(CloudtaskTest, self).setUp()
    self.mock_client = mock.Mock()
    self.mock_client.task_path.return_value = 'projects/p/locations/l/queues/q/tasks/t'

  @mock.patch.dict(os.environ, {'GAE_SERVICE': 'default-service'}, clear=False)
  @mock.patch('google.appengine.api.app_identity.get_default_version_hostname', return_value='app.appspot.com')
  def test_build_ct_task_payload_with_default_app_version_target(self, _):
    task = taskqueue.Task(url='/test', target=taskqueue.DEFAULT_APP_VERSION)
    payload = cloudtask._build_ct_task_payload(
        queue_name='default',
        task=task,
        client=self.mock_client,
        project='p',
        region='us-central1'
    )
    self.assertIn('app_engine_http_request', payload)
    self.assertEqual(
        payload['app_engine_http_request'].get('app_engine_routing', {}).get('service'),
        'default-service'
    )

  @mock.patch.dict(os.environ, {}, clear=True)
  @mock.patch('google.appengine.api.app_identity.get_default_version_hostname', return_value='app.appspot.com')
  def test_build_ct_task_payload_with_string_target(self, _):
    task = taskqueue.Task(url='/test', target='worker-dot')
    payload = cloudtask._build_ct_task_payload(
        queue_name='default',
        task=task,
        client=self.mock_client,
        project='p',
        region='us-central1'
    )
    self.assertEqual(
        payload['app_engine_http_request'].get('app_engine_routing', {}).get('service'),
        'worker'
    )

  @mock.patch.dict(os.environ, {}, clear=True)
  @mock.patch('google.appengine.api.app_identity.get_default_version_hostname', return_value='app.appspot.com')
  def test_build_ct_task_payload_with_version_service_target(self, _):
    task = taskqueue.Task(url='/test', target='v2.worker')
    payload = cloudtask._build_ct_task_payload(
        queue_name='default',
        task=task,
        client=self.mock_client,
        project='p',
        region='us-central1'
    )
    routing = payload['app_engine_http_request'].get('app_engine_routing', {})
    self.assertEqual(routing.get('service'), 'worker')
    self.assertEqual(routing.get('version'), 'v2')

  def test_build_ct_task_payload_with_countdown(self):
    now = time.time()
    countdown_seconds = 60
    task = taskqueue.Task(url='/test', countdown=countdown_seconds)
    payload = cloudtask._build_ct_task_payload(
        queue_name='default',
        task=task,
        client=self.mock_client,
        project='p',
        region='us-central1'
    )
    self.assertIn('schedule_time', payload)
    st = payload['schedule_time']
    self.assertAlmostEqual(st.seconds, int(now + countdown_seconds), delta=2)

  def test_build_ct_task_payload_with_eta(self):
    eta = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=120)
    task = taskqueue.Task(url='/test', eta=eta)
    payload = cloudtask._build_ct_task_payload(
        queue_name='default',
        task=task,
        client=self.mock_client,
        project='p',
        region='us-central1'
    )
    self.assertIn('schedule_time', payload)
    st = payload['schedule_time']
    self.assertAlmostEqual(st.seconds, int(eta.timestamp()), delta=2)

  def test_get_project_id(self):
    with mock.patch.dict(os.environ, {cloudtask.ENV_GOOGLE_CLOUD_PROJECT: 's~my-app'}):
      self.assertEqual(cloudtask._get_project_id(), 'my-app')
    with mock.patch.dict(os.environ, {cloudtask.ENV_GOOGLE_CLOUD_PROJECT: 'e~my-app'}):
      self.assertEqual(cloudtask._get_project_id(), 'my-app')
    with mock.patch.dict(os.environ, {cloudtask.ENV_GOOGLE_CLOUD_PROJECT: 'my-app'}):
      self.assertEqual(cloudtask._get_project_id(), 'my-app')

  def test_is_cloudtask_push_queue_enabled(self):
    with mock.patch.dict(os.environ, {cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'true'}):
      self.assertTrue(cloudtask.is_cloudtask_push_queue_enabled())
    with mock.patch.dict(os.environ, {cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'True'}):
      self.assertTrue(cloudtask.is_cloudtask_push_queue_enabled())
    with mock.patch.dict(os.environ, {cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'false'}):
      self.assertFalse(cloudtask.is_cloudtask_push_queue_enabled())
    with mock.patch.dict(os.environ, {}, clear=True):
      self.assertFalse(cloudtask.is_cloudtask_push_queue_enabled())

  def test_map_rest_code_to_tq_code(self):
    self.assertEqual(
        cloudtask._map_rest_code_to_tq_code(code_pb2.NOT_FOUND),
        taskqueue_service_pb2.TaskQueueServiceError.UNKNOWN_TASK
    )
    self.assertEqual(
        cloudtask._map_rest_code_to_tq_code(http.HTTPStatus.NOT_FOUND),
        taskqueue_service_pb2.TaskQueueServiceError.UNKNOWN_TASK
    )
    self.assertEqual(
        cloudtask._map_rest_code_to_tq_code(code_pb2.ALREADY_EXISTS),
        taskqueue_service_pb2.TaskQueueServiceError.TASK_ALREADY_EXISTS
    )
    self.assertEqual(
        cloudtask._map_rest_code_to_tq_code(code_pb2.INVALID_ARGUMENT),
        taskqueue_service_pb2.TaskQueueServiceError.INVALID_TASK_NAME
    )
    self.assertEqual(
        cloudtask._map_rest_code_to_tq_code(code_pb2.PERMISSION_DENIED),
        taskqueue_service_pb2.TaskQueueServiceError.PERMISSION_DENIED
    )


if __name__ == '__main__':
  unittest.main()
