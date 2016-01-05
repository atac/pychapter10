
from .base import IterativeBase


class Message(IterativeBase):

    csdw_format = ('=HH', (
        ((None, 6), ('packet_type', 2)),
        'counter'))

    iph_format = ('=qI', (
        'ipts', (
            ('de', 1),
            ('fe', 1),
            ('subchannel', 14),
            ('length', 16)
        ),
    ))
    item_label = 'Message Data'

    def parse(self):
        if self.format != 0:
            raise NotImplementedError('Message format %s is reserved!'
                                      % self.format)

        self.parse_csdw()

        # @todo: support for segmented messages

        # Type: complete
        if not self.packet_type:
            self.parse_data()
