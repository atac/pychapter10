
from .util import BitFormat
from .packet import Packet


class MessageF0(Packet):
    """
    .. py:attribute:: count

        Segment number of packet (for non-zero packet_type) or a count of \
messages contained in the packet.

    .. py:attribute:: packet_type

        * 0 - One or more complete messages
        * 1 - Beginning of a long message
        * 2 - Last part of a long message
        * 3 - Middle part of a long message

    **Message Format**

    .. py:attribute:: ipts
    .. py:attribute:: length

        Message length (bytes)

    .. py:attribute:: subchannel
    .. py:attribute:: format_error
    .. py:attribute:: data_error
    """

    csdw_format = BitFormat('''
        u16 count
        u2 packet_type
        p14''')
    iph_format = BitFormat('''
        u64 ipts
        u16 length
        u14 subchannel
        u1 format_error
        u1 data_error''')
    item_label = 'Message Data'
