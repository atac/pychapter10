
import struct

from .base import Base, Data


class Message(Base):
    data_attrs = Base.data_attrs + (
        'packet_type',
        'counter',
        'messages',
        'all',
    )

    def parse(self):
        Base.parse(self)

        if self.format != 0:
            raise NotImplementedError('Message format %s is reserved!'
                                      % self.format)

        self.packet_type = self.csdw[16:17].int
        self.counter = self.csdw[:15].int

        # Type: complete
        if not self.packet_type:
            data = self.data[:]
            self.messages, self.all = [], []

            for i in range(self.counter):

                ipth = Data('IPTH', data[:8])
                data = data[8:]

                ipdh = Data('IPDH', data[:4])
                data = data[4:]

                length = struct.unpack('HH', ipdh.data)[0]

                msg = Data('Message Data', data[length:])
                data = data[length:]
                self.messages.append(msg)
                self.all += [ipth, ipdh, msg]

                # Account for filler byte when length is odd.
                if length % 2:
                    data = data[1:]

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
