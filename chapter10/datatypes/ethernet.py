
import struct

from base import Base, Data


class Ethernet(Base):
    data_attrs = Base.data_attrs + (
        'frames',
        'all',
        'fmt',
        'frame_count',
    )

    def parse(self):
        Base.parse(self)

        if self.format > 1:
            raise NotImplementedError('Ethernet format %s is reserved!'
                                      % self.format)

        if self.format == 0:

            # CSDW
            self.fmt = int(self.csdw >> 28)
            self.frame_count = int(self.csdw & 0xffff)

            # Parse frames
            data = self.data[:]
            self.all, self.frames = [], []
            for i in range(self.frame_count):

                # IPH
                iph = Data('IPH', data[8:12])
                self.all += [Data('Timestamp', data[:8]), iph]
                data = data[12:]

                iph = struct.unpack('I', iph.data)[0]
                length = int(iph & 0x3fff)

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
        return len(self.frames)
