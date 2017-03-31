
import os

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest

from chapter10 import C10
from chapter10.datatypes import ms1553


SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'sample.c10')


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in [0x18] + list(range(0x1B, 0x20))])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        m = ms1553.MS1553(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value=b'1234')),
            pos=0,
            data_type=data_type,
            data_length=2))
        m.parse()


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet.body, ms1553.MS1553):
            break
    assert packet.body.message_count == len(packet.body)
