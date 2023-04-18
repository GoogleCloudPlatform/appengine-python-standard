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
""" @package google.appengine._internal.antlr3.tree
@brief ANTLR3 runtime package, tree module

This module contains all support classes for AST construction and tree parsers.

"""


































from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from google.appengine._internal.antlr3.constants import UP, DOWN, EOF, INVALID_TOKEN_TYPE
from google.appengine._internal.antlr3.exceptions import MismatchedTreeNodeException, MissingTokenException, UnwantedTokenException, MismatchedTokenException, NoViableAltException
from google.appengine._internal.antlr3.recognizers import BaseRecognizer, RuleReturnScope
from google.appengine._internal.antlr3.streams import IntStream
from google.appengine._internal.antlr3.tokens import CommonToken, Token, INVALID_TOKEN
import six
from six.moves import range









class RewriteCardinalityException(RuntimeError):
  """
    @brief Base class for all exceptions thrown during AST rewrite construction.

    This signifies a case where the cardinality of two or more elements
    in a subrule are different: (ID INT)+ where |ID|!=|INT|
    """

  def __init__(self, elementDescription):
    RuntimeError.__init__(self, elementDescription)

    self.elementDescription = elementDescription

  def getMessage(self):
    return self.elementDescription


class RewriteEarlyExitException(RewriteCardinalityException):
  """@brief No elements within a (...)+ in a rewrite rule"""

  def __init__(self, elementDescription=None):
    RewriteCardinalityException.__init__(self, elementDescription)


class RewriteEmptyStreamException(RewriteCardinalityException):
  """
    @brief Ref to ID or expr but no tokens in ID stream or subtrees in expr
    stream
    """

  pass








class Tree(object):
  """
    @brief Abstract baseclass for tree nodes.

    What does a tree look like?  ANTLR has a number of support classes
    such as CommonTreeNodeStream that work on these kinds of trees.  You
    don't have to make your trees implement this interface, but if you do,
    you'll be able to use more support code.

    NOTE: When constructing trees, ANTLR can build any kind of tree; it can
    even use Token objects as trees if you add a child list to your tokens.

    This is a tree node without any payload; just navigation and factory stuff.
    """

  def getChild(self, i):
    raise NotImplementedError

  def getChildCount(self):
    raise NotImplementedError

  def getParent(self):
    """Tree tracks parent and child index now > 3.0"""

    raise NotImplementedError

  def setParent(self, t):
    """Tree tracks parent and child index now > 3.0"""

    raise NotImplementedError

  def getChildIndex(self):
    """This node is what child index? 0..n-1"""

    raise NotImplementedError

  def setChildIndex(self, index):
    """This node is what child index? 0..n-1"""

    raise NotImplementedError

  def freshenParentAndChildIndexes(self):
    """Set the parent and child index values for all children"""

    raise NotImplementedError

  def addChild(self, t):
    """
        Add t as a child to this node.  If t is null, do nothing.  If t
        is nil, add all children of t to this' children.
        """

    raise NotImplementedError

  def setChild(self, i, t):
    """Set ith child (0..n-1) to t; t must be non-null and non-nil node"""

    raise NotImplementedError

  def deleteChild(self, i):
    raise NotImplementedError

  def replaceChildren(self, startChildIndex, stopChildIndex, t):
    """
        Delete children from start to stop and replace with t even if t is
        a list (nil-root tree).  num of children can increase or decrease.
        For huge child lists, inserting children can force walking rest of
        children to set their childindex; could be slow.
        """

    raise NotImplementedError

  def isNil(self):
    """
        Indicates the node is a nil node but may still have children, meaning
        the tree is a flat list.
        """

    raise NotImplementedError

  def getTokenStartIndex(self):
    """
        What is the smallest token index (indexing from 0) for this node
           and its children?
        """

    raise NotImplementedError

  def setTokenStartIndex(self, index):
    raise NotImplementedError

  def getTokenStopIndex(self):
    """
        What is the largest token index (indexing from 0) for this node
        and its children?
        """

    raise NotImplementedError

  def setTokenStopIndex(self, index):
    raise NotImplementedError

  def dupNode(self):
    raise NotImplementedError

  def getType(self):
    """Return a token type; needed for tree parsing."""

    raise NotImplementedError

  def getText(self):
    raise NotImplementedError

  def getLine(self):
    """
        In case we don't have a token payload, what is the line for errors?
        """

    raise NotImplementedError

  def getCharPositionInLine(self):
    raise NotImplementedError

  def toStringTree(self):
    raise NotImplementedError

  def toString(self):
    raise NotImplementedError



