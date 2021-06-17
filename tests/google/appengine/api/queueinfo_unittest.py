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


"""Tests for google.appengine.api.queueinfo."""

import re

from google.appengine.api import queueinfo
from google.appengine.api import validation
from google.appengine.api import yaml_errors
from absl.testing import absltest




class QueueEntryTest(absltest.TestCase):
  """Tests for the queueinfo.QueueEntry class."""

  def testQueueEntryConstructor(self):
    """Tests a normal queue entry can be constructed."""
    queue = queueinfo.QueueEntry(name='mail-queue', rate='2000/d')
    queue.CheckInitialized()
    self.assertEqual('2000/d', queue.rate)

    queue = queueinfo.QueueEntry(name='mail-queue', rate='2000/d',
                                 bucket_size='11')
    queue.CheckInitialized()
    self.assertEqual('2000/d', queue.rate)
    self.assertEqual(11, queue.bucket_size)

    queue = queueinfo.QueueEntry(name='mail-queue', rate='0')
    queue.CheckInitialized()
    self.assertEqual('0', queue.rate)

    queue = queueinfo.QueueEntry(name='a-queue', rate='20/s',
                                 max_concurrent_requests='3')
    queue.CheckInitialized()
    self.assertEqual('20/s', queue.rate)
    self.assertEqual(3, queue.max_concurrent_requests)

    queue = queueinfo.QueueEntry(name='mail-queue', rate='5/s',
                                 mode='push')
    queue.CheckInitialized()
    self.assertEqual('5/s', queue.rate)
    self.assertEqual('push', queue.mode)

  def testMissingQueueEntryConstructor(self):
    """Tests for required values."""
    queue = queueinfo.QueueEntry(rate='20/d')
    self.assertRaises(validation.MissingAttribute, queue.CheckInitialized)
    queue = queueinfo.QueueEntry(name='q-is-for-qookie')
    queue.CheckInitialized()


class QueueInfoTest(absltest.TestCase):
  """Tests for the queueinfo.QueueInfoExternal class."""

  def testQueueInfoConstructor(self):
    info = queueinfo.QueueInfoExternal(queue=[
        queueinfo.QueueEntry(name='foo', rate='2/s'),
        queueinfo.QueueEntry(name='baz', rate='10/m'),
        queueinfo.QueueEntry(name='beep', rate='5/h', bucket_size='2')
        ])
    info.CheckInitialized()

  def testQueueInfoConstructorWithStorageLimit(self):
    info = queueinfo.QueueInfoExternal(
        total_storage_limit='200M',
        queue=[queueinfo.QueueEntry(name='foofy', rate='13/s')])
    info.CheckInitialized()


