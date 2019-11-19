Chapter 10
==========

|StatusImage|_

This project seeks to provide a library and tools for dealing with `IRIG 106`_
Chapter 10 format files.

Dependencies
------------

* Python_ 2.7 or greater (tested on 2.7, 3.6 and 3.7)

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

Build the docs with::

    python setup.py build_docs

The docs will be built to build/sphinx/html

To Do
-----

* Implement standardized IPTS parsing.
* Strengthen test suite with more robust and varied data.
* Implement support for segmented Message data
* Implement TMATS XML parser
* Finish 1553 message parsing
* Implement TSPI/CTS parser


.. _Irig 106: http://irig106.org
.. _Python: http://python.org
.. |StatusImage| image:: https://dev.azure.com/atac-bham/pychapter10/_apis/build/status/atac-bham.pychapter10?branchName=master
.. _StatusImage: https://dev.azure.com/atac-bham/pychapter10/_build/latest?definitionId=4&branchName=master