class TreeAdaptor(object):
  """
    @brief Abstract baseclass for tree adaptors.

    How to create and navigate trees.  Rather than have a separate factory
    and adaptor, I've merged them.  Makes sense to encapsulate.

    This takes the place of the tree construction code generated in the
    generated code in 2.x and the ASTFactory.

    I do not need to know the type of a tree at all so they are all
    generic Objects.  This may increase the amount of typecasting needed. :(
    """



  def createWithPayload(self, payload):
    """
        Create a tree node from Token object; for CommonTree type trees,
        then the token just becomes the payload.  This is the most
        common create call.

        Override if you want another kind of node to be built.
        """

    raise NotImplementedError

  def dupNode(self, treeNode):
    """Duplicate a single tree node.

        Override if you want another kind of node to be built.
    """

    raise NotImplementedError

  def dupTree(self, tree):
    """Duplicate tree recursively, using dupNode() for each node"""

    raise NotImplementedError

  def nil(self):
    """
        Return a nil node (an empty but non-null node) that can hold
        a list of element as the children.  If you want a flat tree (a list)
        use "t=adaptor.nil(); t.addChild(x); t.addChild(y);"
        """

    raise NotImplementedError

  def errorNode(self, input, start, stop, exc):
    """
        Return a tree node representing an error.  This node records the
        tokens consumed during error recovery.  The start token indicates the
        input symbol at which the error was detected.  The stop token indicates
        the last symbol consumed during recovery.

        You must specify the input stream so that the erroneous text can
        be packaged up in the error node.  The exception could be useful
        to some applications; default implementation stores ptr to it in
        the CommonErrorNode.

        This only makes sense during token parsing, not tree parsing.
        Tree parsing should happen only when parsing and tree construction
        succeed.
        """

    raise NotImplementedError

  def isNil(self, tree):
    """Is tree considered a nil node used to make lists of child nodes?"""

    raise NotImplementedError

  def addChild(self, t, child):
    """
        Add a child to the tree t.  If child is a flat tree (a list), make all
        in list children of t.  Warning: if t has no children, but child does
        and child isNil then you can decide it is ok to move children to t via
        t.children = child.children; i.e., without copying the array.  Just
        make sure that this is consistent with have the user will build
        ASTs. Do nothing if t or child is null.
        """

    raise NotImplementedError

  def becomeRoot(self, newRoot, oldRoot):
    """
        If oldRoot is a nil root, just copy or move the children to newRoot.
        If not a nil root, make oldRoot a child of newRoot.

           old=^(nil a b c), new=r yields ^(r a b c)
           old=^(a b c), new=r yields ^(r ^(a b c))

        If newRoot is a nil-rooted single child tree, use the single
        child as the new root node.

           old=^(nil a b c), new=^(nil r) yields ^(r a b c)
           old=^(a b c), new=^(nil r) yields ^(r ^(a b c))

        If oldRoot was null, it's ok, just return newRoot (even if isNil).

           old=null, new=r yields r
           old=null, new=^(nil r) yields ^(nil r)

        Return newRoot.  Throw an exception if newRoot is not a
        simple node or nil root with a single child node--it must be a root
        node.  If newRoot is ^(nil x) return x as newRoot.

        Be advised that it's ok for newRoot to point at oldRoot's
        children; i.e., you don't have to copy the list.  We are
        constructing these nodes so we should have this control for
        efficiency.
        """

    raise NotImplementedError

  def rulePostProcessing(self, root):
    """
        Given the root of the subtree created for this rule, post process
        it to do any simplifications or whatever you want.  A required
        behavior is to convert ^(nil singleSubtree) to singleSubtree
        as the setting of start/stop indexes relies on a single non-nil root
        for non-flat trees.

        Flat trees such as for lists like "idlist : ID+ ;" are left alone
        unless there is only one ID.  For a list, the start/stop indexes
        are set in the nil node.

        This method is executed after all rule tree construction and right
        before setTokenBoundaries().
        """

    raise NotImplementedError

  def getUniqueID(self, node):
    """For identifying trees.

        How to identify nodes so we can say "add node to a prior node"?
        Even becomeRoot is an issue.  Use System.identityHashCode(node)
        usually.
        """

    raise NotImplementedError



  def createFromToken(self, tokenType, fromToken, text=None):
    """
        Create a new node derived from a token, with a new token type and
        (optionally) new text.

        This is invoked from an imaginary node ref on right side of a
        rewrite rule as IMAG[$tokenLabel] or IMAG[$tokenLabel "IMAG"].

        This should invoke createToken(Token).
        """

    raise NotImplementedError

  def createFromType(self, tokenType, text):
    """Create a new node derived from a token, with a new token type.

        This is invoked from an imaginary node ref on right side of a
        rewrite rule as IMAG["IMAG"].

        This should invoke createToken(int,String).
        """

    raise NotImplementedError



  def getType(self, t):
    """For tree parsing, I need to know the token type of a node"""

    raise NotImplementedError

  def setType(self, t, type):
    """Node constructors can set the type of a node"""

    raise NotImplementedError

  def getText(self, t):
    raise NotImplementedError

  def setText(self, t, text):
    """Node constructors can set the text of a node"""

    raise NotImplementedError

  def getToken(self, t):
    """Return the token object from which this node was created.

        Currently used only for printing an error message.
        The error display routine in BaseRecognizer needs to
        display where the input the error occurred. If your
        tree of limitation does not store information that can
        lead you to the token, you can create a token filled with
        the appropriate information and pass that back.  See
        BaseRecognizer.getErrorMessage().
        """

    raise NotImplementedError

  def setTokenBoundaries(self, t, startToken, stopToken):
    """
        Where are the bounds in the input token stream for this node and
        all children?  Each rule that creates AST nodes will call this
        method right before returning.  Flat trees (i.e., lists) will
        still usually have a nil root node just to hold the children list.
        That node would contain the start/stop indexes then.
        """

    raise NotImplementedError

  def getTokenStartIndex(self, t):
    """
        Get the token start index for this subtree; return -1 if no such index
        """

    raise NotImplementedError

  def getTokenStopIndex(self, t):
    """
        Get the token stop index for this subtree; return -1 if no such index
        """

    raise NotImplementedError



  def getChild(self, t, i):
    """Get a child 0..n-1 node"""

    raise NotImplementedError

  def setChild(self, t, i, child):
    """Set ith child (0..n-1) to t; t must be non-null and non-nil node"""

    raise NotImplementedError

  def deleteChild(self, t, i):
    """Remove ith child and shift children down from right."""

    raise NotImplementedError

  def getChildCount(self, t):
    """How many children?  If 0, then this is a leaf node"""

    raise NotImplementedError

  def getParent(self, t):
    """
        Who is the parent node of this node; if null, implies node is root.
        If your node type doesn't handle this, it's ok but the tree rewrites
        in tree parsers need this functionality.
        """

    raise NotImplementedError

  def setParent(self, t, parent):
    """
        Who is the parent node of this node; if null, implies node is root.
        If your node type doesn't handle this, it's ok but the tree rewrites
        in tree parsers need this functionality.
        """

    raise NotImplementedError

  def getChildIndex(self, t):
    """
        What index is this node in the child list? Range: 0..n-1
        If your node type doesn't handle this, it's ok but the tree rewrites
        in tree parsers need this functionality.
        """

    raise NotImplementedError

  def setChildIndex(self, t, index):
    """
        What index is this node in the child list? Range: 0..n-1
        If your node type doesn't handle this, it's ok but the tree rewrites
        in tree parsers need this functionality.
        """

    raise NotImplementedError

  def replaceChildren(self, parent, startChildIndex, stopChildIndex, t):
    """
        Replace from start to stop child index of parent with t, which might
        be a list.  Number of children may be different
        after this call.

        If parent is null, don't do anything; must be at root of overall tree.
        Can't replace whatever points to the parent externally.  Do nothing.
        """

    raise NotImplementedError



  def create(self, *args):
    """
        Deprecated, use createWithPayload, createFromToken or createFromType.

        This method only exists to mimic the Java interface of TreeAdaptor.

        """

    if len(args) == 1 and isinstance(args[0], Token):






      return self.createWithPayload(args[0])

    if (len(args) == 2 and isinstance(args[0], six.integer_types) and
        isinstance(args[1], Token)):






      return self.createFromToken(args[0], args[1])

    if (len(args) == 3 and isinstance(args[0], six.integer_types) and
        isinstance(args[1], Token) and isinstance(args[2], six.string_types)):






      return self.createFromToken(args[0], args[1], args[2])

    if (len(args) == 2 and isinstance(args[0], six.integer_types) and
        isinstance(args[1], six.string_types)):






      return self.createFromType(args[0], args[1])

    raise TypeError("No create method with this signature found: %s" %
                    (", ".join(type(v).__name__ for v in args)))















