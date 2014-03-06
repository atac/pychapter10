#!/usr/bin/env python

"""usage: headers.py <file> [options]

Options:
    -c CHANNEL..., --channel CHANNEL...  Specify channels to include(csv).
    -e CHANNEL..., --exclude CHANNEL...  Specify channels to ignore (csv).
    -t TYPE, --type TYPE  The types of data to show (csv, may be decimal or \
hex eg: 0x40)."""

from docopt import docopt

from chapter10 import C10

from walk import walk_packets

if __name__ == '__main__':
    args = docopt(__doc__)

    for packet in walk_packets(C10(args['<file>']), args):
        packet.print_header()
