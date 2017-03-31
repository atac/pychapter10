
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest

from chapter10.datatypes import parallel


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x61, 0x68)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        p = parallel.Parallel(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value=b'1234')),
            pos=0,
            data_type=data_type,
            data_length=2))
        p.parse()
