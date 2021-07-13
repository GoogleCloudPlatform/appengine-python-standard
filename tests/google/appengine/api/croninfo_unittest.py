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


"""Tests for google.appengine.api.croninfo."""

import datetime
import re

from google.appengine.api import croninfo
from google.appengine.api import validation
from google.appengine.api import yaml_errors
from absl.testing import absltest




class CronEntryTest(absltest.TestCase):
  """Tests for the croninfo.CronEntry class."""

  def testCronEntryConstructor(self):
    """Tests a normal cron entry can be constructed."""
    cron = croninfo.CronEntry(url='/foo/bar/biz', schedule='every 2 mins')
    cron.CheckInitialized()
    self.assertEqual('/foo/bar/biz', cron.url)
    self.assertIsNone(cron.retry_parameters)

  def testCronEntryConstructorWithRetryParameters(self):
    """Tests a normal cron entry with retry parameters can be constructed."""
    retry_parameters = croninfo.RetryParameters(job_retry_limit=3)
    cron = croninfo.CronEntry(url='/foo/bar/biz',
                              schedule='every 2 mins',
                              retry_parameters=retry_parameters)
    cron.CheckInitialized()
    self.assertEqual('/foo/bar/biz', cron.url)
    self.assertEqual(3, cron.retry_parameters.job_retry_limit)
    self.assertIsNotNone(cron.retry_parameters)

  def testCronEntryConstructorWithAllRetryParameters(self):
    """Tests a normal cron entry with retry parameters can be constructed."""
    retry_parameters = croninfo.RetryParameters(job_retry_limit=4,
                                                job_age_limit='2d',
                                                min_backoff_seconds=17,
                                                max_backoff_seconds=17.77,
                                                max_doublings=8)
    cron = croninfo.CronEntry(url='/foo/bar/biz',
                              schedule='every 2 mins',
                              retry_parameters=retry_parameters)
    cron.CheckInitialized()
    self.assertEqual('/foo/bar/biz', cron.url)
    self.assertEqual(4, cron.retry_parameters.job_retry_limit)
    self.assertEqual('2d', cron.retry_parameters.job_age_limit)
    self.assertEqual(17, cron.retry_parameters.min_backoff_seconds)
    self.assertEqual(17.77, cron.retry_parameters.max_backoff_seconds)
    self.assertEqual(8, cron.retry_parameters.max_doublings)

  def testCronEntryConstructorWithEmptyRetryParameters(self):
    """Tests an empty cron entry with retry parameters can be constructed."""
    retry_parameters = croninfo.RetryParameters()
    cron = croninfo.CronEntry(url='/foo/bar/biz',
                              schedule='every 2 mins',
                              retry_parameters=retry_parameters)
    self.assertIsNotNone(cron.retry_parameters)
    self.assertIsNone(cron.retry_parameters.job_retry_limit)
    self.assertIsNone(cron.retry_parameters.job_age_limit)
    self.assertIsNone(cron.retry_parameters.min_backoff_seconds)
    self.assertIsNone(cron.retry_parameters.max_backoff_seconds)
    self.assertIsNone(cron.retry_parameters.max_doublings)

  def testRetryParameterConstructorBadRetryAgeLimit(self):
    """Tests retry parameters with a bad age limit."""
    self.assertRaises(validation.ValidationError,
                      croninfo.RetryParameters,
                      job_age_limit='2x')

  def testRetryParameterConstructorNegativeValues(self):
    """Tests that (illegal) retry parameter negative values raise an error."""
    self.assertRaises(validation.ValidationError,
                      croninfo.RetryParameters,
                      job_retry_limit=-1)
    self.assertRaises(validation.ValidationError,
                      croninfo.RetryParameters,
                      max_doublings=-2.0)
    self.assertRaises(validation.ValidationError,
                      croninfo.RetryParameters,
                      min_backoff_seconds=-3.0)
    self.assertRaises(validation.ValidationError,
                      croninfo.RetryParameters,
                      max_backoff_seconds=-4)

  def testCronEntryConstructorWithAttemptDeadline(self):
    """Tests a normal cron entry with retry parameters can be constructed."""
    cron = croninfo.CronEntry(
        url='/foo/bar/biz', schedule='every 2 mins', attempt_deadline='15.1s')
    cron.CheckInitialized()
    self.assertEqual(datetime.timedelta(seconds=15.1), cron.attempt_deadline)

  def testLoadCronWithAttemptDeadlineEndOfLineChracters(self):
    """Tests that end-of-line characters are removed from cron entry."""
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  attempt_deadline: 25.1s\n\r')
    config = croninfo.LoadSingleCron(input_data)
    self.assertEqual('test-retry-app', config.application)
    self.assertLen(config.cron, 1)
    self.assertIsInstance(config.cron[0], croninfo.CronEntry)
    self.assertEqual(
        datetime.timedelta(seconds=25.1), config.cron[0].attempt_deadline)

  def testCronAttemptDeadlineInvalidFormat(self):
    """Tests that a badly formatted attempt deadline string raise an exception."""
    self.assertRaises(
        validation.ValidationError,
        croninfo.CronEntry,
        url='/',
        schedule='every 1 minutes',
        attempt_deadline='20m')
    self.assertRaises(
        validation.ValidationError,
        croninfo.CronEntry,
        url='/',
        schedule='every 1 minutes',
        attempt_deadline='..223s')

  def testBadCronEntryConstructor(self):
    """Tests that absolute URLs are rejected."""
    self.assertRaises(validation.ValidationError, croninfo.CronEntry,
                      url='http://www.google.com/',
                      schedule='every 2 mins')

  def testMissingCronEntryConstructor(self):
    """Tests for required values."""
    cron = croninfo.CronEntry(schedule='every 2 mins')
    self.assertRaises(validation.MissingAttribute, cron.CheckInitialized)
    cron = croninfo.CronEntry(url='/cron.html')
    self.assertRaises(validation.MissingAttribute, cron.CheckInitialized)


















  def testInvalidTimezoneConstructor(self):
    """Tests that an invalid timezone is rejected."""
    self.assertRaises(validation.ValidationError, croninfo.CronEntry,
                      url='/foo/bar/baz', schedule='every 2 minutes',
                      timezone='orbiting jupiter')


