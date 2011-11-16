#!/usr/bin/env python
"""The implementation of the linty indentation checks."""

from __future__ import with_statement

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@fu-berlin.de>'

import logging
import sys

import linty.violations as lv
import linty.checks as lc

import clang.cindex as ci

def lengthExpandedTabs(s, to_idx, tab_width):
    l = 0
    for i in range(0, to_idx):
        if s[i] == '\t':
            l += (l / tab_width + 1)  * tab_width
        else:
            l += 1
    return l


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
        assert (indent is not None) or (base is not None) or (offset is not None)
        self.levels = set()
        if indent is not None:
            self.levels.add(indent)
        else:
            assert (base is not None) and (offset is not None)
            for l in base.indent_levels:
                levels.add(l + offset)
    
    def isMultilevel(self):
        return len(levels) > 1

    def accept(self, indent):
        ##print 'accept(), level=', self.levels, 'indent=', indent
        return indent in self.levels

    def gt(self, indent):
        return sorted(self.levels)[-1] > indent

    def addAcceptedIndent(self, level):
        if type(level) is IndentLevel:
            for i in level.levels:
                self.levels.add(i)
        else:
            self.levels.add(level)

    def __str__(self):
        return '(%s)' % (', '.join(map(str, list(self.levels))))


class IndentSyntaxNodeHandler(object):
    def __init__(self, indentation_check, handler_name, node, parent):
        self.indentation_check = indentation_check
        self.handler_name = handler_name
        self.node = node
        self.parent = parent
        self.level = self._getLevelImpl()
        self.violations = indentation_check.violations

    def _getLevelImpl(self):
        res = self.parent.suggestedChildLevel(self)
        ##print '_getLevelImpl()', self, self.parent, res
        return res

    def suggestedChildLevel(self, indent_syntax_node_handler):
        return self.level

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

    def expandedTabsColumnNo(self, node):
        npath, contents, lines = self.indentation_check.file_reader.readFile(node.location.file.name)
        line = lines[node.location.line - 1]
        return lengthExpandedTabs(line, node.location.column - 1, self.indentation_check.config.tab_width)
        ##print >>sys.stderr, 'LINE:', line


class BlockParenHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(BlockParenHandler, self).__init__(indentation_check, handler_name, node, parent)
        self._token_set = None

    def checkLParen(self, node, left_brace_sameline=None):
        ##print 'checkLParen(self,', left_paren, ',', left_brace_sameline, ')'
        if left_brace_sameline is None:
            left_brace_sameline = self.indentation_check.config.brace_sameline
        if node is None:
            return  # No parenthesis, no error.
        ##print self, self.level
        if self.node.location.line == node.location.line:
            if not left_brace_sameline:
                self.violations.add(lv.RuleViolation('indentation.brace', node.location.file.name,
                                                     node.location.line, node.location.column,
                                                     'Left brace not allowed on same line as definition.'))
                return  # Return after logging error.
            else:
                return  # OK, is allowed, everything's swell.
        else:
            if left_brace_sameline:
                self.violations.add(lv.RuleViolation('indentation.brace', node.location.file.name,
                                                     node.location.line, node.location.column,
                                                     'Left brace must be on same line as definition.'))
                return  # Return after logging error.
            else:
                if self.level.accept(self.expandedTabsColumnNo(left_paren)):
                    return  # Parenthesis on correct column.
        self.violations.add(lv.RuleViolation('indentation.brace', node.location.file.name,
                                             node.location.line, node.location.column,
                                             'Invalid column for left brace.'))

    def checkRParen(self, node_left, node_right):
        if node_right is None:
            assert node_right is None
            return  # No parenthsis, no error.
        if not self.level.accept(self.expandedTabsColumnNo(node_right)):
            self.violations.add(lv.RuleViolation('indentation.brace', node_right.location.file.name,
                                                 node_right.location.line, node_right.location.column,
                                                 'Invalid column for right brace.'))

    def getLParen(self):
        tk = ci.TokenKind
        token_set = self._getTokenSet()
        for t in token_set:
            if t.kind == tk.PUNCTUATION or t.spelling == '{':
                return t
        return None

    def getRParen(self):
        tk = ci.TokenKind
        token_set = self._getTokenSet()
        for t in reversed(token_set):
            if t.kind == tk.PUNCTUATION or t.spelling == '}':
                return t
        return None

    def _getTokenSet(self):
        if self._token_set:
            return self._token_set
        extent = self.node.extent
        translation_unit = self.node.translation_unit
        self._token_set = ci.tokenize(translation_unit, extent)
        return self._token_set
        
    def checkIndentation(self):
        # Check left and right parenthesis.
        self.checkLParen(self.getLParen())
        self.checkRParen(self.getLParen(), self.getRParen())


class RootHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check):
        super(RootHandler, self).__init__(indentation_check, None, None, None)
    
    def checkIndentation(self):
        pass  # Nothing to check.

    def suggestedChildLevel(self, child):
        return IndentLevel(indent=0)

    def _getLevelImpl(self):
        return IndentLevel(indent=0)


class TranslationUnitHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(type(self), self).__init__(indentation_check, handler_name, node, parent)

    def checkIndentation(self):
        pass


class NamespaceHandler(BlockParenHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(type(self), self).__init__(indentation_check, handler_name, node, parent)

    def checkLParen(self, left_paren):
        return super(type(self), self).checkLParen(left_paren, self.indentation_check.config.brace_sameline_namespace)

    def checkIndentation(self):
        # Check that the line with the namespace name starts at the correct
        # indentation.

        # Call the generic block handler.
        super(NamespaceHandler, self).checkIndentation()


class FunctionDeclHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(type(self), self).__init__(indentation_check, handler_name, node, parent)

    def checkIndentation(self):
        pass


class CompoundStmtHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(type(self), self).__init__(indentation_check, handler_name, node, parent)

    def checkIndentation(self):
        pass


class ReturnStmtHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(type(self), self).__init__(indentation_check, handler_name, node, parent)

    def checkIndentation(self):
        pass


def getHandler(indentation_check, node, parent):
    ##print 'getHandler()', indentation_check, node, parent
    ck = ci.CursorKind
    HANDLERS = {
        ck.TRANSLATION_UNIT: TranslationUnitHandler(indentation_check, 'namespace', node, parent),
        ck.COMPOUND_STMT: CompoundStmtHandler(indentation_check, 'compound stmt', node, parent),
        ck.RETURN_STMT: ReturnStmtHandler(indentation_check, 'compound stmt', node, parent),
        ck.NAMESPACE: NamespaceHandler(indentation_check, 'namespace', node, parent),
        ck.FUNCTION_DECL: FunctionDeclHandler(indentation_check, 'function_decl', node, parent),
        }
    res = HANDLERS.get(node.kind, None)
    ##print ' -->', res
    return res


class IndentationConfig(object):
    def __init__(self, indent_width=4, tab_width=4, brace_adjustment=None,
                 case_indent=None, brace_sameline=False, brace_sameline_class=None,
                 brace_sameline_fun=None, brace_sameline_infun=None, brace_sameline_namespace=None):
        self.indent_width = indent_width
        self.tab_width = tab_width
        self.brace_adjustment = brace_adjustment or indent_width
        self.case_indent = case_indent or indent_width
        self.brace_sameline = brace_sameline
        if brace_sameline_class is None:
            self.brace_sameline_class = brace_sameline
        else:
            self.brace_sameline_class = brace_sameline_class
        if brace_sameline_fun is None:
            self.brace_sameline_fun = brace_sameline
        else:
            self.brace_sameline_fun = brace_sameline_fun
        if brace_sameline_infun is None:
            self.brace_sameline_infun = brace_sameline
        else:
            self.brace_sameline_infun = brace_sameline_infun
        if brace_sameline_namespace is None:
            self.brace_sameline_namespace = brace_sameline
        else:
            self.brace_sameline_namespace = brace_sameline_namespace


class IndentationCheck(TreeCheck):
    def __init__(self, config=IndentationConfig()):
        super(IndentationCheck, self).__init__()
        self.config = config
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
