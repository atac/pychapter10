import atexit

from packet import Packet

BUFFER_SIZE = 100000


class C10(object):
    """A Chapter 10 parser."""

    def __init__(self, f):
        """Takes a file or filename and reads packets."""

        atexit.register(self.close)
        if isinstance(f, str):
            f = open(f, 'rb')
        self.file = f

    def close(self):
        """Make sure we close our file if we can."""

        try:
            self.file.close()
        except:
            pass

    def next(self):
        try:
            pos = self.file.tell()
            s = self.file.read(BUFFER_SIZE)
            if not s:
                raise EOFError
            elif '\x25\xeb' in s:
                self.file.seek(pos + s.find('\x25\xeb'))
                p = Packet(self.file)
                self.file.seek(pos + p.packet_length)
                if p.check():
                    return p

            # Keep calling until we get a result or end.
            return self.next()
        except EOFError:
            raise StopIteration

    def __repr__(self):
        return '<C10: {}>'.format(self.file.name)

    def __iter__(self):
        return self
