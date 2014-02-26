import atexit

from packet import Packet


class C10(object):
    """A Chapter 10 parser."""

    def __init__(self, f):
        """Takes a file or filename and reads packets."""

        if isinstance(f, str):
            f = open(f, 'rb')
            atexit.register(f.close)

        self.file = f

        # Parse headers until EOF
        self.packets, self.size = [], 0
        while True:
            try:
                self.packets.append(Packet(f))
                self.size += len(self.packets[-1])
            except EOFError:
                break

    def __repr__(self):
        return '<C10: {} {} bytes {} packets>'.format(
            self.file.name, self.size, len(self))

    def __len__(self):
        return len(self.packets)

    def __iter__(self):
        return iter(self.packets)
