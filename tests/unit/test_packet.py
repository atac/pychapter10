
from unittest.mock import Mock
from io import BytesIO

import pytest

from chapter10 import packet
from chapter10.util import BitFormat
from fixtures import SAMPLE


class TestPacket:
    def test_construct_file(self):
        with open(SAMPLE, 'rb') as f:
            assert packet.Packet(f).data_type == 1

    def test_construct_blank(self):
        p = packet.Packet()
        assert p._messages == []

    def test_iter_messages(self):
        p = packet.Packet()
        p._messages = [0, 1, 2, 3]
        for i, msg in enumerate(p):
            assert i == msg

    def test_iter_stop(self):
        count = 0
        for msg in packet.Packet():
            count += 1
        assert count == 0

    def test_next_from_packet(self):
        class Dummy(packet.Packet):
            Message = Mock()

        p = Dummy()
        for msg in p:
            pass
        assert Dummy.Message.called_with(p)

    def test_next_from_list(self):
        class Dummy(packet.Packet):
            Message = Mock()

        p = Dummy()
        p._messages = [0, 1, 2]
        assert list(p) == [0, 1, 2]
        assert not Dummy.Message.called

    def test_bytes_file(self):
        with open(SAMPLE, 'rb') as f:
            p = packet.Packet(f)
            f.seek(0)
            assert f.read(p.packet_length) == bytes(p)

    def test_bytes_generated(self):
        class Dummy(packet.Packet):
            class Message(packet.Message):
                length = 1

        p = Dummy()
        p.csdw = 0
        p._messages = [packet.Message(b'\01'), packet.Message(b'\02')]
        result = bytes(p)

        assert len(result) == 30
        assert len(Dummy(BytesIO(result))) == 2


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

    def test_blank(self, fake):
        msg = fake.Message('')
        assert msg.data == ''

    def test_new(self, fake):
        msg = fake.Message('', hello='World')
        assert msg.hello == 'World'

    def test_bytes(self, fake):
        fake.Message.FORMAT = BitFormat('u4 one\nu4 two')
        msg = fake.Message(b'\xff\x00', one=1, two=2)
        assert bytes(msg) == b'\x12\xff\x00'
