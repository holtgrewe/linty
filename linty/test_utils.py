#!/usr/env/bin python
"""Utility code for the linty tests."""

import logging
import tempfile

import linty.main as lm

def checkTUStr(cppStr, ast_check=None, file_check=None):
    """Run check on the C++ program given as the string cPPStr.

    Returns a set with the violations.
    """
    # Create temporary file.
    tmp_file = tempfile.mkstemp(text=cppStr)
    print tmp_file.name
    # TODO(holtgrew): We need to restore the level again.
    logging.basicConfig(level=None)

    # Setup Checker, especially options.
    options = object()
    options.include_dirs = [os.path.dirname(tmp_file.name)]
    options.ignore_nolint = False
    options.show_source = False
    options.ignore_rules = []
    ast_checks = []
    if ast_check:
        ast_checks.append(ast_check)
    if file_check:
        file_checks.append(file_check)
    checker = lm.Checker(options, ast_checks, file_checks)

    res = checker.process([tmp_file.name])
    return checker.violations
