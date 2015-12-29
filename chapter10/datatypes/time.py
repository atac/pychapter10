
from datetime import datetime, timedelta
import struct

from .base import Base


class Time(Base):

    def parse(self):
        Base.parse(self)

        if self.format != 1:
            raise NotImplementedError('Time Data format %s is reserved!'
                                      % self.format)

        # 0 = IRIG day available
        # 1 = Month and year available
        self.date_fmt = (self.csdw >> 9) & 0x1

        # Leap year flag
        self.leap = (self.csdw >> 8) & 0x1

        # 0 = IRIG-B
        # 1 = IRIG-A
        # 2 = IRIG-G
        # 3 = Real-Time Clock
        # 4 = UTC Time from GPS
        # 5 = Native GPS Time
        # F = None (payload invalid)
        self.time_fmt = int((self.csdw >> 4) & 0xf)

        # 0 = Internal (to the recorder)
        # 1 = External (to the recorder)
        # 2 = Internal from RMM
        # F = None
        self.source = int(self.csdw & 0xf)

        if self.date_fmt:
            data = struct.unpack('HHHH', self.data)
        else:
            data = struct.unpack('HHH', self.data)

        # data = [BitArray(int=word, length=16) for word in data]
        # for arr in data:
        #     arr.byteswap()

        TSn = int((data[0] >> 12) & 0b111)  # Tens of Seconds
        Sn = int((data[0] >> 8) & 0xf)      # Seconds
        Hmn = int((data[0] >> 4) & 0xf)     # Hundreds of milliseconds
        Tmn = int(data[0] & 0xf)            # Tens of milliseconds

        THn = int((data[1] >> 12) & 0b11)  # Tens of hours
        Hn = int((data[1] >> 8) & 0xf)     # Hours
        TMn = int((data[1] >> 4) & 0b11)   # Tens of minutes
        Mn = int(data[1] & 0xf)            # Minutes

        microseconds = ((Hmn * 10) + Tmn)
        seconds = Sn + (TSn * 10)
        minutes = Mn + (TMn * 10)
        hours = Hn + (THn * 10)

        # IRIG day format
        if not self.date_fmt:
            HDn = int((data[2] >> 8) & 0b11)  # Hundreds of days
            TDn = int((data[2] >> 4) & 0xf)   # Tens of days
            Dn = int(data[2] & 0xf)           # Days

            day = Dn + (HDn * 100) + (TDn * 10)

            today = datetime.today()
            self.time = datetime(today.year, 1, 1) + timedelta(day - 1)

        # Month and Year Format
        else:
            TOn = int((data[2] >> 12) & 0b1)   # Tens of months
            On = int((data[2] >> 8) & 0xf)     # Months
            TDn = int((data[2] >> 4) & 0xf)    # Tens of days
            Dn = int(data[2] & 0xf)            # Days
            OYn = int((data[3] >> 12) & 0b11)  # Thousands of years
            HYn = int((data[3] >> 8) & 0xf)    # Hundreds of years
            TYn = int((data[3] >> 4) & 0xf)    # Tens of years
            Yn = int(data[3] & 0xf)            # Years

            month = On + (TOn * 10)
            day = Dn + (TDn * 10)
            year = Yn + (TYn * 10) + (HYn * 100) + (OYn * 1000)
            self.time = datetime(year, month, day)

        self.time = self.time.replace(
            microsecond=microseconds,
            second=seconds,
            minute=minutes,
            hour=hours,
            tzinfo=None)
