# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scripts\../ui\video.ui'
#
# Created: Thu Mar 20 11:56:48 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 533)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 511))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grid = QtGui.QGridLayout()
        self.grid.setObjectName("grid")
        self.verticalLayout.addLayout(self.grid)
        self.playback = QtGui.QVBoxLayout()
        self.playback.setObjectName("playback")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.slider = QtGui.QSlider(self.verticalLayoutWidget)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.verticalLayout_2.addWidget(self.slider)
        self.play_btn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.play_btn.setObjectName("play_btn")
        self.verticalLayout_2.addWidget(self.play_btn)
        self.audio = QtGui.QComboBox(self.verticalLayoutWidget)
        self.audio.setObjectName("audio")
        self.verticalLayout_2.addWidget(self.audio)
        self.volume = QtGui.QSlider(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume.sizePolicy().hasHeightForWidth())
        self.volume.setSizePolicy(sizePolicy)
        self.volume.setOrientation(QtCore.Qt.Vertical)
        self.volume.setObjectName("volume")
        self.verticalLayout_2.addWidget(self.volume)
        self.playback.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.playback)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionPlay_Pause = QtGui.QAction(MainWindow)
        self.actionPlay_Pause.setObjectName("actionPlay_Pause")
        self.open_file = QtGui.QAction(MainWindow)
        self.open_file.setObjectName("open_file")
        self.exit = QtGui.QAction(MainWindow)
        self.exit.setObjectName("exit")
        self.menuFile.addAction(self.open_file)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "CH10 Video Player", None, QtGui.QApplication.UnicodeUTF8))
        self.play_btn.setText(QtGui.QApplication.translate("MainWindow", "Play / Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlay_Pause.setText(QtGui.QApplication.translate("MainWindow", "Play / Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.open_file.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.open_file.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.exit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

