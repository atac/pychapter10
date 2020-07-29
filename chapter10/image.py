
from .util import BitFormat
from .packet import Packet


class Image(Packet):
    item_label = 'Image Segment'

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        if self.iph:
            self.iph_format = 'u64 ipts\n'


class ImageF0(Image):
    csdw_format = BitFormat('''
        u27 segment_length
        u1 iph
        u3 sum
        u3 parts''')

    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)

        self.item_length = self.segment_length
        self.iph_format = BitFormat(self.iph_format)


class ImageF1(Image):
    csdw_format = BitFormat('''
        p23
        u4 format
        u1 iph
        u2 sum
        u2 parts''')

    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)
        self.iph_format = BitFormat(self.iph_format + 'u32 length')


class ImageF2(Image):
    csdw_format = BitFormat('''
        p21
        u6 format
        u1 iph
        u2 sum
        u2 parts''')

    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)
        self.iph_format = BitFormat(self.iph_format + 'u32 length')
