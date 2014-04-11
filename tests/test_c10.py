
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
import pytest

from chapter10 import c10


def test_construct(monkeypatch):
    monkeypatch.setattr(c10, 'Packet', Mock(side_effect=EOFError,
                                            return_value=[]))
    f = Mock()
    assert c10.C10(f).file == f


def test_next(monkeypatch):
    f = Mock(read=Mock(return_value=b'\x25\xeb'), tell=Mock(return_value=2))
    monkeypatch.setattr(c10, 'Packet', Mock(
        return_value=Mock(packet_length=2, check=Mock(return_value=True))))
    assert c10.C10(f).next().packet_length == 2


def test_next_stop(monkeypatch):
    with pytest.raises(StopIteration):
        c10.C10(Mock(read=Mock(side_effect=EOFError))).next()
