
from collections import OrderedDict

from .util import BitFormat, bitstruct
from . import packet


class ComputerF0(packet.Packet):
    """User-defined"""

    def __init__(self, *args, **kwargs):
        self.data = bytes()
        packet.Packet.__init__(self, *args, **kwargs)
        if self.buffer:
            self.data = self.buffer.read(self.data_length - 4)

    def _raw_body(self):
        return (b'\0' * 4) + self.data


class ComputerF1(packet.Packet):
    """Setup record (TMATS)

    Using dictionary lookup syntax returns an OrderedDict of values that start
    with the given string::

        >> tmats_packet['G']
        OrderedDict({'G\\COM': 'Comment'})

    .. py:attribute:: version

        Irig106 release:

        * 7 = 2007
        * 8 = 2009
        * 9 = 2010
        * 10 = 2013
        * 11 = 2015
        * 12 = 2017

    .. py:attribute:: configuration_change

        When streaming, indicates if the TMATS configuration has changed from
        the previous one.

    .. py:attribute:: format

        Indicates ASCII (0) or XML (1)
    """

    csdw_format = BitFormat('''
        u8 version
        u1 configuration_change
        u1 format
        p22''')

    def __init__(self, *args, **kwargs):
        packet.Packet.__init__(self, *args, **kwargs)
        if self.buffer:
            self.data = self.buffer.read(self.data_length - 4)
        elif not self.data:
            self.data = bytes()

    def _raw_body(self):
        csdw = self.csdw_format.pack(self.__dict__)
        if isinstance(self.data, str):
            return csdw + bytes(self.data, 'utf8')
        return csdw + self.data

    def __getitem__(self, key):
        key = bytearray(key, 'utf-8')
        d = OrderedDict()
        for line in self.data.splitlines():
            if not line.strip() or b':' not in line:
                continue
            line = line.strip()[:-1].split(b':', 1)  # Strip the semicolon.
            if line[0].startswith(key):
                d[line[0]] = line[1]
        return d


class ComputerF2(packet.Packet):
    """Recording Event

    .. py:attribute:: count
    .. py:attribute:: ipdh
    """

    csdw_format = BitFormat('''
        u12 count
        p19
        u1 ipdh''')

    def __init__(self, *args, **kwargs):
        packet.Packet.__init__(self, *args, **kwargs)

        fmt = 'u64 ipts'
        if self.ipdh:
            fmt += '\nu64 ipdh'
        fmt += '''
            u12 number
            u16 count
            u1 occurrence
            p3'''
        self.Message.FORMAT = BitFormat(fmt)

    class Message(packet.Message):
        """
        .. py:attribute:: ipts
        .. py:attribute:: ipdh

            If present (see CSDW), contains the absolute time of the event.

        .. py:attribute:: number

            Event type number

        .. py:attribute:: count

            Number of events of this type as of the packet being written.

        .. py:attribute:: occurrence

            1 if event occurred during .RECORD mode.
        """
        def __repr__(self):
            return '<Recording event>'


class ComputerF3(packet.Packet):
    """Index Packet

    .. py:attribute:: count
    .. py:attribute:: ipdh
    .. py:attribute:: file_size_present
    .. py:attribute:: index_type

        * 0 - Root Index
        * 1 - Node Index

    .. py:attribute::file_size

        If enabled (see CSDW) indicates file size when packet was written.

    .. py:attribute::root_offset

        For root index, indicates offset to previous root index packet.
    """

    csdw_format = BitFormat('''
        u16 count
        p13
        u1 ipdh
        u1 file_size_present
        u1 index_type''')

    class Message(packet.Message):
        """
        .. py:attribute:: ipts
        .. py:attribute:: ipdh
        .. py:attribute:: offset

            Offset to packet from beginning of file.

        **Node Index Only**

        .. py:attribute:: channel_id
        .. py:attribute:: data_type
        """

        def __repr__(self):
            return '<%s Index>' % (
                'Node' if self.parent.index_type else 'Root')

    def __init__(self, *args, **kwargs):
        packet.Packet.__init__(self, *args, **kwargs)

        if self.file_size_present:
            self.file_size = bitstruct.unpack('u64<', self.buffer.read(8))

        fmt = 'u64 ipts'
        if self.ipdh:
            fmt += '\nu64 ipdh'

        if self.index_type == 0:
            fmt = '\nu64 offset'
        elif self.index_type == 1:
            fmt = '''
                u16 channel_id
                u8 data_type
                u8 offset'''

        self.Message.FORMAT = BitFormat(fmt)

        if self.index_type == 0:
            pos = self.buffer.tell()
            self.buffer.seek(self.data_length - 8)
            self.root_offset = bitstruct.unpack('u64<', self.buffer.read(8))
            self.buffer.seek(pos)
