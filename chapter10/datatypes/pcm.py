
import struct

from .base import IterativeBase, Item


class PCM(IterativeBase):

    def parse(self):
        IterativeBase.parse(self)

        if self.format != 1:
            raise NotImplementedError(
                'PCM Format %s is reserved!' % self.format)

        # Channel Specific Data Word (csdw).
        self.iph = (self.csdw >> 30) & 0x1         # Intra-packet header
        self.ma = (self.csdw >> 29) & 0x1          # Major frame indicator
        self.mi = (self.csdw >> 28) & 0x1          # Minor frame indicator
        self.mifs = int((self.csdw >> 26) & 0b11)  # Major frame status
        self.mafs = int((self.csdw >> 24) & 0b11)  # Minor frame status
        self.align = (self.csdw >> 21) & 0x1       # Alignment mode
        self.throughput = (self.csdw >> 20) & 0x1  # Throughput mode
        self.packed = (self.csdw >> 19) & 0x1      # Packed mode
        self.unpacked = (self.csdw >> 18) & 0x1    # Unpacked mode
        self.s_offset = int(self.csdw & 0x3ffff)   # Sync offset

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

                iph = self.data[offset:offset + iph_len]
                iph, = struct.unpack('=H' if len(iph) == 2 else '=I', iph)
                attrs['lockst'] = int((iph >> 12) & 0xf)
                offset += iph_len
            data = self.data[offset:offset + frame_size]
            offset += frame_size
            self.all.append(Item(data, 'PCM Frame', **attrs))
