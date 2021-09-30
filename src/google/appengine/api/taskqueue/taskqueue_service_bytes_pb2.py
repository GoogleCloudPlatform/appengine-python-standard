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



"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database


_sym_db = _symbol_database.Default()


from google.appengine.datastore import datastore_v3_bytes_pb2 as google_dot_appengine_dot_datastore_dot_datastore__v3__bytes__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/appengine/api/taskqueue/taskqueue_service_bytes.proto',
  package='apphosting_bytes',
  syntax='proto2',
  serialized_options=b'\n\"com.google.appengine.api.taskqueueB\013TaskQueuePb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n<google/appengine/api/taskqueue/taskqueue_service_bytes.proto\x12\x10\x61pphosting_bytes\x1a\x33google/appengine/datastore/datastore_v3_bytes.proto\"\xa0\n\n\x15TaskQueueServiceError\"\x86\n\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x11\n\rUNKNOWN_QUEUE\x10\x01\x12\x13\n\x0fTRANSIENT_ERROR\x10\x02\x12\x12\n\x0eINTERNAL_ERROR\x10\x03\x12\x12\n\x0eTASK_TOO_LARGE\x10\x04\x12\x15\n\x11INVALID_TASK_NAME\x10\x05\x12\x16\n\x12INVALID_QUEUE_NAME\x10\x06\x12\x0f\n\x0bINVALID_URL\x10\x07\x12\x16\n\x12INVALID_QUEUE_RATE\x10\x08\x12\x15\n\x11PERMISSION_DENIED\x10\t\x12\x17\n\x13TASK_ALREADY_EXISTS\x10\n\x12\x13\n\x0fTOMBSTONED_TASK\x10\x0b\x12\x0f\n\x0bINVALID_ETA\x10\x0c\x12\x13\n\x0fINVALID_REQUEST\x10\r\x12\x10\n\x0cUNKNOWN_TASK\x10\x0e\x12\x14\n\x10TOMBSTONED_QUEUE\x10\x0f\x12\x17\n\x13\x44UPLICATE_TASK_NAME\x10\x10\x12\x0b\n\x07SKIPPED\x10\x11\x12\x12\n\x0eTOO_MANY_TASKS\x10\x12\x12\x13\n\x0fINVALID_PAYLOAD\x10\x13\x12\x1c\n\x18INVALID_RETRY_PARAMETERS\x10\x14\x12\x16\n\x12INVALID_QUEUE_MODE\x10\x15\x12\x14\n\x10\x41\x43L_LOOKUP_ERROR\x10\x16\x12#\n\x1fTRANSACTIONAL_REQUEST_TOO_LARGE\x10\x17\x12\x1a\n\x16INCORRECT_CREATOR_NAME\x10\x18\x12\x16\n\x12TASK_LEASE_EXPIRED\x10\x19\x12\x10\n\x0cQUEUE_PAUSED\x10\x1a\x12\x0f\n\x0bINVALID_TAG\x10\x1b\x12\x1a\n\x16INVALID_LOGGING_CONFIG\x10\x1c\x12\x1d\n\x19INVALID_DISPATCH_DEADLINE\x10\x1d\x12\x14\n\x0f\x44\x41TASTORE_ERROR\x10\x90N\x12\x1a\n\x15\x44\x41TASTORE_BAD_REQUEST\x10\x91N\x12%\n DATASTORE_CONCURRENT_TRANSACTION\x10\x92N\x12\x1d\n\x18\x44\x41TASTORE_INTERNAL_ERROR\x10\x93N\x12\x19\n\x14\x44\x41TASTORE_NEED_INDEX\x10\x94N\x12\x16\n\x11\x44\x41TASTORE_TIMEOUT\x10\x95N\x12 \n\x1b\x44\x41TASTORE_PERMISSION_DENIED\x10\x96N\x12\x1d\n\x18\x44\x41TASTORE_BIGTABLE_ERROR\x10\x97N\x12+\n&DATASTORE_COMMITTED_BUT_STILL_APPLYING\x10\x98N\x12\"\n\x1d\x44\x41TASTORE_CAPABILITY_DISABLED\x10\x99N\x12$\n\x1f\x44\x41TASTORE_TRY_ALTERNATE_BACKEND\x10\x9aN\x12 \n\x1b\x44\x41TASTORE_SAFE_TIME_TOO_OLD\x10\x9bN\x12!\n\x1c\x44\x41TASTORE_RESOURCE_EXHAUSTED\x10\x9cN\x12\x18\n\x13\x44\x41TASTORE_NOT_FOUND\x10\x9dN\x12\x1d\n\x18\x44\x41TASTORE_ALREADY_EXISTS\x10\x9eN\x12\"\n\x1d\x44\x41TASTORE_FAILED_PRECONDITION\x10\x9fN\x12\x1e\n\x19\x44\x41TASTORE_UNAUTHENTICATED\x10\xa0N\x12\x16\n\x11\x44\x41TASTORE_ABORTED\x10\xa1N\x12\'\n\"DATASTORE_SNAPSHOT_VERSION_TOO_OLD\x10\xa2N\"\x1b\n\x0bTaskPayload*\x08\x08\n\x10\xff\xff\xff\xff\x07:\x02\x08\x01\"\x9e\x01\n\x18TaskQueueRetryParameters\x12\x13\n\x0bretry_limit\x18\x01 \x01(\x05\x12\x15\n\rage_limit_sec\x18\x02 \x01(\x03\x12\x1c\n\x0fmin_backoff_sec\x18\x03 \x01(\x01:\x03\x30.1\x12\x1d\n\x0fmax_backoff_sec\x18\x04 \x01(\x01:\x04\x33\x36\x30\x30\x12\x19\n\rmax_doublings\x18\x05 \x01(\x05:\x02\x31\x36\"8\n\x0cTaskQueueAcl\x12\x12\n\nuser_email\x18\x01 \x03(\x0c\x12\x14\n\x0cwriter_email\x18\x02 \x03(\x0c\"1\n\x13TaskQueueHttpHeader\x12\x0b\n\x03key\x18\x01 \x02(\x0c\x12\r\n\x05value\x18\x02 \x02(\x0c\"+\n\rTaskQueueMode\"\x1a\n\x04Mode\x12\x08\n\x04PUSH\x10\x00\x12\x08\n\x04PULL\x10\x01\"\x87\x07\n\x13TaskQueueAddRequest\x12\x12\n\nqueue_name\x18\x01 \x02(\x0c\x12\x11\n\ttask_name\x18\x02 \x02(\x0c\x12\x10\n\x08\x65ta_usec\x18\x03 \x02(\x03\x12I\n\x06method\x18\x05 \x01(\x0e\x32\x33.apphosting_bytes.TaskQueueAddRequest.RequestMethod:\x04POST\x12\x0b\n\x03url\x18\x04 \x01(\x0c\x12<\n\x06header\x18\x06 \x03(\n2,.apphosting_bytes.TaskQueueAddRequest.Header\x12\x10\n\x04\x62ody\x18\t \x01(\x0c\x42\x02\x08\x01\x12?\n\x0btransaction\x18\n \x01(\x0b\x32*.apphosting_datastore_v3_bytes.Transaction\x12\x1d\n\x15\x64\x61tastore_transaction\x18\x15 \x01(\x0c\x12\x0e\n\x06\x61pp_id\x18\x0b \x01(\x0c\x12J\n\rcrontimetable\x18\x0c \x01(\n23.apphosting_bytes.TaskQueueAddRequest.CronTimetable\x12\x13\n\x0b\x64\x65scription\x18\x0f \x01(\x0c\x12.\n\x07payload\x18\x10 \x01(\x0b\x32\x1d.apphosting_bytes.TaskPayload\x12\x44\n\x10retry_parameters\x18\x11 \x01(\x0b\x32*.apphosting_bytes.TaskQueueRetryParameters\x12\x32\n\x04mode\x18\x12 \x01(\x0e\x32$.apphosting_bytes.TaskQueueMode.Mode\x12\x0b\n\x03tag\x18\x13 \x01(\x0c\x12I\n\x15\x63ron_retry_parameters\x18\x14 \x01(\x0b\x32*.apphosting_bytes.TaskQueueRetryParameters\x12\x1e\n\x16\x64ispatch_deadline_usec\x18\x16 \x01(\x03\x1a$\n\x06Header\x12\x0b\n\x03key\x18\x07 \x02(\x0c\x12\r\n\x05value\x18\x08 \x02(\x0c\x1a\x33\n\rCronTimetable\x12\x10\n\x08schedule\x18\r \x02(\x0c\x12\x10\n\x08timezone\x18\x0e \x02(\x0c\"A\n\rRequestMethod\x12\x07\n\x03GET\x10\x01\x12\x08\n\x04POST\x10\x02\x12\x08\n\x04HEAD\x10\x03\x12\x07\n\x03PUT\x10\x04\x12\n\n\x06\x44\x45LETE\x10\x05\"0\n\x14TaskQueueAddResponse\x12\x18\n\x10\x63hosen_task_name\x18\x01 \x01(\x0c\"U\n\x17TaskQueueBulkAddRequest\x12:\n\x0b\x61\x64\x64_request\x18\x01 \x03(\x0b\x32%.apphosting_bytes.TaskQueueAddRequest\"\xd0\x01\n\x18TaskQueueBulkAddResponse\x12I\n\ntaskresult\x18\x01 \x03(\n25.apphosting_bytes.TaskQueueBulkAddResponse.TaskResult\x1ai\n\nTaskResult\x12\x41\n\x06result\x18\x02 \x02(\x0e\x32\x31.apphosting_bytes.TaskQueueServiceError.ErrorCode\x12\x18\n\x10\x63hosen_task_name\x18\x03 \x01(\x0c\"O\n\x16TaskQueueDeleteRequest\x12\x12\n\nqueue_name\x18\x01 \x02(\x0c\x12\x11\n\ttask_name\x18\x02 \x03(\x0c\x12\x0e\n\x06\x61pp_id\x18\x03 \x01(\x0c\"\\\n\x17TaskQueueDeleteResponse\x12\x41\n\x06result\x18\x03 \x03(\x0e\x32\x31.apphosting_bytes.TaskQueueServiceError.ErrorCode\"Q\n\x18TaskQueueForceRunRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\x0c\x12\x12\n\nqueue_name\x18\x02 \x02(\x0c\x12\x11\n\ttask_name\x18\x03 \x02(\x0c\"^\n\x19TaskQueueForceRunResponse\x12\x41\n\x06result\x18\x03 \x02(\x0e\x32\x31.apphosting_bytes.TaskQueueServiceError.ErrorCode\"\xa1\x03\n\x1bTaskQueueUpdateQueueRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\x0c\x12\x12\n\nqueue_name\x18\x02 \x02(\x0c\x12 \n\x18\x62ucket_refill_per_second\x18\x03 \x02(\x01\x12\x17\n\x0f\x62ucket_capacity\x18\x04 \x02(\x05\x12\x1b\n\x13user_specified_rate\x18\x05 \x01(\t\x12\x44\n\x10retry_parameters\x18\x06 \x01(\x0b\x32*.apphosting_bytes.TaskQueueRetryParameters\x12\x1f\n\x17max_concurrent_requests\x18\x07 \x01(\x05\x12\x32\n\x04mode\x18\x08 \x01(\x0e\x32$.apphosting_bytes.TaskQueueMode.Mode\x12+\n\x03\x61\x63l\x18\t \x01(\x0b\x32\x1e.apphosting_bytes.TaskQueueAcl\x12>\n\x0fheader_override\x18\n \x03(\x0b\x32%.apphosting_bytes.TaskQueueHttpHeader\"\x1e\n\x1cTaskQueueUpdateQueueResponse\"?\n\x1bTaskQueueFetchQueuesRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\x0c\x12\x10\n\x08max_rows\x18\x02 \x02(\x05\"\x97\x04\n\x1cTaskQueueFetchQueuesResponse\x12\x43\n\x05queue\x18\x01 \x03(\n24.apphosting_bytes.TaskQueueFetchQueuesResponse.Queue\x1a\xb1\x03\n\x05Queue\x12\x12\n\nqueue_name\x18\x02 \x02(\x0c\x12 \n\x18\x62ucket_refill_per_second\x18\x03 \x02(\x01\x12\x17\n\x0f\x62ucket_capacity\x18\x04 \x02(\x01\x12\x1b\n\x13user_specified_rate\x18\x05 \x01(\t\x12\x0e\n\x06paused\x18\x06 \x02(\x08\x12\x44\n\x10retry_parameters\x18\x07 \x01(\x0b\x32*.apphosting_bytes.TaskQueueRetryParameters\x12\x1f\n\x17max_concurrent_requests\x18\x08 \x01(\x05\x12\x32\n\x04mode\x18\t \x01(\x0e\x32$.apphosting_bytes.TaskQueueMode.Mode\x12+\n\x03\x61\x63l\x18\n \x01(\x0b\x32\x1e.apphosting_bytes.TaskQueueAcl\x12>\n\x0fheader_override\x18\x0b \x03(\x0b\x32%.apphosting_bytes.TaskQueueHttpHeader\x12$\n\x0c\x63reator_name\x18\x0c \x01(\t:\napphostingB\x02\x08\x01\"\\\n\x1fTaskQueueFetchQueueStatsRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\x0c\x12\x12\n\nqueue_name\x18\x02 \x03(\x0c\x12\x15\n\rmax_num_tasks\x18\x03 \x01(\x05\"\xab\x01\n\x19TaskQueueScannerQueueInfo\x12\x1c\n\x14\x65xecuted_last_minute\x18\x01 \x02(\x03\x12\x1a\n\x12\x65xecuted_last_hour\x18\x02 \x02(\x03\x12!\n\x19sampling_duration_seconds\x18\x03 \x02(\x01\x12\x1a\n\x12requests_in_flight\x18\x04 \x01(\x05\x12\x15\n\renforced_rate\x18\x05 \x01(\x01\"\xf2\x01\n TaskQueueFetchQueueStatsResponse\x12Q\n\nqueuestats\x18\x01 \x03(\n2=.apphosting_bytes.TaskQueueFetchQueueStatsResponse.QueueStats\x1a{\n\nQueueStats\x12\x11\n\tnum_tasks\x18\x02 \x02(\x05\x12\x17\n\x0foldest_eta_usec\x18\x03 \x02(\x03\x12\x41\n\x0cscanner_info\x18\x04 \x01(\x0b\x32+.apphosting_bytes.TaskQueueScannerQueueInfo\"O\n\x1aTaskQueuePauseQueueRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x02(\x0c\x12\x12\n\nqueue_name\x18\x02 \x02(\x0c\x12\r\n\x05pause\x18\x03 \x02(\x08\"\x1d\n\x1bTaskQueuePauseQueueResponse\"@\n\x1aTaskQueuePurgeQueueRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\x0c\x12\x12\n\nqueue_name\x18\x02 \x02(\x0c\"\x1d\n\x1bTaskQueuePurgeQueueResponse\"A\n\x1bTaskQueueDeleteQueueRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x02(\x0c\x12\x12\n\nqueue_name\x18\x02 \x02(\x0c\"\x1e\n\x1cTaskQueueDeleteQueueResponse\"-\n\x1bTaskQueueDeleteGroupRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x02(\x0c\"\x1e\n\x1cTaskQueueDeleteGroupResponse\"\x99\x01\n\x1aTaskQueueQueryTasksRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\x0c\x12\x12\n\nqueue_name\x18\x02 \x02(\x0c\x12\x17\n\x0fstart_task_name\x18\x03 \x01(\x0c\x12\x16\n\x0estart_eta_usec\x18\x04 \x01(\x03\x12\x11\n\tstart_tag\x18\x06 \x01(\x0c\x12\x13\n\x08max_rows\x18\x05 \x01(\x05:\x01\x31\"\xb0\x08\n\x1bTaskQueueQueryTasksResponse\x12@\n\x04task\x18\x01 \x03(\n22.apphosting_bytes.TaskQueueQueryTasksResponse.Task\x1a\xce\x07\n\x04Task\x12\x11\n\ttask_name\x18\x02 \x02(\x0c\x12\x10\n\x08\x65ta_usec\x18\x03 \x02(\x03\x12\x0b\n\x03url\x18\x04 \x01(\x0c\x12P\n\x06method\x18\x05 \x01(\x0e\x32@.apphosting_bytes.TaskQueueQueryTasksResponse.Task.RequestMethod\x12\x13\n\x0bretry_count\x18\x06 \x01(\x05\x12I\n\x06header\x18\x07 \x03(\n29.apphosting_bytes.TaskQueueQueryTasksResponse.Task.Header\x12\x11\n\tbody_size\x18\n \x01(\x05\x12\x10\n\x04\x62ody\x18\x0b \x01(\x0c\x42\x02\x08\x01\x12\x1a\n\x12\x63reation_time_usec\x18\x0c \x02(\x03\x12W\n\rcrontimetable\x18\r \x01(\n2@.apphosting_bytes.TaskQueueQueryTasksResponse.Task.CronTimetable\x12I\n\x06runlog\x18\x10 \x01(\n29.apphosting_bytes.TaskQueueQueryTasksResponse.Task.RunLog\x12\x13\n\x0b\x64\x65scription\x18\x15 \x01(\x0c\x12.\n\x07payload\x18\x16 \x01(\x0b\x32\x1d.apphosting_bytes.TaskPayload\x12\x44\n\x10retry_parameters\x18\x17 \x01(\x0b\x32*.apphosting_bytes.TaskQueueRetryParameters\x12\x16\n\x0e\x66irst_try_usec\x18\x18 \x01(\x03\x12\x0b\n\x03tag\x18\x19 \x01(\x0c\x12\x17\n\x0f\x65xecution_count\x18\x1a \x01(\x05\x12\x1e\n\x16\x64ispatch_deadline_usec\x18\x1c \x01(\x03\x1a$\n\x06Header\x12\x0b\n\x03key\x18\x08 \x02(\x0c\x12\r\n\x05value\x18\t \x02(\x0c\x1a\x33\n\rCronTimetable\x12\x10\n\x08schedule\x18\x0e \x02(\x0c\x12\x10\n\x08timezone\x18\x0f \x02(\x0c\x1av\n\x06RunLog\x12\x17\n\x0f\x64ispatched_usec\x18\x11 \x02(\x03\x12\x10\n\x08lag_usec\x18\x12 \x02(\x03\x12\x14\n\x0c\x65lapsed_usec\x18\x13 \x02(\x03\x12\x15\n\rresponse_code\x18\x14 \x01(\x03\x12\x14\n\x0cretry_reason\x18\x1b \x01(\t\"A\n\rRequestMethod\x12\x07\n\x03GET\x10\x01\x12\x08\n\x04POST\x10\x02\x12\x08\n\x04HEAD\x10\x03\x12\x07\n\x03PUT\x10\x04\x12\n\n\x06\x44\x45LETE\x10\x05\"R\n\x19TaskQueueFetchTaskRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\x0c\x12\x12\n\nqueue_name\x18\x02 \x02(\x0c\x12\x11\n\ttask_name\x18\x03 \x02(\x0c\"Y\n\x1aTaskQueueFetchTaskResponse\x12;\n\x04task\x18\x01 \x02(\x0b\x32-.apphosting_bytes.TaskQueueQueryTasksResponse\"C\n\"TaskQueueUpdateStorageLimitRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x02(\x0c\x12\r\n\x05limit\x18\x02 \x02(\x03\"8\n#TaskQueueUpdateStorageLimitResponse\x12\x11\n\tnew_limit\x18\x01 \x02(\x03\"\x83\x01\n TaskQueueQueryAndOwnTasksRequest\x12\x12\n\nqueue_name\x18\x01 \x02(\x0c\x12\x15\n\rlease_seconds\x18\x02 \x02(\x01\x12\x11\n\tmax_tasks\x18\x03 \x02(\x03\x12\x14\n\x0cgroup_by_tag\x18\x04 \x01(\x08\x12\x0b\n\x03tag\x18\x05 \x01(\x0c\"\xcc\x01\n!TaskQueueQueryAndOwnTasksResponse\x12\x46\n\x04task\x18\x01 \x03(\n28.apphosting_bytes.TaskQueueQueryAndOwnTasksResponse.Task\x1a_\n\x04Task\x12\x11\n\ttask_name\x18\x02 \x02(\x0c\x12\x10\n\x08\x65ta_usec\x18\x03 \x02(\x03\x12\x13\n\x0bretry_count\x18\x04 \x01(\x05\x12\x10\n\x04\x62ody\x18\x05 \x01(\x0c\x42\x02\x08\x01\x12\x0b\n\x03tag\x18\x06 \x01(\x0c\"q\n\x1fTaskQueueModifyTaskLeaseRequest\x12\x12\n\nqueue_name\x18\x01 \x02(\x0c\x12\x11\n\ttask_name\x18\x02 \x02(\x0c\x12\x10\n\x08\x65ta_usec\x18\x03 \x02(\x03\x12\x15\n\rlease_seconds\x18\x04 \x02(\x01\"<\n TaskQueueModifyTaskLeaseResponse\x12\x18\n\x10updated_eta_usec\x18\x01 \x02(\x03\x42\x31\n\"com.google.appengine.api.taskqueueB\x0bTaskQueuePb'
  ,
  dependencies=[google_dot_appengine_dot_datastore_dot_datastore__v3__bytes__pb2.DESCRIPTOR,])



_TASKQUEUESERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='apphosting_bytes.TaskQueueServiceError.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_QUEUE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRANSIENT_ERROR', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INTERNAL_ERROR', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TASK_TOO_LARGE', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_TASK_NAME', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_QUEUE_NAME', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_URL', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_QUEUE_RATE', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PERMISSION_DENIED', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TASK_ALREADY_EXISTS', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TOMBSTONED_TASK', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_ETA', index=12, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_REQUEST', index=13, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_TASK', index=14, number=14,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TOMBSTONED_QUEUE', index=15, number=15,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DUPLICATE_TASK_NAME', index=16, number=16,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SKIPPED', index=17, number=17,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TOO_MANY_TASKS', index=18, number=18,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_PAYLOAD', index=19, number=19,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_RETRY_PARAMETERS', index=20, number=20,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_QUEUE_MODE', index=21, number=21,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ACL_LOOKUP_ERROR', index=22, number=22,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRANSACTIONAL_REQUEST_TOO_LARGE', index=23, number=23,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INCORRECT_CREATOR_NAME', index=24, number=24,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TASK_LEASE_EXPIRED', index=25, number=25,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='QUEUE_PAUSED', index=26, number=26,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_TAG', index=27, number=27,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_LOGGING_CONFIG', index=28, number=28,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INVALID_DISPATCH_DEADLINE', index=29, number=29,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_ERROR', index=30, number=10000,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_BAD_REQUEST', index=31, number=10001,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_CONCURRENT_TRANSACTION', index=32, number=10002,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_INTERNAL_ERROR', index=33, number=10003,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_NEED_INDEX', index=34, number=10004,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_TIMEOUT', index=35, number=10005,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_PERMISSION_DENIED', index=36, number=10006,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_BIGTABLE_ERROR', index=37, number=10007,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_COMMITTED_BUT_STILL_APPLYING', index=38, number=10008,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_CAPABILITY_DISABLED', index=39, number=10009,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_TRY_ALTERNATE_BACKEND', index=40, number=10010,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_SAFE_TIME_TOO_OLD', index=41, number=10011,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_RESOURCE_EXHAUSTED', index=42, number=10012,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_NOT_FOUND', index=43, number=10013,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_ALREADY_EXISTS', index=44, number=10014,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_FAILED_PRECONDITION', index=45, number=10015,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_UNAUTHENTICATED', index=46, number=10016,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_ABORTED', index=47, number=10017,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DATASTORE_SNAPSHOT_VERSION_TOO_OLD', index=48, number=10018,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=162,
  serialized_end=1448,
)
_sym_db.RegisterEnumDescriptor(_TASKQUEUESERVICEERROR_ERRORCODE)

