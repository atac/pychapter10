
from mock import Mock
import pytest

from chapter10 import c10


def test_construct(monkeypatch):
    monkeypatch.setattr(c10, 'Packet', Mock(side_effect=EOFError,
                                            return_value=[]))
    f = Mock()
    assert c10.C10(f).file == f


def test_next(monkeypatch):
    monkeypatch.setattr(c10.C10, 'find_and_parse', Mock(return_value=12))
    assert c10.C10(Mock()).next() == 12


def test_next_stop(monkeypatch):
    monkeypatch.setattr(c10.C10, 'find_and_parse', Mock(side_effect=EOFError))
    with pytest.raises(StopIteration):
        c10.C10(Mock()).next()
