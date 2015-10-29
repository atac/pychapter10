
from datetime import datetime, timedelta
import struct

from bitstring import BitArray

from .base import Base


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

        data = [BitArray(word) for word in data]
        for arr in data:
            arr.byteswap()

        TSn = data[0][-14:-12].int  # Tens of Seconds
        Sn = data[0][-11:-8].int    # Seconds
        Hmn = data[0][-7:-4].int    # Hundreds of milliseconds
        Tmn = data[0][-3:].int      # Tens of milliseconds
        THn = data[1][-14:-12].int  # Tens of hours
        Hn = data[1][-11:-8].int    # Hours
        TMn = data[1][-6:-4].int    # Tens of minutes
        Mn = data[1][-3:].int       # Minutes

        seconds = Sn + (TSn * 10) + (Hmn / 10) + (Tmn / 100)
        minutes = Mn + (TMn * 10)
        hours = Hn + (THn * 10)

        # IRIG day format
        if not self.date_fmt:
            HDn = data[2][-10:-8].int  # Hundreds of days
            TDn = data[2][-7:-4].int   # Tens of days
            Dn = data[2][-3:].int      # Days

            day = Dn + (HDn * 100) + (TDn * 10)

            today = datetime.today()
            self.time = datetime(today.year, 1, 1) + timedelta(day - 1)

        # Month and Year Format
        else:
            TOn = data[2][-13:-12].int  # Tens of months
            On = data[2][-11:-8].int    # Months
            TDn = data[2][-7:-4].int    # Tens of days
            Dn = data[2][-3:].int       # Days
            OYn = data[3][-13:-12].int  # Thousands of years
            HYn = data[3][-11:-8].int   # Hundreds of years
            TYn = data[3][-7:-4].int    # Tens of years
            Yn = data[3][-3:].int       # Years

            month = On + (TOn * 10)
            day = Dn + (TDn * 10)
            year = Yn + (TYn * 10) + (HYn * 100) + (OYn * 1000)
            self.time = datetime(year, month, day)

        self.time = self.time.replace(
            second=seconds,
            minute=minutes,
            hour=hours,
            tzinfo=None)
