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

import base64
import datetime
import http
import json
import os
import sys
import time
import unittest
from unittest import mock

import pytest

if sys.version_info < (3, 10):
  # google-cloud-tasks>=2.25.0 is only installed on Python 3.10+.
  pytest.skip('Cloud Tasks push queues require Python 3.10+',
              allow_module_level=True)

from google.api_core import exceptions as google_exceptions
from google.api_core import operation
from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.api import namespace_manager
from google.appengine.api.taskqueue import cloudtask
from google.appengine.api.taskqueue import cloudtask_transactional
from google.appengine.api.taskqueue import taskqueue
from google.appengine.api.taskqueue import taskqueue_service_bytes_pb2 as taskqueue_service_pb2
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.cloud import tasks_v2
from google.longrunning import operations_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from google.rpc import code_pb2
from google.rpc import status_pb2


def _make_batch_create_operation(task_names=None, failed_requests=None):
  resp_pb = tasks_v2.BatchCreateTasksResponse.pb()(
      tasks=[tasks_v2.Task.pb()(name=n) for n in (task_names or [])]
  )
  meta_pb = tasks_v2.BatchCreateTasksMetadata.pb()(
      failed_requests=failed_requests or {}
  )
  op_pb = operations_pb2.Operation(name='operations/batch-create-1', done=True)
  op_pb.response.Pack(resp_pb)
  op_pb.metadata.Pack(meta_pb)
  return operation.from_gapic(
      op_pb,
      mock.Mock(),
      tasks_v2.BatchCreateTasksResponse,
      metadata_type=tasks_v2.BatchCreateTasksMetadata,
  )


def _make_batch_delete_operation(failed_requests=None, op_error=None):
  meta_pb = tasks_v2.BatchDeleteTasksMetadata.pb()(
      failed_requests=failed_requests or {}
  )
  op_pb = operations_pb2.Operation(name='operations/batch-delete-1', done=True)
  if op_error is not None:
    op_pb.error.CopyFrom(op_error)
  else:
    op_pb.response.Pack(empty_pb2.Empty())
  op_pb.metadata.Pack(meta_pb)
  return operation.from_gapic(
      op_pb,
      mock.Mock(),
      empty_pb2.Empty,
      metadata_type=tasks_v2.BatchDeleteTasksMetadata,
  )


