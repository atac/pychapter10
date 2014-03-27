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
    subprocess.Popen = partial(subprocess.Popen, shell=True)

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
        self.length = 0
        self.start_offset = 0

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
        self.destroyed.connect(self.closeEvent)

        self.volume.setValue(40.0)
        self.audio_source(0)

    def menu_action(self, action):
        action = action.text()
        if action == 'Open':
            self.load_file()

        elif action == 'Exit':
            self.closeEvent()

    def closeEvent(self, event=None):
        self.ticker.running = False
        self.ticker.wait()
        if self.loader:
            self.loader.quit()
            self.loader.wait()
        self.app.closeAllWindows()
        QtGui.QMainWindow.closeEvent(self, event)

    def load_file(self, filename=None):
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(
                self, 'Load Chapter 10 File', os.curdir,
                'Chapter 10 Files (*.c10 *.ch10);;All Files (*.*)')
            filename = str(filename[0])

        self.loader = FileLoader(self, filename)
        self.loader.done.connect(self.finished_loading)
        self.loader.start()

        time.sleep(0.25)
        self.show_videos(self.loader.tmp)

    def show_videos(self, tmp):
        tmp = str(tmp)
        for vid in self.videos:
            self.grid.removeWidget(vid)
            vid.player.quit()
            vid.destroy()
            del vid
        self.videos = []
        self.audio.clear()
        for path in os.listdir(tmp):
            self.add_video(os.path.join(tmp, path))
            self.audio.addItem(os.path.basename(path))

        self.show()

        time.sleep(0.25)
        self.start_offset = (self.videos[0].player.time_pos or 0)

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

        t = (to / 100.0) * max(self.length - self.start_offset, 1)
        pos = (self.videos[0].player.time_pos or 0) - self.start_offset
        if pos > t:
            offset = -(pos - t)
        else:
            offset = t - pos
        for vid in self.videos:
            vid.player.seek(int(offset))

    def tick(self):
        """Called once a second."""

        # Update progress if loading a file.
        if self.loader and not self.loader.finished:
            percent = (float(self.loader.pos) / self.loader.size) * 100
            self.load_meter.setValue(percent)
            self.load_label.setText('Read %s / %s mb'
                                    % (self.loader.pos / 1024 / 1024,
                                       self.loader.size / 1024 / 1024))

        else:
            percent = 100
            self.load_label.setText('Done')

        self.load_meter.setValue(percent)

        # Update seek and play/pause button.
        if self.videos:
            self.play_btn.setText(
                'Play' if self.videos[0].player.paused else 'Pause')

            if self.loader.finished:
                pos = self.videos[0].player.time_pos
                if pos is not None:
                    pos -= self.start_offset
                    length = max(self.length - self.start_offset, 1)
                    percent = pos / length * 100

                    self.slider.setMaximum(100)
                    self.slider.setValue(percent)

    def finished_loading(self):
        tmp = mplayer.Player((
            '-vo', 'null', '-ao', 'null',
            self.videos[0].player.path))
        tmp.loadfile(self.videos[0].player.path)
        tmp.seek(99, 1)
        self.length = tmp.time_pos
        tmp.quit()
        self.slider.setEnabled(True)

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

        vid = VideoWidget(self.verticalLayoutWidget, ('-volume', '0', '-quiet',
                                                      '-really-quiet'))
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

    done = QtCore.Signal()

    def __init__(self, parent, filename):
        super(FileLoader, self).__init__()
        self.finished = True
        self.parent, self.filename = parent, filename
        self.size, self.pos = os.stat(filename).st_size, 0

    def run(self):
        self.finished = False
        self.tmp = mkdtemp()
        out = {}
        try:
            for packet in C10(self.filename):

                # Cancel if requested.
                if self.finished:
                    break

                # Ignore non-video.
                if datatypes.format(packet.data_type)[0] != 8:
                    continue

                # Ensure a target path exists.
                path = os.path.join(self.tmp, str(packet.channel_id)) + '.mpg'
                if path not in out:
                    out[path] = open(path, 'wb')

                for ts in packet.body.mpeg:
                    out[path].write(ts.data)
                self.pos = packet.pos
        except ValueError:
            pass

        for f in out.values():
            if not f.closed:
                f.close()

        self.quit()

    def quit(self):
        self.finished = True
        self.done.emit()
        QtCore.QThread.quit(self)


class Ticker(QtCore.QThread):
    """Emits a 'tick' signal once a second."""

    tick = QtCore.Signal()
    running = True

    def run(self):
        while self.running:
            try:
                self.tick.emit()
            except RuntimeError:
                break
            time.sleep(0.5)
        self.quit()

if __name__ == '__main__':
    main = Main(QtGui.QApplication([]))
    main.run()
