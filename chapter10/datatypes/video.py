
from array import array

from .base import IterativeBase, Item


class Video(IterativeBase):
    """Parse video (type 0x40-0x47)."""

    def parse(self):
        """Process channel specific data word (cdsw) and parse data."""

        IterativeBase.parse(self)

        # Channel Specific Data Word (csdw).
        if self.format == 0:
            self.et = (self.csdw >> 31) & 0b1       # Embedded time
            self.iph = (self.csdw >> 30) & 0b1      # Intra-packet header
            self.srs = (self.csdw >> 29) & 0b1      # SCR/RTC Sync
            self.klv = (self.csdw >> 28) & 0b1      # KLV Metadata
            self.pl = int((self.csdw >> 24) & 0xf)  # Payload type
            self.ba = (self.csdw >> 23) & 0b1       # Byte alignment
        elif self.format == 1:
            self.klv = (self.csdw >> 21) & 0b1       # KLV Metadata
            self.srs = (self.csdw >> 20) & 0b1       # SCR/RTC Sync
            self.iph = (self.csdw >> 19) & 0b1       # Intra-packet header
            self.epl = int((self.csdw >> 15) & 0xf)  # Encode profile & level
            self.et = (self.csdw >> 14) & 0b1        # Embedded time
            self.md = (self.csdw >> 13) & 0b1        # Bit rate mode
            self.tp = (self.csdw >> 12) & 0b1        # Bit stream type
            self.pc = int(self.csdw & 0xfff)         # Packet count
        elif self.format == 2:
            self.aet = (self.csdw >> 26) & 0b1      # Audio Encoding Type
            self.el = int((self.csdw >> 22) & 0xf)  # Encoding Level
            self.klv = (self.csdw >> 21) & 0b1      # KLV metadata
            self.srs = (self.csdw >> 20) & 0b1      # SCR/RTC Sync
            self.iph = (self.csdw >> 19) & 0b1      # Intra-packet header
            self.ep = int((self.csdw >> 15) & 0xf)  # Encoding Profile
            self.et = (self.csdw >> 14) & 0b1       # Embedded Time
            self.md = (self.csdw >> 13) & 0b1       # Bit rate mode
            self.tp = (self.csdw >> 12) & 0b1       # Bit stream type
            self.pc = int(self.csdw & 0xfff)        # Packet Count
        else:
            raise NotImplementedError(
                'Video Format %s is reserved!' % self.format)

        offset = 0
        for i in range(int(len(self.data) / 188)):
            attrs = {}

            if self.iph:
                attrs['ipts'] = self.data[offset:offset + 8]
                offset += 8

            data = array('H', self.data[offset:offset + 188])
            offset += 188
            if not getattr(self, 'ba', False):
                data.byteswap()
            self.all.append(Item(data, 'MPEG Packet', **attrs))
