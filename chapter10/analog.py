
from .util import BitFormat
from . import packet


class AnalogF1(packet.Packet):
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

    .. py:attribute:: subchannel_count

        Number of subchannels (and CSDWs) in the packet.

    .. py:attribute:: factor

        Exponent of power of 2 sampling rate factor denominator.

    .. py:attribute:: same

        Indicates whether this CSDW applies to all subchannels.

    """

    csdw_format = BitFormat('''
        u6 length
        u2 mode
        u8 subchannel
        u8 subchannel_count
        p3
        u1 same
        u4< factor
    ''')

    class Message(packet.Message):
        def __repr__(self):
            return '<Analog Sample %s bytes>' % len(self.data)

    def __init__(self, *args, **kwargs):
        packet.Packet.__init__(self, *args, **kwargs)

        self._subchannel = 0

        if self.length == 0:
            self.length = 16

        keys = (
            'mode',
            'length',
            'subchannel',
            'subchannel_count',
            'factor',
            'same')
        self.subchannels = [{k: getattr(self, k) for k in keys}]

        # Read CSDWs for subchannels if applicable.
        if not self.same:
            for i in range(self.subchannel_count):
                self.subchannels.append(
                    self.csdw_format.unpack(self.buffer.read(4)))

    def __next__(self):
        subchannel = self._subchannel
        if self.same:
            csdw = self.subchannels[0]
        else:
            csdw = self.subchannels[subchannel]

        # Find the sample size in bytes (16 bit aligned).
        length = csdw['length'] or 64  # Length 0 = 64 bits
        length = length // 8 + (length % 16 and 1 or 0)

        data = self.buffer.read(length)
        if len(data) < length:
            raise StopIteration

        # Account for filler byte when length is odd.
        if length % 2:
            self.packet.file.seek(1, 1)

        self._subchannel += 1

        return self.Message(data, parent=self, **csdw)
