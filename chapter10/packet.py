
from io import BytesIO
from array import array

from .util import BitFormat


class InvalidPacket(Exception):
    pass


class Packet(object):
    """Base class for the various datatypes.

    :param file: Source file to read from.
    :type file: file-like
    :param header: Initial header values. Read from file if not provided.

    **Chapter 10 Header**

    .. py:attribute:: sync_pattern
    .. py:attribute:: channel_id
    .. py:attribute:: packet_length
    .. py:attribute:: data_length
    .. py:attribute:: header_version
    .. py:attribute:: sequence_number
    .. py:attribute:: secondary_header
    .. py:attribute:: ipts_source
    .. py:attribute:: rtc_sync_error
    .. py:attribute:: data_overflow_error
    .. py:attribute:: secondary_format
    .. py:attribute:: data_checksum_present
    .. py:attribute:: data_type
    .. py:attribute:: rtc
    .. py:attribute:: header_checksum

    **Secondary Header (if present)**

    .. py:attribute:: time
    .. py:attribute:: secondary_checksum

    **Other Attributes**

    .. py:attribute:: FORMAT
        :type: BitFormat

        Description of the chapter 10 header

    .. py:attribute:: SECONDARY_FORMAT
        :type: BitFormat

        Describes the secondary header

    .. py:attribute:: csdw_format
        :type: BitFormat
        :value: None

        Describes a datatype's channel specific data word (CSDW)
    """

    FORMAT = BitFormat('''
        u16 sync_pattern
        u16 channel_id
        u32 packet_length
        u32 data_length
        u8 header_version
        u8 sequence_number
        u1 secondary_header
        u1 ipts_source
        u1 rtc_sync_error
        u1 data_overflow_error
        u2 secondary_format
        u2 data_checksum_present
        u8 data_type
        u48 rtc
        u16 header_checksum''')

    SECONDARY_FORMAT = BitFormat('''
        u64 secondary_time
        p16 reserved
        u16 secondary_checksum''')

    csdw_format = BitFormat('u32 csdw')

    def __init__(self, file, **header):

        # Read header if not done already.
        if not header:
            raw_header = file.read(24)
            header = self.FORMAT.unpack(raw_header)
        else:
            raw_header = self.FORMAT.pack(header)

        # Compute checksum and update attributes with header values.
        self.header_sums = sum(array('H', raw_header)[:-1]) & 0xffff
        self.__dict__.update(header)

        # Read the secondary header (if any).
        self.time = None
        secondary = bytes()
        if self.secondary_header:
            secondary = file.read(12)
            self.secondary_sums = sum(array('H', secondary)[:-1]) & 0xffff
            self.__dict__.update(self.SECONDARY_FORMAT.unpack(file.read(12)))

        # Read from the file or buffer into our own personal buffer.
        header_size = len(raw_header + secondary)
        body = file.read(self.packet_length - header_size)
        self.buffer = BytesIO(raw_header + secondary + body)
        self.buffer.seek(header_size)

        error = self.get_errors()
        if error:
            raise error

        # Read channel specific data word (CSDW)
        self.__dict__.update(self.csdw_format.unpack(self.buffer.read(4)))

    def __next__(self):
        """Return the next message until the end, then raise StopIteration."""

        if not getattr(self, 'Message', None):
            raise StopIteration

        try:
            return self.Message.from_packet(self)
        except EOFError:
            raise StopIteration

    def __iter__(self):
        return self

    def get_errors(self):
        """Validate the packet using checksums and verifying fields."""

        if self.sync_pattern != 0xeb25:
            return InvalidPacket('Incorrect sync pattern!')
        elif self.header_sums != self.header_checksum:
            return InvalidPacket('Header checksum mismatch!')
        elif self.secondary_header:
            if self.secondary_sums != self.secondary_checksum:
                return InvalidPacket('Secondary header checksum mismatch!')
        elif self.data_length > 524288:
            return InvalidPacket('Data length larger than allowed!')

    def check(self):
        """Return validity boolean. See get_errors method."""

        return self.get_errors() is None

    def __len__(self):
        """Return length if we can find one, else raise TypeError."""

        if hasattr(self, 'count'):
            return self.count
        elif self.Message.length:
            msg_size = self.Message.length
            if getattr(self.Message, 'FORMAT', None):
                msg_size += self.Message.FORMAT.calcsize() // 8
            return (self.data_length - 4) // msg_size
        raise TypeError("object of type '%s' has no len()" % self.__class__)

    def __bytes__(self):
        """Returns the entire packet as raw bytes."""

        return self.buffer.getvalue()

    def __repr__(self):
        return '<{} {} bytes>'.format(
            self.__class__.__name__, len(bytes(self)))

    # Pickle compatability.
    def __setstate__(self, state):
        state['file'] = BytesIO(state['file'])
        self.__dict__.update(state)

    def __getstate__(self):
        state = self.__dict__.copy()
        state['file'] = bytes(self)
        for k, v in list(state.items()):
            if callable(v):
                del state[k]
        return state


class Message:
    """The base container for packet message data.

    :param bytes data: The binary data to be stored. May be empty (for
        instance, if FORMAT fully describes the format).
    :param Packet parent: The Packet object this message belongs to.
    :param kwargs: Arbitrary key-value pairs to add as attributes to the item
        instance. Used for IPH values.

    **Class Attributes**

    .. py:attribute:: FORMAT
        :type: BitFormat
        :value: None

        Describes the intra-packet header (IPH) or message format in general.

    .. py:attribute:: length
        :type: int
        :value: 0

        Byte size of message body. If not specified will look for a 'length'
        field in the IPH.

    **Instance Attributes**

    .. py:attribute:: parent
        :type: Packet

        The Packet object this message is attached to.

    .. py:attribute:: data
        :type: bytes

        Raw data not identified in FORMAT
    """

    FORMAT = None
    length = 0

    def __init__(self, data, parent=None, **kwargs):
        self.__dict__.update(kwargs)
        self.parent = parent
        self.data = data

    @classmethod
    def from_packet(cls, packet):

        # Exit when we reach the end of the packet body
        end = packet.data_length + (packet.secondary_header and 36 or 24)
        if packet.buffer.tell() >= end:
            raise EOFError

        # Read and parse the IPH
        iph = {}
        if getattr(cls, 'FORMAT', None):
            iph_size = cls.FORMAT.calcsize() // 8
            raw = packet.buffer.read(iph_size)
            if len(raw) < iph_size:
                raise EOFError
            iph = cls.FORMAT.unpack(raw)

        # Read the message data and account for filler if length is odd.
        length = iph.get('length', cls.length)
        data = packet.buffer.read(length)
        if length % 2:
            packet.buffer.seek(1, 1)

        return packet.Message(data, parent=packet, **iph)

    def __bytes__(self):
        """Return bytes() containing any IPH and data."""

        return self.FORMAT.pack(self.__dict__) + self.data
