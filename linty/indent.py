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


class IndentLevel(object):
    def __init__(self, indent=None, base=None, offset=None):
        assert (indent is not None) or (base is not None) or (offset is not None)
        self.levels = set()
        if indent is not None:
            self.levels.add(indent)
        else:
            assert (base is not None) and (offset is not None)
            for l in base.levels:
                self.levels.add(l + offset)
    
    def isMultilevel(self):
        return len(self.levels) > 1

    def accept(self, indent):
        print type(self), 'accept(), level=', self.levels, 'indent=', indent
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

    def suggestedChildLevel(self, child):
        return IndentLevel(base=self.level, offset=1)

    def suggestedChildLevel(self, indent_syntax_node_handler):
        return self.level

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
        # Check indentation of current line start.
        token_set = self._getTokenSet()
        first_token = token_set[0]
        if not self.level.accept(self.expandedTabsColumnNo(first_token)):
            self.violations.add(lv.RuleViolation('indentation', first_token.location.file.name,
                                                 first_token.location.line, first_token.location.column,
                                                 'Invalid indentation!'))
        # Check left and right parenthesis.
        self.checkLParen(self.getLParen())
        self.checkRParen(self.getLParen(), self.getRParen())


class RootHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check):
        super(RootHandler, self).__init__(indentation_check, None, None, None)
    
    def checkIndentation(self):
        pass  # Nothing to check.

    def _getLevelImpl(self):
        return IndentLevel(indent=0)


class NullHandler(IndentSyntaxNodeHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(type(self), self).__init__(indentation_check, handler_name, node, parent)

    def checkIndentation(self):
        pass


class NamespaceHandler(BlockParenHandler):
    def __init__(self, indentation_check, handler_name, node, parent):
        super(type(self), self).__init__(indentation_check, handler_name, node, parent)

    def checkLParen(self, left_paren):
        return super(type(self), self).checkLParen(left_paren, self.indentation_check.config.brace_sameline_namespace)


class ClassDeclHandler(IndentSyntaxNodeHandler):
    """Indentation syntax node handler for classes/structs."""
    def __init__(self, indentation_check, handler_name, node, parent):
        super(type(self), self).__init__(indentation_check, handler_name, node, parent)

    def checkIndentation(self):
        pass

    def checkLParen(self, left_paren):
        return super(type(self), self).checkLParen(left_paren, self.indentation_check.config.brace_sameline_class)



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
        ck.STRUCT_DECL: ClassDeclHandler(indentation_check, 'struct', node, parent),
        ck.UNION_DECL: NullHandler(indentation_check, '<null>', node, parent),
        ck.CLASS_DECL: ClassDeclHandler(indentation_check, 'class', node, parent),
        ck.ENUM_DECL: NullHandler(indentation_check, '<null>', node, parent),
        ck.FUNCTION_DECL: FunctionDeclHandler(indentation_check, 'function', node, parent),
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
        ck.COMPOUND_STMT: CompoundStmtHandler(indentation_check, 'compound stmt', node, parent),
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
        ck.RETURN_STMT: ReturnStmtHandler(indentation_check, '<null>', node, parent),
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


class IndentationCheck(lc.TreeCheck):
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