_TASKQUEUEMODE_MODE = _descriptor.EnumDescriptor(
  name='Mode',
  full_name='apphosting_bytes.TaskQueueMode.Mode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PUSH', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PULL', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1766,
  serialized_end=1792,
)
_sym_db.RegisterEnumDescriptor(_TASKQUEUEMODE_MODE)

_TASKQUEUEADDREQUEST_REQUESTMETHOD = _descriptor.EnumDescriptor(
  name='RequestMethod',
  full_name='apphosting_bytes.TaskQueueAddRequest.RequestMethod',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GET', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='POST', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HEAD', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PUT', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DELETE', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2633,
  serialized_end=2698,
)
_sym_db.RegisterEnumDescriptor(_TASKQUEUEADDREQUEST_REQUESTMETHOD)

_TASKQUEUEQUERYTASKSRESPONSE_TASK_REQUESTMETHOD = _descriptor.EnumDescriptor(
  name='RequestMethod',
  full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.RequestMethod',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GET', index=0, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='POST', index=1, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HEAD', index=2, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PUT', index=3, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DELETE', index=4, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=2633,
  serialized_end=2698,
)
_sym_db.RegisterEnumDescriptor(_TASKQUEUEQUERYTASKSRESPONSE_TASK_REQUESTMETHOD)


_TASKQUEUESERVICEERROR = _descriptor.Descriptor(
  name='TaskQueueServiceError',
  full_name='apphosting_bytes.TaskQueueServiceError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TASKQUEUESERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=136,
  serialized_end=1448,
)


_TASKPAYLOAD = _descriptor.Descriptor(
  name='TaskPayload',
  full_name='apphosting_bytes.TaskPayload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'\010\001',
  is_extendable=True,
  syntax='proto2',
  extension_ranges=[(10, 2147483647), ],
  oneofs=[
  ],
  serialized_start=1450,
  serialized_end=1477,
)


_TASKQUEUERETRYPARAMETERS = _descriptor.Descriptor(
  name='TaskQueueRetryParameters',
  full_name='apphosting_bytes.TaskQueueRetryParameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='retry_limit', full_name='apphosting_bytes.TaskQueueRetryParameters.retry_limit', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='age_limit_sec', full_name='apphosting_bytes.TaskQueueRetryParameters.age_limit_sec', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='min_backoff_sec', full_name='apphosting_bytes.TaskQueueRetryParameters.min_backoff_sec', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_backoff_sec', full_name='apphosting_bytes.TaskQueueRetryParameters.max_backoff_sec', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(3600),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_doublings', full_name='apphosting_bytes.TaskQueueRetryParameters.max_doublings', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=16,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1480,
  serialized_end=1638,
)


