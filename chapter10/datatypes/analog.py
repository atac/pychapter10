
import struct

from .base import Base


class Analog(Base):
    def parse(self):
        Base.parse(self)

        if self.format != 1:
            raise NotImplementedError('Analog format %s is reserved!'
                                      % self.format)

        self.data = struct.pack('I', self.csdw) + self.data
