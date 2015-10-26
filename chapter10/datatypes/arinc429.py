
import bitstruct

from .base import IterativeBase, Item


class ARINC429(IterativeBase):
    data_attrs = IterativeBase.data_attrs + ('msg_count',)

    def parse(self):
        IterativeBase.parse(self)

        if self.format > 0:
            raise NotImplementedError('ARINC-429 format %s is reserved!'
                                      % self.format)

        self.msg_count = int(self.csdw & 0xffff)

        iph_keys = (
            'bus',
            'fe',  # Format error flag
            'pe',  # Parity error flag
            'bs',  # Bus speed (0 = low speed, 1 = high speed)
            'gap_time')
        for i in range(self.msg_count):
            offset = i * 8

            raw_iph = bitstruct.unpack(
                'u7u1u1u1p1u19', bytearray(self.data[offset:offset + 4]))
            iph = dict(zip(iph_keys, raw_iph))

            self.all.append(Item(self.data[offset + 4:offset + 8],
                                 'ARINC-429 Data Word', **iph))
