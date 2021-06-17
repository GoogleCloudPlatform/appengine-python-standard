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
"""Get the App Engine app ID from environment.

Not to be confused with google.appengine.api.app_identity.get_application_id()
which gets a "display" app ID.
"""






import os
from typing import MutableMapping, Text, Union


OsEnvironLike = Union[MutableMapping[Text, Text], None]


def get(environ: OsEnvironLike = None) -> str:
  """Get the application ID from the environment.

  Args:
    environ: Environment dictionary; os.environ if None.

  Returns:
    Default application ID as a string.

  We read from the environment APPLICATION_ID (deprecated) or else
  GAE_APPLICATION.
  """

  if environ is None:
    environ = os.environ

  return environ.get('APPLICATION_ID', environ.get('GAE_APPLICATION', ''))


def put(app_id: str, environ: OsEnvironLike = None):
  """Set the application ID in the environment.

  Args:
    app_id: application ID as a string.
    environ: Environment dictionary; os.environ if None.
  """

  if environ is None:
    environ = os.environ

  environ['APPLICATION_ID'] = app_id
  environ['GAE_APPLICATION'] = app_id


def normalize(environ: OsEnvironLike = None):
  """Normalize the environment variables which set the app ID."""

  put(get(environ=environ), environ=environ)


def clear(environ: OsEnvironLike = None):
  """Unset the application ID in the environment.

  Args:
    environ: Environment dictionary; os.environ if None.
  """

  if environ is None:
    environ = os.environ

  environ.pop('APPLICATION_ID', None)
  environ.pop('GAE_APPLICATION', None)
