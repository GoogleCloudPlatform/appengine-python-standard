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
import contextlib
import datetime
import json
import logging
import os
import uuid

from google.api_core import exceptions as google_exceptions
from google.appengine.api import datastore
from google.appengine.api.taskqueue import cloudtask
from google.appengine.api.taskqueue import taskqueue
from google.cloud import tasks_v2beta3
from google.protobuf.timestamp_pb2 import Timestamp

try:
  from google.appengine.ext import ndb
except ImportError:
  ndb = None

# Constants
_PENDING_TASK_KIND = '_AE_PendingCloudTask'
_TX_TASK_STATUS_PENDING = 'PENDING'
_TX_TASK_STATUS_PROCESSING = 'PROCESSING'
_TX_TASK_STATUS_DONE = 'DONE'
_TX_TASK_STATUS_FAILED = 'FAILED'

_SWEEPER_MAX_RETRIES = 5
_SWEEPER_LOCK_TIMEOUT_SECONDS = 60
_SWEEPER_FAST_PATH_GRACE_SECONDS = 60


# ==============================================================================
# Public APIs
# ==============================================================================


def add_transactional_tasks(queue_name, tasks, multiple):
  """Stages transactional tasks in Datastore within the active transaction."""
  # Check pre-conditions (duplicate names or already queued)
  for task in tasks:
    if task.name:
      raise taskqueue.InvalidTaskNameError(
          'A task bound to a transaction cannot be named.'
      )
    if task.was_enqueued:
      raise taskqueue.BadTaskStateError('The task has already been enqueued.')

  pending_keys = []
  for task in tasks:
    task_uuid = uuid.uuid4().hex
    generated_name = f"tx-{task_uuid}"
    task._Task__name = generated_name
    task._Task__queue_name = queue_name

    ct_task_payload = build_task_payload_for_transactional_task(
        queue_name, task
    )

    # Serialize payload for storage in Datastore
    st_dict = None
    if 'schedule_time' in ct_task_payload:
      st = ct_task_payload['schedule_time']
      st_dict = {'seconds': getattr(st, 'seconds', 0), 'nanos': getattr(st, 'nanos', 0)}

    ae_req = dict(ct_task_payload['app_engine_http_request'])
    body_serialized = ae_req.get('body', b'')
    if isinstance(body_serialized, bytes):
      body_serialized = base64.b64encode(body_serialized).decode('utf-8')
    ae_req['body'] = body_serialized

    serializable_payload = {
        'name': ct_task_payload.get('name'),
        'app_engine_http_request': ae_req,
    }
    if st_dict:
      serializable_payload['schedule_time'] = st_dict
    if 'retry_config' in ct_task_payload:
      serializable_payload['retry_config'] = ct_task_payload['retry_config']

    entity = datastore.Entity(_PENDING_TASK_KIND)
    entity['task_name'] = generated_name
    entity['queue_name'] = queue_name
    entity['payload'] = json.dumps(serializable_payload)
    entity['status'] = _TX_TASK_STATUS_PENDING
    entity['created'] = datetime.datetime.utcnow()
    entity['retry_count'] = 0

    with _use_default_datastore_adapter():
      datastore.Put(entity)
    pending_keys.append(entity.key())
    task._Task__enqueued = True

  _register_post_commit_dispatch(queue_name, pending_keys)

  if multiple:
    return tasks
  else:
    return tasks[0]


def build_task_payload_for_transactional_task(queue_name, task):
  """Builds the Cloud Tasks task payload for a transactional task."""
  client = tasks_v2beta3.CloudTasksClient()
  project = cloudtask._get_project_id()
  region = cloudtask._get_region()

  return cloudtask._build_ct_task_payload(queue_name, task, client, project, region)


def dispatch_task_payload(queue_name, task_payload):
  """Dispatches a pre-built task payload immediately using CloudTasksClient."""
  client = tasks_v2beta3.CloudTasksClient()
  project = cloudtask._get_project_id()
  region = cloudtask._get_region()

  parent = client.queue_path(project, region, queue_name)

  # Prepare task payload for GAPIC client call
  if 'app_engine_http_request' in task_payload:
    ae_req = dict(task_payload['app_engine_http_request'])
    if 'body' in ae_req and isinstance(ae_req['body'], str):
      ae_req['body'] = base64.b64decode(ae_req['body'].encode('utf-8'))
    task_payload['app_engine_http_request'] = ae_req

  if 'schedule_time' in task_payload and isinstance(task_payload['schedule_time'], dict):
    st = task_payload['schedule_time']
    task_payload['schedule_time'] = Timestamp(seconds=st.get('seconds', 0), nanos=st.get('nanos', 0))

  client.create_task(request={'parent': parent, 'task': task_payload})


