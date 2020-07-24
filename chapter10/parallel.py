
from .packet import Packet


class Parallel(Packet):
    def parse(self):
        if self._format > 0:
            raise NotImplementedError('Parallel data format %s is reserved!'
                                      % self._format)

        Packet.parse(self)
