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


"""Unit tests for the stub OAuth API."""




from google.appengine.api import apiproxy_stub_map
from google.appengine.api import module_testutil
from google.appengine.api import oauth
from google.appengine.api import user_service_pb2
from google.appengine.api import user_service_stub
from google.appengine.runtime import apiproxy_errors
from google.appengine.runtime.context import ctx_test_util
from absl.testing import absltest


class ModuleInterfaceTest(module_testutil.ModuleInterfaceTest,
                          absltest.TestCase):
  """Test the module interface for consistency."""

  MODULE = oauth


@ctx_test_util.isolated_context()
class OAuthApiTest(absltest.TestCase):

  def setUp(self):
    self.users_stub = user_service_stub.UserServiceStub()
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    apiproxy_stub_map.apiproxy.RegisterStub('user', self.users_stub)

  def testGetCurrentUserSuccess(self):
    user = oauth.get_current_user()
    self.assertEqual('example@example.com', user.email())
    self.assertEqual('0', user.user_id())
    self.assertEqual('gmail.com', user.auth_domain())

  def testGetCurrentUserCaches(self):
    user1 = oauth.get_current_user()
    self.assertEqual('example@example.com', user1.email())

    user2 = oauth.get_current_user()
    self.assertEqual(user1, user2)

  def testGetCurrentUserCachesErrors(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.NOT_ALLOWED, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.NotAllowedError, 'error details',
                                      oauth.get_current_user)
    self.assertRaisesWithLiteralMatch(oauth.NotAllowedError, 'error details',
                                      oauth.get_current_user)
    self.assertRaisesWithLiteralMatch(oauth.NotAllowedError, 'error details',
                                      oauth.get_current_user)

  def testGetCurrentUserDifferentScopes(self):
    user1 = oauth.get_current_user()
    self.assertEqual('example@example.com', user1.email())



    self.users_stub.SetOAuthUser('example2@example.com')
    user2 = oauth.get_current_user('custom scope')
    self.assertNotEqual(user1, user2)



    self.users_stub.SetOAuthUser('example3@example.com')
    user3 = oauth.get_current_user()
    self.assertNotEqual(user3, user2)

    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.NOT_ALLOWED, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.NotAllowedError, 'error details',
                                      oauth.get_current_user, 'custom scope')


    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_INVALID_REQUEST,
        'error details'))
    self.assertRaisesWithLiteralMatch(
        oauth.InvalidOAuthParametersError, 'error details',
        oauth.get_current_user, 'another scope')


    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_INVALID_TOKEN, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.InvalidOAuthTokenError,
                                      'error details', oauth.get_current_user)

  def testGetCurrentUserNotAllowed(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.NOT_ALLOWED, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.NotAllowedError, 'error details',
                                      oauth.get_current_user)

  def testGetCurrentUserInvalidRequest(self):
    self.users_stub.SetOAuthUser(None)
    self.assertRaises(oauth.InvalidOAuthParametersError, oauth.get_current_user)

  def testGetCurrentUserInvalidToken(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_INVALID_TOKEN, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.InvalidOAuthTokenError,
                                      'error details', oauth.get_current_user)

  def testGetCurrentUserError(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_ERROR, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.OAuthServiceFailureError,
                                      'error details', oauth.get_current_user)

  def testGetCurrentUserUnknownError(self):

    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.REDIRECT_URL_TOO_LONG,
        'error details'))
    self.assertRaisesWithLiteralMatch(oauth.OAuthServiceFailureError,
                                      'error details', oauth.get_current_user)

  def testIsCurrentUserAdminIsNotAdmin(self):
    self.assertFalse(oauth.is_current_user_admin())
    self.assertFalse(oauth.is_current_user_admin())

  def testIsCurrentUserAdminIsAdmin(self):
    self.users_stub.SetOAuthUser(email='foo@google.com',
                                 domain='google.com',
                                 is_admin=True)

    self.assertTrue(oauth.is_current_user_admin())
    self.assertTrue(oauth.is_current_user_admin())

  def testIsCurrentUserAdminNotAllowed(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.NOT_ALLOWED, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.NotAllowedError, 'error details',
                                      oauth.get_current_user)

  def testIsCurrentUserAdminInvalidRequest(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_INVALID_REQUEST,
        'error details'))
    self.assertRaisesWithLiteralMatch(oauth.InvalidOAuthParametersError,
                                      'error details', oauth.get_current_user)

  def testIsCurrentUserAdminInvalidToken(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_INVALID_TOKEN,
        'error details'))
    self.assertRaisesWithLiteralMatch(oauth.InvalidOAuthTokenError,
                                      'error details', oauth.get_current_user)

  def testIsCurrentUserAdminError(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_ERROR, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.OAuthServiceFailureError,
                                      'error details', oauth.get_current_user)

  def testIsCurrentUserAdminUnknownError(self):

    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.REDIRECT_URL_TOO_LONG,
        'error details'))
    self.assertRaisesWithLiteralMatch(oauth.OAuthServiceFailureError,
                                      'error details', oauth.get_current_user)

  def testGetOAuthConsumerKeyInvalidRequest(self):
    self.assertRaisesWithLiteralMatch(
        oauth.InvalidOAuthParametersError,
        'Two-legged OAuth1 not supported any more',
        oauth.get_oauth_consumer_key)

  def testSetOAuthUserAdmin(self):
    self.users_stub.SetOAuthUser(email='foo@google.com',
                                 domain='google.com',
                                 is_admin=True)
    self.assertTrue(oauth.is_current_user_admin())

  def testSetScopeNoParameter(self):
    self.users_stub.SetOAuthUser(email='foo@google.com',
                                 domain='google.com',
                                 scopes=['https://www.mynet.net/myscope'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_current_user)

  def testSetScopeUnauthorized(self):
    self.users_stub.SetOAuthUser(email='foo@google.com',
                                 domain='google.com',
                                 scopes=['https://www.mynet.net/myscope'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_current_user,
                      'http://www.mynet.net/other')

  def testSetScopeAuthorized(self):
    self.users_stub.SetOAuthUser(email='foo@google.com',
                                 domain='google.com',
                                 scopes=['https://www.mynet.net/myscope'])
    user = oauth.get_current_user('https://www.mynet.net/myscope')
    self.assertEqual('foo@google.com', user.email())

  def testGetClientIdSuccess(self):
    self.users_stub.SetOAuthUser(scopes=['https://www.mynet.net/myscope'])
    client_id = oauth.get_client_id('https://www.mynet.net/myscope')
    self.assertEqual('123456789.apps.googleusercontent.com', client_id)

  def testGetClientIdUnauthorized(self):
    self.users_stub.SetOAuthUser(scopes=['https://www.mynet.net/myscope'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_current_user,
                      'http://www.mynet.net/other')

  def testGetClientIdCache(self):
    self.users_stub.SetOAuthUser(scopes=['https://www.mynet.net/myscope'])
    client_id = oauth.get_client_id('https://www.mynet.net/myscope')
    self.assertEqual('123456789.apps.googleusercontent.com', client_id)

    self.users_stub.SetOAuthUser(client_id='another_client_id')
    client_id = oauth.get_client_id('https://www.mynet.net/myscope')
    self.assertEqual('123456789.apps.googleusercontent.com', client_id)

  def testGetClientIdCacheSharedWithGetCurrentUser(self):
    self.users_stub.SetOAuthUser(scopes=['https://www.mynet.net/myscope'])
    oauth.get_current_user('https://www.mynet.net/myscope')
    self.users_stub.SetOAuthUser(client_id='another_client_id')
    client_id = oauth.get_client_id('https://www.mynet.net/myscope')
    self.assertEqual('123456789.apps.googleusercontent.com', client_id)

  def testGetClientIdCacheError(self):
    self.users_stub.SetOAuthUser(scopes=['https://www.mynet.net/myscope'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_client_id,
                      'http://www.mynet.net/other')

    self.users_stub.SetOAuthUser(scopes=['https://www.mynet.net/other'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_client_id,
                      'http://www.mynet.net/other')

  def testGetClientIdDifferentScope(self):
    self.users_stub.SetOAuthUser(scopes=['https://www.mynet.net/myscope',
                                         'https://www.mynet.net/other'])
    client_id = oauth.get_client_id('https://www.mynet.net/myscope')
    self.assertEqual('123456789.apps.googleusercontent.com', client_id)

    self.users_stub.SetOAuthUser(client_id='another_client_id')
    client_id = oauth.get_client_id('https://www.mynet.net/other')
    self.assertEqual('another_client_id', client_id)

  def testGetClientIdNotAllowed(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.NOT_ALLOWED, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.NotAllowedError, 'error details',
                                      oauth.get_client_id, 'fake_scope')

  def testGetClientIdInvalidRequest(self):
    self.users_stub.SetOAuthUser(None)
    self.assertRaises(oauth.InvalidOAuthParametersError, oauth.get_client_id,
                      'fake_scope')

  def testGetClientIdInvalidToken(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_INVALID_TOKEN, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.InvalidOAuthTokenError,
                                      'error details', oauth.get_client_id,
                                      'fake_scope')

  def testGetClientIdError(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_ERROR, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.OAuthServiceFailureError,
                                      'error details', oauth.get_client_id,
                                      'fake_scope')

  def testGetClientIdUnknownError(self):

    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.REDIRECT_URL_TOO_LONG,
        'error details'))
    self.assertRaisesWithLiteralMatch(oauth.OAuthServiceFailureError,
                                      'error details', oauth.get_client_id,
                                      'fake_scope')

  def testMultipleScopesSuccess(self):
    self.users_stub.SetOAuthUser(scopes=['scope1', 'scope2', 'scope3'])
    authorized_scopes = oauth.get_authorized_scopes(
        ('scope1', 'scope2', 'scope4'))
    client_id = oauth.get_client_id(('scope1', 'scope2', 'scope4'))
    user = oauth.get_current_user(['scope1', 'scope2', 'scope5'])
    self.assertCountEqual(['scope1', 'scope2'], authorized_scopes)
    self.assertEqual('123456789.apps.googleusercontent.com', client_id)
    self.assertEqual('example@example.com', user.email())
    self.assertEqual('0', user.user_id())
    self.assertEqual('gmail.com', user.auth_domain())
    self.assertFalse(oauth.is_current_user_admin(('scope1', 'scope2')))

    authorized_scopes = oauth.get_authorized_scopes(
        ['scope1', 'scope2', 'scope4'])
    client_id = oauth.get_client_id(['scope1', 'scope2', 'scope4'])
    user = oauth.get_current_user(['scope1', 'scope2', 'scope4'])
    self.assertCountEqual(['scope1', 'scope2'], authorized_scopes)
    self.assertEqual('123456789.apps.googleusercontent.com', client_id)
    self.assertEqual('example@example.com', user.email())
    self.assertEqual('0', user.user_id())
    self.assertEqual('gmail.com', user.auth_domain())
    self.assertFalse(oauth.is_current_user_admin(('scope1', 'scope2')))

  def testMultipleScopesUnauthorized(self):
    self.users_stub.SetOAuthUser(scopes=['scope1', 'scope2'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_authorized_scopes,
                      ['scope3', 'scope4'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_authorized_scopes,
                      'scope3')
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_client_id,
                      ('scope3', 'scope4'))
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_client_id,
                      'scope3')
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_current_user,
                      ['scope3', 'scope4'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_current_user,
                      'scope3')
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.is_current_user_admin,
                      ('scope3', 'scope4'))
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.is_current_user_admin,
                      'scope3')

  def testGetAuthorizedScopesCache(self):
    self.users_stub.SetOAuthUser(scopes=['scope1', 'scope2'])
    authorized_scopes = oauth.get_authorized_scopes(('scope1', 'scope3'))
    self.assertCountEqual(['scope1'], authorized_scopes)

    self.users_stub.SetOAuthUser(scopes=['scope2', 'scope3'])
    authorized_scopes = oauth.get_authorized_scopes(('scope3', 'scope1'))
    self.assertCountEqual(['scope1'], authorized_scopes)

  def testGetAuthorizedScopesCacheSharedWithGetCurrentUser(self):
    self.users_stub.SetOAuthUser(scopes=['scope1', 'scope2'])
    oauth.get_current_user(['scope1', 'scope3'])
    self.users_stub.SetOAuthUser(scopes=['scope2', 'scope3'])
    authorized_scopes = oauth.get_authorized_scopes(['scope1', 'scope3'])
    self.assertCountEqual(['scope1'], authorized_scopes)

  def testGetAuthorizedScopesCacheError(self):
    self.users_stub.SetOAuthUser(scopes=['scope1', 'scope2'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_authorized_scopes,
                      'scope3')

    self.users_stub.SetOAuthUser(scopes=['scope1', 'scope3'])
    self.assertRaises(oauth.InvalidOAuthTokenError, oauth.get_authorized_scopes,
                      'scope3')

  def testGetAuthorizedScopesDifferentScope(self):
    self.users_stub.SetOAuthUser(scopes=['scope1', 'scope2'])
    authorized_scopes = oauth.get_authorized_scopes(('scope1', 'scope3'))
    self.assertCountEqual(['scope1'], authorized_scopes)

    self.users_stub.SetOAuthUser(scopes=['scope1', 'scope3'])
    authorized_scopes = oauth.get_authorized_scopes(['scope2', 'scope3'])
    self.assertCountEqual(['scope3'], authorized_scopes)

  def testGetAuthorizedScopesNotAllowed(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.NOT_ALLOWED, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.NotAllowedError, 'error details',
                                      oauth.get_authorized_scopes, 'fake_scope')

  def testGetAuthorizedScopesInvalidRequest(self):
    self.users_stub.SetOAuthUser(None)
    self.assertRaises(oauth.InvalidOAuthParametersError,
                      oauth.get_authorized_scopes, 'fake_scope')

  def testGetAuthorizedScopesInvalidToken(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_INVALID_TOKEN, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.InvalidOAuthTokenError,
                                      'error details',
                                      oauth.get_authorized_scopes, 'fake_scope')

  def testGetAuthorizedScopesError(self):
    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.OAUTH_ERROR, 'error details'))
    self.assertRaisesWithLiteralMatch(oauth.OAuthServiceFailureError,
                                      'error details',
                                      oauth.get_authorized_scopes, 'fake_scope')

  def testGetAuthorizedScopesUnknownError(self):

    self.users_stub.SetError(apiproxy_errors.ApplicationError(
        user_service_pb2.UserServiceError.REDIRECT_URL_TOO_LONG,
        'error details'))
    self.assertRaisesWithLiteralMatch(oauth.OAuthServiceFailureError,
                                      'error details',
                                      oauth.get_authorized_scopes, 'fake_scope')


if __name__ == '__main__':
  absltest.main()

