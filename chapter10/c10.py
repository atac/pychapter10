from packet import Packet
import os


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
        while True:
            try:
                packet = Packet(self.file)
                self.packets.append(packet)
                self.size += len(packet)
            except EOFError:
                break

    def repr(self):
        return '<C10: {} bytes {} packets>'.format(
            os.path.abspath(self.file.name),
            self.size, len(self))

    def __len__(self):
        return len(self.packets)

    def __iter__(self):
        return iter(self.packets)
