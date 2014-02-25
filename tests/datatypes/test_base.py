
from mock import Mock

from chapter10.datatypes import base


def test_lazy(f, monkeypatch):
    body = base.Base(Mock())
    assert body.__dict__.get('data') is None


def test_load(f, monkeypatch):
    body = base.Base(Mock())
    assert body.data is not None
