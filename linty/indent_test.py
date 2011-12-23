#!/usr/bin/env python
"""Tests for the module of whitespace."""

import indent as li
import test_utils as lt

import sys

# Tests for the namespace handler.

def test_namespace_correct():
    cpp_str = """
namespace myns {
}  // namespace myns
"""
    violations = lt.checkTUStr(cpp_str, ast_check=li.IndentationCheck())
    assert len(violations) == 0

def test_namespace_lbrace_line():
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

def test_namespace_rbrace_indent():
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


