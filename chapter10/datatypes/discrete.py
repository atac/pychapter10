
from ..util import compile_fmt
from .base import Base


class Discrete(Base):
    csdw_format = compile_fmt('''
        u3 mode
        u5 length
        p24''')
    item_label = 'Discrete data'
    item_size = 4
    iph_format = compile_fmt('u64 ipts')

    def parse(self):
        if self._format != 1:
            raise NotImplementedError('Discrete data format %s is reserved!'
                                      % self._format)

        Base.parse(self)
