
from datetime import datetime, timedelta

from .util import BitFormat
from .packet import Packet


class TimeF1(Packet):
    """Time Packets

    **Note:** Low level fields such as HSn, TSn, etc. are not documented here
    nor are they intended to be used directly. Use the .time attribute instead.

    .. py:attribute:: time_source

        * 0 - Internal (recorder clock)
        * 1 - External
        * 2 - Internal from RMM
        * 15 - None

    .. py:attribute:: time_format

        Indicates time data packet format

        * 0 - IRIG-B
        * 1 - IRIG-A
        * 2 - IRIG-G
        * 3 - Real-Time clock
        * 4 - UTC time from GPS
        * 5 - Native GPS time
        * 15 - None (payload invalid)

    .. py:attribute:: leap

        Indicates if this is a leap year.

    .. py:attribute:: date_format

        0 for IRIG day format, 1 for month and year format.

    .. py:attribute:: irig_source

        IRIG time source

        * 0 - TCG freewheeling (no/lost time source)
        * 1 - TCG freewheeling from .TIME command
        * 2 - TCG freewheeling from RMM time
        * 3 - TCG locked to external IRIG time signal
        * 4 - TCG locked to external GPS
        * 5 - TCG locked to external Network Time Protocol (NTP)
        * 6 - TCG locked to external Precision Time Protocol (PTP)
        * 7 - TCG locked to external embedded time from input track/channel\
such as PCM or 1553

    .. py:attribute:: time

        Python datetime object representing the packet payload.
    """

    csdw_format = BitFormat('''
        u4 time_format
        u4 time_source

        u4 irig_source

        p2
        u1 date_format
        u1 leap

        p16''')

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        self.data_format = '''
            u4 Hmn
            u4 Tmn
            u4 TSn
            u4 Sn

            u4 TMn
            u4 Mn
            u4 THn
            u4 Hn

            u4 TDn
            u4 Dn
            '''

        if not self.date_format:
            self.data_format += 'u8 HDn'
        else:
            self.data_format += '''
                p3
                u1 TOn
                u4 On

                u4 TYn
                u4 Yn
                p2
                u2 OYn
                u4 HYn
                '''

        self.data_format = BitFormat(self.data_format)

        if not self.buffer:
            for name in self.data_format.names:
                setattr(self, name, 0)
            self._initial_time = 0
            if not self.time:
                self.time = datetime.now()
            return

        raw = self.buffer.read(self.data_length - 4)
        self.__dict__.update(self.data_format.unpack(raw))

        ms = ((self.Hmn * 10) + self.Tmn)
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
            microsecond=ms * 1000,
            second=seconds,
            minute=minutes,
            hour=hours,
            tzinfo=None)
        self._initial_time = self.time

    def _raw_body(self):
        ms = self.time.microsecond // 1000
        self.Hmn = ms // 100
        self.Tmn = (ms - (self.Hmn * 100)) // 10

        self.TSn = self.time.second // 10
        self.Sn = self.time.second - (self.TSn * 10)
        self.TMn = self.time.minute // 10
        self.Mn = self.time.minute - (self.TMn * 10)
        self.THn = self.time.hour // 10
        self.Hn = self.time.hour - (self.THn * 10)

        # Month and year format
        if self.date_format:
            year = self.time.year
            self.OYn = year // 1000
            year -= self.OYn * 1000
            self.HYn = year // 100
            year -= self.HYn * 100
            self.TYn // 10
            year -= self.TYn * 10
            self.Yn = year

        else:
            day = int(self.time.strftime('%j'))
            self.HDn = day // 100
            day -= self.HDn * 100
            self.TDn = day // 10
            day -= self.TDn * 10
            self.Dn = day

        body = self.data_format.pack(self.__dict__)
        if len(body) % 2:
            body += b'\0'

        # Add CSDW and body
        return self.csdw_format.pack(self.__dict__) + body
