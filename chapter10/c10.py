
from io import BytesIO
import os
import struct

from .packet import Packet, InvalidPacket
from .util import Buffer
from .computer import ComputerF0, ComputerF1, ComputerF2, ComputerF3
from .pcm import PCMF1
from .time import TimeF1
from .ms1553 import MS1553F1, MS1553F2
from .analog import AnalogF1
from .discrete import DiscreteF1
from .message import MessageF0
from .arinc429 import ARINC429F0
from .video import Video
from .image import Image
from .uart import UART
from .i1394 import I1394
from .parallel import Parallel
from .ethernet import Ethernet

# Top level data types.
TYPES_LIST = (('Computer Generated', ComputerF1),
              ('PCM', PCMF1),
              ('Time', TimeF1),
              ('Mil-STD-1553', MS1553F1),
              ('Analog', AnalogF1),
              ('Discrete', DiscreteF1),
              ('Message', MessageF0),
              ('ARINC 429', ARINC429F0),
              ('Video', Video),
              ('Image', Image),
              ('UART', UART),
              ('IEEE-1394', I1394),
              ('Parallel', Parallel),
              ('Ethernet', Ethernet),
              # ('TSPI/CTS Data', Base),
              # ('Controller Area Network Bus', Base),
              )

TYPES = {
    0x00: ComputerF0,
    0x01: ComputerF1,  # TMATS
    0x02: ComputerF2,  # Event
    0x03: ComputerF3,  # Index
    0x09: PCMF1,
    0x11: TimeF1,
    0x19: MS1553F1,
    0x1A: MS1553F2,
    0x21: AnalogF1,
    0x29: DiscreteF1,
    0x30: MessageF0,
    0x38: ARINC429F0,
}


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
                    handler = TYPES[header['data_type']]
                except KeyError:
                    handler = TYPES_LIST[header['data_type'] // 8][1]
                except IndexError:
                    raise NotImplementedError('Type %s not implemented',
                                              hex(header['data_type'])[2:])
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
