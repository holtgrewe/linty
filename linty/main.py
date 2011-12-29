#!/usr/bin/env python
"""Assorted stuff."""

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@fu-berlin.de>'

import logging
import os
import os.path

import clang.cindex as ci

import violations as lv


class AuditEvent(object):
    def __init__(self, checker, filename=None):
        self.checker = checker
        self.filename = filename


class AuditListener(object):
    def addError(self, audit_event):
        pass
    def addException(self, audit_event):
        pass
    def auditFinished(self, audit_event):
        pass
    def auditStarted(self, audit_event):
        pass
    def fileFinished(self, audit_event):
        pass
    def fileStarted(self, audit_event):
        pass


class FilterSet(object):
    def __init__(self):
        pass

    def accept(self, audit_event):
        # TODO(holtgrew): Write me
        return True


class CachingFileReader(object):
    """Provide cached access to files."""

    def __init__(self):
        self._cache = {}

    def readFile(self, path):
        """Reads file at path and returns (npath, contents, lines).

        npath is the normalized absolute path to path.  This method provides
        cached access to files.  It normalizes the path name to keep duplicates
        low.  The lines do not contain line breaks, contents is the verbatim
        file content.
        """
        path = os.path.abspath(path)
        if not self._cache.has_key(path):
            with open(path, 'rb') as f:
                fcontents = f.read()
                flines = [x for x in fcontents.splitlines()]
            self._cache[path] = (path, fcontents, flines)
        return self._cache[path]


def _hasFileLocation(node):
    """Return True if node has a file lcoation."""
    if hasattr(node, '_has_file_location'):
        return node._has_file_location
    if not hasattr(node, 'location'):
        node._has_file_location = False
        return False
    if not hasattr(node.location, 'file'):
        node._has_file_location = False
        return False
    if not node.location.file:
        node._has_file_location = False
        return False
    if not hasattr(node.location.file, 'name'):
        node._has_file_location = False
        return False
    if not node.location.file.name:
        node._has_file_location = False
        return False
    node._has_file_location = True
    return True


class VisitAllowedFilter(object):
    """A lot of things are combined here, maybe split out into multiple classes?"""
    def __init__(self, include_dirs):
        self.include_dirs = [os.path.abspath(x) for x in include_dirs]
        self.cache = {}
        self.blocked_files = set()

    def nodeAllowed(self, node):
        # Visit if translation unit.
        if node.kind == ci.CursorKind.TRANSLATION_UNIT:
            return True
        # Don't visit if it has no location (built-in).
        if not _hasFileLocation(node):
            logging.debug('Skipping %s because there is no file location.', node.displayname)
            return False
        return self.fileAllowed(node.location.file.name)

    def fileAllowed(self, filename):
        # Try to hit cache.
        if self.cache.has_key(filename):
            logging.debug('fileAllowed(%s) ? hit cache -> %s',
                          filename, self.cache[filename])
            return self.cache[filename]
        # Check whether the file is blocked.
        if filename in self.blocked_files:
            # print 'Blocked', node.location.file.name
            logging.debug('fileAllowed(%s) ? -> blocked',
                          filename, self.cache[filename])
            self.cache[filename] = False
            return False
        # Check whether node's location is below the include directories.  It is
        # only visited if this is the case.
        filename = os.path.abspath(filename)
        result = False
        for x in self.include_dirs:
            if filename.startswith(x):
                # print filename, x
                result = True
                break
        logging.debug('fileAllowed(%s) ? -> %s', filename, {True: 'YES', False: 'NO'}[result])
        self.cache[filename] = result  # Save in cache.
        return result

    def seenToBlocked(self, seen_files):
        """Move seen files to blocked files."""
        self.blocked_files |= seen_files


