
from bitstring import BitArray

from .base import IterativeBase, Item


class Message(IterativeBase):
    data_attrs = IterativeBase.data_attrs + (
        'packet_type',
        'counter',
    )

    def parse(self):
        IterativeBase.parse(self)

        if self.format != 0:
            raise NotImplementedError('Message format %s is reserved!'
                                      % self.format)

        self.packet_type = self.csdw[-17:-16].int
        self.counter = self.csdw[-15:].int

        # @todo: support for segmented messages

        # Type: complete
        if not self.packet_type:
            offset = 0

            for i in range(self.counter):

                attrs = {'ipts': self.data[offset:offset + 8]}
                offset += 8
                ipdh = self.data[offset:offset + 4]
                ipdh = BitArray(bytearray(ipdh))
                ipdh.byteswap()
                offset += 4
                attrs['de'] = ipdh[-31]
                attrs['fe'] = ipdh[-30]
                attrs['subchannel'] = ipdh[-29:-16].int
                length = ipdh[-15:].int
                attrs['length'] = length

                data = self.data[offset:offset + length]
                offset += length
                self.all.append(Item(data, 'Message Data', **attrs))

                # Account for filler byte when length is odd.
                if length % 2:
                    offset += 1
