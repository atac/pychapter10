
.. py:module:: chapter10
    :synopsis: Pure-python library for parsing Chapter 10 data. 

API Reference
=============

.. toctree::
    :maxdepth: 1
    :caption: Submodules:

    datatypes/index

.. py:class:: chapter10.C10(f, lazy=False, packet=Packet)

    Top-level Chapter10 object. Contains chapter 10 data from string or file.
    Roughly answers to a list (iterable technically) of packets.

    :param f: A file-like object or a filename string.
    :type f: file-like or str
    :param bool lazy: Specify whether to lazy-load packet contents.
    :param type packet: Class to use for parsing packets. Defaults to Packet.

    .. py:attribute:: file
        
        The actual file object containing the packet data.

    .. py:attribute:: lazy

        The value of the lazy parameter

    .. py:attribute:: packet

        The value of the packet parameter

    .. py:classmethod:: from_string
        
        :param str s: The string/bytes containing the packet data.
        :returns: C10

        Create a C10 object from a string.

    .. py:method:: close

.. py:class:: chapter10.Packet(file, lazy=False)

    Reads a packet header and associates a type-specific parser.
    Packets may be pickled, and can also be converted back to bytes with the
    builtin bytes(packet) function. If the datatype contains a number of
    messages, the packet object may be iterated on (returning individual
    messages).

    :param file file: The file object to read from.
    :param bool lazy: Whether to lazily load packet body.

    .. py:attribute:: pos
        
        Byte-offset of packet start.

    .. py:attribute:: sync_pattern
    .. py:attribute:: channel_id
    .. py:attribute:: packet_length
    .. py:attribute:: data_length
    .. py:attribute:: header_version
    .. py:attribute:: sequence_number
    .. py:attribute:: flags
    .. py:attribute:: data_type
    .. py:attribute:: rtc
    .. py:attribute:: ipts_source
    .. py:attribute:: rtc_sync_error
    .. py:attribute:: data_overflow_error
    .. py:attribute:: rtc
    .. py:attribute:: header_checksum
    .. py:attribute:: secondary_format

    .. py:classmethod:: from_string(s, lazy=False)
        
        Create a packet from bytes/string.

        :param str s: Source bytes/string.
        :param bool lazy: Lazy load packet body.
        :returns: Packet

    .. py:method:: get_errors()
        
        Validate the packet via checksums and testing for in-bounds fields.

        :returns: Exception

    .. py:method:: check

        Same as get_errors, but returns a boolean.

        :returns: bool
