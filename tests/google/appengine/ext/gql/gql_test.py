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





"""GQL interface around the datastore API.

The functionality here is not the same as the normal datastore
as the function interface is significantly different and the behavior
of the output is somewhat different.

For a high level explanation, see (for now):
  https://docs.google.com/a/google.com/Doc?docid=cgdvt6n7_99fn5wm4fj&hl=en

The simple tests ensure that SELECT * behaves like the normal datastore
API. This will change as the GQL API adds functionality not available in
the datastore API.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import logging
import os
import sys
import time

from six.moves import range
from six.moves import zip

from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_file_stub
from google.appengine.api import datastore_types
from google.appengine.api import namespace_manager
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import gql
from absl.testing import absltest




def setUpModule():

  logging.basicConfig(level=gql.LOG_LEVEL + 1, stream=sys.stdout)




class GqlTest(absltest.TestCase):
  """Test the SQL interface to the Python datastore.

  sql.Query just parses a SQL statement and compiles it to a datastore.Query.
  Given that, these tests don't exhaustively test all query functionality.
  They just test the parsing and compilation.
  """

  def setUp(self):
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()


    stub = datastore_file_stub.DatastoreFileStub('test_app',
                                                 '/dev/null',
                                                 '/dev/null')
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
    os.environ['APPLICATION_ID'] = 'test_app'


    os.environ['TZ'] = 'UTC'
    os.environ['AUTH_DOMAIN'] = 'google.com'
    time.tzset()


    self.bret = datastore.Entity('Person')
    self.bret['email'] = 'btaylor@google.com'
    self.bret['phone'] = ['555-1234', '555-4000']
    self.bret['ringtone'] = 12
    self.bret['google_color'] = 'green'
    self.bret['birthday'] = datetime.datetime(1991, 10, 10)
    datastore.Put(self.bret)

    self.jon = datastore.Entity('Person')
    self.jon['email'] = 'jonmac@google.com'
    self.jon['phone'] = ['555-5678', '555-4000']
    self.jon['ringtone'] = 12
    self.jon['google_color'] = 'red'
    datastore.Put(self.jon)

    self.ken = datastore.Entity('Person')
    self.ken['email'] = 'kash@google.com'
    self.ken['favorite_number'] = -1
    self.ken['ringtone'] = 15
    self.ken['google_color'] = 'red'
    self.ken['nullable'] = True
    datastore.Put(self.ken)

    self.kevin = datastore.Entity('Person')
    self.kevin['email'] = 'kgibbs@google.com'
    self.kevin['phone'] = '555-6789'
    self.kevin['salary'] = 1000.1
    self.kevin['ringtone'] = 15
    self.kevin['google_color'] = 'green'
    self.kevin['nullable'] = False
    datastore.Put(self.kevin)

    self.chris = datastore.Entity('Person')
    self.chris['email'] = 'mysen@google.com'
    self.chris['phone'] = '555-1234'
    self.chris['favorite_number'] = 93
    self.chris['top_score'] = 42
    self.chris['ringtone'] = 12
    self.chris['google_color'] = 'blue'
    self.chris['location'] = datastore_types.GeoPt(40.0, 100.0)
    self.chris['birthday'] = datetime.datetime(1980, 2, 2)
    self.chris['email=elvis@google.com'] = False
    self.chris['nullable'] = None
    datastore.Put(self.chris)

    self.larry = datastore.Entity('Person')
    self.larry['email'] = 'larry@google.com'
    self.larry['phone'] = '111-1234'
    self.larry['favorite_number'] = 123
    self.larry['top_score'] = 321
    self.larry['dog'] = 'tom'
    self.larry['salary'] = 1.0
    self.larry['website'] = datastore_types.Link('http://www.google.com')
    self.larry['user'] = users.User('larry@google.com',
                                    _auth_domain='google.com')
    self.larry['founded.google'] = True
    self.larry['nullable'] = None
    datastore.Put(self.larry)

    self.elvis = datastore.Entity('Person')
    self.elvis['email'] = 'elvis@google.com'
    self.elvis['phone'] = '888-phone-elvis'
    self.elvis['dead'] = True
    self.elvis['rocks'] = True
    self.elvis['nullable'] = 0
    datastore.Put(self.elvis)

    self.hillary = datastore.Entity('Person')
    self.hillary['email'] = 'mrsbill@google.com'
    self.hillary['phone'] = '555-9876'
    self.hillary['favorite_number'] = 256000000
    self.hillary['ringtone'] = 3
    self.hillary['google_color'] = 'blue'
    self.hillary['nullable'] = 'NULL'
    datastore.Put(self.hillary)

    self.bizarrolarry = datastore.Entity('Person')
    self.bizarrolarry['email'] = 'larry@google.com'
    self.bizarrolarry['phone'] = '111-1234'
    self.bizarrolarry['favorite_number'] = -123
    self.bizarrolarry['top_score'] = -321
    self.bizarrolarry['dog'] = 'mot'
    self.bizarrolarry['job'] = 'man\'s man'
    self.bizarrolarry['salary'] = -1.0
    self.bizarrolarry['dead'] = True
    self.bizarrolarry['rocks'] = False
    self.bizarrolarry['hero'] = self.elvis.key()


    self.bizarrolarry['time_of_birth'] = datetime.datetime(1970, 1, 1, 4, 20, 0)
    datastore.Put(self.bizarrolarry)

    self.thefoo = datastore.Entity('Person')
    self.thefoo['email'] = 'foo@google.com'
    self.thefoo['phone'] = '555-9012'
    self.thefoo['favorite_number'] = '555-9012'
    datastore.Put(self.thefoo)

    self.lisamarie = datastore.Entity('Person', parent=self.elvis)
    self.lisamarie['email'] = 'lisamarie@google.com'
    self.lisamarie['phone'] = '888-phone-lisa'
    self.lisamarie['dead'] = False
    self.lisamarie['rocks'] = True
    datastore.Put(self.lisamarie)

    self.all_entities = (self.bret, self.jon, self.ken, self.kevin,
                         self.elvis, self.lisamarie,
                         self.chris, self.hillary, self.larry,
                         self.bizarrolarry, self.thefoo)

    self.gianni = datastore.Entity('Person', namespace='Sydney')
    self.gianni['email'] = 'gianni@google.com'
    self.gianni['phone'] = '111-1234'
    self.gianni['favorite_number'] = 123
    self.gianni['top_score'] = 321
    self.gianni['dog'] = 'tom'
    self.gianni['salary'] = 1.0
    self.gianni['website'] = datastore_types.Link('http://www.google.com')
    self.gianni['user'] = users.User('gianni@google.com',
                                     _auth_domain='google.com')
    self.gianni['nullable'] = None
    datastore.Put(self.gianni)

    self.iwade = datastore.Entity('Person', namespace='Sydney')
    self.iwade['email'] = 'iwade@google.com'
    self.iwade['phone'] = '555-1234'
    self.iwade['favorite_number'] = 93
    self.iwade['top_score'] = 42
    self.iwade['ringtone'] = 12
    self.iwade['google_color'] = 'blue'
    self.iwade['location'] = datastore_types.GeoPt(-33.8665, 151.1955)
    self.iwade['birthday'] = datetime.datetime(2009, 3, 1)
    self.iwade['nullable'] = None
    datastore.Put(self.iwade)

    self.bizarrogianni = datastore.Entity('Person', namespace='Sydney')
    self.bizarrogianni['email'] = 'giannibizzaro@google.com'
    self.bizarrogianni['phone'] = '111-1234-999'
    self.bizarrogianni['favorite_number'] = -1239
    self.bizarrogianni['top_score'] = -3210
    self.bizarrogianni['dog'] = 'mot'
    self.bizarrogianni['job'] = 'man\'s man'
    self.bizarrogianni['salary'] = -1.0
    self.bizarrogianni['dead'] = True
    self.bizarrogianni['rocks'] = False
    self.bizarrogianni['hero'] = self.gianni.key()
    datastore.Put(self.bizarrogianni)

    self.all_sydney_entities = (self.gianni, self.iwade, self.bizarrogianni)

    self.lion = datastore.Entity('some-animals')
    self.lion['name'] = 'leo'
    datastore.Put(self.lion)

    self.shark = datastore.Entity('some-animals')
    self.shark['name'] = 'jaws'
    datastore.Put(self.shark)

    self.all_animals = (self.lion, self.shark)

  def tearDown(self):
    """Clean up test harness."""

    namespace_manager.set_namespace('')

  def testBasicSelect(self):
    """Test parsing simple select statements."""
    select = gql.GQL('SELECT * FROM Person')
    self.assertEqual(select._kind, 'Person')
    self.assertEqual(select.kind(), 'Person')
    self.assertEqual(select._entity, 'Person')

    select = gql.GQL('select * from Person')
    self.assertEqual(select._kind, 'Person')


    select = gql.GQL('select * from Things')
    self.assertEqual(select._kind, 'Things')


    select = gql.GQL('select * from "my-table::with.crazy.characters"')
    self.assertEqual(select._kind, 'my-table::with.crazy.characters')


    select = gql.GQL('select * from "embedded""(quote)"')
    self.assertEqual(select._kind, 'embedded"(quote)')


    select = gql.GQL
    self.assertRaises(datastore_errors.BadQueryError,
                      select, 'select * * from Things')

  def testBasicSelectQuery(self):
    """Test that we get real results from the backend."""


    select = gql.GQL('select * from Person')
    results = [a for a in select.Run()]
    self.assertCountEqual(self.all_entities, results)

  def testBasicSelectQueryTerminatingSemicolon(self):
    """Test that a single terminating semi-colon is accepted."""
    select = gql.GQL('select * from Person;')
    results = [a for a in select.Run()]
    self.assertCountEqual(self.all_entities, results)

  def testBasicSelectQueryInvalidTerminatingCharacters(self):
    bad_query = 'select * from Person;;'
    self.assertRaises(datastore_errors.BadQueryError,
                      gql.GQL, bad_query)

    bad_query = 'select * from Person.'
    self.assertRaises(datastore_errors.BadQueryError,
                      gql.GQL, bad_query)

  def testBasicSelectQueryWithQuotedKindName(self):
    """Test that we get results when the kind name doesn't match (\w+)."""
    select = gql.GQL('select * from "some-animals"')
    results = [a for a in select.Run()]
    self.assertCountEqual(self.all_animals, results)

  def testBasicSelectQueryNamespaced(self):
    """Test that we get real results for a different namespace."""
    select = gql.GQL('select * from Person', namespace='Sydney')
    results = [a for a in select.Run()]
    self.assertCountEqual(self.all_sydney_entities, results)

  def testBasicSelectQueryDefaultNamespace(self):
    """Test that we get real results for a different namespace."""
    namespace_manager.set_namespace('Sydney')
    select = gql.GQL('select * from Person')
    results = [a for a in select.Run()]
    self.assertCountEqual(self.all_sydney_entities, results)

  def testBasicSelectQueryKeyNamespace(self):

    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE hero = KEY(\'Person\', %i)' %
        self.gianni.key().id(),
        namespace='Sydney')
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bizarrogianni], res_key)

  def testKeysOnlySelectQuery(self):
    """Test a keys only query."""
    select = gql.GQL('SELECT * FROM Person')
    self.assertFalse(select.is_keys_only())

    select = gql.GQL('SELECT __key__ FROM Person')
    self.assertTrue(select.is_keys_only())
    results = [a for a in select.Run()]
    self.assertCountEqual([e.key() for e in self.all_entities], results)

  def testProjectionSelect(self):
    self.AssertRaisesBadQuery('Identifier Expected', gql.GQL, 'SELECT')
    self.AssertRaisesBadQuery('Identifier is a reserved keyword', gql.GQL,
                              'SELECT FROM Person')
    self.AssertRaisesBadQuery('Identifier Expected', gql.GQL, 'SELECT ,')
    self.AssertRaisesBadQuery('Identifier Expected', gql.GQL, 'SELECT email,')

    select = gql.GQL('SELECT FROM')
    self.assertFalse(select.is_keys_only())
    self.assertEqual(('FROM',), select.projection())
    self.assertEqual(None, select.kind())

    select = gql.GQL('SELECT FROM FROM kind')
    self.assertFalse(select.is_keys_only())
    self.assertEqual(('FROM',), select.projection())
    self.assertEqual('kind', select.kind())

    select = gql.GQL('SELECT email, phone FROM Person')
    self.assertFalse(select.is_keys_only())
    self.assertEqual(('email', 'phone'), select.projection())
    self.assertEqual('Person', select.kind())

    select = gql.GQL('SELECT email,phone FROM Person')
    self.assertFalse(select.is_keys_only())
    self.assertEqual(('email', 'phone'), select.projection())
    self.assertEqual('Person', select.kind())

    select = gql.GQL('SELECT email ,phone FROM Person')
    self.assertFalse(select.is_keys_only())
    self.assertEqual(('email', 'phone'), select.projection())
    self.assertEqual('Person', select.kind())

  def testDistinctProjectionSelect(self):
    select = gql.GQL('SELECT DISTINCT color, type FROM Flower')
    self.assertTrue(select.is_distinct())
    self.assertEqual(('color', 'type'), select.projection())
    self.assertEqual('Flower', select.kind())

  def testDistinctProjectionSelectWithOrder(self):
    select = gql.GQL('SELECT DISTINCT color, type'
                     ' FROM Flower ORDER BY type, color')
    self.assertTrue(select.is_distinct())
    self.assertEqual(('color', 'type'), select.projection())
    self.assertEqual('Flower', select.kind())

  def testDistinctProjectionWithFilter(self):
    select = gql.GQL('SELECT DISTINCT price, color, type'
                     ' FROM Flower WHERE price > :1 AND price < :2'
                     ' ORDER BY price, type, color')
    self.assertTrue(select.is_distinct())
    self.assertEqual(('price', 'color', 'type'), select.projection())
    self.assertEqual('Flower', select.kind())

  def testDistinctWithoutProjection(self):
    select = gql.GQL('SELECT DISTINCT * FROM FLOWER')

    self.assertTrue(select.is_distinct())
    self.AssertRaisesBadQuery('cannot specify distinct without a projection',
                              select.Run)

  def testReservedNamesErrorWithDistinct(self):


    self.AssertRaisesBadQuery('Identifier is a reserved keyword',
                              gql.GQL,
                              'SELECT DISTINCT from FROM FLOWER')

    self.AssertRaisesBadQuery('Identifier is a reserved keyword',
                              gql.GQL,
                              'SELECT DISTINCT from, a FROM FLOWER')

    self.AssertRaisesBadQuery('Identifier is a reserved keyword',
                              gql.GQL,
                              'SELECT DISTINCT where WHERE a = :1')

    self.AssertRaisesBadQuery('Identifier is a reserved keyword',
                              gql.GQL,
                              'SELECT DISTINCT from WHERE a = :1')

  def testReservedNamesWillAllowEscapedPropertyNames(self):

    select = gql.GQL('SELECT a, "DISTINCT" FROM FLOWER')
    self.assertEqual(select.projection(), tuple(['a', 'DISTINCT']))
    self.assertFalse(select.is_distinct())

    select = gql.GQL('SELECT DISTINCT a, "DISTINCT" FROM FLOWER')
    self.assertEqual(select.projection(), tuple(['a', 'DISTINCT']))
    self.assertTrue(select.is_distinct())

    select = gql.GQL('SELECT "from" FROM "where"')
    self.assertEqual(select.projection(), ('from',))
    self.assertEqual(select.kind(), 'where')

    select = gql.GQL('SELECT DISTINCT "from" FROM "where"')
    self.assertEqual(select.projection(), ('from',))
    self.assertTrue(select.is_distinct())
    self.assertEqual(select.kind(), 'where')

  def testReservedNamesBackwardsCompatibility(self):


    select = gql.GQL('SELECT DISTINCT FROM FLOWER')
    self.assertEqual(select.projection(), tuple(['DISTINCT']))
    self.assertFalse(select.is_distinct())

    select = gql.GQL('SELECT distinct FROM FLOWER')
    self.assertEqual(select.projection(), tuple(['distinct']))
    self.assertFalse(select.is_distinct())

    select = gql.GQL('SELECT a, DISTINCT FROM FLOWER')
    self.assertEqual(select.projection(), tuple(['a', 'DISTINCT']))
    self.assertFalse(select.is_distinct())

    select = gql.GQL('SELECT DISTINCT, a FROM FLOWER')
    self.assertEqual(select.projection(), tuple(['DISTINCT', 'a']))
    self.assertFalse(select.is_distinct())

    select = gql.GQL('SELECT distinct WHERE a = :1')
    self.assertEqual(select.projection(), tuple(['distinct']))
    self.assertFalse(select.is_distinct())
    self.assertLen(select.filters(), 1)

    select = gql.GQL('SELECT distinct ORDER BY a')
    self.assertEqual(select.projection(), tuple(['distinct']))
    self.assertFalse(select.is_distinct())
    self.assertEqual(select.orderings(), [('a', 1)])

    select = gql.GQL('SELECT distinct FROM where')
    self.assertEqual(select.projection(), ('distinct',))
    self.assertFalse(select.is_distinct())
    self.assertEqual(select.kind(), 'where')

  def testWhereParsing(self):
    select = gql.GQL('SELECT * FROM Person WHERE email=:1')
    self.assertLen(select.filters(), 1)

    select = gql.GQL("""SELECT * FROM Person
                        WHERE email=:1 AND phone > :2""")

    select = gql.GQL("""SELECT * FROM Person
                        WHERE email=:1 AND phone > :phone""")
    self.assertLen(select.filters(), 2)

  def testWhereQuery(self):

    select = gql.GQL('SELECT * FROM Person WHERE email = :1')
    results = [a for a in select.Run('jonmac@google.com')]
    self.assertLen(results, 1)
    self.assertEqual(self.jon, results[0])


    select = gql.GQL("""SELECT * FROM Person
                        WHERE email > :1 AND phone = :2""")
    results = [a for a in select.Run('jonmac@google.com', '555-6789')]
    self.assertLen(results, 1)
    self.assertEqual(self.kevin, results[0])

  def testWhereQueryMultipleReferences(self):

    select = gql.GQL('SELECT * FROM Person WHERE '
                     'phone = :1 AND favorite_number = :1')
    results = [a for a in select.Run('555-9012')]
    self.assertLen(results, 1)
    self.assertEqual(self.thefoo, results[0])


    select = gql.GQL('SELECT * FROM Person WHERE '
                     'phone = :special_num AND favorite_number = :special_num')
    results_named = [a for a in select.Run(**{'special_num': '555-9012'})]
    self.assertLen(results_named, 1)
    self.assertEqual(self.thefoo, results_named[0])

  def testWhereQueryMultipleFilterValues(self):
    """Test that we support multiple values for the same filter."""
    select = gql.GQL("SELECT * FROM Person "
                     "WHERE phone = '555-1234' AND phone = '555-4000'")
    self.assertEqual([self.bret], list(select.Run()))

    select = gql.GQL("SELECT * FROM Person "
                     "WHERE phone = '555-1234' AND phone = '555-4000' "
                     "AND phone = '555-5678'")
    self.assertEqual([], list(select.Run()))

  def testWhereQueryNamed(self):
    select = gql.GQL('SELECT * FROM Person WHERE email = :email')
    params = {}
    params['email'] = 'jonmac@google.com'
    results = [a for a in select.Run(**params)]
    self.assertLen(results, 1)
    self.assertEqual(self.jon, results[0])

  def testWhereQueryNumberLiterals(self):

    select = gql.GQL('SELECT * FROM Person WHERE favorite_number = 93')
    results = [a for a in select.Run()]
    self.assertLen(results, 1)
    self.assertEqual(self.chris, results[0])


    select_float = gql.GQL('SELECT * FROM Person WHERE salary = 1000.1')
    results_float = [a for a in select_float.Run()]
    self.assertLen(results_float, 1)
    self.assertEqual(self.kevin, results_float[0])


    select_gt_float = gql.GQL('SELECT * FROM Person WHERE salary > 0')
    results_gt_float = [a for a in select_gt_float.Run()]
    self.assertLen(results_gt_float, 3)
    self.assertCountEqual([self.kevin, self.larry, self.bizarrolarry],
                          results_gt_float)

  def testWhereQueryBooleanLiterals(self):

    select = gql.GQL('SELECT * FROM Person WHERE dead = True')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertCountEqual([self.elvis, self.bizarrolarry], results)

    select_false = gql.GQL('SELECT * FROM Person WHERE rocks = False')
    results_false = [a for a in select_false.Run()]
    self.assertLen(results_false, 1)
    self.assertCountEqual([self.bizarrolarry], results_false)


    select = gql.GQL('SELECT * FROM Person WHERE dead = True AND rocks = True')
    results = [a for a in select.Run()]
    self.assertLen(results, 1)
    self.assertCountEqual([self.elvis], results)

    select = gql.GQL('SELECT * FROM Person WHERE dead = True AND rocks = False')
    results = [a for a in select.Run()]
    self.assertLen(results, 1)
    self.assertCountEqual([self.bizarrolarry], results)


    select_0 = gql.GQL('SELECT * FROM Person WHERE rocks = 0')
    results_0 = [a for a in select_0.Run()]
    self.assertEqual([], results_0)

    select_01 = gql.GQL('SELECT * FROM Person WHERE dead = 0 AND rocks = 1')
    results_01 = [a for a in select_01.Run()]
    self.assertEqual([], results_01)

  def testWhereQueryNullLiterals(self):

    select = gql.GQL('SELECT * FROM Person WHERE nullable = Null')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertCountEqual([self.chris, self.larry], results)


    select = gql.GQL('SELECT * FROM Person WHERE nullable != NULL')
    results = [a for a in select.Run()]
    self.assertLen(results, 4)
    self.assertCountEqual([self.ken, self.kevin, self.elvis, self.hillary],
                          results)


    select = gql.GQL('SELECT * FROM Person WHERE nullable IN (Null, True)')
    results = [a for a in select.Run()]
    self.assertLen(results, 3)
    self.assertCountEqual([self.chris, self.larry, self.ken], results)


    select = gql.GQL('SELECT * FROM Person WHERE nullable = USER(Null)')
    self.AssertRaisesBadQuery('Type Cast Error', select.Run)

  def testWhereQueryStringLiterals(self):

    select = gql.GQL('SELECT * FROM Person WHERE email = \'kgibbs@google.com\'')
    results_str_literal = [a for a in select.Run()]
    self.assertLen(results_str_literal, 1)
    self.assertEqual(self.kevin, results_str_literal[0])


    select = gql.GQL('SELECT * FROM Person WHERE job = \'man\'\'s man\'')
    results_str_literal = [a for a in select.Run()]
    self.assertLen(results_str_literal, 1)
    self.assertEqual(self.bizarrolarry, results_str_literal[0])

  def testWhereQueryMixedLiterals(self):
    """Test mixed types in select literals."""

    select = gql.GQL('SELECT * FROM Person WHERE'
                     ' email = \'kash@google.com\' AND favorite_number = -1')
    results_mixed_literals = [a for a in select.Run()]
    self.assertLen(results_mixed_literals, 1)
    self.assertEqual(self.ken, results_mixed_literals[0])

  def testWhereQueryFailedLiterals(self):

    select = gql.GQL
    self.assertRaises(datastore_errors.BadQueryError,
                      select, 'SELECT * FROM Person WHERE job = \'man\'s man\'')


    select = gql.GQL
    self.assertRaises(datastore_errors.BadQueryError,
                      select, 'SELECT * FROM Person WHERE salary = 1000.1.1')


    select = gql.GQL
    self.assertRaises(datastore_errors.BadQueryError,
                      select, 'SELECT * FROM Person WHERE salary =')

  def testWhereQueryMixed(self):
    select = gql.GQL("""SELECT * FROM Person WHERE email = :email and
                        favorite_number = :2 and phone = :1""")
    params = {}
    params['email'] = 'mysen@google.com'
    results = [a for a in select.Run('555-1234', 93, **params)]
    self.assertLen(results, 1)
    self.assertEqual(self.chris, results[0])

    self.assertRaises(datastore_errors.BadArgumentError,
                      select.Run, **params)
    self.assertRaises(datastore_errors.BadArgumentError,
                      select.Run, '555-1234', 93)

  def testWhereQueryQuotedFilterProperties(self):
    select = gql.GQL('SELECT * FROM Person WHERE "founded.google" = true')
    results = [a for a in select.Run()]
    self.assertLen(results, 1)
    self.assertEqual(self.larry, results[0])

    select = gql.GQL("""SELECT * FROM Person WHERE "phone" = '555-6789' and
                     "ringtone" = 15""")
    results = [a for a in select.Run()]
    self.assertLen(results, 1)
    self.assertEqual(self.kevin, results[0])

    select = gql.GQL('SELECT * FROM Person WHERE "email=elvis@google.com" = '
                     'FALSE')
    results = [a for a in select.Run()]
    self.assertLen(results, 1)
    self.assertEqual(self.chris, results[0])

    select = gql.GQL("SELECT * FROM Person WHERE email = 'elvis@google.com'")
    results = [a for a in select.Run()]
    self.assertLen(results, 1)
    self.assertEqual(self.elvis, results[0])

  def testUnicodeStrings(self):
    """Test that unicode strings parse and execute properly."""

    select = gql.GQL(
        u"SELECT * FROM Person WHERE email = 'kgibbs@google.com'")
    results_str_literal = [a for a in select.Run()]
    self.assertLen(results_str_literal, 1)
    self.assertEqual(self.kevin, results_str_literal[0])


    key_compare = gql.GQL(
        u"SELECT * FROM Person "
        u"  WHERE birthday = DATETIME('1980-02-02 00:00:00')")
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.chris], res_key)


    key_compare = gql.GQL(
        u"SELECT * FROM Person WHERE birthday = DATE('1991-10-10')")
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bret], res_key)


    key_compare = gql.GQL(
        u"SELECT * FROM Person "
        u"  WHERE time_of_birth = TIME('04:20:00')")
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bizarrolarry], res_key)


    key_compare = gql.GQL(
        u'SELECT * FROM Person WHERE hero = KEY(\'%s\')'
        % str(self.elvis.key()))
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bizarrolarry], res_key)

  def testFailedUnicodeStrings(self):
    """Test that unicode strings that cannot be parsed fail properly."""



    key_compare = gql.GQL(
        u'SELECT * FROM Person '
        u'  WHERE birthday = DATETIME(\'1980-02-02 00:00:00 \xc3\xa7a va\')')
    self.AssertRaisesBadQuery('Type Cast Error', key_compare.Run)


    key_compare = gql.GQL(
        u'SELECT * FROM Person '
        u'  WHERE birthday = DATE(\'1991-10-10 \xc3\xa7a va\')')
    self.AssertRaisesBadQuery('Type Cast Error', key_compare.Run)


    key_compare = gql.GQL(
        u'SELECT * FROM Person '
        u'  WHERE time_of_birth = TIME(\'04:20:00 \xc3\xa7a va\')')
    self.AssertRaisesBadQuery('Type Cast Error', key_compare.Run)

  def testFailedCastNoValue(self):
    """Test that cast operator properly fails with no values."""

    self.AssertRaisesBadQuery(
        'Parse Error', gql.GQL,
        'SELECT * FROM Person WHERE birthday = DATETIME()')

    self.AssertRaisesBadQuery(
        'Parse Error', gql.GQL,
        'SELECT * FROM Person WHERE birthday = DATE()')

    self.AssertRaisesBadQuery(
        'Parse Error', gql.GQL,
        'SELECT * FROM Person WHERE birthday = TIME()')

    self.AssertRaisesBadQuery(
        'Parse Error', gql.GQL,
        'SELECT * FROM Person WHERE birthday = GEOPT()')

    self.AssertRaisesBadQuery(
        'Parse Error', gql.GQL,
        'SELECT * FROM Person WHERE birthday = USER()')

    self.AssertRaisesBadQuery(
        'Parse Error', gql.GQL,
        'SELECT * FROM Person WHERE birthday = KEY()')

  def testFailedCastBadValue(self):
    """Test that cast operator properly fails with bad values."""

    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE birthday = DATETIME(:1, :2)')

    self.assertRaises(TypeError, key_compare.Run, 2008, 11)

    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE birthday = DATE(:1, :2)')
    self.AssertRaisesBadQuery('function takes 1 string or 3 integer values',
                              key_compare.Run, 2008, 11)

    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE birthday = TIME(:1, :2, :3, :4, :5)')
    self.AssertRaisesBadQuery('function takes', key_compare.Run,
                              9, 10, 11, 12, 13)

  def testLiteralCastingOperator(self):
    """Test literal casting operators."""
    link_compare = gql.GQL(
        'SELECT * FROM Person WHERE user = USER(\'larry@google.com\')')
    res = [a for a in link_compare.Run()]
    self.assertCountEqual([self.larry], res)

    geo_compare = gql.GQL(
        'SELECT * FROM Person WHERE location = GEOPT(40.0, 100.0)')
    res_geo = [a for a in geo_compare.Run()]
    self.assertCountEqual([self.chris], res_geo)

    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE hero = KEY(\'Person\', %i)' %
        self.elvis.key().id())
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bizarrolarry], res_key)


    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE hero = KEY(\'%s\')' % str(self.elvis.key()))
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bizarrolarry], res_key)


    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE birthday = DATETIME(1980, 2, 2)')
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.chris], res_key)


    key_compare = gql.GQL(
        'SELECT * FROM Person '
        '  WHERE birthday = DATETIME(\'1980-02-02 00:00:00\')')
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.chris], res_key)


    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE birthday = DATE(1991, 10, 10)')
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bret], res_key)


    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE birthday = DATE(\'1991-10-10\')')
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bret], res_key)


    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE time_of_birth = TIME(4,20,0)')
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bizarrolarry], res_key)


    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE time_of_birth = TIME(\'04:20:00\')')
    res_key = [a for a in key_compare.Run()]
    self.assertCountEqual([self.bizarrolarry], res_key)

  def testParemeterCastingOperator(self):
    """Test literal casting operators."""
    link_compare = gql.GQL(
        'SELECT * FROM Person WHERE user = USER(:1)')
    res = [a for a in link_compare.Run('larry@google.com')]
    self.assertCountEqual([self.larry], res)

    geo_compare = gql.GQL(
        'SELECT * FROM Person WHERE location = GEOPT(:1, :2)')
    res_geo = [a for a in geo_compare.Run(40.0, 100.0)]
    self.assertCountEqual([self.chris], res_geo)

    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE hero = KEY(:2, :1)')
    res_key = [a for a in key_compare.Run(self.elvis.key().id(), 'Person')]
    self.assertCountEqual([self.bizarrolarry], res_key)


    key_compare = gql.GQL(
        'SELECT * FROM Person '
        '  WHERE birthday = DATETIME(:1)')
    res_key = [a for a in key_compare.Run('1980-02-02 00:00:00')]
    self.assertCountEqual([self.chris], res_key)


    time_compare = gql.GQL(
        'SELECT * FROM Person '
        '  WHERE birthday = TIME(:1, :2, :3)')
    self.assertRaises(datastore_errors.BadQueryError,
                      time_compare.Run, 19, 59, 100)

  def testMixedLiteralParamCastingOperator(self):
    """Test mixed literal and parameter casting operators."""
    geo_compare = gql.GQL(
        'SELECT * FROM Person WHERE location = GEOPT(40.0, :1)')
    res_geo = [a for a in geo_compare.Run(100.0)]
    self.assertCountEqual([self.chris], res_geo)

    key_compare = gql.GQL(
        'SELECT * FROM Person WHERE hero = KEY(\'Person\', :1)')
    res_key = [a for a in key_compare.Run(self.elvis.key().id())]
    self.assertCountEqual([self.bizarrolarry], res_key)


    key_compare = gql.GQL(
        'SELECT * FROM Person '
        '  WHERE birthday = DATETIME(1980, :1, :2)')
    res_key = [a for a in key_compare.Run(2, 2)]
    self.assertCountEqual([self.chris], res_key)

  def testUnusedArguments(self):
    """Test failure on running a query which passes unnecessary arguments."""
    select = gql.GQL("""SELECT * FROM Person
                        WHERE favorite_number = :2 and phone = :1""")
    self.assertRaises(datastore_errors.BadArgumentError,
                      select.Run, '111-1111', 100, 50)

  def testWhereInQueryParseable(self):

    gql.GQL('SELECT * FROM Person WHERE email in :1')
    gql.GQL('SELECT * FROM Person WHERE email in :1 AND phone IN :2')

  def testWhereAncestorQuery(self):
    select = gql.GQL('SELECT * FROM Person WHERE ANCESTOR IS :1')
    results = [a for a in select.Run(self.elvis)]
    self.assertLen(results, 2)
    self.assertCountEqual([self.elvis, self.lisamarie], results)


    results_with_key = [a for a in select.Run(self.elvis.key())]
    self.assertLen(results_with_key, 2)
    self.assertCountEqual([self.elvis, self.lisamarie], results_with_key)


    select_multiple = gql.GQL('SELECT * FROM Person'
                              '  WHERE ANCESTOR IS :1 AND email > :email')
    results = [a for a in select_multiple.Run(self.elvis, **self.elvis)]
    self.assertLen(results, 1)
    self.assertCountEqual([self.lisamarie], results)

  def testWhereAncestorFails(self):
    failed_select = gql.GQL
    self.assertRaises(datastore_errors.BadQueryError,
                      failed_select,
                      'SELECT * FROM Person WHERE ancestor = :1')
    self.assertRaises(datastore_errors.BadQueryError,
                      failed_select,
                      'SELECT * FROM Person WHERE ancestor > :1')
    self.assertRaises(datastore_errors.BadQueryError,
                      failed_select,
                      'SELECT * FROM Person WHERE ancestor >= :1')
    self.assertRaises(datastore_errors.BadQueryError,
                      failed_select,
                      'SELECT * FROM Person WHERE ancestor < :1')
    self.assertRaises(datastore_errors.BadQueryError,
                      failed_select,
                      'SELECT * FROM Person WHERE ancestor <= :1')
    self.assertRaises(datastore_errors.BadQueryError,
                      failed_select,
                      'SELECT * FROM Person WHERE ancestor != :1')


    self.assertRaises(datastore_errors.BadQueryError,
                      failed_select,
                      'SELECT * FROM Person'
                      '  WHERE ANCESTOR IS :1 AND ANCESTOR IS :2')

  def testWhereFailedIsComparison(self):

    select = gql.GQL
    self.assertRaises(datastore_errors.BadQueryError,
                      select, 'SELECT * FROM Person WHERE email is :1')

  def testExecuteWhereQuery(self):
    """Test that binding in the Execute command works."""
    params = {}
    params['email'] = 'mysen@google.com'
    results = [a for a in gql.Execute(
        """SELECT * FROM Person WHERE email = :email and
        favorite_number = :2 and phone = :1""",
        '555-1234', 93, **params)]
    self.assertLen(results, 1)
    self.assertEqual(self.chris, results[0])

  def testHintParsing(self):


    select = gql.GQL('SELECT * FROM Person HINT order_first')
    self.assertEqual(select.hint(), 'ORDER_FIRST')

    select = gql.GQL('SELECT * FROM Person HINT ANCESTOR_FIRST')
    self.assertEqual(select.hint(), 'ANCESTOR_FIRST')

    select = gql.GQL('SELECT * FROM Person HINT filter_first')
    self.assertEqual(select.hint(), 'FILTER_FIRST')



  def testLimitParsing(self):
    select = gql.GQL('SELECT * FROM Person LIMIT 100')
    self.assertEqual(select.limit(), 100)

    select_offset = gql.GQL('SELECT * FROM Person LIMIT 50, 100')
    self.assertEqual(select_offset.limit(), 100)

    select_offset2 = gql.GQL('SELECT * FROM Person LIMIT 100 OFFSET 50')
    self.assertEqual(select_offset2.limit(), 100)

    select = gql.GQL
    self.assertRaises(datastore_errors.BadQueryError,
                      select, 'SELECT * FROM Person limit 0')

    select = gql.GQL
    self.assertRaises(datastore_errors.BadQueryError,
                      select, 'SELECT * FROM Person limit 1,1 OFFSET 1')

  def testLimitQuery(self):

    select = gql.GQL('SELECT * FROM Person ORDER BY email LIMIT 2')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertEqual([self.bret, self.elvis], results)


    select = gql.GQL('SELECT * FROM Person ORDER BY email LIMIT 0, 2')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertEqual([self.bret, self.elvis], results)


    select = gql.GQL('SELECT * FROM Person ORDER BY email LIMIT 1, 2')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertEqual([self.elvis, self.thefoo], results)


    select = gql.GQL('SELECT * FROM Person ORDER BY email LIMIT 10, 4')
    results = [a for a in select.Run()]
    self.assertLen(results, 1)
    self.assertEqual([self.chris], results)

  def testOffsetQuery(self):

    select = gql.GQL('SELECT * FROM Person OFFSET 0')
    results = [a for a in select.Run()]
    self.assertEqual(len(results), len(self.all_entities))
    self.assertCountEqual(self.all_entities, results)


    select = gql.GQL('SELECT * FROM Person ORDER BY email LIMIT 2 OFFSET 1')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertEqual([self.elvis, self.thefoo], results)


    select_skip_to_end = gql.GQL('SELECT * FROM Person ORDER BY email OFFSET 9')
    results = [a for a in select_skip_to_end.Run()]
    self.assertLen(results, 2)
    self.assertEqual([self.hillary, self.chris], results)

  def testOrderByParsing(self):



    select = gql.GQL('SELECT * FROM Person ORDER by email desc')
    self.assertLen(select.orderings(), 1)
    self.assertEqual(select.orderings()[0][1], datastore.Query.DESCENDING)

    select = gql.GQL('SELECT * FROM Person ORDER   by email')
    self.assertLen(select.orderings(), 1)
    self.assertEqual(select.orderings()[0][1], datastore.Query.ASCENDING)

    select = gql.GQL('SELECT * FROM Person ORDER by email ASC')
    self.assertLen(select.orderings(), 1)
    self.assertEqual(select.orderings()[0][1], datastore.Query.ASCENDING)

    select = gql.GQL('SELECT * FROM Person ORDER by email, phone')
    self.assertLen(select.orderings(), 2)
    self.assertEqual(select.orderings()[0][1], datastore.Query.ASCENDING)

    select = gql.GQL('SELECT * FROM Person ORDER by email DESC, phone')
    self.assertLen(select.orderings(), 2)
    self.assertEqual(select.orderings()[0][1], datastore.Query.DESCENDING)
    self.assertEqual(select.orderings()[1][1], datastore.Query.ASCENDING)

  def testOrderByQuery(self):

    select = gql.GQL('SELECT * FROM Person ORDER by email DESC LIMIT 1')
    results = select.Run()
    self.assertLen(results, 1)
    self.assertEqual(results[0], self.chris)

  def testMultipleOrderByQuery(self):

    select = gql.GQL("""SELECT * FROM Person
        ORDER by email, phone DESC, favorite_number""")
    results = list(select.Run())
    self.assertEqual(results,
                     [self.thefoo, self.bizarrolarry, self.larry, self.hillary,
                      self.chris])

  def testKeywordCase(self):
    """Test to ensure that case is ignored when parsing keywords."""
    select = gql.GQL(
        'select * from Person where email = :1 order by email desc limit 1')
    results = select.Run('mysen@google.com')
    self.assertLen(results, 1)
    self.assertEqual(results[0], self.chris)

    select = gql.GQL(
        'SELECT * FROM Person WHERE email = :1 ORDER BY email DESC LIMIT 1')
    results = select.Run('mysen@google.com')
    self.assertLen(results, 1)
    self.assertEqual(results[0], self.chris)

    select = gql.GQL(
        'SElect * FROM Person wheRE email = :1 order by email desc limIT 1')
    results = select.Run('mysen@google.com')
    self.assertLen(results, 1)
    self.assertEqual(results[0], self.chris)

  def testKindless(self):
    select = gql.GQL('SELECT __key__')
    self.assertEqual(select._kind, None)
    select = gql.GQL('SELECT *')
    self.assertEqual(select._kind, None)
    select = gql.GQL('SELECT * WHERE __key__ > :1')
    self.assertEqual(select._kind, None)
    select = gql.GQL('SELECT * WHERE __key__ > :1 ORDER BY __key__ ASC')
    self.assertEqual(select._kind, None)
    select = gql.GQL('SELECT * WHERE __key__ > :1 AND acestor = :2 '
                     'ORDER BY __key__ ASC')
    self.assertEqual(select._kind, None)
    select = gql.GQL('SELECT * ORDER BY __key__ ASC')
    self.assertEqual(select._kind, None)

  def testKeysOnly(self):
    """Tests 'SELECT __key__ FROM ...' queries."""
    select = gql.GQL('SELECT __key__ FROM Person')
    self.assertCountEqual((e.key() for e in self.all_entities), select.Run())

    select = gql.GQL("SELECT __key__ FROM Person "
                     "WHERE email = 'foo@google.com'")
    self.assertCountEqual([self.thefoo.key()], select.Run())

  def testKeysOnlyMultiQueryNotSupported(self):
    """Tests that IN and != queries can't be keys only."""
    select = gql.GQL("SELECT __key__ FROM Person WHERE email != 'foo'")
    self.assertRaises(datastore_errors.BadQueryError, select.Run)

    select = gql.GQL('SELECT __key__ FROM Person WHERE email IN :1')
    self.assertRaises(datastore_errors.BadQueryError, select.Run,
                      ['foo', 'bar'])




    select = gql.GQL('SELECT __key__ FROM Person WHERE email IN :1')
    self.assertRaises(datastore_errors.BadQueryError, select.Run, ['foo'])

  def testDotInProperty(self):

    guido = datastore.Entity('Person')
    guido['address.street'] = 'Spear'
    guido['address.city'] = 'SF'
    guido['address.zip'] = 94105
    datastore.Put(guido)
    select = gql.GQL("SELECT * FROM Person WHERE address.street = 'Spear'")
    results = [a for a in select.Run()]
    self.assertEqual([guido], results)

  def AssertRaisesBadQuery(self, substr, callable_obj, *args):
    """Asserts that callable_obj(*args) raises a matching BadQueryError."""
    try:
      callable_obj(*args)
    except datastore_errors.BadQueryError as err:
      self.assertIn(substr, str(err))
    else:
      self.fail('Expected a BadQueryError but parsed successfully')

  def AssertSameProperties(self, expected_list, actual_list, properties):
    """Asserts that two sets of results are equal for the given properties.

    Args:
      expected_list: the list of expected Entitys.
      actual_list: the list of actual Entitys.
      properties: the list of properties to compare on.
    """
    self.assertEqual(len(expected_list), len(actual_list))
    for expected, actual in zip(expected_list, actual_list):
      for prop in properties:
        self.assertEqual(prop in expected, prop in actual)
        if prop in expected:
          self.assertEqual(expected[prop], actual[prop])


