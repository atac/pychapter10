
from .packet import Packet
from .util import BitFormat


class ParallelF0(Packet):
    """
    .. py:attribute:: scan_number

        If present contains the scan number of the first scan (for DCRsi data)

    .. py:attribute:: type

        If between 0x10 and 0x80 contains the number of bits of recorded data
    """

    csdw_format = BitFormat('''
        u24 scan_number
        u8 type
    ''')
