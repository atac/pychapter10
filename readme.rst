Chapter 10
==========

|StatusImage|_

This project seeks to provide a library and tools for dealing with `IRIG 106`_
Chapter 10 format files.

Dependencies
------------

* Python_ 2.7 or greater (tested on 2.7 and 3.5)
* pytest_ and Mock_ (for test suite)

Installation
------------

To install the library run::

    python setup.py install_lib

To automatically install required dependencies using pip_ use::

    pip install -r requirements.txt

Running Tests
-------------

To run the included test suite run::

    py.test

Or, if you have tox_ installed you can use it instead::

    tox

This will run the test suite against both Python 2.7 and 3.5 if they are
installed.

To Do
-----

General
.......

* Implement standardized IPTS parsing.
* Strengthen test suite with more robust and varied data.
* Packet/file generation
* Packet/file validation

Data Types (/datatypes)
.......................

* message.py - Implement support for segmented messages
* computer.py - Implement TMATS XML parser
* ms1553.py - Finish message parsing
* Implement TSPI/CTS parser


.. _pip: http://pip-installer.org
.. _Irig 106: http://irig106.org
.. _Python: http://python.org
.. _pytest: http://pytest.org
.. _Mock: http://www.voidspace.org.uk/python/mock/
.. _tox: http://tox.readthedocs.org/en/latest/
.. |StatusImage| image:: https://dev.azure.com/atac-bham/pychapter10/_apis/build/status/atac-bham.pychapter10?branchName=master
.. _StatusImage: https://dev.azure.com/atac-bham/pychapter10/_apis/build/status/atac-bham.pychapter10?branchName=master
