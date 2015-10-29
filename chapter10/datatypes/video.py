
from array import array

from .base import IterativeBase, Item


class Video(IterativeBase):
    """Parse video (type 0x40-0x47)."""

    data_attrs = IterativeBase.data_attrs + (
        'et',
        'iph',
        'srs',
        'klv',
        'pl',
        'ba',
        'epl',
        'md',
        'tp',
        'pc')

    def parse(self):
        """Process channel specific data word (cdsw) and parse data."""

        IterativeBase.parse(self)

        # Channel Specific Data Word (csdw).
        if self.format == 0:
            self.et = self.csdw[-31]          # Embedded time
            self.iph = self.csdw[-30]         # Intra-packet header
            self.srs = self.csdw[-29]         # SCR/RTC Sync
            self.klv = self.csdw[-28]         # KLV Metadata
            self.pl = self.csdw[-27:-24].int  # Payload type
            self.ba = self.csdw[-23]          # Byte alignment
        elif self.format == 1:
            self.klv = self.csdw[-21]          # KLV Metadata
            self.srs = self.csdw[-20]          # SCR/RTC Sync
            self.iph = self.csdw[-19]          # Intra-packet header
            self.epl = self.csdw[-18:-15].int  # Encode profile & level
            self.et = self.csdw[-14]           # Embedded time
            self.md = self.csdw[-13]           # Bit rate mode
            self.tp = self.csdw[-12]           # Bit stream type
            self.pc = self.csdw[-11:].int      # Packet count
        elif self.format == 2:
            self.aet = self.csdw[-26]         # Audio Encoding Type
            self.el = self.csdw[-25:-22].int  # Encoding Level
            self.klv = self.csdw[-21]         # KLV metadata
            self.srs = self.csdw[-20]         # SCR/RTC Sync
            self.iph = self.csdw[-19]         # Intra-packet header
            self.ep = self.csdw[-18:-15].int  # Encoding Profile
            self.et = self.csdw[-14]          # Embedded Time
            self.md = self.csdw[-13]          # Bit rate mode
            self.tp = self.csdw[-12]          # Bit stream type
            self.pc = self.csdw[-11:].int     # Packet Count
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
