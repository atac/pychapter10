
from .packet import Packet
from .util import BitFormat


class ParallelF0(Packet):
    csdw_format = BitFormat('''
        u24 scan_number
        u8 type
    ''')