_TASKQUEUEACL = _descriptor.Descriptor(
  name='TaskQueueAcl',
  full_name='apphosting_bytes.TaskQueueAcl',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_email', full_name='apphosting_bytes.TaskQueueAcl.user_email', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='writer_email', full_name='apphosting_bytes.TaskQueueAcl.writer_email', index=1,
      number=2, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1640,
  serialized_end=1696,
)


_TASKQUEUEHTTPHEADER = _descriptor.Descriptor(
  name='TaskQueueHttpHeader',
  full_name='apphosting_bytes.TaskQueueHttpHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='apphosting_bytes.TaskQueueHttpHeader.key', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='apphosting_bytes.TaskQueueHttpHeader.value', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1698,
  serialized_end=1747,
)


_TASKQUEUEMODE = _descriptor.Descriptor(
  name='TaskQueueMode',
  full_name='apphosting_bytes.TaskQueueMode',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TASKQUEUEMODE_MODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1749,
  serialized_end=1792,
)


_TASKQUEUEADDREQUEST_HEADER = _descriptor.Descriptor(
  name='Header',
  full_name='apphosting_bytes.TaskQueueAddRequest.Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='apphosting_bytes.TaskQueueAddRequest.Header.key', index=0,
      number=7, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='apphosting_bytes.TaskQueueAddRequest.Header.value', index=1,
      number=8, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2542,
  serialized_end=2578,
)

_TASKQUEUEADDREQUEST_CRONTIMETABLE = _descriptor.Descriptor(
  name='CronTimetable',
  full_name='apphosting_bytes.TaskQueueAddRequest.CronTimetable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='schedule', full_name='apphosting_bytes.TaskQueueAddRequest.CronTimetable.schedule', index=0,
      number=13, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timezone', full_name='apphosting_bytes.TaskQueueAddRequest.CronTimetable.timezone', index=1,
      number=14, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2580,
  serialized_end=2631,
)

_TASKQUEUEADDREQUEST = _descriptor.Descriptor(
  name='TaskQueueAddRequest',
  full_name='apphosting_bytes.TaskQueueAddRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueAddRequest.queue_name', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_name', full_name='apphosting_bytes.TaskQueueAddRequest.task_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='eta_usec', full_name='apphosting_bytes.TaskQueueAddRequest.eta_usec', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='method', full_name='apphosting_bytes.TaskQueueAddRequest.method', index=3,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='apphosting_bytes.TaskQueueAddRequest.url', index=4,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='header', full_name='apphosting_bytes.TaskQueueAddRequest.header', index=5,
      number=6, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='body', full_name='apphosting_bytes.TaskQueueAddRequest.body', index=6,
      number=9, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transaction', full_name='apphosting_bytes.TaskQueueAddRequest.transaction', index=7,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='datastore_transaction', full_name='apphosting_bytes.TaskQueueAddRequest.datastore_transaction', index=8,
      number=21, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueAddRequest.app_id', index=9,
      number=11, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crontimetable', full_name='apphosting_bytes.TaskQueueAddRequest.crontimetable', index=10,
      number=12, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='apphosting_bytes.TaskQueueAddRequest.description', index=11,
      number=15, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload', full_name='apphosting_bytes.TaskQueueAddRequest.payload', index=12,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retry_parameters', full_name='apphosting_bytes.TaskQueueAddRequest.retry_parameters', index=13,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode', full_name='apphosting_bytes.TaskQueueAddRequest.mode', index=14,
      number=18, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tag', full_name='apphosting_bytes.TaskQueueAddRequest.tag', index=15,
      number=19, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cron_retry_parameters', full_name='apphosting_bytes.TaskQueueAddRequest.cron_retry_parameters', index=16,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dispatch_deadline_usec', full_name='apphosting_bytes.TaskQueueAddRequest.dispatch_deadline_usec', index=17,
      number=22, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TASKQUEUEADDREQUEST_HEADER, _TASKQUEUEADDREQUEST_CRONTIMETABLE, ],
  enum_types=[
    _TASKQUEUEADDREQUEST_REQUESTMETHOD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1795,
  serialized_end=2698,
)


_TASKQUEUEADDRESPONSE = _descriptor.Descriptor(
  name='TaskQueueAddResponse',
  full_name='apphosting_bytes.TaskQueueAddResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='chosen_task_name', full_name='apphosting_bytes.TaskQueueAddResponse.chosen_task_name', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2700,
  serialized_end=2748,
)


_TASKQUEUEBULKADDREQUEST = _descriptor.Descriptor(
  name='TaskQueueBulkAddRequest',
  full_name='apphosting_bytes.TaskQueueBulkAddRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='add_request', full_name='apphosting_bytes.TaskQueueBulkAddRequest.add_request', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2750,
  serialized_end=2835,
)


_TASKQUEUEBULKADDRESPONSE_TASKRESULT = _descriptor.Descriptor(
  name='TaskResult',
  full_name='apphosting_bytes.TaskQueueBulkAddResponse.TaskResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='apphosting_bytes.TaskQueueBulkAddResponse.TaskResult.result', index=0,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chosen_task_name', full_name='apphosting_bytes.TaskQueueBulkAddResponse.TaskResult.chosen_task_name', index=1,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2941,
  serialized_end=3046,
)

_TASKQUEUEBULKADDRESPONSE = _descriptor.Descriptor(
  name='TaskQueueBulkAddResponse',
  full_name='apphosting_bytes.TaskQueueBulkAddResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='taskresult', full_name='apphosting_bytes.TaskQueueBulkAddResponse.taskresult', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TASKQUEUEBULKADDRESPONSE_TASKRESULT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2838,
  serialized_end=3046,
)


_TASKQUEUEDELETEREQUEST = _descriptor.Descriptor(
  name='TaskQueueDeleteRequest',
  full_name='apphosting_bytes.TaskQueueDeleteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueDeleteRequest.queue_name', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_name', full_name='apphosting_bytes.TaskQueueDeleteRequest.task_name', index=1,
      number=2, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueDeleteRequest.app_id', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3048,
  serialized_end=3127,
)


_TASKQUEUEDELETERESPONSE = _descriptor.Descriptor(
  name='TaskQueueDeleteResponse',
  full_name='apphosting_bytes.TaskQueueDeleteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='apphosting_bytes.TaskQueueDeleteResponse.result', index=0,
      number=3, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3129,
  serialized_end=3221,
)


_TASKQUEUEFORCERUNREQUEST = _descriptor.Descriptor(
  name='TaskQueueForceRunRequest',
  full_name='apphosting_bytes.TaskQueueForceRunRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueForceRunRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueForceRunRequest.queue_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_name', full_name='apphosting_bytes.TaskQueueForceRunRequest.task_name', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3223,
  serialized_end=3304,
)


_TASKQUEUEFORCERUNRESPONSE = _descriptor.Descriptor(
  name='TaskQueueForceRunResponse',
  full_name='apphosting_bytes.TaskQueueForceRunResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='apphosting_bytes.TaskQueueForceRunResponse.result', index=0,
      number=3, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3306,
  serialized_end=3400,
)


_TASKQUEUEUPDATEQUEUEREQUEST = _descriptor.Descriptor(
  name='TaskQueueUpdateQueueRequest',
  full_name='apphosting_bytes.TaskQueueUpdateQueueRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.queue_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bucket_refill_per_second', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.bucket_refill_per_second', index=2,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bucket_capacity', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.bucket_capacity', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_specified_rate', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.user_specified_rate', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retry_parameters', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.retry_parameters', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_concurrent_requests', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.max_concurrent_requests', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.mode', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acl', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.acl', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='header_override', full_name='apphosting_bytes.TaskQueueUpdateQueueRequest.header_override', index=9,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3403,
  serialized_end=3820,
)


_TASKQUEUEUPDATEQUEUERESPONSE = _descriptor.Descriptor(
  name='TaskQueueUpdateQueueResponse',
  full_name='apphosting_bytes.TaskQueueUpdateQueueResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3822,
  serialized_end=3852,
)


_TASKQUEUEFETCHQUEUESREQUEST = _descriptor.Descriptor(
  name='TaskQueueFetchQueuesRequest',
  full_name='apphosting_bytes.TaskQueueFetchQueuesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueFetchQueuesRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_rows', full_name='apphosting_bytes.TaskQueueFetchQueuesRequest.max_rows', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3854,
  serialized_end=3917,
)


_TASKQUEUEFETCHQUEUESRESPONSE_QUEUE = _descriptor.Descriptor(
  name='Queue',
  full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.queue_name', index=0,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bucket_refill_per_second', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.bucket_refill_per_second', index=1,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bucket_capacity', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.bucket_capacity', index=2,
      number=4, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_specified_rate', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.user_specified_rate', index=3,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='paused', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.paused', index=4,
      number=6, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retry_parameters', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.retry_parameters', index=5,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_concurrent_requests', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.max_concurrent_requests', index=6,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.mode', index=7,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acl', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.acl', index=8,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='header_override', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.header_override', index=9,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='creator_name', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.Queue.creator_name', index=10,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"apphosting".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4022,
  serialized_end=4455,
)

