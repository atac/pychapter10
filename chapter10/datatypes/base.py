

class Base(object):
    """Base object for packet data. All data types include a "csdw" attribute
    containing the channel specific raw data word (or words in some cases), and
    a "data" attribute containing the raw packet data. Subclasses should extend
    the parse method to process the raw data into more useful forms.
    """

    csdw_format = None
    data_format = None
    # TODO: rename to message label & format?
    iph_format = None
    item_label = None

    def __init__(self, packet):
        """Logs the file cursor location for later and skips past the data."""

        self.packet = packet

        # Get our type and format.
        from . import format
        self.type, self._format = format(self.packet.data_type)
        self.parse()

    def parse(self):
        """Seek to packet body, call type-specific parsing, and return file
        to its previous index.
        """

        self.parse_csdw()
        self.parse_data()

    def parse_csdw(self):
        if self.csdw_format:
            self.__dict__.update(self.csdw_format.unpack(
                self.packet.file.read(4)))

    def parse_data(self):
        self.all = []
        if not self.iph_format:
            data_len = self.packet.packet_length - (
                self.packet.secondary_header and 36 or 24)
            self.data = self.packet.file.read(data_len - 4)
            if self.data_format is not None:
                raw = self.data[:self.data_format.calcsize()]
                self.__dict__.update(self.data_format.unpack(raw))
        else:
            end = self.packet.file.tell() - 4 + self.packet.data_length
            while True:
                length = getattr(self, 'item_size', 0)

                iph_size = self.iph_format.calcsize() // 8
                raw = self.packet.file.read(iph_size)
                iph = self.iph_format.unpack(raw)

                if 'length' in iph:
                    length = iph['length']

                data = self.packet.file.read(length)
                self.all.append(Item(data, self.item_label, self.iph_format,
                                     **iph))

                # Account for filler byte when length is odd.
                if length % 2:
                    self.packet.file.seek(1, 1)

                if getattr(self, 'count', None) and len(self) == self.count:
                    break

                if self.packet.file.tell() >= end:
                    break

    # TODO: switch to a generator instead of building .all immediately?
    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getstate__(self):
        state = self.__dict__.copy()
        for k, v in list(state.items()):
            if callable(v):
                del state[k]
        return state


class Item(object):
    """The base container for packet data."""

    def __init__(self, data, label="Packet Data", item_format=None, **kwargs):
        self.__dict__.update(kwargs)
        self.item_format = item_format
        self.data, self.label = data, label

    def __repr__(self):
        return '<%s>' % (self.label)

    def bytes(self):
        return self.data

    def __bytes__(self):
        return self.pack()

    def __str__(self):
        return str(self.pack())

    def pack(self, format=None):
        """Return bytes() containing the item's IPH and data."""

        if format is None:
            format = self.item_format
        return format.pack(self.__dict__)
