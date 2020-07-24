
from .util import compile_fmt
from .packet import Packet


class UART(Packet):
    csdw_format = compile_fmt('''
        p31
        u1 iph''')
    item_label = 'UART Data'

    def parse(self):
        if self._format > 0:
            raise NotImplementedError('UART format %s is reserved!'
                                      % self._format)

        self.parse_csdw()

        iph_format = ''
        if self.iph:
            iph_format = 'u64 ipts'

        self.iph_format = compile_fmt(iph_format + '''
            u16 length
            u14 subchannel
            p1
            u1 parity_error''')

        self.parse_data()
