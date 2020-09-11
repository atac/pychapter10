
from .util import BitFormat
from . import packet


__all__ = ('VideoF0', 'VideoF1', 'VideoF2')


class Video(packet.Packet):
    """Generic video superclass."""

    class Message(packet.Message):
        length = 188

        def __repr__(self):
            return '<MPEG Frame %s bytes>' % len(self.data)

    def __init__(self, *args, **kwargs):
        packet.Packet.__init__(self, *args, **kwargs)

        if self.iph:
            self.Message.FORMAT = BitFormat('u64 ipts')


class VideoF0(Video):
    """MPEG2/H.264

    .. py:attribute:: byte_alignment

        * 0 - Little endian
        * 1 - Big endian

    .. py:attribute:: payload

        * 0 - MPEG-2 MP @ ML
        * 1 - H.264 MP @ L2.1
        * 2 - H.264 MP @ L2.2
        * 3 - H.264 MP @ L3

    .. py:attribute:: key_length

        Indicates if key-length-value metadata is present

    .. py:attribute:: scr_rtc_sync

        Indicates if MPEG-2 SCR is RTC

    .. py:attribute:: iph
    .. py:attribute:: embedded_time

        Indicates time embedded in MPEG-2 stream.
    """

    csdw_format = BitFormat('''
        p23
        u1 byte_alignment
        u4 payload
        u1 key_length
        u1 scr_rtc_sync
        u1 iph
        u1 embedded_time''')

    class Message(Video.Message):
        """
        .. py:attribute:: ipts

            If indicated by iph flag in CSDW (see above)
        """


class VideoF1(Video):
    """ISO 13818-1 MPEG-2 bit stream

    .. py:attribute:: count
    .. py:attribute:: type

        * 0 - Transport data bit stream
        * 1 - Program data bit stream

    .. py:attribute:: mode

        * 0 - CBR stream
        * 1 - Variable bit rate stream

    .. py:attribute:: embedded_time

        Indicates time embedded in MPEG-2 stream.

    .. py:attribute:: encoding_profile

        * 0 - Simple profile @ main level
        * 1 - Main profile @ low level
        * 2 - Main profile @ main level
        * 3 - Main profile @ high-1440 level
        * 4 - Main profile @ high level
        * 5 - SNR profile @ low level
        * 6 - SNR profile @ main level
        * 7 - Spatial profile @ high-1440 level
        * 8 - High profile @ main level
        * 9 - High profile @ high-1440 level
        * 10 - High profile @ high level
        * 11 - 4:2:2 profile @ main level

    .. py:attribute:: iph
    .. py:attribute:: scr_rtc_sync

        Indicates if MPEG-2 SCR is RTC

    .. py:attribute:: key_length

        Indicates if key length value metadata is present.

    """

    csdw_format = BitFormat('''
        u12 count
        u1 type
        u1 mode
        u1 embedded_time
        u4 encoding_profile
        u1 iph
        u1 scr_rtc_sync
        u1 key_length
        p10''')

    class Message(Video.Message):
        """
        .. py:attribute:: ipts

            If indicated by iph flag in CSDW (see above)
        """


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

    class Message(Video.Message):
        """
        .. py:attribute:: ipts

            If indicated by iph flag in CSDW (see above)
        """
