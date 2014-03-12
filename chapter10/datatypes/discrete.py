
from .base import Base, Data


class Discrete(Base):
    data_attrs = Base.data_attrs + (
        'all',
        'events',
        'd31',
        'd30',
        'd1',
        'd0',
    )

    def parse(self):
        Base.parse(self)

        if self.format != 1:
            raise NotImplementedError('Discrete data format %s is reserved!'
                                      % self.format)

        self.d31 = bool(self.csdw & (0x1 << 31))
        self.d30 = bool(self.csdw & (0x1 << 30))
        self.d1 = bool(self.csdw & (0x1 << 1))
        self.d0 = bool(self.csdw & 0b1)

        data = self.data[:]
        self.all, self.events = [], []
        for i in range(len(data) / 12):
            iph = Data('IPH', data[:8])
            data = data[8:]
            self.all.append(iph)

            event = Data(data[:4])
            data = data[4:]
            self.events.append(event)
            self.all.append(event)

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
