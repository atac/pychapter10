
from .util import compile_fmt
from .packet import Packet


class MS1553F1(Packet):
    item_label = '1553 Message'
    csdw_format = compile_fmt('''
        u24 count
        p6
        u2 time_tag_bits''')

    # Note: bitfields from status word are listed in different order than shown
    # in the standard. bitstruct doesn't allow for specifying bit order across
    # multiple fields.
    iph_format = compile_fmt('''
        u64 ipts

        p2
        u1 le
        u1 se
        u1 we
        p3

        p2
        u1 bus
        u1 me
        p1
        u1 fe
        u1 timeout
        p1

        u16 gap_time
        u16 length''')


class MS1553F2(Packet):
    csdw_format = compile_fmt('u32 count')
    item_label = '16PP194 Message'
    iph_format = compile_fmt('''
        u64 ipts
        u16 length
        u1 se
        p1
        u1 ee
        p3
        u1 te
        u1 re
        u1 tm
        p6''')
