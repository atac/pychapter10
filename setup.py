#!/usr/bin/env python

from distutils.core import setup

try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {'build_docs': BuildDoc}
except ImportError:
    cmdclass = {}

setup(
    name='Chapter10',
    version='0.1',
    author='Micah Ferrill',
    author_email='ferrillm@avtest.com',
    description='A parser library for the IRIG 106 Chapter 10 data format.',
    packages=[
        'chapter10',
        'chapter10.datatypes',
    ],
    cmdclass=cmdclass
)
