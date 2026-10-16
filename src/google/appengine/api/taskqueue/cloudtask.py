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
import functools
import http
import json
import os
import re
import threading
import time
import urllib.error
import urllib.request
from google.appengine.api import app_identity
from google.appengine.api.taskqueue import taskqueue
from google.appengine.api.taskqueue import taskqueue_service_bytes_pb2 as taskqueue_service_pb2
from google.protobuf import duration_pb2
from google.protobuf import field_mask_pb2
from google.protobuf.timestamp_pb2 import Timestamp

# google-cloud-tasks>=2.25.0 (the first release with the v2 batch APIs)
# requires Python 3.10+, so it is only installed there. Import it lazily so
# the legacy TaskQueue path keeps working when it is not available.
try:
  from google.api_core import exceptions as google_exceptions
  from google.api_core import retry as google_retry
  from google.cloud import tasks_v2
  from google.cloud import tasks_v2beta3
  from google.rpc import code_pb2
  _CLOUD_TASKS_IMPORT_ERROR = None
except ImportError as e:
  google_exceptions = google_retry = tasks_v2 = tasks_v2beta3 = code_pb2 = None
  _CLOUD_TASKS_IMPORT_ERROR = e

# Environment variable constants
ENV_USE_CLOUDTASK_PUSH_QUEUE = 'APPENGINE_USE_CLOUDTASK_PUSH_QUEUE'
ENV_LOCATION_ID = 'LOCATION_ID'
ENV_GAE_LOCATION = 'GAE_LOCATION'
ENV_GAE_REGION = 'GAE_REGION'
ENV_REGION_ID = 'REGION_ID'
ENV_LOCAL_GCP_REGION = 'LOCAL_GCP_REGION'
ENV_GOOGLE_CLOUD_PROJECT = 'GOOGLE_CLOUD_PROJECT'
ENV_GAE_SERVICE = 'GAE_SERVICE'
ENV_GAE_VERSION = 'GAE_VERSION'

_LEGACY_REGION_MAP = {
    'us-central': 'us-central1',
    'europe-west': 'europe-west1',
}

# Sizing & concurrency constants
_MAX_CONCURRENT_API_CALLS = 100
_BATCH_CREATE_TASKS_MAX_SIZE = 100
_BATCH_DELETE_TASKS_MAX_SIZE = 1000
_METADATA_SERVER_TIMEOUT_SECONDS = 2
# Default RPC timeout for batch calls when the caller sets no deadline, and
# the upper bound on caller-supplied RPC deadlines. The client library sets
# 20s for non-batch RPCs (and no default for batch RPCs) because the Cloud
# Tasks service rejects request deadlines more than 30s in the future.
_DEFAULT_RPC_TIMEOUT_SECONDS = 20

# Cloud Tasks error details carry the backend TaskQueue error name, e.g.
# "apphosting::ExecutorServiceError::UNKNOWN_QUEUE".
_EXECUTOR_ERROR_RE = re.compile(r'ExecutorServiceError::([A-Z_]+)')

_THREAD_POOL = futures.ThreadPoolExecutor(_MAX_CONCURRENT_API_CALLS)

# Cloud Tasks clients are expensive to create (credential lookup and gRPC
# channel setup), so one client per API version is created lazily and reused.
# GAPIC clients are thread-safe. The cache is keyed by process ID so that a
# forked worker never reuses a gRPC channel created in its parent process.
_CLIENT_LOCK = threading.Lock()
_CLIENTS = {}
_CACHED_REGION = None


