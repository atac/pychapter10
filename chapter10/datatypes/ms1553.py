
import struct

from .base import Base, Data


class IPH(object):
    def __init__(self, s):

        self.s = s
        self.timestamp = s[:8]
        status, self.gap, self.length = struct.unpack('HHH', s[8:])
        self.bid = bool(status & (0x1 << 13))  # Bus ID (A/B)
        self.me = bool(status & (0x1 << 12))   # Message Error
        self.rr = bool(status & (0x1 << 11))   # RT to RT Transfer
        self.fe = bool(status & (0x1 << 10))   # Format Error
        self.tm = bool(status & (0x1 << 9))    # Response Time Out
        self.le = bool(status & (0x1 << 5))    # Word Count Error
        self.se = bool(status & (0x1 << 4))    # Sync Type Error
        self.we = bool(status & (0x1 << 3))    # Invalid Word Error

    def __str__(self):
        return self.s


class MS1553(Base):
    data_attrs = Base.data_attrs + (
        'messages',
        'all',
        'ttb',
        'msg_count',
    )

    def parse(self):
        Base.parse(self)

        if self.format == 0:
            raise NotImplementedError('1553 Format %s is reserved!'
                                      % self.format)

        self.ttb = int(self.csdw >> 30)
        self.msg_count = int(self.csdw & 0xffffff)

        self.all, self.messages = [], []

        data = self.data[:]
        for i in range(self.msg_count):
            iph = IPH(data[:14])
            data = data[14:]
            self.all.append(iph)

            message = Data('Message', data[:iph.length])
            data = data[iph.length:]
            self.messages.append(message)
            self.all.append(message)
