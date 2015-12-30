
import struct


def mask(i):
    """Create a mask of i length."""

    return int('0b' + ('1' * i), 2)


class Base(object):
    """Base object for packet data. All data types include a "csdw" attribute
    containing the channel specific raw data word (or words in some cases), and
    a "data" attribute containing the raw packet data. Subclasses should extend
    the parse method to process the raw data into more useful forms.
    """

    csdw_structure = None

    def __init__(self, packet):
        """Logs the file cursor location for later and skips past the data."""

        self.packet, self.init = (packet, False)

        # Find the body position.
        self.pos = self.packet.file.tell()

        # Get our type and format.
        from . import format
        self.type, self.format = format(self.packet.data_type)
        self.parse()

    def _dissect(self, data, structure):
        # just csdw for now
        # data, = struct.unpack('=I', data)
        for attr, size in reversed(structure):
            value = data & mask(size)
            if size > 1:
                value = int(value)
            data = data >> size
            if attr is not None:
                for a in attr.split(','):
                    setattr(self, a, value)

    def parse(self):
        """Reads the Channel Specific Data Word (csdw) and data into
        attributes.
        """

        self.csdw, = struct.unpack('=I', self.packet.file.read(4))
        if self.csdw_structure is not None:
            self._dissect(self.csdw, self.csdw_structure)
        self.data = self.packet.file.read(self.packet.data_length - 4)

    def __len__(self):
        return self.packet.data_length


class IterativeBase(Base):
    """Allows for easily packaging sub-elements into an iterable object based
    on an "all" attribute. Subclasses merely populate this attribute (a list)
    and length, iteration, etc. should just work.
    """

    def __init__(self, *args, **kwargs):
        self.all = []
        Base.__init__(self, *args, **kwargs)

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)


class Item(object):
    """The base container for packet data."""

    def __init__(self, data, label="Packet Data", **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

            self.data, self.label = data, label

    def __repr__(self):
        return '<%s>' % (self.label)

    def bytes(self):
        return self.data
