
from chapter10 import C10, arinc429

from fixtures import SAMPLE


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet, arinc429.ARINC429F0):
            for i, msg in enumerate(packet):
                if i == 0:
                    assert msg.gap_time == 0
            break
    assert i+1 == 221
    assert len(packet) == 221
