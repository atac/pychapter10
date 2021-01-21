
try:
    import cbitstruct as bitstruct
except ImportError:
    import bitstruct


class BitFormat:
    """Bitstruct wrapper that allows for compiling from readable format
    strings.

    :param str src: "struct" like format with newline separated pairs of <fmt>,
        <name> where fmt is a bitstruct format string (generally as
        "<bitsize>") and name is the attribute name to use.
    :param str byteswap: Optional bitstruct style byteswap description. See
        bitstruct docs
    :value byteswap: None

    .. py:attribute:: fmt_str
        :type: string

        The original format string.

    .. py:attribute:: names
        :type: list

        A list of the field names from the format string.
    """

    def __init__(self, src, byteswap=None):
        self.byteswap = byteswap
        self.fmt_str = ''
        self.names = []
        for line in src.strip().splitlines():
            line = line.strip().split()
            if not line:
                continue
            if len(line) == 1 or line[-1].lower().endswith('reserved'):
                fmt = line[0]
            else:
                fmt, name = line
                self.names.append(name)
            self.fmt_str += fmt

        # Default to little endian if we're not explicitly defining swapping
        if not byteswap and self.fmt_str[-1] not in '<>':
            self.fmt_str += '<'

        self._compiled = bitstruct.compile(self.fmt_str, names=self.names)

    def __getattr__(self, name, default=None):
        if name in ('byteswap', 'pack', 'unpack', 'raw', 'fmt_str', 'names'):
            return object.__getattr__(self, name, default)
        return getattr(self._compiled, name, default)

    def unpack(self, data):
        """Use compiled format to unpack data. Uses self.byteswap if provided.

        :param bytes data: Raw data to unpack
        :returns dict: Unpacked values based on compiled format.
        """

        if self.byteswap:
            data = bitstruct.byteswap(self.byteswap, data)
        self.raw = data
        return self._compiled.unpack(data)

    def pack(self, values):
        raw = self._compiled.pack(values)
        if self.byteswap:
            raw = bitstruct.byteswap(self.byteswap, raw)
        return raw


# TODO: is this needed any more?
class Buffer(object):
    """File wrapper that raises EOF on a short read."""

    def __init__(self, io):
        self.io = io
        self.tell = self.io.tell
        self.seek = self.io.seek

    def read(self, size=None):
        value = self.io.read(size)
        if size and len(value) != size:
            raise EOFError
        return value
