
from chapter10 import C10, ms1553
from fixtures import SAMPLE


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet, ms1553.MS1553F1):
            for i, msg in enumerate(packet):
                assert len(msg.data) == msg.length
            break
    assert i+1 == len(packet)
