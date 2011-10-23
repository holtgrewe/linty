#!/usr/bin/env python
"""Main entry point with default configuration."""

from __future__ import with_statement

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@fu-berlin.de>'

import optparse
import sys

import linty.main as lm

def createDefaultConfig():
    return []


def main(config):
    # Setup option parser.
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', dest='filenames', default=[],
                      action='append', metavar='FILE',
                      help='Compilation unit File(s) (*.c, *.cpp, ...).')
    # Parse command line.
    options, args = parser.parse_args()

    # Setup objects for the actual checking.
    audit_listener = lm.AuditListener()
    checker = lm.Checker(options, config)
    checker.listeners.append(audit_listener)
    # Run the checker.
    res = checker.process(options.filenames)
    return res


if __name__ == '__main__':
    sys.exit(main(createDefaultConfig()))
