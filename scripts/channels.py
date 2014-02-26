#!/usr/bin/env python

"""Display channel information for an IRIG 106 Chapter 10 file."""

import sys

from chapter10 import C10


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: channels.py <file>'
        raise SystemExit

    channels = {}

    c = C10(sys.argv[1])
    for packet in c:
        if packet.channel_id not in channels:
            channels[packet.channel_id] = {
                'packets': 0, 'type': packet.data_type,
                'id': packet.channel_id}
        channels[packet.channel_id]['packets'] += 1

    for channel in channels.values():
        print '-' * 80
        print 'Channel ID: %s' % channel['id']
        print 'Data Type: %s' % hex(channel['type'])
        print 'Packets: %s' % channel['packets']
        print '-' * 80

    print 'Summary for %s:' % sys.argv[1]
    print '    Size: %s bytes' % c.size
    print '    Packets: %s' % len(c)
    print '    Channels: %s' % len(channels)
