
from bitstring import BitArray

from .base import IterativeBase, Item


class ARINC429(IterativeBase):
    data_attrs = IterativeBase.data_attrs + ('msg_count',)

    def parse(self):
        IterativeBase.parse(self)

        if self.format > 0:
            raise NotImplementedError('ARINC-429 format %s is reserved!'
                                      % self.format)

        self.msg_count = self.csdw[-16:].int

        offset = 0
        for i in range(self.msg_count):
            raw = BitArray(bytes=self.data[offset:offset + 4])
            raw.byteswap()
            iph = {
                'bus': raw[-31:-24].int,
                'fe': raw[-23],          # Format error flag
                'pe': raw[-22],          # Parity error flag
                'bs': raw[-21],          # Bus speed (0 = low, 1 = high)
                'gap_time': raw[:-19].int}
            offset += 4

            self.all.append(Item(self.data[offset:offset + 4],
                                 'ARINC-429 Data Word', **iph))
            offset += 4
