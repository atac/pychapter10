
from .util import BitFormat
from .packet import Packet


class I1394F0(Packet):
    """
    .. py:attribute:: count
    .. py:attribute:: sync

        Synchronization code

    .. py:attribute:: packet_body_type

    **Message Format**

    .. py:attribute:: reset

        If packet type 0 (bus status) indicates if bus reset has occurred

    .. py:attribute:: ipts

        Present for packet type = 2 (general purpose)
    """

    item_label = 'IEEE-1394 Transaction'
    csdw_format = BitFormat('''
        u16 count
        p9
        u4 sync
        u3 packet_body_type''')

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        # Bus Status
        if self.packet_body_type == 0:
            self.iph_format = BitFormat('''
                p31
                u1 reset''')

        # Data Streaming
        elif self.packet_body_type == 1:
            self.item_size = self.packet.data_length - 4

        # General Purpose
        elif self.packet_body_type == 2:
            self.item_size = (
                (self.packet.data_length - 4) / self.transaction_count) - 8
            self.iph_format = BitFormat('u64 ipts')


class I1394F1(Packet):
    """IEEE 1394 Physical Layer

    .. py:attribute:: count

    **Message Format**

    .. py:attribute:: ipts
    .. py:attribute:: length

        Transfer length (bytes)

    .. py:attribute:: buffer_overflow
    .. py:attribute:: overflow_error

        * 0 - no overflow
        * 1 - transfer started correctly, but is longer than standard \
transfer length
        * 2 - previous transfer was a type 1 overflow, this transfer ended \
correctly
        * 3 - previous transfer was a type 1 overflow and this transfer did \
not end correctly
    .. py:attribute:: speed

        See chapter 10 standard

    .. py:attribute:: status
    """

    csdw_format = BitFormat('''
        u16 count
        p16''')
    iph_format = BitFormat('''
        u64 ipts
        u16 length
        p1
        u1 buffer_overflow
        u2 overflow_error
        u4 speed
        u8 status''')
