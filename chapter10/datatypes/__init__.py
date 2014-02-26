from base import Base
from ethernet import Ethernet
from pcm import PCM

# a dictionary of (<hex>, <class>) pairs mapping data types to python objects
# (default is base)
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


def get_handler(data_type):
    """Find an appropriate parser for a given data type."""

    return Base


def get_label(data_type):
    """Return a human readable format label."""

    t = int(data_type / 8.0)
    return '%s data, format %i' % (TYPES[t], data_type - (t * 8))