class BaseTree(Tree):
  """
    @brief A generic tree implementation with no payload.

    You must subclass to
    actually have any user data.  ANTLR v3 uses a list of children approach
    instead of the child-sibling approach in v2.  A flat tree (a list) is
    an empty node whose children represent the list.  An empty, but
    non-null node is called "nil".
    """





  def __init__(self, node=None):
    """
        Create a new node from an existing node does nothing for BaseTree
        as there are no fields other than the children list, which cannot
        be copied as the children are not considered part of this node.
        """

    Tree.__init__(self)
    self.children = []
    self.parent = None
    self.childIndex = 0

  def getChild(self, i):
    try:
      return self.children[i]
    except IndexError:
      return None

  def getChildren(self):
    """@brief Get the children internal List

        Note that if you directly mess with
        the list, do so at your own risk.
        """


    return self.children

  def getFirstChildWithType(self, treeType):
    for child in self.children:
      if child.getType() == treeType:
        return child

    return None

  def getChildCount(self):
    return len(self.children)

  def addChild(self, childTree):
    """Add t as child of this node.

        Warning: if t has no children, but child does
        and child isNil then this routine moves children to t via
        t.children = child.children; i.e., without copying the array.
        """




    if childTree is None:
      return

    if childTree.isNil():


      if self.children is childTree.children:
        raise ValueError("attempt to add child list to itself")


      for idx, child in enumerate(childTree.children):
        child.parent = self
        child.childIndex = len(self.children) + idx

      self.children += childTree.children

    else:

      self.children.append(childTree)
      childTree.parent = self
      childTree.childIndex = len(self.children) - 1

  def addChildren(self, children):
    """Add all elements of kids list as children of this node"""

    self.children += children

  def setChild(self, i, t):
    if t is None:
      return

    if t.isNil():
      raise ValueError("Can't set single child to a list")

    self.children[i] = t
    t.parent = self
    t.childIndex = i

  def deleteChild(self, i):
    killed = self.children[i]

    del self.children[i]


    for idx, child in enumerate(self.children[i:]):
      child.childIndex = i + idx

    return killed

  def replaceChildren(self, startChildIndex, stopChildIndex, newTree):
    """
        Delete children from start to stop and replace with t even if t is
        a list (nil-root tree).  num of children can increase or decrease.
        For huge child lists, inserting children can force walking rest of
        children to set their childindex; could be slow.
        """

    if (startChildIndex >= len(self.children) or
        stopChildIndex >= len(self.children)):
      raise IndexError("indexes invalid")

    replacingHowMany = stopChildIndex - startChildIndex + 1


    if newTree.isNil():
      newChildren = newTree.children

    else:
      newChildren = [newTree]

    replacingWithHowMany = len(newChildren)
    delta = replacingHowMany - replacingWithHowMany

    if delta == 0:

      for idx, child in enumerate(newChildren):
        self.children[idx + startChildIndex] = child
        child.parent = self
        child.childIndex = idx + startChildIndex

    else:



      del self.children[startChildIndex:stopChildIndex + 1]


      self.children[startChildIndex:startChildIndex] = newChildren


      self.freshenParentAndChildIndexes(startChildIndex)

  def isNil(self):
    return False

  def freshenParentAndChildIndexes(self, offset=0):
    for idx, child in enumerate(self.children[offset:]):
      child.childIndex = idx + offset
      child.parent = self

  def sanityCheckParentAndChildIndexes(self, parent=None, i=-1):
    if parent != self.parent:
      raise ValueError("parents don't match; expected %r found %r" %
                       (parent, self.parent))

    if i != self.childIndex:
      raise ValueError("child indexes don't match; expected %d found %d" %
                       (i, self.childIndex))

    for idx, child in enumerate(self.children):
      child.sanityCheckParentAndChildIndexes(self, idx)

  def getChildIndex(self):
    """BaseTree doesn't track child indexes."""

    return 0

  def setChildIndex(self, index):
    """BaseTree doesn't track child indexes."""

    pass

  def getParent(self):
    """BaseTree doesn't track parent pointers."""

    return None

  def setParent(self, t):
    """BaseTree doesn't track parent pointers."""

    pass

  def toStringTree(self):
    """Print out a whole tree not just a node"""

    if len(self.children) == 0:
      return self.toString()

    buf = []
    if not self.isNil():
      buf.append("(")
      buf.append(self.toString())
      buf.append(" ")

    for i, child in enumerate(self.children):
      if i > 0:
        buf.append(" ")
      buf.append(child.toStringTree())

    if not self.isNil():
      buf.append(")")

    return "".join(buf)

  def getLine(self):
    return 0

  def getCharPositionInLine(self):
    return 0

  def toString(self):
    """Override to say how a node (not a tree) should look as text"""

    raise NotImplementedError



