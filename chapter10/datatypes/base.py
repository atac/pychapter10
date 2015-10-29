
from bitstring import BitArray


class Base(object):
    """Base object for packet data. All data types include a "csdw" attribute
    containing the channel specific raw data word (or words in some cases), and
    a "data" attribute containing the raw packet data. Subclasses should extend
    the parse method to process the raw data into more useful forms.
    """

    # The names of any data attributes for lazy-loading.
    data_attrs = (
        'data',
        'csdw',
    )

    def __init__(self, packet):
        """Logs the file cursor location for later and skips past the data."""

        self.packet, self.init = (packet, False)

        # Find the body position and skip to the packet trailer.
        self.pos = self.packet.file.tell()
        try:
            packet.file.seek(self.pos + self.packet.data_length)
        except OverflowError:
            pass

        # Get our type and format.
        from . import format
        self.type, self.format = format(self.packet.data_type)

    def parse(self):
        """Called lazily (only when requested) to avoid memory overflows.
        Reads the Channel Specific Data Word (csdw) and data into attributes.
        """

        pos = self.packet.file.tell()
        self.packet.file.seek(self.pos)
        csdw = BitArray(bytes=self.packet.file.read(4))
        csdw.byteswap()
        self.csdw = csdw
        self.data = self.packet.file.read(self.packet.data_length - 4)
        self.packet.file.seek(pos)
        self.init = True

    def __len__(self):
        return self.packet.data_length

    def __getattribute__(self, name):
        """Loads packet data on demand."""

        if name != 'data_attrs' and name in self.data_attrs and not self.init:
            self.parse()
        return object.__getattribute__(self, name)


class IterativeBase(Base):
    """Allows for easily packaging sub-elements into an iterable object based
    on an "all" attribute. Subclasses merely populate this attribute (a list)
    and length, iteration, etc. should just work.
    """

    data_attrs = Base.data_attrs + ('all', )

    def __init__(self, *args, **kwargs):
        Base.__init__(self, *args, **kwargs)
        self.all = []

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
