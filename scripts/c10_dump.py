#!/usr/bin/env python

"""usage: c10_dmp.py <file> [options]

Options:
    -o OUT, --output OUT  The directory to place files [default: .].
    -c CHANNEL..., --channel CHANNEL...  Specify channels to include(csv).
    -e CHANNEL..., --exclude CHANNEL...  Specify channels to ignore (csv).
    -t TYPE, --type TYPE  The types of data to export (csv, may be decimal or \
hex eg: 0x40)
    -f, --force           Overwrite existing files."""

import atexit
import os

from docopt import docopt

from chapter10 import C10, datatypes
from chapter10.walk import walk_packets


if __name__ == '__main__':
    args = docopt(__doc__)

    # Ensure OUT exists.
    if not os.path.exists(args['--output']):
        os.makedirs(args['--output'])

    out = {}
    for packet in walk_packets(C10(args['<file>']), args):

        filename = os.path.join(args['--output'], str(packet.channel_id))

        if datatypes.format(packet.data_type)[0] == 8:
            filename += '.mpg'

        # Ensure an output file is open (and will close) for a given channel.
        if filename not in out:

            # Don't overwrite without explicit direction.
            if os.path.exists(filename) and not args['--force']:
                print '%s already exists. Use -f to overwrite.' % filename
                break

            out[filename] = open(filename, 'wb')
            atexit.register(out[filename].close)

        # Special case for video.
        if datatypes.format(packet.data_type)[0] == 8:
            data = ''.join([p.data for p in packet.body.mpeg])
        else:
            data = packet.body.data

        # Write out raw packet body.
        out[filename].write(data)
