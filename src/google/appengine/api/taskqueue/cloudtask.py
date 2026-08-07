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

"""Cloud Tasks backend integration for Taskqueue SDK."""

import base64
from concurrent import futures
import datetime
import http
import json
import os
import urllib.error
import urllib.request
from google.api_core import exceptions as google_exceptions
from google.appengine.api import app_identity
from google.appengine.api.taskqueue import taskqueue
from google.appengine.api.taskqueue import taskqueue_service_bytes_pb2 as taskqueue_service_pb2
from google.cloud import tasks_v2beta3
from google.protobuf import duration_pb2
from google.protobuf import field_mask_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from google.rpc import code_pb2

# Environment variable constants
ENV_USE_CLOUDTASK_PUSH_QUEUE = 'APPENGINE_USE_CLOUDTASK_PUSH_QUEUE'
ENV_LOCATION_ID = 'LOCATION_ID'
ENV_GAE_LOCATION = 'GAE_LOCATION'
ENV_GAE_REGION = 'GAE_REGION'
ENV_LOCAL_GCP_REGION = 'LOCAL_GCP_REGION'
ENV_GOOGLE_CLOUD_PROJECT = 'GOOGLE_CLOUD_PROJECT'
ENV_GAE_SERVICE = 'GAE_SERVICE'
ENV_GAE_VERSION = 'GAE_VERSION'

# Sizing & concurrency constants
_MAX_CONCURRENT_API_CALLS = 100
_BATCH_CREATE_TASKS_MAX_SIZE = 100
_BATCH_DELETE_TASKS_MAX_SIZE = 1000
_METADATA_SERVER_TIMEOUT_SECONDS = 2

_THREAD_POOL = futures.ThreadPoolExecutor(_MAX_CONCURRENT_API_CALLS)


# ==============================================================================
# Public APIs
# ==============================================================================


def is_cloudtask_push_queue_enabled():
  """Checks if Cloud Tasks backend is enabled for Push Queues."""
  return str(os.environ.get(ENV_USE_CLOUDTASK_PUSH_QUEUE, '')).lower() == 'true'


def create_tasks_in_cloud_tasks(queue_name, tasks, multiple):
  """Creates one or more tasks using Cloud Tasks API (supporting BatchCreateTasks)."""
  if len(tasks) == 1:
    return _create_single_task_in_cloud_tasks(queue_name, tasks[0], multiple)
  else:
    return _create_batch_tasks_in_cloud_tasks(queue_name, tasks, multiple)


def delete_tasks_in_cloud_tasks(queue_name, tasks, multiple):
  """Deletes tasks from a queue using Cloud Tasks Client SDK (supporting BatchDeleteTasks)."""
  client = tasks_v2beta3.CloudTasksClient()
  project = _get_project_id()
  region = _get_region()

  parent = client.queue_path(project, region, queue_name)

  # Check pre-conditions (duplicate names or already deleted)
  task_names_set = set()
  for task in tasks:
    if not task.name:
      raise taskqueue.BadTaskStateError('A task name must be specified for a task')
    if task.was_deleted:
      raise taskqueue.BadTaskStateError(
          'The task %s has already been deleted' % task.name
      )
    if task.name in task_names_set:
      raise taskqueue.DuplicateTaskNameError(
          'The task name %s is duplicated' % task.name
      )
    task_names_set.add(task.name)

  for i in range(0, len(tasks), _BATCH_DELETE_TASKS_MAX_SIZE):
    batch = tasks[i : i + _BATCH_DELETE_TASKS_MAX_SIZE]
    task_names = [
        client.task_path(project, region, queue_name, t.name) for t in batch
    ]

    try:
      op = client.batch_delete_tasks(
          request={'parent': parent, 'names': task_names}
      )
      metadata = getattr(op, 'metadata', {})
      failed_requests = getattr(metadata, 'failed_requests', getattr(metadata, 'failedRequests', {}))

      exception = None
      for idx, t in enumerate(batch):
        error_status = failed_requests.get(idx) or failed_requests.get(str(idx))
        if error_status:
          code = getattr(error_status, 'code', None)
          tq_code = _map_rest_code_to_tq_code(code)
          if tq_code in [taskqueue_service_pb2.TaskQueueServiceError.UNKNOWN_TASK, taskqueue_service_pb2.TaskQueueServiceError.TOMBSTONED_TASK]:
            t._Task__deleted = False
          elif exception is None:
            exception = taskqueue._TranslateError(tq_code)
        else:
          t._Task__deleted = True

      if exception is not None:
        raise exception
    except Exception as e:
      raise e

  if multiple:
    return tasks
  else:
    return tasks[0]


