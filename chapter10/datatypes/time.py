
from .base import Base


class Time(Base):
    data_attrs = Base.data_attrs + (
        'date_fmt',
        'time_fmt',
        'source',
    )

    def parse(self):
        Base.parse(self)

        self.date_fmt = int(self.csdw >> 8 & 0xffff)
        self.time_fmt = int(self.csdw >> 4 & 0xffff)
        self.source = int(self.csdw & 0xffff)