def _to_taskqueue_error(error):
  """Maps a Cloud Tasks API error to the TaskQueue error legacy would raise.

  Returns error unchanged if it is already a taskqueue.Error or is not a
  Cloud Tasks API error.
  """
  if isinstance(error, taskqueue.Error):
    return error
  detail = str(error)
  # The client library only retries transient errors, so running out of
  # retries is a transient error too.
  if (google_exceptions is not None
      and isinstance(error, google_exceptions.RetryError)):
    return taskqueue.TransientError(detail)
  if (google_exceptions is None
      or not isinstance(error, google_exceptions.GoogleAPICallError)):
    return error

  match = _EXECUTOR_ERROR_RE.search(detail)
  error_codes = taskqueue_service_pb2.TaskQueueServiceError.ErrorCode
  if match and match.group(1) in error_codes.keys():
    code = error_codes.Value(match.group(1))
    if code in taskqueue._ERROR_MAPPING:
      return taskqueue._TranslateError(code, detail)

  # Aborted subclasses Conflict (HTTP 409) but does not mean the task exists.
  if isinstance(error, (google_exceptions.Aborted,
                        google_exceptions.ServiceUnavailable,
                        google_exceptions.DeadlineExceeded,
                        google_exceptions.TooManyRequests)):
    return taskqueue.TransientError(detail)
  if isinstance(error, (google_exceptions.AlreadyExists,
                        google_exceptions.Conflict)):
    return taskqueue.TaskAlreadyExistsError(detail)
  if isinstance(error, google_exceptions.NotFound):
    return taskqueue.UnknownQueueError(detail)
  if (isinstance(error, google_exceptions.BadRequest)
      and 'queue does not exist' in detail.lower()):
    return taskqueue.UnknownQueueError(detail)
  if isinstance(error, (google_exceptions.PermissionDenied,
                        google_exceptions.Unauthenticated)):
    return taskqueue.PermissionDeniedError(detail)
  if isinstance(error, google_exceptions.InternalServerError):
    return taskqueue.InternalError(detail)
  return taskqueue.Error(detail)


def _translate_errors(fn):
  """Re-raises Cloud Tasks API errors from fn as taskqueue.Error subclasses."""

  @functools.wraps(fn)
  def wrapper(*args, **kwargs):
    try:
      return fn(*args, **kwargs)
    except Exception as e:  # pylint: disable=broad-except
      mapped = _to_taskqueue_error(e)
      if mapped is e:
        raise
      raise mapped from e

  return wrapper


# ==============================================================================
# Public APIs
# ==============================================================================


def is_cloudtask_push_queue_enabled():
  """Checks if Cloud Tasks backend is enabled for Push Queues.

  Raises:
    ImportError: If the backend is enabled but google-cloud-tasks is not
      installed.
  """
  enabled = (
      str(os.environ.get(ENV_USE_CLOUDTASK_PUSH_QUEUE, '')).lower() == 'true')
  if enabled and _CLOUD_TASKS_IMPORT_ERROR is not None:
    raise ImportError(
        '%s is set, but google-cloud-tasks>=2.25.0 could not be imported. '
        'Cloud Tasks push queues require Python 3.10 or later.'
        % ENV_USE_CLOUDTASK_PUSH_QUEUE) from _CLOUD_TASKS_IMPORT_ERROR
  return enabled


@_translate_errors
def create_tasks_in_cloud_tasks(queue_name, tasks, multiple, deadline=None):
  """Creates one or more tasks using Cloud Tasks API (supporting BatchCreateTasks)."""
  if len(tasks) > _BATCH_CREATE_TASKS_MAX_SIZE:
    raise taskqueue.TooManyTasksError(
        'No more than %d tasks can be added in a single call'
        % _BATCH_CREATE_TASKS_MAX_SIZE
    )
  for task in tasks:
    if task.was_enqueued:
      raise taskqueue.BadTaskStateError('The task has already been enqueued.')
  deadline_at = _deadline_at(deadline)
  if len(tasks) == 1:
    return _create_single_task_in_cloud_tasks(
        queue_name, tasks[0], multiple, deadline_at)
  else:
    return _create_batch_tasks_in_cloud_tasks(
        queue_name, tasks, multiple, deadline_at)


@_translate_errors
def delete_tasks_in_cloud_tasks(queue_name, tasks, multiple, deadline=None):
  """Deletes tasks from a queue using Cloud Tasks Client SDK (supporting BatchDeleteTasks)."""
  if not tasks:
    return [] if multiple else None
  if len(tasks) > _BATCH_DELETE_TASKS_MAX_SIZE:
    raise taskqueue.TooManyTasksError(
        'No more than %d tasks can be deleted in a single call'
        % _BATCH_DELETE_TASKS_MAX_SIZE
    )
  deadline_at = _deadline_at(deadline)
  client = _get_client()
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

  task_names = [
      client.task_path(project, region, queue_name, t.name) for t in tasks
  ]
  op = client.batch_delete_tasks(
      request={'parent': parent, 'names': task_names},
      **_timeout_kwargs(deadline_at, _DEFAULT_RPC_TIMEOUT_SECONDS)
  )
  metadata = getattr(op, 'metadata', None)
  failed_requests = (
      getattr(
          metadata,
          'failed_requests',
          getattr(metadata, 'failedRequests', None),
      )
      if metadata
      else None
  )
  _extract_lro_response(op, has_failed_requests=bool(failed_requests))

  exception = None
  for idx, t in enumerate(tasks):
    error_status = _get_failed_request(failed_requests, idx)
    if error_status:
      code = getattr(error_status, 'code', None)
      msg = getattr(error_status, 'message', '')
      tq_code = _map_rest_code_to_tq_code(code, msg)
      if tq_code in [
          taskqueue_service_pb2.TaskQueueServiceError.UNKNOWN_TASK,
          taskqueue_service_pb2.TaskQueueServiceError.TOMBSTONED_TASK,
      ]:
        t._Task__deleted = False
      elif exception is None:
        exception = taskqueue._TranslateError(tq_code, msg)
    else:
      t._Task__deleted = True

  if exception is not None:
    raise exception

  if multiple:
    return tasks
  else:
    return tasks[0]


