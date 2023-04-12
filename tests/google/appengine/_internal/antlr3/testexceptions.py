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
import unittest
import google.appengine._internal.antlr3
import testbase


class TestRecognitionException(unittest.TestCase):
    """Tests for the google.appengine._internal.antlr3.RecognitionException class"""

    def testInitNone(self):
        """RecognitionException.__init__()"""

        exc = google.appengine._internal.antlr3.RecognitionException()


class TestEarlyExitException(unittest.TestCase):
    """Tests for the google.appengine._internal.antlr3.EarlyExitException class"""

    @testbase.broken("FIXME", Exception)
    def testInitNone(self):
        """EarlyExitException.__init__()"""

        exc = google.appengine._internal.antlr3.EarlyExitException()


class TestFailedPredicateException(unittest.TestCase):
    """Tests for the google.appengine._internal.antlr3.FailedPredicateException class"""

    @testbase.broken("FIXME", Exception)
    def testInitNone(self):
        """FailedPredicateException.__init__()"""

        exc = google.appengine._internal.antlr3.FailedPredicateException()


class TestMismatchedNotSetException(unittest.TestCase):
    """Tests for the google.appengine._internal.antlr3.MismatchedNotSetException class"""

    @testbase.broken("FIXME", Exception)
    def testInitNone(self):
        """MismatchedNotSetException.__init__()"""

        exc = google.appengine._internal.antlr3.MismatchedNotSetException()


class TestMismatchedRangeException(unittest.TestCase):
    """Tests for the google.appengine._internal.antlr3.MismatchedRangeException class"""

    @testbase.broken("FIXME", Exception)
    def testInitNone(self):
        """MismatchedRangeException.__init__()"""

        exc = google.appengine._internal.antlr3.MismatchedRangeException()


class TestMismatchedSetException(unittest.TestCase):
    """Tests for the google.appengine._internal.antlr3.MismatchedSetException class"""

    @testbase.broken("FIXME", Exception)
    def testInitNone(self):
        """MismatchedSetException.__init__()"""

        exc = google.appengine._internal.antlr3.MismatchedSetException()


class TestMismatchedTokenException(unittest.TestCase):
    """Tests for the google.appengine._internal.antlr3.MismatchedTokenException class"""

    @testbase.broken("FIXME", Exception)
    def testInitNone(self):
        """MismatchedTokenException.__init__()"""

        exc = google.appengine._internal.antlr3.MismatchedTokenException()


class TestMismatchedTreeNodeException(unittest.TestCase):
    """Tests for the google.appengine._internal.antlr3.MismatchedTreeNodeException class"""

    @testbase.broken("FIXME", Exception)
    def testInitNone(self):
        """MismatchedTreeNodeException.__init__()"""

        exc = google.appengine._internal.antlr3.MismatchedTreeNodeException()


class TestNoViableAltException(unittest.TestCase):
    """Tests for the google.appengine._internal.antlr3.NoViableAltException class"""

    @testbase.broken("FIXME", Exception)
    def testInitNone(self):
        """NoViableAltException.__init__()"""

        exc = google.appengine._internal.antlr3.NoViableAltException()


if __name__ == "__main__":
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))
