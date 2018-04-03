
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
                ('format', 4),
                (None, 12),
                ('number_of_frames', 16),
            ),),)
            self.iph_format = ('=QI', ('intra_packet_timestamp', (
                ('frame_crc_error', 1),      # Frame CRC Error
                ('frame_error', 1),       # Frame Error
                ('captured_data_content', 2),
                ('ethernet_speed', 4),    # Ethernet Speed
                ('network_identifier', 8),
                ('data_crc_error', 1),      # Data CRC Error
                ('data_length_error', 1),       # Data Length Error
                ('length', 14),
            ),),)

        elif self._format == 1:
            self.csdw_format = ('=HH', ('iph_length', 'message_count'),)
            self.iph_format = ('=QHBBxxHLLHH', (
                'intra_packet_timestamp',
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
