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

        self.packets = []

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
                self.packets.append(self.find_and_parse())
            except EOFError:
                break

    def parse_sequential(self):
        """Parse a file assuming valid packets in exact sequence."""

        while True:
            try:
                self.packets.append(Packet(self.file))
            except EOFError:
                break

    def next(self):
        try:
            return self.find_and_parse()
        except EOFError:
            raise StopIteration

    def find_and_parse(self):
        """Find the next sync pattern and attempt to read a packet."""

        pos = self.file.tell()
        s = self.file.read(102400)
        if '\x25\xeb' in s:
            self.file.seek(pos + s.find('\x25\xeb'))
            p = Packet(self.file)
            if p.check():
                return p

        elif not s:
            raise EOFError

        # Keep calling until we get a result or end.
        return self.find_and_parse()

    def __repr__(self):
        return '<C10: {} {} bytes {} packets>'.format(
            self.file.name, self.size, len(self))

    @property
    def size(self):
        return sum(p.packet_length for p in self.packets)

    def __len__(self):
        return len(self.packets)

    def __iter__(self):
        return self
