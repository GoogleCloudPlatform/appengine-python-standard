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
import json
import os
import time
import unittest
from unittest import mock

from google.api_core import exceptions as google_exceptions
from google.api_core import operation
from google.appengine.api import datastore
from google.appengine.api.taskqueue import cloudtask
from google.appengine.api.taskqueue import cloudtask_transactional
from google.appengine.api.taskqueue import taskqueue
from google.appengine.api.taskqueue import taskqueue_service_bytes_pb2 as taskqueue_service_pb2
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


def _make_batch_delete_operation(failed_requests=None):
  meta_pb = tasks_v2.BatchDeleteTasksMetadata.pb()(
      failed_requests=failed_requests or {}
  )
  op_pb = operations_pb2.Operation(name='operations/batch-delete-1', done=True)
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

  @mock.patch.dict(os.environ, {'GOOGLE_CLOUD_PROJECT': 'my-proj', 'LOCATION_ID': 'us-central1'})
  @mock.patch('google.cloud.tasks_v2.CloudTasksClient')
  def test_async_lro_waits_for_result_before_reading_metadata(self, mock_client_cls):
    mock_client_cls.return_value = self.mock_client

    # Simulate an async LRO where metadata is only populated after op.result() completes
    class _AsyncCreateOp:
      def __init__(self):
        self.metadata = None

      def result(self):
        self.metadata = tasks_v2.BatchCreateTasksMetadata(
            failed_requests={
                1: status_pb2.Status(code=code_pb2.ALREADY_EXISTS, message='Duplicate')
            }
        )
        return tasks_v2.BatchCreateTasksResponse(
            tasks=[
                tasks_v2.Task(
                    name='projects/my-proj/locations/us-central1/queues/default/tasks/async-ok'
                )
            ]
        )

    self.mock_client.batch_create_tasks.return_value = _AsyncCreateOp()
    t1 = taskqueue.Task(name='async-ok', url='/worker')
    t2 = taskqueue.Task(name='async-dup', url='/worker')
    with self.assertRaises(taskqueue.TaskAlreadyExistsError):
      cloudtask.create_tasks_in_cloud_tasks('default', [t1, t2], multiple=True)
    self.assertTrue(t1.was_enqueued)
    self.assertFalse(t2.was_enqueued)

    # Simulate an async LRO for batch_delete_tasks where metadata is populated after op.result()
    class _AsyncDeleteOp:
      def __init__(self):
        self.metadata = None
        self.result_called = False

      def result(self):
        self.result_called = True
        self.metadata = tasks_v2.BatchDeleteTasksMetadata(
            failed_requests={
                0: status_pb2.Status(code=code_pb2.NOT_FOUND, message='Missing')
            }
        )
        return empty_pb2.Empty()

    delete_op = _AsyncDeleteOp()
    self.mock_client.batch_delete_tasks.return_value = delete_op
    td1 = taskqueue.Task(name='missing-del')
    td2 = taskqueue.Task(name='ok-del')
    cloudtask.delete_tasks_in_cloud_tasks('default', [td1, td2], multiple=True)
    self.assertTrue(delete_op.result_called)
    self.assertFalse(td1.was_deleted)
    self.assertTrue(td2.was_deleted)

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
    mock_conn = mock.Mock(_BaseConnection__adapter=None)
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

    # Verify JSON payload in Datastore entity is valid JSON and contains serialized retry_config
    stored_payload = json.loads(saved_entities[0]['payload'])
    self.assertEqual(stored_payload['retry_config']['max_attempts'], 4)
    self.assertEqual(
        stored_payload['retry_config']['max_retry_duration'],
        {'seconds': 120, 'nanos': 0},
    )
    self.assertEqual(
        stored_payload['retry_config']['min_backoff'],
        {'seconds': 2, 'nanos': 500000000},
    )
    self.assertEqual(
        stored_payload['retry_config']['max_backoff'],
        {'seconds': 10, 'nanos': 0},
    )
    self.assertEqual(stored_payload['retry_config']['max_doublings'], 2)

    # Now test dispatch_task_payload reconstructs Duration and Timestamp objects for GAPIC
    cloudtask_transactional.dispatch_task_payload('default', stored_payload)
    self.mock_client.create_task.assert_called_once()
    call_req = self.mock_client.create_task.call_args[1]['request']
    self.assertEqual(
        call_req['parent'], 'projects/my-proj/locations/us-central1/queues/default'
    )
    dispatched_task = call_req['task']
    self.assertEqual(dispatched_task['app_engine_http_request']['body'], b'tx-body')
    self.assertIsInstance(dispatched_task['schedule_time'], Timestamp)
    dispatched_rc = dispatched_task['retry_config']
    self.assertEqual(
        dispatched_rc['max_retry_duration'],
        duration_pb2.Duration(seconds=120, nanos=0),
    )
    self.assertEqual(
        dispatched_rc['min_backoff'],
        duration_pb2.Duration(seconds=2, nanos=500000000),
    )
    self.assertEqual(
        dispatched_rc['max_backoff'],
        duration_pb2.Duration(seconds=10, nanos=0),
    )

    # Verify constructible as a real tasks_v2.CreateTaskRequest protobuf message
    proto_req = tasks_v2.CreateTaskRequest(call_req)
    self.assertEqual(proto_req.task.retry_config.max_attempts, 4)
    self.assertEqual(
        proto_req.task.retry_config.max_retry_duration.total_seconds(), 120.0
    )
    self.assertEqual(
        proto_req.task.retry_config.min_backoff.total_seconds(), 2.5
    )
    self.assertEqual(
        proto_req.task.retry_config.max_backoff.total_seconds(), 10.0
    )

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


if __name__ == '__main__':
  unittest.main()
