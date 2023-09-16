
import pytest

from chapter10 import C10, analog
from fixtures import ANALOG


@pytest.fixture
def packet():
    for packet in C10(ANALOG):
        if isinstance(packet, analog.AnalogF1):
            return packet


def test_csdw(packet):
    assert packet.mode == 0
    assert packet.length == 8
    assert packet.subchannel == 0
    assert packet.factor == 0
    assert packet.same == 1


def test_count(packet):
    assert len(packet.subchannels) == packet.subchannel_count


def test_next(packet):
    for i, sample in enumerate(packet):
        assert sample.data == b'\xfc'
        if i >= 2:
            break


def test_bytes(packet):
    assert packet.buffer.getvalue() == bytes(packet)


def test_generate():
    a = analog.AnalogF1(same=1)
    msg1 = analog.AnalogF1.Message(length=2, data=b'\xbe\xef')
    a.append(msg1)

    assert b'\xbe\xef' in bytes(a)