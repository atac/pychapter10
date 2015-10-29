
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

        self.packet_type = self.csdw[-17:-16].int
        self.counter = self.csdw[-15:].int

        # Type: complete
        if not self.packet_type:
            offset = 0

            for i in range(self.counter):

                ipts = self.data[offset:offset + 8]
                offset += 8
                ipdh = self.data[offset:offset + 4]
                offset += 4
                length = struct.unpack('HH', ipdh)[0]

                attrs = {'ipts': ipts, 'length': length}

                data = self.data[offset:offset + length]
                offset += length
                self.all.append(Item(data, 'Message Data', **attrs))

                # Account for filler byte when length is odd.
                if length % 2:
                    offset += 1
