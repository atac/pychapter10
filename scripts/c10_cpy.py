#!/usr/bin/env python

"""usage: c10_cpy.py <src> <dst> [options]

Options:
    -e CHANNEL..., --exclude CHANNEL...  Specify channels to ignore (csv) \
[default: ].
    -f --force                           Overwrite existing files.
    -t TYPE, --type TYPE                 Only copy a given data type \
[default: ]."""

import os

from docopt import docopt
from chapter10 import C10


if __name__ == '__main__':
    args = docopt(__doc__)

    # Parse types (if given) into ints.
    types = [t.strip() for t in args['--type'].split(',') if t.strip()]
    types = [int(t, 16) if t.startswith('0x') else int(t) for t in types]

    # Don't overwrite unless explicitly required.
    if os.path.exists(args['<dst>']) and not args['--force']:
        print 'dst file already exists. Use -f to overwrite.'
        raise SystemExit

    exclude = [e.strip() for e in args['--exclude'].split(',')]
    with open(args['<dst>'], 'wb') as out:
        for packet in C10(args['<src>']):
            if str(packet.channel_id) in exclude:
                continue
            elif types and packet.data_type not in types:
                continue
            out.write(packet.raw())
