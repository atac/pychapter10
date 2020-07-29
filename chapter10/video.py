
from .util import BitFormat
from .packet import Packet


class Video(Packet):
    """Parse video (type 0x40-0x47)."""

    item_label = 'MPEG Packet'
    item_size = 188

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        if self.iph:
            self.iph_format = BitFormat('u64 ipts')


class VideoF0(Video):
    csdw_format = BitFormat('''
        p23
        u1 byte_alignment
        u4 payload
        u1 key_length
        u1 scr_rtc_sync
        u1 iph
        u1 embedded_time''')


class VideoF1(Video):
    csdw_format = BitFormat('''
        u12 count
        u1 type
        u1 mode
        u1 embedded_time
        u4 encoding_profile
        u1 iph
        u1 scr_rtc_sync
        u1 key_length_value
        p10''')


class VideoF2(Video):
    csdw_format = BitFormat('''
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