class BaseTreeAdaptor(TreeAdaptor):
  """
    @brief A TreeAdaptor that works with any Tree implementation.
    """





  def nil(self):
    return self.createWithPayload(None)

  def errorNode(self, input, start, stop, exc):
    """
        create tree node that holds the start and stop tokens associated
        with an error.

        If you specify your own kind of tree nodes, you will likely have to
        override this method. CommonTree returns Token.INVALID_TOKEN_TYPE
        if no token payload but you might have to set token type for diff
        node type.
        """

    return CommonErrorNode(input, start, stop, exc)

  def isNil(self, tree):
    return tree.isNil()

  def dupTree(self, t, parent=None):
    """
        This is generic in the sense that it will work with any kind of
        tree (not just Tree interface).  It invokes the adaptor routines
        not the tree node routines to do the construction.
        """

    if t is None:
      return None

    newTree = self.dupNode(t)




    self.setChildIndex(newTree, self.getChildIndex(t))

    self.setParent(newTree, parent)

    for i in range(self.getChildCount(t)):
      child = self.getChild(t, i)
      newSubTree = self.dupTree(child, t)
      self.addChild(newTree, newSubTree)

    return newTree

  def addChild(self, tree, child):
    """
        Add a child to the tree t.  If child is a flat tree (a list), make all
        in list children of t.  Warning: if t has no children, but child does
        and child isNil then you can decide it is ok to move children to t via
        t.children = child.children; i.e., without copying the array.  Just
        make sure that this is consistent with have the user will build
        ASTs.
        """




    if tree is not None and child is not None:
      tree.addChild(child)

  def becomeRoot(self, newRoot, oldRoot):
    """
        If oldRoot is a nil root, just copy or move the children to newRoot.
        If not a nil root, make oldRoot a child of newRoot.

          old=^(nil a b c), new=r yields ^(r a b c)
          old=^(a b c), new=r yields ^(r ^(a b c))

        If newRoot is a nil-rooted single child tree, use the single
        child as the new root node.

          old=^(nil a b c), new=^(nil r) yields ^(r a b c)
          old=^(a b c), new=^(nil r) yields ^(r ^(a b c))

        If oldRoot was null, it's ok, just return newRoot (even if isNil).

          old=null, new=r yields r
          old=null, new=^(nil r) yields ^(nil r)

        Return newRoot.  Throw an exception if newRoot is not a
        simple node or nil root with a single child node--it must be a root
        node.  If newRoot is ^(nil x) return x as newRoot.

        Be advised that it's ok for newRoot to point at oldRoot's
        children; i.e., you don't have to copy the list.  We are
        constructing these nodes so we should have this control for
        efficiency.
        """

    if isinstance(newRoot, Token):
      newRoot = self.create(newRoot)

    if oldRoot is None:
      return newRoot

    if not isinstance(newRoot, CommonTree):
      newRoot = self.createWithPayload(newRoot)


    if newRoot.isNil():
      nc = newRoot.getChildCount()
      if nc == 1:
        newRoot = newRoot.getChild(0)

      elif nc > 1:

        raise RuntimeError("more than one node as root")




    newRoot.addChild(oldRoot)
    return newRoot

  def rulePostProcessing(self, root):
    """Transform ^(nil x) to x and nil to null"""

    if root is not None and root.isNil():
      if root.getChildCount() == 0:
        root = None

      elif root.getChildCount() == 1:
        root = root.getChild(0)

        root.setParent(None)
        root.setChildIndex(-1)

    return root

  def createFromToken(self, tokenType, fromToken, text=None):
    assert isinstance(tokenType, six.integer_types), type(tokenType).__name__
    assert isinstance(fromToken, Token), type(fromToken).__name__
    assert text is None or isinstance(text,
                                      six.string_types), type(text).__name__

    fromToken = self.createToken(fromToken)
    fromToken.type = tokenType
    if text is not None:
      fromToken.text = text
    t = self.createWithPayload(fromToken)
    return t

  def createFromType(self, tokenType, text):
    assert isinstance(tokenType, six.integer_types), type(tokenType).__name__
    assert isinstance(text, six.string_types), type(text).__name__

    fromToken = self.createToken(tokenType=tokenType, text=text)
    t = self.createWithPayload(fromToken)
    return t

  def getType(self, t):
    return t.getType()

  def setType(self, t, type):
    raise RuntimeError("don't know enough about Tree node")

  def getText(self, t):
    return t.getText()

  def setText(self, t, text):
    raise RuntimeError("don't know enough about Tree node")

  def getChild(self, t, i):
    return t.getChild(i)

  def setChild(self, t, i, child):
    t.setChild(i, child)

  def deleteChild(self, t, i):
    return t.deleteChild(i)

  def getChildCount(self, t):
    return t.getChildCount()

  def getUniqueID(self, node):
    return hash(node)

  def createToken(self, fromToken=None, tokenType=None, text=None):
    """
        Tell me how to create a token for use with imaginary token nodes.
        For example, there is probably no input symbol associated with imaginary
        token DECL, but you need to create it as a payload or whatever for
        the DECL node as in ^(DECL type ID).

        If you care what the token payload objects' type is, you should
        override this method and any other createToken variant.
        """

    raise NotImplementedError


















