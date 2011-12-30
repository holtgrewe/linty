#!/usr/bin/env python
"""The implementation of the linty indentation checks."""

from __future__ import with_statement

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@fu-berlin.de>'

import logging
import sys

import violations as lv
import checks as lc

import clang.cindex as ci

# ============================================================================
# Global Indentation Related Code
# ============================================================================


def lengthExpandedTabs(s, to_idx, tab_width):
    l = 0
    for i in range(0, to_idx):
        if s[i] == '\t':
            l += (l / tab_width + 1)  * tab_width
        else:
            l += 1
    return l


class IndentLevel(object):
    """Encapsulates a set of acceptable indentation levels."""

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
        ##print type(self), 'accept(), level=', self.levels, 'indent=', indent
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
        return 'IndentLevel({%s})' % (', '.join(map(str, list(self.levels))))


# ============================================================================
# Basic And Generic Node Handlers
# ============================================================================


class IndentSyntaxNodeHandler(object):
    """Base class for node handlers in the IndentationCheck."""

    def __init__(self, indentation_check, handler_name, node, parent):
        self.indentation_check = indentation_check
        self.handler_name = handler_name
        self.node = node
        self.parent = parent
        self.config = indentation_check.config
        self.level = self._getLevelImpl()
        self.violations = indentation_check.violations
        self._token_set = None

    # ------------------------------------------------------------------------
    # Token Retrieval Related.
    # ------------------------------------------------------------------------

    def getFirstToken(self):
        """Returns first token."""
        ts = self._getTokenSet()
        assert len(ts) > 0, 'There must be a first token!'
        return ts[0]

    def _getTokenSet(self):
        """Return TokenSet for this node, cached in self._token_set."""
        if self._token_set:
            return self._token_set
        tu = self.node.translation_unit
        # TODO(holtgrew): The following workaround is only necessary because of inconsistency in libclang.
        # Get extent data, to be fixed below.
        start_file = self.node.extent.start.file
        start_line = self.node.extent.start.line
        start_column = self.node.extent.start.column
        start = ci.SourceLocation.from_position(tu, start_file, start_line, start_column)
        end_file = self.node.extent.end.file
        end_line = self.node.extent.end.line
        end_column = self.node.extent.end.column
        # Fix extent.
        npath, contents, lines = self.indentation_check.file_reader.readFile(start_file.name)
        line = lines[self.node.extent.end.line - 1]
        end_column = min(end_column, len(line.rstrip()))
        # Build SourceRange.
        end = ci.SourceLocation.from_position(tu, end_file, end_line, end_column)
        extent = ci.SourceRange.from_locations(start, end)
        # End of fixing extent.
        self._token_set = ci.tokenize(tu, extent)
        return self._token_set

    # ------------------------------------------------------------------------
    # Level-Related Methods
    # ------------------------------------------------------------------------

    def _getLevelImpl(self):
        """Return suggested level for this handler, as suggested by the parent."""
        suggested_level = self.parent.suggestedChildLevel(self)
        return suggested_level

    def suggestedChildLevel(self, indent_syntax_node_handler):
        """Return suggested level for children."""
        additional_offset = self.config.indentation_size * self.additionalIndentLevels()
        ##print 'SUGGESTED CHILD LEVEL', self, additional_offset, 'level=', self.level
        return IndentLevel(base=self.level, offset=additional_offset)

    def logViolation(self, rule_type, node, text):
        """Log a rule violation with the given type, location, and text."""
        file_name = None
        if node.extent.start.file is not None:
            file_name = node.extent.start.file.name
        v = lv.RuleViolation(rule_type, file_name, node.extent.start.line,
                             node.extent.start.column, text)
        self.violations.add(v)

    def additionalIndentLevels(self):
        """Returns number of levels to increase the indent by.

        Override this function to change the default behaviour of returning 0.
        """
        return 0

    # ------------------------------------------------------------------------
    # Indentation Checking-Related
    # ------------------------------------------------------------------------

    def checkIndentation(self):
        """Most basic implementation for indentation checks.

        The basic implementation just calls checkStartColumn().
        """
        self.checkStartColumn()

    def checkStartColumn(self):
        """Check the start column of the handled node for valid indentation.

        If the node does not start the line (i.e. there are nodes left of it on
        the same line) then the check is skipped.
        """
        ##print >>sys.stderr, 'START\t\t', self.node.extent.start
        ##print >>sys.stderr, 'LEVELs\t\t', self.level.levels
        if not self.startsLine(self.node):
            logging.debug("Node does not start line (%s).", self.node.extent)
            return
        if not self.level.accept(self.expandedTabsColumnNo(self.node)):
            params = (', '.join(map(str, self.level.levels)), )
            msg = 'Invalid indent. Expecting one of {%s}' % params
            self.logViolation('indent.generic', self.node, msg)

    def handlesChildCurlyBraces(self):
        """Returns True when it handles child curly braces itself."""
        return False

    # ------------------------------------------------------------------------
    # Method For Checking Cursor/Token Positions
    # ------------------------------------------------------------------------

    def startsLine(self, node):
        """Check whether the given node is at the beginning of the line."""
        return self.getLineStart(node) == self.expandedTabsColumnNo(node)

    def areOnSameLine(self, node1, node2):
        """Check whether two nodes start on the same line."""
        return node1 and node2 and node1.extent.start.line == node2.extent.start.line

    def areOnSameColumn(self, node1, node2):
        """Check whether two nodes start on the same column."""
        return node1 and node2 and node1.extent.start.column == node2.extent.start.column

    def areAdjacent(self, node1, node2):
        """Check whether two nodes are directly adjacent."""
        if node1.location.file.name != node2.location.file.name:
            return False
        if node1.extent.end.line != node2.extent.start.line:
            return False
        if node1.extent.end.column != node2.extent.start.column:
            return False
        return True

    def expandedTabsColumnNo(self, node):
        """Return column of node after expanding tabs."""
        if node.extent.start.file is None:
            return 0
        npath, contents, lines = self.indentation_check.file_reader.readFile(node.extent.start.file.name)
        line = lines[node.extent.start.line - 1]
        return lengthExpandedTabs(line, node.extent.start.column - 1, self.indentation_check.config.tab_size)

    def getLineStart(self, node):
        """Return expanded column of line starts (non-whitespace char)."""
        if node.extent.start.file is None:
            return 0
        npath, contents, lines = self.indentation_check.file_reader.readFile(node.extent.start.file.name)
        line = lines[node.extent.start.line - 1]
        i = 0
        for i, x in enumerate(line):
            if not x.isspace():
                break
        return lengthExpandedTabs(line, i, self.indentation_check.config.tab_size)


