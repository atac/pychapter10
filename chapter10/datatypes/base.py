

class Base(object):
    """Base for packet data. Reads out raw bytes and stores in an attribute."""

    # The names of any data attributes for lazy-loading.
    data_attrs = (
        'data',
    )

    def __init__(self, packet):
        """Logs the file cursor location for later and skips past the data."""

        self.packet = packet

        # Whether data has been loaded.
        self.init = False

        # Store the body position.
        self.start = self.packet.file.tell()

        # Skip to the packet trailer.
        packet.file.seek(self.packet.data_length, 1)

    def __load(self):
        """Moves the file cursor and calls parse method to load data."""

        pos = self.packet.file.tell()
        self.packet.file.seek(self.start)
        self.parse()
        self.packet.file.seek(pos)
        self.init = True

    def parse(self):
        """Called lazily (only when requested) to avoid memory overflows."""

        self.data = self.packet.file.read(self.packet.data_length)

    def __getattribute__(self, name):
        """Loads packet data on demand."""

        if name != 'data_attrs' and name in self.data_attrs and not self.init:
            self.__load()
        return object.__getattribute__(self, name)
