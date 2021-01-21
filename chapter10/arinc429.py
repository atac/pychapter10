
from .util import BitFormat
from . import packet


class ARINC429F0(packet.Packet):
    """
    .. py:attribute:: count

        Number of ARINC 429 words in packet body.
    """

    csdw_format = BitFormat('''
        u16 count
        p16''')

    class Message(packet.Message):
        """
        .. py:attribute:: gap_time

            Gap time from the beginning of the preceding bus word (regardless \
of bus) to the beginning of the current bus word in 0.1-us increments.
        .. py:attribute:: bus_speed

            * 0 - low-speed bus (12.5kHz)
            * 1 - high-speed bus (100kHz)

        .. py:attribute:: parity_error
        .. py:attribute:: format_error
        .. py:attribute:: bus

            ARINC bus number (0-255)
        """
        FORMAT = BitFormat('''
            u16 gap_time

            u1 format_error
            u1 parity_error
            u1 bus_speed
            p1

            u4 gap_upper

            u8 bus
        ''', '211')
        length = 4

        # TODO: there should be a neater way to do this with bitstruct, but I
        # haven't found it yet.
        def __init__(self, *args, **kwargs):
            packet.Message.__init__(self, *args, **kwargs)
            self.gap_time += (self.gap_upper << 16)

        def __bytes__(self):
            old_gap = self.gap_time
            self.gap_upper = self.gap_time >> 16
            self.gap_time &= 0xffff
            b = packet.Message.__bytes__(self)
            self.gap_time = old_gap
            return b

        def __repr__(self):
            return '<ARINC-429 Data Word>'
