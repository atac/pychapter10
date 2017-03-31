
import os

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest

from chapter10 import C10
from chapter10.datatypes import ARINC429

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'sample.c10')


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x39, 0x3f)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        a = ARINC429(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value=b'1234')),
            pos=0,
            data_type=data_type,
            data_length=2))
        a.parse()


def test_count():
    for packet in C10(SAMPLE):
        if isinstance(packet.body, ARINC429):
            break
    assert packet.body.message_count == len(packet.body)
