
from .base import IterativeBase


class MS1553(IterativeBase):
    item_label = 'Message'

    def parse(self):
        if self._format == 0 or self._format > 2:
            raise NotImplementedError('1553 Format %s is reserved!'
                                      % self._format)

        if self._format == 1:
            self.csdw_format = ('=I', ((
                ('ttb', 2),
                (None, 6),
                ('msg_count', 24),
            ),),)
            self.iph_format = ('=QHHH', ('ipts', (
                (None, 2),
                ('bid', 1),  # Bus ID (A/B)
                ('me', 1),   # Message Error
                ('rr', 1),   # RT to RT Transfer
                ('fe', 1),   # Format Error
                ('tm', 1),   # Response Time Out
                (None, 3),
                ('le', 1),   # Word Count Error
                ('se', 1),   # Sync Type Error
                ('we', 1),   # Invalid Word Error
                (None, 3),
            ), 'gap', 'length'))

        elif self._format == 2:
            self.csdw_format = ('=I', ('msg_count',))

            self.iph_format = ('=QHH', ('ipts', 'length', (
                ('te', 1),  # Transaction Error
                ('re', 1),  # Reset
                ('tm', 1),  # Message Time Out
                ('se', 1),  # Status Error
                ('ee', 1),  # Echo Error
            )))

        IterativeBase.parse(self)
