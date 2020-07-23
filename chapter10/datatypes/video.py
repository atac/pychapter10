
from ..util import compile_fmt
from .base import IterativeBase


class Video(IterativeBase):
    """Parse video (type 0x40-0x47)."""

    item_label = 'MPEG Packet'
    item_size = 188

    def _parse(self):
        """Process channel specific data word (cdsw) and parse data."""

        # Channel Specific Data Word (csdw).
        if self._format == 0:
            self.csdw_format = compile_fmt('''
                p23
                u1 byte_alignment
                u4 payload
                u1 key_length
                u1 scr_rtc_sync
                u1 iph
                u1 embedded_time''')
        elif self._format == 1:
            self.csdw_format = compile_fmt('''
                u12 count
                u1 type
                u1 mode
                u1 embedded_time
                u4 encoding_profile
                u1 iph
                u1 scr_rtc_sync
                u1 key_length_value
                p10''')
        elif self._format == 2:
            self.csdw_format = compile_fmt('''
                u12 count
                u1 type
                u1 mode
                u1 embedded_time
                u4 encoding_profile
                u1 iph
                u1 scr_rtc_sync
                u1 key_length_value
                u4 encoding_level
                u1 audio_encoding_type
                p5''')
        else:
            raise NotImplementedError(
                'Video Format %s is reserved!' % self._format)

        self.parse_csdw()

        if self.iph:
            self.iph_format = compile_fmt('u64 ipts')

        self.parse_data()
