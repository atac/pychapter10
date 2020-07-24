
from ..util import compile_fmt
from .base import Base


class Image(Base):
    item_label = 'Image Segment'

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
            self.csdw_format = compile_fmt('''
                u27 length
                u1 iph
                u2 sum
                u2 parts''')

            self.parse_csdw()
            self.item_length = self.length

            if self.iph:
                self.iph_format = compile_fmt('u64 ipts')

            self.parse_data()

        else:
            if self._format == 1:
                self.csdw_format = compile_fmt('''
                    p23
                    u4 format
                    u1 iph
                    u2 sum
                    u2 parts''')
            elif self._format == 2:
                self.csdw_format = compile_fmt('''
                    p21
                    u6 format
                    u1 iph
                    u2 sum
                    u2 parts''')

            self.iph_format = compile_fmt('''
                u64 ipts
                u32 length''')

            Base.parse(self)
