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

"""Contains some functions that come in handy with XML parsing."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals


def GetTag(node):
  """Strips namespace prefix."""
  return node.tag.rsplit('}', 1)[-1]


def GetChild(node, tag):
  """Returns first child of node with tag."""
  for child in node:
    if GetTag(child) == tag:
      return child


def BooleanValue(node_text):
  """Returns boolean value."""
  return node_text.lower() in ('1', 'true')


def GetAttribute(node, attr):
  """Wrapper function to retrieve attributes from XML nodes."""
  return node.attrib.get(attr, '')


def GetChildNodeText(node, child_tag, default=''):
  """Finds child XML node with desired tag and returns its text."""
  for child in node:
    if GetTag(child) == child_tag:
      return GetNodeText(child) or default
  return default


def GetNodeText(node):
  """Returns the node text after stripping whitespace."""

  return node.text.strip() if node.text else ''


def GetNodes(node, match_tag):
  """Gets all children of a node with the desired tag."""
  return (child for child in node if GetTag(child) == match_tag)
