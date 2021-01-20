
from chapter10 import C10, uart
from fixtures import UART


def test_count():
    for packet in C10(UART):
        if isinstance(packet, uart.UARTF0):
            assert packet.iph
            assert len(list(packet)) == 2
            break


def test_message():
    expected = [
        (561182982, 55, 0),
        (561754950, 33, 0),
    ]
    for packet in C10(UART):
        if isinstance(packet, uart.UARTF0):
            for i, msg in enumerate(packet):
                assert (msg.ipts, msg.length, msg.subchannel) == expected[i]
            break
