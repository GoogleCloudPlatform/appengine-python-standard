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


"""URL downloading API."""

import email
import os
import threading

import six
from six.moves import urllib
from six.moves import UserDict as IterableUserDict
import six.moves.http_client
import six.moves.urllib.parse

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import urlfetch_service_pb2
from google.appengine.api.urlfetch_errors import *
from google.appengine.runtime import apiproxy_errors












MAX_REDIRECTS = 5


GET = 1
POST = 2
HEAD = 3
PUT = 4
DELETE = 5
PATCH = 6

_URL_STRING_MAP = {
    'GET': GET,
    'POST': POST,
    'HEAD': HEAD,
    'PUT': PUT,
    'DELETE': DELETE,
    'PATCH': PATCH,
}

_VALID_METHODS = frozenset(list(_URL_STRING_MAP.values()))

_thread_local_settings = threading.local()


class _CaselessDict(IterableUserDict):
  """Case insensitive `dict`.

  This class was lifted from os.py and slightly modified.
  """

  def __init__(self, dict=None, **kwargs):
    self.caseless_keys = {}
    IterableUserDict.__init__(self, dict, **kwargs)

  def __setitem__(self, key, item):
    """Sets `dict` item.

    Args:
      key: Key of new item. Key is case insensitive, so `d['Key'] = value` will
        replace previous values set by `d['key'] = old_value`.
      item: Item to store.
    """
    caseless_key = key.lower()

    if caseless_key in self.caseless_keys:
      del self.data[self.caseless_keys[caseless_key]]
    self.caseless_keys[caseless_key] = key
    self.data[key] = item

  def __getitem__(self, key):
    """Gets `dict` item.

    Args:
      key: Key of item to get. Key is case insensitive, so `d['Key']` is the
        same as `d['key']`.

    Returns:
      Item associated with `key`.

    Raises:
      KeyError: If the `key` is not found.
    """
    return self.data[self.caseless_keys[key.lower()]]

  def __delitem__(self, key):
    """Removes item from `dict`.

    Args:
      key: Key of item to remove.  Key is case insensitive, so `del d['Key']` is
        the same as `del d['key']`.
    """
    caseless_key = key.lower()
    del self.data[self.caseless_keys[caseless_key]]
    del self.caseless_keys[caseless_key]

  def has_key(self, key):
    """Determines if the `dict` has an item with a specific `key`.

    Args:
      key: Key to check for presence. Key is case insensitive, so
        `d.has_key('Key')` evaluates to the same value as `d.has_key('key')`.

    Returns:
      `True` if `dict` contains the specified `key`, else `False`.
    """
    return key.lower() in self.caseless_keys

  def __contains__(self, key):
    """Same as `has_key`, but used for `in` operator."""
    return self.has_key(key)

  def get(self, key, failobj=None):
    """Gets `dict` item, defaulting to another value if it does not exist.

    Args:
      key: Key of item to get. Key is case insensitive, so `d['Key']` is the
        same as `d['key']`.
      failobj: Value to return if key not in `dict`.

    Returns:
      A `dict` item.
    """
    try:
      cased_key = self.caseless_keys[key.lower()]
    except KeyError:
      return failobj
    return self.data[cased_key]

  def update(self, dict=None, **kwargs):
    """Updates the `dict` using values from another `dict` and keywords.

    Args:
      dict: Dictionary to update from.
      **kwargs: Keyword arguments to update from.
    """
    if dict:
      try:
        keys = list(dict.keys())
      except AttributeError:

        for k, v in dict:
          self[k] = v
      else:



        for k in keys:
          self[k] = dict[k]
    if kwargs:
      self.update(kwargs)

  def copy(self):
    """Makes a shallow, case-sensitive copy of `self`.

    Returns:
      A `dict` copy of `self`.
    """
    return dict(self)


