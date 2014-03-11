
import struct

from .base import Base, Data


class IPH(object):
    def __init__(self, s, format):
        self.s = s

        if format == 1:
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
        elif format == 2:
            self.timestamp, self.length, self.status = struct.unpack('QHH', s)
            self.te = bool(self.status & (0x1 << 15))  # Transaction Error
            self.re = bool(self.status & (0x1 << 14))  # Reset
            self.tm = bool(self.status & (0x1 << 13))  # Message Time Out
            self.se = bool(self.status & (0x1 << 6))   # Status Error
            self.ee = bool(self.status & (0x1 << 3))   # Echo Error

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

        self.all, self.messages = [], []
        data = self.data[:]

        if self.format == 1:
            self.ttb = int(self.csdw >> 30)
            self.msg_count = int(self.csdw & 0xffffff)
            iph_len = 14

        elif self.format == 2:
            self.msg_count = int(self.csdw)
            iph_len = 12

        for i in range(self.msg_count):
            iph = IPH(data[:iph_len], self.format)
            data = data[iph_len:]
            self.all.append(iph)

            message = Data('Message', data[:iph.length])
            data = data[iph.length:]
            self.messages.append(message)
            self.all.append(message)
