#!/usr/bin/env python

"""Extract video from a chapter 10 file."""

from array import array
import atexit
import os
import sys

from chapter10 import C10


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: dump_video.py <file> [<output>]'

    # Select the output directory and ensure it exists.
    output = os.path.abspath(
        os.curdir if not len(sys.argv) > 2 else sys.argv[2])
    if not os.path.exists(output):
        os.makedirs(output)

    # Walk the packets and write out any video channels to their own mpg file.
    out = {}
    for packet in C10(sys.argv[1]):
        if packet.data_type in (0x40, 0x41, 0x42):

            # Open an output file (and ensure it closes later).
            if packet.channel_id not in out:
                out[packet.channel_id] = open(
                    os.path.join(output, str(packet.channel_id)) + '.mpg')
                atexit.register(out[packet.channel_id].close)

            a = array('H', packet.body.data[4:])
            a.byteswap()
            out[packet.channel_id].write(a.tostring())
