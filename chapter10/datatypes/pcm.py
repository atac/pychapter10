
from bitstring import BitArray

from .base import IterativeBase, Item


class PCM(IterativeBase):

    data_attrs = IterativeBase.data_attrs + (
        'iph',
        'ma',
        'mi',
        'mafs',
        'mifs',
        'align',
        'throughput',
        'packed',
        'unpacked',
        's_offset',
    )

    def parse(self):
        IterativeBase.parse(self)

        if self.format != 1:
            raise NotImplementedError(
                'PCM Format %s is reserved!' % self.format)

        # Channel Specific Data Word (csdw).
        self.iph = self.csdw[-30]            # Intra-packet header
        self.ma = self.csdw[-29]             # Major frame indicator
        self.mi = self.csdw[-28]             # Minor frame indicator
        self.mafs = self.csdw[-27:-26].int   # Major frame status
        self.mifs = self.csdw[-25:-24].int   # Minor frame status
        self.align = self.csdw[-21]          # Alignment mode
        self.throughput = self.csdw[-20]     # Throughput mode
        self.packed = self.csdw[-19]         # Packed mode
        self.unpacked = self.csdw[-18]       # Unpacked mode
        self.s_offset = self.csdw[-17:].int  # Sync offset

        # Throughput basically means we don't need to do anything.
        if self.throughput:
            return

        # Figure the frame size for this packet (excluding IPH).
        frame_size = 12  # Two words sync, four data.
        iph_len = 0
        if self.iph:
            iph_len = 2

            # Extra IPH word in 32 bit alignment.
            if self.align:
                iph_len += 2

            frame_size += iph_len

        offset = 0
        for i in range(len(self.data) / frame_size):
            attrs = {}
            if self.iph:
                attrs['ipts'] = self.data[offset:offset + 8]
                offset += 8

                iph = BitArray(bytes=self.data[offset:offset + iph_len])
                iph.byteswap()
                attrs['lockst'] = iph[-15:-12].int
                offset += iph_len
            data = self.data[offset:offset + frame_size]
            offset += frame_size
            self.all.append(Item(data, 'PCM Frame', **attrs))
