
from .base import IterativeBase


class PCM(IterativeBase):

    csdw_format = ('=I', ((
        ('iph', 1),
        ('ma', 1),
        ('mi', 1),
        ('mifs', 2),
        ('mafs', 2),
        (None, 2),
        ('align', 1),
        ('throughput', 1),
        ('packed', 1),
        ('unpacked', 1),
        ('s_offset', 18),
    ),),)
    item_label = 'PCM Frame'
    item_size = 12  # Two words sync, four data.

    def parse(self):
        if self.format != 1:
            raise NotImplementedError(
                'PCM Format %s is reserved!' % self.format)

        self.parse_csdw()

        # Throughput basically means we don't need to do anything.
        if self.throughput:
            return

        # Figure out the correct IPH format based on CSDW.
        if self.iph:
            # Extra IPH word in 32 bit alignment.
            if self.align:
                self.iph_format = ('=QI', (
                    'ipts', (
                        ('lockst', 4),
                        (None, 12),
                    )
                ))
            else:
                self.iph_format = ('=QH', (
                    'ipts', (
                        ('lockst', 4),
                        (None, 12),
                    )
                ))

        self.parse_data()
