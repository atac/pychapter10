
from mock import Mock

from chapter10 import c10


def test_construct(monkeypatch):
    monkeypatch.setattr(c10.C10, 'parse', Mock())
    c = c10.C10(Mock())
    assert c.parse.called
