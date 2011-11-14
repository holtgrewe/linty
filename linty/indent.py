#!/usr/bin/env python
"""The implementation of the linty indentation checks."""

from __future__ import with_statement

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@fu-berlin.de>'

import logging

import linty.checks as lc

import clang.cindex as ci


class TreeCheck(lc.Check):
    def beginTree(self, node):
        logging.debug('Starting tree %s', node.spelling)

    def endTree(self, node):
        logging.debug('Ending tree %s', node.spelling)

    def enterNode(self, node):
        logging.debug('Entering %s', node.spelling)

    def exitNode(self, node):
        logging.debug('Leaving %s', node.spelling)


class IndentSyntaxNodeHandler(object):
    def __init__(self, indentation_check, handler_name, node, parent):
        self.indentation_check = indentation_check
        self.handler_name = handler_name
        self.node = node
        self.parent = parent


class NamespaceHandler(IndentSyntaxNodeHandler):
    pass


class RootHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check, handler_name, node):
        super(RootHandler, self).__init__(indentation_check, handler_name, node, None)


def getHandler(indentation_check, node, parent):
    ck = ci.CursorKind
    HANDLERS = {
        ck.NAMESPACE: NamespaceHandler(indentation_check, 'namespace', node, parent),
        }
    return HANDLERS.get(node.kind, None)


class IndentationCheck(TreeCheck):
    def __init__(self, indent_width=4, tab_width=None):
        super(IndentationCheck, self).__init__()
        self.indent_width = indent_width
        self.tab_width = tab_width or indent_width
        self.brace_adjustment = indent_width
        self.case_indent = indent_width
        self.handlers = []
        self.level = 0

    def beginTree(self, node):
        assert len(self.handlers) == 0
        self.handlers = [RootHandler(self, 'root', node)]

    def endTree(self, node):
        assert len(self.handlers) == 1
        self.handlers = []

    def enterNode(self, node):
        logging.info('%sNode: %s %s (%s)', ' ' * self.level, node.kind, node.spelling, node.location)
        handler = getHandler(self, node, self.handlers[-1])
        self.handlers.append(handler)
        self.level += 1

    def exitNode(self, node):
        self.level -= 1
        self.handlers.pop()
