#!/usr/bin/env python
"""The implementation of the linty checks.

This module contains the base class Check for all checks and the core
checks that are useful in many situations.
"""

from __future__ import with_statement

__author__ = 'Manuel Holtgrewe <manuel.holtgrewe@fu-berlin.de>'

import bisect
import sys
import re


class Check(object):
    """Base class for all checks."""

    def process(self, filename, fcontents, flines):
        # TODO(holtgrew): reset message collector?
        # Check file extension?
        res = []
        res += self.processFiltered(filename, fcontents, flines)
        return res
    
    def beginProcessing(self):
        pass
    def finishProcessing(self):
        pass


class HeaderCheck(Check):
    """Check the header of a file.

    You can either give the header lines as a string or load them from
    a file.
    """

    def __init__(self, path=None, lines=None):
        self.path = path
        self.lines = lines
        if self.path and self.lines:
            raise Exception('Cannot give both path and lines to HeaderCheck.')
        if not self.path and not self.lines:
            raise Exception('One of path and lines has to be given to HeaderCheck.')
        # Load expected header from path if given.
        if self.path:
            with open(self.path, 'r') as f:
                self.lines = f.read().splitlines()

    def processFiltered(self, path, fcontents, flines):
        if len(flines) < len(self.lines):
            print >>sys.stderr, '%s: missing header.' % path
            return
        for i in range(0, len(self.lines)):
            line_is_good = self.checkLine(i, self.lines[i], flines[i])
            if not line_is_good:
                print >>sys.stderr, '%s: Header invalid at line %i, stopping.' % (path, i)
        return []

    def checkLine(self, num, expected, actual):
        return expected == actual


class RegexpHeaderCheck(HeaderCheck):
    """Check the header of a file against regular expressions.

    Check that each line in the header matches a line in a list of
    regular expressions.  The regular expressions can also be read
    from a file.
    """

    def __init__(self, path=None, lines=None):
        super(RegexpHeaderCheck, self).__init__(path, lines)
        # Make all lines regular expression objects.
        self.lines = [re.compile(l) for l in self.lines]

    def checkLine(self, num, pattern, actual):
        return pattern.match(actual) != None


class OnlyUnixLineEndings(Check):
    """Check that a file does not contain Windows line endings."""

    def processFiltered(self, path, fcontents, files):
        for i, line in enumerate(fcontents.splitlines(True)):
            if line.endswith('\r\n'):
                print >>sys.stderr, '%s:%d: Ends with CRLF (Windows line ending).' % (path, i + 1)
        return []


class FileEndsWithNewlineCheck(Check):
    """Check that a file ends with a given newline.

    Example:

        FileEndsWithNewlineCheck('\n', '\r\n')
    """
    def __init__(self, *args):
        """Constructor.

        The parameters are the valid strings that are allowed as last
        characters in a file.
        """
        
        if not args:
            args = ['\n']
        self.allowed_newlines = args

    def processFiltered(self, path, fcontents, flines):
        for nl in self.allowed_newlines:
            if fcontents.endswith(nl):
                return []  # OK!
        print >> sys.stderr, '%s: Did not end with valid newline char.' % path
        return []


class NoTrailingWhitespaceCheck(Check):
    """Check that no line in a file has trailing whitespace."""

    def processFiltered(self, path, fcontents, flines):
        for i, line in enumerate(flines):
            if line != line.rstrip():
                print >>sys.stderr, '%s:%d has trailing whitespace.' % (path, i + 1)
        return []


class SourceFile(object):
    def __init__(self, name):
        self.name = name


class SourceLocation(object):
    def __init__(self, filename, line, column, offset):
        self.file = SourceFile(filename)
        self.line = line
        self.column = column
        self.offset = offset

    def __str__(self):
        return '%s:%d/%d (@%d)' % (self.file.name, self.line, self.column,
                                   self.offset)

    def __repr__(self):
        return str(self)


def enumerateComments(filename, fcontents, flines):
    # Build line break index.
    line_starts = [0]
    for line in flines:
        line_starts.append(line_starts[-1] + len(line))
    #print line_starts
    # Search for all comments.
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE)
    for match in re.finditer(pattern, fcontents):
        line_start = bisect.bisect(line_starts, match.start(0))
        line_end = bisect.bisect(line_starts, match.end(0) - 1)
        column_start = match.start(0) - line_starts[line_start - 1]
        column_end = match.end(0) - line_starts[line_end - 1]
        yield (SourceLocation(filename, line_start, column_start + 1, match.start(0)),
               SourceLocation(filename, line_end, column_end + 1, match.end(0)),
               match.group(0))


class TodoCommentChecker(Check):
    """Check TODO comments.

    TODO comments should look as follows.

        // TODO(holtgrew): This is a TODO comment.

    There should be exactly on space between // and TODO, no space before the
    (user) and no space after it, then one":", then exactly one space before
    the text.
    """

    def processFiltered(self, path, fcontents, flines):
        RE_TODO = r'^//(\s*)TODO(\(.+?\))?:?(\s|$)?'
        vs = []
        for cstart, cend, comment in enumerateComments(path, fcontents, flines):
            if comment.startswith('//'):
                # Check TODO comments.
                match = re.match(RE_TODO, comment)
                if match:
                    if len(match.group(1)) > 1:
                        print >>sys.stderr, '%s:%d:%d There should be exactly one space before TODO.' % (path, cstart.line, cstart.column)
                    if not match.group(2):
                        print >>sys.stderr, 'TODO comments should look like this: "// TODO(username): Text".' % (path, cstart.line, cstart.column)
                    if match.group(3) != ' ' and match.group(3) != '':
                        print >>sys.stderr, '"TODO (username):" should be followed by a space.' % (path, cstart.line, cstart.column)
        return []
