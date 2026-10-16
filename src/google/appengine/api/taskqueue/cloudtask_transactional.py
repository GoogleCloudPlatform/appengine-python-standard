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

"""Cloud Tasks transactional task support for Taskqueue SDK."""

import base64
from concurrent import futures
import contextlib
import contextvars
import datetime
import json
import logging
import os
import uuid

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.api.taskqueue import cloudtask
from google.appengine.api.taskqueue import taskqueue
from google.appengine.api.taskqueue import taskqueue_service_bytes_pb2 as taskqueue_service_pb2
from google.appengine.datastore import datastore_pb
from google.protobuf import duration_pb2
from google.protobuf import json_format
from google.protobuf.timestamp_pb2 import Timestamp

# Only available with google-cloud-tasks (Python 3.10+). See cloudtask.py.
google_exceptions = cloudtask.google_exceptions
tasks_v2 = cloudtask.tasks_v2

try:
  from google.appengine.ext import ndb
except ImportError:
  ndb = None

# Constants
# The kind and property names of staged tasks are shared with the Go and Java
# App Engine SDKs, so a sweeper in a service written in any of them can
# dispatch the task.
_PENDING_TASK_KIND = '_AE_PendingCloudTask'
_SDK_LANG = 'PYTHON'
_TX_TASK_STATUS_PENDING = 'PENDING'
_TX_TASK_STATUS_PROCESSING = 'PROCESSING'
_TX_TASK_STATUS_DONE = 'DONE'
_TX_TASK_STATUS_FAILED = 'FAILED'

_SWEEPER_MAX_RETRIES = 5
# Maximum entities of each status read by one sweep. Later cron runs pick up
# the rest of a backlog.
_SWEEPER_BATCH_SIZE = 500
# Like the legacy TaskQueue API, at most 5 tasks can be added in one
# transaction.
_MAX_TASKS_PER_TRANSACTION = 5
_SWEEPER_LOCK_TIMEOUT_SECONDS = 60
_SWEEPER_FAST_PATH_GRACE_SECONDS = 60
# Entities that exhausted their retries are kept this long for inspection,
# then deleted by the sweeper.
_FAILED_TASK_RETENTION = datetime.timedelta(days=7)


# ==============================================================================
# Public APIs
# ==============================================================================


def add_transactional_tasks(queue_name, tasks, multiple):
  """Stages transactional tasks in Datastore within the active transaction.

  Each task is staged as a root entity, i.e. its own entity group, so the
  transaction must be cross-group (db: CreateTransactionOptions(xg=True);
  ndb: @ndb.transactional(xg=True)) unless it touches no other entity group.
  Staging N tasks consumes N of Datastore's 25 entity groups per cross-group
  transaction (up to _MAX_TASKS_PER_TRANSACTION = 5 entity groups).
  """
  # Check pre-conditions (duplicate names or already queued)
  for task in tasks:
    if task.name:
      raise taskqueue.InvalidTaskNameError(
          'A task bound to a transaction cannot be named.'
      )
    if task.was_enqueued:
      raise taskqueue.BadTaskStateError('The task has already been enqueued.')

  if not (ndb and ndb.in_transaction()) and not datastore.IsInTransaction():
    raise taskqueue.BadTransactionStateError(
        'Transactional tasks must be added inside a transaction.'
    )

  pending_keys = _pending_keys_for_current_transaction()
  if len(pending_keys) + len(tasks) > _MAX_TASKS_PER_TRANSACTION:
    # Same error the legacy API raises from the datastore commit.
    raise taskqueue._TranslateError(
        taskqueue_service_pb2.TaskQueueServiceError.DATASTORE_ERROR
        + datastore_pb.Error.BAD_REQUEST,
        'Too many messages, maximum allowed %d' % _MAX_TASKS_PER_TRANSACTION)

  for task in tasks:
    task_uuid = uuid.uuid4().hex
    generated_name = f"tx-{task_uuid}"
    task._Task__name = generated_name
    task._Task__queue_name = queue_name

    ct_task_payload = build_task_payload_for_transactional_task(
        queue_name, task
    )

    entity = datastore.Entity(_PENDING_TASK_KIND, namespace='')
    entity['queue_name'] = queue_name
    entity['cloud_task_name'] = generated_name
    # Text is unindexed; indexed strings are limited to 1500 bytes and task
    # payloads can be up to 100KB.
    entity['cloud_task_payload'] = datastore_types.Text(
        _encode_task_payload(ct_task_payload))
    entity['status'] = _TX_TASK_STATUS_PENDING
    entity['created'] = datetime.datetime.utcnow()
    entity['retry_count'] = 0
    entity['sdk_lang'] = _SDK_LANG

    with _use_default_datastore_adapter():
      datastore.Put(entity)
    pending_keys.append(entity.key())
    task._Task__enqueued = True

  if multiple:
    return tasks
  else:
    return tasks[0]


