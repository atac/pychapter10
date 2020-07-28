
from chapter10 import C10, ms1553
from fixtures import SAMPLE


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet, ms1553.MS1553F1):
            for i, msg in enumerate(packet):
                if i == 0:
                    assert msg.bus == 1
                assert len(msg.data) == msg.length
            break
    assert len(packet) == 82
    assert i+1 == len(packet)
