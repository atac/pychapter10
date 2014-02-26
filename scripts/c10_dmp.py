#!/usr/bin/env python

"""Usage: c10_dmp.py <file> [options]

Options:
    -o OUT, --output OUT  The directory to place files [default: .].
    -t TYPE, --type TYPE  The types of data to export (csv, may be decimal or \
hex eg: 0x40) [default: ]"""

from array import array
import atexit
import os

from docopt import docopt

from chapter10 import C10


if __name__ == '__main__':
    args = docopt(__doc__)

    # Parse types (if given) into ints.
    types = [t.strip() for t in args['--type'].split(',') if t.strip()]
    types = [int(t, 16) if t.startswith('0x') else int(t) for t in types]

    # Ensure OUT exists.
    if not os.path.exists(args['--output']):
        os.makedirs(args['--output'])

    out = {}
    for packet in C10(args['<file>']):
        if types and packet.data_type not in types:
            continue

        filename = os.path.join(args['--output'], str(packet.channel_id))

        # Ensure an output file is open (and will close) for a given channel.
        if filename not in out:

            # Don't overwrite without explicit direction.
            if os.path.exists(filename) and not args['--force']:
                print '%s already exists. Use -f to overwrite.' % filename
                break

            out[filename] = open(filename, 'wb')
            atexit.register(out[filename].close)

        data = packet.body.data[4:]

        # Special case for video.
        if packet.data_type in (0x40, 0x41, 0x42):
            a = array('H', data)
            a.byteswap()
            out[filename].write(a.tostring())
            continue

        # Write out raw packet body.
        out[filename].write(data)
