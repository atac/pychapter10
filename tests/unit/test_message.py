
import pytest

from chapter10 import C10, message
from fixtures import dummy_packet, SAMPLE


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x31, 0x38)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        m = message.Message.from_string(raw)
        m.parse()


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet, message.Message):
            break
    assert packet.count == len(packet)
