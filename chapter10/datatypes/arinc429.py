
from .base import IterativeBase


class ARINC429(IterativeBase):

    csdw_format = ('=I', ((
        (None, 16),
        ('msg_count', 16),
    ),),)
    iph_format = ('=I', ((
        ('bus', 8),
        ('fe', 1),        # Format error flag
        ('pe', 1),        # Parity error flag
        ('bs', 1),        # Bus speed (0 = low, 1 = high)
        (None, 1),
        ('gap_time', 20),
    ),),)
    item_size = 4
    item_label = 'ARINC-429 Data Word'

    def parse(self):
        if self.format > 0:
            raise NotImplementedError('ARINC-429 format %s is reserved!'
                                      % self.format)

        IterativeBase.parse(self)
