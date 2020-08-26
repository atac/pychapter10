
from .util import BitFormat
from .packet import Packet


class UARTF0(Packet):
    """
    .. py:attribute:: iph

    **Message Format**

    .. py:attribute:: ipts

        If enabled (see above), contains intra-packet timestamp

    .. py:attribute:: length

        Message length (bytes)

    .. py:attribute:: subchannel
    .. py:attribute:: parity_error
    """

    csdw_format = BitFormat('''
        p31
        u1 iph''')
    item_label = 'UART Data'

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        iph_format = ''
        if self.iph:
            iph_format = 'u64 ipts'
        self.iph_format = BitFormat(iph_format + '''
            u16 length
            u14 subchannel
            p1
            u1 parity_error''')
