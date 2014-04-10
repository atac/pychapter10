
from mock import Mock
import pytest

from chapter10.datatypes import video


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x43, 0x48)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        v = video.Video(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value='1234')),
            data_type=data_type,
            data_length=2))
        v.parse()