class CommonTree(BaseTree):
  """@brief A tree node that is wrapper for a Token object.

    After 3.0 release
    while building tree rewrite stuff, it became clear that computing
    parent and child index is very difficult and cumbersome.  Better to
    spend the space in every tree node.  If you don't want these extra
    fields, it's easy to cut them out in your own BaseTree subclass.

    """

  def __init__(self, payload):
    BaseTree.__init__(self)



    self.startIndex = -1
    self.stopIndex = -1


    self.parent = None


    self.childIndex = -1


    if payload is None:
      self.token = None

    elif isinstance(payload, CommonTree):
      self.token = payload.token
      self.startIndex = payload.startIndex
      self.stopIndex = payload.stopIndex

    elif payload is None or isinstance(payload, Token):
      self.token = payload

    else:
      raise TypeError(type(payload).__name__)

  def getToken(self):
    return self.token

  def dupNode(self):
    return CommonTree(self)

  def isNil(self):
    return self.token is None

  def getType(self):
    if self.token is None:
      return INVALID_TOKEN_TYPE

    return self.token.getType()

  type = property(getType)

  def getText(self):
    if self.token is None:
      return None

    return self.token.text

  text = property(getText)

  def getLine(self):
    if self.token is None or self.token.getLine() == 0:
      if self.getChildCount():
        return self.getChild(0).getLine()
      else:
        return 0

    return self.token.getLine()

  line = property(getLine)

  def getCharPositionInLine(self):
    if self.token is None or self.token.getCharPositionInLine() == -1:
      if self.getChildCount():
        return self.getChild(0).getCharPositionInLine()
      else:
        return 0

    else:
      return self.token.getCharPositionInLine()

  charPositionInLine = property(getCharPositionInLine)

  def getTokenStartIndex(self):
    if self.startIndex == -1 and self.token is not None:
      return self.token.getTokenIndex()

    return self.startIndex

  def setTokenStartIndex(self, index):
    self.startIndex = index

  tokenStartIndex = property(getTokenStartIndex, setTokenStartIndex)

  def getTokenStopIndex(self):
    if self.stopIndex == -1 and self.token is not None:
      return self.token.getTokenIndex()

    return self.stopIndex

  def setTokenStopIndex(self, index):
    self.stopIndex = index

  tokenStopIndex = property(getTokenStopIndex, setTokenStopIndex)

  def getChildIndex(self):

    return self.childIndex

  def setChildIndex(self, idx):

    self.childIndex = idx

  def getParent(self):

    return self.parent

  def setParent(self, t):

    self.parent = t

  def toString(self):
    if self.isNil():
      return "nil"

    if self.getType() == INVALID_TOKEN_TYPE:
      return "<errornode>"

    return self.token.text

  __str__ = toString

  def toStringTree(self):
    if not self.children:
      return self.toString()

    ret = ""
    if not self.isNil():
      ret += "(%s " % (self.toString())

    ret += " ".join([child.toStringTree() for child in self.children])

    if not self.isNil():
      ret += ")"

    return ret


INVALID_NODE = CommonTree(INVALID_TOKEN)


class CommonErrorNode(CommonTree):
  """A node representing erroneous token range in token stream"""

  def __init__(self, input, start, stop, exc):
    CommonTree.__init__(self, None)

    if (stop is None or (stop.getTokenIndex() < start.getTokenIndex() and
                         stop.getType() != EOF)):




      stop = start

    self.input = input
    self.start = start
    self.stop = stop
    self.trappedException = exc

  def isNil(self):
    return False

  def getType(self):
    return INVALID_TOKEN_TYPE

  def getText(self):
    if isinstance(self.start, Token):
      i = self.start.getTokenIndex()
      j = self.stop.getTokenIndex()
      if self.stop.getType() == EOF:
        j = self.input.size()

      badText = self.input.toString(i, j)

    elif isinstance(self.start, Tree):
      badText = self.input.toString(self.start, self.stop)

    else:


      badText = "<unknown>"

    return badText

  def toString(self):
    if isinstance(self.trappedException, MissingTokenException):
      return ("<missing type: " + str(self.trappedException.getMissingType()) +
              ">")

    elif isinstance(self.trappedException, UnwantedTokenException):
      return ("<extraneous: " +
              str(self.trappedException.getUnexpectedToken()) + ", resync=" +
              self.getText() + ">")

    elif isinstance(self.trappedException, MismatchedTokenException):
      return ("<mismatched token: " + str(self.trappedException.token) +
              ", resync=" + self.getText() + ">")

    elif isinstance(self.trappedException, NoViableAltException):
      return ("<unexpected: " + str(self.trappedException.token) + ", resync=" +
              self.getText() + ">")

    return "<error: " + self.getText() + ">"


class CommonTreeAdaptor(BaseTreeAdaptor):
  """
    @brief A TreeAdaptor that works with any Tree implementation.

    It provides
    really just factory methods; all the work is done by BaseTreeAdaptor.
    If you would like to have different tokens created than ClassicToken
    objects, you need to override this and then set the parser tree adaptor to
    use your subclass.

    To get your parser to build nodes of a different type, override
    create(Token).
    """

  def dupNode(self, treeNode):
    """
        Duplicate a node.  This is part of the factory;
        override if you want another kind of node to be built.

        I could use reflection to prevent having to override this
        but reflection is slow.
        """

    if treeNode is None:
      return None

    return treeNode.dupNode()

  def createWithPayload(self, payload):
    return CommonTree(payload)

  def createToken(self, fromToken=None, tokenType=None, text=None):
    """
        Tell me how to create a token for use with imaginary token nodes.
        For example, there is probably no input symbol associated with imaginary
        token DECL, but you need to create it as a payload or whatever for
        the DECL node as in ^(DECL type ID).

        If you care what the token payload objects' type is, you should
        override this method and any other createToken variant.
        """

    if fromToken is not None:
      return CommonToken(oldToken=fromToken)

    return CommonToken(type=tokenType, text=text)

  def setTokenBoundaries(self, t, startToken, stopToken):
    """
        Track start/stop token for subtree root created for a rule.
        Only works with Tree nodes.  For rules that match nothing,
        seems like this will yield start=i and stop=i-1 in a nil node.
        Might be useful info so I'll not force to be i..i.
        """

    if t is None:
      return

    start = 0
    stop = 0

    if startToken is not None:
      start = startToken.index

    if stopToken is not None:
      stop = stopToken.index

    t.setTokenStartIndex(start)
    t.setTokenStopIndex(stop)

  def getTokenStartIndex(self, t):
    if t is None:
      return -1
    return t.getTokenStartIndex()

  def getTokenStopIndex(self, t):
    if t is None:
      return -1
    return t.getTokenStopIndex()

  def getText(self, t):
    if t is None:
      return None
    return t.getText()

  def getType(self, t):
    if t is None:
      return INVALID_TOKEN_TYPE

    return t.getType()

  def getToken(self, t):
    """
        What is the Token associated with this node?  If
        you are not using CommonTree, then you must
        override this in your own adaptor.
        """

    if isinstance(t, CommonTree):
      return t.getToken()

    return None

  def getChild(self, t, i):
    if t is None:
      return None
    return t.getChild(i)

  def getChildCount(self, t):
    if t is None:
      return 0
    return t.getChildCount()

  def getParent(self, t):
    return t.getParent()

  def setParent(self, t, parent):
    t.setParent(parent)

  def getChildIndex(self, t):
    return t.getChildIndex()

  def setChildIndex(self, t, index):
    t.setChildIndex(index)

  def replaceChildren(self, parent, startChildIndex, stopChildIndex, t):
    if parent is not None:
      parent.replaceChildren(startChildIndex, stopChildIndex, t)


















