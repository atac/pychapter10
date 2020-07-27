
from chapter10 import C10
from fixtures import SAMPLE, EVENTS, INDEX


def test_tmats():
    for packet in C10(SAMPLE):
        if packet.data_type == 1:
            break
    assert list(packet['V-1'].items()) == [
        (b'V-1\\ID', b'DATASOURCE'),
        (b'V-1\\VN', b'HDS'),
        (b'V-1\\HDS\\SYS', b'sov2')]


def test_events():
    for packet in C10(EVENTS):
        if packet.data_type == 2:
            assert len(packet) == packet.count


def test_index():
    for packet in C10(INDEX):
        if packet.data_type == 3:
            if packet.index_type:
                for part in packet:
                    assert part.label == 'Node Index'
            else:
                for part in packet:
                    assert part.label == 'Root Index'
