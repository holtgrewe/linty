#!/usr/bin/env python
"""Assorted stuff."""

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@fu-berlin.de>'

import os

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
        return true


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


class Checker(object):
    def __init__(self, options, config):
        self.options = options
        self.config = config
        self.error_count = 0
        self.checks = []
        self.listeners = []
        self.filters = FilterSet()
        self.file_reader = CachingFileReader()
        self._interpretConfig()

    def _interpretConfig(self):
        self.checks = self.config

    def process(self, files):
        """Process all given files and return the error count."""
        # Startup.
        self._fireAuditStarted()
        for check in self.checks:
            check.beginProcessing()

        # Process all given files.
        for filename in files:
            messages = set()
            self._fireFileStarted(filename)
            fpath, fcontent, flines = self.file_reader.readFile(filename)
            for check in self.checks:
                messages.update(check.process(fpath, fcontent, flines))
            self._fireErrors(filename, messages)
            self._fireFileFinished(filename)

        # Shutdown.
        for check in self.checks:
            check.finishProcessing()
        self._fireAuditFinished()
        return self.error_count

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

    def _fireErrors(self, filename, error_msgs):
        # TODO(holtgrew): Strip filename?
        for msg in error_msgs:
            ae = AuditEvent(self, filename)
            if self.filters.accept(ae):
                for l in self.listeners:
                    l.addError(ae)
