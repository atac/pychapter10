
from .base import IterativeBase


class I1394(IterativeBase):
    item_label = 'IEEE-1394 Transaction'

    def parse(self):
        if self._format > 1:
            raise NotImplementedError('IEEE-1394 format %s is reserved!'
                                      % self._format)

        if self._format == 0:
            self.csdw_format = ('=I', ((
                ('packet_body_type', 3),
                ('sync_code', 4),
                (None, 9),
                ('transaction_count', 16),
            ),),)

            self.parse_csdw()

            # Bus Status
            if self.packet_body_type == 0:
                self.iph_format = ('=I', ((('reset', 1),),),)

            # Data Streaming
            elif self.packet_body_type == 1:
                self.item_size = self.packet.data_length - 4

            # General Purpose
            elif self.packet_body_type == 2:
                self.item_size = (
                    (self.packet.data_length - 4) / self.transaction_count) - 8
                self.iph_format = ('=Q', ('intra_packet_time_stamp',),)

            self.parse_data()

        elif self._format == 1:
            self.csdw_format = ('=xxH', ('intra_packet_count',))
            self.iph_format = ('=QHH', ('intra_packet_time_stamp', (
                ('status', 8),
                ('speed', 4),
                ('transfer_overflow_error', 2),
                ('local_buffer_overflow', 1),
                (None, 1),
                ('length', 16),
            ),),)

            IterativeBase.parse(self)
