
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

import os
import pytest

from chapter10 import c10


def test_construct(monkeypatch):
    monkeypatch.setattr(c10, 'Packet', Mock(side_effect=EOFError,
                                            return_value=[]))
    f = Mock()
    assert c10.C10(f).file.io == f


def test_next(monkeypatch):
    with open(
            os.path.join(os.path.dirname(__file__), 'sample.c10'), 'rb') as f:
        monkeypatch.setattr(c10, 'Packet', Mock(
            return_value=Mock(
                packet_length=26, check=Mock(return_value=True))))
        assert c10.C10(f).next().packet_length == 6680


def test_next_stop(monkeypatch):
    with pytest.raises(StopIteration):
        c10.C10(Mock(read=Mock(side_effect=EOFError))).next()
