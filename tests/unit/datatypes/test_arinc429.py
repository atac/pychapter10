
import os

import pytest

from chapter10 import C10
from chapter10 import arinc429
from test_sanity import dummy_packet

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'sample.c10')


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x39, 0x3f)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        a = arinc429.ARINC429.from_string(raw)
        a.parse()


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet, arinc429.ARINC429):
            break
    assert packet.count == len(packet)
