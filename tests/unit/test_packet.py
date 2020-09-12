
from io import BytesIO

import pytest

from chapter10 import packet
from chapter10.util import BitFormat
from fixtures import SAMPLE


def test_construct():
    with open(SAMPLE, 'rb') as f:
        assert packet.Packet(f).data_type == 1


def test_raw():
    with open(SAMPLE, 'rb') as f:
        p = packet.Packet(f)
        f.seek(0)
        assert f.read(p.packet_length) == bytes(p)


@pytest.fixture
def fake():
    class FakePacket:
        buffer = BytesIO(b'0' * 1000)
        data_length = 5
        secondary_header = 0

        class Message(packet.Message):
            length = 3

    return FakePacket()


class TestMessage:
    def test_from_packet_eof(self, fake):
        fake.buffer.seek(1000)
        with pytest.raises(EOFError):
            fake.Message.from_packet(fake)

    def test_from_packet_iph(self, fake):
        fake.Message.FORMAT = BitFormat('u8 ipts')
        fake.buffer = BytesIO(b'\xff\x00\x00\x00')
        msg = fake.Message.from_packet(fake)
        assert msg.ipts == 255

    def test_from_packet_no_format(self, fake):
        msg = fake.Message.from_packet(fake)
        assert len(msg.data) == fake.Message.length
