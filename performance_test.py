#!/usr/bin/env python3

"""Script to benchmark Chapter 10 parsing."""

from datetime import timedelta
import os
import time

from chapter10 import C10
from tqdm import tqdm

RUNS = 100
SOURCE_FILE = 'tests/eth.c10'

file_size = os.stat(SOURCE_FILE).st_size

if __name__ == '__main__':
    start_time = time.perf_counter()
    with tqdm(total=file_size * RUNS,
              unit='bytes',
              unit_scale=True,
              leave=False) as progress:
        for i in range(RUNS):
            for packet in C10(SOURCE_FILE):
                progress.update(packet.packet_length)
                try:
                    if len(packet):
                        for msg in packet:
                            bus = getattr(msg, 'bus', None)
                except TypeError:
                    continue
    print('Completed in %s' %
          timedelta(seconds=time.perf_counter() - start_time))
