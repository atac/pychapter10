
import sys

from cx_Freeze import setup, Executable

kwargs = dict(
    name='Chapter10',
    version='0.1',
    author='Micah Ferrill',
    author_email='mcferrill@gmail.com',
    description='A parser library and toolset for the IRIG 106 Chapter 10 \
data format.',
    options={
        'build_exe': {
            'includes': 'atexit',
            'excludes': ['_ctypes', '_hashlib', '_socket', '_ssl', 'bz2'],
            'append_script_to_exe': True,
            'optimize': 2,
            'include_files': (
                ('scripts/mplayer.exe', 'mplayer.exe'),
            )
        }
    },
    executables=[
        Executable('scripts/c10_stat.py', base='Console'),
        Executable('scripts/c10_dump.py', base='Console'),
        Executable('scripts/c10_copy.py', base='Console'),
        Executable('scripts/video.py',
                   base=sys.platform == 'win32' and 'Win32GUI' or None),
    ],
    packages=[
        'chapter10',
        'chapter10.datatypes',
    ])

setup(**kwargs)
