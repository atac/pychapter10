
from .base import Base, Data


class Video(Base):
    """Parse video (type 0x40-0x47)."""

    data_attrs = Base.data_attrs + ('all', 'mpeg')

    def parse(self):
        """Process channel specific data word (cdsw) and parse data."""

        Base.parse(self)

        # Channel Specific Data Word (csdw).
        if self.format == 0:
            self.et = bool(self.csdw & (1 << 31))      # Embedded time
            self.iph = bool(self.csdw & (1 << 30))     # Intra-packet header
            self.srs = bool(self.csdw & (1 << 29))     # SCR/RTC Sync
            self.klv = bool(self.csdw & (1 << 28))     # KLV Metadata
            self.pl = int(self.csdw >> 24 & 0b1111)    # Payload type
            self.ba = bool(self.csdw & (1 << 23))      # Byte alignment
        elif self.format == 1:
            self.klv = bool(self.csdw & (1 << 21))     # KLV Metadata
            self.srs = bool(self.csdw & (1 << 20))     # SCR/RTC Sync
            self.iph = bool(self.csdw & (1 << 19))     # Intra-packet header
            self.epl = int(self.csdw >> 15 & 0b1111)   # Encode profile & level
            self.et = bool(self.csdw & (1 << 14))      # Embedded time
            self.md = bool(self.csdw & (1 << 13))      # Bit rate mode
            self.tp = bool(self.csdw & (1 << 12))      # Bit stream type
            self.pc = int(self.csdw & 0b111111111111)  # Packet count
        elif self.format == 2:
            self.aet = bool(self.csdw & (1 << 26))     # Audio Encoding Type
            self.el = int(self.csdw >> 22 & 0b1111)    # Encoding Level
            self.klv = bool(self.csdw & (1 << 21))     # KLV metadata
            self.srs = bool(self.csdw & (1 << 20))     # SCR/RTC Sync
            self.iph = bool(self.csdw & (1 << 19))     # Intra-packet header
            self.ep = int(self.csdw >> 15 & 0b1111)    # Encoding Profile
            self.et = bool(self.csdw & (1 << 14))      # Embedded Time
            self.md = bool(self.csdw & (1 << 13))      # Bit rate mode
            self.tp = bool(self.csdw & (1 << 12))      # Bit stream type
            self.pc = int(self.csdw & 0b111111111111)  # Packet Count

        # Track all chunks (IPHs and MPEG packets) as well as MPEG alone.
        self.all, self.mpeg = [], []

        data = self.data[:]
        for i in range(len(data) / 188 + (8 if self.iph else 0)):
            if self.iph:
                self.all.append(Data('IPH', data[:8]))
                data = data[8:]

            mpeg = Data('MPEG Packet', data[:188])
            self.all.append(mpeg)
            self.mpeg.append(mpeg)
            data = data[188:]

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
