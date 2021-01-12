
import pytest

from chapter10 import C10, discrete
from fixtures import DISCRETE


@pytest.fixture
def packet():
    for packet in C10(DISCRETE):
        if isinstance(packet, discrete.DiscreteF1):
            return packet


def test_packet(packet):
    assert packet.mode == 0
    assert packet.length == 0


def test_msg(packet):
    for msg in packet:
        assert msg.ipts == 28894167514
        assert msg.data == b'\xff\xff\xff\xff'
        break
