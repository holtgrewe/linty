Linty - C/C++ Style Checking with Python & libclang
===================================================

Linty is a style checker built upon Python and libclang.

Status
------

Linty is currently under heavy development.

There are some basic checks.  The main work currently is the indentation check
module.  There, we aim to provide fine-grained control over the style, compa-
rable with the available settings in the Eclipse CDT settings.

Contributions through merge requests are welcome.  However, consider that large
patch bombs hard hard to review.  It is recommended to contact the authors with
the intent of your changes.  This allows us to help you with any problems and
will speed up incorporations of patches.

Support for Objective-C and Microsoft SEH is currently not implemented, contri-
butions in this area are welcome, though.

Running
-------

Linty is a collection of checks and driver code to run them.  You write "confi-
guration" files for it that are actual Python programs.  For example, run the
seqan style checker:

    python conf/seqan/run.py -i ${include_dir} -s ${source_file}

Tests
-----

There is a comprehensive suite of tests, we use the [nosetests framework] [1]
for writing such tests.  There currently is a known issue with garbage
collection that occurs when running nosetests.  As a workaround, use the
`--nologcapture` option to nosestest:

    nosetests --nologcapture

  [1]: http://readthedocs.org/docs/nose/en/latest/

Authors
-------

* Manuel Holtgrewe

Acknowledgements
----------------

The indentation checks roughly follow the design of the Checkstyle tool for
checking Java source code.