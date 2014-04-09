
Chapter 10
==========

This project seeks to provide a library and tools for dealing with `IRIG 106`_
Chapter 10 format files.

Dependencies
------------

Optional dependencies have explanations given.

* Python_ 2.7 or greater
* Docopt_
* PySide_ (for native GUI applications)
* pytest_ and Mock_ (for test suite)
* cx_Freeze_ (for building binary executables)

Installation
------------

To install the library run::

    python setup.py install_lib

To automatically install dependencies using pip_ use::

    pip install -r requirements.txt

Building Binary Executables
---------------------------

If you also have cx_Freeze_ installed you can run::

    python setup.py build

and generate standalone binary executables for your platform.


.. _PySide: http://qt-project.org/wiki/Category:LanguageBindings::PySide
.. _cx_Freeze: http://cx-freeze.sourceforge.net/index.html
.. _pip: http://pip-installer.org
.. _Irig 106: http://irig106.org
.. _Python: http://python.org
.. _Docopt: http://docopt.org
.. _pytest: http://pytest.org
.. _Mock: http://www.voidspace.org.uk/python/mock/
