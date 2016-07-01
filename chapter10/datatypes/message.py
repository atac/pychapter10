
from .base import IterativeBase


class Message(IterativeBase):

    csdw_format = ('=I', ((
        ('packet_type', 2),
        ('counter', 16)
    ),),)

    iph_format = ('=qI', (
        'intra_packet_timestamp', (
            ('data_error', 1),
            ('format_error', 1),
            ('subchannel', 14),
            ('length', 16)
        ),
    ))
    item_label = 'Message Data'

    def parse(self):
        if self._format != 0:
            raise NotImplementedError('Message format %s is reserved!'
                                      % self._format)

        IterativeBase.parse(self)
