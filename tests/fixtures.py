
from array import array
import os
import struct


BASEDIR = os.path.dirname(__file__)
ETHERNET = os.path.join(BASEDIR, 'eth.c10')
EVENTS = os.path.join(BASEDIR, 'event.c10')
INDEX = os.path.join(BASEDIR, 'index.c10')
PCM = os.path.join(BASEDIR, 'pcm.c10')
SAMPLE = os.path.join(BASEDIR, 'sample.c10')


def dummy_packet(type, size):
    """Create a dummy packet of given type and size. Returns bytes."""

    header = [
        0xeb25,
        0,
        size + 24,
        size,
        1,
        0,
        0,
        type,
        0,
        0
    ]
    header[2] += 4 - (header[2] % 4)
    checksum = sum(array('H', struct.pack('=HHIIBBBBIH', *header))) & 0xffff
    header.append(checksum)
    header = struct.pack('=HHIIBBBBIHH', *header)
    return header + (b'\x00' * size)