@_translate_errors
def purge_queue_in_cloud_tasks(queue_name):
  """Purges all tasks in a queue using Cloud Tasks API."""
  client = _get_client()
  project = _get_project_id()
  region = _get_region()

  name = client.queue_path(project, region, queue_name)
  try:
    client.purge_queue(request={'name': name})
  except Exception as e:
    raise e


@_translate_errors
def fetch_queue_stats_in_cloud_tasks(queues, multiple, deadline=None):
  """Fetches queue statistics for given queues using Cloud Tasks API (v2beta3)."""
  deadline_at = _deadline_at(deadline)
  # QueueStats is retained on v2beta3 as it is out of scope for v2 GA
  client = _get_v2beta3_client()
  project = _get_project_id()
  region = _get_region()

  queue_stats_list = []
  read_mask = field_mask_pb2.FieldMask(paths=['stats'])

  for queue in queues:
    queue_name = queue.name if hasattr(queue, 'name') else str(queue)
    name = client.queue_path(project, region, queue_name)
    try:
      call_options = _timeout_kwargs(deadline_at)
      if call_options:
        call_options['retry'] = _get_queue_retry(call_options['timeout'])
      q_resp = client.get_queue(
          request={'name': name, 'read_mask': read_mask}, **call_options)
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

  def __init__(self, future_or_callable, callback=None):
    if callable(future_or_callable):
      self._future = _THREAD_POOL.submit(future_or_callable)
    else:
      self._future = future_or_callable
    self.callback = callback
    self._callback_called = False

  def get_result(self):
    self.wait()
    return self._future.result()

  def wait(self):
    """Waits for completion and runs the callback once, like UserRPC.wait."""
    futures.wait([self._future])
    if self.callback is not None and not self._callback_called:
      self._callback_called = True
      self.callback()

  def check_success(self):
    self.wait()
    self._future.result()

  @property
  def future(self):
    return self._future


class _DeadlineOnlyRPC(object):
  """Carries a deadline to _make_rpc in place of a UserRPC.

  Used by the synchronous methods that take a deadline argument. Creating a
  UserRPC requires the taskqueue API stub, which Cloud Tasks mode does not
  otherwise need.
  """

  def __init__(self, deadline):
    self.deadline = deadline
    self.callback = None


def _make_rpc(fn, rpc=None):
  """Runs fn in the background and returns an RPC-like object for it.

  If the caller supplied a UserRPC, it is returned with wait, check_success
  and get_result bound to the Cloud Tasks call, and its callback is run on
  wait like the legacy path. UserRPC.wait_any and wait_all are not supported.
  """
  ct_rpc = _CloudTaskRPC(fn, callback=getattr(rpc, 'callback', None))
  if rpc is None:
    return ct_rpc
  rpc.wait = ct_rpc.wait
  rpc.check_success = ct_rpc.check_success
  rpc.get_result = ct_rpc.get_result
  return rpc


def _deadline_at(deadline):
  """Returns the monotonic time at which a caller's RPC deadline expires.

  Returns None if the caller did not set a deadline.
  """
  return None if deadline is None else time.monotonic() + deadline


