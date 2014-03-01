import atexit

from packet import Packet


class C10(object):
    """A Chapter 10 parser."""

    def __init__(self, f, parse=True):
        """Takes a file or filename and reads packets."""

        if isinstance(f, str):
            f = open(f, 'rb')
            atexit.register(f.close)

        self.file = f

        self.packets= []

        if parse:
            self.parse_sequential()

    @classmethod
    def load(cls, f):
        c = cls(f, False)
        c.parse_careful()
        return c

    def parse_careful(self):
        """Search and parse packets one at a time."""

        while True:
            try:
                pos = self.file.tell()
                s = self.file.read(1024)
                if '\x25\xeb' in s:
                    i = pos + s.index('\x25\xeb')
                    self.file.seek(i)
                    p = Packet(self.file)
                    if p.check():
                        self.packets.append(p)
                    else:
                        self.file.seek(pos + 2)
                if not s:
                    break
            except EOFError:
                break

    def parse_sequential(self):
        """Parse a file assuming valid packets in exact sequence."""

        while True:
            try:
                self.packets.append(Packet(self.file))
            except EOFError:
                break

    def __repr__(self):
        return '<C10: {} {} bytes {} packets>'.format(
            self.file.name, self.size, len(self))

    @property
    def size(self):
        return sum(p.packet_length for p in self.packets)

    def __len__(self):
        return len(self.packets)

    def __iter__(self):
        return iter(self.packets)
