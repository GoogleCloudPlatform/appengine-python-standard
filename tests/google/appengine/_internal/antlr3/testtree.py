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


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import unittest

from google.appengine._internal.antlr3 import CommonToken, UP, DOWN, EOF
from google.appengine._internal.antlr3.tree import CommonTreeNodeStream, CommonTree, CommonTreeAdaptor
from six import StringIO
from six.moves import range


class TestTreeNodeStream(unittest.TestCase):
  """Test case for the TreeNodeStream class."""

  def setUp(self):
    self.adaptor = CommonTreeAdaptor()

  def newStream(self, t):
    """Build new stream; let's us override to test other streams."""
    return CommonTreeNodeStream(t)

  def testSingleNode(self):
    t = CommonTree(CommonToken(101))

    stream = self.newStream(t)
    expecting = "101"
    found = self.toNodesOnlyString(stream)
    self.failUnlessEqual(expecting, found)

    expecting = "101"
    found = str(stream)
    self.failUnlessEqual(expecting, found)

  def testTwoChildrenOfNilRoot(self):

    class V(CommonTree):

      def __init__(self, token=None, ttype=None, x=None):
        if x is not None:
          self.x = x

        if ttype is not None and token is None:
          self.token = CommonToken(type=ttype)

        if token is not None:
          self.token = token

      def __str__(self):
        if self.token is not None:
          txt = self.token.text
        else:
          txt = ""

        txt += "<V>"
        return txt

    root_0 = self.adaptor.nil()
    t = V(ttype=101, x=2)
    u = V(token=CommonToken(type=102, text="102"))
    self.adaptor.addChild(root_0, t)
    self.adaptor.addChild(root_0, u)
    self.assert_(root_0.parent is None)
    self.assertEquals(-1, root_0.childIndex)
    self.assertEquals(0, t.childIndex)
    self.assertEquals(1, u.childIndex)

  def test4Nodes(self):

    t = CommonTree(CommonToken(101))
    t.addChild(CommonTree(CommonToken(102)))
    t.getChild(0).addChild(CommonTree(CommonToken(103)))
    t.addChild(CommonTree(CommonToken(104)))

    stream = self.newStream(t)
    expecting = "101 102 103 104"
    found = self.toNodesOnlyString(stream)
    self.failUnlessEqual(expecting, found)

    expecting = "101 2 102 2 103 3 104 3"
    found = str(stream)
    self.failUnlessEqual(expecting, found)

  def testList(self):
    root = CommonTree(None)

    t = CommonTree(CommonToken(101))
    t.addChild(CommonTree(CommonToken(102)))
    t.getChild(0).addChild(CommonTree(CommonToken(103)))
    t.addChild(CommonTree(CommonToken(104)))

    u = CommonTree(CommonToken(105))

    root.addChild(t)
    root.addChild(u)

    stream = CommonTreeNodeStream(root)
    expecting = "101 102 103 104 105"
    found = self.toNodesOnlyString(stream)
    self.failUnlessEqual(expecting, found)

    expecting = "101 2 102 2 103 3 104 3 105"
    found = str(stream)
    self.failUnlessEqual(expecting, found)

  def testFlatList(self):
    root = CommonTree(None)

    root.addChild(CommonTree(CommonToken(101)))
    root.addChild(CommonTree(CommonToken(102)))
    root.addChild(CommonTree(CommonToken(103)))

    stream = CommonTreeNodeStream(root)
    expecting = "101 102 103"
    found = self.toNodesOnlyString(stream)
    self.failUnlessEqual(expecting, found)

    expecting = "101 102 103"
    found = str(stream)
    self.failUnlessEqual(expecting, found)

  def testListWithOneNode(self):
    root = CommonTree(None)

    root.addChild(CommonTree(CommonToken(101)))

    stream = CommonTreeNodeStream(root)
    expecting = "101"
    found = self.toNodesOnlyString(stream)
    self.failUnlessEqual(expecting, found)

    expecting = "101"
    found = str(stream)
    self.failUnlessEqual(expecting, found)

  def testAoverB(self):
    t = CommonTree(CommonToken(101))
    t.addChild(CommonTree(CommonToken(102)))

    stream = self.newStream(t)
    expecting = "101 102"
    found = self.toNodesOnlyString(stream)
    self.failUnlessEqual(expecting, found)

    expecting = "101 2 102 3"
    found = str(stream)
    self.failUnlessEqual(expecting, found)

  def testLT(self):

    t = CommonTree(CommonToken(101))
    t.addChild(CommonTree(CommonToken(102)))
    t.getChild(0).addChild(CommonTree(CommonToken(103)))
    t.addChild(CommonTree(CommonToken(104)))

    stream = self.newStream(t)
    self.failUnlessEqual(101, stream.LT(1).getType())
    self.failUnlessEqual(DOWN, stream.LT(2).getType())
    self.failUnlessEqual(102, stream.LT(3).getType())
    self.failUnlessEqual(DOWN, stream.LT(4).getType())
    self.failUnlessEqual(103, stream.LT(5).getType())
    self.failUnlessEqual(UP, stream.LT(6).getType())
    self.failUnlessEqual(104, stream.LT(7).getType())
    self.failUnlessEqual(UP, stream.LT(8).getType())
    self.failUnlessEqual(EOF, stream.LT(9).getType())

    self.failUnlessEqual(EOF, stream.LT(100).getType())

  def testMarkRewindEntire(self):



    r0 = CommonTree(CommonToken(101))
    r1 = CommonTree(CommonToken(102))
    r0.addChild(r1)
    r1.addChild(CommonTree(CommonToken(103)))
    r2 = CommonTree(CommonToken(106))
    r2.addChild(CommonTree(CommonToken(107)))
    r1.addChild(r2)
    r0.addChild(CommonTree(CommonToken(104)))
    r0.addChild(CommonTree(CommonToken(105)))

    stream = CommonTreeNodeStream(r0)
    m = stream.mark()
    for _ in range(13):
      stream.LT(1)
      stream.consume()

    self.failUnlessEqual(EOF, stream.LT(1).getType())
    self.failUnlessEqual(UP, stream.LT(-1).getType())
    stream.rewind(m)


    for _ in range(13):
      stream.LT(1)
      stream.consume()

    self.failUnlessEqual(EOF, stream.LT(1).getType())
    self.failUnlessEqual(UP, stream.LT(-1).getType())

  def testMarkRewindInMiddle(self):



    r0 = CommonTree(CommonToken(101))
    r1 = CommonTree(CommonToken(102))
    r0.addChild(r1)
    r1.addChild(CommonTree(CommonToken(103)))
    r2 = CommonTree(CommonToken(106))
    r2.addChild(CommonTree(CommonToken(107)))
    r1.addChild(r2)
    r0.addChild(CommonTree(CommonToken(104)))
    r0.addChild(CommonTree(CommonToken(105)))

    stream = CommonTreeNodeStream(r0)
    for _ in range(7):

      stream.consume()

    self.failUnlessEqual(107, stream.LT(1).getType())
    m = stream.mark()
    stream.consume()
    stream.consume()
    stream.consume()
    stream.consume()
    stream.rewind(m)

    self.failUnlessEqual(107, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(UP, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(UP, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(104, stream.LT(1).getType())
    stream.consume()

    self.failUnlessEqual(105, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(UP, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(EOF, stream.LT(1).getType())
    self.failUnlessEqual(UP, stream.LT(-1).getType())

  def testMarkRewindNested(self):



    r0 = CommonTree(CommonToken(101))
    r1 = CommonTree(CommonToken(102))
    r0.addChild(r1)
    r1.addChild(CommonTree(CommonToken(103)))
    r2 = CommonTree(CommonToken(106))
    r2.addChild(CommonTree(CommonToken(107)))
    r1.addChild(r2)
    r0.addChild(CommonTree(CommonToken(104)))
    r0.addChild(CommonTree(CommonToken(105)))

    stream = CommonTreeNodeStream(r0)
    m = stream.mark()
    stream.consume()
    stream.consume()
    m2 = stream.mark()
    stream.consume()
    stream.consume()
    stream.consume()
    stream.consume()
    stream.rewind(m2)
    self.failUnlessEqual(102, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(DOWN, stream.LT(1).getType())
    stream.consume()

    stream.rewind(m)
    self.failUnlessEqual(101, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(DOWN, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(102, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(DOWN, stream.LT(1).getType())

  def testSeek(self):



    r0 = CommonTree(CommonToken(101))
    r1 = CommonTree(CommonToken(102))
    r0.addChild(r1)
    r1.addChild(CommonTree(CommonToken(103)))
    r2 = CommonTree(CommonToken(106))
    r2.addChild(CommonTree(CommonToken(107)))
    r1.addChild(r2)
    r0.addChild(CommonTree(CommonToken(104)))
    r0.addChild(CommonTree(CommonToken(105)))

    stream = CommonTreeNodeStream(r0)
    stream.consume()
    stream.consume()
    stream.consume()
    stream.seek(7)
    self.failUnlessEqual(107, stream.LT(1).getType())
    stream.consume()
    stream.consume()
    stream.consume()
    self.failUnlessEqual(104, stream.LT(1).getType())

  def testSeekFromStart(self):



    r0 = CommonTree(CommonToken(101))
    r1 = CommonTree(CommonToken(102))
    r0.addChild(r1)
    r1.addChild(CommonTree(CommonToken(103)))
    r2 = CommonTree(CommonToken(106))
    r2.addChild(CommonTree(CommonToken(107)))
    r1.addChild(r2)
    r0.addChild(CommonTree(CommonToken(104)))
    r0.addChild(CommonTree(CommonToken(105)))

    stream = CommonTreeNodeStream(r0)
    stream.seek(7)
    self.failUnlessEqual(107, stream.LT(1).getType())
    stream.consume()
    stream.consume()
    stream.consume()
    self.failUnlessEqual(104, stream.LT(1).getType())

  def toNodesOnlyString(self, nodes):
    buf = []
    for i in range(nodes.size()):
      t = nodes.LT(i + 1)
      type = nodes.getTreeAdaptor().getType(t)
      if not (type == DOWN or type == UP):
        buf.append(str(type))

    return " ".join(buf)


class TestCommonTreeNodeStream(unittest.TestCase):
  """Test case for the CommonTreeNodeStream class."""

  def testPushPop(self):



    r0 = CommonTree(CommonToken(101))
    r1 = CommonTree(CommonToken(102))
    r1.addChild(CommonTree(CommonToken(103)))
    r0.addChild(r1)
    r2 = CommonTree(CommonToken(104))
    r2.addChild(CommonTree(CommonToken(105)))
    r0.addChild(r2)
    r3 = CommonTree(CommonToken(106))
    r3.addChild(CommonTree(CommonToken(107)))
    r0.addChild(r3)
    r0.addChild(CommonTree(CommonToken(108)))
    r0.addChild(CommonTree(CommonToken(109)))

    stream = CommonTreeNodeStream(r0)
    expecting = "101 2 102 2 103 3 104 2 105 3 106 2 107 3 108 109 3"
    found = str(stream)
    self.failUnlessEqual(expecting, found)



    indexOf102 = 2
    indexOf107 = 12
    for _ in range(indexOf107):
      stream.consume()


    self.failUnlessEqual(107, stream.LT(1).getType())
    stream.push(indexOf102)
    self.failUnlessEqual(102, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(DOWN, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(103, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(UP, stream.LT(1).getType())

    stream.pop()
    self.failUnlessEqual(107, stream.LT(1).getType())

  def testNestedPushPop(self):



    r0 = CommonTree(CommonToken(101))
    r1 = CommonTree(CommonToken(102))
    r1.addChild(CommonTree(CommonToken(103)))
    r0.addChild(r1)
    r2 = CommonTree(CommonToken(104))
    r2.addChild(CommonTree(CommonToken(105)))
    r0.addChild(r2)
    r3 = CommonTree(CommonToken(106))
    r3.addChild(CommonTree(CommonToken(107)))
    r0.addChild(r3)
    r0.addChild(CommonTree(CommonToken(108)))
    r0.addChild(CommonTree(CommonToken(109)))

    stream = CommonTreeNodeStream(r0)




    indexOf102 = 2
    indexOf107 = 12
    for _ in range(indexOf107):
      stream.consume()

    self.failUnlessEqual(107, stream.LT(1).getType())

    stream.push(indexOf102)
    self.failUnlessEqual(102, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(DOWN, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(103, stream.LT(1).getType())
    stream.consume()


    indexOf104 = 6
    stream.push(indexOf104)
    self.failUnlessEqual(104, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(DOWN, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(105, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(UP, stream.LT(1).getType())

    stream.pop()

    self.failUnlessEqual(UP, stream.LT(1).getType())

    stream.pop()
    self.failUnlessEqual(107, stream.LT(1).getType())

  def testPushPopFromEOF(self):



    r0 = CommonTree(CommonToken(101))
    r1 = CommonTree(CommonToken(102))
    r1.addChild(CommonTree(CommonToken(103)))
    r0.addChild(r1)
    r2 = CommonTree(CommonToken(104))
    r2.addChild(CommonTree(CommonToken(105)))
    r0.addChild(r2)
    r3 = CommonTree(CommonToken(106))
    r3.addChild(CommonTree(CommonToken(107)))
    r0.addChild(r3)
    r0.addChild(CommonTree(CommonToken(108)))
    r0.addChild(CommonTree(CommonToken(109)))

    stream = CommonTreeNodeStream(r0)

    while stream.LA(1) != EOF:
      stream.consume()

    indexOf102 = 2
    indexOf104 = 6
    self.failUnlessEqual(EOF, stream.LT(1).getType())


    stream.push(indexOf102)
    self.failUnlessEqual(102, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(DOWN, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(103, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(UP, stream.LT(1).getType())

    stream.pop()
    self.failUnlessEqual(EOF, stream.LT(1).getType())


    stream.push(indexOf104)
    self.failUnlessEqual(104, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(DOWN, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(105, stream.LT(1).getType())
    stream.consume()
    self.failUnlessEqual(UP, stream.LT(1).getType())

    stream.pop()
    self.failUnlessEqual(EOF, stream.LT(1).getType())


class TestCommonTree(unittest.TestCase):
  """Test case for the CommonTree class."""

  def setUp(self):
    """Setup test fixure"""

    self.adaptor = CommonTreeAdaptor()

  def testSingleNode(self):
    t = CommonTree(CommonToken(101))
    self.failUnless(t.parent is None)
    self.failUnlessEqual(-1, t.childIndex)

  def test4Nodes(self):

    r0 = CommonTree(CommonToken(101))
    r0.addChild(CommonTree(CommonToken(102)))
    r0.getChild(0).addChild(CommonTree(CommonToken(103)))
    r0.addChild(CommonTree(CommonToken(104)))

    self.failUnless(r0.parent is None)
    self.failUnlessEqual(-1, r0.childIndex)

  def testList(self):

    r0 = CommonTree(None)
    c0 = CommonTree(CommonToken(101))
    r0.addChild(c0)
    c1 = CommonTree(CommonToken(102))
    r0.addChild(c1)
    c2 = CommonTree(CommonToken(103))
    r0.addChild(c2)

    self.failUnless(r0.parent is None)
    self.failUnlessEqual(-1, r0.childIndex)
    self.failUnlessEqual(r0, c0.parent)
    self.failUnlessEqual(0, c0.childIndex)
    self.failUnlessEqual(r0, c1.parent)
    self.failUnlessEqual(1, c1.childIndex)
    self.failUnlessEqual(r0, c2.parent)
    self.failUnlessEqual(2, c2.childIndex)

  def testList2(self):


    root = CommonTree(CommonToken(5))


    r0 = CommonTree(None)
    c0 = CommonTree(CommonToken(101))
    r0.addChild(c0)
    c1 = CommonTree(CommonToken(102))
    r0.addChild(c1)
    c2 = CommonTree(CommonToken(103))
    r0.addChild(c2)

    root.addChild(r0)

    self.failUnless(root.parent is None)
    self.failUnlessEqual(-1, root.childIndex)

    self.failUnlessEqual(root, c0.parent)
    self.failUnlessEqual(0, c0.childIndex)
    self.failUnlessEqual(root, c0.parent)
    self.failUnlessEqual(1, c1.childIndex)
    self.failUnlessEqual(root, c0.parent)
    self.failUnlessEqual(2, c2.childIndex)

  def testAddListToExistChildren(self):


    root = CommonTree(CommonToken(5))
    root.addChild(CommonTree(CommonToken(6)))


    r0 = CommonTree(None)
    c0 = CommonTree(CommonToken(101))
    r0.addChild(c0)
    c1 = CommonTree(CommonToken(102))
    r0.addChild(c1)
    c2 = CommonTree(CommonToken(103))
    r0.addChild(c2)

    root.addChild(r0)

    self.failUnless(root.parent is None)
    self.failUnlessEqual(-1, root.childIndex)

    self.failUnlessEqual(root, c0.parent)
    self.failUnlessEqual(1, c0.childIndex)
    self.failUnlessEqual(root, c0.parent)
    self.failUnlessEqual(2, c1.childIndex)
    self.failUnlessEqual(root, c0.parent)
    self.failUnlessEqual(3, c2.childIndex)

  def testDupTree(self):

    r0 = CommonTree(CommonToken(101))
    r1 = CommonTree(CommonToken(102))
    r0.addChild(r1)
    r1.addChild(CommonTree(CommonToken(103)))
    r2 = CommonTree(CommonToken(106))
    r2.addChild(CommonTree(CommonToken(107)))
    r1.addChild(r2)
    r0.addChild(CommonTree(CommonToken(104)))
    r0.addChild(CommonTree(CommonToken(105)))

    dup = self.adaptor.dupTree(r0)

    self.failUnless(dup.parent is None)
    self.failUnlessEqual(-1, dup.childIndex)
    dup.sanityCheckParentAndChildIndexes()

  def testBecomeRoot(self):

    newRoot = CommonTree(CommonToken(5))

    oldRoot = CommonTree(None)
    oldRoot.addChild(CommonTree(CommonToken(101)))
    oldRoot.addChild(CommonTree(CommonToken(102)))
    oldRoot.addChild(CommonTree(CommonToken(103)))

    self.adaptor.becomeRoot(newRoot, oldRoot)
    newRoot.sanityCheckParentAndChildIndexes()

  def testBecomeRoot2(self):

    newRoot = CommonTree(CommonToken(5))

    oldRoot = CommonTree(CommonToken(101))
    oldRoot.addChild(CommonTree(CommonToken(102)))
    oldRoot.addChild(CommonTree(CommonToken(103)))

    self.adaptor.becomeRoot(newRoot, oldRoot)
    newRoot.sanityCheckParentAndChildIndexes()

  def testBecomeRoot3(self):

    newRoot = CommonTree(None)
    newRoot.addChild(CommonTree(CommonToken(5)))

    oldRoot = CommonTree(None)
    oldRoot.addChild(CommonTree(CommonToken(101)))
    oldRoot.addChild(CommonTree(CommonToken(102)))
    oldRoot.addChild(CommonTree(CommonToken(103)))

    self.adaptor.becomeRoot(newRoot, oldRoot)
    newRoot.sanityCheckParentAndChildIndexes()

  def testBecomeRoot5(self):

    newRoot = CommonTree(None)
    newRoot.addChild(CommonTree(CommonToken(5)))

    oldRoot = CommonTree(CommonToken(101))
    oldRoot.addChild(CommonTree(CommonToken(102)))
    oldRoot.addChild(CommonTree(CommonToken(103)))

    self.adaptor.becomeRoot(newRoot, oldRoot)
    newRoot.sanityCheckParentAndChildIndexes()

  def testBecomeRoot6(self):

    root_0 = self.adaptor.nil()
    root_1 = self.adaptor.nil()
    root_1 = self.adaptor.becomeRoot(CommonTree(CommonToken(5)), root_1)

    self.adaptor.addChild(root_1, CommonTree(CommonToken(6)))

    self.adaptor.addChild(root_0, root_1)

    root_0.sanityCheckParentAndChildIndexes()



  def testReplaceWithNoChildren(self):
    t = CommonTree(CommonToken(101))
    newChild = CommonTree(CommonToken(5))
    error = False
    try:
      t.replaceChildren(0, 0, newChild)

    except IndexError:
      error = True

    self.failUnless(error)

  def testReplaceWithOneChildren(self):

    t = CommonTree(CommonToken(99, text="a"))
    c0 = CommonTree(CommonToken(99, text="b"))
    t.addChild(c0)

    newChild = CommonTree(CommonToken(99, text="c"))
    t.replaceChildren(0, 0, newChild)
    expecting = "(a c)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceInMiddle(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChild = CommonTree(CommonToken(99, text="x"))
    t.replaceChildren(1, 1, newChild)
    expecting = "(a b x d)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceAtLeft(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChild = CommonTree(CommonToken(99, text="x"))
    t.replaceChildren(0, 0, newChild)
    expecting = "(a x c d)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceAtRight(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChild = CommonTree(CommonToken(99, text="x"))
    t.replaceChildren(2, 2, newChild)
    expecting = "(a b c x)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceOneWithTwoAtLeft(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChildren = self.adaptor.nil()
    newChildren.addChild(CommonTree(CommonToken(99, text="x")))
    newChildren.addChild(CommonTree(CommonToken(99, text="y")))

    t.replaceChildren(0, 0, newChildren)
    expecting = "(a x y c d)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceOneWithTwoAtRight(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChildren = self.adaptor.nil()
    newChildren.addChild(CommonTree(CommonToken(99, text="x")))
    newChildren.addChild(CommonTree(CommonToken(99, text="y")))

    t.replaceChildren(2, 2, newChildren)
    expecting = "(a b c x y)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceOneWithTwoInMiddle(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChildren = self.adaptor.nil()
    newChildren.addChild(CommonTree(CommonToken(99, text="x")))
    newChildren.addChild(CommonTree(CommonToken(99, text="y")))

    t.replaceChildren(1, 1, newChildren)
    expecting = "(a b x y d)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceTwoWithOneAtLeft(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChild = CommonTree(CommonToken(99, text="x"))

    t.replaceChildren(0, 1, newChild)
    expecting = "(a x d)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceTwoWithOneAtRight(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChild = CommonTree(CommonToken(99, text="x"))

    t.replaceChildren(1, 2, newChild)
    expecting = "(a b x)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceAllWithOne(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChild = CommonTree(CommonToken(99, text="x"))

    t.replaceChildren(0, 2, newChild)
    expecting = "(a x)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()

  def testReplaceAllWithTwo(self):
    t = CommonTree(CommonToken(99, text="a"))
    t.addChild(CommonTree(CommonToken(99, text="b")))
    t.addChild(CommonTree(CommonToken(99, text="c")))
    t.addChild(CommonTree(CommonToken(99, text="d")))

    newChildren = self.adaptor.nil()
    newChildren.addChild(CommonTree(CommonToken(99, text="x")))
    newChildren.addChild(CommonTree(CommonToken(99, text="y")))

    t.replaceChildren(0, 2, newChildren)
    expecting = "(a x y)"
    self.failUnlessEqual(expecting, t.toStringTree())
    t.sanityCheckParentAndChildIndexes()



if __name__ == "__main__":
  unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))
