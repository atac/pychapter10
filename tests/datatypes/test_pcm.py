
from mock import Mock
import pytest

from chapter10.datatypes import pcm


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in [0x8] + list(range(0x0A, 0x10))])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        p = pcm.PCM(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value='1234')),
            data_type=data_type,
            data_length=2))
        p.parse()
