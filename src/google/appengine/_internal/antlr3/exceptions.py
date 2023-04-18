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
"""ANTLR3 exception hierarchy"""































from google.appengine._internal.antlr3.constants import INVALID_TOKEN_TYPE


class BacktrackingFailed(Exception):
  """@brief Raised to signal failed backtrack attempt"""

  pass


class RecognitionException(Exception):
  """@brief The root of the ANTLR exception hierarchy.

    To avoid English-only error messages and to generally make things
    as flexible as possible, these exceptions are not created with strings,
    but rather the information necessary to generate an error.  Then
    the various reporting methods in Parser and Lexer can be overridden
    to generate a localized error message.  For example, MismatchedToken
    exceptions are built with the expected token type.
    So, don't expect getMessage() to return anything.

    Note that as of Java 1.4, you can access the stack trace, which means
    that you can compute the complete trace of rules from the start symbol.
    This gives you considerable context information with which to generate
    useful error messages.

    ANTLR generates code that throws exceptions upon recognition error and
    also generates code to catch these exceptions in each rule.  If you
    want to quit upon first error, you can turn off the automatic error
    handling mechanism using rulecatch action, but you still need to
    override methods mismatch and recoverFromMismatchSet.

    In general, the recognition exceptions can track where in a grammar a
    problem occurred and/or what was the expected input.  While the parser
    knows its state (such as current input symbol and line info) that
    state can change before the exception is reported so current token index
    is computed and stored at exception time.  From this info, you can
    perhaps print an entire line of input not just a single token, for example.
    Better to just say the recognizer had a problem and then let the parser
    figure out a fancy report.

    """

  def __init__(self, input=None):
    Exception.__init__(self)


    self.input = None



    self.index = None




    self.token = None



    self.node = None


    self.c = None




    self.line = None

    self.charPositionInLine = None





    self.approximateLineInfo = False

    if input is not None:
      self.input = input
      self.index = input.index()


      from google.appengine._internal.antlr3.streams import TokenStream, CharStream
      from google.appengine._internal.antlr3.tree import TreeNodeStream

      if isinstance(self.input, TokenStream):
        self.token = self.input.LT(1)
        self.line = self.token.line
        self.charPositionInLine = self.token.charPositionInLine

      if isinstance(self.input, TreeNodeStream):
        self.extractInformationFromTreeNodeStream(self.input)

      else:
        if isinstance(self.input, CharStream):
          self.c = self.input.LT(1)
          self.line = self.input.line
          self.charPositionInLine = self.input.charPositionInLine

        else:
          self.c = self.input.LA(1)

  def extractInformationFromTreeNodeStream(self, nodes):
    from google.appengine._internal.antlr3.tree import Tree, CommonTree
    from google.appengine._internal.antlr3.tokens import CommonToken

    self.node = nodes.LT(1)
    adaptor = nodes.adaptor
    payload = adaptor.getToken(self.node)
    if payload is not None:
      self.token = payload
      if payload.line <= 0:

        i = -1
        priorNode = nodes.LT(i)
        while priorNode is not None:
          priorPayload = adaptor.getToken(priorNode)
          if priorPayload is not None and priorPayload.line > 0:

            self.line = priorPayload.line
            self.charPositionInLine = priorPayload.charPositionInLine
            self.approximateLineInfo = True
            break

          i -= 1
          priorNode = nodes.LT(i)

      else:
        self.line = payload.line
        self.charPositionInLine = payload.charPositionInLine

    elif isinstance(self.node, Tree):
      self.line = self.node.line
      self.charPositionInLine = self.node.charPositionInLine
      if isinstance(self.node, CommonTree):
        self.token = self.node.token

    else:
      type = adaptor.getType(self.node)
      text = adaptor.getText(self.node)
      self.token = CommonToken(type=type, text=text)

  def getUnexpectedType(self):
    """Return the token type or char of the unexpected input element"""

    from google.appengine._internal.antlr3.streams import TokenStream
    from google.appengine._internal.antlr3.tree import TreeNodeStream

    if isinstance(self.input, TokenStream):
      return self.token.type

    elif isinstance(self.input, TreeNodeStream):
      adaptor = self.input.treeAdaptor
      return adaptor.getType(self.node)

    else:
      return self.c

  unexpectedType = property(getUnexpectedType)


