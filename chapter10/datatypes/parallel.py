
from .base import Base


class Parallel(Base):
    def parse(self):
        Base.parse(self)

        if self.format > 0:
            raise NotImplementedError('Parallel data format %s is reserved!'
                                      % self.format)
