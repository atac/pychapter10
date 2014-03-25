#!/usr/bin/env python

from functools import partial
from tempfile import mkdtemp
import ctypes
import os
import subprocess
import sys
import time

from PySide import QtGui, QtCore
from mplayer_pyside import qt4
import mplayer_pyside as mplayer

from chapter10 import C10, datatypes
from ui.video import Ui_MainWindow

# Tell mplayer.py where mplayer actually is.
try:
    basedir = os.path.dirname(__file__)
except NameError:
    basedir = os.path.dirname(sys.executable)

try:
    subprocess.Popen(mplayer.Player.exec_path).wait()
except OSError:
    mplayer.Player.exec_path = os.path.join(basedir, 'mplayer.exe')

# Force subprocess.Popen to use shell=True on windows.
if sys.platform == 'win32':
    subprocess.Popen = partial(subprocess.Popen, shell=True, stdout=None)

mplayer.Player.introspect()

TOOLBAR_OFFSET = 200


# Force QtPlayer to use inherited constructor.
qt4.QtPlayer.__init__ = mplayer.Player.__init__


class VideoWidget(qt4.QPlayerView):
    def winId(self):
        """Generate an actual int for the player."""

        id = qt4.QPlayerView.winId(self)
        try:
            id = int(id)
        except TypeError:
            ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
            id = ctypes.pythonapi.PyCObject_AsVoidPtr(id)
        return id


class Main(QtGui.QMainWindow, Ui_MainWindow):
    audio_from = 0
    loader = None

    def __init__(self, app):
        super(Main, self).__init__(None)

        self.app = app

        self.setupUi(self)

        self.ticker = Ticker()
        self.ticker.start()

        self.videos = []
        self.slider.setEnabled(False)

        # Connect events.
        self.play_btn.clicked.connect(self.play)
        self.ticker.tick.connect(self.tick)
        self.audio.currentIndexChanged.connect(self.audio_source)
        self.slider.sliderMoved.connect(self.seek)
        self.volume.sliderMoved.connect(self.adjust_volume)
        self.menubar.triggered.connect(self.menu_action)
        self.destroyed.connect(self.quit)

        self.volume.setValue(40.0)
        self.audio_source(0)

    def menu_action(self, action):
        action = action.text()
        if action == 'Open':
            self.load_file()

        elif action == 'Exit':
            self.quit()

    def quit(self):
        if self.loader and not self.loader.finished:
            self.loader.cancel = True
            self.ticker.running = False
            self.loader.wait()
            self.ticker.wait()
        self.app.closeAllWindows()

    def load_file(self, filename=None):
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(
                self, 'Load Chapter 10 File', os.curdir,
                'Chapter 10 Files (*.c10 *.ch10);;All Files (*.*)')
            filename = str(filename[0])

        self.loader = FileLoader(self, filename)
        self.loader.start()

        time.sleep(1)
        self.show_videos(self.loader.tmp)

    def show_videos(self, tmp):
        tmp = str(tmp)
        for vid in self.videos:
            self.grid.removeWidget(vid)
        self.videos = []
        self.audio.clear()
        for path in os.listdir(tmp):
            self.add_video(os.path.join(tmp, path))
            self.audio.addItem(os.path.basename(path))

        self.show()

    def adjust_volume(self, to):
        self.videos[self.audio_from].player.volume = float(to or 0)

    def audio_source(self, index):
        if not self.videos:
            return
        if self.audio_from:
            self.videos[self.audio_from].player.volume = 0.0
        self.videos[index].player.volume = float(self.volume.value())
        self.audio_from = index

    def seek(self, to):
        """Jump to an absolute index in all videos."""

        for vid in self.videos:
            vid.player.seek(to, 1)

    def tick(self):
        """Called once a second."""

        # Update progress if loading a file.
        if self.loader and not self.loader.finished:
            try:
                self.load_meter.setMaximum(self.loader.size)
                self.load_meter.setValue(self.loader.pos)
            except OverflowError:
                self.load_meter.setMaximum(100)
                self.load_meter.setValue(
                    (float(self.loader.pos) / self.loader.size) * 100)
            self.load_label.setText('Read %s / %s mb'
                                    % (self.loader.pos / 1024 / 1024,
                                       self.loader.size / 1024 / 1024))

        else:
            self.load_label.setText('Done')
            self.load_meter.setValue(100)

        # Update seek and volume.
        if self.videos:
            self.play_btn.setText(
                'Play' if self.videos[0].player.paused else 'Pause')
            self.slider.setValue(self.videos[0].player.percent_pos or 0)

    def resizeEvent(self, e=None):
        """Resize elements to match changing window size."""

        super(Main, self).resizeEvent(e)

        # Extend primary layout to match the window.
        geo = self.geometry()
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(0, 0, geo.width(), geo.height() - TOOLBAR_OFFSET))

        self.playback.move(0, geo.height() - TOOLBAR_OFFSET)

    def add_video(self, path):
        """Add a video widget for a file."""

        vid = VideoWidget(self.verticalLayoutWidget, ('-volume', '0'))
        vid.player.loadfile(path)
        x, y = 0, self.grid.rowCount() - 1
        if y < 0:
            y = 0
        while self.grid.itemAtPosition(y, x) is not None:
            if x == 2:
                x = 0
                y += 1
                continue
            x += 1
        self.grid.addWidget(vid, y, x)
        self.videos.append(vid)

    def play(self):
        """Play or pause all videos."""

        for vid in main.videos:
            vid.player.pause()

    def run(self):
        if len(sys.argv) > 1:
            self.load_file(sys.argv[1])
        else:
            self.load_file()
        sys.exit(self.app.exec_())


class FileLoader(QtCore.QThread):
    """Parse video from a chapter 10 file into a temporary directory."""

    def __init__(self, parent, filename):
        super(FileLoader, self).__init__()
        self.finished = True
        self.parent, self.filename = parent, filename
        self.size, self.pos = os.stat(filename).st_size, 0
        self.cancel = False

    def run(self):
        self.finished = False
        self.tmp = mkdtemp()
        out = {}
        for packet in C10(self.filename):

            # Cancel if requested.
            if self.cancel:
                self.quit()
                return

            # Ignore non-video.
            if datatypes.format(packet.data_type)[0] != 8:
                continue

            # Ensure a target path exists.
            path = os.path.join(self.tmp, str(packet.channel_id)) + '.mpg'
            if path not in out:
                out[path] = open(path, 'wb')

            out[path].write(''.join([p.data for p in packet.body.mpeg]))
            self.pos = packet.pos

        for f in out.values():
            try:
                f.close()
            except:
                pass

        self.quit()

    def quit(self):
        self.finished = True
        QtCore.QThread.quit(self)


class Ticker(QtCore.QThread):
    """Emits a 'tick' signal once a second."""

    tick = QtCore.Signal()
    running = True

    def run(self):
        while self.running:
            self.tick.emit()
            time.sleep(1)
        self.quit()

if __name__ == '__main__':
    main = Main(QtGui.QApplication([]))
    main.run()
