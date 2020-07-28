
from collections import OrderedDict
import struct

from .util import compile_fmt
from .packet import Packet


class ComputerF0(Packet):
    """User-defined."""

    pass


class ComputerF1(Packet):
    """Setup record (TMATS)"""

    csdw_format = compile_fmt('''
        u8 version
        u1 configuration_change
        u1 format''')

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)
        self.data = self.file.read(self.data_length - 4)

    def __getitem__(self, key):
        key = bytearray(key, 'utf-8')
        d = OrderedDict()
        for line in self.data.splitlines():
            if not line.strip() or b':' not in line:
                continue
            line = line.strip()[:-1].split(b':', 1)  # Strip the semicolon.
            if line[0].startswith(key):
                d[line[0]] = line[1]
        return d


class ComputerF2(Packet):
    """Recording Event."""

    csdw_format = compile_fmt('''
        u12 count
        p19
        u1 ipdh''')
    item_label = 'Recording Event'
    item_format = '''
        u12 number
        u16 count
        u1 occurrence
        p3'''

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        self.iph_format = 'u64 ipts'
        if self.ipdh:
            self.iph_format += '\nu64 ipdh'


class ComputerF3(Packet):
    """Index Packet"""

    csdw_format = compile_fmt('''
        u16 count
        p13
        u1 ipdh
        u1 file_size_present
        u1 index_type''')
    item_size = 0

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        if self.file_size_present:
            self.file_size, = struct.unpack('Q', self.file.read(8))

        self.iph_format = 'u64 ipts'
        if self.ipdh:
            self.iph_format += '\nu64 ipdh'

        if self.index_type == 0:
            self.item_label = 'Root Index'
            item_format = '\nu64 offset'
        elif self.index_type == 1:
            self.item_label = 'Node Index'
            item_format = '''
                u16 channel_id
                u8 data_type
                u8 offset'''

        self.iph_format = compile_fmt(self.iph_format + item_format)

        if self.index_type == 0:
            pos = self.file.tell()
            self.file.seek(self.data_length - 8)
            self.root_offset, = struct.unpack('Q', self.file.read(8))
            self.file.seek(pos)

    def __len__(self):
        data_size = self.data_length - 4
        if self.file_size_present:
            data_size -= 8

        # Root index
        if not self.index_type:
            msg_size = 16
            data_size -= 8
        else:
            msg_size = 20
        if self.ipdh:
            msg_size += 8

        return data_size // msg_size
