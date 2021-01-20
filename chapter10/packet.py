
from io import BytesIO
from array import array
import struct

from .util import BitFormat


class InvalidPacket(Exception):
    pass


class Packet:
    """Base class for the various datatypes. May be created from a file-like
    object or started from scratch.

    :param file: Source file to read from.
    :type file: file-like
    :param kwargs: Initial header values. Read from file if not provided.

    **Chapter 10 Header Attributes**

    - sync_pattern
    - channel_id
    - packet_length
    - data_length
    - header_version
    - sequence_number
    - secondary_header
    - ipts_source
    - rtc_sync_error
    - data_overflow_error
    - secondary_format
    - data_checksum
    - data_type
    - rtc
    - header_checksum

    **Secondary Header (if present)**

    - secondary_time
    - secondary_checksum

    **Other Members**

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
        u2 data_checksum
        u8 data_type
        u48 rtc
        u16 header_checksum''')

    SECONDARY_FORMAT = BitFormat('''
        u64 secondary_time
        p16 reserved
        u16 secondary_checksum''')

    csdw_format = BitFormat('u32 csdw')

    def __init__(self, file=None, **kwargs):

        # Set defaults
        for fmt in (self.FORMAT, self.SECONDARY_FORMAT, self.csdw_format):
            for name in fmt.names:
                setattr(self, name, 0)
        self.sync_pattern = 0xeb25

        self.__dict__.update(kwargs)
        self._messages = []
        self.buffer = None

        # If file is not given, start from scratch.
        if not file:
            self.clear()
            return

        # Read header if not done already.
        if not kwargs:
            raw_header = file.read(24)
            kwargs = self.FORMAT.unpack(raw_header)
            self.__dict__.update(kwargs)
        else:
            raw_header = self.FORMAT.pack(kwargs)

        # Compute checksum and update attributes with header values.
        self.header_sums = sum(array('H', raw_header)[:-1]) & 0xffff

        # Read the secondary header (if any).
        secondary = bytes()
        if self.secondary_header:
            secondary = file.read(12)
            self.secondary_sums = sum(array('H', secondary)[:-1]) & 0xffff
            self.__dict__.update(self.SECONDARY_FORMAT.unpack(file.read(12)))

        # Read into our own personal buffer.
        header_size = 24 + len(secondary)
        body = file.read(self.packet_length - header_size)
        self.buffer = BytesIO(raw_header + secondary + body)
        self.buffer.seek(header_size)

        self.validate()

        # Read channel specific data word (CSDW)
        self.__dict__.update(self.csdw_format.unpack(self.buffer.read(4)))

    def _read_messages(self):
        """Internal: ensure all messages are read in order to manipulate data
        in an internal list.
        """

        if self.buffer:
            header_size = 36 if self.secondary_header else 24
            self.buffer.seek(header_size + 4)
            self._messages = list(self)

    def __next__(self):
        """Return the next message until the end, then raise StopIteration."""

        if self.buffer is None:
            return next(self._messages)

        if not getattr(self, 'Message', None):
            raise StopIteration

        try:
            msg = self.Message.from_packet(self)
            self._messages.append(msg)
            return msg
        except EOFError:
            self.buffer = None
            raise StopIteration

    def __iter__(self):
        if self.buffer:
            return self
        else:
            return iter(self._messages)

    def validate(self, silent=False):
        """Validate the packet using checksums and verifying fields. If silent
        = False raises InvalidPacket.
        """

        err = None
        if self.sync_pattern != 0xeb25:
            err = InvalidPacket('Incorrect sync pattern!')
        elif self.header_sums != self.header_checksum:
            err = InvalidPacket('Header checksum mismatch!')
        elif self.secondary_header:
            if self.secondary_sums != self.secondary_checksum:
                err = InvalidPacket('Secondary header checksum mismatch!')
        elif self.data_length > 524288:
            err = InvalidPacket('Data length larger than allowed!')

        if err:
            if not silent:
                raise err
            return False
        return True

    def __len__(self):
        """Return length if we can find one, else raise TypeError."""

        if self.buffer is None and self._messages is not None:
            return len(self._messages)
        if hasattr(self, 'count'):
            return self.count
        elif hasattr(self, 'Message') and self.Message.length:
            msg_size = self.Message.length
            if getattr(self.Message, 'FORMAT', None):
                msg_size += self.Message.FORMAT.calcsize() // 8
            return (self.data_length - 4) // msg_size
        raise TypeError("object of type '%s' has no len()" % self.__class__)

    def _raw_body(self):
        """Returns the raw bytes of the packet body, including the CSDW."""

        # Pack messages into body
        body = b''.join(bytes(m) for m in self._messages)
        return self.csdw_format.pack(self.__dict__) + body

    def __bytes__(self):
        """Returns the entire packet as raw bytes."""

        self._read_messages()

        body = self._raw_body()
        self.data_length = len(body)

        # Add filler to maintain 32 bit alignment
        checksum_size = (0, 1, 2, 4)[self.data_checksum]
        while (checksum_size + len(body)) % 4:
            body += b'\0'

        # Compute the data checksum
        if self.data_checksum:
            fmt = 'xBHI'[self.data_checksum]
            checksum = sum(array(fmt, body))
            checksum &= (0, 0xff, 0xffff, 0xffffffff)[self.data_checksum]
            body += struct.pack(fmt, checksum)

        # Pack header (with updated checksum) and secondary header if needed.
        header_length = 36 if self.secondary_header else 24
        self.packet_length = header_length + len(body)
        raw = self.FORMAT.pack(self.__dict__)
        self.header_checksum = sum(array('H', raw)[:-1]) & 0xffff
        raw = self.FORMAT.pack(self.__dict__)
        if self.secondary_header:
            raw += self.SECONDARY_FORMAT.pack(self.__dict__)

        # Add body and filler
        return raw + body

    def __repr__(self):
        return '<{} {} bytes>'.format(
            self.__class__.__name__, getattr(self, 'packet_length', '?'))

    def append(self, *messages):
        """Add one or more messages to the packet."""

        self._read_messages()
        for message in messages:
            self._messages.append(message)

    def clear(self):
        """Remove all messages."""

        self._read_messages()
        self._messages = []

    def copy(self):
        """Duplicate this packet."""

        return self.__class__(**self.__dict__.copy())

    def remove(self, i):
        """Remove message at index 'i'"""

        self._read_messages()
        del self._messages[i]

    # Pickle compatability.
    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getstate__(self):
        self._read_messages()
        return {k: v for k, v in self.__dict__.items() if not callable(v)}


class Message:
    """The base class for packet message data. Subclasses define FORMAT,
    length, etc. to give the format and can be instantiated empty or from a
    packet using the from_packet method.

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
        :type: Packet or None

        The Packet object this message is attached to.

    .. py:attribute:: data
        :type: bytes

        Raw data not identified in FORMAT
    """

    FORMAT = None
    length = 0

    def __init__(self, data=b'', parent=None, **kwargs):
        if self.FORMAT:
            self.__dict__.update({name: 0 for name in self.FORMAT.names})
        self.__dict__.update(kwargs)
        self.parent = parent
        self.data = data

    @classmethod
    def from_packet(cls, packet):
        """Helper method to read a message from packet."""

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

        raw = bytes()
        if self.FORMAT is not None:
            raw += self.FORMAT.pack(self.__dict__)
        raw += self.data
        if len(raw) % 2:
            raw += b'\0'
        return raw
