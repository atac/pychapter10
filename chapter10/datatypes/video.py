
from .base import IterativeBase


class Video(IterativeBase):
    """Parse video (type 0x40-0x47)."""

    iph_format = (None, None)
    item_label = 'MPEG Packet'
    item_size = 188

    def _parse(self):
        """Process channel specific data word (cdsw) and parse data."""

        # Channel Specific Data Word (csdw).
        if self._format == 0:
            self.csdw_format = ('=I', ((
                ('embedded_time', 1),
                ('intra_packet_header', 1),
                ('scr_rtc_sync', 1),
                ('key_length_value', 1),
                ('payload', 4),
                ('byte_alignment', 1),
                (None, 23),
            ),),)
        elif self._format == 1:
            self.csdw_format = ('=I', ((
                (None, 10),
                ('key_length_value', 1),
                ('scr_rtc_sync', 1),
                ('intra_packet_header', 1),
                ('encoding_profile_and_level', 4),
                ('embedded_time', 1),
                ('mode', 1),
                ('type', 1),
                ('packet_count', 12),
            ),),)
        elif self._format == 2:
            self.csdw_format = ('=I', ((
                ('audio_encoding_type', 1),  # Audio Encoding Type
                ('encoding_level', 4),   # Encoding Level
                ('key_length_value', 1),  # KLV metadata
                ('scr_rtc_sync', 1),  # SCR/RTC Sync
                ('intra_packet_header', 1),  # Intra-packet header
                ('encoding_profile', 4),   # Encoding Profile
                ('embedded_time', 1),   # Embedded Time
                ('mode', 1),   # Bit rate mode
                ('type', 1),   # Bit stream type
                ('packet_count', 12),  # Packet Count
            ),),)
        else:
            raise NotImplementedError(
                'Video Format %s is reserved!' % self._format)

        self.parse_csdw()

        if self.intra_packet_header:
            self.iph_format = ('=q', ('intra_packet_timestamp',))

        self.parse_data()
