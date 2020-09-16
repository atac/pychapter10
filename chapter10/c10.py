
from io import BytesIO
import os

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
from .video import VideoF0, VideoF1, VideoF2
from .image import ImageF0, ImageF1, ImageF2
from .uart import UARTF0
from .i1394 import I1394F0, I1394F1
from .parallel import ParallelF0
from .ethernet import EthernetF0, EthernetF1

__all__ = ('TYPES', 'C10')

# Top level data types.
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
    0x40: VideoF0,
    0x41: VideoF1,
    0x42: VideoF2,
    0x48: ImageF0,
    0x49: ImageF1,
    0x4A: ImageF2,
    0x50: UARTF0,
    0x58: I1394F0,
    0x59: I1394F1,
    0x60: ParallelF0,
    0x68: EthernetF0,
    0x69: EthernetF1,
}


class C10(object):
    """A Chapter 10/11 parser.

    :param f: A file like object or file path to read from.
    :type f: file or str
    """

    def __init__(self, f):
        if isinstance(f, str):
            f = open(f, 'rb')
        self.file = Buffer(f)

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
                handler = TYPES.get(header['data_type'], None)
                if handler:
                    return handler(self.file, **header)

                raise NotImplementedError('Type %s not implemented' %
                                          hex(header['data_type']))
            except EOFError:
                raise StopIteration
            except InvalidPacket:
                self.file.seek(pos + 1)

    def __repr__(self):
        return '<C10: {}>'.format(os.path.basename(self.file.name))

    def __iter__(self):
        return self
