#!/usr/bin/env python3

"""Script to benchmark Chapter 10 parsing."""

from datetime import timedelta
import sys
import os
import time

try:
    from i106 import C10
except ImportError:
    from chapter10 import C10

if os.environ.get('LIBRARY', None) == 'c10':
    from chapter10 import C10

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

RUNS = 100
SOURCE_FILE = 'tests/ethernet.c10'

file_size = os.stat(SOURCE_FILE).st_size
total = file_size * RUNS
bytes_to_go = total


def show_progress(percent):
    """Takes a percentage (as a decimal fraction) and shows progress."""

    bar = ('=' * int(74 * percent)).ljust(74)
    sys.stdout.write('[{}] {}%\r'.format(bar, round(percent * 100)))
    sys.stdout.flush()


if __name__ == '__main__':
    start_time = time.perf_counter()
    print('Running with %s' % (os.environ.get('LIBRARY', 'i106')))
    if tqdm:
        progress = tqdm(
            total=total, unit='bytes', unit_scale=True, leave=False)
    for i in range(RUNS):
        for packet in C10(SOURCE_FILE):

            if tqdm:
                progress.update(packet.packet_length)
            else:
                bytes_to_go -= packet.packet_length
                percent = (total - bytes_to_go) / total
                show_progress(percent)

            for msg in packet:
                bus = getattr(msg, 'bus', None)
    print('\nCompleted in %s' %
          timedelta(seconds=time.perf_counter() - start_time))
