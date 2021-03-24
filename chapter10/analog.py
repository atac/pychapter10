
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

    # u4 factor
    # u1 same
    # p3

    # u6 length
    # u2 mode

    # u8 subchannel_count

    # u8 subchannel
    csdw_format = BitFormat('''
        u8 one
        u8 two
        u8 three
        u8 four
    ''')

    class Message(packet.Message):
        def __repr__(self):
            return '<Analog Sample %s bytes>' % len(self.data)

        @classmethod
        def from_packet(cls, packet):
            subchannel = packet._subchannel
            if packet.same:
                csdw = packet.subchannels[0]
            else:
                csdw = packet.subchannels[subchannel]

            # Find the sample size in bytes (16 bit aligned).
            length = csdw['length'] or 64  # Length 0 = 64 bits
            length = length // 8 + (length % 16 and 1 or 0)

            data = packet.buffer.read(length)
            if len(data) < length:
                raise EOFError

            # Account for filler byte when length is odd.
            if length % 2:
                packet.buffer.seek(1, 1)

            packet._subchannel += 1
            if packet._subchannel >= len(packet.subchannels):
                packet._subchannel = 0

            return packet.Message(data, parent=packet, **csdw)

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
            for i in range(self.subchannel_count):
                raw = self.buffer.read(4)
                print('parse: ', raw)
                # assert 0
                self.subchannels.append(
                    self.csdw_format.unpack(raw))

    def _raw_body(self):
        raw = bytes()
        for channel in self.subchannels:
            print(channel)
            csdw = self.csdw_format.pack(channel)
            raw += csdw
        raw += b''.join([bytes(msg) for msg in list(self)])
        return raw
