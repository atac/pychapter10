
import pytest

from chapter10 import C10, pcm
from fixtures import PCM


@pytest.fixture
def packet():
    for packet in C10(PCM):
        if isinstance(packet, pcm.PCMF1):
            return packet


@pytest.fixture
def throughput():
    for packet in C10(PCM):
        if isinstance(packet, pcm.PCMF1):
            if packet.throughput:
                return packet


def test_csdw(packet):
    assert packet.sync_offset == 0
    assert packet.alignment == 0
    assert packet.throughput == 0
    assert packet.packed == 1
    assert packet.iph == 1


def test_packed(packet):
    assert len(list(packet)) == 2974


def test_throughput(throughput):
    with pytest.raises(StopIteration):
        next(throughput)


def test_throughput_len(throughput):
    with pytest.raises(TypeError):
        len(throughput)