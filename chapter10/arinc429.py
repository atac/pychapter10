
from .util import BitFormat
from .packet import Packet


class ARINC429F0(Packet):
    csdw_format = BitFormat('''
        u16 count
        p16''')
    iph_format = BitFormat('''
        u20 gap_time
        p1
        u1 bus_speed
        u1 parity_error
        u1 format_error
        u8 bus''', '22')
    item_size = 4
    item_label = 'ARINC-429 Data Word'
