#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import linty.app as la
import linty.checks as lc
import linty.indent as li
import linty.whitespace as lw

BASE_PATH = os.path.dirname(__file__)

INDENT_CONFIG = li.IndentationConfig(
    brace_positions_class_struct_declaration = 'next-line',
    brace_positions_function_declaration = 'next-line',
    brace_positions_blocks = 'next-line',
    brace_positions_blocks_in_case_statement = 'next-line',
    brace_positions_switch_statement = 'next-line',
    brace_positions_namespace_declaration = 'same-line',
    )

WHITESPACE_CONFIG = lw.WhitespaceConfig()

AST_CHECKS = [
    li.IndentationCheck(INDENT_CONFIG),
    lw.WhitespaceCheck(WHITESPACE_CONFIG),
    ]

FILE_CHECKS = [
    # ------------------------------------------------------------------------
    # Text-Level Checks.
    # ------------------------------------------------------------------------
    # These checks are based on the text of the file only.  Only simple parsing
    # is done such as parsing out comments.
    
    # All libray files must have a matching SeqAn library header.
    lc.RegexpHeaderCheck(path=os.path.join(BASE_PATH, 'seqan_library.header')),
    # All files must end with a newline.
    lc.FileEndsWithNewlineCheck('\n'),
    # No line may have trailing whitespace.
    lc.NoTrailingWhitespaceCheck(),
    # We only allow Unix line endings.
    lc.OnlyUnixLineEndings(),
    # Check TODO comments.
    lc.TodoCommentChecker(),
    ]

def main():
    return la.main(AST_CHECKS, FILE_CHECKS)

if __name__ == '__main__':
    sys.exit(main())
