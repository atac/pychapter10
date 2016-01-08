
from .base import IterativeBase


class Message(IterativeBase):

    csdw_format = ('=I', ((
        ('packet_type', 2),
        ('counter', 16)
    ),),)

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

        IterativeBase.parse(self)
