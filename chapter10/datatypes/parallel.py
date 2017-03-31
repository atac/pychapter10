
from .base import Base


class Parallel(Base):
    def _parse(self):
        if self._format > 0:
            raise NotImplementedError('Parallel data format %s is reserved!'
                                      % self._format)

        Base._parse(self)
