
Base Types
==========

Specifying Formats
------------------

Formats are specified as a pair of (struct_format, names) where
"struct_format" is a struct format string (see the builtin struct
module), and "names" is a list of attribute names for the values to be assigned
to. In more advanced cases, bit-level attributes can be specified by another
layer as seen with 1553 format one::

    self.iph_format = (
        '=QHHH', (
            'rtc', (
                (None, 2),
                ('bus', 1),
                ('me', 1),
                ('rt2rt', 1),
                ('fe', 1),
                ('timeout', 1),
                (None, 3),
                ('le', 1),
                ('se', 1),
                ('we', 1),
                (None, 3),
            ),
            'gap_time',
            'length'))

In this case, we have 3 simple fields (rtc, gap_time, length) and a number of
bit-level fields specified in a sequence of (name, bit_size).

.. py:class:: chapter10.datatypes.base.Base(packet)
    
    Base object for packet data. Subclasses should override the csdw_format
    and data_format variables as well as the parse method for their
    specific types.

    :param Packet packet: The parent Packet object.

    .. py:attribute:: csdw_format = ('=I', None)

        Format for the Channel Specific Data Word (CSDW). Overridden in
        subclasses.

    .. py:attribute:: data_format = None

        Format for data messages. Left as None if handled manually by the parse
        method. Overridden in subclasses as needed.

    .. py:attribute:: packet

    .. py:attribute:: pos

        Byte-offset in the file object to the start of the packet CSDW.

    .. py:method:: parse()

        Parse CSDW and data.

    .. py:method:: parse_csdw()
    .. py:method:: parse_data()

.. py:class:: chapter10.datatypes.base.IterativeBase

    Iterable base class for data types containing multiple messages.

    .. py:attribute:: item_label = None

        Human-readable label for messages.

    .. py:attribute:: iph_format = None

        Format for Intra-Packet Headers (IPH)

.. py:class:: chapter10.datatypes.base.Item(data, [label='Packet Data', item_format=None, **kwargs])

    Base class for individual messages.

    :param bytes data: Message content.
    :param str label: Human readable message label.
    :param item_format: Optional format info for specific attributes in data.
    :param dict kwargs: Additional kwargs become message attributes.

    .. py:method:: pack([format=None])

        Pack the message back into its binary form.

        :param format: Optional format  for attributes to be re-packed into
        binary.
        :returns: bytes