def _is_fetching_self(url, method):
  """Checks if the fetch is for the same URL from which it originated.

  Args:
    url: `string`. The URL being fetched.
    method: Value from `_VALID_METHODS`.

  Returns:
    Boolean indicating whether or not it seems that the app is trying to fetch
        itself.
  """
  if (method != GET or
      "HTTP_HOST" not in os.environ or
      "PATH_INFO" not in os.environ):
    return False

  _, host_port, path, _, _ = six.moves.urllib.parse.urlsplit(url)

  if host_port == os.environ['HTTP_HOST']:

    current_path = urllib.parse.unquote(os.environ['PATH_INFO'])
    desired_path = urllib.parse.unquote(path)

    if (current_path == desired_path or
        (current_path in ('', '/') and desired_path in ('', '/'))):
      return True

  return False


def create_rpc(deadline=None, callback=None):
  """Creates an RPC object for use with the URL Fetch API.

  Args:
    deadline: Optional deadline in seconds for the operation; the default is a
      system-specific deadline (typically 5 seconds).
    callback: Optional callable to invoke on completion.

  Returns:
    An `apiproxy_stub_map.UserRPC` object specialized for this service.
  """
  if deadline is None:
    deadline = get_default_fetch_deadline()
  return apiproxy_stub_map.UserRPC('urlfetch', deadline, callback)


def fetch(url, payload=None, method=GET, headers={},
          allow_truncated=False, follow_redirects=True,
          deadline=None, validate_certificate=None):
  """Fetches the given HTTP `url`, blocking until the result is returned.

  URLs are fetched using one of the following HTTP methods:
      - `GET`
      - `POST`
      - `HEAD`
      - `PUT`
      - `DELETE`
      - `PATCH`

  To fetch the result, a HTTP/1.1-compliant proxy is used.

  Args:
    method: The constants `GET`, `POST`, `HEAD`, `PUT`, `DELETE`, or `PATCH` or
      the same `HTTP` methods as strings.
    payload: `POST`, `PUT`, or `PATCH` payload (implies method is not `GET`,
      `HEAD`, or `DELETE`). This argument is ignored if the method is not
      `POST`, `PUT`, or `PATCH`.
    headers: Dictionary of `HTTP` headers to send with the request.
    allow_truncated: If set to `True`, truncates large responses and returns
      them without raising an error. Otherwise, a `ResponseTooLargeError` is
      raised when a response is truncated.
    follow_redirects: If set to `True` (the default), redirects are
      transparently followed. If there are less than five redirects, the
      response contains the final destination's payload, and the response status
      is `200`. You lose, however, the redirect chain information. If set to
      `False`, you see the `HTTP` response yourself, including the `Location`
      header, and redirects are not followed.
    deadline: Deadline in seconds for the operation.
    validate_certificate: If set to `True`, requests are not sent to the server
      unless the certificate is valid, signed by a trusted `CA`, and the host
      name matches the certificate. A value of `None` (default) indicates that
      the behavior will be chosen by the underlying `urlfetch` implementation.

  Returns:
    object: An object containing following fields:

        - `content`: A `string` that contains the response from the server.
        - `status_code`: The `HTTP` status code that was returned by the server.
        - `headers`: The `dict` of headers that was returned by the server.

  Raises:
    urlfetch_errors.Error: If an error occurs. See the `urlfetch_errors` module
        for more information.


  Note:
      `HTTP` errors are returned as a part of the return structure. `HTTP`
      errors like `404` do not result in an exception. See `urlfetch_errors` for
      details.

  """

  payload = six.ensure_binary(payload, 'utf-8') if payload else None
  rpc = create_rpc(deadline=deadline)
  make_fetch_call(rpc, url, payload, method, headers,
                  allow_truncated, follow_redirects, validate_certificate)
  return rpc.get_result()


