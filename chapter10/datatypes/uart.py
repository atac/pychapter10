
from .base import IterativeBase


class UART(IterativeBase):
    csdw_format = ('=I', ((
        ('iph', 1),
        (None, 31),
    ),),)
    iph_format = ['=I', [
        (('pe', 1),
            ('subchannel', 14),
            ('length', 16),),
    ]]
    item_label = 'UART Data'

    def parse(self):
        if self.format > 0:
            raise NotImplementedError('UART format %s is reserved!'
                                      % self.format)

        self.parse_csdw()

        if self.iph:
            self.iph_format[0].insert(1, 'Q')
            self.iph_format[1].insert(0, 'ipts')

        self.parse_data()
