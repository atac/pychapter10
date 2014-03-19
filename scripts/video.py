
from functools import partial
from tempfile import mkdtemp
import os
import subprocess
import sys
import time

from PyQt4 import QtGui, QtCore
from mplayer.qt4 import QPlayerView
import mplayer

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

TOOLBAR_OFFSET = 75


class Main(QtGui.QMainWindow, Ui_MainWindow):
    playing = False
    audio_from = 0
    progress = None

    def __init__(self, app):
        super(Main, self).__init__(None)

        self.app = app

        self.setupUi(self)

        self.ticker = Ticker()
        self.ticker.start()

        self.videos = []

        # Connect events.
        self.play_btn.clicked.connect(self.play)
        self.ticker.tick.connect(self.tick)
        self.audio.currentIndexChanged.connect(self.audio_source)
        self.slider.sliderMoved.connect(self.seek)
        self.volume.sliderMoved.connect(self.adjust_volume)
        self.menubar.triggered.connect(self.menu_action)

        self.volume.setValue(40.0)
        self.audio_source(0)

    def menu_action(self, action):
        action = action.text()
        if action == 'Open':
            filename = QtGui.QFileDialog.getOpenFileName(
                self, 'Load Chapter 10 File', os.curdir,
                'Chapter 10 Files (*.c10 *.ch10);;All Files (*.*)')

            self.loader = FileLoader(self, str(filename))
            self.loader.done.connect(self.show_videos)
            self.loader.start()

            self.progress = QtGui.QProgressDialog('Loading...', 'Cancel',
                                                  0, 100, self)
            self.progress.setWindowTitle('Loading %s...' % filename)
            self.progress.setModal(True)
            self.progress.canceled.connect(self.cancel_load)
            self.progress.show()

        elif action == 'Exit':
            self.app.closeAllWindows()

    def cancel_load(self):
        self.progress.close()
        self.progress = None
        self.loader.cancel = True

    def show_videos(self, tmp):
        tmp = str(tmp)
        self.videos = []
        for path in os.listdir(tmp):
            self.add_video(os.path.join(tmp, path))
            self.audio.addItem(os.path.basename(path))

        self.progress.close()

    def adjust_volume(self, to):
        self.videos[self.audio_from].volume = float(to or 0)

    def audio_source(self, index):
        if not self.videos:
            return
        self.videos[self.audio_from].volume = 0.0
        self.videos[index].volume = float(self.volume.value())
        self.audio_from = index

    def seek(self, to):
        """Jump to an absolute index in all videos."""

        for vid in self.videos:
            vid.seek(to, 1)

    def tick(self):
        """Called once a second."""

        # Update progress dialog if loading a file.
        if self.progress and self.progress.isEnabled():
            self.progress.setMaximum(self.loader.size)
            self.progress.setValue(self.loader.pos)
            self.progress.setLabelText('Read %s / %s mb'
                                       % (self.loader.pos / 1024,
                                          self.loader.size / 1024))

        # Update seek and volume.
        if self.videos:
            self.slider.setValue(self.videos[0].percent_pos or 0)
            self.volume.setValue(int(self.videos[self.audio_from].volume or 0))

    def resizeEvent(self, e=None):
        """Resize elements to match changing window size."""

        super(Main, self).resizeEvent(e)

        # Extend primary layout to match the window.
        geo = self.geometry()
        height, width = geo.height(), geo.width()
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(0, 0, width, height - TOOLBAR_OFFSET))

    def add_video(self, path):
        """Add a video widget for a file."""

        vid = QPlayerView(self.verticalLayoutWidget)
        vid._player = mplayer.Player(('-msglevel', 'global=6', '-fixed-vo',
                                      '-really-quiet', '-fs', '-wid',
                                      int(vid.winId())))
        vid.player.loadfile(path)
        vid.player.volume = 0
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
        self.videos.append(vid.player)

    def play(self):
        """Play or pause all videos."""

        if self.playing:
            self.play_btn.setText('Play')
            self.playing = False
        else:
            self.play_btn.setText('Pause')
            self.playing = True
        for vid in main.videos:
            vid.pause()

    def run(self):
        self.show()
        sys.exit(self.app.exec_())


class FileLoader(QtCore.QThread):
    """Parse video from a chapter 10 file into a temporary directory."""

    done = QtCore.pyqtSignal(str)

    def __init__(self, parent, filename):
        super(FileLoader, self).__init__()
        self.parent, self.filename = parent, filename
        self.size, self.pos = os.stat(filename).st_size, 0
        self.cancel = False

    def run(self):
        tmp = mkdtemp()
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
            path = os.path.join(tmp, str(packet.channel_id)) + '.mpg'
            if path not in out:
                out[path] = open(path, 'wb')

            out[path].write(''.join([p.data for p in packet.body.mpeg]))
            self.pos = packet.pos

        for f in out.values():
            f.close()

        self.done.emit(tmp)
        self.quit()


class Ticker(QtCore.QThread):
    """Emits a 'tick' signal once a second."""

    tick = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.tick.emit()
            time.sleep(1)

if __name__ == '__main__':
    main = Main(QtGui.QApplication([]))
    main.run()