def build_task_payload_for_transactional_task(queue_name, task):
  """Builds the Cloud Tasks task payload for a transactional task."""
  client = cloudtask._get_client()
  project = cloudtask._get_project_id()
  region = cloudtask._get_region()

  return cloudtask._build_ct_task_payload(queue_name, task, client, project, region)


def dispatch_task_payload(queue_name, task):
  """Creates a staged task, a `tasks_v2.Task`, in Cloud Tasks."""
  client = cloudtask._get_client()
  project = cloudtask._get_project_id()
  region = cloudtask._get_region()

  parent = client.queue_path(project, region, queue_name)
  client.create_task(request={'parent': parent, 'task': task})


def _encode_task_payload(task_payload):
  """Returns the staged form of a Cloud Tasks task payload dict.

  The form is shared with the Go and Java SDKs: the JSON object {"task": T},
  where T is the proto3 JSON form of the Cloud Tasks v2 Task.
  """
  task = tasks_v2.Task(task_payload)
  return json.dumps({'task': json_format.MessageToDict(tasks_v2.Task.pb(task))})


def _decode_task_payload(payload_str):
  """Parses a payload written by _encode_task_payload or another SDK."""
  obj = json.loads(payload_str)
  if isinstance(obj.get('task'), dict):
    obj = obj['task']
  task_pb = tasks_v2.Task.pb()()
  json_format.ParseDict(obj, task_pb, ignore_unknown_fields=True)
  return tasks_v2.Task.wrap(task_pb)


def _decode_preview_payload(payload_str):
  """Parses the payload of a task staged by the preview release.

  The preview stored a dict of Task fields in the 'payload' property, with
  the body base64 encoded and times as {'seconds': s, 'nanos': n}.
  """
  task_payload = json.loads(payload_str)
  if 'app_engine_http_request' in task_payload:
    ae_req = dict(task_payload['app_engine_http_request'])
    if 'body' in ae_req and isinstance(ae_req['body'], str):
      ae_req['body'] = base64.b64decode(ae_req['body'].encode('utf-8'))
    task_payload['app_engine_http_request'] = ae_req

  if 'schedule_time' in task_payload and isinstance(task_payload['schedule_time'], dict):
    st = task_payload['schedule_time']
    task_payload['schedule_time'] = Timestamp(seconds=st.get('seconds', 0), nanos=st.get('nanos', 0))

  if 'retry_config' in task_payload and isinstance(task_payload['retry_config'], dict):
    rc = dict(task_payload['retry_config'])
    for dur_field in ('max_retry_duration', 'min_backoff', 'max_backoff'):
      if dur_field in rc and isinstance(rc[dur_field], dict):
        d = rc[dur_field]
        rc[dur_field] = duration_pb2.Duration(
            seconds=d.get('seconds', 0), nanos=d.get('nanos', 0)
        )
    task_payload['retry_config'] = rc

  return tasks_v2.Task(task_payload)


def sweep():
  """Queries Datastore for pending Cloud Tasks and dispatches them."""
  # Each status is read separately with a limit, so that memory use is
  # bounded and failed entities kept for inspection cannot crowd out
  # pending ones.
  entities = []
  for status in (_TX_TASK_STATUS_PROCESSING, _TX_TASK_STATUS_PENDING,
                 _TX_TASK_STATUS_FAILED):
    try:
      with _use_default_datastore_adapter():
        query = datastore.Query(
            _PENDING_TASK_KIND, {'status =': status}, namespace=''
        )
        # Fetch inside the adapter context; Run() returns a lazy iterator.
        entities.extend(query.Run(limit=_SWEEPER_BATCH_SIZE))
    except Exception as e:
      logging.error("Failed to query %s in sweeper: %s", _PENDING_TASK_KIND, e)
      return

  now = datetime.datetime.utcnow()
  keys_to_dispatch = []
  expired_failed_keys = []
  for entity in entities:
    if not entity:
      continue
    status = entity.get('status', _TX_TASK_STATUS_PENDING)
    if status == _TX_TASK_STATUS_DONE:
      continue
    if status == _TX_TASK_STATUS_FAILED:
      failed_at = entity.get('failed_at') or entity.get('created')
      if (isinstance(failed_at, datetime.datetime)
          and now - failed_at > _FAILED_TASK_RETENTION):
        expired_failed_keys.append(entity.key())
      continue  # exceeded max sweeper retries
    if not _is_dispatchable(entity, now):
      continue

    created = entity.get('created')
    if status == _TX_TASK_STATUS_PENDING and created and isinstance(created, datetime.datetime):
      if (now - created).total_seconds() < _SWEEPER_FAST_PATH_GRACE_SECONDS:
        continue  # give fast-path grace period to dispatch post-commit

    keys_to_dispatch.append(entity.key())

  if expired_failed_keys:
    try:
      with _use_default_datastore_adapter():
        datastore.Delete(expired_failed_keys)
      logging.info("Cloud Tasks sweeper deleted %d expired failed tasks.",
                   len(expired_failed_keys))
    except Exception as e:
      logging.error("Failed to delete expired failed tasks: %s", e)

  if keys_to_dispatch:
    logging.info("Cloud Tasks sweeper found %d tasks to process.", len(keys_to_dispatch))
    _dispatch_pending_keys_now(keys_to_dispatch, handled_by_sweeper=True)


