
import struct

from bitstring import BitArray
from .base import IterativeBase, Item


class Ethernet(IterativeBase):
    data_attrs = IterativeBase.data_attrs + (
        'fmt',
        'length',
        'iph_length',
    )

    def parse(self):
        IterativeBase.parse(self)

        if self.format > 1:
            raise NotImplementedError('Ethernet format %s is reserved!'
                                      % self.format)

        # CSDW
        if self.format == 0:
            self.fmt = int(self.csdw >> 28)
            iph_length = 4
        elif self.format == 1:
            self.iph_length = int(self.csdw >> 16)
            iph_length = 20
        self.length = int(self.csdw & 0xffff)

        # Parse frames
        offset = 0
        for i in range(self.length):

            attrs = {}

            # IPTS @todo: replace with a useful type.
            attrs['ipts'] = self.data[offset:offset + 8]
            offset += 8

            # IPH
            if self.format == 0:
                iph = BitArray(bytes=self.data[offset:offset + iph_length])
                iph.byteswap()
                attrs.update({
                    'fce': iph[-31],              # Frame CRC Error
                    'fe': iph[-30],               # Frame Error
                    'content': iph[-29:-28].int,
                    'speed': iph[-27:-24].int,    # Ethernet Speed
                    'net_id': iph[-23:-16].int,
                    'dce': iph[-15],              # Data CRC Error
                    'le': iph[-14],               # Data Length Error
                    'data_length': iph[-13:].int})
            else:
                keys = (
                    'data_length',
                    'error_bits',
                    'flags_bits',
                    'virtual_link',
                    'source_ip',
                    'dest_ip',
                    'src_port',
                    'dst_port')
                values = struct.unpack('HBBxxHLLHH',
                                       self.data[offset:offset + iph_length])
                attrs.update(dict(zip(keys, values)))
            offset += iph_length

            # The actual ethernet frame.
            data = self.data[offset:offset + attrs['data_length']]
            self.all.append(Item(data, 'Ethernet Frame', **attrs))
            offset += attrs['data_length']

            # Account for filler byte when length is odd.
            if attrs['data_length'] % 2:
                offset += 1