class RootHandler(IndentSyntaxNodeHandler):
    """Handler registered at the root of the cursor hierarchy."""

    def __init__(self, indentation_check):
        super(RootHandler, self).__init__(indentation_check, None, None, None)

    def checkIndentation(self):
        """Do nothing by design."""
        pass  # Nothing to check.

    def _getLevelImpl(self):
        """Return IndentLevel(indent=0) to start with."""
        return IndentLevel(indent=0)


class UnexposedNodeHandler(IndentSyntaxNodeHandler):
    """Base class for handlers of unexposed nodes.

    Currently only forwards handlesChildCurlyBraces() to parent and indentation
    check is switched off.
    """

    def checkIndentation(self):
        """Does nothing by design."""

    def handlesChildCurlyBraces(self):
        """Forward to parent."""
        return self.parent.handlesChildCurlyBraces()


class CurlyBraceBlockHandler(IndentSyntaxNodeHandler):
    """Handler for curly brace blocks."""

    def handlesChildCurlyBraces(self):
        """Return True."""
        return True
    
    def checkCurlyBraces(self, indent_type):
        """Check curly braces of the block.

        @param indent_type  The indent type for the braces, one of 'same-line',
                            'next-line', and 'next-line-indent'.
        """
        lbrace = self.getLCurlyBrace()
        rbrace = self.getRCurlyBrace()
        t = self.getTokenLeftOfLeftLCurlyBrace()
        # Exit if there is no left curly brace and check for coherence of rbrace
        # and t.
        if lbrace is None:
            assert rbrace is None
            assert t is None
            return
        if indent_type == 'same-line':
            if not self.areOnSameLine(t, lbrace):
                msg = 'Opening brace should be on the same line as the token left of it.'
                self.logViolation('indent.brace', lbrace, msg)
            ##print 'fst    ', self.getFirstToken().extent, self.getFirstToken().spelling
            ##print 't      ', t.extent, t.spelling
            ##print 'lbrace ', rbrace.extent, rbrace.spelling
            ##print 'rbrace ', rbrace.extent, rbrace.spelling
            if not self.areOnSameColumn(self.getFirstToken(), rbrace):
                msg = 'Closing brace should be on the same column as block start.'
                self.logViolation('indent.brace', rbrace, msg)
        elif indent_type == 'next-line':
            if not self.areOnSameColumn(self.getFirstToken(), lbrace):
                msg = 'Opening brace should be on the same column as block start.'
                self.logViolation('indent.brace', lbrace, msg)
            if t.extent.start.line == lbrace.extent.start.line + 1:
                msg = 'Opening brace should be on the line directly after block start.'
                self.logViolation('indent.brace', lbrace, msg)
            if not self.areOnSameColumn(self.getFirstToken(), rbrace):
                msg = 'Closing brace should be on the same column as block start.'
                self.logViolation('indent.brace', rbrace, msg)
        else:
            assert indent_type == 'next-line-indent'
            if t.extent.start.line == lbrace.extent.start.line + 1:
                msg = 'Opening brace should be on the line directly after block start.'
                self.logViolation('indent.brace', lbrace, msg)
            # Check that the opening and closing braces are indented one level
            # further than the block start.
            next_level = IndentLevel(base=self.level, offset=self.config.indentation_size)
            ##print 'rbrace     ', rbrace.spelling, rbrace.extent
            ##print 'next level ', next_level
            if not next_level.accept(self.expandedTabsColumnNo(lbrace)):
                msg = 'Opening brace should be indented one level further than block start.'
                self.logViolation('indent.brace', lbrace, msg)
            if not next_level.accept(self.expandedTabsColumnNo(rbrace)):
                msg = 'Closing brace should be indented one level further than block start.'
                self.logViolation('indent.brace', rbrace, msg)

    def getTokenLeftOfLeftLCurlyBrace(self):
        """Return the token left of the first opening curly brace or None."""
        tk = ci.TokenKind
        token_set = self._getTokenSet()
        res = None
        for t in token_set:
            if t.kind == tk.PUNCTUATION and t.spelling == '{':
                return res
            res = t
        return None

    def getLCurlyBrace(self):
        """"Return the first opening curly brace or None."""
        tk = ci.TokenKind
        token_set = self._getTokenSet()
        for t in token_set:
            if t.kind == tk.PUNCTUATION and t.spelling == '{':
                return t
        return None

    def getRCurlyBrace(self):
        """Return the last closing curly brace or None."""
        tk = ci.TokenKind
        token_set = self._getTokenSet()
        ##for x in token_set:
        ##    print x.spelling, ', ',
        ##print
        for t in reversed(token_set):
            if t.kind == tk.PUNCTUATION and t.spelling == '}':
                return t
        return None


# ============================================================================
# Handlers For AST Nodes
# ============================================================================

# TODO(holtgrew): Checks for more complex structure.

