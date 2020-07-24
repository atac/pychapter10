
from array import array
import struct

import pytest

from chapter10 import Packet
from chapter10.packet import InvalidPacket


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


@pytest.mark.parametrize('size', (6, 8, 10, 12, 16))
@pytest.mark.parametrize('data_type', range(120))
def test_sanity(data_type, size):
    """Test default constructors for every data type and 5 base sizes."""

    raw = dummy_packet(data_type, size)
    try:
        Packet.from_string(raw)
    except (NotImplementedError, struct.error, InvalidPacket, TypeError):
        return
