
from mock import Mock

from chapter10 import packet


def test_construct(f, monkeypatch):
    monkeypatch.setattr(packet, 'map', {})
    monkeypatch.setattr(packet, 'Base', Mock())
    if f is not None:
        with open(f) as f:
            packet.Packet(f)


def test_raw(f, monkeypatch):
    monkeypatch.setattr(packet, 'map', {})
    monkeypatch.setattr(packet, 'Base', Mock())
    if f is not None:
        with open(f) as f:
            p = packet.Packet(f)
            f.seek(0)
            assert f.read(len(p)) == p.raw()
