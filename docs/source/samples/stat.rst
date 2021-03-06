
Scan Channels and Data Types
============================

Don't mind the heavy formatting in the printing section. It's simply whitespace
handling::

    #!/usr/bin/env python

    import sys

    from chapter10 import C10, TYPES


    if __name__ == '__main__':

        # Get commandline args.
        if len(sys.argv) < 2:
            print('usage: stat.py <file>')
            raise SystemExit
        filename = sys.argv[-1]

        # Scan channel info
        channels = {}
        for packet in C10(filename):
            key = (packet.channel_id, packet.data_type)
            if key not in channels:
                channels[key] = {
                    'packets': 0,
                    'size': 0,
                    'type': packet.data_type,
                    'id': packet.channel_id}

            channels[key]['packets'] += 1
            channels[key]['size'] += packet.packet_length

        # Print details for each channel.
        print('{} {:>13} {:>38} {:>16}'.format(
            'Channel ID', 'Data Type', 'Packets', 'Size'))
        print('-' * 80)
        packets, size = 0, 0
        for key, channel in sorted(channels.items()):
            print('Channel {:<7}'.format(channel['id']), end='')
            hextype = hex(channel['type'])[2:]
            label = TYPES[channel['type']].__name__
            print('{:>2} - {:<30}'.format(hextype, label), end='')
            print('{:,}'.format(channel['packets']).rjust(13), end='')
            print('{:>16,}b'.format(channel['size']))
            packets += channel['packets']
            size += channel['size']

        # Print file summary.
        print('-' * 80)
        print('''Summary for {}:
        Channels: {}
        Packets: {:,}
        Size: {:,} bytes'''.format(filename, len(channels), packets, size))