class TreeNodeStream(IntStream):
  """@brief A stream of tree nodes

    It accessing nodes from a tree of some kind.
    """





  def get(self, i):
    """Get a tree node at an absolute index i; 0..n-1.

        If you don't want to buffer up nodes, then this method makes no
        sense for you.
        """

    raise NotImplementedError

  def LT(self, k):
    """
        Get tree node at current input pointer + i ahead where i=1 is next node.
        i<0 indicates nodes in the past.  So LT(-1) is previous node, but
        implementations are not required to provide results for k < -1.
        LT(0) is undefined.  For i>=n, return null.
        Return null for LT(0) and any index that results in an absolute address
        that is negative.

        This is analogus to the LT() method of the TokenStream, but this
        returns a tree node instead of a token.  Makes code gen identical
        for both parser and tree grammars. :)
        """

    raise NotImplementedError

  def getTreeSource(self):
    """
        Where is this stream pulling nodes from?  This is not the name, but
        the object that provides node objects.
        """

    raise NotImplementedError

  def getTokenStream(self):
    """
        If the tree associated with this stream was created from a TokenStream,
        you can specify it here.  Used to do rule $text attribute in tree
        parser.  Optional unless you use tree parser rule text attribute
        or output=template and rewrite=true options.
        """

    raise NotImplementedError

  def getTreeAdaptor(self):
    """
        What adaptor can tell me how to interpret/navigate nodes and
        trees.  E.g., get text of a node.
        """

    raise NotImplementedError

  def setUniqueNavigationNodes(self, uniqueNavigationNodes):
    """
        As we flatten the tree, we use UP, DOWN nodes to represent
        the tree structure.  When debugging we need unique nodes
        so we have to instantiate new ones.  When doing normal tree
        parsing, it's slow and a waste of memory to create unique
        navigation nodes.  Default should be false;
        """

    raise NotImplementedError

  def toString(self, start, stop):
    """
        Return the text of all nodes from start to stop, inclusive.
        If the stream does not buffer all the nodes then it can still
        walk recursively from start until stop.  You can always return
        null or "" too, but users should not access $ruleLabel.text in
        an action of course in that case.
        """

    raise NotImplementedError


  def replaceChildren(self, parent, startChildIndex, stopChildIndex, t):
    """
        Replace from start to stop child index of parent with t, which might
        be a list.  Number of children may be different
        after this call.  The stream is notified because it is walking the
        tree and might need to know you are monkeying with the underlying
        tree.  Also, it might be able to modify the node stream to avoid
        restreaming for future phases.

        If parent is null, don't do anything; must be at root of overall tree.
        Can't replace whatever points to the parent externally.  Do nothing.
        """

    raise NotImplementedError


