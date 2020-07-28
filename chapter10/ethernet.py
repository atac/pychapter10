
from .util import compile_fmt
from .packet import Packet


class EthernetF0(Packet):
    item_label = 'Ethernet Frame'
    csdw_format = compile_fmt('''
        u16 count
        p9 reserved
        u3 ttb
        u4 format''')
    # Note: bitfields may need to be listed in reverse of expected
    # order.
    iph_format = compile_fmt('''
        u64 ipts
        u14 length
        u1 data_length_error
        u1 data_crc_error
        u8 network_id
        u1 crc_error
        u1 frame_error
        u2 content
        u4 ethernet_speed''')


class EthernetF1(Packet):
    item_label = 'Ethernet Frame'
    csdw_format = compile_fmt('''
        u16 count
        u16 iph_length''')
    iph_format = compile_fmt('''
        u64 ipts
        u8 flags
        u8 error
        u16 length
        u16 virtual_link
        p16
        u32 src_ip
        u32 dst_ip
        u16 dst_port
        u16 src_port''')
