import atexit

from packet import Packet

BUFFER_SIZE = 100000


class C10(object):
    """A Chapter 10 parser."""

    def __init__(self, f):
        """Takes a file or filename and reads packets."""

        if isinstance(f, str):
            f = open(f, 'rb')
            atexit.register(f.close)

        self.file = f

    def next(self):
        try:
            return self.find_and_parse()
        except EOFError:
            raise StopIteration

    def find_and_parse(self):
        """Find the next sync pattern and attempt to read a packet."""

        pos = self.file.tell()
        s = self.file.read(BUFFER_SIZE)
        if not s:
            raise EOFError
        elif '\x25\xeb' in s:
            self.file.seek(pos + s.find('\x25\xeb'))
            p = Packet(self.file)
            if p.check():
                return p

        # Keep calling until we get a result or end.
        return self.find_and_parse()

    def __repr__(self):
        return '<C10: {} {} bytes {} packets>'.format(
            self.file.name, self.size, len(self))

    @property
    def size(self):
        return sum(p.packet_length for p in self)

    def __len__(self):
        return len([1 for i in self])

    def __iter__(self):
        return self
