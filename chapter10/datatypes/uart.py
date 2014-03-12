
import struct

from .base import Base, Data


class UART(Base):
    data_attrs = Base.data_attrs + (
        'all',
        'uart',
        'iph',
    )

    def parse(self):
        Base.parse(self)

        if self.format > 0:
            raise NotImplementedError('UART format %s is reserved!'
                                      % self.format)

        self.iph = bool(self.csdw & (0x1 << 31))

        self.all, self.uart = [], []
        data = self.data[:]
        while True:
            try:
                if self.iph:
                    timestamp = Data('Timestamp', data[:8])
                    data = data[8:]
                    self.all.append(timestamp)

                iph = Data('IPH', data[:4])
                data = data[4:]
                self.all.append(iph)

                length = struct.unpack('HH', iph.data)[-1]

                uart = Data('UART Data', data[:length])
                data = data[length:]
                self.uart.append(uart)
                self.all.append(uart)
            except IndexError:
                break

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
