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


"""OAuth API.

A service that enables App Engine apps to validate OAuth requests.

Classes defined here:

- `Error`: base exception type
- `NotAllowedError`: OAuthService exception
- `OAuthRequestError`: OAuthService exception
- `InvalidOAuthParametersError`: OAuthService exception
- `InvalidOAuthTokenError`: OAuthService exception
- `OAuthServiceFailureError`: OAuthService exception
"""

import contextvars
import json
import os
import six

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import user_service_pb2
from google.appengine.api import users
from google.appengine.runtime import apiproxy_errors












_OAUTH_AUTH_DOMAIN = contextvars.ContextVar('OAUTH_AUTH_DOMAIN')
_OAUTH_EMAIL = contextvars.ContextVar('OAUTH_EMAIL')
_OAUTH_USER_ID = contextvars.ContextVar('OAUTH_USER_ID')
_OAUTH_CLIENT_ID = contextvars.ContextVar('OAUTH_CLIENT_ID')
_OAUTH_IS_ADMIN = contextvars.ContextVar('OAUTH_IS_ADMIN')
_OAUTH_ERROR_CODE = contextvars.ContextVar('OAUTH_ERROR_CODE')
_OAUTH_ERROR_DETAIL = contextvars.ContextVar('OAUTH_ERROR_DETAIL')
_OAUTH_LAST_SCOPE = contextvars.ContextVar('OAUTH_LAST_SCOPE')
_OAUTH_AUTHORIZED_SCOPES = contextvars.ContextVar('OAUTH_AUTHORIZED_SCOPES')

_TESTBED_RESET_TOKENS = dict()


class Error(Exception):
  """Base error class for this module."""


class OAuthRequestError(Error):
  """Base error type for invalid OAuth requests."""


class NotAllowedError(OAuthRequestError):
  """Raised if the requested URL does not permit OAuth authentication."""


class InvalidOAuthParametersError(OAuthRequestError):
  """Raised if the request was a malformed OAuth request.

  For example, the request may have omitted a required parameter, contained
  an invalid signature, or was made by an unknown consumer.
  """


class InvalidOAuthTokenError(OAuthRequestError):
  """Raised if the request contained an invalid token.

  For example, the token may have been revoked by the user.
  """


class OAuthServiceFailureError(Error):
  """Raised if there was a problem communicating with the OAuth service."""


def get_current_user(_scope=None):
  """Returns the User on whose behalf the request was made.

  Args:
    _scope: The custom OAuth scope or an iterable of scopes at least one of
      which is accepted.

  Returns:
    User

  Raises:
    OAuthRequestError: The request was not a valid OAuth request.
    OAuthServiceFailureError: An unknown error occurred.
  """

  _maybe_call_get_oauth_user(_scope)
  return _get_user_from_environ()


def is_current_user_admin(_scope=None):
  """Returns true if the User on whose behalf the request was made is an admin.

  Args:
    _scope: The custom OAuth scope or an iterable of scopes at least one of
      which is accepted.

  Returns:
    Boolean.

  Raises:
    OAuthRequestError: The request was not a valid OAuth request.
    OAuthServiceFailureError: An unknown error occurred.
  """

  _maybe_call_get_oauth_user(_scope)
  return _OAUTH_IS_ADMIN.get(None)


def get_oauth_consumer_key():
  """OAuth1 authentication is deprecated and turned down."""



  raise InvalidOAuthParametersError('Two-legged OAuth1 not supported any more')


def get_client_id(_scope):
  """Returns the value of OAuth2 Client ID from an OAuth2 request.

  Args:
    _scope: The custom OAuth scope or an iterable of scopes at least one of
      which is accepted.

  Returns:
    string: The value of Client ID.

  Raises:
    OAuthRequestError: The request was not a valid OAuth2 request.
    OAuthServiceFailureError: An unknown error occurred.
  """
  _maybe_call_get_oauth_user(_scope)
  return _get_client_id_from_environ()


def get_authorized_scopes(scope):
  """Returns authorized scopes from input scopes.

  Args:
    scope: The custom OAuth scope or an iterable of scopes at least one of
      which is accepted.

  Returns:
    list: A list of authorized OAuth2 scopes

  Raises:
    OAuthRequestError: The request was not a valid OAuth2 request.
    OAuthServiceFailureError: An unknown error occurred
  """
  _maybe_call_get_oauth_user(scope)
  return _get_authorized_scopes_from_environ()