class AddrLabelExprHandler(IndentSyntaxNodeHandler):
    """Handler for AddrLabelExpr nodes."""
    # TODO(holtgrew): Decide what to do with this.


class ArraySubscriptExprHandler(IndentSyntaxNodeHandler):
    """Handler for ArraySubscriptExpr nodes."""


class AsmStmtHandler(IndentSyntaxNodeHandler):
    """Handler for AsmStmt nodes."""


class BinaryOperatorHandler(IndentSyntaxNodeHandler):
    """Handler for BinaryOperator nodes."""


class BlockExprHandler(CurlyBraceBlockHandler):
    """Handler for BlockExpr nodes."""

    # TODO(holtgrew): Sophisticated checks.


class BreakStmtHandler(IndentSyntaxNodeHandler):
    """Handler for BreakStmt nodes."""


class CallExprHandler(IndentSyntaxNodeHandler):
    """Handler for CallExpr nodes."""


class CaseStmtHandler(IndentSyntaxNodeHandler):
    """Handler for CaseStmt nodes."""


class CharacterLiteralHandler(IndentSyntaxNodeHandler):
    """Handler for CharacterLiteral nodes."""


class ClassDeclHandler(CurlyBraceBlockHandler):
    """Handler for class declarations.

    This does not include class template declarations or partial class template
    specializations.
    """

    def checkIndentation(self):
        # TODO(holtgrew): Need to implement more involved checks, positioning of keyword etc.?
        # Check the start column of the class declaration.
        self.checkStartColumn()
        # Check position of braces.
        self.checkCurlyBraces(self.config.brace_positions_class_struct_declaration)

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_class_struct_declaration == 'next-line-indent')
        i2 = int(self.config.indent_inside_class_struct_body)
        return i1 + i2


class ClassTemplateHandler(CurlyBraceBlockHandler):
    """Handler for class templates.

    This includes struct templates.
    """

    def checkIndentation(self):
        # TODO(holtgrew): Need to implement more involved checks, positioning of keyword etc.?
        # Check the start column of the class declaration.
        self.checkStartColumn()
        # Check position of braces.
        self.checkCurlyBraces(self.config.brace_positions_class_struct_declaration)

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_class_struct_declaration == 'next-line-indent')
        i2 = int(self.config.indent_inside_class_struct_body)
        return i1 + i2


class ClassTemplatePartialSpecializationHandler(CurlyBraceBlockHandler):
    """Handler for partial class template specializations.

    This includes struct templates.
    """

    def checkIndentation(self):
        # TODO(holtgrew): Need to implement more involved checks, positioning of keyword etc.?
        # Check the start column of the class declaration.
        self.checkStartColumn()
        # Check position of braces.
        self.checkCurlyBraces(self.config.brace_positions_class_struct_declaration)

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_class_struct_declaration == 'next-line-indent')
        i2 = int(self.config.indent_inside_class_struct_body)
        return i1 + i2


class CompoundAssignmentOperatorHandler(IndentSyntaxNodeHandler):
    """Handler for CompoundAssignmentOperator nodes."""


class CompoundLiteralExprHandler(IndentSyntaxNodeHandler):
    """Handler for CompoundLiteralExpr nodes."""


class CompoundStmtHandler(CurlyBraceBlockHandler):
    """Handler for CompoundStmt nodes."""

    def checkIndentation(self):
        """Check indentation when required.

        Checking of indentation is only required when the parenting node does
        not take care of this itself.
        """
        if not self.needsToCheckIndentation():
            return  # Skip checking

        lbrace = self.getLCurlyBrace()
        if not self.level.accept(lbrace):
            msg = 'Opening brace not properly indented.'
            self.logViolation('indent.brace', lbrace, msg)
        rbrace = self.getRCurlyBrace()
        if not self.level.accept(rbrace):
            msg = 'Closing brace not properly indented.'
            self.logViolation('indent.brace', rbrace, msg)

    def needsToCheckIndentation(self):
        """Returns True if handler needs to check indentation."""
        return not self.parent.handlesChildCurlyBraces()

    def additionalIndentLevels(self):
        if self.parent.handlesChildCurlyBraces():
            return 0
        return int(self.config.indent_statements_within_blocks)


class ConditionalOperatorHandler(IndentSyntaxNodeHandler):
    """Handler for ConditionalOperatorHandler nodes."""


class ConstructorHandler(IndentSyntaxNodeHandler):
    """Handler for Constructor nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class ContinueStmtHandler(IndentSyntaxNodeHandler):
    """Handler for ContinueStmt nodes."""


class ConversionFunctionHandler(CurlyBraceBlockHandler):
    """Handler for ConversionFunction nodes."""

    def checkIndentation(self):
        # TODO(holtgrew): Need to implement more involved checks, positioning of keyword etc.?
        # Check the start column of the class declaration.
        self.checkStartColumn()
        # Check position of braces.
        self.checkCurlyBraces(self.config.brace_positions_function_declaration)

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_function_declaration == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_function_bodies)
        return i1 + i2


class CstyleCastExprHandler(IndentSyntaxNodeHandler):
    """Handler for CStyleCastExpr nodes."""


class CxxAccessSpecDeclHandler(IndentSyntaxNodeHandler):
    """Handler for CxxAccessSpecDecl nodes."""

    def checkIndentation(self):
        pass  # Do nothing.

    # TODO(holtgrew): Should be indented by one more level if self.config.indent_visibility_specifiers.
    # TODO(holtgrew): Adding indentation for next tokens in case of self.config.indent_below_visibility_specifiers.


class CxxBaseSpecifierHandler(IndentSyntaxNodeHandler):
    """Handler for CxxBaseSpecifier nodes."""


class CxxBoolLiteralExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxBoolLiteralExpr nodes."""


class CxxCatchStmtHandler(IndentSyntaxNodeHandler):
    """Handler for CxxCatchStmtHandler nodes."""


class CxxConstCastExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxConstCastExpr nodes."""


class CxxDeleteExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxDeleteExpr nodes."""


class CxxDynamicCastExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxDynamicCastExpr nodes."""


class CxxForRangeStmtHandler(CurlyBraceBlockHandler):
    """Handler for CxxForRangeStmt nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_blocks == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_blocks)
        return i1 + i2


class CxxFunctionalCastExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxFunctionalCastExpr nodes."""


class CxxMethodHandler(CurlyBraceBlockHandler):
    """Handler for CxxMethodHandler nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_function_declaration == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_function_bodies)
        return i1 + i2


class CxxNewExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxNewExpr nodes."""


class CxxNullPtrLiteralExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxNullPtrLiteralExpr nodes."""


class CxxReinterpretCastExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxReinterpretCastExpr nodes."""


class CxxStaticCastExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxStaticCastExpr nodes."""


class CxxThisExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxThisExprHandler nodes."""


class CxxThrowExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxThrowExprHandler nodes."""


class CxxTryStmtHandler(CurlyBraceBlockHandler):
    """Handler for CxxTryStmtHandler nodes."""

    ##def checkIndentation(self):
    ##    pass
        # TODO(holtgrew): Need to implement more involved checks, positioning of keyword etc.?
        # Check the start column of the class declaration.
        ##self.checkStartColumn()
        # Check position of braces.
        ##self.checkCurlyBraces(self.config.brace_positions_class_struct_declaration)

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_blocks == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_blocks)
        return i1 + i2


class CxxTypeidExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxTypeidExpr nodes."""


class CxxUnaryExprHandler(IndentSyntaxNodeHandler):
    """Handler for CxxUnaryExprHandler nodes."""


class DeclRefExprHandler(IndentSyntaxNodeHandler):
    """Handler for DeclRefExprHandler nodes."""


class DeclStmtHandler(IndentSyntaxNodeHandler):
    """Handler for DeclStmt nodes."""


class DefaultStmtHandler(IndentSyntaxNodeHandler):
    """Handler for DefaultStmt nodes."""


class DestructorHandler(CurlyBraceBlockHandler):
    """Handler for CxxMethodHandler nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_function_declaration == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_function_bodies)
        return i1 + i2


class DoStmtHandler(CurlyBraceBlockHandler):
    """Handler for DoStmt nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_blocks == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_blocks)
        return i1 + i2


class EnumConstantDeclHandler(IndentSyntaxNodeHandler):
    """Handler for EnumConstantDecl nodes."""


class EnumDeclHandler(IndentSyntaxNodeHandler):
    """Handler for EnumDecl nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_class_struct_declaration == 'next-line-indent')
        i2 = int(self.config.indent_inside_class_struct_body)
        return i1 + i2


class FieldDeclHandler(IndentSyntaxNodeHandler):
    """Handler for FieldDecl nodes."""


class FloatingLiteralHandler(IndentSyntaxNodeHandler):
    """Handler for FloatingLiteralHandler nodes."""


class ForStmtHandler(CurlyBraceBlockHandler):
    """Handler for ForStmtHandler nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_blocks == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_blocks)
        return i1 + i2


class FunctionDeclHandler(CurlyBraceBlockHandler):
    """Handler for FunctionDecl nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_function_declaration == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_function_bodies)
        return i1 + i2


class FunctionTemplateHandler(CurlyBraceBlockHandler):
    """Handler for FunctionTemplate nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_function_declaration == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_function_bodies)
        return i1 + i2


class GenericSelectionExprHandler(IndentSyntaxNodeHandler):
    """Handler for GenericSelectionExpr nodes."""


class GnuNullExprHandler(IndentSyntaxNodeHandler):
    """Handler for GnuNullExpr nodes."""


class GotoStmtHandler(IndentSyntaxNodeHandler):
    """Handler for GotoStmt nodes."""


class IbActionAttrHandler(IndentSyntaxNodeHandler):
    """Handler for IbActionAttr nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class IbOutletAttrHandler(IndentSyntaxNodeHandler):
    """Handler for IbOutletAttr nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class IbOutletCollectionAttrHandler(IndentSyntaxNodeHandler):
    """Handler for IbOutletCollectionAttr nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class IfStmtHandler(CurlyBraceBlockHandler):
    """Handler for IfStmt nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_blocks == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_blocks)
        return i1 + i2


class ImaginaryLiteralHandler(IndentSyntaxNodeHandler):
    """Handler for ImaginaryLiteral nodes."""


class InclusionDirectiveHandler(IndentSyntaxNodeHandler):
    """Handler for InclusionDirective nodes."""
    # TODO(holtgrew): What's this?

    def checkIndentation(self):
        pass  # Do nothing.


class IndirectGotoStmtHandler(IndentSyntaxNodeHandler):
    """Handler for IndirectGotoStmt nodes."""


class InitListExprHandler(IndentSyntaxNodeHandler):
    """Handler for InitListExpr nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class IntegerLiteralHandler(IndentSyntaxNodeHandler):
    """Handler for IntegerLiteral nodes."""


class InvalidCodeHandler(IndentSyntaxNodeHandler):
    """Handler for InvalidCode nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class InvalidFileHandler(IndentSyntaxNodeHandler):
    """Handler for InvalidFile nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class LabelRefHandler(IndentSyntaxNodeHandler):
    """Handler for LabelRef nodes. Do nothing.

    This cannot appear on the top level.
    """

    def checkIndentation(self):
        pass  # Do nothing.


