
from mock import Mock

from chapter10 import c10


def test_construct(monkeypatch):
    monkeypatch.setattr(c10, 'Packet', Mock(return_value=[]))
    c10.C10(Mock(side_effect=EOFError))
    assert c10.Packet.called
