
from datetime import datetime, timedelta
import struct

import bitstring

from .base import Base


class BitArray(bitstring.BitArray):
    @property
    def int(self):
        if len(self):
            return bitstring.BitArray.int.fget(self)
        return 0


class Time(Base):
    data_attrs = Base.data_attrs + (
        'date_fmt',
        'leap',
        'time_fmt',
        'source',
        'time',
    )

    def parse(self):
        Base.parse(self)

        if self.format != 1:
            raise NotImplementedError('Time Data format %s is reserved!'
                                      % self.format)

        # 0 = IRIG day available
        # 1 = Month and year available
        self.date_fmt = self.csdw[-9]

        # Leap year flag
        self.leap = self.csdw[-8]

        # 0 = IRIG-B
        # 1 = IRIG-A
        # 2 = IRIG-G
        # 3 = Real-Time Clock
        # 4 = UTC Time from GPS
        # 5 = Native GPS Time
        # F = None (payload invalid)
        self.time_fmt = self.csdw[-7:-4].int

        # 0 = Internal (to the recorder)
        # 1 = External (to the recorder)
        # 2 = Internal from RMM
        # F = None
        self.source = self.csdw[-3:].int

        if self.date_fmt:
            data = struct.unpack('HHHH', self.data)
        else:
            data = struct.unpack('HHH', self.data)

        data = [BitArray(int=word, length=16) for word in data]
        # for arr in data:
        #     arr.byteswap()

        TSn = data[0][-14:-12].uint  # Tens of Seconds
        Sn = data[0][-12:-8].uint    # Seconds
        Hmn = data[0][-8:-4].uint    # Hundreds of milliseconds
        Tmn = data[0][-3:].uint      # Tens of milliseconds
        THn = data[1][-14:-12].uint  # Tens of hours
        Hn = data[1][-12:-8].uint    # Hours
        TMn = data[1][-6:-4].uint    # Tens of minutes
        Mn = data[1][-3:].uint       # Minutes

        microseconds = ((Hmn * 10) + Tmn)
        seconds = Sn + (TSn * 10)
        minutes = Mn + (TMn * 10)
        hours = Hn + (THn * 10)

        # IRIG day format
        if not self.date_fmt:
            HDn = data[2][-10:-8].uint  # Hundreds of days
            TDn = data[2][-7:-4].uint   # Tens of days
            Dn = data[2][-3:].uint      # Days

            day = Dn + (HDn * 100) + (TDn * 10)

            today = datetime.today()
            self.time = datetime(today.year, 1, 1) + timedelta(day - 1)

        # Month and Year Format
        else:
            TOn = data[2][-13:-12].uint  # Tens of months
            On = data[2][-11:-8].uint    # Months
            TDn = data[2][-7:-4].uint    # Tens of days
            Dn = data[2][-3:].uint       # Days
            OYn = data[3][-13:-12].uint  # Thousands of years
            HYn = data[3][-11:-8].uint   # Hundreds of years
            TYn = data[3][-7:-4].uint    # Tens of years
            Yn = data[3][-3:].uint       # Years

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