class CommonTreeNodeStream(TreeNodeStream):
  """@brief A buffered stream of tree nodes.

    Nodes can be from a tree of ANY kind.

    This node stream sucks all nodes out of the tree specified in
    the constructor during construction and makes pointers into
    the tree using an array of Object pointers. The stream necessarily
    includes pointers to DOWN and UP and EOF nodes.

    This stream knows how to mark/release for backtracking.

    This stream is most suitable for tree interpreters that need to
    jump around a lot or for tree parsers requiring speed (at cost of memory).
    There is some duplicated functionality here with UnBufferedTreeNodeStream
    but just in bookkeeping, not tree walking etc...

    @see UnBufferedTreeNodeStream
    """

  def __init__(self, *args):
    TreeNodeStream.__init__(self)

    if len(args) == 1:
      adaptor = CommonTreeAdaptor()
      tree = args[0]

    elif len(args) == 2:
      adaptor = args[0]
      tree = args[1]

    else:
      raise TypeError("Invalid arguments")



    self.down = adaptor.createFromType(DOWN, "DOWN")
    self.up = adaptor.createFromType(UP, "UP")
    self.eof = adaptor.createFromType(EOF, "EOF")









    self.nodes = []


    self.root = tree


    self.tokens = None


    self.adaptor = adaptor


    self.uniqueNavigationNodes = False



    self.p = -1


    self.lastMarker = None


    self.calls = []

  def fillBuffer(self):
    """Walk tree with depth-first-search and fill nodes buffer.

        Don't do DOWN, UP nodes if its a list (t is isNil).
        """

    self._fillBuffer(self.root)
    self.p = 0

  def _fillBuffer(self, t):
    nil = self.adaptor.isNil(t)

    if not nil:
      self.nodes.append(t)


    n = self.adaptor.getChildCount(t)
    if not nil and n > 0:
      self.addNavigationNode(DOWN)


    for c in range(n):
      self._fillBuffer(self.adaptor.getChild(t, c))


    if not nil and n > 0:
      self.addNavigationNode(UP)

  def getNodeIndex(self, node):
    """What is the stream index for node?

    0..n-1
        Return -1 if node not found.
        """

    if self.p == -1:
      self.fillBuffer()

    for i, t in enumerate(self.nodes):
      if t == node:
        return i

    return -1

  def addNavigationNode(self, ttype):
    """
        As we flatten the tree, we use UP, DOWN nodes to represent
        the tree structure.  When debugging we need unique nodes
        so instantiate new ones when uniqueNavigationNodes is true.
        """

    navNode = None

    if ttype == DOWN:
      if self.hasUniqueNavigationNodes():
        navNode = self.adaptor.createFromType(DOWN, "DOWN")

      else:
        navNode = self.down

    else:
      if self.hasUniqueNavigationNodes():
        navNode = self.adaptor.createFromType(UP, "UP")

      else:
        navNode = self.up

    self.nodes.append(navNode)

  def get(self, i):
    if self.p == -1:
      self.fillBuffer()

    return self.nodes[i]

  def LT(self, k):
    if self.p == -1:
      self.fillBuffer()

    if k == 0:
      return None

    if k < 0:
      return self.LB(-k)


    if self.p + k - 1 >= len(self.nodes):
      return self.eof

    return self.nodes[self.p + k - 1]

  def getCurrentSymbol(self):
    return self.LT(1)

  def LB(self, k):
    """Look backwards k nodes"""

    if k == 0:
      return None

    if self.p - k < 0:
      return None

    return self.nodes[self.p - k]

  def getTreeSource(self):
    return self.root

  def getSourceName(self):
    return self.getTokenStream().getSourceName()

  def getTokenStream(self):
    return self.tokens

  def setTokenStream(self, tokens):
    self.tokens = tokens

  def getTreeAdaptor(self):
    return self.adaptor

  def hasUniqueNavigationNodes(self):
    return self.uniqueNavigationNodes

  def setUniqueNavigationNodes(self, uniqueNavigationNodes):
    self.uniqueNavigationNodes = uniqueNavigationNodes

  def consume(self):
    if self.p == -1:
      self.fillBuffer()

    self.p += 1

  def LA(self, i):
    return self.adaptor.getType(self.LT(i))

  def mark(self):
    if self.p == -1:
      self.fillBuffer()

    self.lastMarker = self.index()
    return self.lastMarker

  def release(self, marker=None):


    pass

  def index(self):
    return self.p

  def rewind(self, marker=None):
    if marker is None:
      marker = self.lastMarker

    self.seek(marker)

  def seek(self, index):
    if self.p == -1:
      self.fillBuffer()

    self.p = index

  def push(self, index):
    """
        Make stream jump to a new location, saving old location.
        Switch back with pop().
        """

    self.calls.append(self.p)
    self.seek(index)

  def pop(self):
    """
        Seek back to previous index saved during last push() call.
        Return top of stack (return index).
        """

    ret = self.calls.pop(-1)
    self.seek(ret)
    return ret

  def reset(self):
    self.p = 0
    self.lastMarker = 0
    self.calls = []

  def size(self):
    if self.p == -1:
      self.fillBuffer()

    return len(self.nodes)



  def replaceChildren(self, parent, startChildIndex, stopChildIndex, t):
    if parent is not None:
      self.adaptor.replaceChildren(parent, startChildIndex, stopChildIndex, t)

  def __str__(self):
    """Used for testing, just return the token type stream"""

    if self.p == -1:
      self.fillBuffer()

    return " ".join([str(self.adaptor.getType(node)) for node in self.nodes])

  def toString(self, start, stop):
    if start is None or stop is None:
      return None

    if self.p == -1:
      self.fillBuffer()












    if self.tokens is not None:
      beginTokenIndex = self.adaptor.getTokenStartIndex(start)
      endTokenIndex = self.adaptor.getTokenStopIndex(stop)



      if self.adaptor.getType(stop) == UP:
        endTokenIndex = self.adaptor.getTokenStopIndex(start)

      elif self.adaptor.getType(stop) == EOF:
        endTokenIndex = self.size() - 2

      return self.tokens.toString(beginTokenIndex, endTokenIndex)


    i, t = 0, None
    for i, t in enumerate(self.nodes):
      if t == start:
        break


    buf = []
    t = self.nodes[i]
    while t != stop:
      text = self.adaptor.getText(t)
      if text is None:
        text = " " + self.adaptor.getType(t)

      buf.append(text)
      i += 1
      t = self.nodes[i]


    text = self.adaptor.getText(stop)
    if text is None:
      text = " " + self.adaptor.getType(stop)

    buf.append(text)

    return "".join(buf)


  def __iter__(self):
    if self.p == -1:
      self.fillBuffer()

    for node in self.nodes:
      yield node








class TreeParser(BaseRecognizer):
  """@brief Baseclass for generated tree parsers.

    A parser for a stream of tree nodes.  "tree grammars" result in a subclass
    of this.  All the error reporting and recovery is shared with Parser via
    the BaseRecognizer superclass.
    """

  def __init__(self, input, state=None):
    BaseRecognizer.__init__(self, state)

    self.input = None
    self.setTreeNodeStream(input)

  def reset(self):
    BaseRecognizer.reset(self)
    if self.input is not None:
      self.input.seek(0)

  def setTreeNodeStream(self, input):
    """Set the input stream"""

    self.input = input

  def getTreeNodeStream(self):
    return self.input

  def getSourceName(self):
    return self.input.getSourceName()

  def getCurrentInputSymbol(self, input):
    return input.LT(1)

  def getMissingSymbol(self, input, e, expectedTokenType, follow):
    tokenText = "<missing " + self.tokenNames[expectedTokenType] + ">"
    return CommonTree(CommonToken(type=expectedTokenType, text=tokenText))

  def matchAny(self, ignore):
    """
        Match '.' in tree parser has special meaning.  Skip node or
        entire tree if node has children.  If children, scan until
        corresponding UP node.
        """

    self._state.errorRecovery = False

    look = self.input.LT(1)
    if self.input.getTreeAdaptor().getChildCount(look) == 0:
      self.input.consume()
      return



    level = 0
    tokenType = self.input.getTreeAdaptor().getType(look)
    while tokenType != EOF and not (tokenType == UP and level == 0):
      self.input.consume()
      look = self.input.LT(1)
      tokenType = self.input.getTreeAdaptor().getType(look)
      if tokenType == DOWN:
        level += 1

      elif tokenType == UP:
        level -= 1

    self.input.consume()

  def mismatch(self, input, ttype, follow):
    """
        We have DOWN/UP nodes in the stream that have no line info; override.
        plus we want to alter the exception type. Don't try to recover
        from tree parser errors inline...
        """

    raise MismatchedTreeNodeException(ttype, input)

  def getErrorHeader(self, e):
    """
        Prefix error message with the grammar name because message is
        always intended for the programmer because the parser built
        the input tree not the user.
        """

    return (
        self.getGrammarFileName() + ": node from %sline %s:%s" %
        (["", "after "][e.approximateLineInfo], e.line, e.charPositionInLine))

  def getErrorMessage(self, e, tokenNames):
    """
        Tree parsers parse nodes they usually have a token object as
        payload. Set the exception token and do the default behavior.
        """

    if isinstance(self, TreeParser):
      adaptor = e.input.getTreeAdaptor()
      e.token = adaptor.getToken(e.node)
      if e.token is not None:
        e.token = CommonToken(
            type=adaptor.getType(e.node), text=adaptor.getText(e.node))

    return BaseRecognizer.getErrorMessage(self, e, tokenNames)

  def traceIn(self, ruleName, ruleIndex):
    BaseRecognizer.traceIn(self, ruleName, ruleIndex, self.input.LT(1))

  def traceOut(self, ruleName, ruleIndex):
    BaseRecognizer.traceOut(self, ruleName, ruleIndex, self.input.LT(1))








