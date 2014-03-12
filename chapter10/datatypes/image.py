
import struct

from .base import Base, Data


class Image(Base):
    data_attrs = Base.data_attrs + (
        'parts',
        'sum',
        'iph',
        'length',
        'segments',
        'all',
    )

    def parse(self):
        Base.parse(self)

        if self.format > 2:
            raise NotImplementedError('Image format %s is reserved!'
                                      % self.format)

        self.parts = int(self.csdw >> 30)
        self.sum = int(self.csdw >> 28 & 0b11)
        self.iph = bool(self.csdw & (0x1 << 27))
        data = self.data[:]
        self.all, self.segments = [], []

        if self.format == 0:
            self.length = int(self.csdw & 0x1a)
            segment_length = self.length
            if self.iph:
                segment_length += 8

            for i in range(self.packet.data_length / segment_length):
                if self.iph:
                    iph = Data('IPH', data[:8])
                    data = data[8:]
                    self.all.append(iph)

                segment = Data('Image Segment', data[:self.length])
                data = data[self.length:]
                self.all.append(segment)
                self.segments.append(segment)

        else:
            if self.format == 1:
                self.fmt = int(self.csdw >> 23 & 0b1111)
            elif self.format == 2:
                self.fmt = int(self.csdw >> 21 & 0b111111)

            while True:
                try:
                    ipts = Data('Timestamp', data[:8])
                    data = data[8:]
                    self.all.append(ipts)

                    iph = Data('IPH', data[:4])
                    data = data[4:]

                    length = struct.unpack('I', iph.data)[0]
                    segment = Data('Image Segment', data[:length])
                    data = data[length:]
                    self.segments.append(segment)
                    self.all.append(segment)
                except IndexError:
                    break

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
