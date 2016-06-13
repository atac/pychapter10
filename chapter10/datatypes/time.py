
from datetime import datetime, timedelta

from .base import Base


class Time(Base):
    csdw_format = ('=I', ((
        (None, 22),
        # 0 = IRIG day available
        # 1 = Month and year available
        ('date_fmt', 1),
        ('leap', 1),
        # 0 = IRIG-B
        # 1 = IRIG-A
        # 2 = IRIG-G
        # 3 = Real-Time Clock
        # 4 = UTC Time from GPS
        # 5 = Native GPS Time
        # F = None (payload invalid)
        ('time_fmt', 4),
        # 0 = Internal (to the recorder)
        # 1 = External (to the recorder)
        # 2 = Internal from RMM
        # F = None
        ('source', 4),
    ),),)

    def parse(self):
        if self.format != 1:
            raise NotImplementedError('Time Data format %s is reserved!'
                                      % self.format)
        self.parse_csdw()

        self.data_format = ['=HHH', [
            ((None, 1),
             ('TSn', 3),    # Tens of Seconds
             ('Sn', 4),     # Seconds
             ('Hmn', 4),    # Hundreds of milliseconds
             ('Tmn', 4),),  # Tens of milliseconds
            ((None, 2),
             ('THn', 2),    # Tens of hours
             ('Hn', 4),     # Hours
             (None, 1),
             ('TMn', 3),    # Tens of minutes
             ('Mn', 4),),   # Minutes
            ((None, 6),
             ('HDn', 2),    # Hundreds of days
             ('TDn', 4),    # Tens of days
             ('Dn', 4),)    # Days
        ]]

        if self.date_fmt:
            self.data_format[0] += 'H'
            del self.data_format[1][2]
            self.data_format[1] += [
                ((None, 3),
                 ('TOn', 1),   # Tens of months
                 ('On', 4),    # Months
                 ('TDn', 4),   # Tens of days
                 ('Dn', 4),),  # Days
                ((None, 2),
                 ('OYn', 2),   # Thousands of years
                 ('HYn', 4),   # Hundreds of years
                 ('TYn', 4),   # Tens of years
                 ('Yn', 4),),  # Years
            ]

        self.parse_data()

        microseconds = ((self.Hmn * 10) + self.Tmn)
        seconds = self.Sn + (self.TSn * 10)
        minutes = self.Mn + (self.TMn * 10)
        hours = self.Hn + (self.THn * 10)

        # IRIG day format
        if not self.date_fmt:
            day = self.Dn + (self.HDn * 100) + (self.TDn * 10)

            today = datetime.today()
            self.time = datetime(today.year, 1, 1) + timedelta(day - 1)

        # Month and Year Format
        else:
            month = self.On + (self.TOn * 10)
            day = self.Dn + (self.TDn * 10)
            year = self.Yn + (self.TYn * 10) + (self.HYn * 100) + (
                self.OYn * 1000)
            self.time = datetime(year, month, day)

        self.time = self.time.replace(
            microsecond=microseconds,
            second=seconds,
            minute=minutes,
            hour=hours,
            tzinfo=None)
