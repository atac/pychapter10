#!/usr/bin/env python

"""usage: channels.py <file> [options]

Options:
    -c CHANNEL..., --channel CHANNEL...  Specify channels to include(csv).
    -e CHANNEL..., --exclude CHANNEL...  Specify channels to ignore (csv).
    -t TYPE, --type TYPE  The types of data to show (csv, may be decimal or \
hex eg: 0x40)."""

from docopt import docopt

from chapter10 import C10
from chapter10.datatypes import get_label

from walk import walk_packets


if __name__ == '__main__':
    args = docopt(__doc__)

    channels = {}
    packets = 0
    size = 0

    for packet in walk_packets(C10(args['<file>']), args):
        size += packet.packet_length
        packets += 1
        if packet.channel_id not in channels:
            channels[packet.channel_id] = {
                'packets': 0, 'type': packet.data_type,
                'id': packet.channel_id}
        channels[packet.channel_id]['packets'] += 1

    print 'Channel ID      Data Type                                   Packets'
    print '-' * 80
    for channel in channels.values():
        print ('Channel %s' % channel['id']).ljust(15),
        print ('%s - %s' % (hex(channel['type']),
                            get_label(channel['type']))).ljust(35),
        print ('%s packets' % channel['packets']).rjust(20)

    unit = 'bytes'
    if size > 1024:
        size = size / 1024
        unit = 'kb'

        if size > 1024:
            size = size / 1024
            unit = 'mb'

            if size > 1024:
                size = size / 1024
                unit = 'gb'

    print '-' * 80
    print 'Summary for %s:' % args['<file>']
    print '    Size: %s %s' % (size, unit)
    print '    Packets: %s' % packets
    print '    Channels: %s' % len(channels)
