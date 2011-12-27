Linty - Style Checking with Python & libclang
=============================================

Linty is a style checker built upon Python and libclang.

Status
------

Linty is currently under heavy development.

Contributions through merge requests are welcome.  However, consider that large
patch bombs hard hard to review.  It is recommended to contact the authors with
the intent of your changes.  This allows us to help you with any problems and
will speed up incorporations of patches.

Running
-------

Linty is a collection of checks and driver code to run them.  You
write "configuration" files for it that are actual Python programs.
For example, run the seqan style checker:

    python conf/seqan/run.py -i ${include_dir} -s ${source_file}

Authors
-------

* Manuel Holtgrewe

Acknowledgements
----------------

The indentation checks roughly follow the design of the Checkstyle tool for
checking Java source code.
