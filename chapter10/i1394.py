
from .util import BitFormat
from .packet import Packet


class I1394F0(Packet):
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
                u1''')

        # Data Streaming
        elif self.packet_body_type == 1:
            self.item_size = self.packet.data_length - 4

        # General Purpose
        elif self.packet_body_type == 2:
            self.item_size = (
                (self.packet.data_length - 4) / self.transaction_count) - 8
            self.iph_format = BitFormat('u64 ipts')


class I1394F1(Packet):
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
