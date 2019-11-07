
Make 1553 Data Single-Bus
=========================

::

    #!/usr/bin/env python

    """usage: allbus.py <src> <dst> [-b]

    Switch 1553 format 1 messages to the same bus. Defaults to A unless "-b" flag
    is present.
    """

    import sys

    from chapter10 import C10


    if __name__ == '__main__':

        # Parse args
        if len(sys.argv) < 3:
            print(__doc__)
            raise SystemExit
        bus = int(sys.argv[-1].lower() == '-b')
        if bus:
            src, dst = sys.argv[-3:-1]
        else:
            src, dst = sys.argv[-2:]

        # Walk through the source file and write data to the output file.
        with open(dst, 'wb') as out:
            for packet in C10(src):

                raw = bytes(packet)

                # Write non-1553 out as-is.
                if packet.data_type != 0x19:
                    out.write(raw)
                    continue

                # Write out packet header secondary if applicable) and CSDW.
                offset = 28
                if packet.flags & (1 << 7):
                    offset += 12
                out.write(raw[:offset])

                # Walk through messages and update bus ID as needed.
                for msg in packet:
                    msg.bus = bus
                    packed = bytes(msg)
                    out.write(packed)
                    offset += len(packed)

                # Write filler if needed.
                for i in range(packet.packet_length - offset):
                    out.write(b'0')
