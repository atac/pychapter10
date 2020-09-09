
from chapter10 import C10, analog
from fixtures import ANALOG


def test_csdw():
    for packet in C10(ANALOG):
        if isinstance(packet, analog.AnalogF1):
            assert packet.mode == 0
            assert packet.length == 16
            assert packet.subchannel == 0
            assert packet.factor == 0
            assert packet.same == 1
            break


def test_count():
    for packet in C10(ANALOG):
        if isinstance(packet, analog.AnalogF1):
            assert len(packet.subchannels) == packet.subchannel_count
            break


def test_next():
    for packet in C10(ANALOG):
        if isinstance(packet, analog.AnalogF1):
            for i, sample in enumerate(packet):
                if i > 10:
                    return
