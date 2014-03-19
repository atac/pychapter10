# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scripts\../ui\video.ui'
#
# Created: Tue Mar 18 19:13:43 2014
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
        MainWindow.resize(893, 682)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 891, 661))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.grid = QtGui.QGridLayout()
        self.grid.setObjectName(_fromUtf8("grid"))
        self.verticalLayout.addLayout(self.grid)
        self.playback = QtGui.QVBoxLayout()
        self.playback.setObjectName(_fromUtf8("playback"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.slider = QtGui.QSlider(self.verticalLayoutWidget)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName(_fromUtf8("slider"))
        self.verticalLayout_2.addWidget(self.slider)
        self.play_btn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.play_btn.setObjectName(_fromUtf8("play_btn"))
        self.verticalLayout_2.addWidget(self.play_btn)
        self.audio = QtGui.QComboBox(self.verticalLayoutWidget)
        self.audio.setObjectName(_fromUtf8("audio"))
        self.verticalLayout_2.addWidget(self.audio)
        self.volume = QtGui.QSlider(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume.sizePolicy().hasHeightForWidth())
        self.volume.setSizePolicy(sizePolicy)
        self.volume.setOrientation(QtCore.Qt.Vertical)
        self.volume.setObjectName(_fromUtf8("volume"))
        self.verticalLayout_2.addWidget(self.volume)
        self.playback.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.playback)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 893, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionPlay_Pause = QtGui.QAction(MainWindow)
        self.actionPlay_Pause.setObjectName(_fromUtf8("actionPlay_Pause"))
        self.open_file = QtGui.QAction(MainWindow)
        self.open_file.setObjectName(_fromUtf8("open_file"))
        self.exit = QtGui.QAction(MainWindow)
        self.exit.setObjectName(_fromUtf8("exit"))
        self.menuFile.addAction(self.open_file)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "CH10 Video Player", None))
        self.play_btn.setText(_translate("MainWindow", "Play", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionPlay_Pause.setText(_translate("MainWindow", "Play / Pause", None))
        self.open_file.setText(_translate("MainWindow", "Open", None))
        self.open_file.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.exit.setText(_translate("MainWindow", "Exit", None))

