
import os
import sys

from PyQt4 import QtGui, QtCore
from mplayer.qt4 import QPlayerView
import mplayer

from ui import Ui_MainWindow


# Tell mplayer.py where mplayer actually is.
mplayer.Player.exec_path = os.path.join(os.path.dirname(__file__),
                                        'mplayer-svn-36986', 'mplayer.exe')

SCREEN_SIZE = (640, 480)


class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main, self).__init__(None)

        self.setupUi(self)

        self.setWindowTitle('CH10 Video Player')

        #self.grid = QtGui.QGridLayout(self.top)

        self.videos = []
        for path in os.listdir('tmp'):
            self.add_video('tmp/%s' % path)

        if len(self.videos) > 3:
            width = SCREEN_SIZE[0] * 3
            height = SCREEN_SIZE[1] * (len(self.videos) / 3)
        else:
            height = SCREEN_SIZE[1]
            width = SCREEN_SIZE[0] * len(self.videos)
        self.resize(width, height)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, width, height))

    def add_video(self, path):
        v = QPlayerView(self.gridLayoutWidget, ('-nosound',))
        #v.eof.connect(self.closeAllWindows)
        v.resize(*SCREEN_SIZE)
        v.player.introspect()
        v.player.loadfile(path)
        x, y = 0, self.grid.rowCount() - 1
        if y < 0:
            y = 0
        while self.grid.itemAtPosition(x, y) is not None:
            if x == 3:
                x = 0
                y += 1
                break
            x += 1
        self.grid.addWidget(v, x, y)
        self.videos.append(v)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    main = Main()
    main.show()
    for v in main.videos:
        v.player.pause()
    sys.exit(app.exec_())
