
from .util import BitFormat
from .packet import Packet


class MessageF0(Packet):
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
