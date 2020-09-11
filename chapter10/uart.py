
from .util import BitFormat
from . import packet


class UARTF0(packet.Packet):
    """
    .. py:attribute:: iph
    """

    csdw_format = BitFormat('''<u32 iph''')

    class Message(packet.Message):
        """
        .. py:attribute:: ipts

            If enabled (see above), contains intra-packet timestamp

        .. py:attribute:: length

            Message length (bytes)

        .. py:attribute:: subchannel
        .. py:attribute:: parity_error
        """

        def __repr__(self):
            return '<UART data %s bytes>' % len(self.data)

    def __init__(self, *args, **kwargs):
        packet.Packet.__init__(self, *args, **kwargs)

        fmt = 'u64 ipts' if self.iph else ''
        fmt += '''
            u16 length
            u14 subchannel
            p1
            u1 parity_error'''
        self.Message.FORMAT = BitFormat(fmt)
