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
"""Functions that prepare GAE user code for running in a GCE VM."""


import functools
import json
import logging
import math
import os
import re
import typing
import wsgiref.util





from google.appengine.runtime import default_api_stub
from google.appengine.runtime import thread_hooks

import six


def GetTraceAndSpanId():
  """Gets the Trace and Span ID for the given request via environment variables.

  Checks and parses the envirionment variable "HTTP_X_CLOUD_TRACE_CONTEXT",
  which is a header provided by AppEngine (and is set as an environment
  variable as a part of the WSGI Specification).

  Returns:
    A tuple of Trace ID and the Span ID
  """


  ctx = os.getenv('HTTP_X_CLOUD_TRACE_CONTEXT')
  if ctx:
    m = re.search(r'^(\w+)/(\d+)(?:;o=[01])?$', ctx)
    if not m:
      return (None, None)
    trace_id = m.group(1)
    span_id = m.group(2)
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    return ('projects/{}/traces/{}'.format(project_id, trace_id), span_id)
  return (None, None)


def GetRequestUrl():
  """Constructs the full request url from WSGI environment variables."""
  try:
    environ = typing.cast(typing.Dict[str, typing.Any], os.environ)
    return wsgiref.util.request_uri(environ)
  except KeyError:
    return None


class JsonFormatter(logging.Formatter):
  """Class for logging to the cloud logging api with json metadata."""

  def format(self, record):
    """Format the record as json the cloud logging agent understands.

    Args:
      record: A logging.LogRecord to format.

    Returns:
      A json string to log.
    """
    float_frac_sec, float_sec = math.modf(record.created)

    message = record.getMessage()
    if record.exc_info:
      message = '%s\n%s' % (message, self.formatException(record.exc_info))

    data = {
        'message': message,
        'thread': record.thread,
        'severity': record.levelname,
        'timestamp': {
            'seconds': int(float_sec),
            'nanos': int(float_frac_sec * 1000000000)
        },
        'logging.googleapis.com/sourceLocation': {
            'file': record.pathname,
            'line': str(record.lineno),
            'function': record.funcName,
        },
        'serviceContext': {
            'version': os.getenv('GAE_VERSION'),
            'service': os.getenv('GAE_SERVICE'),
        },
        'context': {
            'user': os.getenv('USER_NICKNAME'),
            'httpRequest': {
                'url': GetRequestUrl(),
                'userAgent': os.getenv('HTTP_USER_AGENT'),
                'requestMethod': os.getenv('REQUEST_METHOD'),
                'protocol': os.getenv('SERVER_PROTOCOL')
            }
        },
    }

    trace_id, span_id = GetTraceAndSpanId()
    if trace_id:
      data['logging.googleapis.com/trace'] = trace_id
      data['logging.googleapis.com/spanId'] = span_id

    return json.dumps(data)


class SplitFileHandler(logging.FileHandler):
  """Class for splitting large logs into chunks."""

  def emit(self, record):
    """Emit a record.

    If the message is larger than the max size of a log entry of 256KB
    (https://cloud.google.com/logging/quotas#log-limits), it's split in
    chunks to prevent it from being lost

    Args:
      record: an instance of logging.LogRecord
    """
    message = str(record.msg)


    max_message_size = 256000
    if len(message) <= max_message_size or six.PY2:
      super(SplitFileHandler, self).emit(record)
    else:
      chunks = [
          message[i:i + max_message_size]
          for i in range(0, len(message), max_message_size)
      ]

      for idx, chunk in enumerate(chunks):
        record.msg = 'Part {}/{}: {}'.format(str(idx + 1), len(chunks), chunk)
        super().emit(record)


def InitializeFileLogging(log_path, clear_logging_handlers,
                          custom_json_formatter=None):
  """Helper called from CreateAndRunService() to set up syslog logging."""




  logging.basicConfig()

  logger = logging.getLogger()

  if clear_logging_handlers:



    if len(logger.handlers) > 1:
      logger.warning(
          'Removing more than one logging handler. '
          'This implies that a user-added logging handler is being removed!')
    logger.handlers[:] = []





  file_handler = SplitFileHandler(log_path)
  json_formatter = custom_json_formatter or JsonFormatter()
  file_handler.setFormatter(json_formatter)
  logger.addHandler(file_handler)

  logger.setLevel(logging.DEBUG)


class SecurityTicketThreadHook(thread_hooks.ThreadHook):
  """Sets and clears UseRequestSecurityTicket on a thread."""

  def PreTarget(self):
    default_api_stub.DefaultApiStub.SetUseRequestSecurityTicketForThread(True)

  def PostTarget(self):
    default_api_stub.DefaultApiStub.SetUseRequestSecurityTicketForThread(False)


@functools.lru_cache(maxsize=None)
def InitializeThreadingApis():
  """Helper to monkey-patch various threading APIs."""


  thread_hooks.PatchStartNewThread(hooks=[
      SecurityTicketThreadHook, thread_hooks.RequestEnvironmentThreadHook
  ])
