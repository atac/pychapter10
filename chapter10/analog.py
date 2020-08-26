
from .util import BitFormat
from .packet import Packet, Item


class AnalogF1(Packet):
    """
    .. py:attribute:: mode

        Indicates packing and aligmnent mode.

        * 0 - Packed
        * 1 - Unpacked, lsb padded
        * 3 - Unpacked, msb padded

    .. py:attribute:: length

        Bit length of samples.

    .. py:attribute:: subchannel

        Subchannel ID

    .. py:attribute:: channel_count

        Number of subchannels (and CSDWs) in the packet.

    .. py:attribute:: factor

        Exponent of power of 2 sampling rate factor denominator.

    .. py:attribute:: same

        Indicates whether this CSDW applies to all subchannels.

    """

    csdw_format = BitFormat('''
        u2 mode
        u6 length
        u8 subchannel
        u8 channel_count
        u4 factor
        u1 same
        p2''')
    item_label = 'Analog Sample'

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        self._subchannel = 0

        keys = (
            'mode', 'length', 'subchannel', 'channel_count', 'factor', 'same')
        self.subchannels = [[getattr(self, k) for k in keys]]

        # Read CSDWs for subchannels if applicable.
        if not self.same:
            for i in range(len(self)):
                self.subchannels.append(
                    self.csdw_format.unpack(self.file.read(4)))

    def __len__(self):
        return self.channel_count or 256

    def __next__(self):
        subchannel = self._subchannel
        if self.same:
            csdw = self.subchannels[0]
        else:
            csdw = self.subchannels[subchannel]

        # Find the sample size in bytes (16 bit aligned).
        length = csdw['length'] or 64  # Length 0 = 64 bits
        length = length // 8 + (length % 16 and 1 or 0)

        data = self.file.read(length)

        # Account for filler byte when length is odd.
        if length % 2:
            self.packet.file.seek(1, 1)

        self._subchannel += 1

        return Item(data, self.item_label, **csdw)
