
import pytest

from chapter10 import i1394
from test_sanity import dummy_packet


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x5A, 0x60)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        i1394.I1394.from_string(raw)
