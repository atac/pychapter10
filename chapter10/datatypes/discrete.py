
from .base import IterativeBase, Item

import bitstruct


class Discrete(IterativeBase):
    data_attrs = IterativeBase.data_attrs + ('length', 'mode')

    def parse(self):
        IterativeBase.parse(self)

        if self.format != 1:
            raise NotImplementedError('Discrete data format %s is reserved!'
                                      % self.format)

        self.length, self.mode = bitstruct.unpack('p24u5u3', self.csdw)

        data = self.data[:]
        offset = 0
        for i in range(len(data) / 12):
            iph = data[offset:offset + 8]
            offset += 8

            data = self.data[offset:offset + 4]
            self.all.append(Item(data, 'Discrete data',
                                 {'iph': iph, 'ipts': iph}))
            offset += 4
