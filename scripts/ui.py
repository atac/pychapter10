# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scripts\video.ui'
#
# Created: Mon Mar 17 18:29:41 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(893, 675)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 891, 651))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.grid = QtGui.QGridLayout()
        self.grid.setObjectName(_fromUtf8("grid"))
        self.verticalLayout.addLayout(self.grid)
        self.playback = QtGui.QHBoxLayout()
        self.playback.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.playback.setObjectName(_fromUtf8("playback"))
        self.play_btn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.play_btn.setObjectName(_fromUtf8("play_btn"))
        self.playback.addWidget(self.play_btn)
        self.verticalLayout.addLayout(self.playback)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 893, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuPlayback = QtGui.QMenu(self.menubar)
        self.menuPlayback.setObjectName(_fromUtf8("menuPlayback"))
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionPlay_Pause = QtGui.QAction(MainWindow)
        self.actionPlay_Pause.setObjectName(_fromUtf8("actionPlay_Pause"))
        self.menuFile.addAction(self.actionOpen)
        self.menuPlayback.addAction(self.actionPlay_Pause)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPlayback.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "CH10 Video Player", None))
        self.play_btn.setText(_translate("MainWindow", "Play", None))
        self.play_btn.setShortcut(_translate("MainWindow", "Space", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuPlayback.setTitle(_translate("MainWindow", "Playback", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionPlay_Pause.setText(_translate("MainWindow", "Play / Pause", None))

