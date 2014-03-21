#!/usr/bin/env python

"""Compile all .ui files into .py using PySide."""

import glob
import os


if __name__ == '__main__':
    for ui in glob.glob(os.path.join(os.path.dirname(__file__), '../ui/*.ui')):
        os.system('pyside-uic %s -o %s' % (ui, ui[:-2] + 'py'))
