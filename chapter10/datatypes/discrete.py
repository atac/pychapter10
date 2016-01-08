
from .base import IterativeBase


class Discrete(IterativeBase):
    csdw_format = ('=I', ((
        (None, 24),
        ('length', 5),
        ('mode', 3),
    ),),)
    item_label = 'Discrete data'
    item_size = 4
    iph_format = ('=Q', ('ipts',))

    def parse(self):
        if self.format != 1:
            raise NotImplementedError('Discrete data format %s is reserved!'
                                      % self.format)

        IterativeBase.parse(self)
