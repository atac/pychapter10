
import pytest

from chapter10 import C10, arinc429
from fixtures import SAMPLE


@pytest.fixture
def packet():
    for packet in C10(SAMPLE):
        if isinstance(packet, arinc429.ARINC429F0):
            return packet


def test_count(packet):
    assert len(list(packet)) == len(packet) == 221


def test_gap(packet):
    expected = (
        (0, 2, 1),
        (2489, 4, 1),
        (1131, 2, 1),
        (2489, 4, 1),
        (1131, 2, 1),
        (1221, 5, 0),
    )
    for i, msg in enumerate(packet):
        if i < len(expected):
            assert (msg.gap_time, msg.bus, msg.bus_speed) == expected[i]
        else:
            break


def test_bytes(packet):
    for msg in packet:
        packet.buffer.seek(-8, 1)
        raw = packet.buffer.read(8)
        assert bytes(msg) == raw
