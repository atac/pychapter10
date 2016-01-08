
import struct

from .base import IterativeBase


class Analog(IterativeBase):

    csdw_format = ('=I', ((
        ('same', 1),     # Is the CSDW the same for all subchannels?
        ('factor', 4),   # Sampling rate factor.
        ('totchan', 8),  # Subchannel count.
        ('subchan', 8),  # Subchannel ID.
        ('length', 6),   # Sample length.
        ('mode', 2),     # Alignment and packing mode.
    ),),)
    item_label = 'Analog Sample'
    iph_format = (None, None)

    def parse_csdw(self):
        fmt, structure = self.csdw_format
        raw = struct.unpack(fmt, self.packet.file.read(4))
        values = dict(self._dissect(raw, structure))
        if self.subchannels == []:
            self.__dict__.update(values)
        self.subchannels.append(values)

    def parse(self):
        if self.format != 1:
            raise NotImplementedError('Analog format %s is reserved!'
                                      % self.format)

        # Parse one CSDW and see how many there are.
        self.subchannels = []
        self.parse_csdw()
        count = self.totchan or 256  # totchan: 0 = 256

        # Read CSDWs for subchannels if applicable.
        if not self.same:
            for i in range(count - 1):
                self.parse_csdw()

        IterativeBase.parse_data()

    def parse_one_item(self):
        if self.same:
            csdw = self.subchannels[0]
        else:
            csdw = self.subchannels[len(self) + 1]

        # Find the sample size (in bits).
        length = csdw['length'] or 64  # Length 0 = 64 bits

        # Convert length to bytes (align on 16 bits first of course).
        self.item_size = (length / 16) + (length % 16 and 1 or 0)

        IterativeBase.parse_one_item(self)
