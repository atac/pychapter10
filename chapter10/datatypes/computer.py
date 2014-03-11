
from collections import OrderedDict

from .base import Base


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
        'tmats'
    )

    def parse(self):
        Base.parse(self)

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
