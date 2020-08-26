
from .util import BitFormat
from .packet import Packet


class DiscreteF1(Packet):
    """Discrete Format 1

    .. py:attribute:: mode

        * 0 - data is recorded when the state changes
        * 1 - data is recorded at a timed interval

    .. py:attribute:: length

        Bit length of data or 0 (32 bits)

    **Message Format**

    .. py:attribute:: ipts
    """

    csdw_format = BitFormat('''
        u3 mode
        u5 length
        p24''')
    item_label = 'Discrete data'
    item_size = 4
    iph_format = BitFormat('u64 ipts')
