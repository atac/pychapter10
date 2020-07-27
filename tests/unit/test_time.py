
from chapter10 import time, C10
from fixtures import SAMPLE


def test_time():
    for packet in C10(SAMPLE):
        if isinstance(packet, time.TimeF1):
            break
    assert packet.time.strftime('%j %H:%M:%S') == '034 11:34:11'
