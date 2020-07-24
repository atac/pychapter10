
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

import pytest

from chapter10 import c10
from fixtures import SAMPLE


def test_construct(monkeypatch):
    monkeypatch.setattr(c10, 'Packet', Mock(side_effect=EOFError,
                                            return_value=[]))
    f = Mock()
    assert c10.C10(f).file.io == f


def test_next(monkeypatch):
    with open(SAMPLE, 'rb') as f:
        assert c10.C10(f).next().packet_length == 6680


def test_next_stop(monkeypatch):
    with pytest.raises(StopIteration):
        c10.C10(Mock(read=Mock(side_effect=EOFError))).next()