class LabelStmtHandler(IndentSyntaxNodeHandler):
    """Handler for LabelStmt nodes."""

    def checkIndentation(self):
        """Make sure the label is indented correctly."""
        if self.config.indent_labels_flush_left:
            if not self.startsLine(self.node):
                msg = 'Label must be first non-whitespace on line.'
                self.logViolation('indent.generic', self.node, msg)
            elif self.expandedTabsColumnNo(self.node) != 0:
                msg = 'Labels should have no indentation.'
                self.logViolation('indent.generic', self.node, msg)
        else:
            # Indent with the rest of the code.    
            self.checkStartColumn()


class LinkageSpecHandler(IndentSyntaxNodeHandler):
    """Handler for LinkageSpec nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class MacroDefinitionHandler(IndentSyntaxNodeHandler):
    """Handler for MacroDefinition nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class MacroInstantiationHandler(IndentSyntaxNodeHandler):
    """Handler for MacroInstantiation nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class MemberRefHandler(IndentSyntaxNodeHandler):
    """Handler for MemberRef nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class MemberRefExprHandler(IndentSyntaxNodeHandler):
    """Handler for MemberRefExpr nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class NamespaceHandler(CurlyBraceBlockHandler):
    """Handler for NamespaceHandler nodes."""

    def checkIndentation(self):
        # Check the start column of the class declaration.
        self.checkStartColumn()
        # Check position of braces.
        self.checkCurlyBraces(self.config.brace_positions_namespace_declaration)

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_namespace_declaration == 'next-line-indent')
        i2 = int(self.config.indent_declarations_within_namespace_definition)
        ##print >>sys.stderr, 'NAMESPACE HANDLER i1=', i1, ', i2=', i2
        return i1 + i2


class NamespaceAliasHandler(IndentSyntaxNodeHandler):
    """Handler for NamespaceAlias nodes."""


class NamespaceRefHandler(IndentSyntaxNodeHandler):
    """Handler for NamespaceRef nodes. Do nothing.

    This cannot be a "top level" statement.
    """

    def checkIndentation(self):
        pass  # Do nothing.


class NotImplementedHandler(IndentSyntaxNodeHandler):
    """Handler for NotImplemented nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class NoDeclFoundHandler(IndentSyntaxNodeHandler):
    """Handler for NoDeclFound nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class NullStmtHandler(IndentSyntaxNodeHandler):
    """Handler for NullStmt nodes."""


class ObjcAtCatchStmtHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcAtCatchStmt nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcAtFinallyStmtHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcAtFinallyStmt nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcAtSynchronizedStmtHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcAtSynchronizedStmt nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcAtThrowStmtHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcAtThrowStmt nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcAtTryStmtHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcAtTryStmt nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcAutoreleasePoolStmtHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcAutoreleasePoolStmt nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcBridgeCastExprHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcBridgeCastExpr nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcCategoryDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcCategoryDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcCategoryImplDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcCategoryImplDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcClassMethodDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcClassMethodDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcClassRefHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcClassRef nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcDynamicDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcDynamicDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcEncodeExprHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcEncodeExpr nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcForCollectionStmtHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcForCollectionStmt nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcImplementationDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcImplementationDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcInstanceMethodDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcInstanceMethodDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcInterfaceDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcInterfaceDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcIvarDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcIvarDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcMessageExprHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcMessageExpr nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcPropertyDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcPropertyDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcProtocolDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcProtocolDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcProtocolExprHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcProtocolExpr nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcProtocolRefHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcProtocolRef nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcSelectorExprHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcSelectorExpr nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcStringLiteralHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcStringLiteral nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcSuperClassRefHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcSuperClassRef nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class ObjcSynthesizeDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ObjcSynthesizedDecl nodes."""
    # TODO(holtgrew): Ignoring Objective-C for now.

    def checkIndentation(self):
        pass  # Do nothing.


class OverloadedDeclRefHandler(IndentSyntaxNodeHandler):
    """Handler for OverloadedDeclRef nodes. Does nothing.

    This does occur in correct programs.
    """

    def checkIndentation(self):
        pass  # Do nothing.


class PackExpansionExprHandler(IndentSyntaxNodeHandler):
    """Handler for PackExpansionExpr nodes."""


class ParenExprHandler(IndentSyntaxNodeHandler):
    """Handler for ParenExpr nodes."""


class ParmDeclHandler(IndentSyntaxNodeHandler):
    """Handler for ParmDecl nodes. Do nothing."""
    # TODO(holtgrew): Not a top-level item.

    def checkIndentation(self):
        pass  # Do nothing.


class PreprocessingDirectiveHandler(IndentSyntaxNodeHandler):
    """Handler for PreprocessingDirective nodes. Do nothing."""
    # TODO(holtgrew): How to even get this out of clang?

    def checkIndentation(self):
        pass  # Do nothing.


class ReturnStmtHandler(IndentSyntaxNodeHandler):
    """Handler for ReturnStmt nodes."""


class SehExceptStmtHandler(IndentSyntaxNodeHandler):
    """Handler for SehExceptStmt nodes."""
    # TODO(holtgrew): Ignoring SEH for now.

    def checkIndentation(self):
        pass  # Do nothing.


class SehFinallyStmtHandler(IndentSyntaxNodeHandler):
    """Handler for SehFinallyStmt nodes."""
    # TODO(holtgrew): Ignoring SEH for now.

    def checkIndentation(self):
        pass  # Do nothing.


class SehTryStmtHandler(IndentSyntaxNodeHandler):
    """Handler for SehTryStmt nodes."""
    # TODO(holtgrew): Ignoring SEH for now.

    def checkIndentation(self):
        pass  # Do nothing.


class SizeOfPackExprHandler(IndentSyntaxNodeHandler):
    """Handler for SizeOfPackExpr nodes."""


class StringLiteralHandler(IndentSyntaxNodeHandler):
    """Handler for StringLiteral nodes."""