_TASKQUEUEFETCHQUEUESRESPONSE = _descriptor.Descriptor(
  name='TaskQueueFetchQueuesResponse',
  full_name='apphosting_bytes.TaskQueueFetchQueuesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='queue', full_name='apphosting_bytes.TaskQueueFetchQueuesResponse.queue', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TASKQUEUEFETCHQUEUESRESPONSE_QUEUE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=3920,
  serialized_end=4455,
)


_TASKQUEUEFETCHQUEUESTATSREQUEST = _descriptor.Descriptor(
  name='TaskQueueFetchQueueStatsRequest',
  full_name='apphosting_bytes.TaskQueueFetchQueueStatsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueFetchQueueStatsRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueFetchQueueStatsRequest.queue_name', index=1,
      number=2, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_num_tasks', full_name='apphosting_bytes.TaskQueueFetchQueueStatsRequest.max_num_tasks', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4457,
  serialized_end=4549,
)


_TASKQUEUESCANNERQUEUEINFO = _descriptor.Descriptor(
  name='TaskQueueScannerQueueInfo',
  full_name='apphosting_bytes.TaskQueueScannerQueueInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='executed_last_minute', full_name='apphosting_bytes.TaskQueueScannerQueueInfo.executed_last_minute', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='executed_last_hour', full_name='apphosting_bytes.TaskQueueScannerQueueInfo.executed_last_hour', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sampling_duration_seconds', full_name='apphosting_bytes.TaskQueueScannerQueueInfo.sampling_duration_seconds', index=2,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='requests_in_flight', full_name='apphosting_bytes.TaskQueueScannerQueueInfo.requests_in_flight', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enforced_rate', full_name='apphosting_bytes.TaskQueueScannerQueueInfo.enforced_rate', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4552,
  serialized_end=4723,
)


_TASKQUEUEFETCHQUEUESTATSRESPONSE_QUEUESTATS = _descriptor.Descriptor(
  name='QueueStats',
  full_name='apphosting_bytes.TaskQueueFetchQueueStatsResponse.QueueStats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_tasks', full_name='apphosting_bytes.TaskQueueFetchQueueStatsResponse.QueueStats.num_tasks', index=0,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='oldest_eta_usec', full_name='apphosting_bytes.TaskQueueFetchQueueStatsResponse.QueueStats.oldest_eta_usec', index=1,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scanner_info', full_name='apphosting_bytes.TaskQueueFetchQueueStatsResponse.QueueStats.scanner_info', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4845,
  serialized_end=4968,
)

_TASKQUEUEFETCHQUEUESTATSRESPONSE = _descriptor.Descriptor(
  name='TaskQueueFetchQueueStatsResponse',
  full_name='apphosting_bytes.TaskQueueFetchQueueStatsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='queuestats', full_name='apphosting_bytes.TaskQueueFetchQueueStatsResponse.queuestats', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TASKQUEUEFETCHQUEUESTATSRESPONSE_QUEUESTATS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4726,
  serialized_end=4968,
)


_TASKQUEUEPAUSEQUEUEREQUEST = _descriptor.Descriptor(
  name='TaskQueuePauseQueueRequest',
  full_name='apphosting_bytes.TaskQueuePauseQueueRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueuePauseQueueRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueuePauseQueueRequest.queue_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pause', full_name='apphosting_bytes.TaskQueuePauseQueueRequest.pause', index=2,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=4970,
  serialized_end=5049,
)


_TASKQUEUEPAUSEQUEUERESPONSE = _descriptor.Descriptor(
  name='TaskQueuePauseQueueResponse',
  full_name='apphosting_bytes.TaskQueuePauseQueueResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5051,
  serialized_end=5080,
)


_TASKQUEUEPURGEQUEUEREQUEST = _descriptor.Descriptor(
  name='TaskQueuePurgeQueueRequest',
  full_name='apphosting_bytes.TaskQueuePurgeQueueRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueuePurgeQueueRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueuePurgeQueueRequest.queue_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5082,
  serialized_end=5146,
)


_TASKQUEUEPURGEQUEUERESPONSE = _descriptor.Descriptor(
  name='TaskQueuePurgeQueueResponse',
  full_name='apphosting_bytes.TaskQueuePurgeQueueResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5148,
  serialized_end=5177,
)


_TASKQUEUEDELETEQUEUEREQUEST = _descriptor.Descriptor(
  name='TaskQueueDeleteQueueRequest',
  full_name='apphosting_bytes.TaskQueueDeleteQueueRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueDeleteQueueRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueDeleteQueueRequest.queue_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5179,
  serialized_end=5244,
)


_TASKQUEUEDELETEQUEUERESPONSE = _descriptor.Descriptor(
  name='TaskQueueDeleteQueueResponse',
  full_name='apphosting_bytes.TaskQueueDeleteQueueResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5246,
  serialized_end=5276,
)


_TASKQUEUEDELETEGROUPREQUEST = _descriptor.Descriptor(
  name='TaskQueueDeleteGroupRequest',
  full_name='apphosting_bytes.TaskQueueDeleteGroupRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueDeleteGroupRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5278,
  serialized_end=5323,
)


_TASKQUEUEDELETEGROUPRESPONSE = _descriptor.Descriptor(
  name='TaskQueueDeleteGroupResponse',
  full_name='apphosting_bytes.TaskQueueDeleteGroupResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5325,
  serialized_end=5355,
)


_TASKQUEUEQUERYTASKSREQUEST = _descriptor.Descriptor(
  name='TaskQueueQueryTasksRequest',
  full_name='apphosting_bytes.TaskQueueQueryTasksRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueQueryTasksRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueQueryTasksRequest.queue_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_task_name', full_name='apphosting_bytes.TaskQueueQueryTasksRequest.start_task_name', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_eta_usec', full_name='apphosting_bytes.TaskQueueQueryTasksRequest.start_eta_usec', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_tag', full_name='apphosting_bytes.TaskQueueQueryTasksRequest.start_tag', index=4,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_rows', full_name='apphosting_bytes.TaskQueueQueryTasksRequest.max_rows', index=5,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5358,
  serialized_end=5511,
)


_TASKQUEUEQUERYTASKSRESPONSE_TASK_HEADER = _descriptor.Descriptor(
  name='Header',
  full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.Header.key', index=0,
      number=8, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.Header.value', index=1,
      number=9, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=6310,
  serialized_end=6346,
)

_TASKQUEUEQUERYTASKSRESPONSE_TASK_CRONTIMETABLE = _descriptor.Descriptor(
  name='CronTimetable',
  full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.CronTimetable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='schedule', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.CronTimetable.schedule', index=0,
      number=14, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timezone', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.CronTimetable.timezone', index=1,
      number=15, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=6348,
  serialized_end=6399,
)

_TASKQUEUEQUERYTASKSRESPONSE_TASK_RUNLOG = _descriptor.Descriptor(
  name='RunLog',
  full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.RunLog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dispatched_usec', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.RunLog.dispatched_usec', index=0,
      number=17, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lag_usec', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.RunLog.lag_usec', index=1,
      number=18, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='elapsed_usec', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.RunLog.elapsed_usec', index=2,
      number=19, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='response_code', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.RunLog.response_code', index=3,
      number=20, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retry_reason', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.RunLog.retry_reason', index=4,
      number=27, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=6401,
  serialized_end=6519,
)

_TASKQUEUEQUERYTASKSRESPONSE_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_name', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.task_name', index=0,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='eta_usec', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.eta_usec', index=1,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.url', index=2,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='method', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.method', index=3,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retry_count', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.retry_count', index=4,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='header', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.header', index=5,
      number=7, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='body_size', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.body_size', index=6,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='body', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.body', index=7,
      number=11, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='creation_time_usec', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.creation_time_usec', index=8,
      number=12, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='crontimetable', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.crontimetable', index=9,
      number=13, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='runlog', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.runlog', index=10,
      number=16, type=10, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.description', index=11,
      number=21, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='payload', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.payload', index=12,
      number=22, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retry_parameters', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.retry_parameters', index=13,
      number=23, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='first_try_usec', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.first_try_usec', index=14,
      number=24, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tag', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.tag', index=15,
      number=25, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='execution_count', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.execution_count', index=16,
      number=26, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dispatch_deadline_usec', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.Task.dispatch_deadline_usec', index=17,
      number=28, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TASKQUEUEQUERYTASKSRESPONSE_TASK_HEADER, _TASKQUEUEQUERYTASKSRESPONSE_TASK_CRONTIMETABLE, _TASKQUEUEQUERYTASKSRESPONSE_TASK_RUNLOG, ],
  enum_types=[
    _TASKQUEUEQUERYTASKSRESPONSE_TASK_REQUESTMETHOD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5612,
  serialized_end=6586,
)

