from base import Base
from ethernet import Ethernet
from pcm import PCM

# a dictionary of (<hex>, <class>) pairs mapping data types to python objects
# (default is base)
map = {
    0x00: Base,
    0x09: PCM,
    #0x30: Ethernet,
}
