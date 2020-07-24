
from collections import OrderedDict
import struct

from .util import compile_fmt
from .packet import Packet


class Computer(Packet):
    """Computer generated data (eg. TMATS setup record)."""

    def parse(self):
        if self._format > 3:
            raise NotImplementedError('Computer Generated Data Format %s is \
reserved!' % self._format)

        # User Defined: do nothing
        elif self._format == 0:
            return

        # TMATS
        elif self._format == 1:
            self.csdw_format = compile_fmt('''
                u8 version
                u1 configuration_change
                u1 format''')
            self.parse_csdw()
            self.parse_data()

            # Parse ASCII style TMATS.
            if self.format == 0:
                for line in self.data.splitlines():
                    if not line.strip():
                        continue
                    line = line.strip()[:-1]  # Strip the semicolon.
                    if b':' in line:
                        k, v = line.split(b':', 1)
                        self.all.append([k, v])
                    else:
                        try:
                            line = [str(line).encode('utf8').strip(), '']
                        except UnicodeDecodeError:
                            continue
            return

        # Recording Event
        if self._format == 2:
            self.csdw_format = compile_fmt('''
                u12 count
                p19
                u1 ipdh''')
            self.item_label = 'Recording Event'
            item_format = '''
                u12 number
                u16 count
                u1 occurrence
                p3'''

        # Recording Index
        elif self._format == 3:
            self.csdw_format = compile_fmt('''
                u16 count
                p13
                u1 ipdh
                u1 file_size_present
                u1 index_type''')

        self.parse_csdw()

        if getattr(self, 'index_type', None) == 0:
            self.item_label = 'Root Index'
            item_format = 'u64 offset'
        elif getattr(self, 'index_type', None) == 1:
            self.item_label = 'Node Index'
            item_format = '''
                u16 channel_id
                u8 data_type
                u8 offset'''

        self.iph_format = 'u64 ipts'

        if self.ipdh:
            self.iph_format += '\nu64 ipdh'

        self.iph_format = compile_fmt(self.iph_format + '\n' + item_format)

        if getattr(self, 'file_size_present', False):
            self.file_size, = struct.unpack('Q', self.file.read(8))

        self.parse_data()

        end = self.packet_length
        if self.file.tell() > end:
            self.all.pop()
            if getattr(self, 'index_type', None) == 0:
                self.file.seek(end - 8)
                self.root_offset, = struct.unpack(
                    'Q', self.file.read(8))
            else:
                self.file.seek(end)

    def __getitem__(self, key):
        key = bytearray(key, 'utf-8')
        if self._format == 1:
            return OrderedDict([line for line in self.all
                                if line[0].startswith(key)])
        return Packet.__getitem__(self, key)
