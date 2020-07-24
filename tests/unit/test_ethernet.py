
import pytest

from chapter10 import C10, ethernet
from fixtures import dummy_packet, ETHERNET


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x6A, 0x70)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        ethernet.Ethernet.from_string(raw)


def test_format_0_count():
    for packet in C10(ETHERNET):
        if packet.data_type == 0x68:
            break
    assert len(packet) == packet.number_of_frames


def test_format_1_count():
    for packet in C10(ETHERNET):
        if packet.data_type == 0x69:
            break
    assert len(packet) == packet.count
