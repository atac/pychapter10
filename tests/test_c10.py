
from mock import Mock

from chapter10 import c10


def test_construct(monkeypatch):
    monkeypatch.setattr(c10, 'Packet', Mock(side_effect=EOFError,
                                            return_value=[]))
    c10.C10(Mock())
    assert c10.Packet.called
