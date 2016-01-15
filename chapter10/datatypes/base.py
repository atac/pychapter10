
import struct


mask_cache = {}


def mask(bitlength):
    """Create a mask of i length."""

    if bitlength not in mask_cache:
        mask_cache[bitlength] = 0
        for i in range(bitlength):
            mask_cache[bitlength] |= (1 << i)
    return mask_cache[bitlength]


class Base(object):
    """Base object for packet data. All data types include a "csdw" attribute
    containing the channel specific raw data word (or words in some cases), and
    a "data" attribute containing the raw packet data. Subclasses should extend
    the parse method to process the raw data into more useful forms.
    """

    csdw_format = ('=I', None)
    data_format = None

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
        for i, field in enumerate(structure):
            value = data[i]
            if isinstance(field, tuple):
                for attr, size in reversed(field):
                    result = None
                    if attr is not None:
                        result = value & mask(size)
                    value = value >> size
                    if result is not None:
                        yield attr, result
            else:
                yield field, value

    def parse(self):
        """Reads the Channel Specific Data Word (csdw) and data into
        attributes.
        """

        self.parse_csdw()
        self.parse_data()

    def parse_csdw(self):
        fmt, structure = self.csdw_format
        raw = struct.unpack(fmt, self.packet.file.read(4))
        if structure is None:
            self.csdw = raw[0]
        else:
            for k, v in self._dissect(raw, structure):
                setattr(self, k, v)

    def parse_data(self):
        self.data = self.packet.file.read(self.packet.data_length - 4)
        if self.data_format is not None:
            fmt, structure = self.data_format
            raw = struct.unpack(fmt, self.data)
            for k, v in self._dissect(raw, structure):
                setattr(self, k, v)

    def __len__(self):
        return self.packet.data_length


class IterativeBase(Base):
    """Allows for easily packaging sub-elements into an iterable object based
    on an "all" attribute. Subclasses merely populate this attribute (a list)
    and length, iteration, etc. should just work.
    """

    item_label = None
    iph_format = None

    def __init__(self, *args, **kwargs):
        self.all = []
        Base.__init__(self, *args, **kwargs)

    def parse_data(self):
        if not self.iph_format:
            Base.parse_data(self)
        else:
            end = self.pos + self.packet.data_length
            while True:
                length = getattr(self, 'item_size', 0)
                fmt, structure = self.iph_format
                iph = {}
                if fmt is not None:
                    iph_size = struct.calcsize(fmt)
                    iph = struct.unpack(fmt, self.packet.file.read(iph_size))
                    iph = dict(self._dissect(iph, structure))
                    if 'length' in iph:
                        length = iph['length']

                data = self.packet.file.read(length)
                self.all.append(Item(data, self.item_label, **iph))

                # Account for filler byte when length is odd.
                if length % 2:
                    self.packet.file.seek(1, 1)

                if self.packet.file.tell() >= end:
                    break

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)


class Item(object):
    """The base container for packet data."""

    def __init__(self, data, label="Packet Data", **kwargs):
        self.__dict__.update(kwargs)
        self.data, self.label = data, label

    def __repr__(self):
        return '<%s>' % (self.label)

    def bytes(self):
        return self.data
