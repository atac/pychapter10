
from chapter10 import packet
from fixtures import SAMPLE


def test_construct():
    with open(SAMPLE, 'rb') as f:
        assert packet.Packet(f).data_type == 1


def test_raw():
    with open(SAMPLE, 'rb') as f:
        p = packet.Packet(f)
        f.seek(0)
        assert f.read(p.packet_length) == bytes(p)
