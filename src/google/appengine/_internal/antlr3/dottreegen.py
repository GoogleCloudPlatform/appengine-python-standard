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
""" @package google.appengine._internal.antlr3.dottreegenerator
@brief ANTLR3 runtime package, tree module

This module contains all support classes for AST construction and tree parsers.

"""


































from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from google.appengine._internal.antlr3.tree import CommonTreeAdaptor
from six.moves import range
import stringtemplate3

class DOTTreeGenerator(object):
  """
    A utility class to generate DOT diagrams (graphviz) from
    arbitrary trees.  You can pass in your own templates and
    can pass in any kind of tree or use Tree interface method.
    """

  _treeST = stringtemplate3.StringTemplate(
      template=(
          "digraph {\n" + "  ordering=out;\n" + "  ranksep=.4;\n" +
          "  node [shape=plaintext, fixedsize=true, fontsize=11, fontname=\"Courier\",\n"
          + "        width=.25, height=.25];\n" + "  edge [arrowsize=.5]\n" +
          "  $nodes$\n" + "  $edges$\n" + "}\n"))

  _nodeST = stringtemplate3.StringTemplate(
      template="$name$ [label=\"$text$\"];\n")

  _edgeST = stringtemplate3.StringTemplate(
      template="$parent$ -> $child$ // \"$parentText$\" -> \"$childText$\"\n")

  def __init__(self):

    self.nodeToNumberMap = {}


    self.nodeNumber = 0

  def toDOT(self, tree, adaptor=None, treeST=_treeST, edgeST=_edgeST):
    if adaptor is None:
      adaptor = CommonTreeAdaptor()

    treeST = treeST.getInstanceOf()

    self.nodeNumber = 0
    self.toDOTDefineNodes(tree, adaptor, treeST)

    self.nodeNumber = 0
    self.toDOTDefineEdges(tree, adaptor, treeST, edgeST)
    return treeST

  def toDOTDefineNodes(self, tree, adaptor, treeST, knownNodes=None):
    if knownNodes is None:
      knownNodes = set()

    if tree is None:
      return

    n = adaptor.getChildCount(tree)
    if n == 0:


      return


    number = self.getNodeNumber(tree)
    if number not in knownNodes:
      parentNodeST = self.getNodeST(adaptor, tree)
      treeST.setAttribute("nodes", parentNodeST)
      knownNodes.add(number)


    for i in range(n):
      child = adaptor.getChild(tree, i)

      number = self.getNodeNumber(child)
      if number not in knownNodes:
        nodeST = self.getNodeST(adaptor, child)
        treeST.setAttribute("nodes", nodeST)
        knownNodes.add(number)

      self.toDOTDefineNodes(child, adaptor, treeST, knownNodes)

  def toDOTDefineEdges(self, tree, adaptor, treeST, edgeST):
    if tree is None:
      return

    n = adaptor.getChildCount(tree)
    if n == 0:


      return

    parentName = "n%d" % self.getNodeNumber(tree)


    parentText = adaptor.getText(tree)
    for i in range(n):
      child = adaptor.getChild(tree, i)
      childText = adaptor.getText(child)
      childName = "n%d" % self.getNodeNumber(child)
      edgeST = edgeST.getInstanceOf()
      edgeST.setAttribute("parent", parentName)
      edgeST.setAttribute("child", childName)
      edgeST.setAttribute("parentText", parentText)
      edgeST.setAttribute("childText", childText)
      treeST.setAttribute("edges", edgeST)
      self.toDOTDefineEdges(child, adaptor, treeST, edgeST)

  def getNodeST(self, adaptor, t):
    text = adaptor.getText(t)
    nodeST = self._nodeST.getInstanceOf()
    uniqueName = "n%d" % self.getNodeNumber(t)
    nodeST.setAttribute("name", uniqueName)
    if text is not None:
      text = text.replace('"', r'\\"')
    nodeST.setAttribute("text", text)
    return nodeST

  def getNodeNumber(self, t):
    try:
      return self.nodeToNumberMap[t]
    except KeyError:
      self.nodeToNumberMap[t] = self.nodeNumber
      self.nodeNumber += 1
      return self.nodeNumber - 1


def toDOT(tree, adaptor=None, treeST=DOTTreeGenerator._treeST, edgeST=DOTTreeGenerator._edgeST):
  """
    Generate DOT (graphviz) for a whole tree not just a node.
    For example, 3+4*5 should generate:

    digraph {
        node [shape=plaintext, fixedsize=true, fontsize=11, fontname="Courier",
            width=.4, height=.2];
        edge [arrowsize=.7]
        "+"->3
        "+"->"*"
        "*"->4
        "*"->5
    }

    Return the ST not a string in case people want to alter.

    Takes a Tree interface object.

    Example of invokation:

        import google.appengine._internal.antlr3
        import google.appengine._internal.antlr3.extras

        input = google.appengine._internal.antlr3.ANTLRInputStream(sys.stdin)
        lex = TLexer(input)
        tokens = google.appengine._internal.antlr3.CommonTokenStream(lex)
        parser = TParser(tokens)
        tree = parser.e().tree
        print tree.toStringTree()
        st = google.appengine._internal.antlr3.extras.toDOT(t)
        print st

    """

  gen = DOTTreeGenerator()
  return gen.toDOT(tree, adaptor, treeST, edgeST)
