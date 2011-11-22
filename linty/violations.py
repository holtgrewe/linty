#!/usr/bin/env python
"""Code related to violations and suppressions."""

from __future__ import with_statement

import logging
import os
import os.path
import sys

import app as app


class LogViolationsMixin(object):
    """Mixin that adds logViolation() method.

    The including object must have a member violations that is a list.
    Violations will be logged as RuleViolation objects.
    """

    def logViolation(self, rule_id, node, msg):
        v = RuleViolation(rule_id, node.location.file.name,
                          node.location.line, node.location.column,
                          msg)
        self.violations.add(v)


class RuleViolation(object):
    def __init__(self, rule_id, file, line, column, msg):
        self.rule_id = rule_id
        self.file = file
        self.line = line
        self.column = column
        self.msg = msg
    
    def key(self):
        return (self.file, self.line, self.column, self.rule_id)

    def __hash__(self):
        return self.key().__hash__()

    def __eq__(self, other):
        return self.key() == other.key()

    def __cmp__(self, other):
        return cmp(self.key(), other.key())
    
    def __str__(self):
        msg = '[%s:%d/%d] %s : %s'
        return msg % ('/'.join(self.file.split('/')[-2:]), self.line, self.column,
                      self.rule_id, self.msg)


class NolintManager(object):
    """Manage the lines ending in '// nolint'."""

    def __init__(self):
        self.locations = {}

    def hasNolint(self, filename, lineno):
        filename = os.path.abspath(filename)
        # Ensure that the nolint lines are registered in self.locations[filename].
        if not self.locations.has_key(filename):
            line_set = set()
            with open(filename, 'rb') as f:
                line_no = 0
                for line in f:
                    line_no += 1
                    if line.strip().endswith('// nolint'):
                        ## print 'nolint', filename, line_no
                        line_set.add(line_no)
            self.locations[filename] = line_set
        # Query self.locations[filename].
        return lineno in self.locations[filename]


class ViolationPrinter(object):
    def __init__(self, file_reader, ignore_nolint, show_source, ignore_rules):
      self.nolints = NolintManager()
      self.file_reader = file_reader
      self.ignore_nolint = ignore_nolint
      self.show_source = show_source
      self.ignore_rules = set(ignore_rules)

    def show(self, vs):
        previous = None
        violation_count = 0
        skipped_count = 0
        for violation in sorted(vs):
            if violation.rule_id in self.ignore_rules:
                logging.debug('Skipping violation %s because rule is ignored.', violation)
                skipped_count += 1
                continue
            violation_count += 1
            if self.ignore_nolint or not self.nolints.hasNolint(violation.file, violation.line):
                print violation
                npath, fcontents, flines = self.file_reader.readFile(violation.file)
                line = flines[violation.line - 1]
                if self.show_source:
                    print line.rstrip()
                    print '%s^' % (' ' * (violation.column - 1))
                    print
            previous = violation
        print 'Displayed %d violations, skipped %d.' % (violation_count, skipped_count)

