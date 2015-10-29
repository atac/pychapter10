Chapter 10
==========

This project seeks to provide a library and tools for dealing with `IRIG 106`_
Chapter 10 format files.

Dependencies
------------

* Python_ 2.7 or greater (tested on 2.7 and 3.3)
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

Data Types (/datatypes)
.......................

* computer.py - Implement TMATS XML parser
* ms1553.py - Finish message parsing
* Implement TSPI/CTS parser


.. _pip: http://pip-installer.org
.. _Irig 106: http://irig106.org
.. _Python: http://python.org
.. _pytest: http://pytest.org
.. _Mock: http://www.voidspace.org.uk/python/mock/
.. _tox: http://tox.readthedocs.org/en/latest/
