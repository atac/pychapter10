To Do
=====

General
-------

* Confirm 0xffff masks are correct

By File
-------

* datatypes
    * computer.py - Finish formats 2 and 3
    * time.py - Add time word parsing
    * ms1553.py - Finish message parsing
    * analog.py - Finish sample parsing (no data to test with)
    * ethernet.py - Implement format 1
    * Implement TSPI/CTS parser

* scripts
    * c10_check.py - Validator
    * c10_reindex.py - Walk a chapter 10 file and build a new index
    * video.py
        * Finish cleaning up UI.
        * Loading dialog should update and not freeze UI
        * Make cross-platform (unix)

* tests - Better coverage for datatypes and top-level package