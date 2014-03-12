from .base import Base
from .computer import Computer
from .time import Time
from .ms1553 import MS1553
from .analog import Analog
from .discrete import Discrete
from .video import Video
from .ethernet import Ethernet
from .pcm import PCM

# Top level data types.
TYPES = (('Computer Generated', Computer),
         ('PCM', PCM),
         ('Time', Time),
         ('Mil-STD-1553', MS1553),
         ('Analog', Analog),
         ('Discrete', Discrete),
         ('Message', Base),
         ('ARINC 429', Base),
         ('Video', Video),
         ('Image', Base),
         ('UART', Base),
         ('IEEE-1394', Base),
         ('Parallel', Base),
         ('Ethernet', Base))


def format(data_type):
    """Find the type index (see TYPES) and format number for a datatype."""

    t = int(data_type / 8.0)
    return (t, data_type - (t * 8))


def get_handler(data_type):
    """Find an appropriate parser for a given data type."""

    t, f = format(data_type)
    return TYPES[t][1]


def get_label(data_type):
    """Return a human readable format label."""

    t, f = format(data_type)
    return '%s (format %i)' % ('unknown' if t > (len(TYPES) - 1)
                               else TYPES[t][0], f)
