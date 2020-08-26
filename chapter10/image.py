
from .util import BitFormat
from .packet import Packet


__all__ = ('ImageF0', 'ImageF1', 'ImageF2')


class Image(Packet):
    """Generic Image superclass."""

    item_label = 'Image Segment'

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        if self.iph:
            self.iph_format = 'u64 ipts\n'


class ImageF0(Image):
    """Image data

    .. py:attribute:: segment_length
    .. py:attribute:: iph
    .. py:attribute:: sum

        * 0 - Less than one complete image
        * 1 - One complete image
        * 2 - Multiple complete images
        * 3 - Multiple incomplete images

    .. py:attribute:: parts

        Indicates which piece[s] are of the frame are contained in the packet:

    **Message Format**

    .. py:attribute:: ipts

        If IPH is true (see above), containts intra-packet timestamp
    """

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
    """Still imagery

    .. py:attribute:: format

        * 0 - MIL-STD-2500 National Imagery Transmission Format
        * 1 - JPEG File Interchange Format
        * 2 - JPEG 2000 (ISO/IEC 154444-1)
        * 3 - Portable Network Graphics Format (PNG)

    .. py:attribute:: iph
    .. py:attribute:: sum

        * 0 - Contains less than one complete image
        * 1 - Contains one complete image
        * 2 - Contains multiple complete images
        * 3 - Contains multiple incomplete messages

    .. py:attribute:: parts

        * 0 - Doesn't contain first or last segment of the image
        * 1 - Contains first segment of image
        * 2 - Contains multiple complete messages
        * 3 - Contains both first and last segment of image

    **Message Format**

    .. py:attribute:: ipts

        If IPH is true (see above), containts intra-packet timestamp

    .. py:attribute:: length

        Length of image or segment (bytes)
    """

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
    """Dynamic Imagery

    .. py:attribute:: format

        Refer to chapter 10 standard

    .. py:attribute:: iph
    .. py:attribute:: sum

        * 0 - Contains less than one complete image (segment)
        * 1 - Contains one complete image
        * 2 - Contains multiple complete images

    .. py:attribute:: parts

        * 0 - Doesn't contain first or last segment of the image
        * 1 - Contains first segment of image
        * 2 - Contains last segment of image

    **Message Format**

    .. py:attribute:: ipts

        If IPH is true (see above), containts intra-packet timestamp

    .. py:attribute:: length

        Image segment length (bytes)
    """

    csdw_format = BitFormat('''
        p21
        u6 format
        u1 iph
        u2 sum
        u2 parts''')

    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)
        self.iph_format = BitFormat(self.iph_format + 'u32 length')