class LoadSingleQueueTest(absltest.TestCase):
  """Tests the queueinfo.LoadSingleQueue function."""

  def testLoaderSaneFile(self):
    input_data = ('application: testapp\n'
                  'queue:\n'
                  '- name: mail-queue\n'
                  '  rate: 2000/d\n'
                  '  bucket_size: 11\n'
                  '- name: speedy-queue\n'
                  '  rate: 5/s\n'
                 )
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertEqual('testapp', config.application)
    self.assertLen(config.queue, 2)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertIsInstance(config.queue[1], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'mail-queue')
    self.assertEqual(config.queue[0].rate, '2000/d')
    self.assertEqual(config.queue[0].bucket_size, 11)

  def testLoaderSaneFileWithStorageLimit(self):
    input_data = ('total_storage_limit: 140M\n'
                  'queue:\n'
                  '- name: mail-queue\n'
                  '  rate: 2000/d\n'
                  '  bucket_size: 11\n'
                  '- name: speedy-queue\n'
                  '  rate: 5/s\n'
                  '  mode: pull'
                  )
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertEqual('140M', config.total_storage_limit)
    self.assertLen(config.queue, 2)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertIsInstance(config.queue[1], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'mail-queue')
    self.assertEqual(config.queue[0].rate, '2000/d')
    self.assertEqual(config.queue[0].bucket_size, 11)
    self.assertEqual(config.queue[1].name, 'speedy-queue')
    self.assertEqual(config.queue[1].rate, '5/s')
    self.assertEqual(config.queue[1].mode, 'pull')

  def testLoaderFileWithMaxConcurrentRequests(self):
    input_data = ('queue:\n'
                  '- name: server-queue\n'
                  '  rate: 50/s\n'
                  '  max_concurrent_requests: 15\n')
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertLen(config.queue, 1)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'server-queue')
    self.assertEqual(config.queue[0].rate, '50/s')
    self.assertEqual(config.queue[0].max_concurrent_requests, 15)

  def testLoaderFileWithTarget(self):
    input_data = ('queue:\n'
                  '- name: server-queue\n'
                  '  rate: 50/s\n'
                  '  target: my-version-name\n')
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertLen(config.queue, 1)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'server-queue')
    self.assertEqual(config.queue[0].rate, '50/s')
    self.assertEqual(config.queue[0].target, 'my-version-name')

  def testLoaderFileWithNumericTarget(self):
    input_data = ('queue:\n'
                  '- name: server-queue\n'
                  '  rate: 50/s\n'
                  '  target: 1\n')
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertLen(config.queue, 1)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'server-queue')
    self.assertEqual(config.queue[0].rate, '50/s')
    self.assertEqual(config.queue[0].target, '1')

  def testLoaderFileWithVersionedModuleTarget(self):
    input_data = ('queue:\n'
                  '- name: server-queue\n'
                  '  rate: 50/s\n'
                  '  target: version1.api\n')
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertLen(config.queue, 1)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'server-queue')
    self.assertEqual(config.queue[0].rate, '50/s')
    self.assertEqual(config.queue[0].target, 'version1.api')

  def testLoaderFileWithNumericVerisionedModuleTarget(self):
    input_data = ('queue:\n'
                  '- name: push-queue\n'
                  '  rate: 5/s\n'

                  '  target: 1.module\n')
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertLen(config.queue, 1)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'push-queue')
    self.assertEqual(config.queue[0].rate, '5/s')
    self.assertEqual(config.queue[0].target, '1.module')

  def testLoaderFileWithTargetParsingError(self):
    """Test an erroneous target."""
    input_data = ('queue:\n'
                  '- name: push-queue\n'
                  '  rate: 5/s\n'
                  '  target: bad:bad\n')
    with self.assertRaisesRegex(
        yaml_errors.EventError,
        re.escape(
            "Value 'bad:bad' for target does not match expression '"
            "^(?:^(?:(?:((?!-)[a-z\d\-]{1,100})\.)?)((?!-)[a-z\d\-]{1,63})$)$'")
    ):
      queueinfo.LoadSingleQueue(input_data)

  def testLoaderFileWithInstanceVerisionedModuleTarget(self):
    """Instance can't be specified in the queue target.

    It's not known whether this is intentional or a bug.
    """
    input_data = ('queue:\n'
                  '- name: push-queue\n'
                  '  rate: 5/s\n'

                  '  target: 1.1.module\n')
    with self.assertRaisesRegex(
        yaml_errors.EventError,
        re.escape(
            "Value '1.1.module' for target does not match expression '"
            "^(?:^(?:(?:((?!-)[a-z\d\-]{1,100})\.)?)((?!-)[a-z\d\-]{1,63})$)$'")
    ):
      queueinfo.LoadSingleQueue(input_data)

  def testLoaderFileWithMode(self):
    input_data = ('queue:\n'
                  '- name: pull-queue\n'
                  '  rate: 2000/d\n'
                  '  mode: pull\n'
                  '- name: default\n'
                  '  rate: 10/m\n'
                  '  mode: push\n'
                 )
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertLen(config.queue, 2)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'pull-queue')
    self.assertEqual(config.queue[0].rate, '2000/d')
    self.assertEqual(config.queue[0].mode, 'pull')
    self.assertIsInstance(config.queue[1], queueinfo.QueueEntry)
    self.assertEqual(config.queue[1].name, 'default')
    self.assertEqual(config.queue[1].rate, '10/m')
    self.assertEqual(config.queue[1].mode, 'push')

  def testLoaderFileWithRetryParameters(self):
    input_data = ('queue:\n'
                  '- name: server-queue\n'
                  '  rate: 50/s\n'
                  '  max_concurrent_requests: 15\n'
                  '  retry_parameters:\n'
                  '    task_retry_limit: 100\n'
                  '    task_age_limit: 1d\n'
                  '    min_backoff_seconds: 1\n'
                  '    max_backoff_seconds: 1800\n'
                  '    max_doublings: 20\n'
                  '- name: data-queue\n'
                  '  retry_parameters:\n'
                  '    task_retry_limit: 0\n')
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertLen(config.queue, 2)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'server-queue')
    self.assertEqual(config.queue[0].rate, '50/s')

    retry = config.queue[0].retry_parameters
    self.assertIsInstance(retry, queueinfo.RetryParameters)
    self.assertEqual(100, retry.task_retry_limit)
    self.assertEqual('1d', retry.task_age_limit)
    self.assertEqual(1.0, retry.min_backoff_seconds)
    self.assertEqual(1800.0, retry.max_backoff_seconds)
    self.assertEqual(20, retry.max_doublings)

    self.assertIsInstance(config.queue[1], queueinfo.QueueEntry)
    self.assertEqual(config.queue[1].name, 'data-queue')

    retry = config.queue[1].retry_parameters
    self.assertIsInstance(retry, queueinfo.RetryParameters)
    self.assertEqual(0, retry.task_retry_limit)

  def testLoaderFileWithAcl(self):
    input_data = ('queue:\n'
                  '- name: server-queue\n'
                  '  rate: 50/s\n'
                  '  max_concurrent_requests: 15\n'
                  '  acl:\n'
                  '  - user_email: a@b.com\n'
                  '  - user_email: c@gmail.com\n'
                  '  - writer_email: c@gmail.com\n')
    config = queueinfo.LoadSingleQueue(input_data)
    self.assertLen(config.queue, 1)
    self.assertIsInstance(config.queue[0], queueinfo.QueueEntry)
    self.assertEqual(config.queue[0].name, 'server-queue')
    self.assertEqual(config.queue[0].rate, '50/s')
    acl = config.queue[0].acl
    self.assertLen(acl, 3)
    self.assertIsInstance(acl[0], queueinfo.Acl)
    self.assertEqual('a@b.com', acl[0].user_email)
    self.assertIsInstance(acl[1], queueinfo.Acl)
    self.assertEqual('c@gmail.com', acl[1].user_email)
    self.assertIsInstance(acl[2], queueinfo.Acl)
    self.assertEqual('c@gmail.com', acl[2].writer_email)


