

def walk_packets(c10, args={}):
    """Walk a chapter 10 file based on sys.argv (type, channel, etc.)."""

    # Apply defaults.
    args['--type'] = args.get('--type', '') or ''
    args['--channel'] = args.get('--channel', '') or ''
    args['--exclude'] = args.get('--exclude', '') or ''

    # Parse types (if given) into ints.
    types = [t.strip() for t in args['--type'].split(',') if t.strip()]
    types = [int(t, 16) if t.startswith('0x') else int(t) for t in types]

    # Parse channel selection.
    channels = [c.strip() for c in args['--channel'].split(',') if c.strip()]
    exclude = [e.strip() for e in args['--exclude'].split(',') if e.strip()]

    for packet in c10:
        if channels and str(packet.channel_id) not in channels:
            continue
        elif str(packet.channel_id) in exclude:
            continue
        elif types and packet.data_type not in types:
            continue

        yield packet
