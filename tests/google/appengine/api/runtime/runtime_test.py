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


"""Tests for google.appengine.api.runtime.runtime."""



from absl.testing import absltest
from google.appengine.api import apiproxy_stub_map
from google.appengine.api.runtime import runtime
from google.appengine.api.system import system_stub
from google.appengine.api.system import system_service_pb2


class RuntimeTest(absltest.TestCase):
  def setUp(self):
    self.cpu_stat = system_service_pb2.SystemStat()
    self.cpu_stat.total = 6000
    self.cpu_stat.rate1m = 100
    self.cpu_stat.rate10m = 150

    self.memory_stat = system_service_pb2.SystemStat()
    self.memory_stat.current = 50
    self.memory_stat.average1m = 100
    self.memory_stat.average10m = 150

    self.system_stub = system_stub.SystemServiceStub(self.cpu_stat,
                                                     self.memory_stat)
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub('system', self.system_stub)

  def assertProtoEquals(self, one, two):
    self.assertEqual(str(one), str(two))

  def testCpuUsage(self):

    cpu = runtime.cpu_usage()


    self.assertEqual(6000, cpu.total)
    self.assertEqual(100, cpu.rate1m)
    self.assertEqual(150, cpu.rate10m)

    self.assertFalse(cpu.HasField('current'))
    self.assertFalse(cpu.HasField('average1m'))
    self.assertFalse(cpu.HasField('average10m'))

    self.assertEqual({'GetSystemStats': 1}, self.system_stub.num_calls)

  def testMemoryUsage(self):

    memory = runtime.memory_usage()


    self.assertEqual(50, memory.current)
    self.assertEqual(100, memory.average1m)
    self.assertEqual(150, memory.average10m)

    self.assertFalse(memory.HasField('total'))
    self.assertFalse(memory.HasField('rate1m'))
    self.assertFalse(memory.HasField('rate10m'))

    self.assertEqual({'GetSystemStats': 1}, self.system_stub.num_calls)

if __name__ == '__main__':
  absltest.main()

