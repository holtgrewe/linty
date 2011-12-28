#!/usr/bin/env python
"""Tests for the module of whitespace in nosetests style."""

import indent as li
import test_utils as lt

import sys

# ============================================================================
# Tests for the struct indent handler.
# ============================================================================

# The StructDeclHandler is a direct child of the ClassDeclHandler and does
# change anything about its parent class.  We do not need to test it.

# ============================================================================
# Tests for the address label expression handler.
# ============================================================================

# TODO(holtgrew): Decide what to do with this.


# ============================================================================
# Tests for the array subscript expression handler.
# ============================================================================

def test_array_subscript_expression_indent_correct():
    cpp_str = """
void f() {
    int arr[10];
    arr[0];  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_array_subscript_expression_indent_incorrect():
    cpp_str = """
void f() {
    int arr[10];
arr[0];  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the asm statement handler.
# ============================================================================

def test_asm_statement_expression_indent_correct():
    cpp_str = """
void f() {
    asm("mov eax 0");  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_asm_statement_expression_indent_incorrect():
    cpp_str = """
void f() {
asm("mov eax 0");  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the binary operator handler.
# ============================================================================

def test_binary_operator_expression_indent_correct():
    cpp_str = """
void f() {
    5 < 6;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_binary_operator_expression_indent_incorrect():
    cpp_str = """
void f() {
5 < 6;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the block expr handler.
# ============================================================================

def test_block_expression_indent_correct():
    cpp_str = """
void f() {
    ^ (int) { return 0; }  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_block_expression_indent_incorrect():
    cpp_str = """
void f() {
^ (int) { return 0; }  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the break statement handler.
# ============================================================================

def test_break_statement_indent_correct():
    cpp_str = """
void f() {
    while (true)
        break;  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_break_statement_indent_incorrect():
    cpp_str = """
void f() {
    while (true)
    break;  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 5


# ============================================================================
# Tests for the call expression handler.
# ============================================================================

def test_call_expression_indent_correct():
    cpp_str = """
void bar() {}

void f() {
    bar();  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_call_expression_indent_incorrect():
    cpp_str = """
void bar() {}

void f() {
bar();  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 5
    assert v.column == 1


# ============================================================================
# Tests for the case statement handler.
# ============================================================================

# TODO(holtgrew): Continue here, this is more involved.


# ============================================================================
# Tests for the character literal handler.
# ============================================================================

def test_character_literal_indent_correct():
    cpp_str = """
void f() {
    'c';  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_character_literal_indent_incorrect():
    cpp_str = """
void f() {
'c';  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the class declaration indent handler.
# ============================================================================

def test_class_indent_correct():
    cpp_str = """
class C {
    class D {
    };
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_class_indent_incorrect():
    cpp_str = """
class C {
class D {
}
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


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


def test_class_brace_position_same_line_correct():
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


def test_class_brace_position_same_line_incorrect_opening_brace():
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


def test_class_brace_position_same_line_incorrect_closing_brace():
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


def test_class_brace_position_next_line_correct():
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


def test_class_brace_position_next_line_incorrect_first_brace_sameline():
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


def test_class_brace_position_next_line_incorrect_first_brace_indent():
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


def test_class_brace_position_next_line_indented_correct():
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


def test_class_brace_position_next_line_indented_incorrect_first_brace():
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


def test_class_brace_position_next_line_indented_incorrect_second_brace():
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


# ============================================================================
# Tests for the class template indent handler.
# ============================================================================

def test_class_template_indent_correct():
    cpp_str = """
class C {
    template <typename T>
    class D {
    };
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_class_template_indent_incorrect():
    cpp_str = """
class C {
template <typename T>
class D {
}
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


def test_class_template_indent_declaration_false_correct():
    cpp_str = """
template <typename T>
class MyClass {
typedef int x;
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_inside_class_struct_body=False
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    assert len(violations) == 0


def test_class_template_indent_declaration_false_incorrect():
    cpp_str = """
template <typename T>
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
    assert v.line == 4
    assert v.column == 5


def test_class_template_indent_declaration_true_incorrect():
    cpp_str = """
template <typename T>
class MyClass {
    typedef int x;
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_inside_class_struct_body=True
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    assert len(violations) == 0


def test_class_template_indent_declaration_true_incorrect():
    cpp_str = """
template <typename T>
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
    assert v.line == 4
    assert v.column == 1


def test_class_template_brace_position_same_line_correct():
    cpp_str = """
template <typename T>
class MyClass {
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='same-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_class_template_brace_position_same_line_incorrect_opening_brace():
    cpp_str = """
template <typename T>
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
    assert v.line == 4
    assert v.column == 1


def test_class_template_brace_position_same_line_incorrect_closing_brace():
    cpp_str = """
template <typename T>
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
    assert v.line == 4
    assert v.column == 5


def test_class_template_brace_position_next_line_correct():
    cpp_str = """
template <typename T>
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


def test_class_template_brace_position_next_line_incorrect_first_brace_sameline():
    cpp_str = """
template <typename T>
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
    assert v.line == 3
    assert v.column == 15


def test_class_template_brace_position_next_line_incorrect_first_brace_indent():
    cpp_str = """
template <typename T>
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
    assert v.line == 4
    assert v.column == 5


def test_class_template_brace_position_next_line_indented_correct():
    cpp_str = """
template <typename T>
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


def test_class_template_brace_position_next_line_indented_incorrect_first_brace():
    cpp_str = """
template <typename T>
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


def test_class_template_brace_position_next_line_indented_incorrect_second_brace():
    cpp_str = """
template <typename T>
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
    assert v.line == 5
    assert v.column == 1

# ============================================================================
# Tests for the partial class template specialization indent handler.
# ============================================================================

# TODO(holtgrew): Indentation of first token.

def test_class_template_specialization_indent_correct():
    cpp_str = """
class C {
    template <typename T1, typename T2> class D;
    template <typename T>
    class D<int, T> {
    };
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_class_template_specialization_indent_incorrect():
    cpp_str = """
class C {
    template <typename T1, typename T2> class D;
template <typename T>
class D<int, T> {
}
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


def test_partial_class_template_specialization_indent_declaration_false_correct():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T><int, T> {
typedef int x;
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_inside_class_struct_body=False
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    assert len(violations) == 0


def test_partial_class_template_specialization_indent_declaration_false_incorrect():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T> {
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
    assert v.line == 6
    assert v.column == 5


def test_partial_class_template_specialization_indent_declaration_true_incorrect():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T> {
    typedef int x;
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            indent_inside_class_struct_body=True
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    assert len(violations) == 0


def test_partial_class_template_specialization_indent_declaration_true_incorrect():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T> {
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
    assert v.line == 6
    assert v.column == 1


def test_partial_class_template_specialization_brace_position_same_line_correct():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T> {
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='same-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_partial_class_template_specialization_brace_position_same_line_incorrect_opening_brace():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T>
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
    assert v.line == 6
    assert v.column == 1


def test_partial_class_template_specialization_brace_position_same_line_incorrect_closing_brace():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T> {
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
    assert v.line == 6
    assert v.column == 5


def test_partial_class_template_specialization_brace_position_next_line_correct():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T>
{
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='next-line'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_partial_class_template_specialization_brace_position_next_line_incorrect_first_brace_sameline():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T> {
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
    assert v.line == 5
    assert v.column == 23


def test_partial_class_template_specialization_brace_position_next_line_incorrect_first_brace_indent():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T>
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
    assert v.line == 6
    assert v.column == 5


def test_partial_class_template_specialization_brace_position_next_line_indented_correct():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T>
    {
    };
"""
    check = li.IndentationCheck(config=li.IndentationConfig(
            brace_positions_class_struct_declaration='next-line-indented'
        ))
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_partial_class_template_specialization_brace_position_next_line_indented_incorrect_first_brace():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T>
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
    assert v.line == 6
    assert v.column == 1


def test_partial_class_template_specialization_brace_position_next_line_indented_incorrect_second_brace():
    cpp_str = """
template <typename T1, typename T2> class MyClass;

template <typename T>
class MyClass<int, T>
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
    assert v.line == 7
    assert v.column == 1


# ============================================================================
# Tests for the compound assignment operator handler.
# ============================================================================

def test_compound_assignment_operator_expression_indent_correct():
    cpp_str = """
void f() {
    int x = 0;
    x += 5;  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_compound_assignment_operator_expression_indent_incorrect():
    cpp_str = """
void f() {
    int x = 0;
x += 5;  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the compound literal expression handler.
# ============================================================================

def test_compound_literal_expression_indent_correct():
    cpp_str = """
void f() {
    (char[]){"string"};  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_compound_literal_expression_indent_incorrect():
    cpp_str = """
void f() {
(char[]){"string"};  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the conditional operator handler.
# ============================================================================

def test_conditional_operator_indent_correct():
    cpp_str = """
void f() {
    (3 > 4) ? true : false;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_conditional_operator_indent_incorrect():
    cpp_str = """
void f() {
(3 > 4) ? true : false;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the constructor handler.
# ============================================================================

# TODO(holtgrew): Implement later on.


# ============================================================================
# Tests for the continue statement handler.
# ============================================================================

def test_continue_statement_indent_correct():
    cpp_str = """
void f() {
    while (true)
        continue;  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_continue_statement_indent_incorrect():
    cpp_str = """
void f() {
    while (true)
    continue;  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 5


# ============================================================================
# Tests for the conversion function handler.
# ============================================================================

def test_conversion_function_indent_correct():
    cpp_str = """
class C {
    operator int() {
        return 0;
    }
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_conversion_function_indent_incorrect():
    cpp_str = """
class C {
operator int() {
    return 0;
}
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C-style cast expression handler.
# ============================================================================

def test_c_style_cast_expr_indent_correct():
    cpp_str = """
void f() {
    (int)3.5;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_c_style_cast_expr_indent_incorrect():
    cpp_str = """
void f() {
(int)3.5;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C++ access specifier handler.
# ============================================================================

# TODO(holtgrew): This is more involved, return here later.


# ============================================================================
# Tests for the C++ base specifier handler.
# ============================================================================

# TODO(holtgrew): This is more involved, return here later.


# ============================================================================
# Tests for the bool literal expression handler.
# ============================================================================

def test_cxx_bool_literal_expr_indent_correct():
    cpp_str = """
void f() {
    false;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_bool_literal_expr_indent_incorrect():
    cpp_str = """
void f() {
false;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C++ catch statement handler.
# ============================================================================

# TODO(holtgrew): This is more involved, return here later.


# ============================================================================
# Tests for the C++ const_cast expression handler.
# ============================================================================

def test_cxx_const_cast_expr_indent_correct():
    cpp_str = """
void f() {
    int x = 5;
    const_cast<int const>(x);  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_const_cast_expr_indent_incorrect():
    cpp_str = """
void f() {
    int x = 5;
const_cast<int const>(x);  // relevant line
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the C++ delete expression handler.
# ============================================================================

def test_cxx_delete_expr_indent_correct():
    cpp_str = """
void f() {
    int * x;
    delete x;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_delete_expr_indent_incorrect():
    cpp_str = """
void f() {
    int * x;
delete x;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the C++ dynamic_cast expression handler.
# ============================================================================

def test_cxx_dynamic_cast_expr_indent_correct():
    cpp_str = """
class C;
class D : C;

void f() {
    D * d;
    dynamic_cast<C *>(d);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_dynamic_cast_expr_indent_incorrect():
    cpp_str = """
class C;
class D : C;

void f() {
    D * d;
dynamic_cast<C *>(d);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 7
    assert v.column == 1


# ============================================================================
# Tests for the C++ for range statement handler.
# ============================================================================

# TODO(holtgrew): Need more tests.
    
def test_cxx_for_range_stmt_indent_correct():
    cpp_str = """
#include <vector>

void f() {
    std::vector<int> v;
    for (int i : v);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_for_range_stmt_indent_incorrect():
    cpp_str = """
#include <vector>

void f() {
    std::vector<int> v;
for (int i : v);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    print violations == 1
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 6
    assert v.column == 1


# ============================================================================
# Tests for the C++ functional cast expression handler.
# ============================================================================

def test_cxx_functional_cast_expr_indent_correct():
    cpp_str = """
void f() {
    int(3.0);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_functional_cast_expr_incorrect():
    cpp_str = """
void f() {
int(3.0);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C++ method handler.
# ============================================================================

# TODO(holtgrew): Need more tests.

def test_cxx_method_handler_indent_correct():
    cpp_str = """
class C {
    int foo() {
    }
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_method_handler_indent_incorrect():
    cpp_str = """
class C {
int foo() {
}
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C++ new expression handler.
# ============================================================================

def test_cxx_new_expr_indent_correct():
    cpp_str = """
void f() {
    new int();
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_new_expr_indent_incorrect():
    cpp_str = """
void f() {
new int();
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C++ nullptr literal expression handler.
# ============================================================================

def test_cxx_nullptr_literal_indent_correct():
    cpp_str = """
void f() {
    nullptr;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


# TODO(holtgrew): Deactivated right now since clang-3.0 ignores statements with nullptr in them.
def XXXtest_cxx_nullptr_literal_indent_incorrect():
    cpp_str = """
void f(nullptr) {
    nullptr;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the C++ reinterpret_cast expression handler.
# ============================================================================

def test_cxx_reinterpret_cast_expr_indent_correct():
    cpp_str = """
void f() {
    reinterpret_cast<unsigned>(5);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_reinterpret_cast_expr_indent_incorrect():
    cpp_str = """
void f() {
reinterpret_cast<unsigned>(5);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C++ static_cast expression handler.
# ============================================================================

def test_cxx_static_cast_expr_indent_correct():
    cpp_str = """
void f() {
    static_cast<unsigned>(5);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_static_cast_expr_indent_incorrect():
    cpp_str = """
void f() {
static_cast<unsigned>(5);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C++ this expression handler.
# ============================================================================

def test_cxx_this_expr_indent_correct():
    cpp_str = """
class C {
    void f() {
        this;
    }
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_this_expr_indent_incorrect():
    cpp_str = """
class C {
    void f() {
this;
    }
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the C++ throw expression handler.
# ============================================================================

def test_cxx_throw_expr_indent_correct():
    cpp_str = """
void f() {
    throw 4;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_throw_expr_indent_incorrect():
    cpp_str = """
void f() {
throw 4;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C++ try statement handler.
# ============================================================================

# TODO(holtgrew): More involved checks.

# TODO(holtgrew): Broken, segfaults :(

def XXXtest_cxx_try_stmt_indent_correct():
    cpp_str = """
void f() {
    try {
    } catch (int i) {
    }
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def XXXtest_cxx_try_stmt_indent_incorrect():
    cpp_str = """
void f() {
try {
} catch (int i) {
}
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the C++ typeid expression handler.
# ============================================================================

def test_cxx_typeid_expr_indent_correct():
    cpp_str = """
#include <typeinfo>

void f() {
    typeid(5);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_typeid_expr_indent_incorrect():
    cpp_str = """
#include <typeinfo>

void f() {
typeid(5);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 5
    assert v.column == 1


# ============================================================================
# Tests for the C++ unary expression handler.
# ============================================================================

# TODO(holtgrew): What's a C++ unary expression?

def test_cxx_unary_expr_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_unary_expr_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the declaration reference expression handler.
# ============================================================================

# TODO(holtgrew): When is this triggered?

def test_cxx_decl_ref_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_decl_ref_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the default statement handler.
# ============================================================================

def test_cxx_default_stmt_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_default_stmt_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the destructor handler.
# ============================================================================

# TODO(holtgrew): More involved tests for destructors.
    
def test_destructor_indent_correct():
    cpp_str = """
class C {
    ~C() {
    }
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_destructor_indent_incorrect():
    cpp_str = """
class C {
~C() {
}
};

"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the do statement handler.
# ============================================================================

# TODO(holtgrew): More involved tests.

def test_do_stmt_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_do_stmt_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the enum constant declaration handler.
# ============================================================================

def test_enum_constant_decl_indent_correct():
    cpp_str = """
void f() {
    do {
    } while (true);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_enum_constant_decl_indent_incorrect():
    cpp_str = """
void f() {
do {
} while (true);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the enum declaration handler.
# ============================================================================

def test_enum_decl_indent_correct():
    cpp_str = """
void f() {
    enum E {
    };
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_enum_decl_indent_incorrect():
    cpp_str = """
void f() {
enum E {
};
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the field declaration handler.
# ============================================================================

def test_field_decl_indent_correct():
    cpp_str = """
class C {
    int x;
};
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_field_decl_indent_incorrect():
    cpp_str = """
class C {
int x;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the floating literal handler.
# ============================================================================

def test_floating_literal_indent_correct():
    cpp_str = """
void f() {
    3.0;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_floating_literal_indent_incorrect():
    cpp_str = """
void f() {
3.0;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the for statement handler.
# ============================================================================

def test_for_stmt_indent_correct():
    cpp_str = """
void f() {
    for (;;) {
    }
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_for_stmt_indent_incorrect():
    cpp_str = """
void f() {
for (;;) {
}
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the function declaration handler.
# ============================================================================

def test_function_decl_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_function_decl_indent_incorrect():
    cpp_str = """
    void f() {
    }
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 2
    assert v.column == 1


# ============================================================================
# Tests for the function template handler.
# ============================================================================

def test_function_template_indent_correct():
    cpp_str = """
template <typename T>
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_function_template_indent_incorrect():
    cpp_str = """
    template <typename T>
    void f() {
    }
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 2
    assert v.column == 1


# ============================================================================
# Tests for the generic selection expression handler.
# ============================================================================

# TODO(holtgrew): How do you trigger this? _Generic?

def test_generic_selection_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_generic_selection_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the GNU NULL expression handler.
# ============================================================================

# TODO(holtgrew): How is this triggered? __gnu_null?

def test_gnu_null_expr_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_gnu_null_expr_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the goto statement handler.
# ============================================================================

def test_goto_stmt_indent_correct():
    cpp_str = """
void f() {
    goto my_label;
my_label:
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_goto_stmt_indent_incorrect():
    cpp_str = """
void f() {
goto my_label;
my_label
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the IB action attr handler.
# ============================================================================

# TODO(holtgrew): Ignore Objective-C for now.

# ============================================================================
# Tests for the IB outlet attr handler.
# ============================================================================

# TODO(holtgrew): Ignore Objective-C for now.


# ============================================================================
# Tests for the IB outlet collection attr handler.
# ============================================================================

# TODO(holtgrew): Ignore Objective-C for now.


# ============================================================================
# Tests for the if statement handler.
# ============================================================================

def test_if_stmt_indent_correct():
    cpp_str = """
void f() {
    if (false) {
    }
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_if_stmt_indent_incorrect():
    cpp_str = """
void f() {
if (false) {
}
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the imaginary literal handler.
# ============================================================================

# TODO(holtgrew): How to trigger this?

def test_imaginary_literal_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_imaginary_literal_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the inclusion directive handler.
# ============================================================================

# TODO(holtgrew): How to trigger this? #include? #import?

def test_inclusion_directive_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_inclusion_directive_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the indirect goto statement handler.
# ============================================================================

# TODO(holtgrew): How does one trigger this?

def test_indirect_goto_stmt_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_indirect_goto_stmt_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the init list expression handler.
# ============================================================================

# TODO(holtgrew): This can probably not appear as the first token. But we need more special checks.


# ============================================================================
# Tests for the integer literal handler.
# ============================================================================

def test_integer_literal_indent_correct():
    cpp_str = """
void f() {
    1;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_integer_literal_indent_incorrect():
    cpp_str = """
void f() {
1;
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1


# ============================================================================
# Tests for the invalid code handler.
# ============================================================================

# TODO(holtgrew): What to do here?

# ============================================================================
# Tests for the invalid file handler.
# ============================================================================

# TODO(holtgrew): What to do here?

# ============================================================================
# Tests for the label reference handler.
# ============================================================================

# TODO(holtgrew): This can probably not appear by its own.

def test_label_reference_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_label_reference_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the label statement handler.
# ============================================================================

# TODO(holtgrew): We probably need configuration for whether to indent or unindent this.
    
def test_label_stmt_indent_correct():
    cpp_str = """
void f() {
my_label:
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_label_stmt_indent_incorrect():
    cpp_str = """
void f() {
    my_label:
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the linkage spec handler handler.
# ============================================================================

# TODO(holtgrew): What exactly is this? >>extern "C"<<?

def test_linkage_spec_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_linkage_spec_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the macro definition handler.
# ============================================================================

# TODO(holtgrew): How do we get this out of clang?

def test_macro_definition_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_macro_definition_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the macro instantiation handler.
# ============================================================================

# TODO(holtgrew): How do we get this out of clang?

def test_macro_instantiation_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_macro_instantiation_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the member reference handler.
# ============================================================================

def test_member_reference_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_member_reference_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


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


def test_namespace_brace_position_same_line_correct():
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


def test_namespace_brace_position_same_line_incorrect_opening_brace():
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


def test_namespace_brace_position_same_line_incorrect_closing_brace():
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


def test_namespace_brace_position_next_line_correct():
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


def test_namespace_brace_position_next_line_incorrect_first_brace_sameline():
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


def test_namespace_brace_position_next_line_incorrect_first_brace_indent():
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


def test_namespace_brace_position_next_line_indented_correct():
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


def test_namespace_brace_position_next_line_indented_incorrect_first_brace():
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


def test_namespace_brace_position_next_line_indented_incorrect_second_brace():
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
# Tests for the namespace alias handler.
# ============================================================================

def test_namespace_alias_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_namespace_alias_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the namespace reference handler.
# ============================================================================

def test_namespace_reference_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_namespace_reference_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the not implemented handler.
# ============================================================================

# TODO(holtgrew): What to do here?


# ============================================================================
# Tests for the no decl found handler.
# ============================================================================

# TODO(holtgrew): What to do here?


# ============================================================================
# Tests for the null statement handler.
# ============================================================================

def test_null_stmt_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_null_stmt_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the Objective-C @catch statement handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C @finally statement handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C @synchronized statement handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C @throw statement handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C @try statement handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C autorelease pool handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C bridge cast expression handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C category declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C category implementation declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C class method declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C class reference handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C dynamic declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C encode expression handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C for collection statement handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C implementation declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C instance method declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C interface declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C ivar declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C message expression declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C property declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C protocol declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C protocol expression handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C protocol reference handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C selector expression handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C string literal handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C super class reference handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the Objective-C synthesized declaration handler.
# ============================================================================

# TODO(holtgrew): Ignoring Objective-C for now.

# ============================================================================
# Tests for the overloaded declaration handler.
# ============================================================================

def test_overloaded_decl_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_overloaded_decl_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the pack expansion expression handler.
# ============================================================================

def test_pack_expansion_expr_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_pack_expansion_expr_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the parenthesis expression handler.
# ============================================================================

def test_parenthesis_expr_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_parenthesis_expr_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the parameter declaration expression handler.
# ============================================================================

def test_parm_decl_expr_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_parm_decl_expr_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the preprocessing directive handler.
# ============================================================================

def test_preprocessing_directive_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_preprocessing_directive_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the return statement handler.
# ============================================================================

def test_return_stmt_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_return_stmt_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the SEH except statement handler.
# ============================================================================

# TODO(holtgrew): Ignoring SEH for now.


# ============================================================================
# Tests for the SEH finally statement handler.
# ============================================================================

# TODO(holtgrew): Ignoring SEH for now.


# ============================================================================
# Tests for the SEH try statement handler.
# ============================================================================

# TODO(holtgrew): Ignoring SEH for now.


# ============================================================================
# Tests for the size of pack expr handler.
# ============================================================================

def test_size_of_pack_expr_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_size_of_pack_expr_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the string literal handler.
# ============================================================================

def test_string_literal_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_string_literal_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the struct declaration handler.
# ============================================================================

# TODO(holtgrew): The same as class declaration by inheritance/aliasing.


# ============================================================================
# Tests for the switch statement handler.
# ============================================================================

def test_switch_stmt_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_switch_stmt_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the statement expression handler.
# ============================================================================

def test_statement_expr_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_statement_expr_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the template non-type parameter handler.
# ============================================================================

def test_template_non_type_parameter_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_template_non_type_parameter_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the template ref handler.
# ============================================================================

def test_template_ref_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_templte_ref_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the template template parameter handler.
# ============================================================================

def test_template_template_parameter_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_template_template_parameter_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the template type parameter handler.
# ============================================================================

def test_template_type_parameter_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_template_type_parameter_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the translation unit handler.
# ============================================================================

# TODO(holtgrew): Nothing to do here, right?


# ============================================================================
# Tests for the typedef declaration handler.
# ============================================================================

def test_typedef_decl_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_typedef_decl_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the type alias declaration handler.
# ============================================================================

def test_type_alias_decl_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_type_alias_decl_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the type reference handler.
# ============================================================================

def test_type_ref_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_type_ref_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the unary operator handler.
# ============================================================================

def test_unary_operator_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_unary_operator_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the union declaration handler.
# ============================================================================

def test_union_decl_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_union_decl_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the using directive  handler.
# ============================================================================

def test_using_directive_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_using_directive_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the variable declaration handler.
# ============================================================================

def test_var_decl_indent_correct():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_var_decl_indent_incorrect():
    cpp_str = """
void f() {
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 4
    assert v.column == 1


# ============================================================================
# Tests for the while statement handler.
# ============================================================================

def test_while_stmt_indent_correct():
    cpp_str = """
void f() {
    while (true);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 0


def test_cxx_delete_expr_indent_incorrect():
    cpp_str = """
void f() {
while (true);
}
"""
    check = li.IndentationCheck(config=li.IndentationConfig())
    violations = lt.checkTUStr(cpp_str, ast_check=check)
    # Check resulting violation.
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.rule_id == 'indent.generic'
    assert v.line == 3
    assert v.column == 1
