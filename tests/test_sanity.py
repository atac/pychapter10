
import struct

from chapter10 import Packet


# Highest numerical datatype available.
TYPE_RANGE = 120


def dummy_packet(type, size):
    header = [
        0xeb25,
        0,
        size + 24,
        size,
        1,
        1,
        0,
        type,
        0,
        0,
    ]
    header.append(sum(header))
    header = struct.pack('HHIIBBBBIHH', *header)
    return Packet.from_string(header + (b'\x00' * size))


# The various data lengths to try.
SIZES = [
    6,
    8,
    10,
    12,
    16
]


def test_sanity():
    for i in range(TYPE_RANGE):

        # Call dummy parse() to build all possible format definitions.
        # @NOTE: analog packets are not tested with this method.
        try:
            for s in SIZES:
                try:
                    dummy_packet(i, s)
                    break
                except struct.error:
                    pass
        except NotImplementedError:
            continue