class ParseRateTest(absltest.TestCase):
  """Tests the rate parsing code."""

  def testParseRate(self):
    self.assertAlmostEqual(1 / 43.2, queueinfo.ParseRate('2000/d'))
    self.assertAlmostEqual(1.0, queueinfo.ParseRate('1/s'))
    self.assertAlmostEqual(0.025, queueinfo.ParseRate('1.5/m'))
    self.assertAlmostEqual(0.0, queueinfo.ParseRate('0./s'))
    self.assertAlmostEqual(0.0, queueinfo.ParseRate('0/s'))
    self.assertAlmostEqual(2.0, queueinfo.ParseRate('7200/h'))
    self.assertAlmostEqual(2.0, queueinfo.ParseRate('7200./h'))
    self.assertAlmostEqual(0.0, queueinfo.ParseRate('0'))
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseRate, '200/d/h')
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseRate, '200/f')
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseRate, 'x/s')


class ParseTotalStorageLimitTest(absltest.TestCase):
  """Tests the total_storage_limit parsing code."""

  def testParseLimit(self):
    K = 1024
    self.assertEqual(1443, queueinfo.ParseTotalStorageLimit('1443'))
    self.assertEqual(1443, queueinfo.ParseTotalStorageLimit('1443B'))
    self.assertEqual(1443 * K, queueinfo.ParseTotalStorageLimit('1443K'))
    self.assertEqual(1443 * K * K, queueinfo.ParseTotalStorageLimit('1443M'))
    self.assertEqual(1443 * K * K * K,
                     queueinfo.ParseTotalStorageLimit('1443G'))
    self.assertEqual(1443 * K * K * K * K,
                     queueinfo.ParseTotalStorageLimit('1443T'))
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseTotalStorageLimit, '1443T3')
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseTotalStorageLimit, '')


class ParseTaskAgeLimitTest(absltest.TestCase):
  """Tests the task_age_limit parsing code."""

  def testValidateAgeLimit(self):
    validator = queueinfo.RetryParameters.ATTRIBUTES['task_age_limit']
    for age_limit in [
        '12345s', '20m', '2h', '1.5d', '12345.5s', '123.45e2s', '1e-2d']:
      validator.Validate(age_limit, 'task_age_limit')

  def testParseAgeLimit(self):
    self.assertEqual(12345, queueinfo.ParseTaskAgeLimit('12345s'))
    self.assertEqual(1200, queueinfo.ParseTaskAgeLimit('20m'))
    self.assertEqual(7200, queueinfo.ParseTaskAgeLimit('2h'))
    self.assertEqual(129600, queueinfo.ParseTaskAgeLimit('1.5d'))
    self.assertEqual(12345, queueinfo.ParseTaskAgeLimit('12345.5s'))
    self.assertEqual(12345, queueinfo.ParseTaskAgeLimit('123.45e2s'))
    self.assertEqual(864, queueinfo.ParseTaskAgeLimit('1e-2d'))
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseTaskAgeLimit, '')
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseTaskAgeLimit, '12345')
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseTaskAgeLimit, '123,45s')
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseTaskAgeLimit, '123.4.5s')
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseTaskAgeLimit, '123e2.3s')
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseTaskAgeLimit, '12345mm')
    self.assertRaises(queueinfo.MalformedQueueConfiguration,
                      queueinfo.ParseTaskAgeLimit, '12345a')


if __name__ == '__main__':
  absltest.main()



