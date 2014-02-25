from datatypes import Base, map
from array import array
import struct


class Packet(object):
    """Reads header and associates a data type specific object."""

    # The attribute names for header fields.
    HEADER_KEYS = (
        ('Sync Pattern',                 'sync'),
        ('Channel ID',                   'channel'),
        ('Packet Length',                'length'),
        ('Data Length',                  'data_length'),
        ('Header Version',               'header_version'),
        ('Sequence Number',              'sequence'),
        ('Packet Flags',                 'flags'),
        ('Data Type',                    'data_type'),
        ('Relative Time Counter (low)',  'rtc_low'),
        ('Relative Time Counter (high)', 'rtc_high'),
        ('Header Checksum',              'checksum'),
    )

    def __init__(self, file):
        """Takes an open file object with its cursor at this packet."""

        self.file = file

        # Store the starting position of the packet within the file.
        self.pos = file.tell()

        # Read out the raw header.
        header = file.read(24)

        # Make sure we're not reading beyond the file length.
        if len(header.strip()) < 24:
            raise EOFError

        # Store our header sums for the checksum.
        a = array('H')
        a.fromstring(header)
        self.sums = sum(a[:11])

        # Parse the header values into attributes.
        values = struct.unpack('HHIIBBBBIHH', header)
        for i, field in enumerate(self.HEADER_KEYS):
            setattr(self, field[1], values[i])

        # Read the secondary header (if any).
        if self.flags & 0x7:

            secondary = file.read(12)

            # Store our sums for checking later on.
            a = array('H')
            a.fromstring(secondary)
            self.sums += sum(a[:-1])

            #@todo: make this convert to an actual time object!
            self.time = secondary[:8]

        # Find out what type of data we have and init the data class.
        datatype = map.get(self.data_type, Base)
        self.body = datatype(self)

        # Skip past any footer data
        skip = len(self) - 24 - self.data_length
        if self.flags & 0x7:
            skip -= 12
        file.seek(skip, 1)

    def print_header(self):
        """Print out the header information."""

        print '-' * 80
        for name, attr in self.HEADER_KEYS:
            print name + str(getattr(self, attr)).rjust(
                80 - len(name) - 2, '.')
        print self.check() and '(valid)' or '(error)'
        print '-' * 80

    def raw(self):
        """Returns the entire packet as raw bytes."""

        pos = self.file.tell()
        self.file.seek(self.pos)
        raw = self.file.read(self.length)
        self.file.seek(pos)

        return raw

    def check(self):
        """Validate the packet using checksums and verifying fields."""

        return (self.sums == self.checksum) and self.sync == 60197

    def __len__(self):
        return self.length
