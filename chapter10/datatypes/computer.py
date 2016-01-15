
from collections import OrderedDict
import struct

from .base import IterativeBase


class Computer(IterativeBase):
    """Computer generated data (eg. TMATS setup record)."""

    def parse(self):
        if self.format > 3:
            raise NotImplementedError(
                'Computer Generated Data Format %s is reserved!' % self.format)

        # User Defined: do nothing
        elif self.format == 0:
            return

        # TMATS
        elif self.format == 1:
            self.csdw_format = ('=I', ((
                (None, 22),
                ('frmt', 1),     # Format: 0 = ASCII, 1 = XML.
                ('srcc', 1),     # Setup Record Config Change
                ('version', 8),  # Chapter 10 version
            ),),)
            self.parse_csdw()
            self.parse_data()

            # Parse ASCII style TMATS.
            if self.frmt == 0:
                for line in self.data.splitlines():
                    line = line.decode()
                    if not line.strip():
                        continue
                    line = line.strip()[:-1]  # Strip the semicolon.
                    if ':' in line:
                        k, v = line.split(':', 1)
                    else:
                        k, v = line, ''
                    self.all.append([k, v])
            return

        # Recording Event
        if self.format == 2:
            self.csdw_format = ('=I', ((
                ('ipdh', 1),
                (None, 19),
                ('reec', 12),  # Rec Event Entry Count
            ),),)
            self.item_label = 'Recording Event'
            item_format = ('I', [(
                (None, 3),
                ('eo', 1),
                ('event_count', 16),
                ('event_number', 12),
            )],)

        # Recording Index
        elif self.format == 3:
            self.csdw_format = ('=I', ((
                ('it', 1),    # Index Type
                ('fsp', 1),   # File Size Present
                ('ipdh', 1),  # Index IPDH
                (None, 13),
                ('iec', 16),  # Index entry count
            ),),)

        self.parse_csdw()

        if getattr(self, 'it', None) == 0:
            self.item_label = 'Root Index'
            item_format = ('Q', ['offset'])
        elif getattr(self, 'it', None) == 1:
            self.item_label = 'Node Index'
            item_format = ('xBHQ', ['data_type', 'channel_id', 'offset'])

        self.iph_format = ['=Q', ['ipts']]

        if self.ipdh:
            self.iph_format[0] += 'Q'
            self.iph_format[1].append('ipdh')

        self.iph_format[0] += item_format[0]
        self.iph_format[1] = tuple(self.iph_format[1] + item_format[1])

        if getattr(self, 'fsp', False):
            self.file_size, = struct.unpack('Q', self.packet.file.read(8))

        self.parse_data()

        end = self.pos + self.packet.data_length
        if self.packet.file.tell() > end:
            self.all.pop()
            if getattr(self, 'it', None) == 0:
                self.seek(end - 8)
                self.root_offset, = struct.unpack(
                    'Q', self.packet.file.read(8))
            else:
                self.seek(end)

    def __getitem__(self, key):
        if self.format == 1:
            return OrderedDict([line for line in self.all
                                if line[0].startswith(key)])
        return IterativeBase.__getitem__(self, key)
