#!/usr/bin/env python

import sys

from chapter10 import C10

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: headers.py <file>'
        raise SystemExit

    for packet in C10(sys.argv[1]):
        packet.print_header()
