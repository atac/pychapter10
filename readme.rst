
Chapter 10
==========

This project seeks to provide a library and tools for dealing with IRIG 106
Chapter 10 format files.

Dependencies
------------

Optional dependencies have explanations given.

* Python 2.7 or greater
* Docopt
* PySide (for native GUI applications)
* pytest and Mock (for test suite)
* cx_Freeze (for building binary executables)

Installation
------------

To install the library run::
After installing pip (http://pip-installer.org) run::

    python setup.py install_lib

To automatically install dependencies using pip (http://pip-installer.org) use::

    pip install -r requirements.txt

Building Binary Executables
---------------------------

If you also have cx_Freeze installed you can run::

    python setup.py build

and generate standalone binary executables for your platform.
