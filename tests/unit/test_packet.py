
import pickle
from unittest.mock import Mock
from io import BytesIO

import pytest

from chapter10 import packet, computer
from chapter10.util import BitFormat
from fixtures import SAMPLE


class TestPacket:
    @pytest.fixture
    def p(self):
        class Dummy(packet.Packet):
            Message = Mock()
        return Dummy(data_length=20)

    # Constructor
    def test_construct_file(self):
        with open(SAMPLE, 'rb') as f:
            assert packet.Packet(f).data_type == 1

    def test_construct_blank(self, p):
        assert p._messages == []

    # __iter__
    def test_iter_messages(self, p):
        p._messages = [0, 1, 2, 3]
        for i, msg in enumerate(p):
            assert i == msg

    def test_iter_stop(self):
        count = 0
        for msg in packet.Packet():
            count += 1
        assert count == 0

    # __next__
    def test_next_from_packet(self, p):
        for msg in p:
            pass
        assert p.Message.called_with(p)

    def test_next_from_list(self, p):
        p._messages = [0, 1, 2]
        assert list(p) == [0, 1, 2]
        assert not p.Message.called

    # __bytes__
    def test_bytes_file(self):
        with open(SAMPLE, 'rb') as f:
            p = computer.ComputerF1(f)
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

        assert len(result) == 32
        assert len(p.__class__(BytesIO(result))) == 4

    # __len__
    def test_len_messages(self, p):
        p._messages = [0, 1, 2]
        assert len(p) == 3

    def test_len_count(self, p):
        p.count = 2
        p._messages = None
        assert len(p) == 2

    def test_len_message_no_format(self, p):
        p._messages = None
        p.data_length = 24
        p.Message.length = 5
        p.Message.FORMAT = None
        assert len(p) == 4

    def test_len_message_format(self, p):
        p._messages = None
        p.data_length = 24
        p.Message.length = 4
        p.Message.FORMAT = BitFormat('u8 one')
        assert len(p) == 4

    def test_append(self, p):
        p.append(1, 2, 3)
        assert p._messages == [1, 2, 3]

    def test_clear(self, p):
        p._messages = [3, 1, 2]
        p.clear()
        assert p._messages == []

    def test_clear_file(self):
        with open(SAMPLE, 'rb') as f:
            p = packet.Packet(f)
        p.clear()
        assert p._messages == []

    def test_copy(self, p):
        p.channel_id = 12
        p2 = p.copy()
        p.channel_id = 11
        assert p2.channel_id == 12

    def remove(self, p):
        p._messages = [0, 1, 2]
        p.remove(1)
        assert p._messages == [0, 2]

    def test_pickle(self):
        p = packet.Packet(channel_id=12)
        s = pickle.dumps(p)
        assert pickle.loads(s).__dict__ == p.__dict__


class TestMessage:
    @pytest.fixture
    def fake(self):
        class FakePacket:
            buffer = BytesIO(b'0' * 1000)
            data_length = 5
            secondary_header = 0

            class Message(packet.Message):
                length = 3

        return FakePacket()

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
        assert bytes(msg) == b'\x12\xff\x00\x00'
