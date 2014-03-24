
from .base import Base


class Time(Base):
    data_attrs = Base.data_attrs + (
        'date_fmt',
        'time_fmt',
        'source',
    )

    def parse(self):
        Base.parse(self)

        if self.format != 1:
            raise NotImplementedError('Time Data format %s is reserved!'
                                      % self.format)

        self.date_fmt = int(self.csdw >> 8 & 0xf)
        self.time_fmt = int(self.csdw >> 4 & 0xf)
        self.source = int(self.csdw & 0xf)