def _timeout_kwargs(deadline_at, default=None):
  """Returns the timeout argument for a Cloud Tasks call.

  The timeout is the time left before deadline_at, capped at
  _DEFAULT_RPC_TIMEOUT_SECONDS because Cloud Tasks rejects request deadlines
  more than 30s in the future. If no deadline is set, default is used, or if
  default is None no timeout is passed and the client's 20s default applies.
  """
  if deadline_at is None:
    return {} if default is None else {'timeout': default}
  remaining = max(deadline_at - time.monotonic(), 0.001)
  return {'timeout': min(remaining, _DEFAULT_RPC_TIMEOUT_SECONDS)}


def _get_queue_retry(timeout):
  """Returns the client's default GetQueue retry, limited to timeout seconds.

  A timeout alone bounds only each attempt; the default retry keeps retrying
  DEADLINE_EXCEEDED for up to 20 seconds.
  """
  return google_retry.Retry(
      initial=0.1,
      maximum=10.0,
      multiplier=1.3,
      predicate=google_retry.if_exception_type(
          google_exceptions.DeadlineExceeded,
          google_exceptions.ServiceUnavailable,
      ),
      deadline=timeout,
  )


def _get_cached_client(api_version, factory):
  """Returns the cached client for api_version, creating it on first use."""
  key = (api_version, os.getpid())
  client = _CLIENTS.get(key)
  if client is None:
    with _CLIENT_LOCK:
      client = _CLIENTS.get(key)
      if client is None:
        client = factory()
        _CLIENTS[key] = client
  return client


def _get_client():
  """Returns the shared Cloud Tasks v2 client."""
  return _get_cached_client('v2', lambda: tasks_v2.CloudTasksClient())


def _get_v2beta3_client():
  """Returns the shared Cloud Tasks v2beta3 client, used only for QueueStats."""
  return _get_cached_client(
      'v2beta3', lambda: tasks_v2beta3.CloudTasksClient()
  )


def _reset_clients():
  """Drops cached clients and region. Intended for tests."""
  global _CACHED_REGION
  with _CLIENT_LOCK:
    _CLIENTS.clear()
    _CACHED_REGION = None


def _get_project_id():
  """Extracts and formats the Google Cloud project ID."""
  project = os.environ.get(ENV_GOOGLE_CLOUD_PROJECT)
  if project and (project.startswith('s~') or project.startswith('e~')):
    project = project[2:]
  return project


def _normalize_region(region):
  """Maps legacy App Engine region names to Cloud Tasks locations."""
  if not region:
    return region
  region = region.strip()
  return _LEGACY_REGION_MAP.get(region, region)


def _get_region():
  """Determines the App Engine region."""
  global _CACHED_REGION
  region = (
      os.environ.get(ENV_LOCATION_ID)
      or os.environ.get(ENV_GAE_LOCATION)
      or os.environ.get(ENV_GAE_REGION)
      or os.environ.get(ENV_REGION_ID)
  )
  if region:
    return _normalize_region(region)

  if _CACHED_REGION:
    return _CACHED_REGION

  try:
    req = urllib.request.Request(
        'http://metadata.google.internal/computeMetadata/v1/instance/region',
        headers={'Metadata-Flavor': 'Google'},
    )
    with urllib.request.urlopen(req, timeout=_METADATA_SERVER_TIMEOUT_SECONDS) as response:
      region_path = response.read().decode('utf-8')
      resolved = _normalize_region(region_path.split('/')[-1])
      if resolved:
        _CACHED_REGION = resolved
        return resolved
  except Exception:
    pass

  # Fallback to us-central1 if we can't detect it; do not cache fallback.
  return _normalize_region(os.environ.get(ENV_LOCAL_GCP_REGION, 'us-central1'))


