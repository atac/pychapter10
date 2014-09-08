import atexit
import os

from .packet import Packet

BUFFER_SIZE = 100000000
SYNC = b'\x25\xeb'


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

    def __next__(self):
        """Walk a chapter 10 file using python's iterator protocol and return
        a chapter10.packet.Packet object for each valid packet found.
        """

        try:

            # Read BUFFER_SIZE.
            pos = self.file.tell()
            s = self.file.read(BUFFER_SIZE)
            if not s:
                raise EOFError

            # If we find a sync pattern, try to parse a packet header.
            if SYNC in s:
                self.file.seek(pos + s.find(SYNC))
                p = Packet(self.file)
                if p.check():
                    self.file.seek(pos + p.packet_length)
                    return p
                else:
                    self.file.seek(p.pos + 1)

            # If no packet then keep calling until we get a result or eof.
            return self.__next__()

        except EOFError:
            raise StopIteration

    next = __next__

    def __repr__(self):
        return '<C10: {}>'.format(os.path.basename(self.file.name))

    def __iter__(self):
        return self
