#!/usr/bin/env python

from distutils import cmd
from distutils.core import setup
from glob import glob
import os
import shutil

cmdclass = {}
try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_docs'] = BuildDoc
except ImportError:
    pass


class Clean(cmd.Command):
    description = 'cleanup build files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree('build', True)
        shutil.rmtree('dist', True)
        try:
            os.remove('MANIFEST')
        except os.error:
            pass
        for f in glob('junit*') + glob('xunit*'):
            os.remove(f)
        shutil.rmtree('Chapter10.egg-info', True)
        shutil.rmtree('docs/build', True)


cmdclass['clean'] = Clean


setup(
    name='Chapter10',
    version='0.1',
    author='Micah Ferrill',
    author_email='ferrillm@avtest.com',
    description='A parser library for the IRIG 106 Chapter 10 data format.',
    install_requires=['bitstruct==8.11.0'],
    packages=['chapter10'],
    cmdclass=cmdclass
)
