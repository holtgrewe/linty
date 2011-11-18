#!/usr/bin/env python

# TODO(holtgrew): Maybe spacing would be more appropriate.

import logging
import sys

import linty.violations as lv
import linty.checks as lc

import clang.cindex as ci

class WhitespaceConfig(object):
    pass


class WhitespaceNodeHandler(lv.LogViolationsMixin):
    def __init__(self, whitespace_check, handler_name, node, parent):
        self.whitespace_check = whitespace_check
        self.handler_name = handler_name
        self.node = node
        self.parent = parent
        self.violations = whitespace_check.violations
        self._token_set = None

    def _getTokenSet(self):
        if self._token_set:
            return self._token_set
        extent = self.node.extent
        translation_unit = self.node.translation_unit
        self._token_set = ci.tokenize(translation_unit, extent)
        return self._token_set
        
    def checkWhitespace(self):
        raise Exception('Abstract method!')


class NullHandler(WhitespaceNodeHandler):
    def checkWhitespace(self):
        pass  # Do nothing.


class RootHandler(WhitespaceNodeHandler):
    def __init__(self, whitespace_check):
        super(type(self), self).__init__(whitespace_check, None, None, None)

    def checkWhitespace(self):
        pass  # Do nothing.


class NamespaceHandler(WhitespaceNodeHandler):
    def checkWhitespace(self):
        tokens = self._getTokenSet()
        tk = ci.TokenKind
        # --------------------------------------------------------------------
        # Get tokens and log violation on errors.
        # --------------------------------------------------------------------
        # Get parenthesis tokens.
        lparen = self.getLParen()
        if not lparen:
            self.logViolation('spacing.namespace', tokens[0],
                              'Could not find opening brace for namespace.')
            return
        rparen = self.getRParen()
        if not rparen:
            self.logViolation('spacing.namespace', tokens[-1],
                              'Could not find closing brace for namespace.')
            return
        # Get namespace keyword token.
        keyword = tokens[0]
        if keyword.kind != tk.KEYWORD or keyword.spelling != 'namespace':
            self.logViolation('spacing.namespace', tokens[-1],
                              'First token for namespace construct must be keyword "namespace".')
            return
        identifier = tokens[1]
        if identifier.kind != tk.IDENTIFIER:
            self.logViolation('spacing.namespace', tokens[0],
                              'Second token for namespace construct must be identifier.')
            return
        if tokens[2] != lparen:
            self.logViolation('spacing.namespace', tokens[0],
                              'Third token for namespace must be opening brace.')
            return
        if tokens[-2] != rparen:
            self.logViolation('spacing.namespace', tokens[0],
                              'Second last token for namespace must be right brace.')
            return
        comment = tokens[-1]
        if comment.kind != tk.COMMENT:
            self.logViolation('spacing.namespace', tokens[-1],
                              'Last token for namespace must be "// namespace <namespace id>" comment.')
            return
        # --------------------------------------------------------------------
        # Check rules for the namespace construct
        # --------------------------------------------------------------------
        # Exactly one space between namespace and identifier.
        if keyword.extent.end.line != identifier.extent.end.line:  # On the same line.
            self.logViolation('spacing.namespace', tokens[0],
                              'Keyword "namespace" must be on same line as identifier.')
            return
        if keyword.extent.end.column + 1 != identifier.extent.start.column:  # One space.
            self.logViolation('spacing.namespace', tokens[0],
                              'There must be exactly on space between keyword "namespace" and identifier.')
            return
        # Exactly one space between identifier and opening bracket.
        if identifier.extent.end.column + 1 != lparen.extent.start.column:  # One space.
            self.logViolation('spacing.namespace', tokens[0],
                              'There must be exactly on space between namespace identifier and opening brace.')
            return
        # Exactly two spaces between closing brace and comment
        if rparen.extent.end.line != comment.extent.end.line:  # On the same line.
            self.logViolation('spacing.namespace', tokens[0],
                              'Right parenthesis and comment must be on same line.')
            return
        if rparen.extent.end.column + 2 != comment.extent.start.column:  # Two spaces.
            self.logViolation('spacing.namespace', tokens[0],
                              'There must be exactly two spaces between right parenthesis and comment.')
            return
        # Comment must be "// namespace <namespace name>"
        if comment.spelling != '// namespace %s' % identifier.spelling:
            self.logViolation('spacing.namespace', tokens[0],
                              'The closing comment must be "// namespace <identifier>".')
            return

    def getLParen(self):  # TODO(holtgrew): Dupe!
        tk = ci.TokenKind
        token_set = self._getTokenSet()
        for t in token_set:
            if t.kind == tk.PUNCTUATION or t.spelling == '{':
                return t
        return None

    def getRParen(self):  # TODO(holtgrew): Dupe!
        tk = ci.TokenKind
        token_set = self._getTokenSet()
        for t in reversed(token_set):
            if t.kind == tk.PUNCTUATION or t.spelling == '}':
                return t
        return None


