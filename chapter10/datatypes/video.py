
from .base import IterativeBase


class Video(IterativeBase):
    """Parse video (type 0x40-0x47)."""

    iph_format = (None, None)
    item_label = 'MPEG Packet'
    item_size = 188

    def parse(self):
        """Process channel specific data word (cdsw) and parse data."""

        # Channel Specific Data Word (csdw).
        if self.format == 0:
            self.csdw_format = ('=I', ((
                ('et', 1),   # Embedded time
                ('iph', 1),  # Intra-packet header
                ('src', 1),  # SCR/RTC Sync
                ('klv', 1),  # KLV Metadata
                ('pl', 4),   # Payload type
                ('ba', 1),   # Byte alignment
                (None, 23),
            ),),)
        elif self.format == 1:
            self.csdw_format = ('=I', ((
                (None, 10),
                ('klv', 1),  # KLV Metadata
                ('src', 1),  # SCR/RTC Sync
                ('iph', 1),  # Intra-packet header
                ('epl', 4),  # Encode profile & level
                ('et', 1),   # Embedded time
                ('md', 1),   # Bit rate mode
                ('tp', 1),   # Bit stream type
                ('pc', 12),  # Packet count
            ),),)
        elif self.format == 2:
            self.csdw_format = ('=I', ((
                ('aet', 1),  # Audio Encoding Type
                ('el', 4),   # Encoding Level
                ('klv', 1),  # KLV metadata
                ('srs', 1),  # SCR/RTC Sync
                ('iph', 1),  # Intra-packet header
                ('ep', 4),   # Encoding Profile
                ('et', 1),   # Embedded Time
                ('md', 1),   # Bit rate mode
                ('tp', 1),   # Bit stream type
                ('pc', 12),  # Packet Count
            ),),)
        else:
            raise NotImplementedError(
                'Video Format %s is reserved!' % self.format)

        self.parse_csdw()

        if self.iph:
            self.iph_format = ('=q', ('ipts',))

        self.parse_data()
