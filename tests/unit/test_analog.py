
import pytest

from chapter10 import analog
from test_sanity import dummy_packet


@pytest.mark.parametrize(
    ('data_type',),
    ((0x20,), (0x22,), (0x23,), (0x24,), (0x25,), (0x26,), (0x27,)))
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        a = analog.Analog.from_string(raw)
        a.parse()
