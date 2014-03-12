
import struct

from .base import Base, Data


class Message(Base):
    data_attrs = Base.data_attrs + (
        'type',
        'counter',
        'messages',
        'all',
    )

    def parse(self):
        Base.parse(self)

        if self.format != 0:
            raise NotImplementedError('Message format %s is reserved!'
                                      % self.format)

        self.type = int(self.csdw >> 16 & 0b11)
        self.counter = int(self.csdw & 0xf)

        # Type: complete
        if not self.type:
            data = self.data[:]
            self.messages, self.all = [], []

            for i in range(self.counter):
                ipth = Data('IPTH', data[:8])
                data = data[8:]
                self.all.append(ipth)

                ipdh = Data('IPDH', data[:4])
                data = data[4:]
                self.all.append(ipdh)

                length = int(struct.unpack('I', ipdh.data)[0] & 0xf)
                msg = Data('Message Data', data[length:])
                data = data[length:]
                self.messages.append(msg)
                self.all.append(msg)

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
