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




"""The User Python datastore class to be used as a datastore data type."""







from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import os

import six

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import user_service_pb2
from google.appengine.runtime import apiproxy_errors








class Error(Exception):
  """Base User error type."""


class UserNotFoundError(Error):
  """No email argument was specified, and no user is logged in."""


class RedirectTooLongError(Error):
  """The generated redirect URL was too long."""


class NotAllowedError(Error):
  """The requested redirect URL is not allowed."""


@functools.total_ordering
class User(object):
  """Provides the email address, nickname, and ID for a user.

  A nickname is a human-readable string that uniquely identifies a Google user,
  akin to a username. For some users, this nickname is an email address, but for
  other users, a different nickname is used.

  A user is a Google Accounts user.

  `federated_identity` and `federated_provider` are decommissioned and should
  not be used.
  """





  __user_id = None
  __federated_identity = None
  __federated_provider = None

  def __init__(self, email=None, _auth_domain=None,
               _user_id=None, federated_identity=None, federated_provider=None,
               _strict_mode=True):
    """Constructor.

    Args:
      email: An optional string of the user's email address. It defaults to
          the current user's email address.
      federated_identity: Decommissioned, don't use.
      federated_provider: Decommissioned, don't use.

    Raises:
      UserNotFoundError: If the user is not logged in and both `email` and
          `federated_identity` are empty.
    """







    if _auth_domain is None:
      _auth_domain = os.environ.get('AUTH_DOMAIN')
    assert _auth_domain

    if email is None and federated_identity is None:
      email = os.environ.get('USER_EMAIL', email)
      _user_id = os.environ.get('USER_ID', _user_id)
      federated_identity = os.environ.get('FEDERATED_IDENTITY',
                                          federated_identity)
      federated_provider = os.environ.get('FEDERATED_PROVIDER',
                                          federated_provider)





    if email is None:
      email = ''

    if not email and not federated_identity and _strict_mode:


      raise UserNotFoundError

    self.__email = email
    self.__federated_identity = federated_identity
    self.__federated_provider = federated_provider
    self.__auth_domain = _auth_domain
    self.__user_id = _user_id or None


  def nickname(self):
    """Returns the user's nickname.

    The nickname will be a unique, human readable identifier for this user with
    respect to this application. It will be an email address for some users,
    and part of the email address for some users.

    Returns:
      The nickname of the user as a string.
    """
    if (self.__email and self.__auth_domain and
        self.__email.endswith('@' + self.__auth_domain)):
      suffix_len = len(self.__auth_domain) + 1
      return self.__email[:-suffix_len]
    elif self.__federated_identity:
      return self.__federated_identity
    else:
      return self.__email

  def email(self):
    """Returns the user's email address."""
    return self.__email

  def user_id(self):
    """Obtains the user ID of the user.

    Returns:
      A permanent unique identifying string or `None`. If the email address was
      set explicitly, this will return `None`.
    """
    return self.__user_id

  def auth_domain(self):
    """Obtains the user's authentication domain.

    Returns:
      A string containing the authentication domain. This method is internal and
      should not be used by client applications.
    """
    return self.__auth_domain

  def federated_identity(self):
    """Decommissioned, don't use.

    Returns:
      A string containing the federated identity of the user. If the user is not
      a federated user, `None` is returned.
    """
    return self.__federated_identity

  def federated_provider(self):
    """Decommissioned, don't use.

    Returns:
      A string containing the federated provider. If the user is not a federated
      user, `None` is returned.
    """
    return self.__federated_provider

  def __unicode__(self):
    return six.text_type(self.nickname())

  def __str__(self):
    return str(self.nickname())

  def __repr__(self):
    values = []
    if self.__email:
      values.append("email='%s'" % self.__email)
    if self.__federated_identity:
      values.append("federated_identity='%s'" % self.__federated_identity)
    if self.__user_id:
      values.append("_user_id='%s'" % self.__user_id)
    return 'users.User(%s)' % ','.join(values)

  def __hash__(self):
    if self.__federated_identity:
      return hash((self.__federated_identity, self.__auth_domain))
    else:
      return hash((self.__email, self.__auth_domain))

  def __eq__(self, other):
    if not isinstance(other, User):
      return NotImplemented

    if self.__federated_identity:
      return ((self.__federated_identity,
               self.__auth_domain) == (other.__federated_identity,
                                       other.__auth_domain))

    return ((self.__email, self.__auth_domain) == (other.__email,
                                                   other.__auth_domain))

  def __ne__(self, other):
    return not self == other

  def __lt__(self, other):

    if self.__federated_identity:
      return ((self.__federated_identity, self.__auth_domain) <
              (other.__federated_identity, other.__auth_domain))

    return ((self.__email, self.__auth_domain) <
            (other.__email, other.__auth_domain))


