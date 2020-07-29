
from datetime import datetime, timedelta

from .util import BitFormat
from .packet import Packet


class TimeF1(Packet):
    csdw_format = BitFormat('''
        u4 time_source
        u4 time_format
        u1 leap
        u1 date_format
        p2
        u4 irig_source
        p16''')

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        self.data_format = '''
            u4 Tmn
            u4 Hmn
            u4 Sn
            u3 TSn
            p1
            u4 Mn
            u3 TMn
            p1
            u4 Hn
            u2 THn
            p2
            u4 Dn
            u4 TDn
            '''

        if not self.date_format:
            self.data_format += 'u1 HDn\np6'
        else:
            self.data_format += '''
                u4 On
                u1 Ton
                p3
                u4 Yn
                u4 TYn
                u4 HYn
                u2 OYn
                p2'''

        raw = self.file.read(self.data_length - 4)
        self.data_format = BitFormat(self.data_format)
        self.__dict__.update(self.data_format.unpack(raw))

        microseconds = ((self.Hmn * 10) + self.Tmn)
        seconds = self.Sn + (self.TSn * 10)
        minutes = self.Mn + (self.TMn * 10)
        hours = self.Hn + (self.THn * 10)

        # IRIG day format
        if not self.date_format:
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