class CronInfoTest(absltest.TestCase):
  """Tests for the croninfo.CronInfoExternal class."""

  def testCronInfoConstructor(self):
    info = croninfo.CronInfoExternal(cron=[
        croninfo.CronEntry(url='/foo', schedule='every 2 mins'),
        croninfo.CronEntry(url='/baz', schedule='every 20 hours'),
        croninfo.CronEntry(url='/baz', schedule='every 20 hours',
                           timezone='PST8PDT'),
        ])
    info.CheckInitialized()


class LoadSingleCronTest(absltest.TestCase):

  def testLoaderSaneFile(self):
    input_data = ('application: test-app\n'
                  'cron:\n'
                  '- url: /admin/hourly\n'
                  '  schedule: every 60 mins\n'
                  '- url: /admin/daily\n'
                  '  schedule: every 24 hours\n'
                  '  timezone: Australia/NSW\n'
                  '- url: /admin/minute\n'
                  '  schedule: every 1 mins\n'
                  '  target: my-alternate-version\n'
                  '- url: /admin/description\n'
                  '  schedule: every 2 mins\n'
                  '  description: A task that runs every 2 minutes.\n'
                 )
    config = croninfo.LoadSingleCron(input_data)
    self.assertEqual('test-app', config.application)
    self.assertLen(config.cron, 4)
    self.assertIsInstance(config.cron[0], croninfo.CronEntry)
    self.assertIsInstance(config.cron[1], croninfo.CronEntry)
    self.assertEqual(config.cron[1].url, '/admin/daily')
    self.assertEqual(config.cron[1].schedule, 'every 24 hours')
    self.assertEqual(config.cron[1].timezone, 'Australia/NSW')
    self.assertEqual(config.cron[2].url, '/admin/minute')
    self.assertEqual(config.cron[2].schedule, 'every 1 mins')
    self.assertEqual(config.cron[2].target, 'my-alternate-version')
    self.assertEqual(config.cron[3].url, '/admin/description')
    self.assertEqual(config.cron[3].schedule, 'every 2 mins')
    self.assertEqual(config.cron[3].description,
                     'A task that runs every 2 minutes.')

  def testLoaderSaneFileWithRetry(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    job_retry_limit: 4\n'
                  '- url: /a/retry/job2\n'
                  '  schedule: every 14 hours\n'
                  '  retry_parameters:\n'
                  '    job_retry_limit: 2\n'
                  '    job_age_limit: 1d\n'
                  '    min_backoff_seconds: 1\n'
                  '    max_backoff_seconds: 1800\n'
                  '    max_doublings: 20\n'
                 )
    config = croninfo.LoadSingleCron(input_data)
    self.assertEqual('test-retry-app', config.application)
    self.assertLen(config.cron, 2)
    self.assertIsInstance(config.cron[0], croninfo.CronEntry)
    self.assertIsNotNone(config.cron[0].retry_parameters)
    self.assertEqual(4, config.cron[0].retry_parameters.job_retry_limit)
    self.assertIsNone(config.cron[0].retry_parameters.job_age_limit)
    self.assertIsNone(config.cron[0].retry_parameters.min_backoff_seconds)
    self.assertIsNone(config.cron[0].retry_parameters.max_backoff_seconds)
    self.assertIsNone(config.cron[0].retry_parameters.max_doublings)
    self.assertIsNotNone(config.cron[1].retry_parameters)
    self.assertEqual(2, config.cron[1].retry_parameters.job_retry_limit)
    self.assertEqual('1d', config.cron[1].retry_parameters.job_age_limit)
    self.assertEqual(1, config.cron[1].retry_parameters.min_backoff_seconds)
    self.assertEqual(1800, config.cron[1].retry_parameters.max_backoff_seconds)
    self.assertEqual(20, config.cron[1].retry_parameters.max_doublings)

  def testLoaderInvalidRetry_1(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    job_retry_limit: -1\n'
                 )
    with self.assertRaisesRegex(yaml_errors.EventListenerError, '-1'):
      croninfo.LoadSingleCron(input_data)

  def testLoaderInvalidRetry_2(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    job_age_limit: 0\n'
                 )
    self.assertRaises(yaml_errors.EventListenerError,
                      croninfo.LoadSingleCron, input_data)

  def testLoaderInvalidRetry_3(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    job_age_limit: xx\n'
                 )
    self.assertRaises(yaml_errors.EventListenerError,
                      croninfo.LoadSingleCron, input_data)

  def testLoaderInvalidRetry_4(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    job_age_limit: {}\n'
                 )
    self.assertRaises(yaml_errors.EventListenerError,
                      croninfo.LoadSingleCron, input_data)

  def testLoaderInvalidRetry_5(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    job_age_limit: xx\n'
                 )
    self.assertRaises(yaml_errors.EventListenerError,
                      croninfo.LoadSingleCron, input_data)

  def testLoaderInvalidRetry_6(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    job_age_limit: {}\n'
                 )
    self.assertRaises(yaml_errors.EventListenerError,
                      croninfo.LoadSingleCron, input_data)

  def testLoaderInvalidRetry_7(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    max_doublings: -5\n'
                 )
    self.assertRaises(yaml_errors.EventListenerError,
                      croninfo.LoadSingleCron, input_data)

  def testLoaderInvalidRetry_8(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    min_backoff_seconds: -55\n'
                 )
    self.assertRaises(yaml_errors.EventListenerError,
                      croninfo.LoadSingleCron, input_data)

  def testLoaderInvalidRetry_9(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    max_backoff_seconds: -2\n'
                 )
    self.assertRaises(yaml_errors.EventListenerError,
                      croninfo.LoadSingleCron, input_data)

  def testLoaderInvalidRetry_10(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters:\n'
                  '    param_doesnt_exist: 2\n'
                 )
    self.assertRaises(yaml_errors.EventListenerError,
                      croninfo.LoadSingleCron, input_data)

  def testLoaderEmptyRetry_11(self):
    input_data = ('application: test-retry-app\n'
                  'cron:\n'
                  '- url: /a/retry/job\n'
                  '  schedule: every 12 mins\n'
                  '  retry_parameters: {}\n'
                 )
    config = croninfo.LoadSingleCron(input_data)
    self.assertLen(config.cron, 1)
    self.assertIsNotNone(config.cron[0].retry_parameters)
    self.assertIsNone(config.cron[0].retry_parameters.job_retry_limit)
    self.assertIsNone(config.cron[0].retry_parameters.job_age_limit)
    self.assertIsNone(config.cron[0].retry_parameters.min_backoff_seconds)
    self.assertIsNone(config.cron[0].retry_parameters.max_backoff_seconds)
    self.assertIsNone(config.cron[0].retry_parameters.max_doublings)

  def testLoaderUnicodeDescription(self):
    input_data = ('cron:\n'
                  '- url: /admin/description\n'
                  '  schedule: every 2 mins\n'
                  '  description: A Chinese description - '
                  u'\u4e2d\u56fd\u63cf\u8ff0.\n'
                 )
    config = croninfo.LoadSingleCron(input_data)
    self.assertLen(config.cron, 1)
    self.assertEqual(config.cron[0].url, '/admin/description')
    self.assertEqual(config.cron[0].description,
                     u'A Chinese description - \u4e2d\u56fd\u63cf\u8ff0.')

  def testLoaderWithoutPytz(self):

    real_pytz_module = croninfo.pytz
    croninfo.pytz = None
    try:
      self.testLoaderSaneFile()
    finally:
      croninfo.pytz = real_pytz_module

  def testLoaderWithModuleTarget(self):
    input_data = ('application: test-app\n'
                  'cron:\n'
                  '- url: /admin/hourly\n'
                  '  schedule: every 60 mins\n'
                  '  target: module\n'
                 )
    config = croninfo.LoadSingleCron(input_data)
    self.assertEqual('test-app', config.application)
    self.assertLen(config.cron, 1)
    self.assertIsInstance(config.cron[0], croninfo.CronEntry)
    self.assertEqual(config.cron[0].url, '/admin/hourly')
    self.assertEqual(config.cron[0].schedule, 'every 60 mins')
    self.assertEqual(config.cron[0].target, 'module')

  def testLoaderWithNumericVerisionedModuleTarget(self):
    """Test b/35767221.

    apphosting/api/croninfo.py should have the same change as b/15887817.
    """



    input_data = ('application: test-app\n'
                  'cron:\n'
                  '- url: /admin/hourly\n'
                  '  schedule: every 60 mins\n'
                  '  target: 1:module\n'
                 )
    config = croninfo.LoadSingleCron(input_data)
    self.assertEqual('test-app', config.application)
    self.assertLen(config.cron, 1)
    self.assertIsInstance(config.cron[0], croninfo.CronEntry)
    self.assertEqual(config.cron[0].url, '/admin/hourly')
    self.assertEqual(config.cron[0].schedule, 'every 60 mins')
    self.assertEqual(config.cron[0].target, '1:module')



    input_data = ('application: test-app\n'
                  'cron:\n'
                  '- url: /admin/hourly\n'
                  '  schedule: every 60 mins\n'
                  '  target: 1.module\n'
                 )


    with self.assertRaisesRegex(
        yaml_errors.EventError,
        re.escape(
            'Value \'1.module\' for target does not match expression \''
            r'^(?:^(?:(?:((?!-)[a-z\d\-]{1,63}):)?)((?!-)[a-z\d\-]{1,100})$)$'
            '\'')):
      croninfo.LoadSingleCron(input_data)


if __name__ == '__main__':
  absltest.main()
