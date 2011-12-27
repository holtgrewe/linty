#!/usr/env/bin python
"""Utility code for the linty tests."""

import logging
import tempfile
import os
import os.path

import main as lm

class Data(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def checkTUStr(cppStr, ast_check=None, file_check=None, config={}):
    """Run check on the C++ program given as the string cppStr.

    Returns a set with the violations.
    """
    # Create temporary file.
    tmp_file_name = tempfile.mktemp('.cpp')
    try:
        tmp_file = open(tmp_file_name, 'w+b')
        tmp_file.write(cppStr)
        tmp_file.seek(0)
        # TODO(holtgrew): We need to restore the level again.
        logging.basicConfig(level=logging.ERROR)

        # Setup Checker, especially options.
        options = Data(include_dirs=[os.path.dirname(tmp_file.name)],
                       ignore_nolint=False,
                       show_source=False,
                       ignore_rules=[])
        ast_checks = []
        if ast_check:
            ast_checks.append(ast_check)
        file_checks = []
        if file_check:
            file_checks.append(file_check)
        checker = lm.Checker(options, ast_checks, file_checks)
                
        res = checker.process([tmp_file.name])
        tmp_file.close()
    finally:
        os.unlink(tmp_file_name)
        violations = set()
        for check in checker.ast_checks + checker.file_checks:
            violations.update(check.violations)
        return violations
