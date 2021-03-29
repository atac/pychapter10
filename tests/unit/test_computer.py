
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


def test_index_csdw():
    for packet in C10(INDEX):
        if packet.data_type == 3:
            break
    assert (packet.count,
            packet.ipdh,
            packet.file_size_present,
            packet.index_type) == (5, 0, 1, 1)


def test_index_node():
    for packet in C10(INDEX):
        if packet.data_type == 3:
            if packet.index_type:
                break
    for node in packet:
        break
    assert node.ipts == 28892518346
    assert node.channel_id == 1
    assert node.data_type == 17
    assert node.offset == 28160


def test_index_root():
    for packet in C10(INDEX):
        if packet.data_type == 3:
            if not packet.index_type:
                break
    for part in packet:
        break
    assert part.ipts == 28892518346
    assert part.offset == 952252


def test_index_bytes():
    for packet in C10(INDEX):
        if packet.data_type == 3:
            break
    assert packet.buffer.getvalue() == bytes(packet)
