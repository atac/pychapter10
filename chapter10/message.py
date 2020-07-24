
from .util import compile_fmt
from .packet import Packet


class Message(Packet):

    csdw_format = compile_fmt('''
        u16 count
        u2 packet_type
        p14''')

    iph_format = compile_fmt('''
        u64 ipts
        u16 length
        u14 subchannel
        u1 format_error
        u1 data_error''')
    item_label = 'Message Data'

    def parse(self):
        if self._format != 0:
            raise NotImplementedError('Message format %s is reserved!'
                                      % self._format)

        Packet.parse(self)
