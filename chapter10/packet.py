from datatypes import Base, map
from array import array
import struct


class Packet(object):
    """A Packet object that reads the header and skips past the body and footer
    (storing the packet start position for later). The data only gets loaded
    if it's requested.
    """

    # the attribute names taken from header fields
    HEADER_KEYS = (
        ('Sync Pattern',                 'sync'),
        ('Channel ID',                   'channel'),
        ('Packet Length',                'length'),
        ('Data Length',                  'dataLength'),
        ('Header Version',               'headerVersion'),
        ('Sequence Number',              'sequence'),
        ('Packet Flags',                 'flags'),
        ('Data Type',                    'dataType'),
        ('Relative Time Counter (low)',  'RTCLow'),
        ('Relative Time Counter (high)', 'RTCHigh'),
        ('Header Checksum',              'checksum'),
    )

    def __init__(self, file):
        """Takes an open file object with its cursor at this packet."""

        object.__init__(self)
        self.file = file

        # Store the starting position of the packet within the file.
        self.filePos = file.tell()

        # Read out the raw header.
        header = file.read(24)

        # Make sure we're not reading beyond the file length.
        if not header:
            raise EOFError

        # Unpack the header.
        values = struct.unpack('HHIIBBBBIHH', header)

        # Store our header sums for the checksum.
        a = array('H')
        a.fromstring(header)
        self.sums = 0
        for part in a[:11]:
            self.sums += part
        self.sums &= 0xffff

        # Parse the header values into attributes.
        for i, header in enumerate(self.HEADER_KEYS):
            setattr(self, header[1], values[i])

        # Store the checksum value.
        self.checksums = self.checksum

        # Read the secondary header (if any).
        if self.flags & 0x7:

            # Read the raw secondary header.
            secondary = file.read(12)

            # Store our sums for checking later on.
            a = array('H')
            a.fromstring(secondary)
            sum = 0
            for part in a[:-1]:
                sum += part

            # the main attribute
            #@todo: make this convert to an actual time object!
            self.time = secondary[:8]

        # Find out what type of data we have and init the data class.
        datatype = map.get(self.dataType * 0x10, Base)
        self.body = datatype(self)

        # just skip past any footer data
        skip = len(self) - 24 - self.dataLength
        if self.flags & 0x7:
            skip -= 12
        file.seek(skip, 1)

    def printHeader(self):
        print '-' * 50
        for name, attr in self.HEADER_KEYS:
            print name + str(getattr(self, attr)).rjust(
                50 - len(name) - 2, '.')
        print self.check() and '(valid)' or '(error)'
        print '-' * 50

    def raw(self):
        """Returns the entire packet raw."""

        # Save our original cursor position.
        oldPos = self.file.tell()

        # Go to the start of the packet.
        self.file.seek(self.filePos)

        # Read out the correct amount of data.
        raw = self.file.read(self.length)

        # Return the cursor to its original position...
        self.file.seek(oldPos)

        # and send back the result.
        return raw

    def check(self):
        return (self.sums == self.checksums) and self.sync == 60197

    def __len__(self):
        return self.length
