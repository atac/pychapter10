
from distutils.core import setup

setup(
    name='Chapter10',
    version='0.1',
    author='Micah Ferrill',
    author_email='mcferrill@gmail.com',
    description='A parser library for the IRIG 106 Chapter 10 data format.',
    packages=[
        'chapter10',
        'chapter10.datatypes',
    ],
)
