
from io import BytesIO
import os
import struct

from .packet import Packet, InvalidPacket
from .util import Buffer
from . import datatypes


class C10(object):
    """A Chapter 10 parser."""

    def __init__(self, f, packet=Packet):
        """Takes a file or filename and reads packets."""

        if isinstance(f, str):
            f = open(f, 'rb')
        self.file = Buffer(f)
        self.packet = packet

    @classmethod
    def from_string(cls, s):
        """Create a C10 object from a string or bytes."""

        return cls(BytesIO(s))

    def __next__(self):
        """Walk a chapter 10 file using python's iterator protocol and return
        a chapter10.packet.Packet object for each valid packet found.
        """

        while True:
            pos = self.file.tell()
            try:
                header = Packet.FORMAT.unpack(self.file.read(24))
                handler = datatypes.get_handler(header['data_type'])
                self.file.seek(pos)
                return handler(self.file)
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