def make_fetch_call(rpc, url, payload=None, method=GET, headers={},
                    allow_truncated=False, follow_redirects=True,
                    validate_certificate=None):
  """Executes the RPC call to fetch a given `HTTP` URL.

  The first argument is a `UserRPC` instance.  See `urlfetch.fetch` for a
  thorough description of the remaining arguments.

  Raises:
    InvalidMethodError: If the requested method is not in `_VALID_METHODS`.
    ResponseTooLargeError: If the response payload is too large.
    InvalidURLError: If there are issues with the content or size of the
        requested `url`.

  Returns:
    The `rpc` object that was passed into the function.

  """

  assert rpc.service == 'urlfetch', repr(rpc.service)
  if isinstance(method, six.string_types):
    method = method.upper()
  method = _URL_STRING_MAP.get(method, method)
  if method not in _VALID_METHODS:
    raise InvalidMethodError('Invalid method %s.' % str(method))

  if _is_fetching_self(url, method):
    raise InvalidURLError('App cannot fetch '
                          'the same `url` as the one used for the request.')

  request = urlfetch_service_pb2.URLFetchRequest()
  response = urlfetch_service_pb2.URLFetchResponse()

  request.Url = url

  if method == GET:
    request.Method = urlfetch_service_pb2.URLFetchRequest.GET
  elif method == POST:
    request.Method = urlfetch_service_pb2.URLFetchRequest.POST
  elif method == HEAD:
    request.Method = urlfetch_service_pb2.URLFetchRequest.HEAD
  elif method == PUT:
    request.Method = urlfetch_service_pb2.URLFetchRequest.PUT
  elif method == DELETE:
    request.Method = urlfetch_service_pb2.URLFetchRequest.DELETE
  elif method == PATCH:
    request.Method = urlfetch_service_pb2.URLFetchRequest.PATCH


  if payload and method in (POST, PUT, PATCH):

    request.Payload = six.ensure_binary(payload, 'utf-8')


  for key, value in six.iteritems(headers):




    request.header.add(Key=key, Value=str(value))

  request.FollowRedirects = follow_redirects
  if validate_certificate is not None:
    request.MustValidateServerCertificate = validate_certificate

  if rpc.deadline is not None:
    request.Deadline = rpc.deadline



  rpc.make_call('Fetch', request, response, _get_fetch_result, allow_truncated)
  return rpc


def _get_fetch_result(rpc):
  """Checks for success, handles exceptions, and returns a converted RPC result.

  This method waits for the `rpc` if it has not yet finished and calls the
  post-call hooks on the first invocation.

  Args:
    rpc: A `UserRPC` object.

  Raises:
    InvalidURLError: If the URL was invalid.
    DownloadError: If there was a problem fetching the URL.
    PayloadTooLargeError: If the request and its payload was larger than the
        allowed limit.
    ResponseTooLargeError: If the response was either truncated (and
        `allow_truncated=False` was passed to `make_fetch_call()`), or if it
        was too big for us to download.
    MalformedReplyError: If an invalid `HTTP` response was returned.
    TooManyRedirectsError: If the redirect limit was hit while `follow_rediects`
        was set to `True`.
    InternalTransientError: An internal error occurred. Wait a few minutes, then
        try again.
    ConnectionClosedError: If the target server prematurely closed the
        connection.
    DNSLookupFailedError: If the `DNS` lookup for the URL failed.
    DeadlineExceededError: If the deadline was exceeded; occurs when the
        client-supplied `deadline` is invalid or if the client did not specify a
        `deadline` and the system default value is invalid.
    SSLCertificateError: If an invalid server certificate was presented.
    AssertionError: If the `assert` statement fails.

  Returns:
    A `_URLFetchResult` object.
  """
  assert rpc.service == 'urlfetch', repr(rpc.service)
  assert rpc.method == 'Fetch', repr(rpc.method)

  url = rpc.request.Url

  try:
    rpc.check_success()
  except apiproxy_errors.RequestTooLargeError as err:
    raise InvalidURLError(
        'Request body too large fetching URL: ' + url)
  except apiproxy_errors.ApplicationError as err:
    error_detail = ''
    if err.error_detail:
      error_detail = ' Error: ' + err.error_detail
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.INVALID_URL):
      raise InvalidURLError(
          'Invalid request URL: ' + url + error_detail)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.PAYLOAD_TOO_LARGE):

      raise PayloadTooLargeError(
          'Request exceeds 10 MiB limit for URL: ' + url)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.CLOSED):
      raise ConnectionClosedError(
          'Connection closed unexpectedly by server at URL: ' + url)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.TOO_MANY_REDIRECTS):
      raise TooManyRedirectsError(
          'Too many redirects at URL: ' + url + ' with redirect=true')
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.MALFORMED_REPLY):
      raise MalformedReplyError(
          'Malformed HTTP reply received from server at URL: '
          + url + error_detail)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.INTERNAL_TRANSIENT_ERROR):
      raise InternalTransientError(
          'Temporary error in fetching URL: ' + url + ', please re-try')
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.DNS_ERROR):
      raise DNSLookupFailedError('DNS lookup failed for URL: ' + url)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.UNSPECIFIED_ERROR):
      raise DownloadError('Unspecified error in fetching URL: '
                          + url + error_detail)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.FETCH_ERROR):
      raise DownloadError("Unable to fetch URL: " + url + error_detail)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.RESPONSE_TOO_LARGE):
      raise ResponseTooLargeError('HTTP response too large from URL: ' + url)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.DEADLINE_EXCEEDED):
      raise DeadlineExceededError(
          'Deadline exceeded while waiting for HTTP response from URL: ' + url)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.SSL_CERTIFICATE_ERROR):
      raise SSLCertificateError(
          'Invalid and/or missing SSL certificate for URL: ' + url)
    if (err.application_error ==
        urlfetch_service_pb2.URLFetchServiceError.CONNECTION_ERROR):
      raise DownloadError('Unable to connect to server at URL: ' + url)

    raise err

  response = rpc.response
  allow_truncated = rpc.user_data
  result = _URLFetchResult(response)
  if response.ContentWasTruncated and not allow_truncated:
    raise ResponseTooLargeError(result)
  return result


