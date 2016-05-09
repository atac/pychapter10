
from array import array
import struct

from . import datatypes
from .buffer import Buffer


class Packet(object):
    """Reads header and associates a datatype specific object."""

    # Attribute names for header fields.
    HEADER_KEYS = (
        'Sync Pattern',
        'Channel ID',
        'Packet Length',
        'Data Length',
        'Header Version',
        'Sequence Number',
        'Flags',
        'Data Type',
        'RTC Low',
        'RTC High',
        'Header Checksum'
    )

    def __init__(self, file, lazy=False):
        """Takes an open file object with its cursor at this packet."""

        self.lazy = lazy

        # Mark our location in the file and read the header.
        self.file, self.pos = file, file.tell()

        # Read the packet header and save header sums for later (masked for bit
        # length).
        header = file.read(24)
        if len(header) < 24:
            raise EOFError
        self.header_sums = sum(array('H', header)[:-1]) & 0xffff

        # Parse header fields into attributes.
        values = struct.unpack('HHIIBBBBIHH', header)
        for i, field in enumerate(self.HEADER_KEYS):
            setattr(self, '_'.join(field.split()).lower(), values[i])

        self.rtc, = struct.unpack(
            'Q', struct.pack('IHxx', self.rtc_low, self.rtc_high))

        # Read the secondary header (if any).
        self.time = None
        self.secondary_sums, self.secondary_checksum = (None, None)
        if self.flags & (1 << 7):
            secondary = file.read(12)
            if len(secondary) < 12:
                raise EOFError

            # Store our sums for checking later on (masked for bit length).
            self.secondary_sums = sum(array('H', secondary)[:-1]) & 0xffff

            # Parse the secondary header time and checksum.
            self.time, self.secondary_checksum = struct.unpack('qxxH',
                                                               secondary)

        # Parse the body based on type.
        datatype = datatypes.get_handler(self.data_type)
        self.body = datatype(self)

        # Skip trailer @TODO: parse trailer if present.
        self.file.seek(self.pos + self.packet_length)

    @classmethod
    def from_string(cls, s, lazy=False):
        """Create a packet object from a string."""

        return cls(Buffer(s), lazy)

    def check(self):
        """Validate the packet using checksums and verifying fields."""

        if self.sync_pattern != 0xeb25:
            return False
        elif self.header_sums != self.header_checksum:
            return False
        elif self.secondary_sums != self.secondary_checksum:
            return False
        elif self.data_length > 524288:
            return False
        return True

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
        return raw

    __str__ = __bytes__

    def __repr__(self):
        return '<C10 Packet {} {} bytes>'.format(self.data_type, len(self))
