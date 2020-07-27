
from chapter10 import C10, message
from fixtures import SAMPLE


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet, message.MessageF0):
            break
    assert packet.count == len(packet)
