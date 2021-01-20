
PyChapter10
===========

|StatusImage|_
|CoverageImage|
|DocsImage|_
|LicenseImage|
|PyPiVersion|_
|PythonVersion|

PyChapter10 is an open source pure Python library for reading and writing IRIG 106 
Chapter 10 (now 11) files. Tested on all 3 major platforms with Python 3.6+.

Installation
------------

Install the latest version with pip::

    pip install pychapter10

To install offline from "full" zip, install the included dependencies and the library with::

    pip install dependencies/* .

**Note:** you may also install cbitstruct (included in requirements.txt, see
below) for a performance improvement.

Basic Usage
-----------

PyChapter10 provides a pythonic API to read, write, and update Chapter 10 data.

.. code-block:: python

    from chapter10 import C10

    # Find all 1553 messages in a file
    for packet in C10('<filename>'):
        if packet.data_type == 0x19:
            for msg in packet:
                # do something with the message

Supported Datatypes
-------------------
====  ==================================================    =========
Type  Name                                                  Supported                      
====  ==================================================    =========
0x00  Computer-Generated F0 - User-Defined                  User-Defined
0x01  Computer-Generated F1 - Setup Record (TMATS)          Yes
0x02  Computer-Generated F2 - Recording Events              Yes
0x03  Computer-Generated F3 - Recording Index               Yes
0x04  Computer-Generated F4 - Streaming Config (TMATS)      No
0x09  PCM F1                                                Yes
0x11  Time Data F1                                          Yes 
0x12  Time Data F2                                          No
0x19  1553 F1                                               Yes
0x1A  1553 F2 - 16PP194                                     Yes
0x21  Analog F1                                             Yes
0x29  Discrete F1                                           Yes
0x30  Message F0                                            Yes
0x38  ARINC-429 F0                                          Yes
0x40  Video F0                                              Yes
0x41  Video F1                                              Yes
0x42  Video F2                                              Yes
0x43  Video F3                                              No
0x44  Video F4                                              No
0x48  Image F0                                              Yes (untested)
0x49  Image F1                                              Yes (untested)
0x4A  Image F2                                              Yes (untested)
0x50  UART F0                                               Yes
0x58  IEEE 1394 F0                                          Yes (untested)
0x59  IEEE 1394 F1                                          Yes (untested)
0x60  Parallel F0                                           Yes (untested)
0x68  Ethernet F0 - Ethernet Data                           Yes
0x69  Ethernet F1 - UDP Payload                             Yes
0x70  TSPI/CTS F0 - GPS NMEA-RTCM                           No
0x71  TSPI/CTS F1 - EAG ACMI                                No
0x72  TSPI/CTS F2 - ACTTS                                   No
0x78  Controller Area Network Bus                           No
0x79  Fibre Channel F0                                      No
0x7A  Fibre Channel F1                                      No
====  ==================================================    =========

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

**Note:** "Full" zip includes built documentation already.

Contributing
------------

See CONTRIBUTING_

.. _Python: http://python.org
.. |StatusImage| image:: https://img.shields.io/azure-devops/build/atac-bham/7e6b2ae2-5609-49c9-9ded-f108e80d8949/7
.. _StatusImage: https://dev.azure.com/atac-bham/pychapter10/_build/latest?definitionId=7&branchName=master
.. |DocsImage| image:: https://readthedocs.org/projects/pychapter10/badge/?version=latest
.. _DocsImage: https://pychapter10.readthedocs.io/en/latest/?badge=latest
.. |CoverageImage| image:: https://img.shields.io/azure-devops/coverage/atac-bham/pychapter10/7
.. |LicenseImage| image:: https://img.shields.io/github/license/atac/pychapter10
.. _PyPiVersion: https://pypi.org/project/pychapter10/
.. |PyPiVersion| image:: https://img.shields.io/pypi/v/pychapter10
.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/pychapter10
.. _CONTRIBUTING: CONTRIBUTING.rst
