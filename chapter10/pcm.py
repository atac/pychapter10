
from .util import BitFormat
from . import packet


class PCMF1(packet.Packet):
    """IRIG 106 Chapter 4/8 PCM data.

    .. py:attribute:: sync_offset

        Offset into the major frame for the first data word in the packet. Not
        applicable for packed or throughput modes.

    .. py:attribute:: alignment

        Indicates 32 bit alignment if 1 or 16 bit by default.

    .. py:attribute:: throughput

        Indicates throughput mode (which would make most state flags
        unapplicable)

    .. py:attribute:: packed

        Indicates presence of packed data.

    .. py:attribute:: unpacked

        Indicates presense of unpacked data.

    .. py:attribute:: major_frame_status

        Combination major frame check flag and major frame lock

    .. py:attribute:: minor_frame_status

        Combination minor frame check flag and minor frame lock

    .. py:attribute:: minor_frame_indicator

        Indicates if the first data word in the packjet is the beginning of a
        minor frame.

    .. py:attribute:: major_frame_indicator

        Indicates if the first data word in the packet is the beginning of a
        major frame.

    .. py:attribute:: iph

        Indicates presence of Intra-Packet Header (IPTS and IPDH)
    """

    csdw_format = BitFormat('''
        u18 sync_offset
        u1 alignment
        u1 throughput
        u1 packed
        u1 unpacked
        p2
        u2 major_frame_status
        u2 minor_frame_status
        u1 minor_frame_indicator
        u1 major_frame_indicator
        u1 iph
        p1''')

    class Message(packet.Message):
        """
        .. py:attribute:: ipts

            Provided if IPH is true (see above).

        .. py:attribute:: lock_status
        """

        length = 12  # Two words sync, four data.

        def __repr__(self):
            return '<PCM Frame>'

    def __init__(self, *args, **kwargs):
        packet.Packet.__init__(self, *args, **kwargs)

        # Throughput basically means we don't need to do anything.
        if self.throughput:
            self.Message = None

        else:
            fmt = '''
                u64 ipts
                p12
                u4 lock_status'''

            # Extra IPH word in 32 bit alignment.
            if self.iph and self.alignment:
                fmt += '\np16'

            self.Message.FORMAT = BitFormat(fmt)
