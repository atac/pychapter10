
from io import BytesIO
from array import array

from .util import BitFormat


class InvalidPacket(Exception):
    pass


class Packet(object):
    """Base class for the various datatypes.

    :param file: Source file to read from.
    :type file: file-like
    :param header: Optionally pass in header values (used by C10 class)
    :type header: tuple of (bytes, dict)

    **Chapter 10 Header attributes**

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

    **Constants**

    .. py:attribute:: FORMAT
        :type: BitFormat

        Description of the chapter 10 header

    .. py:attribute:: SECONDARY_FORMAT
        :type: BitFormat

        Describes the secondary header

    **Format Specification**

    .. py:attribute:: csdw_format
        :type: BitFormat
        :value: None

        Describes a datatype's channel specific data word (CSDW)

    .. py:attribute:: iph_format
        :type: BitFormat
        :value: None

        Describes a datatype's intra-packet header (IPH)

    .. py:attribute:: item_label
        :type: str
        :value: None

        Human-readable label for messages. A not None value indicates a
        datatype contains messages.

    .. py:attribute:: item_size
        :type: int
        :value: None

        Byte size of message body. If not specified will look for a 'length'
        field in the IPH.

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

    csdw_format = None
    iph_format = None
    item_label = None
    item_size = None

    def __init__(self, file, header=None):
        # Read the packet header and save header sums for later.
        if header:
            header, values = header
        else:
            header = file.read(24)
            values = self.FORMAT.unpack(header)

        self.header_sums = sum(array('H', header)[:-1]) & 0xffff
        self.__dict__.update(values)

        # Read the secondary header (if any).
        self.time = None
        secondary = bytes()
        if self.secondary_header:
            secondary = file.read(12)
            self.secondary_sums = sum(array('H', secondary)[:-1]) & 0xffff
            self.__dict__.update(self.SECONDARY_FORMAT.unpack(file.read(12)))

        header_size = len(header + secondary)
        body = file.read(self.packet_length - header_size)
        self.file = BytesIO(header + secondary + body)
        self.file.seek(header_size)

        error = self.get_errors()
        if error:
            raise error

        if self.csdw_format:
            raw = self.file.read(4)
            self.__dict__.update(self.csdw_format.unpack(raw))

    def __next__(self):
        """Return the next message until the end, then raise StopIteration."""

        if not self.item_label:
            raise StopIteration

        # Exit when we reach the end of the packet body
        end = self.data_length + (self.secondary_header and 36 or 24)
        if self.file.tell() >= end:
            raise StopIteration

        # Read and parse the IPH
        iph = {}
        if self.iph_format:
            iph_size = self.iph_format.calcsize() // 8
            raw = self.file.read(iph_size)
            if len(raw) < iph_size:
                raise StopIteration
            iph = self.iph_format.unpack(raw)

        # Read the message data
        length = getattr(self, 'item_size', 0) or 0
        if 'length' in iph:
            length = iph['length']
        data = self.file.read(length)

        # Account for filler byte when length is odd.
        if length % 2:
            self.file.seek(1, 1)

        return Item(data, self.item_label, self.iph_format, **iph)

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
        elif self.item_size:
            msg_size = self.item_size
            if self.iph_format:
                msg_size += self.iph_format.calcsize() // 8
            return (self.data_length - 4) // msg_size
        raise TypeError("object of type '%s' has no len()" % self.__class__)

    def __bytes__(self):
        """Returns the entire packet as raw bytes."""

        return self.file.getvalue()

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


class Item(object):
    """The base container for packet message data.

    :param bytes data: The binary data to be stored. May be empty (for
        instance, if item_format fully describes the format).
    :param str label: Human-readable label for this type. Will be used for
        repr()
    :param item_format: Describes the IPH and/or data format.
    :type item_format: BitFormat or None
    :param kwargs: Arbitrary key-value pairs to add as attributes to the item
        instance. Used for IPH values.

    .. py:attribute:: data
        :type: bytes

        Raw data not identified in item_format
    """

    def __init__(self, data, label="Packet Data", item_format=None, **kwargs):
        self.__dict__.update(kwargs)
        self.item_format = item_format
        self.data, self.label = data, label

    def __repr__(self):
        return '<%s %s bytes>' % (self.label, len(self.data))

    def __bytes__(self):
        return self.pack()

    def pack(self, format=None):
        """Return bytes() containing the item's IPH and data."""

        if format is None:
            format = self.item_format
        return format.pack(self.__dict__) + self.data
