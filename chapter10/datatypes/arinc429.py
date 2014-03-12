
from .base import Base, Data


class ARINC429(Base):
    data_attrs = Base.data_attrs + (
        'all',
        'words',
        'msg_count')

    def parse(self):
        Base.parse(self)

        if self.format > 0:
            raise NotImplementedError('ARINC-429 format %s is reserved!'
                                      % self.format)

        self.msg_count = int(self.csdw & 0xf)

        data = self.data[:]
        self.all, self.words = [], []
        for i in range(self.msg_count):
            iph = Data('IPH', data[:4])
            data = data[4:]
            self.all.append(iph)

            words = Data('ARINC429 Word', data[:4])
            data = data[4:]
            self.words.append(words)
            self.all.append(words)