class MismatchedTokenException(RecognitionException):
  """@brief A mismatched char or Token or tree node."""

  def __init__(self, expecting, input):
    RecognitionException.__init__(self, input)
    self.expecting = expecting

  def __str__(self):

    return "MismatchedTokenException(%r!=%r)" % (self.getUnexpectedType(),
                                                 self.expecting)

  __repr__ = __str__


class UnwantedTokenException(MismatchedTokenException):
  """An extra token while parsing a TokenStream"""

  def getUnexpectedToken(self):
    return self.token

  def __str__(self):
    exp = ", expected %s" % self.expecting
    if self.expecting == INVALID_TOKEN_TYPE:
      exp = ""

    if self.token is None:
      return "UnwantedTokenException(found=%s%s)" % (None, exp)

    return "UnwantedTokenException(found=%s%s)" % (self.token.text, exp)

  __repr__ = __str__


class MissingTokenException(MismatchedTokenException):
  """
    We were expecting a token but it's not found.  The current token
    is actually what we wanted next.
    """

  def __init__(self, expecting, input, inserted):
    MismatchedTokenException.__init__(self, expecting, input)

    self.inserted = inserted

  def getMissingType(self):
    return self.expecting

  def __str__(self):
    if self.inserted is not None and self.token is not None:
      return "MissingTokenException(inserted %r at %r)" % (self.inserted,
                                                           self.token.text)

    if self.token is not None:
      return "MissingTokenException(at %r)" % self.token.text

    return "MissingTokenException"

  __repr__ = __str__


class MismatchedRangeException(RecognitionException):
  """@brief The next token does not match a range of expected types."""

  def __init__(self, a, b, input):
    RecognitionException.__init__(self, input)

    self.a = a
    self.b = b

  def __str__(self):
    return "MismatchedRangeException(%r not in [%r..%r])" % (
        self.getUnexpectedType(), self.a, self.b)

  __repr__ = __str__


class MismatchedSetException(RecognitionException):
  """@brief The next token does not match a set of expected types."""

  def __init__(self, expecting, input):
    RecognitionException.__init__(self, input)

    self.expecting = expecting

  def __str__(self):
    return "MismatchedSetException(%r not in %r)" % (self.getUnexpectedType(),
                                                     self.expecting)

  __repr__ = __str__


class MismatchedNotSetException(MismatchedSetException):
  """@brief Used for remote debugger deserialization"""

  def __str__(self):
    return "MismatchedNotSetException(%r!=%r)" % (self.getUnexpectedType(),
                                                  self.expecting)

  __repr__ = __str__


class NoViableAltException(RecognitionException):
  """@brief Unable to decide which alternative to choose."""

  def __init__(self, grammarDecisionDescription, decisionNumber, stateNumber,
               input):
    RecognitionException.__init__(self, input)

    self.grammarDecisionDescription = grammarDecisionDescription
    self.decisionNumber = decisionNumber
    self.stateNumber = stateNumber

  def __str__(self):
    return "NoViableAltException(%r!=[%r])" % (self.unexpectedType,
                                               self.grammarDecisionDescription)

  __repr__ = __str__


class EarlyExitException(RecognitionException):
  """@brief The recognizer did not match anything for a (..)+ loop."""

  def __init__(self, decisionNumber, input):
    RecognitionException.__init__(self, input)

    self.decisionNumber = decisionNumber


class FailedPredicateException(RecognitionException):
  """@brief A semantic predicate failed during validation.

    Validation of predicates
    occurs when normally parsing the alternative just like matching a token.
    Disambiguating predicate evaluation occurs when we hoist a predicate into
    a prediction decision.
    """

  def __init__(self, input, ruleName, predicateText):
    RecognitionException.__init__(self, input)

    self.ruleName = ruleName
    self.predicateText = predicateText

  def __str__(self):
    return "FailedPredicateException(" + self.ruleName + ",{" + self.predicateText + "}?)"

  __repr__ = __str__


class MismatchedTreeNodeException(RecognitionException):
  """@brief The next tree mode does not match the expected type."""

  def __init__(self, expecting, input):
    RecognitionException.__init__(self, input)

    self.expecting = expecting

  def __str__(self):
    return "MismatchedTreeNodeException(%r!=%r)" % (self.getUnexpectedType(),
                                                    self.expecting)

  __repr__ = __str__
