#!/usr/bin/env python
"""Tests for the module of whitespace in nosetests style."""

import indent as li
import test_utils as lt

import sys

# ============================================================================
# Tests for the namespace indent handler.
# ============================================================================

# TODO(holtgrew): Indentation of first token.
# TODO(holtgrew): Closing comment.

def test_namespace_indent_declaration_false_correct():
    cpp_str = """
namespace myns {
typedef int x;
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_declarations_within_namespace_definition=False
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    assert len(violations) == 0


def test_namespace_indent_declaration_false_incorrect():
    cpp_str = """
namespace myns {
    typedef int x;
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_declarations_within_namespace_definition=False
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.statement'
    assert v.line == 3
    assert v.column == 5


def test_namespace_indent_declaration_true_incorrect():
    cpp_str = """
namespace myns {
    typedef int x;
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_declarations_within_namespace_definition=True
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    assert len(violations) == 0


def test_namespace_indent_declaration_true_incorrect():
    cpp_str = """
namespace myns {
typedef int x;
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
        indent_declarations_within_namespace_definition=True
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.statement'
    assert v.line == 3
    assert v.column == 1


def test_namespace_brace_positon_same_line_correct():
    cpp_str = """
namespace myns {
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_namespace_declaration='same-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_namespace_brace_positon_same_line_incorrect_opening_brace():
    cpp_str = """
namespace myns
{
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_namespace_declaration='same-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 3
    assert v.column == 1


def test_namespace_brace_positon_same_line_incorrect_closing_brace():
    cpp_str = """
namespace myns {
    }  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_namespace_declaration='same-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 3
    assert v.column == 5


def test_namespace_brace_positon_next_line_correct():
    cpp_str = """
namespace myns
{
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_namespace_declaration='next-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_namespace_brace_positon_next_line_incorrect_first_brace_sameline():
    cpp_str = """
namespace myns {
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_namespace_declaration='next-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 2
    assert v.column == 16


def test_namespace_brace_positon_next_line_incorrect_first_brace_indent():
    cpp_str = """
namespace myns
    {
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_namespace_declaration='next-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 3
    assert v.column == 5


def test_namespace_brace_positon_next_line_indented_correct():
    cpp_str = """
namespace myns
    {
    }  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_namespace_declaration='next-line-indented'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_namespace_brace_positon_next_line_indented_incorrect_first_brace():
    cpp_str = """
namespace myns
{
    }  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_namespace_declaration='next-line-indent'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 3
    assert v.column == 1


def test_namespace_brace_positon_next_line_indented_incorrect_second_brace():
    cpp_str = """
namespace myns
    {
}  // namespace myns
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_namespace_declaration='next-line-indent'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the struct indent handler.
# ============================================================================

# The StructDeclHandler is a direct child of the ClassDeclHandler and does
# change anything about its parent class.  We do not need to test it.

# ============================================================================
# Tests for the class indent handler.
# ============================================================================

# TODO(holtgrew): Indentation of first token.

def test_class_indent_declaration_false_correct():
    cpp_str = """
class MyClass {
typedef int x;
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_inside_class_struct_body=False
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    assert len(violations) == 0


def test_class_indent_declaration_false_incorrect():
    cpp_str = """
class MyClass {
    typedef int x;
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_inside_class_struct_body=False
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.statement'
    assert v.line == 3
    assert v.column == 5


def test_class_indent_declaration_true_incorrect():
    cpp_str = """
class MyClass {
    typedef int x;
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_inside_class_struct_body=True
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    assert len(violations) == 0


def test_class_indent_declaration_true_incorrect():
    cpp_str = """
class MyClass {
typedef int x;
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_inside_class_struct_body=True
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.statement'
    assert v.line == 3
    assert v.column == 1


def test_namespace_brace_positon_same_line_correct():
    cpp_str = """
class MyClass {
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='same-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_namespace_brace_positon_same_line_incorrect_opening_brace():
    cpp_str = """
class MyClass
{
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='same-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 3
    assert v.column == 1


def test_namespace_brace_positon_same_line_incorrect_closing_brace():
    cpp_str = """
class MyClass {
    };
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='same-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 3
    assert v.column == 5


def test_namespace_brace_positon_next_line_correct():
    cpp_str = """
class MyClass
{
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='next-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_namespace_brace_positon_next_line_incorrect_first_brace_sameline():
    cpp_str = """
class MyClass {
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='next-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 2
    assert v.column == 15


def test_namespace_brace_positon_next_line_incorrect_first_brace_indent():
    cpp_str = """
class MyClass
    {
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='next-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 3
    assert v.column == 5


def test_namespace_brace_positon_next_line_indented_correct():
    cpp_str = """
class MyClass
    {
    };
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='next-line-indented'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_namespace_brace_positon_next_line_indented_incorrect_first_brace():
    cpp_str = """
class MyClass
{
    };
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='next-line-indent'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 3
    assert v.column == 1


def test_namespace_brace_positon_next_line_indented_incorrect_second_brace():
    cpp_str = """
class MyClass
    {
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='next-line-indent'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.brace'
    assert v.line == 4
    assert v.column == 1


