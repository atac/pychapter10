
import os

from mock import Mock
import pytest

from chapter10.datatypes import computer
from chapter10.datatypes.base import Data
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
            data_type=data_type,
            data_length=2))
        p.parse()


def test_tmats():
    for packet in C10(SAMPLE):
        if packet.data_type == 1:
            break
    assert packet.body.tmats['V-1'].items() == [('V-1\\ID', 'DATASOURCE'),
                                                ('V-1\\VN', 'HDS'),
                                                ('V-1\\HDS\\SYS', 'sov2')]


def test_events():
    for packet in C10(EVENTS):
        if packet.data_type == 2:
            assert len(packet.body.events) == packet.body.reec


def test_index():
    for packet in C10(INDEX):
        if packet.data_type == 3:
            if packet.body.it:
                for part in packet.body.indices:
                    assert isinstance(part, computer.NodeIndex)
            else:
                for part in packet.body:
                    assert isinstance(part, Data)
