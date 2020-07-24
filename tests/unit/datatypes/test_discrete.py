
import pytest

from chapter10 import discrete
from test_sanity import dummy_packet


@pytest.mark.parametrize(
    ('data_type',), [(0x28,)] + [(t,) for t in range(0x2a, 0x30)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        b = discrete.Discrete.from_string(raw)
        b.parse()
