#!/usr/bin/env python

"""Compile all .ui files into .py using PyQt4."""

import glob
import os


if __name__ == '__main__':
    for ui in glob.glob(os.path.join(os.path.dirname(__file__), '../ui/*.ui')):
        os.system('pyuic4 %s -o %s' % (ui, ui[:-2] + 'py'))
