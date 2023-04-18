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
"""ANTLR3 runtime package"""
































from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import optparse
import sys

import google.appengine._internal.antlr3
from six.moves import input


class _Main(object):

  def __init__(self):
    self.stdin = sys.stdin
    self.stdout = sys.stdout
    self.stderr = sys.stderr

  def parseOptions(self, argv):
    optParser = optparse.OptionParser()
    optParser.add_option(
        "--encoding", action="store", type="string", dest="encoding")
    optParser.add_option("--input", action="store", type="string", dest="input")
    optParser.add_option(
        "--interactive", "-i", action="store_true", dest="interactive")
    optParser.add_option("--no-output", action="store_true", dest="no_output")
    optParser.add_option("--profile", action="store_true", dest="profile")
    optParser.add_option("--hotshot", action="store_true", dest="hotshot")

    self.setupOptions(optParser)

    return optParser.parse_args(argv[1:])

  def setupOptions(self, optParser):
    pass

  def execute(self, argv):
    options, args = self.parseOptions(argv)

    self.setUp(options)

    if options.interactive:
      while True:
        try:
          input = input(">>> ")
        except (EOFError, KeyboardInterrupt):
          self.stdout.write("\nBye.\n")
          break

        inStream = google.appengine._internal.antlr3.ANTLRStringStream(input)
        self.parseStream(options, inStream)

    else:
      if options.input is not None:
        inStream = google.appengine._internal.antlr3.ANTLRStringStream(options.input)

      elif len(args) == 1 and args[0] != "-":
        inStream = google.appengine._internal.antlr3.ANTLRFileStream(args[0], encoding=options.encoding)

      else:
        inStream = google.appengine._internal.antlr3.ANTLRInputStream(
            self.stdin, encoding=options.encoding)

      if options.profile:
        try:
          import cProfile as profile
        except ImportError:
          import profile

        profile.runctx("self.parseStream(options, inStream)", globals(),
                       locals(), "profile.dat")

        import pstats
        stats = pstats.Stats("profile.dat")
        stats.strip_dirs()
        stats.sort_stats("time")
        stats.print_stats(100)

      elif options.hotshot:
        import hotshot

        profiler = hotshot.Profile("hotshot.dat")
        profiler.runctx("self.parseStream(options, inStream)", globals(),
                        locals())

      else:
        self.parseStream(options, inStream)

  def setUp(self, options):
    pass

  def parseStream(self, options, inStream):
    raise NotImplementedError

  def write(self, options, text):
    if not options.no_output:
      self.stdout.write(text)

  def writeln(self, options, text):
    self.write(options, text + "\n")


class LexerMain(_Main):

  def __init__(self, lexerClass):
    _Main.__init__(self)

    self.lexerClass = lexerClass

  def parseStream(self, options, inStream):
    lexer = self.lexerClass(inStream)
    for token in lexer:
      self.writeln(options, str(token))


class ParserMain(_Main):

  def __init__(self, lexerClassName, parserClass):
    _Main.__init__(self)

    self.lexerClassName = lexerClassName
    self.lexerClass = None
    self.parserClass = parserClass

  def setupOptions(self, optParser):
    optParser.add_option(
        "--lexer",
        action="store",
        type="string",
        dest="lexerClass",
        default=self.lexerClassName)
    optParser.add_option(
        "--rule", action="store", type="string", dest="parserRule")

  def setUp(self, options):
    lexerMod = __import__(options.lexerClass)
    self.lexerClass = getattr(lexerMod, options.lexerClass)

  def parseStream(self, options, inStream):
    lexer = self.lexerClass(inStream)
    tokenStream = google.appengine._internal.antlr3.CommonTokenStream(lexer)
    parser = self.parserClass(tokenStream)
    result = getattr(parser, options.parserRule)()
    if result is not None:
      if hasattr(result, "tree"):
        if result.tree is not None:
          self.writeln(options, result.tree.toStringTree())
      else:
        self.writeln(options, repr(result))


class WalkerMain(_Main):

  def __init__(self, walkerClass):
    _Main.__init__(self)

    self.lexerClass = None
    self.parserClass = None
    self.walkerClass = walkerClass

  def setupOptions(self, optParser):
    optParser.add_option(
        "--lexer",
        action="store",
        type="string",
        dest="lexerClass",
        default=None)
    optParser.add_option(
        "--parser",
        action="store",
        type="string",
        dest="parserClass",
        default=None)
    optParser.add_option(
        "--parser-rule",
        action="store",
        type="string",
        dest="parserRule",
        default=None)
    optParser.add_option(
        "--rule", action="store", type="string", dest="walkerRule")

  def setUp(self, options):
    lexerMod = __import__(options.lexerClass)
    self.lexerClass = getattr(lexerMod, options.lexerClass)
    parserMod = __import__(options.parserClass)
    self.parserClass = getattr(parserMod, options.parserClass)

  def parseStream(self, options, inStream):
    lexer = self.lexerClass(inStream)
    tokenStream = google.appengine._internal.antlr3.CommonTokenStream(lexer)
    parser = self.parserClass(tokenStream)
    result = getattr(parser, options.parserRule)()
    if result is not None:
      assert hasattr(result, "tree"), "Parser did not return an AST"
      nodeStream = google.appengine._internal.antlr3.tree.CommonTreeNodeStream(result.tree)
      nodeStream.setTokenStream(tokenStream)
      walker = self.walkerClass(nodeStream)
      result = getattr(walker, options.walkerRule)()
      if result is not None:
        if hasattr(result, "tree"):
          self.writeln(options, result.tree.toStringTree())
        else:
          self.writeln(options, repr(result))
