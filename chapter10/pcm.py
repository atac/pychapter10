
from .util import compile_fmt
from .packet import Packet


class PCMF1(Packet):

    csdw_format = compile_fmt('''
        u18 sync_offset
        u4 mode
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
        if self.mode != 4:
            self.item_label = 'PCM Frame'
            self.item_size = 12  # Two words sync, four data.
            iph_format = '''
                u64 ipts
                p12
                u4 lock_status'''

            # Extra IPH word in 32 bit alignment.
            if self.iph and self.alignment:
                iph_format += '\np16'

            self.iph_format = compile_fmt(iph_format)