class BugsTest(absltest.TestCase):
  """Unittests for bugs found in GQL."""

  def setUp(self):
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()


    stub = datastore_file_stub.DatastoreFileStub('test_app',
                                                 '/dev/null',
                                                 '/dev/null')
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
    os.environ['APPLICATION_ID'] = 'test_app'


    self.bret = datastore.Entity('Person')
    self.bret['email'] = 'btaylor@google.com'
    self.bret['phone'] = ['555-1234', '555-4000']
    datastore.Put(self.bret)

    self.jon = datastore.Entity('Person')
    self.jon['email'] = 'jonmac@google.com'
    self.jon['phone'] = ['555-5678', '555-4000']
    datastore.Put(self.jon)

    self.ken = datastore.Entity('Person')
    self.ken['email'] = 'kash@google.com'
    datastore.Put(self.ken)

    self.kevin = datastore.Entity('Person')
    self.kevin['email'] = 'kgibbs@google.com'
    self.kevin['phone'] = '555-6789'
    datastore.Put(self.kevin)

    self.chris = datastore.Entity('Person')
    self.chris['email'] = 'mysen@google.com'
    self.chris['phone'] = '555-1234'
    self.chris['favorite_number'] = 93
    self.chris['quote'] = ''
    datastore.Put(self.chris)

    self.all_entities = [self.bret, self.jon, self.ken, self.kevin, self.chris]

    self.one = datastore.Entity('A')
    self.one['count'] = 2
    self.one['rating'] = 1
    datastore.Put(self.one)

    self.two = datastore.Entity('A')
    self.two['count'] = 1
    self.two['rating'] = 4
    datastore.Put(self.two)

    self.all_a = [self.one, self.two]

  def testSelectWithUnprocessedTokens(self):
    """Test for Bug # 1042804.

    Bug found that invalid queries were properly being processed.
    For example:
      SELECT * FROM MyModel SELECT * FROM MyModel ORDER BY date DESC

    In cases like these, the parser would finish processing valid tokens and
    complete with tokens still unprocessed, which is really a malformed query
    (though it was assumed to be a good one because there were no parse errors
    on existing tokens).
    """
    bad_query = 'SELECT * FROM Person SELECT * FROM Person ORDER BY date DESC'
    self.assertRaises(datastore_errors.BadQueryError,
                      gql.GQL, bad_query)

  def testOrderByMultipleValues(self):
    """Test for Bug # 1070637."""
    select = gql.GQL('Select * From A Order By rating, count DESC')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertEqual([self.one, self.two], results)

    select = gql.GQL('Select * From A Order By rating DESC, count DESC')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertEqual([self.two, self.one], results)

    select = gql.GQL('Select * From A Order By rating DESC, count DESC LIMIT 2')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertEqual([self.two, self.one], results)

  def testWhereEmptyString(self):
    """Test for Empty String Parse Bug."""
    select = gql.GQL('SELECT * FROM Person WHERE quote = \'\'')
    results = [a for a in select.Run()]
    self.assertEqual([self.chris], results)

  def testEqualModelParseError(self):
    """Test for bug #1183399 which is improperly parsing in a model."""

    class stringType(db.Model):
      strData = db.StringProperty()

    entity = stringType()
    entity.strData = 'bbb'
    entity.put()

    entity_match = stringType()
    entity_match.strData = 'aaa'
    entity_match.put()

    entity = stringType()
    entity.strData = 'ccc'
    entity.put()

    query = stringType.gql("where strData = 'aaa'")
    entity = query.get()
    self.assertEqual(entity.strData, entity_match.strData)

  def testNotEqualModelParseError(self):
    """Test for bug #1183399 which is improperly parsing in a model."""

    class stringType(db.Model):
      strData = db.StringProperty()

    entity = stringType()
    entity.strData = 'aaa'
    entity.put()

    entity_match = stringType()
    entity_match.strData = 'bbb'
    entity_match.put()

    entity = stringType()
    entity.strData = 'aaa'
    entity.put()

    query = stringType.gql("where strData != 'aaa'")
    entity = query.get()
    self.assertEqual(entity.strData, entity_match.strData)

  def testMultiQueryCounts(self):
    """Test for BUG # 1291401.

    Tests failures when calling count() on multi-query results.
    Bug was found when doing counts on an IN condition on a model. But, the
    problem should surface regardless of the existence of a model.
    """

    class MyEntity(db.Model):
      mylist = db.ListProperty(int)

    ent = MyEntity(mylist=[1])
    ent.put()

    ent = MyEntity(mylist=[3])
    ent.put()


    q1 = db.GqlQuery('SELECT * FROM MyEntity')
    self.assertEqual(2, q1.count())
    self.assertEqual(1, q1.count(1))


    q2 = db.GqlQuery('SELECT * FROM MyEntity WHERE mylist IN :1', [1])
    self.assertEqual(1, q2.count())


    q3 = db.GqlQuery('SELECT * FROM MyEntity WHERE mylist IN :1', [1, 2])
    self.assertEqual(1, q3.count())
    self.assertEqual(1, q3.count(2))


    q_limit = db.GqlQuery('SELECT * FROM MyEntity WHERE mylist IN :1', [1, 3])
    self.assertEqual(1, q_limit.count(1))
    self.assertEqual(2, q_limit.count(2))

  def testNonINListValueErrorHandler(self):
    """Test related to bug #1688699.

    Tests an error handler that prevented list filter values with operators
    other than IN.
    """
    self.assertRaises(datastore_errors.BadQueryError, gql.GQL,
                      'SELECT * FROM Foo WHERE x = (0, 1)')


