
import struct

from .base import IterativeBase, Item


class MS1553(IterativeBase):

    def parse(self):
        IterativeBase.parse(self)

        if self.format == 0 or self.format > 2:
            raise NotImplementedError('1553 Format %s is reserved!'
                                      % self.format)

        offset = 0

        if self.format == 1:
            self.ttb = int(self.csdw >> 30)
            self.msg_count = int(self.csdw & 0xffffff)
            iph_len = 6

        elif self.format == 2:
            self.msg_count = int(self.csdw)
            iph_len = 4

        for i in range(self.msg_count):
            attrs = {'ipts': self.data[offset:offset + 8]}
            offset += 8
            iph = self.data[offset:offset + iph_len]
            offset += iph_len
            if self.format == 1:
                gap, length = struct.unpack('=HH', iph[-4:])
                status, = struct.unpack('=H', iph[:2])
                attrs = {
                    'gap': gap,
                    'length': length,
                    'bid': (status >> 13) & 0x1,  # Bus ID (A/B)
                    'me': (status >> 12) & 0x1,   # Message Error
                    'rr': (status >> 11) & 0x1,   # RT to RT Transfer
                    'fe': (status >> 10) & 0x1,   # Format Error
                    'tm': (status >> 9) & 0x1,    # Response Time Out
                    'le': (status >> 5) & 0x1,    # Word Count Error
                    'se': (status >> 4) & 0x1,    # Sync Type Error
                    'we': (status >> 3) & 0x1,    # Invalid Word Error
                }
            elif self.format == 2:
                length, status = struct.unpack('=HH', iph)
                attrs = {
                    'length': length,
                    'te': (status >> 15) & 0x1,  # Transaction Error
                    're': (status >> 14) & 0x1,  # Reset
                    'tm': (status >> 13) & 0x1,  # Message Time Out
                    'se': (status >> 6) & 0x1,   # Status Error
                    'ee': (status >> 3) & 0x1,   # Echo Error
                }

            data = self.data[offset:offset + attrs['length']]
            offset += attrs['length']
            self.all.append(Item(data, 'Message', **attrs))
