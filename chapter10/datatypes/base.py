

class Base(object):
    """Base for packet data. Reads out raw bytes and stores in an attribute."""

    # The names of any data attributes for lazy-loading.
    data_attrs = (
        'data',
    )

    def __init__(self, packet, no_skip=False):
        """Logs the file cursor location for later and skips past the data."""

        object.__init__(self)
        self.packet = packet

        # Whether data has been loaded.
        self.init = False

        # Store the file cursor position for the start of the body.
        self.start = self.packet.file.tell()

        # Skip past the data for now.
        if not no_skip:
            packet.file.seek(self.packet.dataLength, 1)

    def __load(self):
        """Moves the file cursor and calls parse method to load data."""

        # The cursor location at the time of data retrieval.
        oldPos = self.packet.file.tell()

        # Skip back to the packet body.
        self.packet.file.seek(self.start)

        # Run the customizable reader method.
        self.parse()

        # Return to the original cursor position.
        self.packet.file.seek(oldPos)

        # Log that we've actually parsed data.
        self.init = True

    def parse(self):
        """Called lazily (only when requested) to avoid memory overflows."""

        self.data = self.packet.file.read(self.packet.dataLength)

    def __getattribute__(self, name):
        """Loads packet data on demand."""

        if name != 'data_attrs' and name in self.data_attrs and not self.init:
            self.__load()
        return object.__getattribute__(self, name)
