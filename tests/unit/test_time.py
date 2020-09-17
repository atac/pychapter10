
import io

from chapter10 import time, C10
from fixtures import SAMPLE


def test_time():
    for packet in C10(SAMPLE):
        if isinstance(packet, time.TimeF1):
            break
    assert packet.time.strftime('%j %H:%M:%S') == '343 16:47:12'


def test_time_bytes():
    for packet in C10(SAMPLE):
        if isinstance(packet, time.TimeF1):
            break
    raw = bytes(packet)
    assert time.TimeF1(io.BytesIO(raw)).time == packet.time
