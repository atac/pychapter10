#!/usr/bin/env python

"""Get a list of channel IDs for a chapter 10 file."""

from optparse import OptionParser
from chapter10 import Packet


if __name__ == '__main__':
    parser = OptionParser('%prog <inputfile>')
    options, args = parser.parse_args()
    if not len(args):
        parser.print_usage()

    else:
        ids = set()

        with open(args[0], 'rb') as f:
            while True:
                try:
                    packet = Packet(f)
                    ids.add(packet.channel)
                except EOFError:
                    break

            # print out the ids
            ids = list(ids)
            ids.sort()
            print 'Channel IDs:'
            for id in ids:
                print '\t%s' % id
