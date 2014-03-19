
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
        windows=['scripts/video.py'],
        data_files=[('', ['scripts/mplayer.exe'])],
        zipfile=None,
        options=dict(
            py2exe=dict(
                packages=['chapter10'],
                includes=['PyQt4', 'sip', 'ui', 'encodings.utf_8'],
                dll_excludes=['msvcr71.dll'],
                ascii=True,
                bundle_files=2,
                optimize=2,
            )
        )
    ))
except ImportError:
    pass

import platform
if platform.architecture()[0] == '64bit':
    del kwargs['options']['py2exe']['bundle_files']

setup(**kwargs)