def purge_queue_in_cloud_tasks(queue_name):
  """Purges all tasks in a queue using Cloud Tasks API."""
  client = tasks_v2beta3.CloudTasksClient()
  project = _get_project_id()
  region = _get_region()

  name = client.queue_path(project, region, queue_name)
  try:
    client.purge_queue(request={'name': name})
    print(
        f"Jetski: Successfully purged queue {queue_name} using Cloud Tasks",
        flush=True,
    )
  except Exception as e:
    raise e


def fetch_queue_stats_in_cloud_tasks(queues, multiple):
  """Fetches queue statistics for given queues using Cloud Tasks API."""
  client = tasks_v2beta3.CloudTasksClient()
  project = _get_project_id()
  region = _get_region()

  queue_stats_list = []
  read_mask = field_mask_pb2.FieldMask(paths=['stats'])

  for queue in queues:
    queue_name = queue.name if hasattr(queue, 'name') else str(queue)
    name = client.queue_path(project, region, queue_name)
    try:
      q_resp = client.get_queue(request={'name': name, 'read_mask': read_mask})
      ct_stats = getattr(q_resp, 'stats', None)

      tasks = getattr(ct_stats, 'tasks_count', 0) if ct_stats else 0
      oldest_eta_usec = None
      if ct_stats and getattr(ct_stats, 'oldest_estimated_arrival_time', None):
        oldest_eta = ct_stats.oldest_estimated_arrival_time
        oldest_eta_usec = int(oldest_eta.timestamp() * 1e6)

      executed_last_minute = getattr(ct_stats, 'executed_last_minute_count', 0) if ct_stats else 0
      in_flight = getattr(ct_stats, 'concurrent_dispatches_count', 0) if ct_stats else 0
      enforced_rate = getattr(ct_stats, 'effective_execution_rate', 0.0) if ct_stats else 0.0

      qs = taskqueue.QueueStatistics(
          queue=queue,
          tasks=tasks,
          oldest_eta_usec=oldest_eta_usec,
          executed_last_minute=executed_last_minute,
          in_flight=in_flight,
          enforced_rate=enforced_rate,
      )
      queue_stats_list.append(qs)
    except google_exceptions.NotFound as e:
      raise taskqueue.UnknownQueueError(f'Queue {queue_name} not found: {e}')
    except Exception as e:
      raise e

  if multiple:
    return queue_stats_list
  else:
    return queue_stats_list[0] if queue_stats_list else None


# ==============================================================================
# Private Helpers
# ==============================================================================


class _CloudTaskRPC(object):
  """RPC object wrapping asynchronous execution via ThreadPoolExecutor.

  Matches the async model of apiproxy_rpc.py using a ThreadPoolExecutor.
  Calls are scheduled onto background threads asynchronously, allowing
  operations to run concurrently until .get_result() or .wait() is called.
  """

  def __init__(self, future_or_callable):
    if callable(future_or_callable):
      self._future = _THREAD_POOL.submit(future_or_callable)
    else:
      self._future = future_or_callable

  def get_result(self):
    return self._future.result()

  def wait(self):
    self._future.result()

  def check_success(self):
    self._future.result()

  @property
  def future(self):
    return self._future


def _get_project_id():
  """Extracts and formats the Google Cloud project ID."""
  project = os.environ.get(ENV_GOOGLE_CLOUD_PROJECT)
  if project and (project.startswith('s~') or project.startswith('e~')):
    project = project[2:]
  return project


def _get_region():
  """Determines the App Engine region."""
  region = (
      os.environ.get(ENV_LOCATION_ID)
      or os.environ.get(ENV_GAE_LOCATION)
      or os.environ.get(ENV_GAE_REGION)
  )
  if region:
    return region

  try:
    req = urllib.request.Request(
        'http://metadata.google.internal/computeMetadata/v1/instance/region',
        headers={'Metadata-Flavor': 'Google'},
    )
    with urllib.request.urlopen(req, timeout=_METADATA_SERVER_TIMEOUT_SECONDS) as response:
      region_path = response.read().decode('utf-8')
      return region_path.split('/')[-1]
  except Exception:
    pass

  # Fallback to us-central1 if we can't detect it
  return os.environ.get(ENV_LOCAL_GCP_REGION, 'us-central1')


