
from mock import Mock
import pytest

from chapter10.datatypes import discrete


@pytest.mark.parametrize(
    ('data_type',), [(0x28,)] + [(t,) for t in range(0x2a, 0x30)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        b = discrete.Discrete(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value=b'1234')),
            data_type=data_type,
            data_length=2))
        b.parse()
