
from ..util import compile_fmt

from .base import Base, Item


class Analog(Base):

    csdw_format = compile_fmt('''
        u2 mode
        u6 length
        u8 subchannel
        u8 channel_count
        u4 factor
        u1 same
        p2''')
    item_label = 'Analog Sample'
    iph_format = (None, None)

    def parse_csdw(self):
        values = self.csdw_format.unpack(self.packet.file.read(4))
        if self.subchannels == []:
            self.__dict__.update(values)
        self.subchannels.append(values)

    def parse(self):
        if self._format != 1:
            raise NotImplementedError('Analog format %s is reserved!'
                                      % self._format)

        # Parse one CSDW and see how many there are.
        self.subchannels = []
        self.parse_csdw()
        count = self.channel_count or 256  # 0 = 256

        # Read CSDWs for subchannels if applicable.
        if not self.same:
            for i in range(count - 1):
                self.parse_csdw()

        self.parse_data()

    def parse_data(self):
        for i in range(self.channel_count):
            if self.same:
                csdw = self.subchannels[0]
            else:
                csdw = self.subchannels[i]

            # Find the sample size (in bits).
            length = csdw['length'] or 64  # Length 0 = 64 bits

            # Convert length to bytes (align on 16 bits first of course).
            length = int(length / 16) + (length % 16 and 1 or 0)

            data = self.packet.file.read(length)
            self.all.append(Item(data, self.item_label))

            # Account for filler byte when length is odd.
            if length % 2:
                self.packet.file.seek(1, 1)