def create_login_url(dest_url=None, _auth_domain=None,
                     federated_identity=None):
  """Computes the login URL for redirection.

  Args:
    dest_url: String that is the desired final destination URL for the user
        once login is complete. If `dest_url` does not specify a host, the host
        from the current request is used.
    federated_identity: Decommissioned, don't use. Setting this to a non-None
        value raises a NotAllowedError

  Returns:
       Login URL as a string. The login URL will use Google Accounts.

  Raises:
      NotAllowedError: If federated_identity is not None.
  """
  req = user_service_pb2.CreateLoginURLRequest()
  resp = user_service_pb2.CreateLoginURLResponse()
  if dest_url:
    req.destination_url = dest_url
  else:
    req.destination_url = ''
  if _auth_domain:
    req.auth_domain = _auth_domain
  if federated_identity:
    raise NotAllowedError('OpenID 2.0 support is decomissioned')

  try:
    apiproxy_stub_map.MakeSyncCall('user', 'CreateLoginURL', req, resp)
  except apiproxy_errors.ApplicationError as e:
    if (e.application_error ==
        user_service_pb2.UserServiceError.REDIRECT_URL_TOO_LONG):
      raise RedirectTooLongError
    elif (e.application_error ==
          user_service_pb2.UserServiceError.NOT_ALLOWED):
      raise NotAllowedError
    else:
      raise e
  return resp.login_url


CreateLoginURL = create_login_url





def create_logout_url(dest_url, _auth_domain=None):
  """Computes the logout URL and specified destination URL for the request.

  This function works for Google Accounts applications.

  Args:
    dest_url: String that is the desired final destination URL for the user
        after the user has logged out. If `dest_url` does not specify a host,
        the host from the current request is used.

  Returns:
    Logout URL as a string.
  """
  req = user_service_pb2.CreateLogoutURLRequest()
  resp = user_service_pb2.CreateLogoutURLResponse()
  req.destination_url = dest_url
  if _auth_domain:
    req.auth_domain = _auth_domain

  try:
    apiproxy_stub_map.MakeSyncCall('user', 'CreateLogoutURL', req, resp)
  except apiproxy_errors.ApplicationError as e:
    if (e.application_error ==
        user_service_pb2.UserServiceError.REDIRECT_URL_TOO_LONG):
      raise RedirectTooLongError
    else:
      raise e
  return resp.logout_url


CreateLogoutURL = create_logout_url


def get_current_user():
  """Retrieves information associated with the user that is making a request.

  Returns:

  """
  try:
    return User()
  except UserNotFoundError:
    return None


GetCurrentUser = get_current_user


def is_current_user_admin():
  """Specifies whether the user making a request is an application admin.

  Because administrator status is not persisted in the datastore,
  `is_current_user_admin()` is a separate function rather than a member function
  of the `User` class. The status only exists for the user making the current
  request.

  Returns:
    `True` if the user is an administrator; all other user types return `False`.
  """
  return (os.environ.get('USER_IS_ADMIN', '0')) == '1'


IsCurrentUserAdmin = is_current_user_admin
