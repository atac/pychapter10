
from bitstring import BitArray

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
            'same': csdw[-28],
            'factor': csdw[-24:-27].int,
            'totchan': csdw[-16:-23].int,
            'subchan': csdw[-8:-15].int,
            'length': csdw[-2:-7].int,
            'mode': csdw[-1:].int}

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
        if not subchannel['same']:

            # Read other subchannel CSDWs.
            for i in range(count - 1):
                i *= 4
                csdw = BitArray(self.data[i:i+4])
                csdw.byteswap()
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
