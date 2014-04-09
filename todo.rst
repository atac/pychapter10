
To Do
=====

General
-------

* Replace usage of datatypes.base.Data with actual values.
* Python 3 compatibility
* Intra-packet elements should link together (ie. related timestamp, IPH, and
  data)

Data Types (/datatypes)
-----------------------

* analog.py - Finish sample parsing (no data to test with)
* computer.py - Implement TMATS XML parser
* discrete.py - Needs more testing (no data on hand)
* ethernet.py - Test format 1 implementation (need data)
* i1394 - More testing (need data)
* ms1553.py - Finish message parsing
* time.py - Add time word parsing
* Implement TSPI/CTS parser

Scripts (/scripts)
------------------

* c10_check.py - Validator
* c10_reindex.py - Walk a chapter 10 file and build a new index
* video.py - New file handling

Tests (/tests)
--------------

Better coverage for datatypes and top-level package
