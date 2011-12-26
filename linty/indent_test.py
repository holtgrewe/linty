#!/usr/bin/env python
"""Tests for the module of whitespace."""

import indent as li
import test_utils as lt

import sys

# ============================================================================
# Tests for the namespace handler.
# ============================================================================

def test_namespace_correct():
    cpp_str = """
namespace myns {
}  // namespace myns
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_namespace_correct_empty():
    cpp_str = """
namespace myns {}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_namespace_lbrace_on_wrong_line():
    cpp_str = """
namespace myns
{
}  // namespace myns
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.line == 3
    assert v.column == 1
    assert v.rule_id == 'indentation.brace'

def test_namespace_rbrace_indent_wrong():
    cpp_str = """
namespace myns {
  }  // namespace myns
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.line == 3
    assert v.column == 3
    assert v.rule_id == 'indentation.brace'

# ============================================================================
# Tests for the function handler.
# ============================================================================

def test_function_correct_minimal():
    cpp_str = """
int main()
{
}
"""
def test_function_correct_empty():
    cpp_str = """
int main()
{}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_function_correct_inline_sameline():
    cpp_str = """
inline int main()
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_function_correct_inline_split():
    cpp_str = """
inline int
main()
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_function_correct_static_sameline():
    cpp_str = """
static int main()
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_function_correct_static_split():
    cpp_str = """
static int
main()
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_function_correct_parameters_wrap():
    cpp_str = """
int main(int p1, int p2, int p3,
         int p4, int p5)
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_function_correct_parameters_newline():
    cpp_str = """
int main(
    int p1, int p2, int p3,
    int p4, int p5)
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_function_correct_nonempty_body():
    cpp_str = """
int main()
{
    int x = 0;
    return x;
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_function_error_lbrace_sameline():
    cpp_str = """
int main() {
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 1
    v = list(violations)[0]
    print v
    assert v.line == 2
    assert v.column == 12
    assert v.rule_id == 'indentation.brace'

def test_function_error_lbrace_space_line():
    cpp_str = """
int main()

{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 1
    v = list(violations)[0]
    assert v.line == 4
    assert v.column == 1
    assert v.rule_id == 'indentation.brace'

def test_function_error_lbrace_wrong_indent():
    cpp_str = """
int main()
    {
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    v = list(violations)[0]
    assert len(violations) == 1
    assert v.line == 3
    assert v.column == 5
    assert v.rule_id == 'indentation.brace'

def test_function_error_rbrace_wrong_indent():
    cpp_str = """
int main()
{
    }
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    v = list(violations)[0]
    assert v.line == 4
    assert v.column == 5
    assert v.rule_id == 'indentation.brace'

def XXXtest_function_error_inline_split_all():
    cpp_str = """
inline
unsigned int
main(int argc, char ** argv)
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 1

def XXXtest_function_error_inline_split_inline():
    cpp_str = """
inline
int main()
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 1

def XXXtest_function_error_static_split_all():
    cpp_str = """
static
int
main()
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 1

def XXXtest_function_error_static_split_static():
    cpp_str = """
static
int main()
{
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 1

def test_function_error_indent_body_oneline():
    cpp_str = """
static
int main() { return 0; }
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 1

def test_function_error_indent_body_wrong_indent():
    cpp_str = """
int main()
{
   int x;
    int y;
     int z;
}
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 2
