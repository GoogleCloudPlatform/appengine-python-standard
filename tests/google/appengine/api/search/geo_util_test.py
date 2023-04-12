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
"""Tests for google.appengine.api.search.geo_util."""

from google.appengine.api.search import geo_util
from absl.testing import absltest


class GeoUtilTest(absltest.TestCase):

  def testLatLng(self):
    sfo = geo_util.LatLng(37.619105, -122.375236)
    syd = geo_util.LatLng(-33.946110, 151.177222)
    self.assertEqual(11949733, int(sfo - syd))
    self.assertEqual(sfo - syd, syd - sfo)

  def testProperties(self):
    everest = geo_util.LatLng(86.921543, 86.921543)
    self.assertEqual(86.921543, everest.latitude)
    self.assertEqual(86.921543, everest.longitude)

  def testMicroDistance(self):
    a = geo_util.LatLng(37.619105, -122.375236)
    b = geo_util.LatLng(37.619106, -122.375236)
    self.assertEqual(0, int(b - a))
    self.assertEqual(0, int(a - b))


if __name__ == '__main__':
  absltest.main()
