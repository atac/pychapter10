
Chapter 10
==========

This project seeks to provide a library and tools for dealing with IRIG 106
Chapter 10 format files.

Dependencies
------------

Optional dependencies have explanations given.

* Python 2.7 or greater
* Docopt
* PyQt4 and mplayer.py (for video player)
* pytest and Mock (for test suite)
* cx_Freeze (for building binary executables)

Installation (using pip)
------------------------

After installing pip (http://pip-installer.org) run::

    pip install .

To automatically install dependencies use::

    pip install -r requirements.txt

Building Binary Executables
---------------------------

If you also have cx_Freeze installed you can run::

    python setup.py build

and generate standalone binary executables for your platform.
