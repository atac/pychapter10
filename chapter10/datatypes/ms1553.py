
from ..util import compile_fmt
from .base import Base


class MS1553(Base):
    item_label = 'Message'

    def parse(self):
        if self._format == 0 or self._format > 2:
            raise NotImplementedError('1553 Format %s is reserved!'
                                      % self._format)

        if self._format == 1:
            self.csdw_format = compile_fmt('''
                u24 message_count
                p6
                u2 time_tag_bits''')

            # TODO: bit/byte order is weird for 16-bit groupings
            self.iph_format = compile_fmt('''
                u64 ipts
                p2 reserved
                u1 le
                u1 se
                u1 we
                p5 reserved
                u1 bus
                u1 me
                u1 rt2rt
                u1 fe
                u1 timeout
                p1 reserved
                u16 gap_time
                u16 length''')

        elif self._format == 2:
            self.csdw_format = compile_fmt('u32 message_count')

            self.iph_format = compile_fmt('''
                u64 ipts
                u16 length
                u1 se
                u1 reserved
                u1 ee
                p3 reserved
                u1 te
                u1 re
                u1 tm
                p6 reserved''')

        Base.parse(self)
