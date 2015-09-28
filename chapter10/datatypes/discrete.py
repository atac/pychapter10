
from .base import Base, Data


class Discrete(Base):
    data_attrs = Base.data_attrs + (
        'all',
        'events',
        'length',
        'mode',
    )

    def parse(self):
        Base.parse(self)

        if self.format != 1:
            raise NotImplementedError('Discrete data format %s is reserved!'
                                      % self.format)

        self.length = int(self.csdw >> 3 & 31)
        self.mode = int(self.csdw & 0b111)

        data = self.data[:]
        self.all, self.events = [], []
        for i in range(len(data) / 12):
            iph = Data('IPH', data[:8])
            data = data[8:]
            self.all.append(iph)

            event = Data('Discrete data', data[:4])
            data = data[4:]
            self.events.append(event)
            self.all.append(event)

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
