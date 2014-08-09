
import struct


class Base(object):
    """Base for packet data. Reads out raw bytes and stores in an attribute."""

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
        packet.file.seek(self.pos + self.packet.data_length)

        # Get our type and format.
        from . import format
        self.type, self.format = format(self.packet.data_type)

    def parse(self):
        """Called lazily (only when requested) to avoid memory overflows.
        Reads the Channel Specific Data Word (csdw) and data into attributes.
        """

        pos = self.packet.file.tell()
        self.packet.file.seek(self.pos)
        self.csdw = struct.unpack('I', self.packet.file.read(4))[0]
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


class Data(object):
    """A simple data container."""

    def __init__(self, label, data):
        self.label, self.data = label, data

    def __repr__(self):
        return '<%s data %s bytes>' % (self.label, len(self.data))
