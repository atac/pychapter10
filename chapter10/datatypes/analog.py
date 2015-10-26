
import bitstruct

from .base import IterativeBase, Item


class Analog(IterativeBase):

    def parse_csdw(self, raw):
        """Parses a CSDW from raw bytes and returns a dict of values."""

        keys = (
            'same',
            'factor',
            'totchan',
            'subchan',
            'length',
            'mode')
        values = bitstruct.unpack('p2u1u3u7u7u5u2', raw)
        return dict(zip(keys, values))

    def parse(self):
        IterativeBase.parse(self)

        if self.format != 1:
            raise NotImplementedError('Analog format %s is reserved!'
                                      % self.format)

        # Parse one CSDW and see how many there are.
        subchannel = self.parse_csdw(self.csdw)
        self.subchannels = [subchannel]
        count = subchannel['totchan'] or 256  # totchan: 0 = 256
        if not subchannel['same']:

            # Read other subchannel CSDWs.
            for i in range(count - 1):
                i *= 4
                self.subchannels.append(self.parse_csdw(self.data[i:i+4]))

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
