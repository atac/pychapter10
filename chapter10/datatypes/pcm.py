from array import array

from base import Base
from bitstring import BitArray


class PCM(Base):

    data_attrs = (
        'frames',
        'iph',
        'ma',
        'mi',
        'mafs',
        'mifs',
        'align',
        'through',
        'packed',
        'unpacked',
    )

    frames = []

    def __iter__(self):
        return iter(self.frames)

    def parse(self):
        f = self.packet.file
        channel_specific_data = array('H', f.read(4))
        channel_specific_data.byteswap()
        bits = BitArray(bytes=channel_specific_data.tostring())
        self.iph = bits[30]
        self.ma = bits[29]
        self.mi = bits[28]
        self.mafs = bits[26:27]
        self.mifs = bits[24:25]
        self.align = bits[21]
        self.through = bits[20]
        self.packed = bits[19]
        self.unpacked = bits[18]
        self.sync_offset = bits[0:17]

        frames = []
        frame_size = 5
        # If IPH is set and not in throughput mode.
        if bits[28] and not bits[20]:
            frame_size += 5
            if bits[21]:
                frame_size += 1

        # If throughput mode
        if bits[20]:
            read = f.read(self.packet.data_length- 4)
            s = BitArray(bytes=read)
        else:
            print self.packet.data_length
            for i in range(self.packet.data_length- 4 / frame_size):
                frame = f.read(frame_size)
                return
                frames.append(frame)
        self.frames = frames
