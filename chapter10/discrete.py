
from .util import BitFormat
from . import packet


class DiscreteF1(packet.Packet):
    """Discrete Format 1

    .. py:attribute:: mode

        * 0 - data is recorded when the state changes
        * 1 - data is recorded at a timed interval

    .. py:attribute:: length

        Bit length of data or 0 (32 bits)
    """

    csdw_format = BitFormat('''
        u3 mode
        u5 length
        p24''')

    class Message(packet.Message):
        """.. py:attribute:: ipts"""

        length = 4
        FORMAT = BitFormat('u64 ipts')

        def __repr__(self):
            return '<Discrete Data %s bytes>' % len(self.data)
