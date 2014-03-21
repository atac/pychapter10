
from collections import OrderedDict
import struct

from .base import Base, Data


class TMATS(object):
    """Container for TMATS key-value pairs (similar to a dict)."""

    def __init__(self, s, xml=False):
        self.data = s
        self.all = []
        self.parse()

    def parse(self):
        """Parse ASCII format TMATS."""

        for line in self.data.splitlines():
            if not line.strip():
                continue
            line = line.strip()[:-1]
            k, v = line.split(':', 1)
            self.all.append([k, v])

    def __getitem__(self, key):
        return OrderedDict([line for line in self.all
                            if line[0].startswith(key)])


class NodeIndex(Data):
    def __init__(self, raw):
        Data.__init__(self, 'Node Index', raw)
        self.data_type = struct.unpack('xB', raw[:2])[0]
        self.channel_id = struct.unpack('H', raw[2:4])[0]
        self.offset = struct.unpack('Q', raw[4:])[0]

        print self.data_type, self.channel_id, self.offset


class Computer(Base):
    """Computer generated data (eg. TMATS setup record)."""

    data_attrs = Base.data_attrs + (
        'frmt',
        'srcc',
        'version',
        'iph',
        'reec',
        'it',
        'fsp',
        'iec',
        'tmats',
        'file_size',
        'all',
        'indices',
        'root_offset',
    )

    def parse(self):
        Base.parse(self)

        self.all, self.indices = [], []

        if self.format > 3:
            raise NotImplementedError(
                'Computer Generated Data Format %s is reserved!' % self.format)

        # TMATS
        elif self.format == 1:
            self.frmt = bool(self.csdw & (1 << 9))  # Format ASCII / XML
            self.srcc = bool(self.csdw & (1 << 8))  # Setup Rec Config Change
            self.version = int(self.csdw & (0xff))  # Ch10 Version
            self.tmats = TMATS(self.data)

        # Recording Event
        elif self.format == 2:
            self.iph = bool(self.csdw & (1 << 31))  # Intra Packet Header
            self.reec = int(self.csdw & 0xfff)      # Rec Event Entry Count

        # Recording Index
        elif self.format == 3:
            self.it = bool(self.csdw & (1 << 31))   # Index Type
            self.fsp = bool(self.csdw & (1 << 30))  # File Size Present
            self.iph = bool(self.csdw & (1 << 29))  # Index IPH
            self.iec = int(self.csdw & 0xffff)      # Index Entry Count

            data = self.data[:]

            if self.fsp:
                self.file_size = struct.unpack('Q', self.data[:8])[0]
                self.data = self.data[8:]

            for i in xrange(self.iec):
                self.all.append(Data('Timestamp', data[:8]))
                data = data[8:]

                if self.iph:
                    self.all.append(Data('IPH', data[:8]))
                    data = data[8:]

                if self.it == 0:
                    index = Data('Root Index', data[:8])
                    data = data[8:]
                else:
                    index = NodeIndex(data[:12])
                    data = data[12:]
                self.indices.append(index)
                self.all.append(index)

            if self.it == 0:
                self.root_offset = struct.unpack('Q', self.data[:8])[0]

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
