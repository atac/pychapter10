
from bitstring import BitArray

from .base import IterativeBase, Item


class UART(IterativeBase):
    data_attrs = IterativeBase.data_attrs + (
        'iph',
    )

    def parse(self):
        IterativeBase.parse(self)

        if self.format > 0:
            raise NotImplementedError('UART format %s is reserved!'
                                      % self.format)

        self.iph = self.csdw[-31]

        offset = 0
        while True:
            attrs = {}

            if self.iph:
                attrs['ipts'] = self.data[offset:offset + 8]
                offset += 8

            iph = BitArray(self.data[offset:offset + 4])
            iph.byteswap()
            offset += 4
            attrs.update({
                'pe': iph[-31],
                'subchannel': iph[-29:-16].int,
                'length': iph[-15:].int})

            data = self.data[offset:offset + attrs['length']]
            offset += attrs['length']
            self.all.append(Item(data, 'UART Data', **attrs))

            if attrs['length'] % 2:
                offset += 1
