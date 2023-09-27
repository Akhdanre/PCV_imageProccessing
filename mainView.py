from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1198, 661)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-1, -1, 1171, 601))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(360, 130, 411, 291))
        self.label.setText("")
        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(1170, 0, 31, 601))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1198, 30))
        self.menubar.setObjectName("menubar")
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.setObjectName("menuOpen")
        self.menuColor = QtWidgets.QMenu(self.menubar)
        self.menuColor.setObjectName("menuColor")
        self.menuGrayscale = QtWidgets.QMenu(self.menuColor)
        self.menuGrayscale.setObjectName("menuGrayscale")
        self.menuAritmatika = QtWidgets.QMenu(self.menubar)
        self.menuAritmatika.setObjectName("menuAritmatika")
        self.menuGeometri = QtWidgets.QMenu(self.menubar)
        self.menuGeometri.setObjectName("menuGeometri")
        self.menuFlip = QtWidgets.QMenu(self.menuGeometri)
        self.menuFlip.setObjectName("menuFlip")
        self.menuHistogram = QtWidgets.QMenu(self.menubar)
        self.menuHistogram.setObjectName("menuHistogram")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(mainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(mainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionQuit = QtWidgets.QAction(mainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionBrightness = QtWidgets.QAction(mainWindow)
        self.actionBrightness.setObjectName("actionBrightness")
        self.actionAverage = QtWidgets.QAction(mainWindow)
        self.actionAverage.setObjectName("actionAverage")
        self.actionLightness = QtWidgets.QAction(mainWindow)
        self.actionLightness.setObjectName("actionLightness")
        self.actionLuminance = QtWidgets.QAction(mainWindow)
        self.actionLuminance.setObjectName("actionLuminance")
        self.actionInvers = QtWidgets.QAction(mainWindow)
        self.actionInvers.setObjectName("actionInvers")
        self.actionCrop = QtWidgets.QAction(mainWindow)
        self.actionCrop.setObjectName("actionCrop")
        self.actionVertical = QtWidgets.QAction(mainWindow)
        self.actionVertical.setObjectName("actionVertical")
        self.actionHorizontal = QtWidgets.QAction(mainWindow)
        self.actionHorizontal.setObjectName("actionHorizontal")
        self.actionHistogram_Equalization = QtWidgets.QAction(mainWindow)
        self.actionHistogram_Equalization.setObjectName("actionHistogram_Equalization")
        self.menuOpen.addAction(self.actionOpen)
        self.menuOpen.addAction(self.actionSave)
        self.menuOpen.addAction(self.actionQuit)
        self.menuGrayscale.addAction(self.actionAverage)
        self.menuGrayscale.addAction(self.actionLightness)
        self.menuGrayscale.addAction(self.actionLuminance)
        self.menuColor.addAction(self.menuGrayscale.menuAction())
        self.menuColor.addAction(self.actionBrightness)
        self.menuColor.addAction(self.actionInvers)
        self.menuFlip.addAction(self.actionVertical)
        self.menuFlip.addAction(self.actionHorizontal)
        self.menuGeometri.addAction(self.menuFlip.menuAction())
        self.menuGeometri.addAction(self.actionCrop)
        self.menuHistogram.addAction(self.actionHistogram_Equalization)
        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuColor.menuAction())
        self.menubar.addAction(self.menuAritmatika.menuAction())
        self.menubar.addAction(self.menuHistogram.menuAction())
        self.menubar.addAction(self.menuGeometri.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.menuOpen.setTitle(_translate("mainWindow", "File"))
        self.menuColor.setTitle(_translate("mainWindow", "Color"))
        self.menuGrayscale.setTitle(_translate("mainWindow", "Grayscale"))
        self.menuAritmatika.setTitle(_translate("mainWindow", "Aritmatika"))
        self.menuGeometri.setTitle(_translate("mainWindow", "Geometri"))
        self.menuFlip.setTitle(_translate("mainWindow", "Flip"))
        self.menuHistogram.setTitle(_translate("mainWindow", "Histogram"))
        self.actionOpen.setText(_translate("mainWindow", "Open"))
        self.actionSave.setText(_translate("mainWindow", "Save"))
        self.actionQuit.setText(_translate("mainWindow", "Quit"))
        self.actionBrightness.setText(_translate("mainWindow", "Brightness"))
        self.actionAverage.setText(_translate("mainWindow", "Average"))
        self.actionLightness.setText(_translate("mainWindow", "Lightness"))
        self.actionLuminance.setText(_translate("mainWindow", "Luminance"))
        self.actionInvers.setText(_translate("mainWindow", "Invers"))
        self.actionCrop.setText(_translate("mainWindow", "Crop"))
        self.actionVertical.setText(_translate("mainWindow", "Vertical"))
        self.actionHorizontal.setText(_translate("mainWindow", "Horizontal"))
        self.actionHistogram_Equalization.setText(_translate("mainWindow", "Histogram Equalization"))
