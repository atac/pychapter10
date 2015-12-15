
import struct

from .base import IterativeBase, Item


class Analog(IterativeBase):
    data_attrs = IterativeBase.data_attrs + (
        'same',
        'factor',
        'totchan',
        'subchan',
        'length',
        'mode')

    def parse_csdw(self, csdw):
        """Parses a CSDW from raw bytes and returns a dict of values."""

        return {
            'same': bool((csdw >> 29) & 0x1),     # Is the CSDW the same for
                                                  # all subchannels?
            'factor': int((csdw >> 24) & 0b111),  # Sampling rate factor.
            'totchan': int((csdw >> 16) & 0xff),  # Subchannel count.
            'subchan': int((csdw >> 8) & 0xff),   # Subchannel ID.
            'length': int((csdw >> 2) & 0x3f),    # Sample length.
            'mode': int(csdw & 0b11)}             # Alignment and packing mode.

    def parse(self):
        IterativeBase.parse(self)

        if self.format != 1:
            raise NotImplementedError('Analog format %s is reserved!'
                                      % self.format)

        # Parse one CSDW and see how many there are.
        subchannel = self.parse_csdw(self.csdw)
        self.__dict__.update(subchannel)
        self.subchannels = [subchannel]
        count = subchannel['totchan'] or 256  # totchan: 0 = 256

        # Read CSDWs for subchannels if applicable.
        if not subchannel['same']:
            for i in range(count - 1):
                i *= 4
                csdw, = struct.unpack('H', self.data[i:i+4])
                # csdw = BitArray(bytes=self.data[i:i+4])
                # csdw.byteswap()
                self.subchannels.append(self.parse_csdw(csdw))

        # The current offset into self.data
        offset = i + 4

        # Update raw data attribute for multiple-csdw case.
        self.data = self.data[offset:]

        # Read analog samples.
        for i in range(count):

            csdw = subchannel if subchannel['same'] else self.subchannels[i]

            # Find the sample size (in bits).
            length = csdw['length'] or 64  # Length 0 = 64 bits

            # Convert length to bytes (align on 16 bits first of course).
            length = (length / 16) + (length % 16 and 1 or 0)

            self.all.append(
                Item(self.data[offset:length], 'Analog Sample'), **csdw)

            offset += length
