
import os

from chapter10 import packet


def test_construct():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'sample.c10'), 'rb') as f:
        assert packet.Packet(f).data_type == 1


def test_raw():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'sample.c10'), 'rb') as f:
        p = packet.Packet(f)
        f.seek(0)
        assert f.read(p.packet_length) == str(p)
