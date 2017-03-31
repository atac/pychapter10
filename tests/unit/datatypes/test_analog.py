
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest

from chapter10.datatypes import analog


@pytest.mark.parametrize(
    ('data_type',),
    ((0x20,), (0x22,), (0x23,), (0x24,), (0x25,), (0x26,), (0x27,)))
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        a = analog.Analog(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value=b'1234')),
            pos=0,
            data_type=data_type,
            data_length=2))
        a.parse()
