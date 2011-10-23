#!/usr/bin/env python
"""Main entry point with default configuration."""

from __future__ import with_statement

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@fu-berlin.de>'

import logging
import optparse
import sys

import linty.main as lm

def createDefaultConfig():
    return [], []


def main(ast_checks, file_checks):
    # Setup option parser.
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', dest='filenames', default=[],
                      action='append', metavar='FILE',
                      help='Compilation unit File(s) (*.c, *.cpp, ...).')
    parser.add_option('-i', '--include-dir', dest='include_dirs', default=[],
                      type='string', help='Specify include directories',
                      action='append')
    parser.add_option('-q', '--quiet', dest='verbosity', default=1,
                      action='store_const', const=0, help='Fewer message.')
    parser.add_option('-v', '--verbose', dest='verbosity', default=1,
                      action='store_const', const=2, help='More messages.')
    parser.add_option('-x', '--ignore-rule', dest='ignore_rules', default=[],
                      action='append', help='Identifiers of rules to ignore.')
    parser.add_option('--ignore-nolint', dest='ignore_nolint', default=False,
                      action='store_const', const=True, help='Ignore "// nolint" statements.')
    parser.add_option('--dont-show-source', dest='show_source', default=True,
                      action='store_const', const=False, help='Suppress source line display')
    # Parse command line.
    options, args = parser.parse_args()

    # Configure logging.
    LEVELS = {0 : logging.ERROR,
              1 : logging.INFO,
              2 : logging.DEBUG}
    logging.basicConfig(level=LEVELS[options.verbosity], format='%(message)s')

    # Setup objects for the actual checking.
    audit_listener = lm.AuditListener()
    checker = lm.Checker(options, ast_checks, file_checks)
    checker.listeners.append(audit_listener)
    # Run the checker.
    res = checker.process(options.filenames)
    return res


if __name__ == '__main__':
    sys.exit(main(*createDefaultConfig()))
