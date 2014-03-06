#!/usr/bin/env python

"""Display channel information for an IRIG 106 Chapter 10 file."""

import sys

from chapter10 import C10
from chapter10.datatypes import get_label


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: channels.py <file>'
        raise SystemExit

    channels = {}
    packets = 0
    size = 0

    c = C10(sys.argv[1])
    for packet in c:
        size += packet.packet_length
        packets += 1
        if packet.channel_id not in channels:
            channels[packet.channel_id] = {
                'packets': 0, 'type': packet.data_type,
                'id': packet.channel_id}
        channels[packet.channel_id]['packets'] += 1

    for channel in channels.values():
        print '-' * 80
        print 'Channel ID: %s' % channel['id']
        print 'Data Type: %s (%s)' % (get_label(channel['type']),
                                      hex(channel['type']))
        print 'Packets: %s' % channel['packets']
        print '-' * 80

    print 'Summary for %s:' % sys.argv[1]
    print '    Size: %s bytes' % size
    print '    Packets: %s' % packets
    print '    Channels: %s' % len(channels)
