
import os

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest

from chapter10 import C10
from chapter10.datatypes import message

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'sample.c10')


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x31, 0x38)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        m = message.Message(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value=b'1234')),
            data_type=data_type,
            data_length=2))
        m.parse()


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet.body, message.Message):
            break
    assert packet.body.counter == len(packet.body)
