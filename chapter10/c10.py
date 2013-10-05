from packet import Packet


class C10(object):
    """A Chapter 10 parser."""

    def __init__(self, f):
        """Takes a file or filename and reads packets."""

        object.__init__(self)

        if type(f) == str:
            f = open(f, 'rb')

        self.file = f

        # Parse packets until the file is empty.
        self.packets = []
        self.size = 0
        self.parse(self.file)

    def parse(self, src):
        while True:
            try:
                packet = Packet(src)
                self.packets.append(packet)
                self.size += len(packet)
            except EOFError:
                break

    def __repr__(self):
        return '<C10: {} {} bytes {} packets>'.format(
            self.file,
            self.size, len(self))

    def __len__(self):
        return len(self.packets)

    def __iter__(self):
        return iter(self.packets)