def getHandler(indentation_check, node, parent):
    ##print 'getHandler()', indentation_check, node, parent
    ck = ci.CursorKind
    HANDLERS = {
        ck.STRUCT_DECL: NullHandler(indentation_check, 'struct', node, parent),
        ck.UNION_DECL: NullHandler(indentation_check, '<null>', node, parent),
        ck.CLASS_DECL: NullHandler(indentation_check, 'class', node, parent),
        ck.ENUM_DECL: NullHandler(indentation_check, '<null>', node, parent),
        ck.FUNCTION_DECL: NullHandler(indentation_check, 'function', node, parent),
        ck.VAR_DECL: NullHandler(indentation_check, '<null>', node, parent),
        ck.PARM_DECL: NullHandler(indentation_check, '<null>', node, parent),
        ck.TYPEDEF_DECL: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_METHOD: NullHandler(indentation_check, '<null>', node, parent),
        ck.NAMESPACE: NamespaceHandler(indentation_check, 'namespace', node, parent),
        ck.LINKAGE_SPEC: NullHandler(indentation_check, '<null>', node, parent),
        ck.CONSTRUCTOR: NullHandler(indentation_check, '<null>', node, parent),
        ck.DESTRUCTOR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CONVERSION_FUNCTION: NullHandler(indentation_check, '<null>', node, parent),
        ck.TEMPLATE_TYPE_PARAMETER: NullHandler(indentation_check, '<null>', node, parent),
        ck.TEMPLATE_NON_TYPE_PARAMETER: NullHandler(indentation_check, '<null>', node, parent),
        ck.FUNCTION_TEMPLATE: NullHandler(indentation_check, '<null>', node, parent),
        ck.CLASS_TEMPLATE: NullHandler(indentation_check, '<null>', node, parent),
        ck.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION: NullHandler(indentation_check, '<null>', node, parent),
        ck.NAMESPACE_ALIAS: NullHandler(indentation_check, '<null>', node, parent),
        ck.USING_DIRECTIVE: NullHandler(indentation_check, '<null>', node, parent),
        ck.TYPE_ALIAS_DECL: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_ACCESS_SPEC_DECL: NullHandler(indentation_check, '<null>', node, parent),
        ck.CALL_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.BLOCK_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.STRING_LITERAL: NullHandler(indentation_check, '<null>', node, parent),
        ck.CHARACTER_LITERAL: NullHandler(indentation_check, '<null>', node, parent),
        ck.PAREN_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.UNARY_OPERATOR: NullHandler(indentation_check, '<null>', node, parent),
        ck.ARRAY_SUBSCRIPT_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.BINARY_OPERATOR: NullHandler(indentation_check, '<null>', node, parent),
        ck.COMPOUND_ASSIGNMENT_OPERATOR: NullHandler(indentation_check, '<null>', node, parent),
        ck.INIT_LIST_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.ADDR_LABEL_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.StmtExpr: NullHandler(indentation_check, '<null>', node, parent),
        ck.GENERIC_SELECTION_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_STATIC_CAST_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_DYNAMIC_CAST_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_REINTERPRET_CAST_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_CONST_CAST_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_FUNCTIONAL_CAST_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_TYPEID_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_BOOL_LITERAL_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_NULL_PTR_LITERAL_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_THIS_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_THROW_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_NEW_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_DELETE_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_UNARY_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.PACK_EXPANSION_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.SIZE_OF_PACK_EXPR: NullHandler(indentation_check, '<null>', node, parent),
        ck.LABEL_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.COMPOUND_STMT: NullHandler(indentation_check, 'compound stmt', node, parent),
        ck.CASE_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.DEFAULT_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.IF_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.SWITCH_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.WHILE_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.DO_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.FOR_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.GOTO_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.INDIRECT_GOTO_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.CONTINUE_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.BREAK_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.RETURN_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.ASM_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_CATCH_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_TRY_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.CXX_FOR_RANGE_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.NULL_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.DECL_STMT: NullHandler(indentation_check, '<null>', node, parent),
        ck.UNEXPOSED_ATTR: NullHandler(indentation_check, '<null>', node, parent),
        ck.PREPROCESSING_DIRECTIVE: NullHandler(indentation_check, '<null>', node, parent),
        ck.MACRO_DEFINITION: NullHandler(indentation_check, '<null>', node, parent),
        ck.MACRO_INSTANTIATION: NullHandler(indentation_check, '<null>', node, parent),
        ck.INCLUSION_DIRECTIVE: NullHandler(indentation_check, '<null>', node, parent),
        }
    res = HANDLERS.get(node.kind, NullHandler(indentation_check, '<null>', node, parent))
    ##print ' -->', res
    return res

class WhitespaceCheck(lc.TreeCheck):
    def __init__(self, config=WhitespaceConfig()):
        super(WhitespaceCheck, self).__init__()
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
            handler.checkWhitespace()
        self.level += 1

    def exitNode(self, node):
        self.level -= 1
        self.handlers.pop()
