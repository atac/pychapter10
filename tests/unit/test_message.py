
import pytest

from chapter10 import C10, message
from fixtures import SAMPLE


@pytest.fixture
def packet():
    for packet in C10(SAMPLE):
        if isinstance(packet, message.MessageF0):
            return packet


@pytest.fixture
def msg(packet):
    return next(packet)


def test_csdw(packet):
    assert packet.packet_type == 0
    assert packet.count == 94


def test_msg(msg):
    assert msg.ipts == 604324042154
    assert msg.length == 350 == len(msg.data)
    assert msg.subchannel == 1
    assert msg.format_error == 0
    assert msg.data_error == 0
