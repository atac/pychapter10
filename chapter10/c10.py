
from io import BytesIO
import os
import struct

from .packet import Packet, InvalidPacket
from .util import Buffer
from .computer import Computer
from .pcm import PCM
from .time import Time
from .ms1553 import MS1553
from .analog import Analog
from .discrete import Discrete
from .message import Message
from .arinc429 import ARINC429
from .video import Video
from .image import Image
from .uart import UART
from .i1394 import I1394
from .parallel import Parallel
from .ethernet import Ethernet

# Top level data types.
TYPES = (('Computer Generated', Computer),
         ('PCM', PCM),
         ('Time', Time),
         ('Mil-STD-1553', MS1553),
         ('Analog', Analog),
         ('Discrete', Discrete),
         ('Message', Message),
         ('ARINC 429', ARINC429),
         ('Video', Video),
         ('Image', Image),
         ('UART', UART),
         ('IEEE-1394', I1394),
         ('Parallel', Parallel),
         ('Ethernet', Ethernet),
         # ('TSPI/CTS Data', Base),
         # ('Controller Area Network Bus', Base),
         )


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
                try:
                    handler = TYPES[header['data_type'] // 8][1]
                except IndexError:
                    handler = Packet
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
