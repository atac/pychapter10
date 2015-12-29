
import struct

from .base import IterativeBase, Item


class Image(IterativeBase):

    def parse(self):
        IterativeBase.parse(self)

        if self.format > 2:
            raise NotImplementedError('Image format %s is reserved!'
                                      % self.format)

        self.parts = int((self.csdw >> 30) & 0b11)
        self.sum = int((self.csdw >> 28) & 0b11)
        self.iph = (self.csdw >> 27) & 0b1

        offset = 0
        if self.format == 0:
            self.length = int(self.csdw & 0x7ffffff)
            segment_length = self.length
            if self.iph:
                segment_length += 8

            for i in range(self.packet.data_length / segment_length):
                attrs = {}
                if self.iph:
                    attrs['ipts'] = self.data[offset:offset + 8]
                    offset += 8

                data = self.data[offset:offset + self.length]
                self.all.append(Item(data, 'Image Segment', **attrs))
                offset += self.length

        else:
            if self.format == 1:
                self.fmt = int((self.csdw >> 23) & 0x1f)
            elif self.format == 2:
                self.fmt = int((self.csdw >> 21) & 0x1f)

            while True:
                try:
                    attrs = {'ipts': self.data[offset:offset + 8]}
                    offset += 8

                    attrs['length'] = struct.unpack(
                        'I', self.data[offset:offset + 4])
                    offset += 4

                    data = self.data[offset:offset + attrs['length']]
                    offset += attrs['length']
                    self.all.append(Item(data, 'Image Segment', **attrs))
                except IndexError:
                    break
