
import os
import sys
import time

from PyQt4 import QtGui, QtCore
from mplayer.qt4 import QPlayerView
import mplayer

from ui import Ui_MainWindow


# Tell mplayer.py where mplayer actually is.
mplayer.Player.exec_path = os.path.join(os.path.dirname(__file__),
                                        'mplayer-svn-36986', 'mplayer.exe')
mplayer.Player.introspect()

INITIAL_RESOLUTION = (320, 240)
TOOLBAR_OFFSET = 75


class Main(QtGui.QMainWindow, Ui_MainWindow):
    playing = False
    audio_from = 0

    def __init__(self):
        super(Main, self).__init__(None)

        self.setupUi(self)

        self.ticker = Ticker()
        self.ticker.start()

        # Load videos.
        self.videos = []
        for path in os.listdir('tmp'):
            self.add_video('tmp/%s' % path)
            self.audio.addItem(os.path.basename(path))

        # Connect events.
        self.play_btn.clicked.connect(self.play)
        self.ticker.tick.connect(self.tick)
        self.audio.currentIndexChanged.connect(self.audio_source)
        self.slider.sliderMoved.connect(self.seek)
        self.volume.sliderMoved.connect(self.adjust_volume)

        self.volume.setValue(40.0)
        self.audio_source(0)

    def adjust_volume(self, to):
        self.videos[self.audio_from].volume = float(to)

    def audio_source(self, index):
        self.videos[self.audio_from].volume = 0.0
        self.videos[index].volume = float(self.volume.value())
        self.audio_from = index

    def seek(self, to):
        for vid in self.videos:
            vid.seek(to, 1)

    def tick(self):
        self.slider.setValue(self.videos[0].percent_pos or 0)
        self.volume.setValue(int(self.videos[self.audio_from].volume))

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
                                      '-fs', '-wid', int(vid.winId())))
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


class Ticker(QtCore.QThread):
    """Use a seperate thread to trigger a mainloop function."""

    tick = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.tick.emit()
            time.sleep(3)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    main = Main()
    main.show()
    sys.exit(app.exec_())
