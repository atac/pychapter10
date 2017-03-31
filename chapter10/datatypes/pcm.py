
from .base import IterativeBase


class PCM(IterativeBase):

    csdw_format = ('=I', ((
        ('intra_packet_header', 1),
        ('major_frame_indicator', 1),
        ('minor_frame_indicator', 1),
        ('minor_frame_status', 2),
        ('major_frame_status', 2),
        (None, 2),
        ('alignment', 1),
        ('throughput', 1),
        ('packed', 1),
        ('unpacked', 1),
        ('sync_offset', 18),
    ),),)
    item_label = 'PCM Frame'
    item_size = 12  # Two words sync, four data.
    iph_format = ['=QH', (
        'intra_packet_timestamp', (
            ('lock_status', 4),
            (None, 12),
        )
    )]

    def _parse(self):
        if self._format != 1:
            raise NotImplementedError(
                'PCM Format %s is reserved!' % self._format)

        self.parse_csdw()

        # Throughput basically means we don't need to do anything.
        if self.throughput:
            return

        # Figure out the correct IPH format based on CSDW.
        if self.intra_packet_header:
            # Extra IPH word in 32 bit alignment.
            if self.alignment:
                self.iph_format[0] = self.iph_format[0][:-1] + 'I'

        self.parse_data()
