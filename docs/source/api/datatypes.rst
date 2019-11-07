
.. py:module:: chapter10.datatypes
    :synopsis: Type-specific data parsing

Datatypes
=========

.. toctree::
    :maxdepth: 1

    base

Helper Functions
----------------

.. automodule:: chapter10.datatypes
    :members:

.. py:module:: chapter10.datatypes.analog

Analog (format 1)
-----------------

.. py:class:: chapter10.datatypes.Analog(IterativeBase)

    Contains multiple analog messages each with its own CSDW.

    .. py:attribute:: same
    
        Is the CSDW the same for all subchannels?

    .. py:attribute:: factor
    
        Sampling rate factor.

    .. py:attribute:: totchan
    
        Subchannel count.

    .. py:attribute:: subchan
    
        Subchannel ID.

    .. py:attribute:: length
    
        Sample length.

    .. py:attribute:: mode

        Alignment and packing mode.

.. py:module:: chapter10.datatypes.arinc429

Arinc 429 (format 0)
--------------------

.. py:class:: chapter10.datatypes.Arinc429(IterativeBase)

    Contains multiple ARINC 429 data words (4 bytes).

    .. py:attribute:: message_count

Message Attributes
++++++++++++++++++

* bus
* format_error
* parity_error
* bus_speed
* gap_time

Computer
--------

.. automodule:: chapter10.datatypes.computer
    :members:

Discrete
--------

.. automodule:: chapter10.datatypes.discrete
    :members:

Ethernet
--------

.. automodule:: chapter10.datatypes.ethernet
    :members:

I1394
-----

.. automodule:: chapter10.datatypes.i1394
    :members:

Image
-----

.. automodule:: chapter10.datatypes.image
    :members:

Message
-------

.. automodule:: chapter10.datatypes.message
    :members:

Mil-Std-1553
------------

.. automodule:: chapter10.datatypes.ms1553
    :members:

Parallel
--------

.. automodule:: chapter10.datatypes.parallel
    :members:

PCM
---

.. automodule:: chapter10.datatypes.pcm
    :members:

Time
----

.. automodule:: chapter10.datatypes.time
    :members:

UART
----

.. automodule:: chapter10.datatypes.uart
    :members:

Video
-----

.. automodule:: chapter10.datatypes.video
    :members:
