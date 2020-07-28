
from .util import compile_fmt
from .packet import Packet


class UARTF0(Packet):
    csdw_format = compile_fmt('''
        p31
        u1 iph''')
    item_label = 'UART Data'

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        iph_format = ''
        if self.iph:
            iph_format = 'u64 ipts'
        self.iph_format = compile_fmt(iph_format + '''
            u16 length
            u14 subchannel
            p1
            u1 parity_error''')
