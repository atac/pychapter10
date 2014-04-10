
import struct

from .base import Base, Data


class Ethernet(Base):
    data_attrs = Base.data_attrs + (
        'frames',
        'all',
        'fmt',
        'length',
    )

    def parse(self):
        Base.parse(self)

        if self.format > 1:
            raise NotImplementedError('Ethernet format %s is reserved!'
                                      % self.format)

        # CSDW
        if self.format == 0:
            self.fmt = int(self.csdw >> 28)
            iph_length = 4
            time_length = 8
        elif self.format == 1:
            self.iph_length = int(self.csdw >> 16)
            iph_length = 20
            time_length = 4
        self.length = int(self.csdw & 0xffff)

        # Parse frames
        data = self.data[:]
        self.all, self.frames = [], []
        for i in range(self.length):

            # IPH
            iph = Data('IPH', data[time_length:iph_length + time_length])
            self.all += [Data('Timestamp', data[:time_length]), iph]
            data = data[time_length + iph_length:]

            if self.format == 0:
                iph = struct.unpack('I', iph.data)[0]
                length = int(iph & 0x3fff)
            else:
                length = struct.unpack('HH', iph.data)[1]

            # The actual ethernet frame.
            frame = Data('Ethernet Frame', data[:length])
            data = data[length:]
            self.frames.append(frame)
            self.all.append(frame)

            # Account for filler byte when length is odd.
            if length % 2:
                data = data[1:]

    def __iter__(self):
        return iter(self.frames)

    def __len__(self):
        return self.length
