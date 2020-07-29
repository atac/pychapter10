
from .util import BitFormat
from .packet import Packet


class PCMF1(Packet):

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

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        # Throughput basically means we don't need to do anything.
        if not self.throughput:
            self.item_label = 'PCM Frame'
            self.item_size = 12  # Two words sync, four data.
            iph_format = '''
                u64 ipts
                p12
                u4 lock_status'''

            # Extra IPH word in 32 bit alignment.
            if self.iph and self.alignment:
                iph_format += '\np16'

            self.iph_format = BitFormat(iph_format)
