
import struct

from .base import IterativeBase, Item


class Image(IterativeBase):
    data_attrs = IterativeBase.data_attrs + (
        'parts',
        'sum',
        'iph',
        'length',
        'segments',
    )

    def parse(self):
        IterativeBase.parse(self)

        if self.format > 2:
            raise NotImplementedError('Image format %s is reserved!'
                                      % self.format)

        self.parts = self.csdw[:-30].int
        self.sum = self.csdw[-29:-28].int
        self.iph = self.csdw[-27]

        offset = 0
        if self.format == 0:
            self.length = self.csdw[-26:].int
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
                self.fmt = self.csdw[-26:-23].int
            elif self.format == 2:
                self.fmt = self.csdw[-26:-21].int

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