_TASKQUEUEQUERYTASKSRESPONSE = _descriptor.Descriptor(
  name='TaskQueueQueryTasksResponse',
  full_name='apphosting_bytes.TaskQueueQueryTasksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task', full_name='apphosting_bytes.TaskQueueQueryTasksResponse.task', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TASKQUEUEQUERYTASKSRESPONSE_TASK, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=5514,
  serialized_end=6586,
)


_TASKQUEUEFETCHTASKREQUEST = _descriptor.Descriptor(
  name='TaskQueueFetchTaskRequest',
  full_name='apphosting_bytes.TaskQueueFetchTaskRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueFetchTaskRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueFetchTaskRequest.queue_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_name', full_name='apphosting_bytes.TaskQueueFetchTaskRequest.task_name', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=6588,
  serialized_end=6670,
)


_TASKQUEUEFETCHTASKRESPONSE = _descriptor.Descriptor(
  name='TaskQueueFetchTaskResponse',
  full_name='apphosting_bytes.TaskQueueFetchTaskResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task', full_name='apphosting_bytes.TaskQueueFetchTaskResponse.task', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=6672,
  serialized_end=6761,
)


_TASKQUEUEUPDATESTORAGELIMITREQUEST = _descriptor.Descriptor(
  name='TaskQueueUpdateStorageLimitRequest',
  full_name='apphosting_bytes.TaskQueueUpdateStorageLimitRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='apphosting_bytes.TaskQueueUpdateStorageLimitRequest.app_id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='limit', full_name='apphosting_bytes.TaskQueueUpdateStorageLimitRequest.limit', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=6763,
  serialized_end=6830,
)


_TASKQUEUEUPDATESTORAGELIMITRESPONSE = _descriptor.Descriptor(
  name='TaskQueueUpdateStorageLimitResponse',
  full_name='apphosting_bytes.TaskQueueUpdateStorageLimitResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='new_limit', full_name='apphosting_bytes.TaskQueueUpdateStorageLimitResponse.new_limit', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=6832,
  serialized_end=6888,
)


_TASKQUEUEQUERYANDOWNTASKSREQUEST = _descriptor.Descriptor(
  name='TaskQueueQueryAndOwnTasksRequest',
  full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksRequest.queue_name', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lease_seconds', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksRequest.lease_seconds', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_tasks', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksRequest.max_tasks', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='group_by_tag', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksRequest.group_by_tag', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tag', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksRequest.tag', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=6891,
  serialized_end=7022,
)


_TASKQUEUEQUERYANDOWNTASKSRESPONSE_TASK = _descriptor.Descriptor(
  name='Task',
  full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksResponse.Task',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_name', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksResponse.Task.task_name', index=0,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='eta_usec', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksResponse.Task.eta_usec', index=1,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retry_count', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksResponse.Task.retry_count', index=2,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='body', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksResponse.Task.body', index=3,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tag', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksResponse.Task.tag', index=4,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7134,
  serialized_end=7229,
)

_TASKQUEUEQUERYANDOWNTASKSRESPONSE = _descriptor.Descriptor(
  name='TaskQueueQueryAndOwnTasksResponse',
  full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task', full_name='apphosting_bytes.TaskQueueQueryAndOwnTasksResponse.task', index=0,
      number=1, type=10, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TASKQUEUEQUERYANDOWNTASKSRESPONSE_TASK, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7025,
  serialized_end=7229,
)


_TASKQUEUEMODIFYTASKLEASEREQUEST = _descriptor.Descriptor(
  name='TaskQueueModifyTaskLeaseRequest',
  full_name='apphosting_bytes.TaskQueueModifyTaskLeaseRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='apphosting_bytes.TaskQueueModifyTaskLeaseRequest.queue_name', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='task_name', full_name='apphosting_bytes.TaskQueueModifyTaskLeaseRequest.task_name', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='eta_usec', full_name='apphosting_bytes.TaskQueueModifyTaskLeaseRequest.eta_usec', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lease_seconds', full_name='apphosting_bytes.TaskQueueModifyTaskLeaseRequest.lease_seconds', index=3,
      number=4, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7231,
  serialized_end=7344,
)


_TASKQUEUEMODIFYTASKLEASERESPONSE = _descriptor.Descriptor(
  name='TaskQueueModifyTaskLeaseResponse',
  full_name='apphosting_bytes.TaskQueueModifyTaskLeaseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='updated_eta_usec', full_name='apphosting_bytes.TaskQueueModifyTaskLeaseResponse.updated_eta_usec', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=7346,
  serialized_end=7406,
)

