
import os
import sys

from PyQt4 import QtGui, QtCore
from mplayer.qt4 import QPlayerView
import mplayer

from ui import Ui_MainWindow


# Tell mplayer.py where mplayer actually is.
mplayer.Player.exec_path = os.path.join(os.path.dirname(__file__),
                                        'mplayer-svn-36986', 'mplayer.exe')

INITIAL_RESOLUTION = (320, 240)
TOOLBAR_OFFSET = 75


class Main(QtGui.QMainWindow, Ui_MainWindow):
    playing = False

    def __init__(self):
        super(Main, self).__init__(None)

        self.setupUi(self)

        # Load videos.
        self.videos = []
        for path in os.listdir('tmp'):
            self.add_video('tmp/%s' % path)
        #self.adjust_size()

        # Connect events.
        self.play_btn.clicked.connect(self.play)

    def resizeEvent(self, e=None):
        """Resize elements to match changing window size."""

        super(Main, self).resizeEvent(e)

        # Extend primary layout to match the window.
        geo = self.geometry()
        height, width = geo.height(), geo.width()
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(0, 0, width, height))

        # Resize the video layout to fill all but the toolbar.
        geo = self.grid.geometry()
        height, width = geo.height(), geo.width()
        height -= TOOLBAR_OFFSET
        self.grid.setGeometry(QtCore.QRect(0, 0, width, height))

        # Resize and reposition the toolbar.
        geo = self.playback.geometry()
        self.playback.setGeometry(
            QtCore.QRect(0, height, geo.width(), TOOLBAR_OFFSET))

    def add_video(self, path):
        """Add a video widget for a file."""

        vid = QPlayerView(self.verticalLayoutWidget, ('-nosound',))
        vid.player.introspect()
        vid.player.loadfile(path)
        x, y = 0, self.grid.rowCount() - 1
        if y < 0:
            y = 0
        while self.grid.itemAtPosition(x, y) is not None:
            if x == 3:
                x = 0
                y += 1
                break
            x += 1
        self.grid.addWidget(vid, x, y)
        self.videos.append(vid)

    def play(self):
        """Play or pause all videos."""

        if self.playing:
            self.play_btn.setText('Play')
            self.playing = False
        else:
            self.play_btn.setText('Pause')
            self.playing = True
        for vid in main.videos:
            vid.player.pause()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    main = Main()
    main.show()
    sys.exit(app.exec_())
