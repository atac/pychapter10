
from bitstring import BitArray

from .base import IterativeBase, Item


class Ethernet(IterativeBase):
    data_attrs = IterativeBase.data_attrs + (
        'fmt',
        'length',
    )

    def parse(self):
        IterativeBase.parse(self)

        if self.format > 1:
            raise NotImplementedError('Ethernet format %s is reserved!'
                                      % self.format)

        # CSDW
        if self.format == 0:
            self.fmt = int(self.csdw >> 28)
            iph_length = 4
        elif self.format == 1:
            self.iph_length = int(self.csdw >> 16)
            iph_length = 20
        self.length = int(self.csdw & 0xffff)

        # Parse frames
        offset = 0
        for i in range(self.length):

            attrs = {}

            # IPTS @todo: replace with a useful type.
            attrs['ipts'] = self.data[offset:offset + 8]
            offset += 8

            # IPH
            iph = BitArray(bytes=self.data[offset:offset + iph_length])
            iph.byteswap()
            offset += iph_length

            if self.format == 0:
                length = iph[-14:].int
            else:
                length = iph[-16:].int

            # The actual ethernet frame.
            self.all.append(Item(
                self.data[offset:offset + length], 'Ethernet Frame', **attrs))
            offset += length

            # Account for filler byte when length is odd.
            if length % 2:
                offset += 1
