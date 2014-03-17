
import os
import sys

from PyQt4 import QtGui
from mplayer.qt4 import QPlayerView
import mplayer


# Tell mplayer.py where mplayer actually is.
mplayer.Player.exec_path = os.path.join(os.path.dirname(__file__),
                                        'mplayer-svn-36986', 'mplayer.exe')

SCREEN_SIZE = (640, 480)


class App(QtGui.QApplication):
    def __init__(self):
        super(App, self).__init__([])

        self.window = QtGui.QDialog()
        self.window.setWindowTitle('CH10 Video Player')

        self.layout = QtGui.QGridLayout()
        self.window.setLayout(self.layout)

        self.videos = []
        for path in os.listdir('tmp'):
            self.add_video('tmp/%s' % path)

        if len(self.videos) > 3:
            width = SCREEN_SIZE[0] * 3
            height = SCREEN_SIZE[1] * (len(self.videos) / 3)
        else:
            height = SCREEN_SIZE[1]
            width = SCREEN_SIZE[0] * len(self.videos)
        self.window.resize(width, height)

    def add_video(self, path):
        v = QPlayerView(self.window, ('-nosound',))
        v.eof.connect(self.closeAllWindows)
        v.resize(*SCREEN_SIZE)
        v.player.introspect()
        v.player.loadfile(path)
        x, y = 0, self.layout.rowCount() - 1
        if y < 0:
            y = 0
        while self.layout.itemAtPosition(x, y) is not None:
            if x == 3:
                x = 0
                y += 1
                break
            x += 1
        self.layout.addWidget(v, x, y)
        self.videos.append(v)

    def main(self):
        self.window.show()
        for v in self.videos:
            v.player.pause()
        sys.exit(self.exec_())

if __name__ == '__main__':
    App().main()