def sweep():
  """Queries Datastore for pending Cloud Tasks and dispatches them."""
  try:
    with _use_default_datastore_adapter():
      query = datastore.Query(_PENDING_TASK_KIND)
      entities = query.Run()
  except Exception as e:
    logging.error("Failed to query %s in sweeper: %s", _PENDING_TASK_KIND, e)
    return

  now = datetime.datetime.utcnow()
  keys_to_dispatch = []
  for entity in entities:
    if not entity:
      continue
    status = entity.get('status', _TX_TASK_STATUS_PENDING)
    if status == _TX_TASK_STATUS_DONE:
      continue
    if status == _TX_TASK_STATUS_PROCESSING:
      lock_expires = entity.get('lock_expires')
      if lock_expires and isinstance(lock_expires, datetime.datetime):
        if now < lock_expires:
          continue  # still actively processing and lock valid
      elif not lock_expires:
        continue  # assume lock valid if just started

    created = entity.get('created')
    if status == _TX_TASK_STATUS_PENDING and created and isinstance(created, datetime.datetime):
      if (now - created).total_seconds() < _SWEEPER_FAST_PATH_GRACE_SECONDS:
        continue  # give fast-path grace period to dispatch post-commit

    retry_count = entity.get('retry_count', 0)
    if status == _TX_TASK_STATUS_FAILED and retry_count >= _SWEEPER_MAX_RETRIES:
      continue  # exceeded max sweeper retries

    keys_to_dispatch.append(entity.key())

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


def _dispatch_pending_keys_now(pending_keys, handled_by_sweeper=False):
  try:
    with _use_default_datastore_adapter(non_transactional=True):
      entities = datastore.Get(pending_keys)
  except Exception as e:
    logging.error("Failed to fetch pending transactional tasks: %s", e)
    return

  if not isinstance(entities, list):
    entities = [entities]

  for entity in entities:
    if not entity:
      continue
    task_name = entity.get('task_name')
    queue_name = entity.get('queue_name')
    payload_str = entity.get('payload')

    # Acquire lock on entity to prevent duplicate sweeper dispatches
    now = datetime.datetime.utcnow()
    try:
      entity['status'] = _TX_TASK_STATUS_PROCESSING
      entity['lock_expires'] = now + datetime.timedelta(seconds=_SWEEPER_LOCK_TIMEOUT_SECONDS)
      entity['handled_by_sweeper'] = handled_by_sweeper
      with _use_default_datastore_adapter(non_transactional=True):
        datastore.Put(entity)
    except Exception as e:
      logging.warning("Failed to acquire lock for task %s: %s", task_name, e)
      continue

    try:
      payload = json.loads(payload_str)
      dispatch_task_payload(queue_name, payload)
      with _use_default_datastore_adapter(non_transactional=True):
        datastore.Delete(entity.key())
      logging.info("Successfully dispatched transactional task %s", task_name)
    except (google_exceptions.AlreadyExists, google_exceptions.Conflict):
      with _use_default_datastore_adapter(non_transactional=True):
        datastore.Delete(entity.key())
      logging.info("Transactional task %s already exists in Cloud Tasks; cleaned up entity", task_name)
    except Exception as e:
      logging.error(
          "Failed to dispatch transactional task %s: %s", task_name, e
      )
      retry_count = entity.get('retry_count', 0) + 1
      entity['retry_count'] = retry_count
      entity['last_error'] = str(e)[:500]
      if retry_count >= _SWEEPER_MAX_RETRIES:
        entity['status'] = _TX_TASK_STATUS_FAILED
        entity['lock_expires'] = None
      else:
        entity['status'] = _TX_TASK_STATUS_PENDING
        entity['lock_expires'] = None
      try:
        with _use_default_datastore_adapter(non_transactional=True):
          datastore.Put(entity)
      except Exception as put_err:
        logging.error("Failed to record error state for task %s: %s", task_name, put_err)


def _register_post_commit_dispatch(queue_name, pending_keys):
  if ndb and ndb.in_transaction():
    ndb.get_context().call_on_commit(
        lambda: _dispatch_pending_keys_now(pending_keys)
    )
    return

  if datastore.IsInTransaction():
    conn = datastore._GetConnection()
    if not hasattr(conn, '_on_commit_callbacks'):
      conn._on_commit_callbacks = []
    conn._on_commit_callbacks.append(
        lambda: _dispatch_pending_keys_now(pending_keys)
    )
    return

  raise taskqueue.BadTransactionStateError(
      'Transactional tasks must be added inside a transaction.'
  )