class RewriteRuleElementStream(object):
  """@brief Internal helper class.

    A generic list of elements tracked in an alternative to be used in
    a -> rewrite rule.  We need to subclass to fill in the next() method,
    which returns either an AST node wrapped around a token payload or
    an existing subtree.

    Once you start next()ing, do not try to add more elements.  It will
    break the cursor tracking I believe.

    @see org.antlr.runtime.tree.RewriteRuleSubtreeStream
    @see org.antlr.runtime.tree.RewriteRuleTokenStream

    TODO: add mechanism to detect/puke on modification after reading from
    stream
    """

  def __init__(self, adaptor, elementDescription, elements=None):


    self.cursor = 0


    self.singleElement = None


    self.elements = None





    self.dirty = False




    self.elementDescription = elementDescription

    self.adaptor = adaptor

    if isinstance(elements, (list, tuple)):

      self.singleElement = None
      self.elements = elements

    else:

      self.add(elements)

  def reset(self):
    """
        Reset the condition of this stream so that it appears we have
        not consumed any of its elements.  Elements themselves are untouched.
        Once we reset the stream, any future use will need duplicates.  Set
        the dirty bit.
        """

    self.cursor = 0
    self.dirty = True

  def add(self, el):
    if el is None:
      return

    if self.elements is not None:
      self.elements.append(el)
      return

    if self.singleElement is None:
      self.singleElement = el
      return


    self.elements = []
    self.elements.append(self.singleElement)
    self.singleElement = None
    self.elements.append(el)

  def nextTree(self):
    """
        Return the next element in the stream.  If out of elements, throw
        an exception unless size()==1.  If size is 1, then return elements[0].

        Return a duplicate node/subtree if stream is out of elements and
        size==1. If we've already used the element, dup (dirty bit set).
        """

    if (self.dirty or (self.cursor >= len(self) and len(self) == 1)):

      el = self._next()
      return self.dup(el)


    el = self._next()
    return el

  def _next(self):
    """
        do the work of getting the next element, making sure that it's
        a tree node or subtree.  Deal with the optimization of single-
        element list versus list of size > 1.  Throw an exception
        if the stream is empty or we're out of elements and size>1.
        protected so you can override in a subclass if necessary.
        """

    if len(self) == 0:
      raise RewriteEmptyStreamException(self.elementDescription)

    if self.cursor >= len(self):
      if len(self) == 1:
        return self.toTree(self.singleElement)


      raise RewriteCardinalityException(self.elementDescription)


    if self.singleElement is not None:
      self.cursor += 1
      return self.toTree(self.singleElement)


    o = self.toTree(self.elements[self.cursor])
    self.cursor += 1
    return o

  def dup(self, el):
    """
        When constructing trees, sometimes we need to dup a token or AST
        subtree.  Dup'ing a token means just creating another AST node
        around it.  For trees, you must call the adaptor.dupTree() unless
        the element is for a tree root; then it must be a node dup.
        """

    raise NotImplementedError

  def toTree(self, el):
    """
        Ensure stream emits trees; tokens must be converted to AST nodes.
        AST nodes can be passed through unmolested.
        """

    return el

  def hasNext(self):
    return ((self.singleElement is not None and self.cursor < 1) or
            (self.elements is not None and self.cursor < len(self.elements)))

  def size(self):
    if self.singleElement is not None:
      return 1

    if self.elements is not None:
      return len(self.elements)

    return 0

  __len__ = size

  def getDescription(self):
    """Deprecated. Directly access elementDescription attribute"""

    return self.elementDescription


class RewriteRuleTokenStream(RewriteRuleElementStream):
  """@brief Internal helper class."""

  def toTree(self, el):


    return el

  def nextNode(self):
    t = self._next()
    return self.adaptor.createWithPayload(t)

  def nextToken(self):
    return self._next()

  def dup(self, el):
    raise TypeError("dup can't be called for a token stream.")


class RewriteRuleSubtreeStream(RewriteRuleElementStream):
  """@brief Internal helper class."""

  def nextNode(self):
    """
        Treat next element as a single node even if it's a subtree.
        This is used instead of next() when the result has to be a
        tree root node.  Also prevents us from duplicating recently-added
        children; e.g., ^(type ID)+ adds ID to type and then 2nd iteration
        must dup the type node, but ID has been added.

        Referencing a rule result twice is ok; dup entire tree as
        we can't be adding trees as root; e.g., expr expr.

        Hideous code duplication here with super.next().  Can't think of
        a proper way to refactor.  This needs to always call dup node
        and super.next() doesn't know which to call: dup node or dup tree.
        """

    if (self.dirty or (self.cursor >= len(self) and len(self) == 1)):


      el = self._next()
      return self.adaptor.dupNode(el)


    el = self._next()
    return el

  def dup(self, el):
    return self.adaptor.dupTree(el)



class RewriteRuleNodeStream(RewriteRuleElementStream):
  """
    Queues up nodes matched on left side of -> in a tree parser. This is
    the analog of RewriteRuleTokenStream for normal parsers.
    """

  def nextNode(self):
    return self._next()

  def toTree(self, el):
    return self.adaptor.dupNode(el)

  def dup(self, el):


    raise TypeError("dup can't be called for a node stream.")


class TreeRuleReturnScope(RuleReturnScope):
  """
    This is identical to the ParserRuleReturnScope except that
    the start property is a tree nodes not Token object
    when you are parsing trees.  To be generic the tree node types
    have to be Object.
    """

  def __init__(self):
    self.start = None
    self.tree = None

  def getStart(self):
    return self.start

  def getTree(self):
    return self.tree
