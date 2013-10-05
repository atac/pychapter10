from base import Base


class PCM(Base):

    def parse(self):
        f = self.packet.file
        channel_specific_data = f.read(4)
