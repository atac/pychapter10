
import os
import sys

kwargs = dict(
    name='Chapter10',
    version='0.1',
    author='Micah Ferrill',
    author_email='mcferrill@gmail.com',
    description='A parser library and toolset for the IRIG 106 Chapter 10 \
data format.',
    options={
        'build_exe': {
            'excludes': ['_hashlib', '_socket', '_ssl', 'bz2'],
            'optimize': 2,
        },
        'install_exe': {
            'install_dir': os.path.join(os.path.dirname(__file__), 'bin'),
        },
    },
    packages=[
        'chapter10',
        'chapter10.datatypes',
        'mplayer_pyside',
    ])

try:
    from cx_Freeze import setup, Executable

    kwargs['executables'] = [
        Executable('scripts/c10_stat.py', base='Console'),
        Executable('scripts/c10_dump.py', base='Console'),
        Executable('scripts/c10_copy.py', base='Console'),
        Executable('scripts/video.py',
                   base=sys.platform == 'win32' and 'Win32GUI' or None),
    ]

    if sys.platform == 'win32':
        kwargs['options']['build_exe']['include_files'] = (
            ('scripts/mplayer.exe', 'mplayer.exe'),
        )

except ImportError:
    from distutils.core import setup


setup(**kwargs)