class StructDeclHandler(ClassDeclHandler):
    """The handler for struct declarations is the same as for classes.

    Subclassing is (mis-)used as quasi-aliasing here.
    """


class SwitchStmtHandler(CurlyBraceBlockHandler):
    """Handler for SwitchStmt nodes."""

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_blocks == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_blocks)
        return i1 + i2


class StmtexprHandler(IndentSyntaxNodeHandler):
    """Handler for Stmtexpr nodes. Do nothing."""
    # TODO(holtgrew): This is a GNU extension skelleton from the closet. Ignore for now.


class TemplateNonTypeParameterHandler(IndentSyntaxNodeHandler):
    """Handler for TemplateNonTypeParameter nodes.

    Cannot appear at the beginning of lines, thus we need no indentation
    checking here."""
    # TODO(holtgrew): We could also mark this using a QuietSyntaxNodeHandler that has an empty checkIndentation() implementation.

    def checkIndentation(self):
        pass  # Do nothing by design.


class TemplateRefHandler(IndentSyntaxNodeHandler):
    """Handler for TemplateRef nodes.

    Cannot appear at the beginning of lines, thus we need no indentation
    checking here."""
    # TODO(holtgrew): We could also mark this using a QuietSyntaxNodeHandler that has an empty checkIndentation() implementation.

    def checkIndentation(self):
        pass  # Do nothing by design.


class TemplateTemplateParameterHandler(IndentSyntaxNodeHandler):
    """Handler for TemplateTemplateParameter nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class TemplateTypeParameterHandler(IndentSyntaxNodeHandler):
    """Handler for TemplateTypeParameter nodes.

    Cannot appear at the beginning of lines, thus we need no indentation
    checking here."""
    # TODO(holtgrew): We could also mark this using a QuietSyntaxNodeHandler that has an empty checkIndentation() implementation.

    def checkIndentation(self):
        pass  # Do nothing by design.


class TranslationUnitHandler(IndentSyntaxNodeHandler):
    """Handler for TranslationUnit nodes.

    Cannot appear at the beginning of lines, thus we need no indentation
    checking here."""
    # TODO(holtgrew): We could also mark this using a QuietSyntaxNodeHandler that has an empty checkIndentation() implementation.

    def checkIndentation(self):
        pass  # Do nothing by design.


class TypedefDeclHandler(IndentSyntaxNodeHandler):
    """Handler for TypedefDecl nodes."""


class TypeAliasDeclHandler(IndentSyntaxNodeHandler):
    """Handler for TypeAliasDecl nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class TypeRefHandler(IndentSyntaxNodeHandler):
    """Handler for TypeRef nodes.

    Cannot appear at the beginning of lines, thus we need no indentation
    checking here."""
    # TODO(holtgrew): We could also mark this using a QuietSyntaxNodeHandler that has an empty checkIndentation() implementation.

    def checkIndentation(self):
        pass  # Do nothing by design.


class UnaryOperatorHandler(IndentSyntaxNodeHandler):
    """Handler for UnaryOperator nodes."""


class UnexposedAttrHandler(UnexposedNodeHandler):
    """Handler for UnexposedAttr nodes.

    By design, this handler does nothing.
    """

    def checkIndentation(self):
        pass  # Do nothing.


class UnexposedDeclHandler(UnexposedNodeHandler):
    """Handler for UnexposedDecl nodes.

    By design, this handler does nothing.
    """

    def checkIndentation(self):
        pass  # Do nothing.


class UnexposedExprHandler(UnexposedNodeHandler):
    """Handler for UnexposedExpr nodes.

    By design, this handler does nothing.
    """

    def checkIndentation(self):
        pass  # Do nothing.


class UnexposedStmtHandler(UnexposedNodeHandler):
    """Handler for UnexposedStmt nodes.

    By design, this handler does nothing.
    """

    def checkIndentation(self):
        pass  # Do nothing.


class UnionDeclHandler(ClassDeclHandler):
    """The handler for struct declarations is the same as for classes.

    Subclassing is (mis-)used as quasi-aliasing here.
    """


class UsingDeclarationHandler(IndentSyntaxNodeHandler):
    """Handler for UsingDeclaration nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class UsingDirectiveHandler(IndentSyntaxNodeHandler):
    """Handler for UsingDirective nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class VarDeclHandler(IndentSyntaxNodeHandler):
    """Handler for VarDecl nodes."""

    def checkIndentation(self):
        pass  # Do nothing.


class WhileStmtHandler(CurlyBraceBlockHandler):
    """Handler for WhileStmt nodes."""

    def checkIndentation(self):
        # TODO(holtgrew): Need to implement more involved checks, positioning of keyword etc.?
        # Check the start column of the class declaration.
        self.checkStartColumn()
        # Check position of braces.
        self.checkCurlyBraces(self.config.brace_positions_blocks)

    def additionalIndentLevels(self):
        i1 = int(self.config.brace_positions_blocks == 'next-line-indent')
        i2 = int(self.config.indent_statements_within_blocks)
        return i1 + i2


# ============================================================================
# Code For Indentation Check
# ============================================================================


def getHandler(indentation_check, node, parent):
    # Get node kind name as UPPER_CASE, get class name and class object.
    kind_name = repr(str(node.kind)).split('.')[-1]
    class_name = kind_name.replace('\'', '').replace('_', ' ').title().replace(' ', '') + 'Handler'
    klass = eval(class_name)
    # Instantiate handler and return.
    handler = klass(indentation_check, kind_name, node, parent)
    return handler


class UnknownParameter(Exception):
    """Raised when an unknown indentation parameter is used."""


