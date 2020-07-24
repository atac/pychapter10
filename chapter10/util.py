
try:
    import cbitstruct as bitstruct
except ImportError:
    import bitstruct


def format(data_type):
    """Find the type index (see TYPES) and format number for a datatype."""

    t = int(data_type / 8.0)
    return (t, data_type - (t * 8))

# TODO: move this to packet
# def get_label(data_type):
#     """Return a human readable format label."""

#     t, f = format(data_type)
#     return '%s (format %i)' % ('unknown' if t > (len(TYPES) - 1)
#                                else TYPES[t][0], f)


def compile_fmt(src):
    """Compile helper that takes a readable string and creates a bitstruct
    CompiledFormatDict.
    """

    fmt_str = ''
    names = []
    for line in src.strip().splitlines():
        line = line.strip().split()
        if not line:
            continue
        if len(line) == 1 or line[-1].lower().endswith('reserved'):
            fmt = line[0]
        else:
            fmt, name = line
            names.append(name)
        fmt_str += fmt

    if fmt_str[-1] not in '<>':
        fmt_str += '<'

    return bitstruct.compile(fmt_str, names=names)


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
