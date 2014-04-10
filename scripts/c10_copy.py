#!/usr/bin/env python

__doc__ = """usage: c10_copy.py <src> <dst> [options]

Options:
    -c CHANNEL..., --channel CHANNEL...  Specify channels to include (csv).
    -e CHANNEL..., --exclude CHANNEL...  Specify channels to ignore (csv).
    -t TYPE, --type TYPE                 The types of data to copy (csv, may\
 be decimal or hex eg: 0x40)
    -f --force                           Overwrite existing files."""

import os

from docopt import docopt

from chapter10 import C10
from chapter10.walk import walk_packets


if __name__ == '__main__':
    args = docopt(__doc__)

    # Don't overwrite unless explicitly required.
    if os.path.exists(args['<dst>']) and not args['--force']:
        print('dst file already exists. Use -f to overwrite.')
        raise SystemExit

    with open(args['<dst>'], 'wb') as out:
        for packet in walk_packets(C10(args['<src>']), args):
            raw = bytes(packet)
            if len(raw) == packet.packet_length:
                out.write(raw)
