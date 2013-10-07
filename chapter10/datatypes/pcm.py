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
        channel_specific_data = f.read(4)
        bits = BitArray(bytes=channel_specific_data)
        iph = bits[30]
        self.iph = iph
        self.ma = bits[29]
        self.mi = bits[28]
        self.mafs = bits[27:26]
        self.mifs = bits[25:24]
        self.align = bits[21]
        self.through = bits[20]
        self.packed = bits[19]
        self.unpacked = bits[18]
        self.sync_offset = bits[17:0]

        frames = []
        frame_size = 5
        if iph:
            frame_size += 6
        for i in range(self.packet.dataLength - 4 / frame_size):
            frame = f.read(frame_size)
            frames.append(frame)
        self.frames = frames
