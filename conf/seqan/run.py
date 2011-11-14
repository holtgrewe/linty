#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import linty.app as la
import linty.checks as lc
import linty.indent as li

BASE_PATH = os.path.dirname(__file__)

AST_CHECKS = [
    li.IndentationCheck()
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