class IndentationConfig(object):
    """Configuration for the indentation check.

    Look into the source for all the settings, there are a LOT.
    """

    def __init__(self, **kwargs):
        """Initialize indentation settings with K&R style."""

        # The settings here are based on the Eclipse CDT indentation config, K&R
        # style.
        #
        # We will first set the default values.  Then, this represents the known
        # style parameters and we will overwrite the properties from kwargs if
        # they are already there.

        # --------------------------------------------------------------------
        # General Settings
        # --------------------------------------------------------------------

        # The policy for tabs to accept.
        # Valid values: 'tabs-only', 'spaces-only', 'mixed'.
        self.tab_policy = 'spaces-only'
        # The number of spaces to use for one indentation.
        self.indentation_size = 4
        # The number of spaces that one TAB character is wide.
        self.tab_size = 4

        # --------------------------------------------------------------------
        # Indent
        # --------------------------------------------------------------------

        # Indent 'public', 'protected', and 'private' within class body.
        self.indent_visibility_specifiers = False
        # Indent declarations relative to 'public', 'procted, and 'private'.
        self.indent_below_visibility_specifiers = True
        # Indent declarations relative to class/struct body.
        self.indent_inside_class_struct_body = True
        # Indent statements within function bodies.
        self.indent_statements_within_function_bodies = True
        # Indent statements within blocks.
        self.indent_statements_within_blocks = True
        # Indent statements within switch blocks.
        self.indent_statements_within_switch_body = False
        # Indent statements within case body.
        self.indent_statements_within_case_body = True
        # Indent 'break' statements.
        self.indent_break_statements = True
        # Indent declarations within 'namespace' definition.
        self.indent_declarations_within_namespace_definition = False
        # Indent empty lines.  DEACTIVATED
        # self.indent_empty_lines = False
        # Whether or not to indent labels with usual code or to flush left.
        self.indent_labels_flush_left = True

        # --------------------------------------------------------------------
        # Brace Positions
        # --------------------------------------------------------------------

        # Valid values for the following variables are 'same-line', 'next-line',
        # 'next-line-indented'.

        # Brace positions for class / struct declarations.
        self.brace_positions_class_struct_declaration = 'same-line'
        # Brace positions for namespace declarations.
        self.brace_positions_namespace_declaration = 'same-line'
        # Brace positions for function declarations.
        self.brace_positions_function_declaration = 'same-line'
        # Brace positions for blocks.
        self.brace_positions_blocks = 'same-line'
        # Brace positions of blocks in case statements.
        self.brace_positions_blocks_in_case_statement = 'same-line'
        # Brace positions of switch statements.
        self.brace_positions_switch_statement = 'same-line'
        # Brace positions for initializer list.
        self.brace_positions_brace_positions_initializer_list = 'same-line'
        # Keep empty initializer list on one line.
        self.brace_positions_keep_empty_initializer_list_on_one_line = True

        # --------------------------------------------------------------------
        # White Space
        # --------------------------------------------------------------------

        # Declarations / Types

        # Insert space before opening brace of a class.
        self.insert_space_before_opening_brace_of_a_class = True
        # Insert space before colon of base clause.
        self.insert_space_before_colon_of_base_clause = False
        # Insert space after colon of base clause.
        self.insert_space_after_colon_of_base_clause = True
        # Insert space before_comma_in_base_clause.
        self.insert_space_before_comma_in_base_clause = False
        # Insert space after comma in base clause.
        self.insert_space_after_comma_in_base_clause = True

        # Declarations / Declarator list

        # Insert space before comma in declarator list.
        self.insert_space_before_comma_in_declarator_list = False
        # Insert space after comma in declarator list.
        self.insert_space_after_comma_in_declarator_list = True

        # Declarations / Functions

        self.insert_space_before_opening_function_parenthesis = False
        self.insert_space_after_opening_function_parenthesis = False
        self.insert_space_before_closing_function_parenthesis = False
        self.insert_space_between_empty_function_parentheses = False
        self.insert_space_before_opening_function_brace = True
        self.insert_space_before_comma_in_parameters = False
        self.insert_space_after_comma_in_parameters = True

        # Declarations / Exception Specification

        self.insert_space_before_opening_exception_specification_parenthesis = True
        self.insert_space_after_opening_exception_specification_parenthesis = False
        self.insert_space_before_closing_exception_specification_parenthesis = False
        self.insert_space_between_empty_exception_specification_parenthesis = True
        self.insert_space_before_comma_in_exception_specification_parameters = False
        self.insert_space_after_comma_in_exception_specification_parameters = True

        # Declarations / Labels

        self.insert_space_before_label_colon = False
        self.insert_space_after_label_colon = True

        # Control Statements

        self.insert_space_before_control_statement_semicolon = False;

        # Control Statements / Blocks

        self.insert_space_before_opening_block_brace = True
        self.insert_space_after_closing_block_brace = True

        # Control Statements / 'if else'

        self.insert_space_before_opening_if_else_parenthesis = True
        self.insert_space_after_opening_if_else_parenthesis = False
        self.insert_space_before_closing_if_else_parenthesis = False

        # Control Statements / 'for'

        self.insert_space_before_opening_for_parenthesis = True
        self.insert_space_after_opening_for_parenthesis = False
        self.insert_space_before_closing_for_parenthesis = False
        self.insert_space_before_for_semicolon = False
        self.insert_space_after_for_semicolon = True

        # Control Statements / 'switch'

        self.insert_space_before_colon_in_switch_case = False
        self.insert_space_before_colon_in_switch_default = False
        self.insert_space_before_opening_switch_brace = True
        self.insert_space_before_opening_switch_parenthesis = True
        self.insert_space_after_opening_switch_parenthesis = False
        self.insert_space_before_closing_switch_parenthesis = False

        # Control Statements / 'while' & 'do while'

        self.insert_space_before_opening_do_while_parenthesis = True
        self.insert_space_after_opening_do_while_parenthesis = False
        self.insert_space_before_closing_do_while_parenthesis = False

        # Control Statements / 'catch'

        self.insert_space_before_opening_catch_parenthesis = True
        self.insert_space_after_opening_catch_parenthesis = False
        self.insert_space_before_closing_catch_parenthesis = False

        # Expressions / Function invocations

        self.insert_space_before_opening_function_invocation_parenthesis = False
        self.insert_space_after_opening_function_invocation_parenthesis = False
        self.insert_space_before_closing_function_invocation_parenthesis = False
        self.insert_space_between_empty_function_invocation_parentheses = False
        self.insert_space_before_comma_in_function_arguments = False
        self.insert_space_after_comma_in_function_arguments = True

        # Expressions / Assignments

        self.insert_space_before_assignment_operator = True
        self.insert_space_after_assignment_operator = True

        # Expressions / Initializer list

        self.insert_space_before_opening_initializer_list_brace = True
        self.insert_space_after_opening_initializer_list_brace = True
        self.insert_space_before_closing_initializer_list_brace = True
        self.insert_space_before_initializer_list_comma = False
        self.insert_space_after_initializer_list_comma = True
        self.insert_space_between_empty_initializer_list_braces = False

        # Expressions / Operators

        self.insert_space_before_binary_operators = True
        self.insert_space_after_binary_operators = True
        self.insert_space_before_unary_operators = False
        self.insert_space_after_unary_operators = False
        self.insert_space_before_prefix_operators = False
        self.insert_space_after_prefix_operators = False
        self.insert_space_before_postfix_operators = False
        self.insert_space_after_postfix_operators = False

        # Expressions / Parenthesized expressions

        self.insert_space_before_opening_parenthesis = False
        self.insert_space_after_opening_parenthesis = False
        self.insert_space_before_closing_parenthesis = False

        # Expressions / Type casts

        self.insert_space_after_opening_parenthesis = False
        self.insert_space_before_closing_parenthesis = False
        self.insert_space_after_closing_parenthesis = True

        # Expressions / Conditionals

        self.insert_space_before_conditional_question_mark = True
        self.insert_space_after_conditional_question_mark = True
        self.insert_space_before_conditional_colon = True
        self.insert_space_after_conditional_colon = True

        # Expressions / Expression list

        self.insert_space_before_comma_in_expression_list = False
        self.insert_space_after_comma_in_expression_list = True

        # Arrays

        self.insert_space_before_opening_array_bracket = False
        self.insert_space_after_opening_array_bracket = False
        self.insert_space_before_closing_array_bracket = False
        self.insert_space_between_empty_array_brackets = False

        # Templates / Template arguments

        self.insert_space_before_opening_template_argument_angle_bracket = False
        self.insert_space_after_opening_template_argument_angle_bracket = False
        self.insert_space_before_template_argument_comma = False
        self.insert_space_after_template_argument_comma = True
        self.insert_space_before_closing_template_argument_angle_bracket = False
        self.insert_space_after_closing_template_argument_angle_bracket = True

        # Templates / Template parameters

        self.insert_space_before_opening_template_parameter_angle_bracket = False
        self.insert_space_after_opening_template_parameter_angle_bracket = False
        self.insert_space_before_template_parameter_comma = False
        self.insert_space_after_template_parameter_comma = True
        self.insert_space_before_closing_template_parameter_angle_bracket = False
        self.insert_space_after_closing_template_parameter_angle_bracket = True


        # --------------------------------------------------------------------
        # Control Statements (General)
        # --------------------------------------------------------------------

        # Insert new line before 'else' in an 'if' statement.
        self.insert_new_line_before_else_in_an_if_statement = False
        # Insert new line before 'catch' in a 'try' statement.
        self.insert_new_line_before_catch_in_a_try_statement = False
        # Insert new line before 'while' in a 'do' statement.
        self.insert_new_line_before_while_in_a_do_statement = False

        # --------------------------------------------------------------------
        # Control Statements ('if else')
        # --------------------------------------------------------------------

        # Keep 'then' statement on same line.
        self.keep_then_statement_on_same_line = False
        # Keep simple 'if' on one line.
        self.keep_simple_if_on_one_line = False
        # Keep 'else' statement on same line.
        self.keep_else_statement_on_same_line = False
        # Keep 'else if' on one line.
        self.keep_else_if_on_one_line = True

        # --------------------------------------------------------------------
        # Line Wrapping
        # --------------------------------------------------------------------

        # Line wrappings in brackets (parameter and initializer lists).

        # Wrapped lines are allowed to flush to the start of the previous list.
        self.line_wrapping_allow_flush = True
        # Wrapped lines are allowed to be indented.
        self.line_wrapping_allow_indent = True
        # By how many levels to indent wrapped lines.
        self.line_wrapping_indent = 2

        # Wrapped initializer list lines are allowed to flush to the start of
        # the previous list.
        self.line_wrapping_initializer_list_allow_flush = True
        # Wrapped initializer list lines are allowed to be indented.
        self.line_wrapping_initializer_list_allow_indent = True
        # By how many levels to indent wrapped initializer list lines.
        self.line_wrapping_initializer_list_indent = 2

        # --------------------------------------------------------------------
        # Overwrite From kwargs
        # --------------------------------------------------------------------

        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise UnknownParameter('Unknown parameter "%s".' % key)
            setattr(self, key, value)


class IndentationCheck(lc.TreeCheck):
    """Check for code and brace indentation."""

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
        logging.debug('%sEntering Node: %s %s (%s)', '  ' * self.level, node.kind, node.spelling, node.location)
        handler = getHandler(self, node, self.handlers[-1])
        logging.debug('  %s[indent level=%s]', '  ' * self.level, str(handler.level))
        self.handlers.append(handler)
        if handler:
            handler.checkIndentation()
        self.level += 1

    def exitNode(self, node):
        self.level -= 1
        self.handlers.pop()
