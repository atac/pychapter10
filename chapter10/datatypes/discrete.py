
from .base import IterativeBase


class Discrete(IterativeBase):
    csdw_format = ('=I', ((
        (None, 24),
        ('length', 5),
        ('mode', 3),
    ),),)
    item_label = 'Discrete data'
    item_size = 4
    iph_format = ('=Q', ('intra_packet_time_stamp',))

    def parse(self):
        if self._format != 1:
            raise NotImplementedError('Discrete data format %s is reserved!'
                                      % self._format)

        IterativeBase.parse(self)
