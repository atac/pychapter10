
from collections import OrderedDict
import struct

import bitstruct

from .base import IterativeBase, Item


class Computer(IterativeBase):
    """Computer generated data (eg. TMATS setup record)."""

    data_attrs = IterativeBase.data_attrs + (
        'frmt',
        'srcc',
        'version',
        'iph',
        'reec',
        'it',
        'fsp',
        'iec',
        'file_size',
        'root_offset',
    )

    def parse(self):
        IterativeBase.parse(self)

        # Offset into the data attribute.
        offset = 0

        if self.format > 3:
            raise NotImplementedError(
                'Computer Generated Data Format %s is reserved!' % self.format)

        # User Defined: do nothing
        elif self.format == 0:
            return

        # TMATS
        elif self.format == 1:
            self.frmt = self.csdw[9]          # Format: 0 = ASCII, 1 = XML.
            self.srcc = self.csdw[8]          # Setup Record Config Change flag
            self.version = self.csdw[:7].int  # Chapter 10 version

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
        elif self.format == 2:
            self.iph = self.csdw[31]        # Intra Packet Header
            self.reec = self.csdw[:11].int  # Rec Event Entry Count

            count = self.reec
            step = 12

        # Recording Index
        elif self.format == 3:
            self.it = self.csdw[31]        # Index Type
            self.fsp = self.csdw[30]       # File Size Present
            self.iph = self.csdw[29]       # Index IPH
            self.iec = self.csdw[:15].int  # Index Entry Count

            count = self.iec

            if self.fsp:
                self.file_size = struct.unpack('Q', self.data[:8])[0]
                offset += 8

            step = 20 if self.it else 16

        if self.iph:
            step += 8

        for i in range(count):

            attrs = {}

            # IPTS @todo: parse into useful type
            attrs['ipts'] = self.data[offset:offset + 8]
            offset += 8

            # IPH (optional) @todo: compute time
            if self.iph:
                attrs['iph'] = self.data[offset:offset + 8]
                offset += 8

            # Data (event, root index, or node index)
            if self.format == 2:
                data = self.data[offset:offset + 4]
                keys = ('eo', 'event_count', 'event_number')
                values = bitstruct.unpack('p2u1u15u12', bytearray(data))

                self.all.append(Item(data, 'Recording Event', **attrs))
                offset += 4

            elif self.format == 3:
                if self.it == 0:
                    data = self.data[offset:offset + 8]
                    attrs['offset'] = struct.unpack('=Q', data)[0]
                    self.all.append(Item(data, 'Root Index', **attrs))
                    offset += 8
                elif self.it == 1:
                    data = self.data[offset:offset + 12]
                    keys = ('channel_id', 'data_type', 'offset')
                    values = struct.unpack('=xBHQ', data)
                    attrs.update(dict(zip(keys, values)))
                    self.all.append(Item(data, 'Node Index', **attrs))
                    offset += 12

        if getattr(self, 'it', None) == 0:
            self.root_offset = struct.unpack('Q', self.data[:8])[0]

    def __getitem__(self, key):
        if self.format == 1:
            return OrderedDict([line for line in self.all
                                if line[0].startswith(key)])
        return IterativeBase.__getitem__(self, key)
