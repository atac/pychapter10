from base import Base
from video import Video
from ethernet import Ethernet
from pcm import PCM

# Top level data types.
TYPES = ('Computer Generated',
         'PCM',
         'Time',
         'Mil-STD-1553',
         'Analog',
         'Discrete',
         'Message',
         'ARINC 429',
         'Video',
         'Image',
         'UART',
         'IEEE-1394',
         'Parallel',
         'Ethernet')


def format(data_type):
    """Find the type index (see TYPES) and format number for a datatype."""

    t = int(data_type / 8.0)
    return (t, data_type - (t * 8))


def get_handler(data_type):
    """Find an appropriate parser for a given data type."""

    t, f = format(data_type)
    if t == 1:
        return PCM
    elif t == 8:
        return Video
    return Base


def get_label(data_type):
    """Return a human readable format label."""

    t, f = format(data_type)
    return '%s (format %i)' % ('unknown' if t > (len(TYPES) - 1)
                               else TYPES[t], f)
