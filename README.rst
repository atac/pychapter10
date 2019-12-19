
PyChapter10
===========

|StatusImage|_

PyChapter10 is an open source pure Python library for reading and writing IRIG 106 
Chapter 10 (now 11) files. Tested on all 3 major platforms and Python 2.7 and 3.6+.

Installation
------------

To install the library run::

    python setup.py install

Running Tests
-------------

To run the included test suite install dependencies with pip::

    pip install -r requirements.txt

Then run::

    pytest

Building the Documentation
--------------------------

After installing dependencies (or just "pip install sphinx") Build the docs with::

    python setup.py build_docs

The generated HTML will be in build/sphinx/html

To Do
-----

* Implement standardized IPTS parsing.
* Strengthen test suite with more robust and varied data.
* Implement support for segmented Message data
* Implement TMATS XML parser
* Finish 1553 message parsing
* Implement TSPI/CTS parser


.. _Python: http://python.org
.. |StatusImage| image:: https://dev.azure.com/atac-bham/pychapter10/_apis/build/status/atac-bham.pychapter10?branchName=master
.. _StatusImage: https://dev.azure.com/atac-bham/pychapter10/_build/latest?definitionId=4&branchName=master