Fetch = fetch


def CreateHTTPHeaders(data):
  """Creates `HTTPHeaders` that are compatible with both Python 2 or Python 3."""
  if six.PY2:
    return six.moves.http_client.HTTPMessage(six.StringIO(data))
  else:
    return email.parser.HeaderParser(HTTPMessageWrapper).parsestr(data)




class HTTPMessageWrapper(six.moves.http_client.HTTPMessage):

  def getheaders(self, key):
    return self.get_all(key)

  @property
  def type(self):
    return self.get('content-type').split(';')[0]


class _URLFetchResult(object):
  """A Pythonic representation of our fetch response protocol buffer."""

  def __init__(self, response_proto):
    """Constructor.

    Args:
      response_proto: The `URLFetchResponse` protocol buffer to wrap.
    """
    self.__pb = response_proto
    self.content = response_proto.Content
    self.status_code = response_proto.StatusCode
    self.content_was_truncated = response_proto.ContentWasTruncated
    self.final_url = response_proto.FinalUrl or None

    data = ''.join(
        ['%s: %s\n' % (h.Key, h.Value) for h in response_proto.header] + ['\n'])
    self.header_msg = CreateHTTPHeaders(data)




    header_keys_values = [(key, self.header_msg.getheaders(key))
                          for key in self.header_msg.keys()]
    header_list = [
        (key, ', '.join(values)) for (key, values) in header_keys_values
    ]
    self.headers = _CaselessDict(header_list)


def get_default_fetch_deadline():
  """Gets the default value for `create_rpc()`'s `deadline` parameter."""
  return getattr(_thread_local_settings, "default_fetch_deadline", None)


def set_default_fetch_deadline(value):
  """Sets the default value for `create_rpc()`'s `deadline` parameter.

  This setting is thread-specific, meaning it that is stored in a thread local.
  This function doesn't check the type or range of the value.  The default
  value is `None`.

  See also: `create_rpc()`, `fetch()`

  Args:
    value: The default value that you want to use for the `deadline` parameter
        of `create_rpc()`.

  """
  _thread_local_settings.default_fetch_deadline = value
