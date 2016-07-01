
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
            ('intra_packet_header', 1),
        ]]]

        if self._format > 2:
            raise NotImplementedError('Image format %s is reserved!'
                                      % self._format)

        if self._format == 0:
            self.csdw_format[1][0].append(('length', 27))

            self.parse_csdw()
            self.item_length = self.length

            if self.intra_packet_header:
                self.iph_format = ('=Q', ('intra_packet_timestamp',))

            self.parse_data()

        else:
            if self._format == 1:
                self.csdw_format[1][0] += [('format', 4), (None, 24)]
            elif self._format == 2:
                self.csdw_format[1][0] += [('format', 6), (None, 21)]

            self.iph_format = ('=QI', ('intra_packet_timestamp', 'length'))

            IterativeBase.parse(self)
