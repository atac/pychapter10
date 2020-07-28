
from chapter10 import video, C10
from fixtures import SAMPLE


def test_videof0():
    for packet in C10(SAMPLE):
        if isinstance(packet, video.VideoF0):
            for msg in packet:
                assert len(msg.data) == 188
            break
    assert len(packet) == 83


def test_videof1():
    for packet in C10(SAMPLE):
        if isinstance(packet, video.VideoF1):
            for msg in packet:
                assert len(msg.data) == 188
            break
    assert len(packet) == 83


def test_videof2():
    for packet in C10(SAMPLE):
        if isinstance(packet, video.VideoF2):
            for msg in packet:
                assert len(msg.data) == 188
            break
    assert len(packet) == 83
