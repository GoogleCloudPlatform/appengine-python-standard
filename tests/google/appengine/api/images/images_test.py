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
"""Tests for google.appengine.api.images."""

import os
from unittest import mock

from absl.testing import absltest
from google.appengine.api.images import images_service_pb2
from google.appengine.api import images

class ImagesGrpcTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    os.environ['USE_CUSTOM_IMAGES_GRPC_SERVICE'] = 'True'
    self.use_grpc_patcher = mock.patch('google.appengine.api.images._USE_GRPC', True)
    self.use_grpc_patcher.start()
    os.environ['IMAGES_SERVICE_ENDPOINT'] = 'https://localhost'

  def tearDown(self):
    self.use_grpc_patcher.stop()
    super().tearDown()
    del os.environ['USE_CUSTOM_IMAGES_GRPC_SERVICE']
    del os.environ['IMAGES_SERVICE_ENDPOINT']

  @mock.patch('google.appengine.api.images._make_grpc_call')
  def test_execute_transforms_async_grpc(self, mock_make_grpc_call):
    """Tests that execute_transforms_async calls the gRPC service."""
    mock_response = images_service_pb2.ImagesTransformResponse()
    mock_response.image.content = b'transformed_image'
    mock_make_grpc_call.return_value = mock_response

    image = images.Image(image_data=b'test_image')
    image.resize(width=100, height=100)
    rpc = image.execute_transforms_async()
    result = rpc.get_result()

    self.assertEqual(result, b'transformed_image')
    mock_make_grpc_call.assert_called_once()
    self.assertEqual(mock_make_grpc_call.call_args[0][0], 'Transform')


  @mock.patch('google.appengine.api.images._make_grpc_call')
  def test_histogram_async_grpc(self, mock_make_grpc_call):
    """Tests that histogram_async calls the gRPC service."""
    mock_response = images_service_pb2.ImagesHistogramResponse()
    mock_response.histogram.red.extend(range(256))
    mock_response.histogram.green.extend(range(256))
    mock_response.histogram.blue.extend(range(256))
    mock_make_grpc_call.return_value = mock_response

    image = images.Image(image_data=b'test_image')
    rpc = image.histogram_async()
    result = rpc.get_result()

    self.assertEqual(result[0], list(range(256)))
    self.assertEqual(result[1], list(range(256)))
    self.assertEqual(result[2], list(range(256)))
    mock_make_grpc_call.assert_called_once()
    self.assertEqual(mock_make_grpc_call.call_args[0][0], 'Histogram')


  @mock.patch('google.appengine.api.images._make_grpc_call')
  def test_composite_async_grpc(self, mock_make_grpc_call):
    """Tests that composite_async calls the gRPC service."""
    mock_response = images_service_pb2.ImagesTransformResponse()
    mock_response.image.content = b'composited_image'
    mock_make_grpc_call.return_value = mock_response

    inputs = [
        (b'test_image_1', 0, 0, 1.0, images.TOP_LEFT),
        (b'test_image_2', 10, 10, 0.5, images.TOP_LEFT),
    ]
    rpc = images.composite_async(
        inputs=inputs,
        width=200,
        height=200,
        color=0xFFFFFFFF,
        output_encoding=images.PNG,
    )
    result = rpc.get_result()

    self.assertEqual(result, b'composited_image')
    mock_make_grpc_call.assert_called_once()
    self.assertEqual(mock_make_grpc_call.call_args[0][0], 'Composite')


if __name__ == '__main__':
  absltest.main()
