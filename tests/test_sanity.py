
import pytest

from chapter10 import C10
from chapter10.packet import InvalidPacket
from fixtures import dummy_packet


@pytest.mark.parametrize('size', (6, 8, 10, 12, 16))
@pytest.mark.parametrize('data_type', range(120))
def test_sanity(data_type, size):
    """Test default constructors for every data type and 5 base sizes."""

    raw = dummy_packet(data_type, size)
    try:
        C10.from_string(raw)
    except (NotImplementedError, InvalidPacket, TypeError):
        return
