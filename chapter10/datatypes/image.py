
from .base import IterativeBase


class Image(IterativeBase):
    item_label = 'Image Segment'

    def parse_csdw(self):
        self.csdw_format[1][0] = tuple(self.csdw_format[1][0])
        self.csdw_format[1] = tuple(self.csdw_format[1])
        IterativeBase.parse_csdw(self)

    def parse(self):
        self.csdw_format = ['=I', [[
            ('parts', 2),
            ('sum', 2),
            ('iph', 1),
        ]]]

        IterativeBase.parse(self)

        if self.format > 2:
            raise NotImplementedError('Image format %s is reserved!'
                                      % self.format)

        if self.format == 0:
            self.csdw_format[1][0].append(('length', 27))

            self.parse_csdw()
            self.item_length = self.length

            if self.iph:
                self.iph_format = ('=Q', ('ipts',))

            self.parse_data()

        else:
            if self.format == 1:
                self.csdw_format[1][0] += [('fmt', 4), (None, 24)]
            elif self.format == 2:
                self.csdw_format[1][0] += [('fmt', 6), (None, 21)]

            self.iph_format = ('=QI', ('ipts', 'length'))

            IterativeBase.parse(self)
