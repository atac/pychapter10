
from .base import IterativeBase


class Ethernet(IterativeBase):
    item_label = 'Ethernet Frame'

    def parse(self):
        if self._format > 1:
            raise NotImplementedError('Ethernet format %s is reserved!'
                                      % self._format)

        # CSDW
        if self._format == 0:
            self.csdw_format = ('=I', ((
                ('fmt', 4),
                (None, 12),
                ('frames', 16),
            ),),)
            self.iph_format = ('=QI', ('ipts', (
                ('fce', 1),      # Frame CRC Error
                ('fe', 1),       # Frame Error
                ('content', 2),
                ('speed', 4),    # Ethernet Speed
                ('net_id', 8),
                ('dce', 1),      # Data CRC Error
                ('le', 1),       # Data Length Error
                ('length', 14),
            ),),)

        elif self._format == 1:
            self.csdw_format = ('=HH', ('iph_length', 'message_count'),)
            self.iph_format = ('HBBxxHLLHH', (
                'length',
                'error_bits',
                'flags_bits',
                'virtual_link',
                'source_ip',
                'dest_ip',
                'src_port',
                'dst_port')
            )

        IterativeBase.parse(self)
