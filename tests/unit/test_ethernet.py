
from chapter10 import C10
from fixtures import ETHERNET


def test_format_0():
    for packet in C10(ETHERNET):
        if packet.data_type == 0x68:
            for msg in packet:
                assert msg.ethernet_speed == 2
            break
    assert len(packet) == packet.count


def test_format_1_count():
    for packet in C10(ETHERNET):
        if packet.data_type == 0x69:
            for i, msg in enumerate(packet):
                if i == 0:
                    assert msg.dst_port == 9311
                assert len(msg.data) == msg.length
            break
    assert i+1 == len(packet)
    assert len(packet) == 2


def test_bytes():
    for packet in C10(ETHERNET):
        if packet.data_type == 0x68:
            break
    assert packet.buffer.getvalue() == bytes(packet)
