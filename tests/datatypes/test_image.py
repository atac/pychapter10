
from mock import Mock
import pytest

from chapter10.datatypes import image


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x4B, 0x50)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        i = image.Image(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value='1234')),
            data_type=data_type,
            data_length=2))
        i.parse()
