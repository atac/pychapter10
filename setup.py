#!/usr/bin/env python

from distutils import cmd
from distutils.core import setup
import shutil

cmdclass = {}
try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_docs'] = BuildDoc
except ImportError:
    pass


class Clean(cmd.Command):
    description = 'cleanup build directory'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree('build', True)


cmdclass['clean'] = Clean


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
