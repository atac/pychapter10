
from collections import OrderedDict
import struct

from .util import BitFormat
from .packet import Packet


class ComputerF0(Packet):
    """User-defined"""

    pass


class ComputerF1(Packet):
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
        u1 format''')

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)
        self.data = self.file.read(self.data_length - 4)

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


class ComputerF2(Packet):
    """Recording Event

    .. py:attribute:: count
    .. py:attribute:: ipdh

    **Message Format**

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

    csdw_format = BitFormat('''
        u12 count
        p19
        u1 ipdh''')
    item_label = 'Recording Event'
    item_format = '''
        u12 number
        u16 count
        u1 occurrence
        p3'''

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        self.iph_format = 'u64 ipts'
        if self.ipdh:
            self.iph_format += '\nu64 ipdh'
        self.iph_format = BitFormat(self.item_format + self.iph_format)


class ComputerF3(Packet):
    """Index Packet

    .. py:attribute:: count
    .. py:attribute:: ipdh
    .. py:attribute:: file_size_present
    .. py:attribute:: index_type

        Index (1) or root index (0).

    .. py:attribute::file_size

        If enabled (see CSDW) indicates file size when packet was written.

    .. py:attribute::root_offset

        For root index, indicates offset to previous root index packet.

    **Root Index Message Format**

    .. py:attribute:: ipts
    .. py:attribute:: ipdh

        If present (see CSDW), contains the absolute time of the message.

    .. py:attribute:: offset

        Offset to node packet from beginning of file.

    **Node Index Message Format**

    .. py:attribute:: ipts
    .. py:attribute:: ipdh

        If present (see CSDW), contains the absolute time of the message.

    .. py:attribute:: channel_id
    .. py:attribute:: data_type
    .. py:attribute:: offset

        Offset to data packet from beginning of file.
    """

    csdw_format = BitFormat('''
        u16 count
        p13
        u1 ipdh
        u1 file_size_present
        u1 index_type''')
    item_size = 0

    def __init__(self, *args, **kwargs):
        Packet.__init__(self, *args, **kwargs)

        if self.file_size_present:
            self.file_size, = struct.unpack('Q', self.file.read(8))

        self.iph_format = 'u64 ipts'
        if self.ipdh:
            self.iph_format += '\nu64 ipdh'

        if self.index_type == 0:
            self.item_label = 'Root Index'
            item_format = '\nu64 offset'
        elif self.index_type == 1:
            self.item_label = 'Node Index'
            item_format = '''
                u16 channel_id
                u8 data_type
                u8 offset'''

        self.iph_format = BitFormat(self.iph_format + item_format)

        if self.index_type == 0:
            pos = self.file.tell()
            self.file.seek(self.data_length - 8)
            self.root_offset, = struct.unpack('Q', self.file.read(8))
            self.file.seek(pos)
