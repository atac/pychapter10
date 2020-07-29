
from .util import BitFormat
from .packet import Packet


class DiscreteF1(Packet):
    csdw_format = BitFormat('''
        u3 mode
        u5 length
        p24''')
    item_label = 'Discrete data'
    item_size = 4
    iph_format = BitFormat('u64 ipts')
