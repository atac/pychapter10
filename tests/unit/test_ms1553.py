
import pytest

from chapter10 import C10
from chapter10 import ms1553
from fixtures import dummy_packet, SAMPLE


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in [0x18] + list(range(0x1B, 0x20))])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        m = ms1553.MS1553.from_string(raw)
        m.parse()


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet, ms1553.MS1553):
            break
    assert packet.message_count == len(packet)
