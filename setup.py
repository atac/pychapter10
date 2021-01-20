#!/usr/bin/env python

from contextlib import suppress
from glob import glob
from setuptools import setup, Command
import os
import shutil
import sys

sys.path.insert(0, 'chapter10')
from version import version
sys.path.remove('chapter10')

cmdclass = {}
with suppress(ImportError):
    from sphinx.setup_command import BuildDoc
    cmdclass['build_docs'] = BuildDoc


class CleanCommand(Command):
    description = 'cleanup build and dist files'
    user_options = []

    CLEAN_FILES = '''
        build dist *.pyc *.tgz *.egg-info __pycache__ dependencies
        htmlcov docs/html docs/doctrees MANIFEST coverage.xml junit*.xml
    '''

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        here = os.path.abspath(os.path.dirname(__file__))
        for path_spec in self.CLEAN_FILES.split():
            abs_paths = glob(os.path.normpath(os.path.join(here, path_spec)))
            for path in abs_paths:
                print('removing %s' % os.path.relpath(path))
                if os.path.isdir(path):
                    shutil.rmtree(path, True)
                else:
                    with suppress(os.error):
                        os.remove(path)


cmdclass['clean'] = CleanCommand

setup(
    name='pychapter10',
    version=version,
    author='Micah Ferrill',
    author_email='ferrillm@avtest.com',
    description='A parser library for the IRIG 106 Chapter 10 data format.',
    long_description=open('README.rst').read(),
    url='https://github.com/atac/pychapter10',
    install_requires=['bitstruct>=8.11.0'],
    packages=['chapter10'],
    cmdclass=cmdclass,
    python_requires='>=py3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    command_options={
        'build_docs': {
            'build_dir': ('setup.py', 'docs',),
        }
    }
)