class CloudtaskTest(unittest.TestCase):

  def setUp(self):
    super(CloudtaskTest, self).setUp()
    cloudtask._reset_clients()
    self.addCleanup(cloudtask._reset_clients)
    self.mock_client = mock.Mock()
    self.mock_client.queue_path.side_effect = (
        lambda p, r, q: f'projects/{p}/locations/{r}/queues/{q}'
    )
    self.mock_client.task_path.side_effect = (
        lambda p, r, q, t: f'projects/{p}/locations/{r}/queues/{q}/tasks/{t}'
    )

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
  @mock.patch('google.appengine.api.app_identity.get_default_version_hostname', return_value='p.appspot.com')
  def test_build_ct_task_payload_with_full_hostname_target(self, _):
    task = taskqueue.Task(url='/test', target='v2-dot-worker-dot-p.uc.r.appspot.com')
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

  @mock.patch.dict(
      os.environ, {'GAE_SERVICE': 'default', 'GAE_VERSION': 'v1'}, clear=True)
  @mock.patch('google.appengine.api.app_identity.get_default_version_hostname', return_value='app.appspot.com')
  def test_build_ct_task_payload_routing_and_reserved_headers(self, _):
    def routing_for(target, **kwargs):
      task = taskqueue.Task(url='/test', target=target, **kwargs)
      req = cloudtask._build_ct_task_payload(
          'q', task, self.mock_client, 'p', 'us-central1'
      )['app_engine_http_request']
      return req, req.get('app_engine_routing', {})

    # Another service without a version uses that service's default version.
    req, routing = routing_for(
        'worker', headers={'X-Custom': '1', 'X-AppEngine-Foo': 'x'})
    self.assertEqual(routing, {'service': 'worker'})
    # Host and X-AppEngine-* cannot be set on Cloud Tasks tasks.
    self.assertEqual(req['headers'], {'X-Custom': '1'})

    # The current service keeps the version that enqueued the task.
    _, routing = routing_for('default-dot')
    self.assertEqual(routing, {'service': 'default', 'version': 'v1'})

    # Version-specific "-dot-" hostnames are split into version and service.
    _, routing = routing_for('v2-dot-worker-dot')
    self.assertEqual(routing, {'service': 'worker', 'version': 'v2'})

    # Domain-scoped project IDs in full .appspot.com targets are stripped.
    task_domain = taskqueue.Task(
        url='/test',
        target='v2-dot-worker-dot-my-app.example.com.uc.r.appspot.com',
    )
    routing_domain = cloudtask._build_ct_task_payload(
        'q', task_domain, self.mock_client, 'example.com:my-app', 'us-central1'
    )['app_engine_http_request'].get('app_engine_routing', {})
    self.assertEqual(routing_domain, {'service': 'worker', 'version': 'v2'})

    # A full .appspot.com target belonging to another project falls back to
    # current GAE_SERVICE / GAE_VERSION.
    _, routing_other = routing_for('v2-dot-worker-dot-other-proj.appspot.com')
    self.assertEqual(routing_other, {'service': 'default', 'version': 'v1'})

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

  def test_build_ct_task_payload_with_retry_options(self):
    retry_opts = taskqueue.TaskRetryOptions(
        task_retry_limit=4,
        task_age_limit=600,
        min_backoff_seconds=1.5,
        max_backoff_seconds=30,
        max_doublings=3,
    )
    task = taskqueue.Task(url='/test', retry_options=retry_opts)
    payload = cloudtask._build_ct_task_payload(
        queue_name='default',
        task=task,
        client=self.mock_client,
        project='p',
        region='us-central1',
    )
    self.assertIn('retry_config', payload)
    rc = payload['retry_config']
    self.assertEqual(rc['max_attempts'], 5)
    self.assertEqual(rc['max_retry_duration'], duration_pb2.Duration(seconds=600, nanos=0))
    self.assertEqual(rc['min_backoff'], duration_pb2.Duration(seconds=1, nanos=500000000))
    self.assertEqual(rc['max_backoff'], duration_pb2.Duration(seconds=30, nanos=0))
    self.assertEqual(rc['max_doublings'], 3)

  def test_get_project_id(self):
    with mock.patch.dict(os.environ, {cloudtask.ENV_GOOGLE_CLOUD_PROJECT: 's~my-app'}):
      self.assertEqual(cloudtask._get_project_id(), 'my-app')
    with mock.patch.dict(os.environ, {cloudtask.ENV_GOOGLE_CLOUD_PROJECT: 'e~my-app'}):
      self.assertEqual(cloudtask._get_project_id(), 'my-app')
    with mock.patch.dict(os.environ, {cloudtask.ENV_GOOGLE_CLOUD_PROJECT: 'my-app'}):
      self.assertEqual(cloudtask._get_project_id(), 'my-app')

  def test_get_region_normalization_and_metadata_caching(self):
    with mock.patch.dict(os.environ, {'LOCATION_ID': 'us-central'}, clear=True):
      self.assertEqual(cloudtask._get_region(), 'us-central1')
    with mock.patch.dict(os.environ, {'GAE_REGION': 'europe-west'}, clear=True):
      self.assertEqual(cloudtask._get_region(), 'europe-west1')
    with mock.patch.dict(os.environ, {'REGION_ID': 'asia-northeast1'}, clear=True):
      self.assertEqual(cloudtask._get_region(), 'asia-northeast1')

    cloudtask._reset_clients()
    mock_resp = mock.MagicMock()
    mock_resp.__enter__.return_value.read.return_value = (
        b'projects/123/regions/us-central'
    )
    with mock.patch.dict(os.environ, {}, clear=True):
      with mock.patch('urllib.request.urlopen', return_value=mock_resp) as m_open:
        self.assertEqual(cloudtask._get_region(), 'us-central1')
        self.assertEqual(cloudtask._get_region(), 'us-central1')
        self.assertEqual(m_open.call_count, 1)

  def test_is_cloudtask_push_queue_enabled(self):
    with mock.patch.dict(os.environ, {cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'true'}):
      self.assertTrue(cloudtask.is_cloudtask_push_queue_enabled())
    with mock.patch.dict(os.environ, {cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'True'}):
      self.assertTrue(cloudtask.is_cloudtask_push_queue_enabled())
    with mock.patch.dict(os.environ, {cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'false'}):
      self.assertFalse(cloudtask.is_cloudtask_push_queue_enabled())
    with mock.patch.dict(os.environ, {}, clear=True):
      self.assertFalse(cloudtask.is_cloudtask_push_queue_enabled())

  def test_enabled_without_cloud_tasks_library_raises(self):
    with mock.patch.object(
        cloudtask, '_CLOUD_TASKS_IMPORT_ERROR', ImportError('missing')):
      with mock.patch.dict(
          os.environ, {cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'true'}):
        with self.assertRaisesRegex(ImportError, 'Python 3.10'):
          cloudtask.is_cloudtask_push_queue_enabled()
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
        taskqueue_service_pb2.TaskQueueServiceError.INVALID_REQUEST
    )
    self.assertEqual(
        cloudtask._map_rest_code_to_tq_code(code_pb2.PERMISSION_DENIED),
        taskqueue_service_pb2.TaskQueueServiceError.PERMISSION_DENIED
    )

  @mock.patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-proj', 'LOCATION_ID': 'us-central1'})
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  def test_create_single_task_success_and_errors(self, mock_client_cls):
    mock_client_cls.return_value = self.mock_client
    self.mock_client.create_task.return_value = tasks_v2.Task(
        name='projects/my-proj/locations/us-central1/queues/default/tasks/gen-task-1'
    )

    t = taskqueue.Task(url='/worker', payload='hello')
    res = cloudtask.create_tasks_in_cloud_tasks('default', [t], multiple=False)
    self.assertIs(res, t)
    self.assertEqual(t.name, 'gen-task-1')
    self.assertEqual(t.queue_name, 'default')
    self.assertTrue(t.was_enqueued)

    # AlreadyExists -> TaskAlreadyExistsError
    self.mock_client.create_task.side_effect = google_exceptions.AlreadyExists('dup')
    with self.assertRaises(taskqueue.TaskAlreadyExistsError):
      cloudtask.create_tasks_in_cloud_tasks('default', [taskqueue.Task(url='/worker')], multiple=False)

    # AlreadyExists with ExecutorServiceError::TOMBSTONED_TASK -> TombstonedTaskError
    self.mock_client.create_task.side_effect = google_exceptions.AlreadyExists(
        'Requested entity already exists [detail: "[ORIGINAL ERROR] '
        'ExecutorError::1015: apphosting::ExecutorServiceError::TOMBSTONED_TASK"]'
    )
    with self.assertRaises(taskqueue.TombstonedTaskError):
      cloudtask.create_tasks_in_cloud_tasks('default', [taskqueue.Task(url='/worker')], multiple=False)

    # NotFound -> UnknownQueueError
    self.mock_client.create_task.side_effect = google_exceptions.NotFound('missing queue')
    with self.assertRaises(taskqueue.UnknownQueueError):
      cloudtask.create_tasks_in_cloud_tasks('missing', [taskqueue.Task(url='/worker')], multiple=False)

    # BadRequest with Queue does not exist -> UnknownQueueError
    self.mock_client.create_task.side_effect = google_exceptions.BadRequest('Queue does not exist')
    with self.assertRaises(taskqueue.UnknownQueueError):
      cloudtask.create_tasks_in_cloud_tasks('missing', [taskqueue.Task(url='/worker')], multiple=False)

  @mock.patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-proj', 'LOCATION_ID': 'us-central1'})
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  def test_create_batch_tasks_with_real_lro_operation(self, mock_client_cls):
    mock_client_cls.return_value = self.mock_client
    self.mock_client.batch_create_tasks.return_value = _make_batch_create_operation(
        task_names=[
            'projects/my-proj/locations/us-central1/queues/default/tasks/b1',
            'projects/my-proj/locations/us-central1/queues/default/tasks/b2',
        ]
    )

    t1 = taskqueue.Task(url='/worker', payload='1')
    t2 = taskqueue.Task(url='/worker', payload='2')
    res = cloudtask.create_tasks_in_cloud_tasks('default', [t1, t2], multiple=True)

    self.assertEqual(len(res), 2)
    self.assertEqual(t1.name, 'b1')
    self.assertEqual(t2.name, 'b2')
    self.assertTrue(t1.was_enqueued)
    self.assertTrue(t2.was_enqueued)
    self.mock_client.batch_create_tasks.assert_called_once()

    # Re-adding an already enqueued task raises BadTaskStateError.
    with self.assertRaises(taskqueue.BadTaskStateError):
      cloudtask.create_tasks_in_cloud_tasks('default', [t1], multiple=False)

    # Exceeding MAX_TASKS_PER_ADD (100) raises TooManyTasksError.
    many_tasks = [taskqueue.Task(url=f'/t-{i}') for i in range(101)]
    with self.assertRaises(taskqueue.TooManyTasksError):
      cloudtask.create_tasks_in_cloud_tasks(
          'default', many_tasks, multiple=True
      )
    with mock.patch.dict(
        os.environ, {cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'true'}
    ):
      with self.assertRaises(taskqueue.TooManyTasksError):
        taskqueue.Queue('default').add(many_tasks)

    # Missing task in BatchCreateTasks response raises InternalError instead of
    # silently leaving task.name as None.
    self.mock_client.batch_create_tasks.return_value = (
        _make_batch_create_operation(task_names=[])
    )
    with self.assertRaises(taskqueue.InternalError):
      cloudtask.create_tasks_in_cloud_tasks(
          'default',
          [taskqueue.Task(url='/1'), taskqueue.Task(url='/2')],
          multiple=True,
      )

    # An incomplete Operation (done=False) raises InternalError immediately
    # without polling Operations.GetOperation.
    refresh_mock = mock.Mock()
    incomplete_op = operation.Operation(
        operations_pb2.Operation(name='operations/incomplete', done=False),
        refresh=refresh_mock,
        cancel=mock.Mock(),
        result_type=tasks_v2.BatchCreateTasksResponse,
        metadata_type=tasks_v2.BatchCreateTasksMetadata,
    )
    self.mock_client.batch_create_tasks.return_value = incomplete_op
    with self.assertRaises(taskqueue.InternalError):
      cloudtask.create_tasks_in_cloud_tasks(
          'default',
          [taskqueue.Task(url='/1'), taskqueue.Task(url='/2')],
          multiple=True,
      )
    refresh_mock.assert_not_called()

  @mock.patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-proj', 'LOCATION_ID': 'us-central1'})
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  def test_create_batch_tasks_partial_failure_and_duplicate_names(self, mock_client_cls):
    mock_client_cls.return_value = self.mock_client

    # Duplicate names pre-condition check
    dup1 = taskqueue.Task(name='same-name', url='/worker')
    dup2 = taskqueue.Task(name='same-name', url='/worker')
    with self.assertRaises(taskqueue.DuplicateTaskNameError):
      cloudtask.create_tasks_in_cloud_tasks('default', [dup1, dup2], multiple=True)

    # Partial failure via LRO metadata.failed_requests (index 1 failed with ALREADY_EXISTS)
    self.mock_client.batch_create_tasks.return_value = _make_batch_create_operation(
        task_names=[
            'projects/my-proj/locations/us-central1/queues/default/tasks/ok-task',
        ],
        failed_requests={
            1: status_pb2.Status(code=code_pb2.ALREADY_EXISTS, message='Task already exists')
        },
    )
    t_ok = taskqueue.Task(name='ok-task', url='/worker')
    t_dup = taskqueue.Task(name='dup-task', url='/worker')
    with self.assertRaises(taskqueue.TaskAlreadyExistsError):
      cloudtask.create_tasks_in_cloud_tasks('default', [t_ok, t_dup], multiple=True)

    self.assertTrue(t_ok.was_enqueued)
    self.assertEqual(t_ok.name, 'ok-task')
    self.assertFalse(t_dup.was_enqueued)

    # INVALID_ARGUMENT is a generic error that keeps the server's message.
    self.mock_client.batch_create_tasks.return_value = _make_batch_create_operation(
        failed_requests={
            0: status_pb2.Status(
                code=code_pb2.INVALID_ARGUMENT, message='schedule time too far')
        },
    )
    with self.assertRaisesRegex(taskqueue.Error, 'schedule time too far') as cm:
      cloudtask.create_tasks_in_cloud_tasks(
          'default', [taskqueue.Task(url='/a'), taskqueue.Task(url='/b')],
          multiple=True)
    self.assertNotIsInstance(cm.exception, taskqueue.InvalidTaskNameError)

  @mock.patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-proj', 'LOCATION_ID': 'us-central1'})
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  def test_delete_tasks_in_cloud_tasks(self, mock_client_cls):
    mock_client_cls.return_value = self.mock_client
    self.mock_client.batch_delete_tasks.return_value = _make_batch_delete_operation()

    t1 = taskqueue.Task(name='del-1')
    t2 = taskqueue.Task(name='del-2')
    res = cloudtask.delete_tasks_in_cloud_tasks('default', [t1, t2], multiple=True)
    self.assertEqual(len(res), 2)
    self.assertTrue(t1.was_deleted)
    self.assertTrue(t2.was_deleted)

    # Already deleted task raises BadTaskStateError
    with self.assertRaises(taskqueue.BadTaskStateError):
      cloudtask.delete_tasks_in_cloud_tasks('default', [t1], multiple=False)

    # Unnamed task raises BadTaskStateError
    with self.assertRaises(taskqueue.BadTaskStateError):
      cloudtask.delete_tasks_in_cloud_tasks('default', [taskqueue.Task()], multiple=False)

    # Duplicate names raises DuplicateTaskNameError
    with self.assertRaises(taskqueue.DuplicateTaskNameError):
      cloudtask.delete_tasks_in_cloud_tasks(
          'default', [taskqueue.Task(name='d'), taskqueue.Task(name='d')], multiple=True
      )

    # Exceeding _BATCH_DELETE_TASKS_MAX_SIZE (1000) raises TooManyTasksError.
    with self.assertRaises(taskqueue.TooManyTasksError):
      cloudtask.delete_tasks_in_cloud_tasks(
          'default',
          [taskqueue.Task(name=f'del-{i}') for i in range(1001)],
          multiple=True,
      )

    # NOT_FOUND in failed_requests marks was_deleted=False without raising
    self.mock_client.batch_delete_tasks.return_value = _make_batch_delete_operation(
        failed_requests={
            0: status_pb2.Status(code=code_pb2.NOT_FOUND, message='Not found')
        }
    )
    t_missing = taskqueue.Task(name='missing-task')
    t_present = taskqueue.Task(name='present-task')
    cloudtask.delete_tasks_in_cloud_tasks('default', [t_missing, t_present], multiple=True)
    self.assertFalse(t_missing.was_deleted)
    self.assertTrue(t_present.was_deleted)

    # Non-ignored error in failed_requests raises translated exception
    self.mock_client.batch_delete_tasks.return_value = _make_batch_delete_operation(
        failed_requests={
            0: status_pb2.Status(code=code_pb2.PERMISSION_DENIED, message='Denied')
        }
    )
    with self.assertRaises(taskqueue.PermissionDeniedError):
      cloudtask.delete_tasks_in_cloud_tasks(
          'default', [taskqueue.Task(name='denied-task')], multiple=False
      )

    # Operation-level error alongside per-task NOT_FOUND in failed_requests still
    # processes failed_requests and marks NOT_FOUND tasks as was_deleted=False.
    self.mock_client.batch_delete_tasks.return_value = (
        _make_batch_delete_operation(
            failed_requests={
                0: status_pb2.Status(
                    code=code_pb2.NOT_FOUND, message='Not found'
                )
            },
            op_error=status_pb2.Status(
                code=code_pb2.NOT_FOUND, message='1 request failed'
            ),
        )
    )
    t_missing_with_op_err = taskqueue.Task(name='missing-with-op-err')
    cloudtask.delete_tasks_in_cloud_tasks(
        'default', [t_missing_with_op_err], multiple=False
    )
    self.assertFalse(t_missing_with_op_err.was_deleted)

  @mock.patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-proj', 'LOCATION_ID': 'us-central1'})
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  def test_purge_queue_in_cloud_tasks(self, mock_client_cls):
    mock_client_cls.return_value = self.mock_client
    cloudtask.purge_queue_in_cloud_tasks('my-queue')
    self.mock_client.purge_queue.assert_called_once_with(
        request={'name': 'projects/my-proj/locations/us-central1/queues/my-queue'}
    )

  @mock.patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-proj', 'LOCATION_ID': 'us-central1'})
  @mock.patch('google.cloud.tasks_v2beta3.CloudTasksClient')
  def test_fetch_queue_stats_in_cloud_tasks(self, mock_v2beta3_client_cls):
    mock_v2beta3_client = mock.Mock()
    mock_v2beta3_client.queue_path.side_effect = (
        lambda p, r, q: f'projects/{p}/locations/{r}/queues/{q}'
    )
    mock_v2beta3_client_cls.return_value = mock_v2beta3_client

    eta_dt = datetime.datetime(2026, 9, 30, 12, 0, 0, tzinfo=datetime.timezone.utc)
    mock_stats = mock.Mock(
        tasks_count=42,
        oldest_estimated_arrival_time=eta_dt,
        executed_last_minute_count=7,
        concurrent_dispatches_count=3,
        effective_execution_rate=5.0,
    )
    mock_v2beta3_client.get_queue.return_value = mock.Mock(stats=mock_stats)

    q = taskqueue.Queue('default')
    stats = cloudtask.fetch_queue_stats_in_cloud_tasks([q], multiple=False)
    self.assertIsInstance(stats, taskqueue.QueueStatistics)
    self.assertEqual(stats.tasks, 42)
    self.assertEqual(stats.oldest_eta_usec, int(eta_dt.timestamp() * 1e6))
    self.assertEqual(stats.executed_last_minute, 7)
    self.assertEqual(stats.in_flight, 3)
    self.assertEqual(stats.enforced_rate, 5.0)

    mock_v2beta3_client.get_queue.side_effect = google_exceptions.NotFound('no queue')
    with self.assertRaises(taskqueue.UnknownQueueError):
      cloudtask.fetch_queue_stats_in_cloud_tasks([q], multiple=False)

  @mock.patch.dict(
      os.environ,
      {
          'APPLICATION_ID': 's~my-proj',
          'GOOGLE_CLOUD_PROJECT': 'my-proj',
          'LOCATION_ID': 'us-central1',
      },
  )
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  @mock.patch('google.appengine.api.datastore.IsInTransaction', return_value=True)
  @mock.patch('google.appengine.api.datastore._GetConnection')
  @mock.patch('google.appengine.api.datastore.Put')
  def test_transactional_tasks_with_retry_options_and_schedule_time(
      self, mock_put, mock_get_conn, mock_in_tx, mock_client_cls
  ):
    mock_client_cls.return_value = self.mock_client
    mock_conn = mock.Mock(_BaseConnection__adapter=None,
                          _ae_pending_cloud_task_keys=None)
    mock_conn._on_commit_callbacks = []
    mock_get_conn.return_value = mock_conn

    saved_entities = []

    def fake_put(entity):
      entity._Entity__key = datastore.Key.from_path(
          cloudtask_transactional._PENDING_TASK_KIND, 1, _app='my-proj'
      )
      saved_entities.append(entity)

    mock_put.side_effect = fake_put

    retry_opts = taskqueue.TaskRetryOptions(
        task_retry_limit=3,
        task_age_limit=120,
        min_backoff_seconds=2.5,
        max_backoff_seconds=10,
        max_doublings=2,
    )
    task = taskqueue.Task(
        url='/worker/tx',
        payload=b'tx-body',
        countdown=30,
        retry_options=retry_opts,
    )

    res = cloudtask_transactional.add_transactional_tasks(
        'default', [task], multiple=False
    )
    self.assertIs(res, task)
    self.assertTrue(task.was_enqueued)
    self.assertTrue(task.name.startswith('tx-'))
    self.assertEqual(len(saved_entities), 1)
    self.assertEqual(len(mock_conn._on_commit_callbacks), 1)

    # The entity uses the kind, property names and payload form shared with
    # the Go and Java SDKs.
    entity = saved_entities[0]
    self.assertEqual(entity['queue_name'], 'default')
    self.assertEqual(entity['cloud_task_name'], task.name)
    self.assertEqual(entity['sdk_lang'], 'PYTHON')
    self.assertIsInstance(entity['cloud_task_payload'], datastore_types.Text)
    staged = json.loads(entity['cloud_task_payload'])['task']
    self.assertEqual(
        staged['name'],
        'projects/my-proj/locations/us-central1/queues/default/tasks/'
        + task.name)
    ae_req = staged['appEngineHttpRequest']
    self.assertEqual(ae_req['httpMethod'], 'POST')
    self.assertEqual(ae_req['relativeUri'], '/worker/tx')
    self.assertEqual(base64.b64decode(ae_req['body']), b'tx-body')
    self.assertIn('scheduleTime', staged)
    self.assertEqual(staged['retryConfig'], {
        'maxAttempts': 4,
        'maxRetryDuration': '120s',
        'minBackoff': '2.500s',
        'maxBackoff': '10s',
        'maxDoublings': 2,
    })

    # The staged payload is dispatched as the same task.
    dispatched = cloudtask_transactional._decode_task_payload(
        entity['cloud_task_payload'])
    cloudtask_transactional.dispatch_task_payload('default', dispatched)
    self.mock_client.create_task.assert_called_once()
    call_req = self.mock_client.create_task.call_args[1]['request']
    self.assertEqual(
        call_req['parent'], 'projects/my-proj/locations/us-central1/queues/default'
    )
    sent = call_req['task']
    self.assertEqual(sent.app_engine_http_request.body, b'tx-body')
    self.assertEqual(sent.app_engine_http_request.relative_uri, '/worker/tx')
    self.assertEqual(sent.app_engine_http_request.http_method,
                     tasks_v2.HttpMethod.POST)
    self.assertEqual(sent.retry_config.max_attempts, 4)
    self.assertEqual(sent.retry_config.max_retry_duration.total_seconds(), 120.0)
    self.assertEqual(sent.retry_config.min_backoff.total_seconds(), 2.5)
    self.assertEqual(sent.retry_config.max_backoff.total_seconds(), 10.0)
    self.assertEqual(sent.retry_config.max_doublings, 2)
    expected_eta = task.eta.timestamp()
    self.assertAlmostEqual(sent.schedule_time.timestamp(), expected_eta, 3)

  def test_to_duration_rounds_to_nanoseconds(self):
    self.assertEqual(
        cloudtask._to_duration(2.3),
        duration_pb2.Duration(seconds=2, nanos=300000000))
    self.assertEqual(
        cloudtask._to_duration(120), duration_pb2.Duration(seconds=120))
    self.assertIsNone(cloudtask._to_duration(None))

  @mock.patch.dict(os.environ, {'APPLICATION_ID': 's~my-proj'})
  def test_transactional_tasks_preconditions(self):
    # Named task in transaction raises InvalidTaskNameError
    with self.assertRaises(taskqueue.InvalidTaskNameError):
      cloudtask_transactional.add_transactional_tasks(
          'default', [taskqueue.Task(name='named-tx', url='/worker')], multiple=False
      )

    # Outside transaction raises BadTransactionStateError
    with mock.patch('google.appengine.api.datastore.IsInTransaction', return_value=False):
      with mock.patch('google.appengine.api.datastore.Put'):
        with mock.patch('google.appengine.api.datastore._GetConnection'):
          with mock.patch('google.cloud.tasks_v2.CloudTasksClient', return_value=self.mock_client):
            with self.assertRaises(taskqueue.BadTransactionStateError):
              cloudtask_transactional.add_transactional_tasks(
                  'default', [taskqueue.Task(url='/worker')], multiple=False
              )

  @mock.patch.dict(
      os.environ,
      {
          'APPLICATION_ID': 's~my-proj',
          'GOOGLE_CLOUD_PROJECT': 'my-proj',
          'LOCATION_ID': 'us-central1',
          'APPENGINE_USE_CLOUDTASK_PUSH_QUEUE': 'true',
      },
  )
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  @mock.patch('google.cloud.tasks_v2beta3.CloudTasksClient')
  def test_queue_integration_with_cloud_tasks_enabled(
      self, mock_v2beta3_cls, mock_v2_cls
  ):
    mock_v2_cls.return_value = self.mock_client
    mock_v2beta3_client = mock.Mock()
    mock_v2beta3_client.queue_path.side_effect = (
        lambda p, r, q: f'projects/{p}/locations/{r}/queues/{q}'
    )
    mock_v2beta3_cls.return_value = mock_v2beta3_client

    q = taskqueue.Queue('default')

    # Single add via Queue.add
    self.mock_client.create_task.return_value = tasks_v2.Task(
        name='projects/my-proj/locations/us-central1/queues/default/tasks/q-t1'
    )
    t1 = q.add(taskqueue.Task(url='/worker', payload=b'hello'))
    self.assertEqual(t1.name, 'q-t1')
    self.assertTrue(t1.was_enqueued)

    # Batch add via Queue.add
    self.mock_client.batch_create_tasks.return_value = (
        _make_batch_create_operation(
            task_names=[
                'projects/my-proj/locations/us-central1/queues/default/tasks/q-b1',
                'projects/my-proj/locations/us-central1/queues/default/tasks/q-b2',
            ]
        )
    )
    batch_res = q.add([
        taskqueue.Task(url='/worker', payload=b'1'),
        taskqueue.Task(url='/worker', payload=b'2'),
    ])
    self.assertEqual([t.name for t in batch_res], ['q-b1', 'q-b2'])

    # Delete tasks via Queue.delete_tasks
    self.mock_client.batch_delete_tasks.return_value = (
        _make_batch_delete_operation()
    )
    del_res = q.delete_tasks(batch_res)
    self.assertEqual([t.was_deleted for t in del_res], [True, True])

    # Purge via Queue.purge
    q.purge()
    self.mock_client.purge_queue.assert_called_once()

    # Fetch statistics via Queue.fetch_statistics
    mock_stats = mock.Mock(
        tasks_count=5,
        oldest_estimated_arrival_time=None,
        executed_last_minute_count=1,
        concurrent_dispatches_count=0,
        effective_execution_rate=10.0,
    )
    mock_v2beta3_client.get_queue.return_value = mock.Mock(stats=mock_stats)
    stats = q.fetch_statistics()
    self.assertEqual(stats.tasks, 5)

  @mock.patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-proj', 'LOCATION_ID': 'us-central1'})
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  @mock.patch('google.cloud.tasks_v2beta3.CloudTasksClient')
  def test_api_errors_are_raised_as_taskqueue_errors(
      self, mock_v2beta3_cls, mock_v2_cls
  ):
    mock_v2_cls.return_value = self.mock_client
    mock_v2beta3_cls.return_value = self.mock_client
    queue_mode_detail = (
        'The task cannot be created because the queue is not a push queue. '
        '[detail: "[ORIGINAL ERROR] ExecutorError::1006: '
        'apphosting::ExecutorServiceError::INVALID_QUEUE_MODE"]')
    cases = [
        (google_exceptions.PermissionDenied('denied'),
         taskqueue.PermissionDeniedError),
        (google_exceptions.Unauthenticated('no creds'),
         taskqueue.PermissionDeniedError),
        (google_exceptions.ServiceUnavailable('unavailable'),
         taskqueue.TransientError),
        (google_exceptions.DeadlineExceeded('deadline'),
         taskqueue.TransientError),
        (google_exceptions.Aborted('aborted'), taskqueue.TransientError),
        (google_exceptions.RetryError(
            'Timeout of 20.0s exceeded',
            google_exceptions.DeadlineExceeded('deadline')),
         taskqueue.TransientError),
        (google_exceptions.InternalServerError('internal'),
         taskqueue.InternalError),
        (google_exceptions.NotFound('Queue does not exist.'),
         taskqueue.UnknownQueueError),
        (google_exceptions.InvalidArgument(queue_mode_detail),
         taskqueue.InvalidQueueModeError),
        (google_exceptions.FailedPrecondition(
            'Queue does not exist. apphosting::ExecutorServiceError::'
            'UNKNOWN_QUEUE'), taskqueue.UnknownQueueError),
        (google_exceptions.AlreadyExists(
            'Requested entity already exists [detail: "[ORIGINAL ERROR] '
            'ExecutorError::1015: apphosting::ExecutorServiceError::'
            'TOMBSTONED_TASK"]'), taskqueue.TombstonedTaskError),
    ]
    calls = {
        'create_task': lambda: cloudtask.create_tasks_in_cloud_tasks(
            'q', [taskqueue.Task(url='/w')], multiple=False),
        'batch_create_tasks': lambda: cloudtask.create_tasks_in_cloud_tasks(
            'q', [taskqueue.Task(url='/w'), taskqueue.Task(url='/w')],
            multiple=True),
        'batch_delete_tasks': lambda: cloudtask.delete_tasks_in_cloud_tasks(
            'q', [taskqueue.Task(name='t1')], multiple=False),
        'purge_queue': lambda: cloudtask.purge_queue_in_cloud_tasks('q'),
        'get_queue': lambda: cloudtask.fetch_queue_stats_in_cloud_tasks(
            ['q'], multiple=False),
    }
    for api_error, expected in cases:
      for method, call in calls.items():
        with self.subTest(error=type(api_error).__name__, method=method):
          getattr(self.mock_client, method).side_effect = api_error
          with self.assertRaises(expected) as cm:
            call()
          self.assertIsInstance(cm.exception, taskqueue.Error)
          getattr(self.mock_client, method).side_effect = None

  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  @mock.patch('google.cloud.tasks_v2beta3.CloudTasksClient')
  def test_caller_supplied_rpc_reports_cloud_tasks_result(
      self, mock_v2beta3_cls, mock_v2_cls
  ):
    mock_v2_cls.return_value = self.mock_client
    mock_v2beta3_cls.return_value = self.mock_client
    tb = testbed.Testbed()
    tb.activate()
    self.addCleanup(tb.deactivate)
    tb.init_taskqueue_stub()
    # Patched after testbed.activate so that deactivate restores the
    # environment without the flag.
    env = mock.patch.dict(os.environ, {
        'GOOGLE_CLOUD_PROJECT': 'my-proj',
        'LOCATION_ID': 'us-central1',
        cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'true',
    })
    env.start()
    self.addCleanup(env.stop)
    self.mock_client.create_task.return_value = tasks_v2.Task(
        name='projects/my-proj/locations/us-central1/queues/default/tasks/t1')
    self.mock_client.get_queue.return_value = mock.Mock(stats=None)
    self.mock_client.batch_delete_tasks.return_value = (
        _make_batch_delete_operation())
    q = taskqueue.Queue('default')

    callbacks = []
    rpc = taskqueue.create_rpc(callback=lambda: callbacks.append('add'))
    self.assertIs(q.add_async(taskqueue.Task(url='/w'), rpc=rpc), rpc)
    self.assertEqual(rpc.get_result().name, 't1')
    rpc.wait()
    self.assertEqual(callbacks, ['add'])  # Called once, like UserRPC.

    rpc = taskqueue.create_rpc()
    self.assertIs(q.fetch_statistics_async(rpc), rpc)
    self.assertEqual(rpc.get_result().tasks, 0)

    rpc = taskqueue.create_rpc()
    self.assertIs(q.delete_tasks_async(taskqueue.Task(name='t1'), rpc=rpc),
                  rpc)
    self.assertTrue(rpc.get_result().was_deleted)

    self.mock_client.create_task.side_effect = (
        google_exceptions.PermissionDenied('denied'))
    rpc = taskqueue.create_rpc()
    q.add_async(taskqueue.Task(url='/w'), rpc=rpc)
    rpc.wait()  # Like UserRPC.wait, does not raise the call's error.
    with self.assertRaises(taskqueue.PermissionDeniedError):
      rpc.check_success()

  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  @mock.patch('google.cloud.tasks_v2beta3.CloudTasksClient')
  def test_caller_deadline_is_passed_to_cloud_tasks(
      self, mock_v2beta3_cls, mock_v2_cls
  ):
    mock_v2_cls.return_value = self.mock_client
    mock_v2beta3_cls.return_value = self.mock_client
    tb = testbed.Testbed()
    tb.activate()
    self.addCleanup(tb.deactivate)
    tb.init_taskqueue_stub()
    env = mock.patch.dict(os.environ, {
        'GOOGLE_CLOUD_PROJECT': 'my-proj',
        'LOCATION_ID': 'us-central1',
        cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'true',
    })
    env.start()
    self.addCleanup(env.stop)
    self.mock_client.create_task.return_value = tasks_v2.Task(
        name='projects/my-proj/locations/us-central1/queues/default/tasks/t1')
    self.mock_client.get_queue.return_value = mock.Mock(stats=None)
    q = taskqueue.Queue('default')

    def assert_timeout(mock_method, deadline):
      timeout = mock_method.call_args[1]['timeout']
      self.assertGreater(timeout, 0)
      self.assertLessEqual(timeout, deadline)

    q.add_async(taskqueue.Task(url='/w'),
                rpc=taskqueue.create_rpc(deadline=2.5)).get_result()
    assert_timeout(self.mock_client.create_task, 2.5)

    create_op = _make_batch_create_operation(
        task_names=[
            'projects/p/locations/l/queues/default/tasks/b1',
            'projects/p/locations/l/queues/default/tasks/b2',
        ]
    )
    self.mock_client.batch_create_tasks.return_value = create_op
    q.add_async([taskqueue.Task(url='/w'), taskqueue.Task(url='/w')],
                rpc=taskqueue.create_rpc(deadline=1.5)).get_result()
    assert_timeout(self.mock_client.batch_create_tasks, 1.5)

    self.mock_client.batch_delete_tasks.return_value = (
        _make_batch_delete_operation())
    q.delete_tasks_async(taskqueue.Task(name='t1'),
                         rpc=taskqueue.create_rpc(deadline=2)).get_result()
    assert_timeout(self.mock_client.batch_delete_tasks, 2)

    # The synchronous methods pass their deadline argument. GetQueue retries
    # are limited to the deadline too.
    q.fetch_statistics(deadline=3)
    assert_timeout(self.mock_client.get_queue, 3)
    self.assertLessEqual(
        self.mock_client.get_queue.call_args[1]['retry'].timeout, 3)
    taskqueue.QueueStatistics.fetch('default', deadline=4)
    assert_timeout(self.mock_client.get_queue, 4)

    # A caller deadline above 20s is capped so Cloud Tasks does not reject the
    # request for having a deadline more than 30s in the future.
    q.fetch_statistics(deadline=60)
    self.assertEqual(
        self.mock_client.get_queue.call_args[1]['timeout'],
        cloudtask._DEFAULT_RPC_TIMEOUT_SECONDS)

    # Without a deadline, the client's default timeout applies for non-batch
    # calls, while batch calls pass _DEFAULT_RPC_TIMEOUT_SECONDS.
    q.add(taskqueue.Task(url='/w'))
    self.assertNotIn('timeout', self.mock_client.create_task.call_args[1])
    q.add([taskqueue.Task(url='/w'), taskqueue.Task(url='/w')])
    self.assertEqual(
        self.mock_client.batch_create_tasks.call_args[1]['timeout'],
        cloudtask._DEFAULT_RPC_TIMEOUT_SECONDS)

  @mock.patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-proj', 'LOCATION_ID': 'us-central1'})
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  @mock.patch('google.cloud.tasks_v2beta3.CloudTasksClient')
  def test_clients_are_created_once_and_reused(
      self, mock_v2beta3_cls, mock_v2_cls
  ):
    mock_v2_cls.return_value = self.mock_client
    mock_v2beta3_client = mock.Mock()
    mock_v2beta3_client.queue_path.side_effect = (
        lambda p, r, q: f'projects/{p}/locations/{r}/queues/{q}'
    )
    mock_v2beta3_client.get_queue.return_value = mock.Mock(stats=None)
    mock_v2beta3_cls.return_value = mock_v2beta3_client
    self.mock_client.create_task.return_value = tasks_v2.Task(
        name='projects/my-proj/locations/us-central1/queues/default/tasks/t'
    )

    cloudtask.create_tasks_in_cloud_tasks(
        'default', [taskqueue.Task(url='/worker')], multiple=False
    )
    cloudtask.create_tasks_in_cloud_tasks(
        'default', [taskqueue.Task(url='/worker')], multiple=False
    )
    cloudtask.purge_queue_in_cloud_tasks('default')
    cloudtask.fetch_queue_stats_in_cloud_tasks(['default'], multiple=False)
    cloudtask.fetch_queue_stats_in_cloud_tasks(['default'], multiple=False)

    self.assertEqual(mock_v2_cls.call_count, 1)
    self.assertEqual(mock_v2beta3_cls.call_count, 1)


