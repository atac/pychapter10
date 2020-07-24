
import pytest

from chapter10 import time
from test_sanity import dummy_packet


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x12, 0x18)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        time.Time.from_string(raw)
