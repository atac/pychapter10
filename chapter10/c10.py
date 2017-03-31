
import atexit
import os
import struct

from .packet import Packet, InvalidPacket
from .buffer import Buffer


class C10(object):
    """A Chapter 10 parser."""

    def __init__(self, f, lazy=False, packet=Packet):
        """Takes a file or filename and reads packets."""

        atexit.register(self.close)
        if isinstance(f, str):
            f = open(f, 'rb')
        self.file = f
        self.lazy = lazy
        self.packet = packet

    @classmethod
    def from_string(cls, s):
        return cls(Buffer(s))

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

        while True:
            pos = self.file.tell()
            try:
                return self.packet(self.file, self.lazy)
            except (struct.error, EOFError):
                raise StopIteration
            except InvalidPacket:
                # @TODO: search for sync pattern and start from there.
                self.file.seek(pos + 1)

    next = __next__

    def __repr__(self):
        return '<C10: {}>'.format(os.path.basename(self.file.name))

    def __iter__(self):
        return self
