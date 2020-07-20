
from io import BytesIO
from array import array

from . import datatypes
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

    def __init__(self, file, lazy=False):
        """Takes an open file object with its cursor at this packet."""

        self.lazy = lazy

        self.file, self.pos = file, file.tell()

        # Read the packet header and save header sums for later.
        header = file.read(24)
        self.header_sums = sum(array('H', header)[:-1]) & 0xffff

        # Parse header fields into attributes.
        self.__dict__.update(self.FORMAT.unpack(header).items())

        # Read the secondary header (if any).
        self.time = None
        if self.secondary_header:
            secondary = file.read(12)
            self.secondary_sums = sum(array('H', secondary)[:-1]) & 0xffff
            self.__dict__.update(self.SECONDARY_FORMAT.unpack(file.read(12)))

        # Parse the body based on type.
        datatype = datatypes.get_handler(self.data_type)
        self.body = datatype(self)

        error = self.get_errors()
        if error:
            raise error

        # Skip packet body and trailer.
        # @TODO: parse trailer if present.
        self.file.seek(self.pos + self.packet_length)

    @classmethod
    def from_string(cls, s, lazy=False):
        """Create a packet object from a string."""

        return cls(BytesIO(s), lazy)

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
        return self.get_errors() is None

    def __len__(self):
        return len(self.body)

    def __iter__(self):
        return iter(self.body)

    def __bytes__(self):
        """Returns the entire packet as raw bytes."""

        pos = self.file.tell()
        self.file.seek(self.pos)
        raw = self.file.read(self.packet_length)
        self.file.seek(pos)
        if not isinstance(raw, bytes):
            raw = bytes(raw)
        return raw

    __str__ = __bytes__

    def __repr__(self):
        return '<C10 Packet {} {} bytes>'.format(self.data_type,
                                                 len(bytes(self)))

    def __setstate__(self, state):
        state['file'] = BytesIO(state['file'])
        state['pos'] = 0
        self.__dict__.update(state)

    def __getstate__(self):
        state, keys = {}, [
            'sync_pattern',
            'channel_id',
            'data_length',
            'data_type',
            'flags',
            'header_checksum',
            'header_sums',
            'header_version',
            'lazy',
            'packet_length',
            'rtc',
            'rtc_high',
            'rtc_low',
            'secondary_header',
            'secondary_checksum',
            'secondary_sums',
            'sequence_number',
            'sync_pattern',
            'time',
            'body',
            'pos',
        ]
        for k in keys:
            state[k] = getattr(self, k)
        state['file'] = bytes(self)
        return state
