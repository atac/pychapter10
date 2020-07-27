
from .util import compile_fmt
from .packet import Packet


class MS1553F1(Packet):
    item_label = '1553 Message'
    csdw_format = compile_fmt('''
        u24 count
        p6
        u2 time_tag_bits''')

    # TODO: bitstruct bit/byte order is weird for 16-bit groupings
    iph_format = compile_fmt('''
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


class MS1553F2(Packet):
    csdw_format = compile_fmt('u32 count')
    item_label = '16PP194 Message'
    iph_format = compile_fmt('''
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