def _to_duration(seconds):
  if seconds is None:
    return None
  duration = duration_pb2.Duration()
  duration.seconds = int(seconds)
  duration.nanos = int((seconds - duration.seconds) * 1e9)
  return duration


def _build_retry_config(retry_options):
  if not retry_options:
    return None

  config = {}

  if retry_options.task_retry_limit is not None:
    config['max_attempts'] = retry_options.task_retry_limit + 1
  if retry_options.task_age_limit is not None:
    config['max_retry_duration'] = _to_duration(retry_options.task_age_limit)
  if retry_options.min_backoff_seconds is not None:
    config['min_backoff'] = _to_duration(retry_options.min_backoff_seconds)
  if retry_options.max_backoff_seconds is not None:
    config['max_backoff'] = _to_duration(retry_options.max_backoff_seconds)
  if retry_options.max_doublings is not None:
    config['max_doublings'] = retry_options.max_doublings

  if config:
    return config
  return None


def _build_ct_task_payload(queue_name, task, client, project, region):
  """Builds the Cloud Tasks Task proto payload from GAE Task."""
  headers = {}
  if task.headers:
    headers = dict(task.headers)

  headers['X-AppEngine-QueueName'] = queue_name
  if task.name:
    headers['X-AppEngine-TaskName'] = task.name

  body = b''
  if task.payload:
    if isinstance(task.payload, str):
      body = task.payload.encode('utf-8')
    else:
      body = task.payload

  http_method = tasks_v2beta3.HttpMethod.POST
  if task.method:
    method_map = {
        'POST': tasks_v2beta3.HttpMethod.POST,
        'GET': tasks_v2beta3.HttpMethod.GET,
        'PUT': tasks_v2beta3.HttpMethod.PUT,
        'DELETE': tasks_v2beta3.HttpMethod.DELETE,
        'HEAD': tasks_v2beta3.HttpMethod.HEAD,
    }
    http_method = method_map.get(task.method, tasks_v2beta3.HttpMethod.POST)

  app_engine_http_request = {
      'http_method': http_method,
      'relative_uri': task.url or '/',
      'body': body,
      'headers': headers,
  }

  routing = {}
  if isinstance(task.target, str) and task.target:
    target_str = task.target
    if target_str.endswith('-dot'):
      target_str = target_str[:-4]
    target_components = target_str.rsplit('.', 3)
    target_service = target_components[-1]
    target_version = len(target_components) > 1 and target_components[-2] or None
    target_instance = len(target_components) > 2 and target_components[-3] or None

    if target_service:
      routing['service'] = target_service
    if target_version:
      routing['version'] = target_version
    elif os.environ.get(ENV_GAE_VERSION):
      routing['version'] = os.environ.get(ENV_GAE_VERSION)
    if target_instance:
      routing['instance'] = target_instance
  else:
    current_service = os.environ.get(ENV_GAE_SERVICE)
    if current_service:
      routing['service'] = current_service
    current_version = os.environ.get(ENV_GAE_VERSION)
    if current_version:
      routing['version'] = current_version

  if routing:
    app_engine_http_request['app_engine_routing'] = routing

  ct_task = {'app_engine_http_request': app_engine_http_request}

  if task.name:
    ct_task['name'] = client.task_path(project, region, queue_name, task.name)

  if task.eta:
    epoch = datetime.datetime.utcfromtimestamp(0)
    eta = task.eta
    if eta.tzinfo is not None:
      eta = eta.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    delta = eta - epoch
    seconds = int(delta.total_seconds())
    nanos = int(delta.microseconds * 1000)
    timestamp = Timestamp(seconds=seconds, nanos=nanos)
    ct_task['schedule_time'] = timestamp

  if task.retry_options:
    retry_config = _build_retry_config(task.retry_options)
    if retry_config:
      ct_task['retry_config'] = retry_config

  return ct_task


