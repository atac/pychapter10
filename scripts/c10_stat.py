#!/usr/bin/env python

__doc__ = """usage: c10_stat.py <file> [options]

Options:
    -c CHANNEL..., --channel CHANNEL...  Specify channels to include(csv).
    -e CHANNEL..., --exclude CHANNEL...  Specify channels to ignore (csv).
    -t TYPE, --type TYPE                 The types of data to show (csv, may \
be decimal or hex eg: 0x40)."""

from docopt import docopt

from chapter10 import C10
from chapter10.datatypes import get_label
from chapter10.walk import walk_packets


if __name__ == '__main__':
    args = docopt(__doc__)

    channels = []
    packets = 0
    size = 0

    for packet in walk_packets(C10(args['<file>']), args):
        size += packet.packet_length
        packets += 1
        channel_index = None
        for i, channel in enumerate(channels):
            if channel['id'] == packet.channel_id and \
                    channel['type'] == packet.data_type:
                channel_index = i
                break
        if channel_index is None:
            channel_index = len(channels)
            channels.append({'packets': 0,
                            'type': packet.data_type,
                            'id': packet.channel_id})
        channels[channel_index]['packets'] += 1

    print('Channel ID      Data Type' + 'Packets'.rjust(47))
    print('-' * 80)
    for channel in channels:
        print (''.join((('Channel %s' % channel['id']).ljust(15),
                       ('%s - %s' % (hex(channel['type']),
                                     get_label(channel['type']))).ljust(35),
                       ('%s packets' % channel['packets']).rjust(20))))

    units = ['gb', 'mb', 'kb']
    unit = 'b'
    while size > 1024 and units:
        size /= 1024.0
        unit = units.pop()

    print('-' * 80)
    print('Summary for %s:' % args['<file>'])
    print('    Size: %s %s' % (round(size, 2), unit))
    print('    Packets: %s' % packets)
    print('    Channels: %s' % len(channels))
