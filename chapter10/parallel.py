
from .packet import Packet
from .util import compile_fmt


class ParallelF0(Packet):
    csdw_format = compile_fmt('''
        u24 scan_number
        u8 type
    ''')
