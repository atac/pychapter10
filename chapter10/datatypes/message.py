
import struct

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

        self.packet_type = int((self.csdw >> 16) & 0b11)
        self.counter = int(self.csdw >> 15)

        # @todo: support for segmented messages

        # Type: complete
        if not self.packet_type:
            offset = 0

            for i in range(self.counter):

                attrs = {'ipts': self.data[offset:offset + 8]}
                offset += 8
                ipdh, = struct.unpack('=I', self.data[offset:offset + 4])
                offset += 4
                attrs['de'] = int(ipdh >> 31)
                attrs['fe'] = int((ipdh >> 30) & 0b1)
                attrs['subchannel'] = int((ipdh >> 16) & 0x1fff)
                length = int(ipdh & 0x7fff)

                attrs['length'] = length

                data = self.data[offset:offset + length]
                offset += length
                self.all.append(Item(data, 'Message Data', **attrs))

                # Account for filler byte when length is odd.
                if length % 2:
                    offset += 1
