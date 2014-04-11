
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest

from chapter10.datatypes import i1394


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x5A, 0x60)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        b = i1394.I1394(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value=b'1234')),
            data_type=data_type,
            data_length=2))
        b.parse()
