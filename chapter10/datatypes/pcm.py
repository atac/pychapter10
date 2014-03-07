
from .base import Base, Data


class PCM(Base):

    data_attrs = Base.data_attrs + (
        'all',
        'frames',
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
        Base.parse(self)

        if self.format != 1:
            raise NotImplementedError(
                'PCM Format %s is reserved!' % self.format)

        # Channel Specific Data Word (csdw).
        self.iph = bool(self.csdw & (1 << 30))         # Intra-packet header
        self.ma = bool(self.csdw & (1 << 29))          # Major frame indicator
        self.mi = bool(self.csdw & (1 << 28))          # Minor frame indicator
        self.mafs = int(self.csdw >> 26 & 0b11)        # Major frame status
        self.mifs = int(self.csdw >> 24 & 0b11)        # Minor frame status
        self.align = bool(self.csdw & (1 << 21))       # Alignment mode
        self.throughput = bool(self.csdw & (1 << 20))  # Throughput mode
        self.packed = bool(self.csdw & (1 << 19))      # Packed mode
        self.unpacked = bool(self.csdw & (1 << 18))    # Unpacked mode
        self.s_offset = int(self.csdw & 262143)        # Sync offset

        self.frames, self.all = [], []

        # Throughput basically means we don't need to do anything.
        if self.throughput:
            return

        # Figure the frame size for this packet (including IPH).
        frame_size = 5  # Two words sync, three data.
        if self.iph:
            iph = 5

            # Extra IPH word in 32 bit alignment.
            if self.align:
                iph += 1

            frame_size += iph

        data = self.data[:]
        for i in range(len(data) / frame_size):
            if self.iph:
                all.append(Data('IPH', data[:iph]))
                data = data[iph:]
            frame = Data('PCM Frame', data[:5])
            self.frames.append(frame)
            self.all.append(frame)
            data = data[5:]

    def __iter__(self):
        return iter(self.all)

    def __len__(self):
        return len(self.all)
