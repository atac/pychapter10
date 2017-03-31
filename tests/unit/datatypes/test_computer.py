
import os

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest

from chapter10.datatypes import computer
from chapter10 import C10

SAMPLE = os.path.join(os.path.dirname(__file__), '..', 'sample.c10')
EVENTS = os.path.join(os.path.dirname(__file__), '..', 'event.c10')
INDEX = os.path.join(os.path.dirname(__file__), '..', 'index.c10')


@pytest.mark.parametrize(
    ('data_type',), [(t,) for t in range(0x04, 0x08)])
def test_reserved(data_type):
    with pytest.raises(NotImplementedError):
        p = computer.Computer(Mock(
            file=Mock(tell=Mock(return_value=0),
                      read=Mock(return_value=b'1234')),
            pos=0,
            data_type=data_type,
            data_length=2))
        p.parse()


def test_tmats():
    for packet in C10(SAMPLE):
        if packet.data_type == 1:
            break
    assert list(packet.body['V-1'].items()) == [
        (b'V-1\\ID', b'DATASOURCE'),
        (b'V-1\\VN', b'HDS'),
        (b'V-1\\HDS\\SYS', b'sov2')]


def test_events():
    for packet in C10(EVENTS):
        if packet.data_type == 2:
            assert len(packet.body) == packet.body.recording_event_entry_count


def test_index():
    for packet in C10(INDEX):
        if packet.data_type == 3:
            if packet.body.index_type:
                for part in packet.body:
                    assert part.label == 'Node Index'
            else:
                for part in packet.body:
                    assert part.label == 'Root Index'