def _create_single_task_in_cloud_tasks(queue_name, task, multiple):
  """Helper to create a single task using CloudTasksClient CreateTask API."""
  client = tasks_v2beta3.CloudTasksClient()
  project = _get_project_id()
  region = _get_region()

  parent = client.queue_path(project, region, queue_name)
  ct_task = _build_ct_task_payload(queue_name, task, client, project, region)

  try:
    response_task = client.create_task(request={'parent': parent, 'task': ct_task})
    task_id = response_task.name.split('/')[-1]
    task._Task__name = task_id
    task._Task__queue_name = queue_name
    task._Task__enqueued = True
    if multiple:
      return [task]
    else:
      return task
  except (google_exceptions.AlreadyExists, google_exceptions.Conflict) as e:
    raise taskqueue.TaskAlreadyExistsError(str(e))
  except google_exceptions.NotFound as e:
    raise taskqueue.UnknownQueueError(str(e))
  except google_exceptions.BadRequest as e:
    if 'Queue does not exist' in str(e):
      raise taskqueue.UnknownQueueError(str(e))
    raise e
  except Exception as e:
    raise e


def _create_batch_tasks_in_cloud_tasks(queue_name, tasks, multiple):
  """Helper to create tasks in batches using CloudTasksClient BatchCreateTasks API."""
  client = tasks_v2beta3.CloudTasksClient()
  project = _get_project_id()
  region = _get_region()

  parent = client.queue_path(project, region, queue_name)

  # Check pre-conditions
  task_names = set()
  for task in tasks:
    if task.name:
      if task.name in task_names:
        raise taskqueue.DuplicateTaskNameError(
            'The task name %s is duplicated' % task.name
        )
      task_names.add(task.name)

  created_tasks = []
  for i in range(0, len(tasks), _BATCH_CREATE_TASKS_MAX_SIZE):
    batch = tasks[i : i + _BATCH_CREATE_TASKS_MAX_SIZE]
    requests_payload = []
    for t in batch:
      ct_task_payload = _build_ct_task_payload(
          queue_name, t, client, project, region
      )
      requests_payload.append({'parent': parent, 'task': ct_task_payload})

    try:
      op = client.batch_create_tasks(
          request={'parent': parent, 'requests': requests_payload}
      )
      metadata = getattr(op, 'metadata', {})
      failed_requests = getattr(metadata, 'failed_requests', getattr(metadata, 'failedRequests', {}))
      response = getattr(op, 'response', None)
      response_tasks = getattr(response, 'tasks', []) if response else []

      res_iter = iter(response_tasks)
      exception = None

      for idx, t in enumerate(batch):
        error_status = failed_requests.get(idx) or failed_requests.get(str(idx))
        if error_status:
          code = getattr(error_status, 'code', None)
          tq_code = _map_rest_code_to_tq_code(code)
          if exception is None or isinstance(exception, taskqueue.TaskAlreadyExistsError) or isinstance(exception, taskqueue.TombstonedTaskError):
            exception = taskqueue._TranslateError(tq_code)
        else:
          try:
            res_task = next(res_iter)
            task_id = res_task.name.split('/')[-1] if hasattr(res_task, 'name') else res_task['name'].split('/')[-1]
            t._Task__name = task_id
            t._Task__queue_name = queue_name
            t._Task__enqueued = True
            created_tasks.append(t)
          except StopIteration:
            pass

      if exception is not None:
        raise exception
    except (google_exceptions.AlreadyExists, google_exceptions.Conflict) as e:
      raise taskqueue.TaskAlreadyExistsError(str(e))
    except google_exceptions.NotFound as e:
      raise taskqueue.UnknownQueueError(str(e))
    except google_exceptions.BadRequest as e:
      if 'Queue does not exist' in str(e):
        raise taskqueue.UnknownQueueError(str(e))
      raise e
    except Exception as e:
      raise e

  if multiple:
    return created_tasks
  else:
    return created_tasks[0]


def _map_rest_code_to_tq_code(code):
  """Maps gRPC / HTTP error status codes to legacy TaskQueue error enum codes."""
  if code in [code_pb2.NOT_FOUND, http.HTTPStatus.NOT_FOUND]:
    return taskqueue_service_pb2.TaskQueueServiceError.UNKNOWN_TASK
  if code in [code_pb2.INVALID_ARGUMENT, http.HTTPStatus.BAD_REQUEST]:
    return taskqueue_service_pb2.TaskQueueServiceError.INVALID_TASK_NAME
  if code in [code_pb2.ALREADY_EXISTS, http.HTTPStatus.CONFLICT]:
    return taskqueue_service_pb2.TaskQueueServiceError.TASK_ALREADY_EXISTS
  if code in [code_pb2.PERMISSION_DENIED, http.HTTPStatus.FORBIDDEN]:
    return taskqueue_service_pb2.TaskQueueServiceError.PERMISSION_DENIED
  return taskqueue_service_pb2.TaskQueueServiceError.INTERNAL_ERROR
