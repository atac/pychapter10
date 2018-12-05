
from .base import IterativeBase


class MS1553(IterativeBase):
    item_label = 'Message'

    def parse(self):
        if self._format == 0 or self._format > 2:
            raise NotImplementedError('1553 Format %s is reserved!'
                                      % self._format)

        if self._format == 1:
            self.csdw_format = ('=I', ((
                ('time_tag_bits', 2),
                (None, 6),
                ('message_count', 24),
            ),),)
            # TODO: review names and decide on long-form or short-form for
            # both PyChapter10 and libirig106-python
            self.iph_format = ('=QHHH', ('rtc', (
                (None, 2),
                ('bus', 1),
                ('me', 1),
                ('rt2rt', 1),
                ('fe', 1),
                ('timeout', 1),
                (None, 3),
                ('le', 1),
                ('se', 1),
                ('we', 1),
                (None, 3),
            ), 'gap_time', 'length'))

        elif self._format == 2:
            self.csdw_format = ('=I', ('message_count',))

            self.iph_format = ('=QHH', ('intra_packet_timestamp', 'length', (
                ('transaction_error', 1),
                ('reset', 1),
                ('message_timeout', 1),
                ('status_error', 1),
                ('echo_error', 1),
            )))

        IterativeBase.parse(self)