def sweep_wsgi_app(environ, start_response):
  """WSGI app handler for /_ah/cloudtask/sweep."""
  is_cron = str(environ.get('HTTP_X_APPENGINE_CRON', '')).lower() == 'true' or str(environ.get('X-AppEngine-Cron', '')).lower() == 'true'
  if not is_cron and not str(environ.get('SERVER_SOFTWARE', '')).lower().startswith('dev'):
    status = '403 Forbidden'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [b'Access denied: endpoint only accessible via App Engine Cron.\n']

  try:
    sweep()
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [b'Sweeper completed successfully.\n']
  except Exception as e:
    logging.error("Cloud Tasks sweeper failed: %s", e)
    status = '500 Internal Server Error'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [f'Sweeper failed: {e}\n'.encode('utf-8')]


# ==============================================================================
# Private Helpers
# ==============================================================================


@contextlib.contextmanager
def _use_default_datastore_adapter(non_transactional=False):
  popped_conn = None
  if non_transactional and datastore.IsInTransaction():
    popped_conn = datastore._PopConnection()

  try:
    conn = datastore._GetConnection()
    orig_adapter = getattr(conn, '_BaseConnection__adapter', None)
    if orig_adapter is not None:
      conn._BaseConnection__adapter = datastore._adapter
      try:
        yield
      finally:
        conn._BaseConnection__adapter = orig_adapter
    else:
      yield
  finally:
    if popped_conn is not None:
      datastore._PushConnection(popped_conn)


def _is_dispatchable(entity, now):
  """Returns True if a pending task entity may be (re)dispatched now."""
  status = entity.get('status', _TX_TASK_STATUS_PENDING)
  if status == _TX_TASK_STATUS_PENDING:
    return True
  if status == _TX_TASK_STATUS_PROCESSING:
    # A dispatcher holds the lock until it expires. A missing expiry means
    # the lock was just taken.
    lock_expires = entity.get('lock_expires')
    return isinstance(lock_expires, datetime.datetime) and now >= lock_expires
  return False


def _acquire_dispatch_lock(key, handled_by_sweeper):
  """Atomically marks a pending entity as PROCESSING.

  Returns:
    The locked entity, or None if it no longer exists or another dispatcher
    holds it.
  """

  def txn():
    entity = datastore.Get(key)
    now = datetime.datetime.utcnow()
    if not _is_dispatchable(entity, now):
      return None
    entity['status'] = _TX_TASK_STATUS_PROCESSING
    entity['lock_expires'] = now + datetime.timedelta(
        seconds=_SWEEPER_LOCK_TIMEOUT_SECONDS)
    entity['handled_by_sweeper'] = handled_by_sweeper
    datastore.Put(entity)
    return entity

  try:
    with _use_default_datastore_adapter(non_transactional=True):
      return datastore.RunInTransaction(txn)
  except datastore_errors.EntityNotFoundError:
    return None  # already dispatched and deleted by another dispatcher


