
from ..util import compile_fmt
from .base import IterativeBase


class PCM(IterativeBase):

    csdw_format = compile_fmt('''
        u18 sync_offset
        u1 unpacked
        u1 packed
        u1 throughput
        u1 alignment
        p2
        u2 major_frame_status
        u2 minor_frame_status
        u1 minor_frame_indicator
        u1 major_frame_indicator
        u1 iph
        p1''')
    item_label = 'PCM Frame'
    item_size = 12  # Two words sync, four data.

    def _parse(self):
        if self._format != 1:
            raise NotImplementedError(
                'PCM Format %s is reserved!' % self._format)

        self.parse_csdw()

        # Throughput basically means we don't need to do anything.
        if self.throughput:
            return

        # Figure out the correct IPH format based on CSDW.
        iph_format = '''
            u64 ipts
            p12
            u4 lock_status'''

        # Extra IPH word in 32 bit alignment.
        if self.iph and self.alignment:
            iph_format += '\np16'

        self.iph_format = compile_fmt(iph_format)

        self.parse_data()
