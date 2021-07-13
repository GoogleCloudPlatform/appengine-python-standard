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


"""Base class useful for testing with API stubs."""



import os
import shutil

from absl import flags
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore_file_stub
from google.appengine.api import full_app_id
from google.appengine.api.blobstore import blobstore_stub
from google.appengine.api.blobstore import file_blob_storage
from google.appengine.api.taskqueue import taskqueue_stub
from google.appengine.datastore import cloud_datastore_v1_remote_stub
from google.appengine.datastore import cloud_datastore_v1_stub
from google.appengine.datastore import datastore_pbs
from google.appengine.datastore import datastore_v4_stub






FLAGS = flags.FLAGS

flags.DEFINE_boolean("use_sqlite", False,
                     "uses the sqlite based datastore stub")

_CLOUD_DATASTORE_ENABLED = datastore_pbs._CLOUD_DATASTORE_ENABLED

_emulator_factory = None


class APITest(object):
  """Base class useful for configuring various API stubs."""

  __apiproxy_initialized = False

  def ResetApiProxyStubMap(self, force=False):
    """Reset the proxy stub-map.

    Args:
      force: When True, always reset the stubs regardless of their status.

    Must be called before stubs can be configured.

    Every time a new test is created, it is necessary to run with a brand new
    stub.  The problem is that RegisterStub won't allow stubs to be replaced.
    If the global instance is not reset, it raises an exception when a run a
    new test gets run that wants to use a new stub.

    Calling this method more than once per APITest instance will only cause
    a new stub-map to be created once.  Therefore it is called automatically
    during each Configure method.
    """
    if self.__apiproxy_initialized and not force:
      return
    self.__apiproxy_initialized = True
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.GetDefaultAPIProxy()

  def ConfigureDatastore(self, app_id='app', **kwargs):
    """Configure datastore stub for test.

    Configure datastore stubs for tests.  Will delete old datastore file and
    history if they already exist.

    Args:
      app_id: App id to assign to datastore stub.
      kwargs: Extra keyword parameters for the DatastoreStub constructor.
    """

    full_app_id.put(app_id)


    self.datastore_file = os.path.join(flags.FLAGS.test_tmpdir, 'datastore_v3')
    self.datastore_history_file = os.path.join(flags.FLAGS.test_tmpdir,
                                               'history')
    for filename in [self.datastore_file, self.datastore_history_file]:
      if os.access(filename, os.F_OK):
        os.remove(filename)

    if flags.FLAGS.use_sqlite:




      raise NotImplementedError('datastore_sqlite_stub not supported')
    else:

      self.datastore_stub = datastore_file_stub.DatastoreFileStub(
          app_id, None, **kwargs)

    self.datastore_v4_stub = datastore_v4_stub.DatastoreV4Stub(app_id)

    if _CLOUD_DATASTORE_ENABLED:
      self.cloud_datastore_v1_stub = (
          cloud_datastore_v1_stub.CloudDatastoreV1Stub(app_id))


    self.ResetApiProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', self.datastore_stub)
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v4',
                                            self.datastore_v4_stub)
    if _CLOUD_DATASTORE_ENABLED:
      helper = datastore_pbs.googledatastore.helper
      disable_cred_env = helper._DATASTORE_USE_STUB_CREDENTIAL_FOR_TEST_ENV
      os.environ[disable_cred_env] = 'True'
      apiproxy_stub_map.apiproxy.RegisterStub('cloud_datastore_v1',
                                              self.cloud_datastore_v1_stub)

  def _ConfigureRemoteCloudDatastore(self, app_id='app'):
    """Configure a separate process to run a Cloud Datastore emulator.

    This emulator will run as a separate process.

    Args:
      app_id: Application id to connect to.
    Raises:
      ValueError: If Cloud Datastore or gcd are not provided to the test target.
    """
    if not _CLOUD_DATASTORE_ENABLED:
      raise ValueError(datastore_pbs.MISSING_CLOUD_DATASTORE_MESSAGE)
    full_app_id.put(app_id)
    global _emulator_factory

    if _emulator_factory is None:

      from googledatastore import datastore_emulator_google as datastore_emulator
      _emulator_factory = datastore_emulator.DatastoreEmulatorGoogle3Factory()

    project_id = datastore_pbs.IdResolver([app_id]).resolve_project_id(app_id)
    emulator = _emulator_factory.Get(project_id)
    emulator.Clear()


    self.cloud_datastore_v1_stub = (
        cloud_datastore_v1_remote_stub.CloudDatastoreV1RemoteStub(
            emulator.GetDatastore()))

    self.ResetApiProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub('cloud_datastore_v1',
                                            self.cloud_datastore_v1_stub)


  def ConfigureBlobstore(self, app_id='app'):
    """Configure blobstore stub for test.

    Configure blobstore with blob-storage for tests.  Will delete old blobstore
    directory if it already exists.

    Args:
      app_id: App id to assign to datastore stub.
    """

    storage_directory = os.path.join(flags.FLAGS.test_tmpdir, 'blob_storage')
    if os.access(storage_directory, os.F_OK):
      shutil.rmtree(storage_directory)

    blob_storage = file_blob_storage.FileBlobStorage(storage_directory,
                                                     app_id)
    self.blobstore_stub = blobstore_stub.BlobstoreServiceStub(blob_storage)


    self.ResetApiProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub('blobstore', self.blobstore_stub)

  def ConfigureTaskQueue(self, root_path=None):
    """Configure task-queue stub for test.

    Args:
      app_id: App id to assign to task-queue stub.
      root_path: Root path where queue.yaml is found.  If None, will not use
        queue.yaml.
    """
    self.taskqueue_stub = taskqueue_stub.TaskQueueServiceStub(
        root_path=root_path)


    self.ResetApiProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub('taskqueue', self.taskqueue_stub)