def _maybe_call_get_oauth_user(scope):
  """Makes an GetOAuthUser RPC and stores the results in context.

  This method will only make the RPC if 'OAUTH_ERROR_CODE' has not already
  been set or 'OAUTH_LAST_SCOPE' is different to str(_scopes).

  Args:
    scope: The custom OAuth scope or an iterable of scopes at least one of which
      is accepted.
  """

  if not scope:
    scope_str = ''
  elif isinstance(scope, six.string_types):
    scope_str = scope
  else:
    scope_str = str(sorted(scope))
  if (_OAUTH_ERROR_CODE.get(None) is None or
      _OAUTH_LAST_SCOPE.get(None) != scope_str or
      os.environ.get('TESTONLY_OAUTH_SKIP_CACHE')):
    req = user_service_pb2.GetOAuthUserRequest()
    if scope:
      if isinstance(scope, six.string_types):
        req.scopes.append(scope)
      else:
        req.scopes.extend(scope)

    resp = user_service_pb2.GetOAuthUserResponse()
    try:
      apiproxy_stub_map.MakeSyncCall('user', 'GetOAuthUser', req, resp)
      token = _OAUTH_EMAIL.set(resp.email)
      _TESTBED_RESET_TOKENS[_OAUTH_EMAIL] = token
      token = _OAUTH_AUTH_DOMAIN.set(resp.auth_domain)
      _TESTBED_RESET_TOKENS[_OAUTH_AUTH_DOMAIN] = token
      token = _OAUTH_USER_ID.set(resp.user_id)
      _TESTBED_RESET_TOKENS[_OAUTH_USER_ID] = token
      token = _OAUTH_CLIENT_ID.set(resp.client_id)
      _TESTBED_RESET_TOKENS[_OAUTH_CLIENT_ID] = token
      token = _OAUTH_AUTHORIZED_SCOPES.set(json.dumps(list(resp.scopes)))
      _TESTBED_RESET_TOKENS[_OAUTH_AUTHORIZED_SCOPES] = token
      token = _OAUTH_IS_ADMIN.set(resp.is_admin)
      _TESTBED_RESET_TOKENS[_OAUTH_IS_ADMIN] = token
      token = _OAUTH_ERROR_CODE.set('')
      _TESTBED_RESET_TOKENS[_OAUTH_ERROR_CODE] = token
    except apiproxy_errors.ApplicationError as e:
      token = _OAUTH_ERROR_CODE.set(str(e.application_error))
      _TESTBED_RESET_TOKENS[_OAUTH_ERROR_CODE] = token
      token = _OAUTH_ERROR_DETAIL.set(e.error_detail)
      _TESTBED_RESET_TOKENS[_OAUTH_ERROR_DETAIL] = token
    token = _OAUTH_LAST_SCOPE.set(scope_str)
    _TESTBED_RESET_TOKENS[_OAUTH_LAST_SCOPE] = token
  _maybe_raise_exception()


def _maybe_raise_exception():
  """Raises an error if one has been stored in context.

  This method requires that 'OAUTH_ERROR_CODE' has already been set (an empty
  string indicates that there is no actual error).
  """
  error = _OAUTH_ERROR_CODE.get()
  if error:
    error_detail = _OAUTH_ERROR_DETAIL.get()
    if error == str(user_service_pb2.UserServiceError.NOT_ALLOWED):
      raise NotAllowedError(error_detail)
    elif error == str(user_service_pb2.UserServiceError.OAUTH_INVALID_REQUEST):
      raise InvalidOAuthParametersError(error_detail)
    elif error == str(user_service_pb2.UserServiceError.OAUTH_INVALID_TOKEN):
      raise InvalidOAuthTokenError(error_detail)
    elif error == str(user_service_pb2.UserServiceError.OAUTH_ERROR):
      raise OAuthServiceFailureError(error_detail)
    else:
      raise OAuthServiceFailureError(error_detail)


def _get_user_from_environ():
  """Returns a User based on values stored in context.

  This method requires that 'OAUTH_EMAIL', 'OAUTH_AUTH_DOMAIN', and
  'OAUTH_USER_ID' have already been set.

  Returns:
    User
  """
  return users.User(
      email=_OAUTH_EMAIL.get(),
      _auth_domain=_OAUTH_AUTH_DOMAIN.get(),
      _user_id=_OAUTH_USER_ID.get())


def _get_client_id_from_environ():
  """Returns Client ID based on values stored in context.

  This method requires that 'OAUTH_CLIENT_ID' has already been set.

  Returns:
    string: the value of Client ID.
  """
  return _OAUTH_CLIENT_ID.get()


def _get_authorized_scopes_from_environ():
  """Returns authorized scopes based on values stored in context.

  This method requires that 'OAUTH_AUTHORIZED_SCOPES' has already been set.

  Returns:
    list: the list of OAuth scopes.
  """

  return json.loads(_OAUTH_AUTHORIZED_SCOPES.get())
