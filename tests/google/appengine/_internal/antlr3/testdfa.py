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


class TestDFA(unittest.TestCase):
    """Test case for the DFA class."""

    def setUp(self):
        """Setup test fixure.

        We need a Recognizer in order to instanciate a DFA.

        """

        class TRecognizer(google.appengine._internal.antlr3.BaseRecognizer):
            antlr_version = google.appengine._internal.antlr3.runtime_version

        self.recog = TRecognizer()


    def testInit(self):
        """DFA.__init__()

        Just a smoke test.

        """

        dfa = google.appengine._internal.antlr3.DFA(
            self.recog, 1,
            eot=[],
            eof=[],
            min=[],
            max=[],
            accept=[],
            special=[],
            transition=[]
            )


    def testUnpack(self):
        """DFA.unpack()"""

        self.failUnlessEqual(
            google.appengine._internal.antlr3.DFA.unpack(
            u"\1\3\1\4\2\uffff\1\5\22\uffff\1\2\31\uffff\1\6\6\uffff"
            u"\32\6\4\uffff\1\6\1\uffff\32\6"
            ),
            [ 3, 4, -1, -1, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
              -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1,
              -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
              6, -1, -1, -1, -1, -1, -1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
              6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, -1, -1, -1, -1, 6, -1,
              6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
              6, 6, 6, 6, 6
              ]
            )



if __name__ == "__main__":
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))
