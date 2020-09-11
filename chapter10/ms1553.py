
from .util import BitFormat
from . import packet


class MS1553F1(packet.Packet):
    """MIL-STD-1553B bus data

    .. py:attribute:: count

        Count of 1553 messages in the packet body.

    .. py:attribute:: time_tag_bits

        Indicates which bit of the message is time tagged:

        * 0 - Last bit of the last word of the message
        * 1 - First bit of the first word of the message
        * 2 - Last bit of the first (command) word of the message
    """

    csdw_format = BitFormat('''
        u24 count
        p6
        u2 time_tag_bits''')

    class Message(packet.Message):
        """
        .. py:attribute:: ipts
        .. py:attribute:: le

            Length error

        .. py:attribute:: se

            Sync type error

        .. py:attribute:: we

            Invalid word error

        .. py:attribute:: bus

            Bus ID (A/B)

        .. py:attribute:: me

            Message error

        .. py:attribute:: fe

            Format error

        .. py:attribute:: timeout
        .. py:attribute:: gap_time

            GAP1 indicates time (in tenths of us) between the command or data \
word and the first (and only) status word. GAP2 measures time between the \
last data word and the second status word.

        .. py:attribute:: length

            Message length (bytes)
        """

        def __repr__(self):
            return '<1553F1 message %s words>' % (len(self.data) // 2)

        # Note: bitfields from status word are listed in different order than
        # shown in the standard. bitstruct doesn't allow for specifying bit
        # order across multiple fields.
        FORMAT = BitFormat('''
            u64 ipts

            p2
            u1 le
            u1 se
            u1 we
            p3

            p2
            u1 bus
            u1 me
            p1
            u1 fe
            u1 timeout
            p1

            u16 gap_time
            u16 length''')


class MS1553F2(packet.Packet):
    """16PP194 Weapons Bus Data

    **Note:** the specifics of the data word format (bus ID, etc.) are not \
implemented here (yet).

    .. py:attribute:: count
    """

    csdw_format = BitFormat('u32 count')

    class Message(packet.Message):
        """
        .. py:attribute:: ipts
        .. py:attribute:: length

            IPDH length. Fixed at 24 bytes.

        .. py:attribute:: se

            Status error

        .. py:attribute:: ee

            Echo error

        .. py:attribute:: te

            Transaction error

        .. py:attribute:: re

            Master reset

        .. py:attribute:: tm

            Timeout
        """

        FORMAT = BitFormat('''
            u64 ipts
            u16 length
            u1 se
            p1
            u1 ee
            p3
            u1 te
            u1 re
            u1 tm
            p6''')

        def __repr__(self):
            return '<16PP194 Message %s words>' % (len(self.data) // 2)