class GqlMultiQueryTest(absltest.TestCase):
  """Test queries which require merge-sorts (multiple queries)."""

  def setUp(self):
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()


    stub = datastore_file_stub.DatastoreFileStub('test_app',
                                                 '/dev/null',
                                                 '/dev/null')
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
    os.environ['APPLICATION_ID'] = 'test_app'


    self.bret = datastore.Entity('Person')
    self.bret['email'] = 'btaylor@google.com'
    self.bret['phone'] = ['555-1234', '555-4000']
    self.bret['cost_center'] = 987
    self.bret['location'] = datastore_types.GeoPt(50.0, 80.0)
    datastore.Put(self.bret)

    self.jon = datastore.Entity('Person')
    self.jon['email'] = 'jonmac@google.com'
    self.jon['phone'] = ['555-4000', '555-5678']
    self.jon['cost_center'] = 987
    self.jon['location'] = datastore_types.GeoPt(40.0, 100.0)
    self.jon['random_data'] = 'bar'
    datastore.Put(self.jon)

    self.ken = datastore.Entity('Person')
    self.ken['email'] = 'kash@google.com'
    self.ken['phone'] = '999-9876'
    self.ken['cost_center'] = 123
    self.ken['random_data'] = 0
    datastore.Put(self.ken)

    self.kevin = datastore.Entity('Person')
    self.kevin['email'] = 'kgibbs@google.com'
    self.kevin['phone'] = '555-6789'
    self.kevin['cost_center'] = 123
    self.kevin['random_data'] = datetime.datetime(1999, 12, 31)
    datastore.Put(self.kevin)

    self.chris = datastore.Entity('Person')
    self.chris['email'] = 'mysen@google.com'
    self.chris['phone'] = '555-1234'
    self.chris['cost_center'] = 123
    datastore.Put(self.chris)

    self.larry = datastore.Entity('Person')
    self.larry['email'] = 'larry@google.com'
    self.larry['phone'] = ['111-1234', '999-9876']
    self.larry['cost_center'] = 987
    datastore.Put(self.larry)

    self.hillary = datastore.Entity('Person')
    self.hillary['email'] = 'mrsbill@google.com'
    self.hillary['phone'] = '555-1234'
    self.hillary['cost_center'] = 987
    datastore.Put(self.hillary)

    self.thefoo = datastore.Entity('Person')
    self.thefoo['email'] = 'foo@google.com'
    self.thefoo['phone'] = ['555-9012', '555-1234']
    self.thefoo['cost_center'] = 123
    datastore.Put(self.thefoo)

    self.all_entities = ([self.bret, self.jon, self.ken, self.kevin, self.chris,
                          self.hillary, self.larry, self.thefoo])

  def testQueryEstimate(self):
    select = gql.GQL("""SELECT * FROM Person WHERE phone != '555-1234'
        ORDER by email""")
    self.assertLen(select.EnumerateQueries(set(), (), {}), 2)

    select_mixed = gql.GQL("""SELECT * FROM Person
        WHERE phone != '555-1234' AND email = 'kash@google.com'""")
    self.assertLen(select_mixed.EnumerateQueries(set(), (), {}), 2)

    select_multi_ne = gql.GQL("""SELECT * FROM Person
        WHERE phone != '555-1234' AND cost_center != 987
        ORDER by email""")
    self.assertLen(select_multi_ne.EnumerateQueries(set(), (), {}), 4)

    select_in = gql.GQL("""SELECT * FROM Person WHERE phone IN :1""")
    self.assertLen(select_in.EnumerateQueries(set(), ([1, 2, 3, 4],), {}), 4)

    select_multi_in = gql.GQL("""SELECT * FROM Person
        WHERE phone IN :1 AND email IN :2""")
    self.assertLen(
        select_multi_in.EnumerateQueries(set(), ([1, 2, 3, 4], [5, 6, 7, 8, 9]),
                                         {}), 20)

    select_mixed = gql.GQL("""SELECT * FROM Person
        WHERE phone IN :1 and name != 'Joe'""")
    self.assertLen(select_mixed.EnumerateQueries(set(), ([1, 2, 3, 4],), {}), 8)

  def testEnumerateQueries(self):
    select = gql.GQL("""SELECT * FROM Person WHERE phone != '555-1234'""")
    result = select.EnumerateQueries(set(), (), {})
    self.assertCountEqual([{
        'phone <': '555-1234'
    }, {
        'phone >': '555-1234'
    }], result)

    select_multi_ne = gql.GQL("""SELECT * FROM Person
        WHERE phone != '555-1234' AND num != 1""")
    result = select_multi_ne.EnumerateQueries(set(), (), {})
    self.assertLen(result, 4)
    self.assertCountEqual([{
        'phone <': '555-1234',
        'num <': 1
    }, {
        'phone <': '555-1234',
        'num >': 1
    }, {
        'phone >': '555-1234',
        'num <': 1
    }, {
        'phone >': '555-1234',
        'num >': 1
    }], result)

  def testEnumerateQueriesIn(self):
    select_in = gql.GQL("""SELECT * FROM Person WHERE phone IN :1""")
    result_in = select_in.EnumerateQueries(set(), ([1, 2, 3],), {})
    self.assertLen(result_in, 3)
    self.assertCountEqual([{
        'phone =': 1
    }, {
        'phone =': 2
    }, {
        'phone =': 3
    }], result_in)

    select_multiple_in = gql.GQL("""SELECT * FROM Person
        WHERE phone IN :1 and num in :2""")
    result_multiple_in = select_multiple_in.EnumerateQueries(
        set(), ([1, 2, 3], [100, 200, 300]), {})
    self.assertLen(result_multiple_in, 9)
    expected = []
    for i in range(1, 4):
      for j in range(1, 4):
        expected.append({'phone =': i, 'num =': j * 100})
    self.assertCountEqual(expected, result_multiple_in)

  def testEnumerateQueriesMixed(self):
    """Test the numeration of all queries given mixed query conditions."""
    select = gql.GQL("""SELECT * FROM Person
        WHERE phone IN :1 AND num IN :2 AND name != 'jon'""")
    result = select.EnumerateQueries(
        set(), ([1, 2, 3], [100, 200, 300]), {})
    self.assertLen(result, 18)
    expected = []
    for i in range(1, 4):
      for j in range(1, 4):
        expected.append({'phone =': i, 'num =': j * 100, 'name <': 'jon'})
        expected.append({'phone =': i, 'num =': j * 100, 'name >': 'jon'})
    self.assertCountEqual(expected, result)

    select = gql.GQL("""SELECT * FROM Person
        WHERE phone IN :1 AND num IN :2 AND name != 'jon' AND number = 1239""")
    result = select.EnumerateQueries(
        set(), ([1, 2, 3], [100, 200, 300]), {})
    self.assertLen(result, 18)
    expected = []
    for i in range(1, 4):
      for j in range(1, 4):
        expected.append({'phone =': i, 'num =': j * 100, 'name <': 'jon'})
        expected.append({'phone =': i, 'num =': j * 100, 'name >': 'jon'})
    self.assertCountEqual(expected, result)

  def testSortOrder(self):
    select = gql.GQL("""SELECT * FROM Person""")
    result = [a for a in select.Run()]
    self.assertCountEqual(self.all_entities, result)

    prev_result = result[0]
    for next_result in result[1:]:
      self.assertLess(prev_result.key(), next_result.key())
      prev_result = next_result

  def testExecuteWhereQueryNotEqual(self):

    select = gql.GQL("""SELECT * FROM Person WHERE phone != '555-1234'""")
    result = [a for a in select.Run()]
    expected_results = [self.jon, self.ken, self.kevin, self.larry,
                        self.thefoo, self.bret]

    self.assertLen(result, 6)
    self.assertCountEqual(expected_results, result)


    select_ordered = gql.GQL("""SELECT * FROM Person WHERE phone != '555-1234'
        ORDER BY phone, cost_center""")
    result_ordered = [a for a in select_ordered.Run()]
    expected_results_ordered = [self.ken, self.kevin, self.thefoo, self.jon,
                                self.larry, self.bret]


    self.assertLen(result_ordered, 6)
    self.assertCountEqual(expected_results_ordered, result_ordered)

  def testOrderByCorrect(self):
    select_ = gql.GQL("""SELECT * FROM Person WHERE phone != '555-1234'
        ORDER BY phone DESC, cost_center, email""")
    result_ = [a for a in select_.Run()]
    expected_results = [self.ken, self.larry, self.thefoo,
                        self.kevin, self.jon, self.bret]


    self.assertCountEqual(expected_results, result_)
    self.assertEqual(len(expected_results), len(result_))
    self.assertEqual(expected_results, result_)

    select_ = gql.GQL("""SELECT * FROM Person WHERE cost_center != 400
        ORDER BY cost_center, email""")
    result_ = [a for a in select_.Run()]
    expected_results = [self.thefoo, self.ken, self.kevin, self.chris,
                        self.bret, self.jon, self.larry, self.hillary]

    self.assertEqual(expected_results, result_)

  def testOrderByWithQuotedOrderProperties(self):
    select_ = gql.GQL("""SELECT * FROM Person WHERE cost_center != 400
        ORDER BY "cost_center", "email" """)
    result_ = [a for a in select_.Run()]
    expected_results = [self.thefoo, self.ken, self.kevin, self.chris,
                        self.bret, self.jon, self.larry, self.hillary]

    self.assertEqual(expected_results, result_)

  def testExecuteWhereQueryIn(self):

    select = gql.GQL('SELECT * FROM Person WHERE email in :1')
    results = [a for a in select.Run(['kash@google.com',
                                      'larry@google.com',
                                      'mysen@google.com'])]
    self.assertLen(results, 3)
    self.assertCountEqual([self.ken, self.larry, self.chris], results)


    select = gql.GQL('SELECT * FROM Person WHERE location in :1')
    results = [a for a in select.Run([datastore_types.GeoPt(50.0, 80.0),
                                      datastore_types.GeoPt(40.0, 100.0)])]
    self.assertLen(results, 2)
    self.assertCountEqual([self.bret, self.jon], results)


    select = gql.GQL('SELECT * FROM Person WHERE random_data in :1')
    results = [a for a in select.Run(['bar', 0,
                                      datetime.datetime(1999, 12, 31)])]
    self.assertLen(results, 3)
    self.assertCountEqual([self.jon, self.ken, self.kevin], results)


    select = gql.GQL('SELECT * FROM Person WHERE email in :1')
    self.assertRaises(datastore_errors.BadValueError,
                      select.Run,
                      ['kash@google.com', []])


    select = gql.GQL('SELECT * FROM Person WHERE email in :1')
    results = [a for a in select.Run([])]
    self.assertEmpty(results)


    select_multi_in = gql.GQL("""SELECT * FROM Person
        WHERE email IN :1 AND cost_center IN :2
        ORDER BY email DESC""")
    results_multi_in = [a for a in
                        select_multi_in.Run(['kash@google.com',
                                             'larry@google.com',
                                             'mrsbill@google.com',
                                             'mysen@google.com'],
                                            [123])]
    self.assertLen(results_multi_in, 2)
    self.assertEqual([self.chris, self.ken], results_multi_in)


    select_multi_in = gql.GQL("""SELECT * FROM Person
        WHERE email IN :1 AND cost_center IN :2
        ORDER BY email DESC""")
    results_multi_in = [a for a in
                        select_multi_in.Run(['kash@google.com',
                                             'larry@google.com',
                                             'mrsbill@google.com',
                                             'mysen@google.com'],
                                            [])]
    self.assertEmpty(results_multi_in)


    select_too_many_queries = gql.GQL("""SELECT * FROM Person
        WHERE email IN :1 AND phone IN :2 AND cost_center IN :3""")

    self.assertRaises(datastore_errors.BadArgumentError,
                      select_too_many_queries.Run,
                      ['kash@google.com', 'larry@google.com',
                       'mrsbill@google.com', 'mysen@google.com'],
                      ['555-1234', '555-9012', '555-5678', '555-4000'],
                      [123, 456, 987])

  def testExecuteWhereQueryInLiteral(self):

    select = gql.GQL('SELECT * FROM Person WHERE email IN '
                     '  (\'kash@google.com\',\'larry@google.com\', :1)')
    results = [a for a in select.Run('mysen@google.com')]
    self.assertLen(results, 3)
    self.assertCountEqual([self.ken, self.larry, self.chris], results)


    select = gql.GQL('SELECT * FROM Person WHERE location in '
                     '(GEOPT(50.0, 80.0), GEOPT(40.0, 100.0))')
    results = [a for a in select.Run()]
    self.assertLen(results, 2)
    self.assertCountEqual([self.bret, self.jon], results)


    select = gql.GQL('SELECT * FROM Person WHERE random_data in '
                     '(\'bar\', 0, DATETIME(1999, 12, 31))')
    results = [a for a in select.Run()]
    self.assertLen(results, 3)
    self.assertCountEqual([self.jon, self.ken, self.kevin], results)


    error_substr = 'Filter list value could not be cast'
    try:
      gql.GQL('SELECT * FROM Person WHERE email in (\'kash@google.com\', ())')
    except datastore_errors.BadQueryError as err:
      self.assertIn(error_substr, str(err))
    else:
      self.fail('Expected a BadQueryError but parsed successfully')

  def testMultiQueryLimit(self):

    select = gql.GQL("""SELECT * FROM Person
        WHERE email in :1 ORDER BY email DESC LIMIT 2""")
    results = list(select.Run(['kash@google.com', 'larry@google.com',
                               'mrsbill@google.com', 'mysen@google.com']))
    self.assertLen(results, 2)
    self.assertEqual([self.chris, self.hillary], results)

  def testMultiQueryLimitOffset(self):

    select = gql.GQL("""SELECT * FROM Person
        WHERE email in :1 ORDER BY email DESC LIMIT 1 OFFSET 1""")
    results = list(select.Run(['kash@google.com', 'larry@google.com',
                               'mrsbill@google.com', 'mysen@google.com']))
    self.assertLen(results, 1)
    self.assertEqual([self.hillary], results)

  def testMixedInAndNotEquals(self):
    select = gql.GQL("""SELECT * FROM Person
        WHERE email IN :1 AND cost_center != 987""")
    results = [a for a in select.Run(['kash@google.com',
                                      'larry@google.com',
                                      'jonmac@google.com',
                                      'mysen@google.com'])]
    self.assertLen(results, 2)
    self.assertCountEqual([self.ken, self.chris], results)

    select_multi_in = gql.GQL("""SELECT * FROM Person
        WHERE email != 'larry@google.com' AND
              cost_center IN :1 AND
              phone IN :2
        ORDER BY email DESC""")
    results_multi_in = [a for a in
                        select_multi_in.Run([123, 987],
                                            ['999-9876', '555-5678',
                                             '555-4000'])]
    self.assertLen(results_multi_in, 3)
    self.assertEqual([self.ken, self.jon, self.bret], results_multi_in)

  def testWhereCharacterParameter(self):
    """Test for Bug # 1119118.

    Tests for the error condition found where the parser was failing due to
    "Unknown parameter" errors, which should not be reachable code.
    """
    select = gql.GQL('SELECT * FROM Person WHERE email = :b')
    args = {}
    args['b'] = 'mysen@google.com'
    results = [a for a in select.Run(b='mysen@google.com')]
    self.assertEqual([self.chris], results)


if __name__ == '__main__':
  absltest.main()