_TASKQUEUESERVICEERROR_ERRORCODE.containing_type = _TASKQUEUESERVICEERROR
_TASKQUEUEMODE_MODE.containing_type = _TASKQUEUEMODE
_TASKQUEUEADDREQUEST_HEADER.containing_type = _TASKQUEUEADDREQUEST
_TASKQUEUEADDREQUEST_CRONTIMETABLE.containing_type = _TASKQUEUEADDREQUEST
_TASKQUEUEADDREQUEST.fields_by_name['method'].enum_type = _TASKQUEUEADDREQUEST_REQUESTMETHOD
_TASKQUEUEADDREQUEST.fields_by_name['header'].message_type = _TASKQUEUEADDREQUEST_HEADER
_TASKQUEUEADDREQUEST.fields_by_name['transaction'].message_type = google_dot_appengine_dot_datastore_dot_datastore__v3__bytes__pb2._TRANSACTION
_TASKQUEUEADDREQUEST.fields_by_name['crontimetable'].message_type = _TASKQUEUEADDREQUEST_CRONTIMETABLE
_TASKQUEUEADDREQUEST.fields_by_name['payload'].message_type = _TASKPAYLOAD
_TASKQUEUEADDREQUEST.fields_by_name['retry_parameters'].message_type = _TASKQUEUERETRYPARAMETERS
_TASKQUEUEADDREQUEST.fields_by_name['mode'].enum_type = _TASKQUEUEMODE_MODE
_TASKQUEUEADDREQUEST.fields_by_name['cron_retry_parameters'].message_type = _TASKQUEUERETRYPARAMETERS
_TASKQUEUEADDREQUEST_REQUESTMETHOD.containing_type = _TASKQUEUEADDREQUEST
_TASKQUEUEBULKADDREQUEST.fields_by_name['add_request'].message_type = _TASKQUEUEADDREQUEST
_TASKQUEUEBULKADDRESPONSE_TASKRESULT.fields_by_name['result'].enum_type = _TASKQUEUESERVICEERROR_ERRORCODE
_TASKQUEUEBULKADDRESPONSE_TASKRESULT.containing_type = _TASKQUEUEBULKADDRESPONSE
_TASKQUEUEBULKADDRESPONSE.fields_by_name['taskresult'].message_type = _TASKQUEUEBULKADDRESPONSE_TASKRESULT
_TASKQUEUEDELETERESPONSE.fields_by_name['result'].enum_type = _TASKQUEUESERVICEERROR_ERRORCODE
_TASKQUEUEFORCERUNRESPONSE.fields_by_name['result'].enum_type = _TASKQUEUESERVICEERROR_ERRORCODE
_TASKQUEUEUPDATEQUEUEREQUEST.fields_by_name['retry_parameters'].message_type = _TASKQUEUERETRYPARAMETERS
_TASKQUEUEUPDATEQUEUEREQUEST.fields_by_name['mode'].enum_type = _TASKQUEUEMODE_MODE
_TASKQUEUEUPDATEQUEUEREQUEST.fields_by_name['acl'].message_type = _TASKQUEUEACL
_TASKQUEUEUPDATEQUEUEREQUEST.fields_by_name['header_override'].message_type = _TASKQUEUEHTTPHEADER
_TASKQUEUEFETCHQUEUESRESPONSE_QUEUE.fields_by_name['retry_parameters'].message_type = _TASKQUEUERETRYPARAMETERS
_TASKQUEUEFETCHQUEUESRESPONSE_QUEUE.fields_by_name['mode'].enum_type = _TASKQUEUEMODE_MODE
_TASKQUEUEFETCHQUEUESRESPONSE_QUEUE.fields_by_name['acl'].message_type = _TASKQUEUEACL
_TASKQUEUEFETCHQUEUESRESPONSE_QUEUE.fields_by_name['header_override'].message_type = _TASKQUEUEHTTPHEADER
_TASKQUEUEFETCHQUEUESRESPONSE_QUEUE.containing_type = _TASKQUEUEFETCHQUEUESRESPONSE
_TASKQUEUEFETCHQUEUESRESPONSE.fields_by_name['queue'].message_type = _TASKQUEUEFETCHQUEUESRESPONSE_QUEUE
_TASKQUEUEFETCHQUEUESTATSRESPONSE_QUEUESTATS.fields_by_name['scanner_info'].message_type = _TASKQUEUESCANNERQUEUEINFO
_TASKQUEUEFETCHQUEUESTATSRESPONSE_QUEUESTATS.containing_type = _TASKQUEUEFETCHQUEUESTATSRESPONSE
_TASKQUEUEFETCHQUEUESTATSRESPONSE.fields_by_name['queuestats'].message_type = _TASKQUEUEFETCHQUEUESTATSRESPONSE_QUEUESTATS
_TASKQUEUEQUERYTASKSRESPONSE_TASK_HEADER.containing_type = _TASKQUEUEQUERYTASKSRESPONSE_TASK
_TASKQUEUEQUERYTASKSRESPONSE_TASK_CRONTIMETABLE.containing_type = _TASKQUEUEQUERYTASKSRESPONSE_TASK
_TASKQUEUEQUERYTASKSRESPONSE_TASK_RUNLOG.containing_type = _TASKQUEUEQUERYTASKSRESPONSE_TASK
_TASKQUEUEQUERYTASKSRESPONSE_TASK.fields_by_name['method'].enum_type = _TASKQUEUEQUERYTASKSRESPONSE_TASK_REQUESTMETHOD
_TASKQUEUEQUERYTASKSRESPONSE_TASK.fields_by_name['header'].message_type = _TASKQUEUEQUERYTASKSRESPONSE_TASK_HEADER
_TASKQUEUEQUERYTASKSRESPONSE_TASK.fields_by_name['crontimetable'].message_type = _TASKQUEUEQUERYTASKSRESPONSE_TASK_CRONTIMETABLE
_TASKQUEUEQUERYTASKSRESPONSE_TASK.fields_by_name['runlog'].message_type = _TASKQUEUEQUERYTASKSRESPONSE_TASK_RUNLOG
_TASKQUEUEQUERYTASKSRESPONSE_TASK.fields_by_name['payload'].message_type = _TASKPAYLOAD
_TASKQUEUEQUERYTASKSRESPONSE_TASK.fields_by_name['retry_parameters'].message_type = _TASKQUEUERETRYPARAMETERS
_TASKQUEUEQUERYTASKSRESPONSE_TASK.containing_type = _TASKQUEUEQUERYTASKSRESPONSE
_TASKQUEUEQUERYTASKSRESPONSE_TASK_REQUESTMETHOD.containing_type = _TASKQUEUEQUERYTASKSRESPONSE_TASK
_TASKQUEUEQUERYTASKSRESPONSE.fields_by_name['task'].message_type = _TASKQUEUEQUERYTASKSRESPONSE_TASK
_TASKQUEUEFETCHTASKRESPONSE.fields_by_name['task'].message_type = _TASKQUEUEQUERYTASKSRESPONSE
_TASKQUEUEQUERYANDOWNTASKSRESPONSE_TASK.containing_type = _TASKQUEUEQUERYANDOWNTASKSRESPONSE
_TASKQUEUEQUERYANDOWNTASKSRESPONSE.fields_by_name['task'].message_type = _TASKQUEUEQUERYANDOWNTASKSRESPONSE_TASK
DESCRIPTOR.message_types_by_name['TaskQueueServiceError'] = _TASKQUEUESERVICEERROR
DESCRIPTOR.message_types_by_name['TaskPayload'] = _TASKPAYLOAD
DESCRIPTOR.message_types_by_name['TaskQueueRetryParameters'] = _TASKQUEUERETRYPARAMETERS
DESCRIPTOR.message_types_by_name['TaskQueueAcl'] = _TASKQUEUEACL
DESCRIPTOR.message_types_by_name['TaskQueueHttpHeader'] = _TASKQUEUEHTTPHEADER
DESCRIPTOR.message_types_by_name['TaskQueueMode'] = _TASKQUEUEMODE
DESCRIPTOR.message_types_by_name['TaskQueueAddRequest'] = _TASKQUEUEADDREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueAddResponse'] = _TASKQUEUEADDRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueBulkAddRequest'] = _TASKQUEUEBULKADDREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueBulkAddResponse'] = _TASKQUEUEBULKADDRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueDeleteRequest'] = _TASKQUEUEDELETEREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueDeleteResponse'] = _TASKQUEUEDELETERESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueForceRunRequest'] = _TASKQUEUEFORCERUNREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueForceRunResponse'] = _TASKQUEUEFORCERUNRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueUpdateQueueRequest'] = _TASKQUEUEUPDATEQUEUEREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueUpdateQueueResponse'] = _TASKQUEUEUPDATEQUEUERESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueFetchQueuesRequest'] = _TASKQUEUEFETCHQUEUESREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueFetchQueuesResponse'] = _TASKQUEUEFETCHQUEUESRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueFetchQueueStatsRequest'] = _TASKQUEUEFETCHQUEUESTATSREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueScannerQueueInfo'] = _TASKQUEUESCANNERQUEUEINFO
DESCRIPTOR.message_types_by_name['TaskQueueFetchQueueStatsResponse'] = _TASKQUEUEFETCHQUEUESTATSRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueuePauseQueueRequest'] = _TASKQUEUEPAUSEQUEUEREQUEST
DESCRIPTOR.message_types_by_name['TaskQueuePauseQueueResponse'] = _TASKQUEUEPAUSEQUEUERESPONSE
DESCRIPTOR.message_types_by_name['TaskQueuePurgeQueueRequest'] = _TASKQUEUEPURGEQUEUEREQUEST
DESCRIPTOR.message_types_by_name['TaskQueuePurgeQueueResponse'] = _TASKQUEUEPURGEQUEUERESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueDeleteQueueRequest'] = _TASKQUEUEDELETEQUEUEREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueDeleteQueueResponse'] = _TASKQUEUEDELETEQUEUERESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueDeleteGroupRequest'] = _TASKQUEUEDELETEGROUPREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueDeleteGroupResponse'] = _TASKQUEUEDELETEGROUPRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueQueryTasksRequest'] = _TASKQUEUEQUERYTASKSREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueQueryTasksResponse'] = _TASKQUEUEQUERYTASKSRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueFetchTaskRequest'] = _TASKQUEUEFETCHTASKREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueFetchTaskResponse'] = _TASKQUEUEFETCHTASKRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueUpdateStorageLimitRequest'] = _TASKQUEUEUPDATESTORAGELIMITREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueUpdateStorageLimitResponse'] = _TASKQUEUEUPDATESTORAGELIMITRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueQueryAndOwnTasksRequest'] = _TASKQUEUEQUERYANDOWNTASKSREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueQueryAndOwnTasksResponse'] = _TASKQUEUEQUERYANDOWNTASKSRESPONSE
DESCRIPTOR.message_types_by_name['TaskQueueModifyTaskLeaseRequest'] = _TASKQUEUEMODIFYTASKLEASEREQUEST
DESCRIPTOR.message_types_by_name['TaskQueueModifyTaskLeaseResponse'] = _TASKQUEUEMODIFYTASKLEASERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TaskQueueServiceError = _reflection.GeneratedProtocolMessageType('TaskQueueServiceError', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUESERVICEERROR,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueServiceError)

