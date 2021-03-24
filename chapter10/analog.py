
from .util import BitFormat
from . import packet

from bitstring import Bits


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
        u4 factor
    ''')

    class Message(packet.Message):
        def __repr__(self):
            return '<Analog Sample %s bits>' % len(self.length)

        @classmethod
        def from_packet(cls, packet):
            subchannel = packet._subchannel
            if packet.same:
                csdw = packet.subchannels[0]
            else:
                csdw = packet.subchannels[subchannel]

            # Find the sample size in bytes (16 bit aligned).
            length = csdw['length'] or 64  # Length 0 = 64 bits

            if packet.bit_offset > len(packet.data):
                raise EOFError

            data = packet.data[packet.bit_offset:packet.bit_offset + length]
            packet.bit_offset += length

            packet._subchannel += 1
            if packet._subchannel >= len(packet.subchannels):
                packet._subchannel = 0

            return packet.Message(data.bytes, parent=packet, **csdw)

        def __bytes__(self):
            return self.data

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

        # Read CSDWs for additional subchannels if applicable.
        if not self.same:
            for i in range(self.subchannel_count - 1):
                self.subchannels.append(
                    self.csdw_format.unpack(self.buffer.read(4)))

        # Get the raw bytes of data since samples are specified in bit length
        raw = self.buffer.read(
            self.data_length - (4 * len(self.subchannels)))
        self.data = Bits(raw)
        self.bit_offset = 0

    def _raw_body(self):
        raw = bytes()
        for channel in self.subchannels:
            raw += self.csdw_format.pack(channel)
        raw += b''.join(bytes(msg) for msg in self._messages)
        return raw
