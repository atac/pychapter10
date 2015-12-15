
import struct

from .base import IterativeBase, Item


class ARINC429(IterativeBase):
    data_attrs = IterativeBase.data_attrs + ('msg_count',)

    def parse(self):
        IterativeBase.parse(self)

        if self.format > 0:
            raise NotImplementedError('ARINC-429 format %s is reserved!'
                                      % self.format)

        self.msg_count = int(self.csdw & 0xffff)

        offset = 0
        for i in range(self.msg_count):
            raw, = struct.unpack('=I', self.data[offset:offset + 4])
            iph = {
                'bus': int((raw >> 24) & 0xff),
                'fe': (raw >> 23) & 0x1,        # Format error flag
                'pe': (raw >> 22) & 0x1,        # Parity error flag
                'bs': (raw >> 21) & 0x1,        # Bus speed (0 = low, 1 = high)
                'gap_time': int(raw & 0xfffff)}
            offset += 4

            self.all.append(Item(self.data[offset:offset + 4],
                                 'ARINC-429 Data Word', **iph))
            offset += 4
