#!/usr/bin/env python
"""The implementation of the linty indentation checks."""

from __future__ import with_statement

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@fu-berlin.de>'

import logging

import linty.checks as lc


class IndentationCheck(lc.Check):
    def __init__(self, indent_width=4, tab_width=None):
        self.indent_width = indent_width
        self.tab_width = tab_width or indent_width
        self.brace_adjustment = indent_width
        self.case_indent = indent_width
        self.violations = set()

    def enterNode(self, node):
        logging.debug('Entering %s', node.spelling)

    def exitNode(self, node):
        logging.debug('Leaving %s', node.spelling)

