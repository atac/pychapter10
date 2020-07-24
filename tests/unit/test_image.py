
import pytest

from chapter10 import image
from test_sanity import dummy_packet


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x4B, 0x50)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        i = image.Image.from_string(raw)
        i.parse()
