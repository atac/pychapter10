
from .base import IterativeBase


class I1394(IterativeBase):
    item_label = 'IEEE-1394 Transaction'

    def parse(self):
        if self.format > 1:
            raise NotImplementedError('IEEE-1394 format %s is reserved!'
                                      % self.format)

        if self.format == 0:
            self.csdw_format = ('=I', ((
                ('pbt', 3),  # Packet Body Type
                ('sy', 4),   # Synchronization Code
                (None, 9),
                ('tc', 16),  # Transaction Count
            ),),)
            self.pbt = int((self.csdw >> 29) & 0b111)
            self.sy = int((self.csdw >> 25) & 0xf)
            self.tc = int(self.csdw & 0xffff)

            self.parse_csdw()

            # Bus Status
            if self.pbt == 0:
                self.iph_format = ('=I', (('reset', 1),),)

            # Data Streaming
            elif self.pbt == 1:
                self.item_size = self.packet.data_length - 4

            # General Purpose
            elif self.pbt == 2:
                self.item_size = ((self.packet.data_length - 4) / self.tc) - 8
                self.iph_format = ('=Q', ('ipts',),)

            self.parse_data()

        elif self.format == 1:
            self.csdw_format = ('=xxH', ('ipc',))  # Intra Packet Count
            self.iph_format = ('=QHH', ('ipts', (
                ('status', 8),
                ('speed', 4),
                ('trfovf', 2),
                ('lbo', 1),
                (None, 1),
                ('length', 16),
            ),),)

            IterativeBase.parse(self)
