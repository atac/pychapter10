
from .util import BitFormat
from . import packet


__all__ = ('ImageF0', 'ImageF1', 'ImageF2')


class ImageMessage:

    def __repr__(self):
        return '<Image Segment>'


class ImageF0(packet.Packet):
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
    """

    csdw_format = BitFormat('''
        u27 length
        u1 iph
        u3 sum
        u3 parts''')

    class Message(packet.Message, ImageMessage):
        """
        .. py:attribute:: ipts

            If IPH is true (see above), containts intra-packet timestamp
        """

    def __init__(self, *args, **kwargs):
        packet.Packet.__init__(self, *args, **kwargs)

        if self.iph:
            self.Message.FORMAT = BitFormat('u64 ipts')


class ImageF1(packet.Packet):
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
    """

    csdw_format = BitFormat('''
        p23
        u4 format
        u1 iph
        u2 sum
        u2 parts''')

    class Message(packet.Message, ImageMessage):
        """
        .. py:attribute:: ipts

            If IPH is true (see above), containts intra-packet timestamp

        .. py:attribute:: length

            Length of image or segment (bytes)
        """

    def __init__(self, *args, **kwargs):
        fmt = ''
        if self.iph:
            fmt = 'u64 ipts\n'
        self.Message.FORMAT = BitFormat(fmt + 'u32 length')


class ImageF2(packet.Packet):
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
    """

    csdw_format = BitFormat('''
        p21
        u6 format
        u1 iph
        u2 sum
        u2 parts''')

    class Message(packet.Message, ImageMessage):
        """
        .. py:attribute:: ipts

            If IPH is true (see above), containts intra-packet timestamp

        .. py:attribute:: length

            Length of image or segment (bytes)
        """

    def __init__(self, *args, **kwargs):
        fmt = ''
        if self.iph:
            fmt = 'u64 ipts\n'
        self.Message.FORMAT = BitFormat(fmt + 'u32 length')
