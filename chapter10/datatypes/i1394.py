
from ..util import compile_fmt
from .base import IterativeBase


class I1394(IterativeBase):
    item_label = 'IEEE-1394 Transaction'

    def parse(self):
        if self._format > 1:
            raise NotImplementedError('IEEE-1394 format %s is reserved!'
                                      % self._format)

        if self._format == 0:
            self.csdw_format = compile_fmt('''
                u16 count
                p9
                u4 sync
                u3 packet_body_type''')

            self.parse_csdw()

            # Bus Status
            if self.packet_body_type == 0:
                self.iph_format = compile_fmt('''
                    p31
                    u1''')

            # Data Streaming
            elif self.packet_body_type == 1:
                self.item_size = self.packet.data_length - 4

            # General Purpose
            elif self.packet_body_type == 2:
                self.item_size = (
                    (self.packet.data_length - 4) / self.transaction_count) - 8
                self.iph_format = compile_fmt('u64 ipts')

            self.parse_data()

        elif self._format == 1:
            self.csdw_format = compile_fmt('''
                u16 count
                p16''')
            self.iph_format = compile_fmt('''
                u64 ipts
                u16 length
                p1
                u1 buffer_overflow
                u2 overflow_error
                u4 speed
                u8 status''')

            IterativeBase.parse(self)
