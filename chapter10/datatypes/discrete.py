
from .base import IterativeBase, Item


class Discrete(IterativeBase):
    data_attrs = IterativeBase.data_attrs + ('length', 'mode')

    def parse(self):
        IterativeBase.parse(self)

        if self.format != 1:
            raise NotImplementedError('Discrete data format %s is reserved!'
                                      % self.format)

        self.length = int((self.csdw >> 3) & 0x1f)
        self.mode = int(self.csdw & 0b111)

        offset = 0
        for i in range(len(self.data) / 12):
            iph = self.data[offset:offset + 8]
            offset += 8

            data = self.data[offset:offset + 4]
            self.all.append(Item(data, 'Discrete data',
                                 {'iph': iph, 'ipts': iph}))
            offset += 4
