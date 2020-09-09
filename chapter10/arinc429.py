
from .util import BitFormat
from .packet import Packet


class ARINC429F0(Packet):
    """
    .. py:attribute:: count

        Number of ARINC 429 words in packet body.

    **Message Format**

    .. py:attribute:: gap_time

        Gap time from the beginning of the preceding bus word (regardless of \
bus) to the beginning of the current bus word in 0.1-us increments.
    .. py:attribute:: bus_speed

        * 0 - low-speed bus (12.5kHz)
        * 1 - high-speed bus (100kHz)

    .. py:attribute:: parity_error
    .. py:attribute:: format_error
    .. py:attribute:: bus

        ARINC bus number (0-255)
    """

    csdw_format = BitFormat('''
        u16 count
        p16''')
    iph_format = BitFormat('''
        u16 gap_time

        u1 format_error
        u1 parity_error
        u1 bus_speed
        p1

        u4 gap_upper

        u8 bus
    ''', '211')
    item_size = 4
    item_label = 'ARINC-429 Data Word'

    # TODO: there should be a neater way to do this with bitstruct, but I
    # haven't found it yet.
    def __next__(self):
        item = Packet.__next__(self)
        item.gap_time += (item.gap_upper << 16)
        return item
