
from io import BytesIO
from array import array

from .util import compile_fmt


class InvalidPacket(Exception):
    pass


class Packet(object):
    """Reads header and associates a datatype specific object."""

    FORMAT = compile_fmt('''
        u16 sync_pattern
        u16 channel_id
        u32 packet_length
        u32 data_length
        u8 header_version
        u8 sequence_number
        u1 secondary_header
        u1 ipts_source
        u1 rtc_sync_error
        u1 data_overflow_error
        u2 secondary_format
        u2 data_checksum_present
        u8 data_type
        u48 rtc
        u16 header_checksum''')

    SECONDARY_FORMAT = compile_fmt('''
        u64 secondary_time
        p16 reserved
        u16 secondary_checksum''')

    csdw_format = None
    iph_format = None
    item_label = None
    item_size = None

    def __init__(self, file):
        """Takes an open file object with its cursor at this packet."""

        # Read the packet header and save header sums for later.
        header = file.read(24)
        self.header_sums = sum(array('H', header)[:-1]) & 0xffff
        self.__dict__.update(self.FORMAT.unpack(header).items())

        # Read the secondary header (if any).
        self.time = None
        secondary = bytes()
        if self.secondary_header:
            secondary = file.read(12)
            self.secondary_sums = sum(array('H', secondary)[:-1]) & 0xffff
            self.__dict__.update(self.SECONDARY_FORMAT.unpack(file.read(12)))

        header_size = len(header + secondary)
        body = file.read(self.packet_length - header_size)
        self.file = BytesIO(header + secondary + body)
        self.file.seek(header_size)

        error = self.get_errors()
        if error:
            raise error

        self.type = self.data_type // 8
        self._format = self.data_type % 8
        self.parse()

    def parse(self):
        """Seek to packet body, call type-specific parsing, and return file
        to its previous index.
        """

        self.parse_csdw()
        self.parse_data()

    def parse_csdw(self):
        if self.csdw_format:
            raw = self.file.read(4)
            self.__dict__.update(self.csdw_format.unpack(raw))

    def parse_data(self):
        if not self.item_label:
            data_len = self.packet_length - (
                self.secondary_header and 36 or 24)
            self.data = self.file.read(data_len - 4)

    def __next__(self):
        """Return the next message until the end, then raise StopIteration."""

        # Exit when we reach the end of the packet body
        end = self.data_length + (self.secondary_header and 36 or 24)
        if self.file.tell() >= end:
            raise StopIteration

        # Read and parse the IPH
        raw = self.file.read(self.iph_format.calcsize() // 8)
        iph = self.iph_format.unpack(raw)

        # Read the message data
        length = getattr(self, 'item_size', 0)
        if 'length' in iph:
            length = iph['length']
        data = self.file.read(length)

        # Account for filler byte when length is odd.
        if length % 2:
            self.file.seek(1, 1)

        return Item(data, self.item_label, self.iph_format, **iph)

    def __iter__(self):
        return self

    @classmethod
    def from_string(cls, s):
        """Create a packet object from a string."""

        return cls(BytesIO(s))

    def get_errors(self):
        """Validate the packet using checksums and verifying fields."""

        if self.sync_pattern != 0xeb25:
            return InvalidPacket('Incorrect sync pattern!')
        elif self.header_sums != self.header_checksum:
            return InvalidPacket('Header checksum mismatch!')
        elif self.secondary_header:
            if self.secondary_sums != self.secondary_checksum:
                return InvalidPacket('Secondary header checksum mismatch!')
        elif self.data_length > 524288:
            return InvalidPacket('Data length larger than allowed!')

    def check(self):
        """Return validity boolean. See get_errors method."""

        return self.get_errors() is None

    def __len__(self):
        """Return length if we can find one, else raise NotImplementedError."""

        if hasattr(self, 'count'):
            return self.count
        elif self.item_size:
            msg_size = self.item_size + (self.iph_format.calcsize() // 8)
            return (self.data_length - 4) // msg_size
        raise NotImplementedError('%s has no len' % self.__class__)

    def __bytes__(self):
        """Returns the entire packet as raw bytes."""

        self.file.seek(0)
        return self.file.read()

    def __repr__(self):
        return '<{} {} bytes>'.format(
            self.__class__.__name__, len(bytes(self)))

    def __setstate__(self, state):
        state['file'] = BytesIO(state['file'])
        self.__dict__.update(state)

    def __getstate__(self):
        state = self.__dict__.copy()
        state['file'] = bytes(self)
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
        return '<%s %s bytes>' % (self.label, len(self.data))

    def __bytes__(self):
        return self.pack()

    def __str__(self):
        return str(self.pack())

    def pack(self, format=None):
        """Return bytes() containing the item's IPH and data."""

        if format is None:
            format = self.item_format
        return format.pack(self.__dict__) + self.data
