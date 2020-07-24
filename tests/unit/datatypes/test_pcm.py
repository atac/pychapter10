
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest

from chapter10 import pcm
from test_sanity import dummy_packet


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in [0x8] + list(range(0x0A, 0x10))])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        p = pcm.PCM.from_string(raw)
        p.parse()
