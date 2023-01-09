
from datetime import datetime
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


def test_time_bytes_with_ms():
    t0 = time.TimeF1(date_format=1)

    # Note trailing 0, IRIG 106-15 Time F1 only allows precision
    # to tenths of ms, but fromisoformat requires specifying to 1-ms.
    t0.time = datetime.fromisoformat('2022-12-05 01:02:03.450')

    raw = bytes(t0)

    assert time.TimeF1(io.BytesIO(raw)).time == t0.time
