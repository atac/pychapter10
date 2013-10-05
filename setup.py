'''
The distutils setup script
'''

from distutils.core import setup

setup(
    name = 'Chapter10',
    version = '0.1',
    author = 'Micah Ferrill',
    author_email = 'webmaster@blazeofglory.org',
    url = 'http://micahsmusings.com.com/c10/',
    download_url = 'http://micahsmusings.com/c10/download/',
    description = 'A parser library for the Chapter 10 data format.',
    long_description = '''Provides a parsing library as well as multiple tools
for basic data reading purposes.''',
    packages = [
        'chapter10',
        'chapter10.datatypes',
    ],
    scripts = [
    ],
)