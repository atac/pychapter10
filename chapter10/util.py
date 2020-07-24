
try:
    import cbitstruct as bitstruct
except ImportError:
    import bitstruct


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
