
PyChapter10
===========

|StatusImage|_
|CoverageImage|
|DocsImage|_

PyChapter10 is an open source pure Python library for reading and writing IRIG 106 
Chapter 10 (now 11) files. Tested on all 3 major platforms with Python 3.6+.

Installation
------------

To install the library run::

    python setup.py install

To install offline from "full" zip, first install bitstruct with pip as in::

    pip install deps/bitstructXX.tar.gz

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

The generated HTML will be in docs/html

.. _Python: http://python.org
.. |StatusImage| image:: https://img.shields.io/azure-devops/build/atac-bham/7e6b2ae2-5609-49c9-9ded-f108e80d8949/7
.. _StatusImage: https://dev.azure.com/atac-bham/pychapter10/_build/latest?definitionId=7&branchName=master
.. |DocsImage| image:: https://readthedocs.org/projects/pychapter10/badge/?version=latest
.. _DocsImage: https://pychapter10.readthedocs.io/en/latest/?badge=latest
.. |CoverageImage| image:: https://img.shields.io/azure-devops/coverage/atac-bham/pychapter10/7
