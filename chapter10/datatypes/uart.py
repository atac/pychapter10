
from .base import IterativeBase


class UART(IterativeBase):
    csdw_format = ('=I', ((
        ('intra_packet_header', 1),
        (None, 31),
    ),),)
    iph_format = ['=I', [
        (('parity_error', 1),
         (None, 1),
         ('subchannel', 14),
         ('length', 16),),
    ]]
    item_label = 'UART Data'

    def _parse(self):
        if self._format > 0:
            raise NotImplementedError('UART format %s is reserved!'
                                      % self._format)

        self.parse_csdw()

        if self.intra_packet_header:
            self.iph_format[0].insert(1, 'Q')
            self.iph_format[1].insert(0, 'intra_packet_timestamp')

        self.parse_data()
