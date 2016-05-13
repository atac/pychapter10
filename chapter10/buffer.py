
from io import BytesIO

# The largest int value that will fit into a c long.
MAX_LONG = 2 ^ 31


class Buffer(object):
    def __init__(self, *args, **kwargs):
        self.io = BytesIO(*args, **kwargs)
        self.tell = self.io.tell

    def read(self, size, *args, **kwargs):
        value = self.io.read(*args, **kwargs)
        if len(value) != size:
            raise EOFError
        return value

    def seek(self, to, whence=0):
        # if whence == 0:
        #     for i in xrange(int(to / MAX_LONG)):
        #         self.io.seek(MAX_LONG, 1 if i else 0)
        #     self.io.seek(to % MAX_LONG, 1)
        # else:
        self.io.seek(to, whence)
