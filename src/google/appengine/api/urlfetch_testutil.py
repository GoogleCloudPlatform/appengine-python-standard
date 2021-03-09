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



"""Utilities for mocking out URL fetches."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import select
import socket
import threading
import time

import mox
import six
from six.moves import http_client
from six.moves import map
from six.moves import urllib
import six.moves.BaseHTTPServer

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import urlfetch_stub
from google.net.util.python import dualstack
from absl.testing import absltest




@dualstack.DecorateSocketServer
class IPv6CompatibleHTTPServer(six.moves.BaseHTTPServer.HTTPServer):
  pass


class MockHTTPHandler(six.moves.BaseHTTPServer.BaseHTTPRequestHandler):
  """HTTP handler subclass to test various kinds of requests from urlfetch.

  Responds to both GET and POST requests for the path /good. Will additionally
  echo any input headers or post payload in the output to verify that it was
  received correctly.
  """

  def do_GET(self):
    """Handler for GET requests.

    Responds to GET requests for the path /good, /huge and /headers; otherwise
    returns httplib.NOT_FOUND. Will additionally echo the Extra-Header in
    the output.
    """
    if self.path.endswith('/good'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      if 'Extra-Header' in self.headers:
        self._write(', '.join(
            urlfetch_stub.GetHeaders(self.headers, 'Extra-Header')))
      else:
        self._write('good')
    elif self.path.endswith('/proxy'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self._write('proxy')
    elif self.path.endswith('/headers_casing'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
      if six.PY2:
        response_headers = self.headers.headers
      else:


        response_headers = [
            '%s: %s\r\n' % (key, value)
            for (key, value) in self.headers.items()
        ]
      self._write(json.dumps(response_headers))
    elif self.path.endswith('/caf%C3%A9'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self._write('caf\xc3\xa9')
    elif self.path.endswith('/good?q=great'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      if 'Extra-Header' in self.headers:
        self._write(self.headers['Extra-Header'])
      else:
        self._write('great')
    elif self.path.endswith('/gzipped'):
      gzip_accept = self.headers.get('accept-encoding') == 'gzip'
      if gzip_accept:
        self.send_response(http_client.OK)
      else:
        self.send_response(http_client.BAD_REQUEST)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Encoding', 'gzip')
      self.end_headers()
      self._write(b'\x1f\x8b\x08\x00\xba\xcb\xf8I\x02\xffK\xcf\xcfO\x01'
                  b'\x00\x92N\x84l\x04\x00\x00\x00')
    elif self.path.endswith('/huge'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self._write('huge resp ' + ('a' * 2**25))
    elif self.path.endswith('/headers'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self._write(str(self.headers).encode('utf-8'))
    elif '/redirect301' in self.path:
      self.send_response(http_client.MOVED_PERMANENTLY)
      redirect_url = 'http://%s' % self.headers.get('host')
      self.send_header('Location', redirect_url + '/good')
      self.end_headers()
    elif '/redirect/' in self.path:
      offset = self.path.find('/redirect/') + len('/redirect/')
      if(self.path.find("?") >= 0):
        query_string = self.path[self.path.find('?'):]
        count = int(self.path[offset:self.path.find('?')])
      else:
        count = int(self.path[offset:])
        query_string = ""
      self.send_response(http_client.FOUND)
      redirect_url = 'http://%s' % self.headers.get('host')
      if count == 0:
        self.send_header('Location', redirect_url + '/good' + query_string)
      else:
        self.send_header('Location', '%s/redirect/%d%s' %
                         (redirect_url, count - 1, query_string) )
      self.end_headers()
    elif self.path.endswith('/no_location_redirect'):
      self.send_response(http_client.FOUND)
      self.end_headers()
      self._write('this is some data here')
    elif self.path.endswith('/bad_location_redirect'):
      self.send_response(http_client.FOUND)
      self.send_header('Location', 'htmp://foo.moo')
      self.end_headers()
    elif self.path.endswith('/relative_redirect'):
      self.send_response(http_client.FOUND)
      self.send_header('Location', '/good')
      self.end_headers()
    elif self.path.endswith('/no_host_redirect'):
      self.send_response(http_client.FOUND)
      self.send_header('Location', 'http:///foo.html')
      self.end_headers()
    elif self.path.endswith('/custom_useragent'):
      useragent_match = False
      for h in self.headers:
        if (h.lower() == 'user-agent' and self.headers[h] ==
            'IE AppEngine-Google; (+http://code.google.com/appengine; ' +
            'appid: mylittleapp)'):
          useragent_match = True
      if useragent_match:
        self.send_response(http_client.OK)
      else:
        self.send_response(http_client.BAD_REQUEST)
      self.end_headers()
    elif self.path.endswith('/no_forbidden_headers'):
      STANDARD_HEADERS = set([
          ('content-length', '0'),
          ('accept-encoding', 'gzip'),
          ('user-agent',
           'AppEngine-Google; (+http://code.google.com/appengine; ' +
           'appid: mylittleapp)')])
      no_user_headers = True
      custom_header = False
      for h in self.headers:
        if h.lower() == 'host' and self.headers[h].startswith('localhost:'):
          continue
        if h.lower() == 'custom' and self.headers[h] == 'ok':
          custom_header = True
          continue
        if (h.lower(), self.headers[h]) not in STANDARD_HEADERS:
          no_user_headers = False
          break
      if custom_header and no_user_headers:
        self.send_response(http_client.OK)
      else:
        self.send_response(http_client.BAD_REQUEST)
      self.end_headers()
    elif '/put_headers?' in self.path:
      self.send_response(http_client.OK)
      for n_v in self.path[self.path.find('?') + 1:].split('&'):
        name, value = list(map(urllib.parse.unquote, n_v.split('=', 1)))
        self.send_header(name, value)
      self.end_headers()
    elif self.path.endswith('/slow'):
      time.sleep(urlfetch_stub._API_CALL_DEADLINE + 0.1)
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self._write('slow')
    elif self.path.endswith('/tooslow'):
      time.sleep(urlfetch_stub._API_CALL_DEADLINE + 0.1)
      self.end_headers()
      try:
        self.send_response(http_client.OK)
      except socket.error:
        pass
      else:
        raise RuntimeError("expected socket.error")
    elif self.path.endswith('/with_content_length'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.send_header('Content-Length', 19)
      self.end_headers()
      self._write('with-content-length')
    elif self.path.endswith('/path;params'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self._write('path;params')
    elif '/status_code' in self.path:
      params = urllib.parse.parse_qs(
          urllib.parse.urlparse(self.path).query)
      self.send_response(int(params['code'][0]))
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
    else:
      self.send_response(http_client.NOT_FOUND,
                         'Not found: %s' % self.path)
      self.end_headers()

  def do_POST(self):
    """Handler for POST requests.

    Responds to POST requests for the path /good and /huge; otherwise returns
    httplib.NOT_FOUND. Will additionally echo the Extra-Header, Content-Type,
    and post payload in the output.
    """
    if self.path.endswith('/good'):
      self.send_response(http_client.OK)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      payload = six.ensure_str(
          self.rfile.read(int(self.headers['Content-Length'])))
      self._write('%s, content-type=%s, payload=%s' % (self.headers.get(
          'Extra-Header', 'good'), self.headers.get('Content-Type'), payload))
    elif self.path.endswith('/redirect_post'):
      self.send_response(http_client.FOUND)
      redirect_url = 'http://%s/redirect/3' % self.headers.get('host')
      self.send_header('Location', redirect_url)
      self.end_headers()
    elif self.path.endswith('/redirect_three_oh_seven'):
      self.send_response(http_client.TEMPORARY_REDIRECT)
      redirect_url = 'http://%s/good' % self.headers.get('Host')
      self.send_header('Location', redirect_url)
      self.end_headers()
    elif '/redirect/' in self.path:
      offset = self.path.find('/redirect/') + len('/redirect/')
      if(self.path.find("?") >= 0):
        query_string = self.path[self.path.find('?'):]
        count = int(self.path[offset:self.path.find('?')])
      else:
        count = int(self.path[offset:])
        query_string = ""
      self.send_response(http_client.FOUND)
      redirect_url = 'http://%s' % self.headers.get('host')
      if count == 0:
        self.send_header('Location', redirect_url + '/good' + query_string)
      else:
        self.send_header('Location', '%s/redirect/%d%s' %
                         (redirect_url, count - 1, query_string) )
      self.end_headers()
    else:
      self.send_response(http_client.NOT_FOUND,
                         'Not found: %s' % self.path)
      self.end_headers()

  def do_HEAD(self):
    """Handler for HEAD requests."""
    if self.path.endswith('/chunked'):
      self.send_response(http_client.OK)
      self.send_header('Transfer-Encoding', 'chunked')
      self.end_headers()
      self.wfile.flush()
      time.sleep(urlfetch_stub._API_CALL_DEADLINE + 0.1)
    elif self.path.endswith('/with_content_length'):
      self.send_response(http_client.OK)
      self.send_header('Content-Length', 19)
      self.end_headers()
    else:
      self.send_response(http_client.OK)
      self.end_headers()

  def do_PUT(self):
    """Handler for PUT requests."""
    self.send_response(http_client.OK)
    self.end_headers()

  def do_DELETE(self):
    """Handler for DELETE requests."""
    self.send_response(http_client.OK)
    self.end_headers()

  def do_PATCH(self):
    """Handler for PATCH requests."""
    self.send_response(http_client.OK)
    self.end_headers()

  def do_CONNECT(self):
    """Handler for CONNECT requests to the HTTPS proxy."""
    self.send_response(http_client.OK)
    self.end_headers()

  def _write(self, value):
    self.wfile.write(six.ensure_binary(value))


class URLFetchTestBase(absltest.TestCase):
  """Tests of the URLFetchServiceStub.

  We execute various fetch requests through the urlfetch.Fetch interface, which
  will then be intercepted by the URLFetchServiceStub. The receiver of the fetch
  is a dummy HTTP server we run locally in a separate thread, which is designed
  to echo the incoming HTTP request so we can validate that requests are
  correctly sent. As such, this is really an integration test to verify that
  urlfetch.fetch() works when combined with URLFetchServiceStub; it does not
  test the case when urlfetch.fetch() is used against the AppServer's
  implementation of URLFetchService.
  """

  def setUp(self):
    """Setup test fixture."""


    logging.getLogger().setLevel(logging.CRITICAL + 1)


    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub(
      'urlfetch', urlfetch_stub.URLFetchServiceStub())
    self.urlfetch_stub = apiproxy_stub_map.apiproxy.GetStub('urlfetch')

    self.mox = mox.Mox()


    self._http_server = None
    self._http_server_shutdown = False
    self._http_thread = None
    self._SetupHTTPServer()

  def tearDown(self):
    """Tear down test fixture."""
    self.mox.UnsetStubs()


    self._http_server_shutdown = True
    if self._http_thread is not None and self._http_thread.isAlive():
      self._http_thread.join()

  def _SetupHTTPServer(self):
    """Setup an HTTP server based on MockHTTPHandler in it's own thread."""
    http_server = IPv6CompatibleHTTPServer(('', 0), MockHTTPHandler)
    self._port = http_server.server_port

    def http_server_loop():
      while not self._http_server_shutdown:
        read_fd = http_server.fileno()
        read, write, exc = select.select([read_fd], [], [], 0.2)
        if read:
          http_server.handle_request()
      http_server.server_close()

    self._http_thread = threading.Thread(target=http_server_loop)
    self._http_thread.setDaemon(True)
    self._http_thread.start()

  def MakeHost(self):
    """Constructs the host."""
    return 'localhost:%d' % self._port

  def MakeURL(self, path, protocol='http'):
    """Constructs an URL from provided components.

    Args:
      path: The desired URL path.
      protocol: The desired URL protocol.

    Returns:
      An URL which will hit the locally running test webserver, based on the
      provided URL components.
    """
    return '%s://%s%s' % (protocol, self.MakeHost(), path)


class RepeatedDict(object):
  """Work around for using repeated headers within urlfetch's use of a dict.

  Using a standard dict typically precludes the ability to provide multiple
  headers with the same name. This class allows repeated headers and is used
  as:

  repeated_dict = RepeatedDict({"Repeated-Header": ["Value1", "Value2"]})
  for key, value in repeated_dict.iteritems():
    print key, value

  --> "Repeated-Header", "Value1"
  --> "Repeated-Header", "Value2"
  """

  def __init__(self, dictionary=None):
    self.dict = dictionary or {}

  def iteritems(self):
    for key, list_of_values in six.iteritems(self.dict):
      for value in list_of_values:
        yield (key, value)

  def items(self):
    return self.iteritems()
