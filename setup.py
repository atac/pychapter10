
from cx_Freeze import setup, Executable

kwargs = dict(
    name='Chapter10',
    version='0.1',
    author='Micah Ferrill',
    author_email='mcferrill@gmail.com',
    description='A parser library for the IRIG 106 Chapter 10 data format.',
    options={
        'build_exe': {
            'includes': 'atexit',
            'include_files': (
                ('scripts/mplayer.exe', 'mplayer.exe'),
            )
        }
    },
    executables=[
        Executable('scripts/c10_stat.py', base='Console'),
        Executable('scripts/c10_dump.py', base='Console'),
        Executable('scripts/c10_copy.py', base='Console'),
        Executable('scripts/video.py', base='Win32GUI'),
    ],
    packages=[
        'chapter10',
        'chapter10.datatypes',
    ])

setup(**kwargs)
