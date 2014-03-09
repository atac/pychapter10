
from distutils.core import setup

kwargs = dict(
    name='Chapter10',
    version='0.1',
    author='Micah Ferrill',
    author_email='mcferrill@gmail.com',
    description='A parser library for the IRIG 106 Chapter 10 data format.',
    packages=[
        'chapter10',
        'chapter10.datatypes',
    ])

try:
    import py2exe
    kwargs.update(dict(
        console=['scripts/c10_stat.py',
                 'scripts/c10_dump.py',
                 'scripts/c10_copy.py'],
        zipfile=None,
        options=dict(
            py2exe=dict(
                packages=['chapter10'],
                excludes=['_ssl', '_ctypes', '_hashlib', '_socket', 'bz2',
                          'select', 'unicodedata'],
                dll_excludes=['msvcr71.dll'],
                ascii=True,
                optimize=2,
            )
        )
    ))
except ImportError:
    pass

setup(**kwargs)
