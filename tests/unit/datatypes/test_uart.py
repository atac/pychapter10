
import pytest

from chapter10 import uart
from test_sanity import dummy_packet


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x51, 0x58)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        raw = dummy_packet(data_type, 20)
        uart.UART.from_string(raw)