class AstWalker(object):
    def __init__(self, translation_unit, ast_checks, include_dirs):
        self.translation_unit = translation_unit
        self.ast_checks = ast_checks
        self.include_dirs = include_dirs
        self.filter = VisitAllowedFilter(include_dirs)
        self.seen_files = set()

    def run(self):
        for check in self.ast_checks:
            check.beginTree(self.translation_unit.cursor)
        self._recurse(self.translation_unit.cursor)
        for check in self.ast_checks:
            check.endTree(self.translation_unit.cursor)
        self.filter.seenToBlocked(self.seen_files)

    def _recurse(self, node):
        if _hasFileLocation(node):
            self.seen_files.add(node.location.file.name)
        if not self.filter.nodeAllowed(node):
            logging.debug('AstWalker: Not allowed: %s', node)
            return False  # We did not visit this node.
        logging.debug('AstWalker: Candidate %s', node)
        for check in self.ast_checks:
            check.enterNode(node)
        for child in node.get_children():
            self._recurse(child)
        for check in self.ast_checks:
            check.exitNode(node)
        return True  # Visit successful!


class Checker(object):
    def __init__(self, options, ast_checks, file_checks):
        self.options = options
        self.ast_checks = ast_checks
        self.file_checks = file_checks
        self.listeners = []
        self.filters = FilterSet()
        self.file_reader = CachingFileReader()
        self.seen_files = set()

    def process(self, files):
        """Process all given files and return the error count."""
        # Startup.
        #print 'Processing files %s' % files
        self._fireAuditStarted()
        for check in self.ast_checks + self.file_checks:
            check.setFileReader(self.file_reader)
            check.beginProcessing()
        messages = set()

        # Process all given files.
        for filename in files:
            # Perform AST walking based checks.
            self._processAstWalk(filename)

        # Run simpler ("text only") checks on all seen files.
        filter_for_simple = VisitAllowedFilter(self.options.include_dirs)
        for filename in self.seen_files:
            if not filter_for_simple.fileAllowed(filename):
                logging.debug('No check for %s', filename)
                continue
            logging.debug('Simple checks on %s', filename)
            self._processSimpleChecks(filename)

        # Shutdown.
        for check in self.ast_checks + self.file_checks:
            check.finishProcessing()
        self._fireAuditFinished()

        # Print violations.
        vs = set()
        for check in self.ast_checks + self.file_checks:
            vs.update(check.violations)
        logging.info('VIOLATIONS')
        printer = lv.ViolationPrinter(self.file_reader, self.options.ignore_nolint, self.options.show_source, self.options.ignore_rules)
        printer.show(vs)
        return int(len(vs) > 0)

    def _processAstWalk(self, filename):
        # Create libclang index for AST access.
        logging.info('Building index for %s.', filename)
        index = ci.Index.create()
        args = ['-I%s' % s for s in self.options.include_dirs]
        # TODO(holtgrew): Make C++11 support configurable.
        args += ['--std=c++11']
        translation_unit = index.parse(filename, args=args)
        logging.info('Translation unit: %s', translation_unit.spelling)

        # Run AST walk based checks.
        logging.debug('AST Walk on %s, checks: %s', filename, self.ast_checks)
        ast_walker = AstWalker(translation_unit, self.ast_checks, self.options.include_dirs)
        ast_walker.run()
        logging.debug('AST Walk DONE on %s', filename)
        self.seen_files |= ast_walker.seen_files

    def _processSimpleChecks(self, filename):
        self._fireFileStarted(filename)
        fpath, fcontent, flines = self.file_reader.readFile(filename)
        for check in self.file_checks:
            check.process(fpath, fcontent, flines)
        self._fireFileFinished(filename)

    def _fireAuditStarted(self):
        ae = AuditEvent(self)
        for l in self.listeners:
            l.auditStarted(ae)

    def _fireAuditFinished(self):
        ae = AuditEvent(self)
        for l in self.listeners:
            l.auditFinished(ae)

    def _fireFileStarted(self, filename):
        # TODO(holtgrew): Strip filename?
        ae = AuditEvent(self, filename)
        for l in self.listeners:
            l.fileStarted(ae)

    def _fireFileFinished(self, filename):
        # TODO(holtgrew): Strip filename?
        ae = AuditEvent(self, filename)
        for l in self.listeners:
            l.fileFinished(ae)

    ## def _fireErrors(self, filename, error_msgs):
    ##     # TODO(holtgrew): Strip filename?
    ##     for msg in error_msgs:
    ##         ae = AuditEvent(self, filename)
    ##         if self.filters.accept(ae):
    ##             for l in self.listeners:
    ##                 l.addError(ae)