TaskPayload = _reflection.GeneratedProtocolMessageType('TaskPayload', (_message.Message,), {
  'DESCRIPTOR' : _TASKPAYLOAD,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskPayload)

TaskQueueRetryParameters = _reflection.GeneratedProtocolMessageType('TaskQueueRetryParameters', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUERETRYPARAMETERS,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueRetryParameters)

TaskQueueAcl = _reflection.GeneratedProtocolMessageType('TaskQueueAcl', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEACL,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueAcl)

TaskQueueHttpHeader = _reflection.GeneratedProtocolMessageType('TaskQueueHttpHeader', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEHTTPHEADER,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueHttpHeader)

TaskQueueMode = _reflection.GeneratedProtocolMessageType('TaskQueueMode', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEMODE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueMode)

TaskQueueAddRequest = _reflection.GeneratedProtocolMessageType('TaskQueueAddRequest', (_message.Message,), {

  'Header' : _reflection.GeneratedProtocolMessageType('Header', (_message.Message,), {
    'DESCRIPTOR' : _TASKQUEUEADDREQUEST_HEADER,
    '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

    })
  ,

  'CronTimetable' : _reflection.GeneratedProtocolMessageType('CronTimetable', (_message.Message,), {
    'DESCRIPTOR' : _TASKQUEUEADDREQUEST_CRONTIMETABLE,
    '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _TASKQUEUEADDREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueAddRequest)
_sym_db.RegisterMessage(TaskQueueAddRequest.Header)
_sym_db.RegisterMessage(TaskQueueAddRequest.CronTimetable)

TaskQueueAddResponse = _reflection.GeneratedProtocolMessageType('TaskQueueAddResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEADDRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueAddResponse)

TaskQueueBulkAddRequest = _reflection.GeneratedProtocolMessageType('TaskQueueBulkAddRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEBULKADDREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueBulkAddRequest)

TaskQueueBulkAddResponse = _reflection.GeneratedProtocolMessageType('TaskQueueBulkAddResponse', (_message.Message,), {

  'TaskResult' : _reflection.GeneratedProtocolMessageType('TaskResult', (_message.Message,), {
    'DESCRIPTOR' : _TASKQUEUEBULKADDRESPONSE_TASKRESULT,
    '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _TASKQUEUEBULKADDRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueBulkAddResponse)
_sym_db.RegisterMessage(TaskQueueBulkAddResponse.TaskResult)

TaskQueueDeleteRequest = _reflection.GeneratedProtocolMessageType('TaskQueueDeleteRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEDELETEREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueDeleteRequest)

TaskQueueDeleteResponse = _reflection.GeneratedProtocolMessageType('TaskQueueDeleteResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEDELETERESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueDeleteResponse)

TaskQueueForceRunRequest = _reflection.GeneratedProtocolMessageType('TaskQueueForceRunRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEFORCERUNREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueForceRunRequest)

TaskQueueForceRunResponse = _reflection.GeneratedProtocolMessageType('TaskQueueForceRunResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEFORCERUNRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueForceRunResponse)

TaskQueueUpdateQueueRequest = _reflection.GeneratedProtocolMessageType('TaskQueueUpdateQueueRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEUPDATEQUEUEREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueUpdateQueueRequest)

TaskQueueUpdateQueueResponse = _reflection.GeneratedProtocolMessageType('TaskQueueUpdateQueueResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEUPDATEQUEUERESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueUpdateQueueResponse)

TaskQueueFetchQueuesRequest = _reflection.GeneratedProtocolMessageType('TaskQueueFetchQueuesRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEFETCHQUEUESREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueFetchQueuesRequest)

TaskQueueFetchQueuesResponse = _reflection.GeneratedProtocolMessageType('TaskQueueFetchQueuesResponse', (_message.Message,), {

  'Queue' : _reflection.GeneratedProtocolMessageType('Queue', (_message.Message,), {
    'DESCRIPTOR' : _TASKQUEUEFETCHQUEUESRESPONSE_QUEUE,
    '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _TASKQUEUEFETCHQUEUESRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueFetchQueuesResponse)
_sym_db.RegisterMessage(TaskQueueFetchQueuesResponse.Queue)

TaskQueueFetchQueueStatsRequest = _reflection.GeneratedProtocolMessageType('TaskQueueFetchQueueStatsRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEFETCHQUEUESTATSREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueFetchQueueStatsRequest)

TaskQueueScannerQueueInfo = _reflection.GeneratedProtocolMessageType('TaskQueueScannerQueueInfo', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUESCANNERQUEUEINFO,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueScannerQueueInfo)

TaskQueueFetchQueueStatsResponse = _reflection.GeneratedProtocolMessageType('TaskQueueFetchQueueStatsResponse', (_message.Message,), {

  'QueueStats' : _reflection.GeneratedProtocolMessageType('QueueStats', (_message.Message,), {
    'DESCRIPTOR' : _TASKQUEUEFETCHQUEUESTATSRESPONSE_QUEUESTATS,
    '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _TASKQUEUEFETCHQUEUESTATSRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueFetchQueueStatsResponse)
_sym_db.RegisterMessage(TaskQueueFetchQueueStatsResponse.QueueStats)

TaskQueuePauseQueueRequest = _reflection.GeneratedProtocolMessageType('TaskQueuePauseQueueRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEPAUSEQUEUEREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueuePauseQueueRequest)

TaskQueuePauseQueueResponse = _reflection.GeneratedProtocolMessageType('TaskQueuePauseQueueResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEPAUSEQUEUERESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueuePauseQueueResponse)

TaskQueuePurgeQueueRequest = _reflection.GeneratedProtocolMessageType('TaskQueuePurgeQueueRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEPURGEQUEUEREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueuePurgeQueueRequest)

TaskQueuePurgeQueueResponse = _reflection.GeneratedProtocolMessageType('TaskQueuePurgeQueueResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEPURGEQUEUERESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueuePurgeQueueResponse)

TaskQueueDeleteQueueRequest = _reflection.GeneratedProtocolMessageType('TaskQueueDeleteQueueRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEDELETEQUEUEREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueDeleteQueueRequest)

TaskQueueDeleteQueueResponse = _reflection.GeneratedProtocolMessageType('TaskQueueDeleteQueueResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEDELETEQUEUERESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueDeleteQueueResponse)

TaskQueueDeleteGroupRequest = _reflection.GeneratedProtocolMessageType('TaskQueueDeleteGroupRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEDELETEGROUPREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueDeleteGroupRequest)

TaskQueueDeleteGroupResponse = _reflection.GeneratedProtocolMessageType('TaskQueueDeleteGroupResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEDELETEGROUPRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueDeleteGroupResponse)

TaskQueueQueryTasksRequest = _reflection.GeneratedProtocolMessageType('TaskQueueQueryTasksRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEQUERYTASKSREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueQueryTasksRequest)

TaskQueueQueryTasksResponse = _reflection.GeneratedProtocolMessageType('TaskQueueQueryTasksResponse', (_message.Message,), {

  'Task' : _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {

    'Header' : _reflection.GeneratedProtocolMessageType('Header', (_message.Message,), {
      'DESCRIPTOR' : _TASKQUEUEQUERYTASKSRESPONSE_TASK_HEADER,
      '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

      })
    ,

    'CronTimetable' : _reflection.GeneratedProtocolMessageType('CronTimetable', (_message.Message,), {
      'DESCRIPTOR' : _TASKQUEUEQUERYTASKSRESPONSE_TASK_CRONTIMETABLE,
      '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

      })
    ,

    'RunLog' : _reflection.GeneratedProtocolMessageType('RunLog', (_message.Message,), {
      'DESCRIPTOR' : _TASKQUEUEQUERYTASKSRESPONSE_TASK_RUNLOG,
      '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

      })
    ,
    'DESCRIPTOR' : _TASKQUEUEQUERYTASKSRESPONSE_TASK,
    '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _TASKQUEUEQUERYTASKSRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueQueryTasksResponse)
_sym_db.RegisterMessage(TaskQueueQueryTasksResponse.Task)
_sym_db.RegisterMessage(TaskQueueQueryTasksResponse.Task.Header)
_sym_db.RegisterMessage(TaskQueueQueryTasksResponse.Task.CronTimetable)
_sym_db.RegisterMessage(TaskQueueQueryTasksResponse.Task.RunLog)

TaskQueueFetchTaskRequest = _reflection.GeneratedProtocolMessageType('TaskQueueFetchTaskRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEFETCHTASKREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueFetchTaskRequest)

TaskQueueFetchTaskResponse = _reflection.GeneratedProtocolMessageType('TaskQueueFetchTaskResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEFETCHTASKRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueFetchTaskResponse)

TaskQueueUpdateStorageLimitRequest = _reflection.GeneratedProtocolMessageType('TaskQueueUpdateStorageLimitRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEUPDATESTORAGELIMITREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueUpdateStorageLimitRequest)

TaskQueueUpdateStorageLimitResponse = _reflection.GeneratedProtocolMessageType('TaskQueueUpdateStorageLimitResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEUPDATESTORAGELIMITRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueUpdateStorageLimitResponse)

TaskQueueQueryAndOwnTasksRequest = _reflection.GeneratedProtocolMessageType('TaskQueueQueryAndOwnTasksRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEQUERYANDOWNTASKSREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueQueryAndOwnTasksRequest)

TaskQueueQueryAndOwnTasksResponse = _reflection.GeneratedProtocolMessageType('TaskQueueQueryAndOwnTasksResponse', (_message.Message,), {

  'Task' : _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
    'DESCRIPTOR' : _TASKQUEUEQUERYANDOWNTASKSRESPONSE_TASK,
    '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

    })
  ,
  'DESCRIPTOR' : _TASKQUEUEQUERYANDOWNTASKSRESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueQueryAndOwnTasksResponse)
_sym_db.RegisterMessage(TaskQueueQueryAndOwnTasksResponse.Task)

TaskQueueModifyTaskLeaseRequest = _reflection.GeneratedProtocolMessageType('TaskQueueModifyTaskLeaseRequest', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEMODIFYTASKLEASEREQUEST,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueModifyTaskLeaseRequest)

TaskQueueModifyTaskLeaseResponse = _reflection.GeneratedProtocolMessageType('TaskQueueModifyTaskLeaseResponse', (_message.Message,), {
  'DESCRIPTOR' : _TASKQUEUEMODIFYTASKLEASERESPONSE,
  '__module__' : 'google.appengine.api.taskqueue.taskqueue_service_bytes_pb2'

  })
_sym_db.RegisterMessage(TaskQueueModifyTaskLeaseResponse)


DESCRIPTOR._options = None
_TASKPAYLOAD._options = None
_TASKQUEUEADDREQUEST.fields_by_name['body']._options = None
_TASKQUEUEFETCHQUEUESRESPONSE_QUEUE.fields_by_name['creator_name']._options = None
_TASKQUEUEQUERYTASKSRESPONSE_TASK.fields_by_name['body']._options = None
_TASKQUEUEQUERYANDOWNTASKSRESPONSE_TASK.fields_by_name['body']._options = None

