
from tempfile import mkdtemp
import atexit
import os
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
mplayer.Player.exec_path = os.path.join(basedir, 'mplayer.exe')
mplayer.Player.introspect()

TOOLBAR_OFFSET = 75


class Main(QtGui.QMainWindow, Ui_MainWindow):
    playing = False
    audio_from = 0

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
            progress = QtGui.QProgressDialog('Loading %s...' % filename,
                                             'Cancel', 0, 100, self)
            progress.setWindowTitle('Loading...')
            progress.show()

            tmp = mkdtemp()
            out = {}
            for packet in C10(str(filename)):
                if datatypes.format(packet.data_type)[0] != 8:
                    continue

                path = os.path.join(tmp, str(packet.channel_id)) + '.mpg'
                if path not in out:
                    out[path] = open(path, 'wb')
                    atexit.register(out[path].close)

                out[path].write(''.join([p.data for p in packet.body.mpeg]))

            progress.close()

            self.videos = []
            for path in os.listdir(tmp):
                self.add_video(os.path.join(tmp, path))
                self.audio.addItem(os.path.basename(path))

        elif action == 'Exit':
            self.app.closeAllWindows()

    def adjust_volume(self, to):
        self.videos[self.audio_from].volume = float(to or 0)

    def audio_source(self, index):
        if not self.videos:
            return
        self.videos[self.audio_from].volume = 0.0
        self.videos[index].volume = float(self.volume.value())
        self.audio_from = index

    def seek(self, to):
        for vid in self.videos:
            vid.seek(to, 1)

    def tick(self):
        if not self.videos:
            return
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


class Ticker(QtCore.QThread):
    """Use a seperate thread to trigger a mainloop function."""

    tick = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.tick.emit()
            time.sleep(3)

if __name__ == '__main__':
    main = Main(QtGui.QApplication([]))
    main.run()