def _to_duration(seconds):
  if seconds is None:
    return None
  duration = duration_pb2.Duration()
  # Rounding avoids float error, e.g. 2.3 seconds becoming 2s 299999999ns.
  duration.FromNanoseconds(int(round(seconds * 1e9)))
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
  # Cloud Tasks does not allow Host, X-Google-* or X-AppEngine-* headers to
  # be set; it sets the App Engine headers (queue name, task name, etc.)
  # itself when the task is dispatched.
  headers = {}
  for key, value in (task.headers or {}).items():
    lower_key = key.lower()
    if (lower_key == 'host' or lower_key.startswith('x-google-')
        or lower_key.startswith('x-appengine-')):
      continue
    headers[key] = value

  body = b''
  if task.payload:
    if isinstance(task.payload, str):
      body = task.payload.encode('utf-8')
    else:
      body = task.payload

  http_method = tasks_v2.HttpMethod.POST
  if task.method:
    method_map = {
        'POST': tasks_v2.HttpMethod.POST,
        'GET': tasks_v2.HttpMethod.GET,
        'PUT': tasks_v2.HttpMethod.PUT,
        'DELETE': tasks_v2.HttpMethod.DELETE,
        'HEAD': tasks_v2.HttpMethod.HEAD,
    }
    http_method = method_map.get(task.method, tasks_v2.HttpMethod.POST)

  app_engine_http_request = {
      'http_method': http_method,
      'relative_uri': task.url or '/',
      'body': body,
      'headers': headers,
  }

  routing = {}
  current_service = os.environ.get(ENV_GAE_SERVICE)
  current_version = os.environ.get(ENV_GAE_VERSION)
  if isinstance(task.target, str) and task.target:
    # A target derived from a "-dot-" hostname looks like "v1-dot-worker-dot".
    # If a full hostname was passed as target, strip the project/domain suffix.
    target_str = task.target.split(':', 1)[0]
    app_host = project
    if project and ':' in project:
      domain, app_id = project.split(':', 1)
      app_host = f'{app_id}.{domain}'

    matched_other_project = False
    if target_str.endswith('.appspot.com'):
      host_body = target_str[: -len('.appspot.com')]
      if host_body.endswith('.r'):
        r_dot = host_body[:-2].rfind('.')
        if r_dot != -1:
          host_body = host_body[:r_dot]
      normalized_host = host_body.replace('-dot-', '.')
      if app_host:
        if normalized_host == app_host:
          target_str = ''
        elif normalized_host.endswith('.' + app_host):
          target_str = normalized_host[: -(len(app_host) + 1)]
        else:
          matched_other_project = True
      else:
        parts = normalized_host.rsplit('.', 1)
        target_str = parts[0] if len(parts) > 1 else ''
    elif app_host:
      for sep in ('-dot-' + app_host + '.', '.' + app_host + '.'):
        if sep in target_str:
          target_str = target_str[: target_str.rfind(sep)]
          break
      else:
        if target_str.startswith(app_host + '.'):
          target_str = ''

    if matched_other_project:
      target_service = current_service
      target_version = current_version
      target_instance = None
    else:
      if target_str.endswith('-dot'):
        target_str = target_str[:-4]
      if not target_str:
        target_service = 'default'
        target_version = None
        target_instance = None
      else:
        target_components = target_str.replace('-dot-', '.').rsplit('.', 3)
        target_service = target_components[-1]
        target_version = (
            len(target_components) > 1 and target_components[-2] or None
        )
        target_instance = (
            len(target_components) > 2 and target_components[-3] or None
        )

    if target_service:
      routing['service'] = target_service
    if target_version:
      routing['version'] = target_version
    elif current_version and target_service == current_service:
      # Like legacy push queues, a task for the current service runs on the
      # version that enqueued it. Other services use their default version.
      routing['version'] = current_version
    if target_instance:
      routing['instance'] = target_instance
  else:
    if current_service:
      routing['service'] = current_service
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


def _create_single_task_in_cloud_tasks(queue_name, task, multiple,
                                       deadline_at=None):
  """Helper to create a single task using CloudTasksClient CreateTask API."""
  client = _get_client()
  project = _get_project_id()
  region = _get_region()

  parent = client.queue_path(project, region, queue_name)
  ct_task = _build_ct_task_payload(queue_name, task, client, project, region)

  response_task = client.create_task(
      request={'parent': parent, 'task': ct_task},
      **_timeout_kwargs(deadline_at))
  task_id = response_task.name.split('/')[-1]
  task._Task__name = task_id
  task._Task__queue_name = queue_name
  task._Task__enqueued = True
  if multiple:
    return [task]
  else:
    return task


def _extract_lro_response(op, has_failed_requests=False):
  """Extracts the unpacked response message from a synchronous LRO."""
  raw_op = getattr(op, 'operation', None)
  if raw_op is not None and not getattr(raw_op, 'done', True):
    raise taskqueue.InternalError(
        'Cloud Tasks batch operation returned done=False'
    )
  if hasattr(op, 'result') and callable(op.result):
    if (not isinstance(op, futures.Future)
        and getattr(op, 'response', None) is not None):
      return op.response
    try:
      return op.result(timeout=0)
    except TypeError:
      return op.result()
    except Exception:  # pylint: disable=broad-except
      if has_failed_requests:
        return None
      raise
  return getattr(op, 'response', None)


