
import struct

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

        self.iph = (self.csdw >> 31) & 0x1

        offset = 0
        while True:
            attrs = {}

            if self.iph:
                attrs['ipts'] = self.data[offset:offset + 8]
                offset += 8

            iph, = struct.unpack('=I', self.data[offset:offset + 4])
            offset += 4
            attrs.update({
                'pe': (iph >> 31) & 0x1,
                'subchannel': int((iph >> 16) & 0x1fff),
                'length': int(iph & 0xffff)})

            data = self.data[offset:offset + attrs['length']]
            offset += attrs['length']
            self.all.append(Item(data, 'UART Data', **attrs))

            if attrs['length'] % 2:
                offset += 1
