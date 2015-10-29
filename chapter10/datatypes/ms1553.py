
import struct

from bitstring import BitArray

from .base import IterativeBase, Item


class MS1553(IterativeBase):
    data_attrs = IterativeBase.data_attrs + (
        'messages',
        'all',
        'ttb',
        'msg_count',
    )

    def parse(self):
        IterativeBase.parse(self)

        if self.format == 0 or self.format > 2:
            raise NotImplementedError('1553 Format %s is reserved!'
                                      % self.format)

        offset = 0

        if self.format == 1:
            self.ttb = self.csdw[:-30].int
            self.msg_count = self.csdw[-23:].int
            iph_len = 6

        elif self.format == 2:
            self.msg_count = self.csdw.int
            iph_len = 4

        for i in range(self.msg_count):
            attrs = {'ipts': self.data[offset:offset + 8]}
            offset += 8
            iph = self.data[offset:offset + iph_len]
            offset += iph_len
            if self.format == 1:
                gap, length = struct.unpack('HH', iph[-4:])
                status = BitArray(bytes=iph[:2])
                status.byteswap()
                attrs = {
                    'gap': gap,
                    'length': length,
                    'bid': status[-13],  # Bus ID (A/B)
                    'me': status[-12],   # Message Error
                    'rr': status[-11],   # RT to RT Transfer
                    'fe': status[-10],   # Format Error
                    'tm': status[-9],    # Response Time Out
                    'le': status[-5],    # Word Count Error
                    'se': status[-4],    # Sync Type Error
                    'we': status[-3],    # Invalid Word Error
                }
            elif self.format == 2:
                length, = struct.unpack('H', iph[:2])
                status = BitArray(bytes=iph[:2])
                status.byteswap()
                attrs = {
                    'length': length,
                    'te': status[-15],  # Transaction Error
                    're': status[-14],  # Reset
                    'tm': status[-13],  # Message Time Out
                    'se': status[-6],   # Status Error
                    'ee': status[-3],   # Echo Error
                }

            data = self.data[offset:offset + attrs['length']]
            offset += attrs['length']
            self.all.append(Item(data, 'Message', **attrs))
