
import struct

from .base import Base, Data


class I1394(Base):
    data_attrs = Base.data_attrs + (
        'transactions',
        'all',
        'pbt',
        'sy',
        'tc',
    )

    def parse(self):
        Base.parse(self)

        if self.format > 1:
            raise NotImplementedError('IEEE-1394 format %s is reserved!'
                                      % self.format)

        data = self.data[:]
        self.all, self.transactions = [], []

        if self.format == 0:
            self.pbt = int(self.csdw >> 29 & 0b111)  # Packet Body Type
            self.sy = int(self.csdw >> 25 & 0b1111)  # Synchronization Code
            self.tc = int(self.csdw & 0xf)           # Transaction Count

            # Bus Status
            if self.pbt == 0:
                pass

            # Data Streaming
            elif self.pbt == 1:
                self.transactions.append(Data('IEEE-1394 Transaction',
                                              self.data))

            # General Purpose
            elif self.pbt == 2:
                length = len(data) / self.tc

                for i in range(self.tc):
                    iph = Data('Timestamp', data[:8])
                    data = data[8:]
                    self.all.append(iph)

                    trans = Data('IEEE-1394 Transaction', data[:length - 8])
                    data = data[length - 8:]
                    self.all.append(trans)
                    self.transactions.append(trans)

        elif self.format == 1:
            self.ipc = int(self.csdw & 0xf)  # Intra Packet Count

            while True:
                try:
                    ipt = Data('Timestamp', data[:8])
                    data = data[8:]
                    self.all.append(ipt)

                    iph = Data('IPH', data[:4])
                    data = data[4:]
                    self.all.append(iph)

                    length = struct.unpack('HH', iph.data)[1]
                    trans = Data('IEEE-1397 Transaction', data[:length])
                    data = data[length:]
                    self.all.append(trans)
                    self.transactions.append(trans)
                except IndexError:
                    break

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
