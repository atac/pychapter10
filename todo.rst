
To Do
=====

General
-------

* Replace usage of datatypes.base.Data with actual values.
* Intra-packet elements should link together (ie. related timestamp, IPH, and
  data)

Data Types (/datatypes)
-----------------------

* computer.py - Implement TMATS XML parser
* ms1553.py - Finish message parsing
* time.py - Add time word parsing
* Implement TSPI/CTS parser

Scripts (/scripts)
------------------

* c10_check.py - Validator
* c10_reindex.py - Walk a chapter 10 file and build a new index
* video.py - New file handling

Testing (data needed)
---------------------

* Analog
* Discrete
* Ethernet format 1
* IEEE-1394
