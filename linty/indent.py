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


class IndentLevel(object):
    def __init__(self, indent=None, base=None, offset=None):
        assert indent or base or offset
        self.levels = set()
        if indent:
            self.levels.add(indent)
        else:
            assert base and offset
            for l in base.indent_levels:
                levels.add(l + offset)
    
    def isMultilevel(self):
        return len(levels) > 1

    def accept(self, indent):
        return indent in levels

    def gt(self, indent):
        return sorted(self.levels)[-1] > indent

    def addAcceptedIndent(self, level):
        if type(level) is IndentLevel:
            for i in level.levels:
                self.levels.add(i)
        else:
            self.levels.add(level)

    def __str__(self):
        return '(%s)' % (', '.join(list(self.levels)))


class IndentSyntaxNodeHandler(object):
    def __init__(self, indentation_check, handler_name, node, parent):
        self.indentation_check = indentation_check
        self.handler_name = handler_name
        self.node = node
        self.parent = parent
        self.level = None

    def getLevel(self):
        if not self.level:
            self.level = self.getLevelImpl()
        return self.level

    def getLvelImpl(self):
        return self.parent.suggestedChildLevel(self)

    def suggestedChildLevel(self, indent_syntax_node_handler):
        return None  # IndentLevel(self.getLevel(), self.getBasicOffset())

    def logError(self, ast_node, subtype_name, actualLevel):
        pass  # Log an error

    def logChildError(self, line, actual_level, expected_level):
        pass  # Log a child indentation error.

    def startsLine(self, node):
        return self.getLineStart(node) == self.expanddTabsColumnNo(node)

    def areOnSameLine(self, node1, node2):
        return node1 and node2 and node1.location.line == node2.location.line

    def getFirstToken(self, node):
        pass

    def getLineStart(self, node):
        pass

    def checkLinesIndent(self, start_line, end_line, indent_level):
        pass

    def shouldIncreaseIndent(self):
        return True

    def checkLinesIndent(self, lines_set, indent_level, first_line_match, first_line):
        pass

    def checkSingleLine(self, line_num, indent_level, col_num=None, must_match=None):
        pass

    def getLineStart(self, line):
        pass

    def checkChildren(self, parent, token_types, start_level, first_line_matches, allow_nesting):
        pass

    def checkExpressionSubtree(self, tree, level, first_line_matches, allow_nesting):
        pass

    def getFirstLine(self, start_line, node):
        pass

    def expandedTabsColumnNo(self, node):
        pass

    def finalSubtreeLines(self, lines, ast_tree, allow_nesting):
        pass
    
    def checkModifiers(self):
        pass

    def checkIndentation(self):
        raise Exception('Abstract method!')

    def getBasicOffset(self):
        return self.indent_check.basic_offset

    def getBraceAdjustment(self):
        return self.indent_check.brace_adjustment

    def checkRParent(self, left_paren, right_paren):
        pass

    def checkLParen(self, left_paren):
        pass


class BlockParenHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(BlockParenHandler, self).__init__(indentation_check, handler_name, node, parent)
        self.token_set = None

    def getLParen(self):
        token_set = self._getTokenSet()

    def getRParen(self):
        pass

    def checkLParen(self, lparen):
        pass

    def checkRParen(self, lparen, rparen):
        pass

    def _getTokenSet(self):
        if self.token_set:
            return self.token_set
        extent = self.node.extent
        translation_unit = self.node.translation_unit
        self.token_set = ci.tokenize(translation_unit, extent)
        for t in self.token_set.tokens:
            print t.kind
            #import pdb; pdb.set_trace()
            print ' ', t.spelling
        
    def checkIndentation(self):
        # Check left and right parenthesis.
        self.checkLParen(self.getLParen())
        self.checkRParen(self.getLParen(), self.getRParen())


class NamespaceHandler(BlockParenHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(NamespaceHandler, self).__init__(indentation_check, handler_name, node, parent)

    def checkIndentation(self):
        # Check that the line with the namespace name starts at the correct
        # indentation.

        # Call the generic block handler.
        super(NamespaceHandler, self).checkIndentation()


class RootHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check):
        super(RootHandler, self).__init__(indentation_check, None, None, None)
    
    def checkIndentation(self):
        pass  # Nothing to check.

    def suggestedChildLevel(self, child):
        return IndentLevel(level=0)

    def getLevelImpl(self):
        return IndentLevel(level=0)


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
        logging.debug('IndentationCheck: BEGIN TREE(%s)', node)
        assert len(self.handlers) == 0
        self.handlers = [RootHandler(self)]

    def endTree(self, node):
        logging.debug('IndentationCheck: END TREE(%s)', node)
        assert len(self.handlers) == 1
        self.handlers = []

    def enterNode(self, node):
        logging.info('%sNode: %s %s (%s)', ' ' * self.level, node.kind, node.spelling, node.location)
        handler = getHandler(self, node, self.handlers[-1])
        self.handlers.append(handler)
        if handler:
            handler.checkIndentation()
        self.level += 1

    def exitNode(self, node):
        self.level -= 1
        self.handlers.pop()