def _record_dispatch_failure(key, error):
  """Atomically records a failed dispatch attempt on the entity.

  Does nothing if the entity was deleted meanwhile, so a dispatcher that
  failed never recreates an entity another dispatcher already completed.
  """

  def txn():
    try:
      entity = datastore.Get(key)
    except datastore_errors.EntityNotFoundError:
      return
    now = datetime.datetime.utcnow()
    retry_count = entity.get('retry_count', 0) + 1
    entity['retry_count'] = retry_count
    entity['last_error'] = datastore_types.Text(str(error)[:500])
    entity['lock_expires'] = None
    if retry_count >= _SWEEPER_MAX_RETRIES:
      entity['status'] = _TX_TASK_STATUS_FAILED
      entity['failed_at'] = now
    else:
      entity['status'] = _TX_TASK_STATUS_PENDING
    datastore.Put(entity)

  with _use_default_datastore_adapter(non_transactional=True):
    datastore.RunInTransaction(txn)


def _finalize_dispatched_entity(entity, task_name, dispatch_error):
  """Deletes a dispatched staged entity or records its dispatch failure."""
  if dispatch_error is None:
    try:
      with _use_default_datastore_adapter(non_transactional=True):
        datastore.Delete(entity.key())
      logging.info("Successfully dispatched transactional task %s", task_name)
    except Exception as del_err:
      logging.error(
          "Failed to delete dispatched transactional task %s: %s",
          task_name,
          del_err,
      )
    return

  if isinstance(
      dispatch_error,
      (google_exceptions.AlreadyExists, google_exceptions.Conflict),
  ):
    try:
      with _use_default_datastore_adapter(non_transactional=True):
        datastore.Delete(entity.key())
      logging.info(
          "Transactional task %s already exists in Cloud Tasks; cleaned up entity",
          task_name,
      )
    except Exception as del_err:
      logging.error(
          "Failed to delete duplicate transactional task %s: %s",
          task_name,
          del_err,
      )
    return

  logging.error(
      "Failed to dispatch transactional task %s: %s", task_name, dispatch_error
  )
  try:
    _record_dispatch_failure(entity.key(), dispatch_error)
  except Exception as put_err:
    logging.error(
        "Failed to record error state for task %s: %s", task_name, put_err
    )


def _dispatch_pending_keys_now(pending_keys, handled_by_sweeper=False):
  locked_items = []
  for key in pending_keys:
    try:
      entity = _acquire_dispatch_lock(key, handled_by_sweeper)
    except Exception as e:
      logging.warning("Failed to acquire lock for task %s: %s", key, e)
      continue
    if entity is None:
      continue

    queue_name = entity.get('queue_name')
    task_name = entity.get('cloud_task_name') or entity.get('task_name')
    try:
      if entity.get('cloud_task_payload') is not None:
        task = _decode_task_payload(entity['cloud_task_payload'])
      else:
        task = _decode_preview_payload(entity.get('payload'))
    except Exception as e:
      _finalize_dispatched_entity(entity, task_name, e)
      continue

    locked_items.append((entity, queue_name, task_name, task))

  if len(locked_items) == 1:
    entity, queue_name, task_name, task = locked_items[0]
    dispatch_err = None
    try:
      dispatch_task_payload(queue_name, task)
    except Exception as e:
      dispatch_err = e
    _finalize_dispatched_entity(entity, task_name, dispatch_err)
  elif len(locked_items) > 1:
    dispatch_futures = [
        cloudtask._THREAD_POOL.submit(
            contextvars.copy_context().run,
            dispatch_task_payload,
            queue_name,
            task,
        )
        for _, queue_name, _, task in locked_items
    ]
    futures.wait(dispatch_futures)
    for (entity, _, task_name, _), fut in zip(locked_items, dispatch_futures):
      _finalize_dispatched_entity(entity, task_name, fut.exception())


def _pending_keys_for_current_transaction():
  """Returns the list of keys staged in the current transaction.

  On the first call in a transaction, the list is created and dispatch of the
  keys it will hold is registered to run after the transaction commits. Each
  transaction attempt has its own ndb context or datastore connection, so a
  retried transaction starts with an empty list.
  """
  if ndb and ndb.in_transaction():
    holder = ndb.get_context()
  elif datastore.IsInTransaction():
    holder = datastore._GetConnection()
  else:
    raise taskqueue.BadTransactionStateError(
        'Transactional tasks must be added inside a transaction.'
    )

  pending_keys = getattr(holder, '_ae_pending_cloud_task_keys', None)
  if pending_keys is not None:
    return pending_keys

  pending_keys = []
  holder._ae_pending_cloud_task_keys = pending_keys
  dispatch = lambda: _dispatch_pending_keys_now(pending_keys)
  if ndb and ndb.in_transaction():
    holder.call_on_commit(dispatch)
  else:
    if not hasattr(holder, '_on_commit_callbacks'):
      holder._on_commit_callbacks = []
    holder._on_commit_callbacks.append(dispatch)
  return pending_keys
