
from collections import OrderedDict
import struct

from .base import IterativeBase


class Computer(IterativeBase):
    """Computer generated data (eg. TMATS setup record)."""

    def _parse(self):
        if self._format > 3:
            raise NotImplementedError('Computer Generated Data Format %s is \
reserved!' % self._format)

        # User Defined: do nothing
        elif self._format == 0:
            return

        # TMATS
        elif self._format == 1:
            self.csdw_format = ('=I', ((
                (None, 22),
                ('format', 1),     # Format: 0 = ASCII, 1 = XML.
                ('setup_record_configuration_change', 1),
                ('version', 8),  # Chapter 10 version
            ),),)
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
            self.csdw_format = ('=I', ((
                ('intra_packet_data_header', 1),
                (None, 19),
                ('recording_event_entry_count', 12),
            ),),)
            self.item_label = 'Recording Event'
            item_format = ('I', [(
                (None, 3),
                ('event_occurrence', 1),
                ('event_count', 16),
                ('event_number', 12),
            )],)

        # Recording Index
        elif self._format == 3:
            self.csdw_format = ('=I', ((
                ('index_type', 1),
                ('file_size_present', 1),
                ('intra_packet_data_header', 1),
                (None, 13),
                ('index_entry_count', 16),
            ),),)

        self.parse_csdw()

        if self._format == 3:
            self.count = self.index_entry_count

        if getattr(self, 'index_type', None) == 0:
            self.item_label = 'Root Index'
            item_format = ('Q', ['offset'])
        elif getattr(self, 'index_type', None) == 1:
            self.item_label = 'Node Index'
            item_format = ('xBHQ', ['data_type', 'channel_id', 'offset'])

        self.iph_format = ['=Q', ['intra_packet_timestamp']]

        if self.intra_packet_data_header:
            self.iph_format[0] += 'Q'
            self.iph_format[1].append('intra_packet_data_header')

        self.iph_format[0] += item_format[0]
        self.iph_format[1] = tuple(self.iph_format[1] + item_format[1])

        if getattr(self, 'file_size_present', False):
            self.file_size, = struct.unpack('Q', self.packet.file.read(8))

        self.parse_data()

        end = self.pos + self.packet.data_length
        if self.packet.file.tell() > end:
            self.all.pop()
            if getattr(self, 'index_type', None) == 0:
                self.packet.file.seek(end - 8)
                self.root_offset, = struct.unpack(
                    'Q', self.packet.file.read(8))
            else:
                self.packet.file.seek(end)

    def __getitem__(self, key):
        key = bytearray(key, 'utf-8')
        if self._format == 1:
            return OrderedDict([line for line in self.all
                                if line[0].startswith(key)])
        return IterativeBase.__getitem__(self, key)
