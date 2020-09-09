
from chapter10 import C10, uart
from fixtures import UART


def test_count():
    for packet in C10(UART):
        if isinstance(packet, uart.UARTF0):
            assert packet.iph
            assert len(list(packet)) == 47
            break


def test_message():
    expected = [
        (30351299904, 20, 0),
        (30351322101, 20, 0),
        (30351344302, 20, 0),
        (30351366502, 20, 0),
        (30351388703, 20, 0),
        (30351420902, 20, 0),
    ]
    for packet in C10(UART):
        if isinstance(packet, uart.UARTF0):
            for i, msg in enumerate(packet):
                if i == len(expected):
                    return
                assert (msg.ipts, msg.length, msg.subchannel) == expected[i], i
