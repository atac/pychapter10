
from chapter10 import C10, pcm
from fixtures import PCM


def test_pcm():
    for packet in C10(PCM):
        if isinstance(packet, pcm.PCMF1):
            for i, word in enumerate(packet):
                assert len(word.data) == 12
            break
    assert i == len(packet)