class CloudtaskTransactionalDatastoreTest(unittest.TestCase):
  """Transactional task staging and dispatch against the datastore stub."""

  def setUp(self):
    super().setUp()
    env = mock.patch.dict(os.environ, {
        'APPLICATION_ID': 's~my-proj',
        'GOOGLE_CLOUD_PROJECT': 'my-proj',
        'LOCATION_ID': 'us-central1',
    })
    env.start()
    self.addCleanup(env.stop)
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.addCleanup(self.testbed.deactivate)
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    cloudtask._reset_clients()
    self.addCleanup(cloudtask._reset_clients)
    self.mock_client = mock.Mock()
    self.mock_client.queue_path.side_effect = (
        lambda p, r, q: f'projects/{p}/locations/{r}/queues/{q}'
    )
    self.mock_client.task_path.side_effect = (
        lambda p, r, q, t: f'projects/{p}/locations/{r}/queues/{q}/tasks/{t}'
    )
    client_patch = mock.patch(
        'google.cloud.tasks_v2.CloudTasksClient', return_value=self.mock_client)
    client_patch.start()
    self.addCleanup(client_patch.stop)

  def _pending_entities(self):
    return list(
        datastore.Query(cloudtask_transactional._PENDING_TASK_KIND).Run())

  def _put_pending(self, **props):
    entity = datastore.Entity(cloudtask_transactional._PENDING_TASK_KIND)
    entity['queue_name'] = 'default'
    entity['cloud_task_name'] = 'tx-1'
    entity['cloud_task_payload'] = datastore_types.Text(json.dumps(
        {'task': {'appEngineHttpRequest': {'relativeUri': '/w'}}}))
    entity['status'] = cloudtask_transactional._TX_TASK_STATUS_PENDING
    entity['created'] = datetime.datetime.utcnow()
    entity['retry_count'] = 0
    entity.update(props)
    datastore.Put(entity)
    return entity.key()

  def test_sweep_dispatches_tasks_staged_by_other_sdks(self):
    # Staged entities are shared with the Go and Java SDKs, so the sweeper
    # dispatches tasks they staged, and tasks staged by the preview release.
    queue = 'projects/my-proj/locations/us-central1/queues/default'
    old = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    # As written by the Go SDK.
    go_payload = (
        '{"task":{"name":"' + queue + '/tasks/tx-go","appEngineHttpRequest":'
        '{"httpMethod":"POST","appEngineRouting":{"service":"worker",'
        '"version":"v2"},"relativeUri":"/go","headers":{"X-Custom":"g"},'
        '"body":"Z28tYm9keQ=="},"scheduleTime":"2026-10-07T20:00:00.250Z",'
        '"retryConfig":{"maxAttempts":2,"minBackoff":"1.500s"}}}')
    self._put_pending(
        cloud_task_name='tx-go', created=old, sdk_lang='GO',
        cloud_task_payload=go_payload, lock_expires=None)
    # As written by the Java SDK, which stores payloads of up to 1500 bytes
    # as indexed strings. fieldAddedLater stands for a Task field that is
    # newer than the installed google-cloud-tasks.
    java_payload = (
        '{"task":{"name":"' + queue + '/tasks/tx-java","appEngineHttpRequest":'
        '{"appEngineRouting":{"service":"worker"},"httpMethod":"DELETE",'
        '"relativeUri":"/java","headers":{}},"scheduleTime":'
        '"2026-10-07T20:00:00Z","fieldAddedLater":1}}')
    self._put_pending(
        cloud_task_name='tx-java', created=old, sdk_lang='JAVA',
        cloud_task_payload=java_payload, lock_expires=None, last_error='',
        handled_by_sweeper=False)
    # As written by the preview release of this SDK.
    preview = datastore.Entity(cloudtask_transactional._PENDING_TASK_KIND)
    preview['task_name'] = 'tx-preview'
    preview['queue_name'] = 'default'
    preview['payload'] = datastore_types.Text(json.dumps({
        'name': queue + '/tasks/tx-preview',
        'app_engine_http_request': {
            'relative_uri': '/preview',
            'body': base64.b64encode(b'preview-body').decode('utf-8'),
        },
        'schedule_time': {'seconds': 1791403200, 'nanos': 0},
    }))
    preview['status'] = cloudtask_transactional._TX_TASK_STATUS_PENDING
    preview['created'] = old
    preview['retry_count'] = 0
    datastore.Put(preview)

    cloudtask_transactional.sweep()

    sent = {}
    for call in self.mock_client.create_task.call_args_list:
      task = call[1]['request']['task']
      sent[task.app_engine_http_request.relative_uri] = task
    self.assertEqual(sorted(sent), ['/go', '/java', '/preview'])
    go_task = sent['/go']
    self.assertEqual(go_task.name, queue + '/tasks/tx-go')
    self.assertEqual(go_task.app_engine_http_request.body, b'go-body')
    self.assertEqual(go_task.app_engine_http_request.headers['X-Custom'], 'g')
    self.assertEqual(
        go_task.app_engine_http_request.app_engine_routing.version, 'v2')
    self.assertEqual(go_task.retry_config.min_backoff.total_seconds(), 1.5)
    self.assertEqual(go_task.schedule_time.timestamp(), 1791403200.25)
    self.assertEqual(sent['/java'].app_engine_http_request.http_method,
                     tasks_v2.HttpMethod.DELETE)
    self.assertEqual(sent['/preview'].app_engine_http_request.body,
                     b'preview-body')
    self.assertEqual(sent['/preview'].schedule_time.timestamp(), 1791403200)
    self.assertEqual(self._pending_entities(), [])

  def test_large_payload_is_staged_and_dispatched_after_commit(self):
    body = b'x' * 5000  # Larger than the 1500-byte indexed string limit.

    def txn():
      cloudtask_transactional.add_transactional_tasks(
          'default', [taskqueue.Task(url='/w', payload=body)], multiple=False)

    datastore.RunInTransaction(txn)

    self.mock_client.create_task.assert_called_once()
    sent = self.mock_client.create_task.call_args[1]['request']['task']
    self.assertEqual(sent.app_engine_http_request.body, body)
    self.assertEqual(self._pending_entities(), [])

  def test_rolled_back_db_transaction_stages_nothing(self):

    def txn():
      cloudtask_transactional.add_transactional_tasks(
          'default', [taskqueue.Task(url='/w')], multiple=False)
      raise datastore_errors.Rollback()

    datastore.RunInTransaction(txn)

    self.mock_client.create_task.assert_not_called()
    self.assertEqual(self._pending_entities(), [])

  def test_ndb_transaction_dispatches_after_commit(self):

    @ndb.transactional
    def txn():
      with mock.patch.dict(
          os.environ, {cloudtask.ENV_USE_CLOUDTASK_PUSH_QUEUE: 'true'}):
        taskqueue.add(url='/w', transactional=True)
      self.mock_client.create_task.assert_not_called()

    txn()

    self.mock_client.create_task.assert_called_once()
    self.assertEqual(self._pending_entities(), [])

  def test_rolled_back_ndb_transaction_stages_nothing(self):

    @ndb.transactional
    def txn():
      cloudtask_transactional.add_transactional_tasks(
          'default', [taskqueue.Task(url='/w')], multiple=False)
      raise ndb.Rollback()

    txn()

    self.mock_client.create_task.assert_not_called()
    self.assertEqual(self._pending_entities(), [])

  def test_dispatch_skips_locked_and_deleted_entities(self):
    locked_until = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    key = self._put_pending(
        status=cloudtask_transactional._TX_TASK_STATUS_PROCESSING,
        lock_expires=locked_until)
    cloudtask_transactional._dispatch_pending_keys_now([key])
    self.mock_client.create_task.assert_not_called()

    datastore.Delete(key)
    cloudtask_transactional._dispatch_pending_keys_now([key])
    self.mock_client.create_task.assert_not_called()
    self.assertEqual(self._pending_entities(), [])

  def test_failed_dispatch_does_not_recreate_entity_deleted_meanwhile(self):
    key = self._put_pending()

    def create_task(request):
      del request
      datastore.Delete(key)  # Another dispatcher finished this task.
      raise google_exceptions.ServiceUnavailable('try again')

    self.mock_client.create_task.side_effect = create_task
    cloudtask_transactional._dispatch_pending_keys_now([key])
    self.assertEqual(self._pending_entities(), [])

  def test_failed_dispatch_is_retried_then_marked_failed(self):
    key = self._put_pending()
    self.mock_client.create_task.side_effect = (
        google_exceptions.ServiceUnavailable('down'))
    for _ in range(cloudtask_transactional._SWEEPER_MAX_RETRIES):
      cloudtask_transactional._dispatch_pending_keys_now([key])
    entity = datastore.Get(key)
    self.assertEqual(
        entity['status'], cloudtask_transactional._TX_TASK_STATUS_FAILED)
    self.assertIsNotNone(entity['failed_at'])

  def test_sweep_deletes_failed_entities_after_retention(self):
    now = datetime.datetime.utcnow()
    failed = cloudtask_transactional._TX_TASK_STATUS_FAILED
    old = self._put_pending(
        status=failed, failed_at=now - datetime.timedelta(days=8))
    recent = self._put_pending(
        status=failed, failed_at=now - datetime.timedelta(days=1))

    cloudtask_transactional.sweep()

    remaining = [e.key() for e in self._pending_entities()]
    self.assertEqual(remaining, [recent])
    self.assertNotIn(old, remaining)
    self.mock_client.create_task.assert_not_called()


  def test_xg_transaction_with_entity_and_task_dispatches_after_commit(self):
    # Staged tasks are root entities, so a transaction that also writes an
    # application entity must be cross-group, as documented.

    def db_txn():
      datastore.Put(datastore.Entity('Order'))
      cloudtask_transactional.add_transactional_tasks(
          'default', [taskqueue.Task(url='/w')], multiple=False)

    datastore.RunInTransactionOptions(
        datastore.CreateTransactionOptions(xg=True), db_txn)

    class Order(ndb.Model):
      pass

    @ndb.transactional(xg=True)
    def ndb_txn():
      Order().put()
      cloudtask_transactional.add_transactional_tasks(
          'default', [taskqueue.Task(url='/w')], multiple=False)

    ndb_txn()

    self.assertEqual(self.mock_client.create_task.call_count, 2)
    self.assertEqual(self._pending_entities(), [])
    self.assertEqual(len(list(datastore.Query('Order').Run())), 2)

    def non_xg_txn():
      datastore.Put(datastore.Entity('Order'))
      cloudtask_transactional.add_transactional_tasks(
          'default', [taskqueue.Task(url='/w')], multiple=False)

    with self.assertRaises(datastore_errors.BadRequestError):
      datastore.RunInTransaction(non_xg_txn)
    self.assertEqual(self.mock_client.create_task.call_count, 2)

  def test_more_than_five_tasks_in_a_transaction_are_rejected(self):
    max_tasks = cloudtask_transactional._MAX_TASKS_PER_TRANSACTION

    def add(count):
      cloudtask_transactional.add_transactional_tasks(
          'default', [taskqueue.Task(url='/w') for _ in range(count)],
          multiple=True)

    # Each staged task is its own entity group, so these transactions are XG.
    xg = datastore.CreateTransactionOptions(xg=True)

    # The limit applies across calls in one transaction, like legacy.
    def db_txn():
      add(3)
      add(3)

    @ndb.transactional(xg=True)
    def ndb_txn():
      add(max_tasks + 1)

    for txn in (lambda: datastore.RunInTransactionOptions(xg, db_txn),
                ndb_txn):
      with self.assertRaises(taskqueue.DatastoreError) as cm:
        txn()
      self.assertIsInstance(cm.exception, datastore_errors.BadRequestError)
    self.mock_client.create_task.assert_not_called()
    self.assertEqual(self._pending_entities(), [])

    def five_calls():
      for _ in range(max_tasks):
        add(1)

    datastore.RunInTransactionOptions(xg, five_calls)
    self.assertEqual(self.mock_client.create_task.call_count, max_tasks)
    self.assertEqual(self._pending_entities(), [])

  @mock.patch.object(cloudtask_transactional, '_SWEEPER_BATCH_SIZE', 2)
  def test_sweep_reads_a_bounded_batch_of_each_status(self):
    now = datetime.datetime.utcnow()
    old = now - datetime.timedelta(minutes=5)
    failed = cloudtask_transactional._TX_TASK_STATUS_FAILED
    pending = cloudtask_transactional._TX_TASK_STATUS_PENDING
    # Failed entities kept for inspection must not crowd out pending ones.
    for _ in range(3):
      self._put_pending(status=failed, failed_at=now)
    for _ in range(3):
      self._put_pending(created=old)

    cloudtask_transactional.sweep()

    self.assertEqual(self.mock_client.create_task.call_count, 2)
    statuses = sorted(e['status'] for e in self._pending_entities())
    self.assertEqual(statuses, [failed] * 3 + [pending])

    cloudtask_transactional.sweep()  # The next run takes the rest.

    self.assertEqual(self.mock_client.create_task.call_count, 3)
    statuses = [e['status'] for e in self._pending_entities()]
    self.assertEqual(statuses, [failed] * 3)

  def test_transactional_tasks_under_non_default_namespace_use_empty_namespace(
      self,
  ):
    old = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    namespace_manager.set_namespace('tenant-a')
    self.addCleanup(lambda: namespace_manager.set_namespace(''))

    # Simulate a transaction whose post-commit hook failed so the sweeper must
    # find the staged entity from the default ('') namespace.
    with mock.patch.object(
        cloudtask_transactional, '_dispatch_pending_keys_now'
    ):
      datastore.RunInTransaction(
          lambda: cloudtask_transactional.add_transactional_tasks(
              'default', [taskqueue.Task(url='/w')], multiple=False
          )
      )

    # Even while 'tenant-a' is active, the staged entity is stored in the ''
    # namespace and visible when querying namespace=''.
    staged = list(
        datastore.Query(
            cloudtask_transactional._PENDING_TASK_KIND, namespace=''
        ).Run()
    )
    self.assertEqual(len(staged), 1)
    self.assertEqual(staged[0].namespace(), '')
    staged[0]['created'] = old
    datastore.Put(staged[0])

    # Sweeper invoked under default namespace ('') or another namespace still
    # finds and dispatches the entity.
    namespace_manager.set_namespace('')
    cloudtask_transactional.sweep()
    self.mock_client.create_task.assert_called_once()
    self.assertEqual(self._pending_entities(), [])


if __name__ == '__main__':
  unittest.main()
