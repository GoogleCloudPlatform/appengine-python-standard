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



"""Unittests for the User class and the stub UserService API."""




import os

from google.appengine.api import apiproxy_stub
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import user_service_pb2
from google.appengine.api import user_service_stub
from google.appengine.api import users
from google.appengine.runtime.context import ctx_test_util
import six

from absl.testing import absltest


@ctx_test_util.isolated_context()
class UserTest(absltest.TestCase):
  def setUp(self):

    os.environ['USER_EMAIL'] = ''
    os.environ['USER_ID'] = ''
    os.environ['USER_IS_ADMIN'] = '0'



    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    self.users_stub = user_service_stub.UserServiceStub()
    self.expected_login_request = user_service_pb2.CreateLoginURLRequest()
    self.expected_logout_request = user_service_pb2.CreateLogoutURLRequest()
    class TestStub(apiproxy_stub.APIProxyStub):
      _ACCEPTS_REQUEST_ID = True

      def _Dynamic_CreateLoginURL(myself, request, response, request_id):
        if request != self.expected_login_request:
          raise AssertionError(
              'Expected: %s\nFound: %s' %
              (str(self.expected_login_request), str(request)))
        self.users_stub._Dynamic_CreateLoginURL(request, response, request_id)
      def _Dynamic_CreateLogoutURL(myself, request, response, request_id):
        if request != self.expected_logout_request:
          raise AssertionError(
              'Expected: %s\nFound: %s' %
              (str(self.expected_logout_request), str(request)))
        self.users_stub._Dynamic_CreateLogoutURL(request, response, request_id)

    apiproxy_stub_map.apiproxy.RegisterStub('user', TestStub('user'))

  def testGetEmail(self):
    jon = users.User('jonmac@google.com', _user_id='11000')
    self.assertEqual('jonmac@google.com', jon.email())

  def testGetFederatedIdentity(self):
    jcai = users.User('',
                      federated_identity='http://www.google.com/jcai',
                      _user_id='100001')
    self.assertEqual('http://www.google.com/jcai', jcai.federated_identity())
    self.assertFalse(jcai.email())

    jcai = users.User('jcai@google.com',
                      federated_identity='http://www.google.com/jcai',
                      _user_id='100001')
    self.assertEqual('http://www.google.com/jcai', jcai.federated_identity())
    self.assertEqual('jcai@google.com', jcai.email())

  def testUserEquality(self):
    jon1 = users.User('jonmac@gmail.com', _user_id='11111')
    jon2 = users.User('jonmac@gmail.com', _user_id='11111')

    self.assertEqual(jon1, jon2)
    self.assertEqual(hash(jon1), hash(jon2))

    ryan = users.User('ryanb@gmail.com', _user_id='11222')
    self.assertNotEqual(jon1, ryan)
    self.assertNotEqual(hash(jon1), hash(ryan))

    ryan_google = users.User('ryanb@gmail.com', _auth_domain='google.com',
                             _user_id='111333')
    self.assertNotEqual(ryan, ryan_google)
    self.assertNotEqual(hash(ryan), hash(ryan_google))

    self.assertNotEquals(ryan, [])


    jcai = users.User(email='jcai@google.com', _user_id='22772',
                      federated_identity='http://google.com/jcai')
    self.assertNotEqual(jcai, ryan)

    jcai1 = users.User(email='', _user_id='22772',
                       federated_identity='http://google.com/jcai')
    self.assertEqual(jcai, jcai1)

    jcai2 = users.User(email='', _user_id='00000',
                       federated_identity='http://google.com/jcai')
    self.assertEqual(jcai1, jcai2)

    jcai3 = users.User(email='', _auth_domain='google.com',
                       federated_identity='http://google.com/jcai')
    self.assertNotEqual(jcai2, jcai3)

  def testGetNickname(self):
    jon = users.User('jonmac@gmail.com', _user_id='11444')
    self.assertEqual('jonmac', jon.nickname())

    jon = users.User('jonmac@google.com', _user_id='11555')
    self.assertEqual('jonmac@google.com', jon.nickname())


    jcai = users.User(email='jcai@google.com',
                      _user_id='22772',
                      _auth_domain='google.com',
                      federated_identity='http://google.com/jcai')
    self.assertEqual('jcai', jcai.nickname())

    jcai = users.User(email='jcai@google.com', _user_id='22772',
                      federated_identity='http://google.com/jcai')
    self.assertEqual('http://google.com/jcai', jcai.nickname())

    jcai = users.User(email='jcai@google.com', _user_id='22772')
    self.assertEqual('jcai@google.com', jcai.nickname())

    jcai = users.User(email='', _user_id='22772',
                      federated_identity='http://google.com/jcai')
    self.assertEqual('http://google.com/jcai', jcai.nickname())

    jcai = users.User(_user_id='22772',
                      federated_identity='http://google.com/jcai')
    self.assertEqual('http://google.com/jcai', jcai.nickname())

  def testDefaultAuthDomain(self):
    gow = users.User(email='gowthamn@google.com', _user_id='24546')
    self.assertEqual('gmail.com', gow.auth_domain())

  def testCustomAuthDomain(self):


    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    users_stub = user_service_stub.UserServiceStub(auth_domain='google.com')
    apiproxy_stub_map.apiproxy.RegisterStub('user', users_stub)
    gow = users.User(email='gowthamn@google.com', _user_id='24546')
    self.assertEqual('google.com', gow.auth_domain())

  def testEmptyAuthDomainFails(self):
    self.assertRaises(AssertionError, users.User, 'a@b.com', '')

  def _TestSimpleLogin(self, requested_continue_url, expected_continue_url,
                       auth_domain=None):
    self.expected_login_request.destination_url = requested_continue_url
    if auth_domain:
      self.expected_login_request.auth_domain = auth_domain
    else:
      self.expected_login_request.ClearField('auth_domain')

    login_url = users.create_login_url(requested_continue_url,
                                       _auth_domain=auth_domain)

    self.assertEqual(
      (user_service_stub._DEFAULT_LOGIN_URL %
       six.moves.urllib.parse.quote(expected_continue_url)),
      login_url)

  def testCreateLoginURL(self):
    os.environ['HTTP_HOST'] = 'giggit.prom.corp.google.com'
    os.environ['SERVER_NAME'] = 'badserver.prom.corp.google.com'
    os.environ['SERVER_PORT'] = '666'


    self._TestSimpleLogin('http://giggit.prom.corp.google.com',
                          'http://giggit.prom.corp.google.com')
    self._TestSimpleLogin('http://giggit.prom.corp.google.com/',
                          'http://giggit.prom.corp.google.com/')
    self._TestSimpleLogin('http://giggit.prom.corp.google.com/profile',
                          'http://giggit.prom.corp.google.com/profile')
    self._TestSimpleLogin('http://othergiggit.com/profile',
                          'http://othergiggit.com/profile')
    self._TestSimpleLogin('http://giggit.prom.corp.google.com/?a=b&c=d',
                          'http://giggit.prom.corp.google.com/?a=b&c=d')


    self._TestSimpleLogin('',
                          'http://giggit.prom.corp.google.com/')
    self._TestSimpleLogin('/',
                          'http://giggit.prom.corp.google.com/')
    self._TestSimpleLogin('/profile',
                          'http://giggit.prom.corp.google.com/profile')
    self._TestSimpleLogin('../profile',
                          'http://giggit.prom.corp.google.com/../profile')
    self._TestSimpleLogin('/?a=b&c=d',
                          'http://giggit.prom.corp.google.com/?a=b&c=d')


    self._TestSimpleLogin('http://giggit.prom.corp.google.com',
                          'http://giggit.prom.corp.google.com',
                          auth_domain='bar.com')


    del os.environ['HTTP_HOST']
    os.environ['SERVER_NAME'] = 'giggit.prom.corp.google.com'
    os.environ['SERVER_PORT'] = '80'
    self._TestSimpleLogin('',
                          'http://giggit.prom.corp.google.com/')



    os.environ['SERVER_PORT'] = '9999'
    self._TestSimpleLogin('',
                          'http://giggit.prom.corp.google.com:9999/')


    os.environ['SERVER_PORT'] = '80'
    login_url = users.CreateLoginURL('')
    self.assertEqual(
      (user_service_stub._DEFAULT_LOGIN_URL %
       six.moves.urllib.parse.quote('http://giggit.prom.corp.google.com/')),
      login_url)

  def _TestSimpleLogout(self, requested_continue_url, expected_continue_url,
                        auth_domain=None):
    self.expected_logout_request.destination_url = requested_continue_url
    if auth_domain:
      self.expected_logout_request.auth_domain = auth_domain
    else:
      self.expected_logout_request.ClearField('auth_domain')

    logout_url = users.create_logout_url(requested_continue_url,
                                         _auth_domain=auth_domain)

    self.assertEqual(
      (user_service_stub._DEFAULT_LOGOUT_URL %
       six.moves.urllib.parse.quote(expected_continue_url)),
      logout_url)

  def testCreateLogoutURL(self):
    os.environ['HTTP_HOST'] = 'giggit.prom.corp.google.com'
    os.environ['SERVER_NAME'] = 'badserver.prom.corp.google.com'
    os.environ['SERVER_PORT'] = '666'


    self._TestSimpleLogout('http://giggit.prom.corp.google.com',
                           'http://giggit.prom.corp.google.com')
    self._TestSimpleLogout('http://giggit.prom.corp.google.com/',
                           'http://giggit.prom.corp.google.com/')
    self._TestSimpleLogout('http://giggit.prom.corp.google.com/profile',
                           'http://giggit.prom.corp.google.com/profile')
    self._TestSimpleLogout('http://othergiggit.com/profile',
                           'http://othergiggit.com/profile')
    self._TestSimpleLogout('http://giggit.prom.corp.google.com/?a=b&c=d',
                           'http://giggit.prom.corp.google.com/?a=b&c=d')


    self._TestSimpleLogout('',
                           'http://giggit.prom.corp.google.com/')
    self._TestSimpleLogout('/',
                           'http://giggit.prom.corp.google.com/')
    self._TestSimpleLogout('/profile',
                           'http://giggit.prom.corp.google.com/profile')
    self._TestSimpleLogout('../profile',
                           'http://giggit.prom.corp.google.com/../profile')
    self._TestSimpleLogout('/?a=b&c=d',
                           'http://giggit.prom.corp.google.com/?a=b&c=d')


    self._TestSimpleLogout('http://giggit.prom.corp.google.com',
                           'http://giggit.prom.corp.google.com',
                           auth_domain='bar.com')


    del os.environ['HTTP_HOST']
    os.environ['SERVER_NAME'] = 'giggit.prom.corp.google.com'
    os.environ['SERVER_PORT'] = '80'
    self._TestSimpleLogout('',
                           'http://giggit.prom.corp.google.com/')



    os.environ['SERVER_PORT'] = '9999'
    self._TestSimpleLogout('',
                           'http://giggit.prom.corp.google.com:9999/')


    os.environ['SERVER_PORT'] = '80'
    logout_url = users.CreateLogoutURL('')
    self.assertEqual(
      (user_service_stub._DEFAULT_LOGOUT_URL %
       six.moves.urllib.parse.quote('http://giggit.prom.corp.google.com/')),
      logout_url)

  def testUserNotFound(self):
    """Ensure that creating a user with no user logged in causes this error."""
    self.assertRaises(users.UserNotFoundError, users.User)

  def testUserNotFound_NonStrictMode(self):
    """Creating a user with no email or federated_identity doesn't error."""
    self.assertIsNot(users.User(_strict_mode=False), None)
    self.assertIsNot(
        users.User(_auth_domain='gmail.com', _strict_mode=False), None)

  def testDefaultUsers(self):
    os.environ['USER_EMAIL'] = 'jonmac@google.com'
    jon = users.User()
    self.assertEqual('jonmac@google.com', jon.email())

    del os.environ['USER_EMAIL']
    os.environ['FEDERATED_IDENTITY'] = 'http://www.google.com/jcai'
    jcai = users.User()
    self.assertEqual('http://www.google.com/jcai', jcai.federated_identity())

  def testCustomEnviron(self):


    os.environ['USER_EMAIL'] = 'jonmac@google.com'
    del os.environ['USER_ID']
    jon = users.User()
    self.assertEqual('jonmac@google.com', jon.email())

  def testStrReprAndUnicode(self):
    jon = users.User('jonmac@google.com')

    for email in ['jonmac', '', None]:
      jon._User__email = email
      expected = str(email)
      self.assertEqual(expected, str(jon))
      if email:
        self.assertEqual(expected, str(eval(repr(jon))))
      self.assertEqual(expected, '%s' % jon)
      self.assertEqual(expected, six.text_type(jon))
      self.assertEqual(six.text_type, six.text_type(jon).__class__)

  def testStrReprWithId(self):
    for jon in [users.User('jonmac@google.com', _user_id='1112'),
                users.User('jonmac@google.com')]:
      new_jon = eval(repr(jon))
      self.assertEqual(jon.user_id(), new_jon.user_id())
      self.assertEqual(jon, new_jon)

  def testUserIdNone(self):
    user = users.User('jonmac@google.com', _user_id='')
    self.assertEqual(None, user.user_id())

    user = users.User('jonmac@google.com')
    self.assertEqual(None, user.user_id())

    user = users.User('jonmac@google.com', _user_id=None)
    self.assertEqual(None, user.user_id())

    user = users.User('jonmac@google.com', _user_id='123')
    self.assertEqual('123', user.user_id())

    os.environ['USER_EMAIL'] = 'jonmac@google.com'
    user = users.User()
    del os.environ['USER_EMAIL']
    self.assertEqual('jonmac@google.com', user.email())
    self.assertEqual(None, user.user_id())

  def testCmp(self):
    user1 = users.User('a@a.com', _user_id='10')
    user1_no_id = users.User('a@a.com')
    self.assertEqual(user1, user1_no_id)
    user1a = users.User('a@a.com', _user_id='10')
    self.assertEqual(user1, user1a)

    user2 = users.User('b@b.com')
    user2a = users.User('b@b.com')
    self.assertEqual(user2, user2a)
    self.assertNotEqual(user1, user2)
    self.assertLess(user1, user2)

    user3 = users.User('c@c.com', _user_id='5')
    self.assertNotEqual(user3, user1)
    self.assertLess(user2, user3)
    self.assertLess(user1, user3)

  def testIsCurrentUserAdmin(self):

    self.assertFalse(users.is_current_user_admin())
    self.assertFalse(users.IsCurrentUserAdmin())

    os.environ['USER_IS_ADMIN'] = '0'
    self.assertFalse(users.is_current_user_admin())
    self.assertFalse(users.IsCurrentUserAdmin())

    os.environ['USER_IS_ADMIN'] = '1'
    self.assertTrue(users.is_current_user_admin())
    self.assertTrue(users.IsCurrentUserAdmin())

  def testSortUsers(self):
    ryan = users.User('ryanb@gmail.com')
    jon = users.User('jonmac@gmail.com')
    jon_abc = users.User('jonmac@gmail.com', _auth_domain='abc.com')
    brett = users.User('bslatkin@gmail.com')

    people = [ryan, jon, brett, jon_abc]
    self.assertEqual([brett, jon_abc, jon, ryan], sorted(people))


if __name__ == '__main__':
  absltest.main()
