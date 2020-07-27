
from chapter10 import C10, pcm
from fixtures import PCM

# TODO: only throughput is tested so far


def test_pcm():
    for packet in C10(PCM):
        if isinstance(packet, pcm.PCMF1):
            break
    assert packet.mode == 4