def _set_preferred_exception(current, candidate):
  """Prefers non-duplicate errors over TaskAlreadyExists/TombstonedTask errors."""
  if candidate is None:
    return current
  if (current is None
      or isinstance(current, (taskqueue.TaskAlreadyExistsError,
                              taskqueue.TombstonedTaskError))):
    return candidate
  return current


def _create_batch_tasks_in_cloud_tasks(queue_name, tasks, multiple,
                                       deadline_at=None):
  """Helper to create tasks in a batch using CloudTasksClient BatchCreateTasks API."""
  client = _get_client()
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

  requests_payload = [
      {
          'parent': parent,
          'task': _build_ct_task_payload(
              queue_name, t, client, project, region
          ),
      }
      for t in tasks
  ]
  op = client.batch_create_tasks(
      request={'parent': parent, 'requests': requests_payload},
      **_timeout_kwargs(deadline_at, _DEFAULT_RPC_TIMEOUT_SECONDS)
  )
  metadata = getattr(op, 'metadata', None)
  failed_requests = (
      getattr(
          metadata,
          'failed_requests',
          getattr(metadata, 'failedRequests', None),
      )
      if metadata
      else None
  )
  response = _extract_lro_response(op, has_failed_requests=bool(failed_requests))
  response_tasks = getattr(response, 'tasks', []) if response else []

  res_iter = iter(response_tasks)
  created_tasks = []
  exception = None
  missing_task_idx = None

  for idx, t in enumerate(tasks):
    error_status = _get_failed_request(failed_requests, idx)
    if error_status:
      code = getattr(error_status, 'code', None)
      msg = getattr(error_status, 'message', '')
      tq_code = _map_rest_code_to_tq_code(code, msg)
      err = taskqueue._TranslateError(tq_code, msg)
      exception = _set_preferred_exception(exception, err)
    else:
      try:
        res_task = next(res_iter)
        task_id = (
            res_task.name.split('/')[-1]
            if hasattr(res_task, 'name')
            else res_task['name'].split('/')[-1]
        )
        t._Task__name = task_id
        t._Task__queue_name = queue_name
        t._Task__enqueued = True
        created_tasks.append(t)
      except StopIteration:
        if missing_task_idx is None:
          missing_task_idx = idx

  if exception is None and missing_task_idx is not None:
    exception = taskqueue.InternalError(
        'BatchCreateTasks response is missing created task at index %d'
        % missing_task_idx
    )

  if exception is not None:
    raise exception

  if multiple:
    return created_tasks
  else:
    return created_tasks[0]


def _get_failed_request(failed_requests, idx):
  """Safely retrieves a failed request status by index from proto map or dict."""
  if not failed_requests:
    return None
  if idx in failed_requests:
    return failed_requests[idx]
  try:
    if str(idx) in failed_requests:
      return failed_requests[str(idx)]
  except TypeError:
    pass
  return None


def _map_rest_code_to_tq_code(code, message=''):
  """Maps gRPC / HTTP error status codes to legacy TaskQueue error enum codes."""
  if message:
    match = _EXECUTOR_ERROR_RE.search(message)
    error_codes = taskqueue_service_pb2.TaskQueueServiceError.ErrorCode
    if match and match.group(1) in error_codes.keys():
      return error_codes.Value(match.group(1))
  if code in [code_pb2.NOT_FOUND, http.HTTPStatus.NOT_FOUND]:
    return taskqueue_service_pb2.TaskQueueServiceError.UNKNOWN_TASK
  if code in [code_pb2.INVALID_ARGUMENT, http.HTTPStatus.BAD_REQUEST]:
    # INVALID_ARGUMENT covers many validation failures, not just task names.
    return taskqueue_service_pb2.TaskQueueServiceError.INVALID_REQUEST
  if code in [code_pb2.ALREADY_EXISTS, http.HTTPStatus.CONFLICT]:
    return taskqueue_service_pb2.TaskQueueServiceError.TASK_ALREADY_EXISTS
  if code in [code_pb2.PERMISSION_DENIED, http.HTTPStatus.FORBIDDEN]:
    return taskqueue_service_pb2.TaskQueueServiceError.PERMISSION_DENIED
  return taskqueue_service_pb2.TaskQueueServiceError.INTERNAL_ERROR
