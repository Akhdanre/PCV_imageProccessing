from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, qRgb
from PIL import Image, ImageQt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(994, 395)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 311, 311))
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setText("")
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(340, 30, 311, 311))
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setText("")
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(660, 30, 311, 311))
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setText("")
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 994, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAND = QtWidgets.QMenu(self.menubar)
        self.menuAND.setObjectName("menuAND")
        self.menuOperasi = QtWidgets.QMenu(self.menubar)
        self.menuOperasi.setObjectName("menuOperasi")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_Image_1 = QtWidgets.QAction(MainWindow)
        self.actionOpen_Image_1.setObjectName("actionOpen_Image_1")
        self.actionOpen_Image_2 = QtWidgets.QAction(MainWindow)
        self.actionOpen_Image_2.setObjectName("actionOpen_Image_2")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAND = QtWidgets.QAction(MainWindow)
        self.actionAND.setObjectName("actionAND")
        self.actionOR = QtWidgets.QAction(MainWindow)
        self.actionOR.setObjectName("actionOR")
        self.actionNOT = QtWidgets.QAction(MainWindow)
        self.actionNOT.setObjectName("actionNOT")
        self.actionPenjumlahan = QtWidgets.QAction(MainWindow)
        self.actionPenjumlahan.setObjectName("actionPenjumlahan")
        self.actionPengurangan = QtWidgets.QAction(MainWindow)
        self.actionPengurangan.setObjectName("actionPengurangan")
        self.actionPerkalian = QtWidgets.QAction(MainWindow)
        self.actionPerkalian.setObjectName("actionPerkalian")
        self.actionPenjumlahan_Skalar_3 = QtWidgets.QAction(MainWindow)
        self.actionPenjumlahan_Skalar_3.setObjectName("actionPenjumlahan_Skalar_3")
        self.actionPengurangan_Skalar_3 = QtWidgets.QAction(MainWindow)
        self.actionPengurangan_Skalar_3.setObjectName("actionPengurangan_Skalar_3")
        self.actionPerkalian_Skalar_C = QtWidgets.QAction(MainWindow)
        self.actionPerkalian_Skalar_C.setObjectName("actionPerkalian_Skalar_C")
        self.actionPembagian_Skalar_C = QtWidgets.QAction(MainWindow)
        self.actionPembagian_Skalar_C.setObjectName("actionPembagian_Skalar_C")
        self.menuFile.addAction(self.actionOpen_Image_1)
        self.menuFile.addAction(self.actionOpen_Image_2)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionExit)
        self.menuAND.addAction(self.actionAND)
        self.menuAND.addAction(self.actionOR)
        self.menuAND.addAction(self.actionNOT)
        self.menuOperasi.addAction(self.actionPenjumlahan)
        self.menuOperasi.addAction(self.actionPengurangan)
        self.menuOperasi.addAction(self.actionPerkalian)
        self.menuOperasi.addAction(self.actionPenjumlahan_Skalar_3)
        self.menuOperasi.addAction(self.actionPengurangan_Skalar_3)
        self.menuOperasi.addAction(self.actionPerkalian_Skalar_C)
        self.menuOperasi.addAction(self.actionPembagian_Skalar_C)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAND.menuAction())
        self.menubar.addAction(self.menuOperasi.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Operasi Aritmatika"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAND.setTitle(_translate("MainWindow", "Logika"))
        self.menuOperasi.setTitle(_translate("MainWindow", "Operasi"))
        self.actionOpen_Image_1.setText(_translate("MainWindow", "Open Image 1"))
        self.actionOpen_Image_2.setText(_translate("MainWindow", "Open Image 2"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAND.setText(_translate("MainWindow", "AND"))
        self.actionOR.setText(_translate("MainWindow", "OR"))
        self.actionNOT.setText(_translate("MainWindow", "NOT"))
        self.actionPenjumlahan.setText(_translate("MainWindow", "Penjumlahan"))
        self.actionPengurangan.setText(_translate("MainWindow", "Pengurangan"))
        self.actionPerkalian.setText(_translate("MainWindow", "Perkalian"))
        self.actionPenjumlahan_Skalar_3.setText(_translate("MainWindow", "Penjumlahan Skalar C"))
        self.actionPengurangan_Skalar_3.setText(_translate("MainWindow", "Pengurangan Skalar C"))
        self.actionPerkalian_Skalar_C.setText(_translate("MainWindow", "Perkalian Skalar C"))
        self.actionPembagian_Skalar_C.setText(_translate("MainWindow", "Pembagian Skalar C"))

        self.actionOpen_Image_1.triggered.connect(self.openFile1)
        self.actionOpen_Image_2.triggered.connect(self.openFile2)
        self.actionSave_As.triggered.connect(self.saveFileAs)
        self.actionExit.triggered.connect(QtWidgets.qApp.quit)

        self.actionAND.triggered.connect(self.LogikaAND)
        self.actionOR.triggered.connect(self.LogikaOR)
        self.actionNOT.triggered.connect(self.LogikaNOT)
        self.actionPenjumlahan.triggered.connect(self.OperasiPenjumlahan)
        self.actionPengurangan.triggered.connect(self.OperasiPengurangan1)
        self.actionPerkalian.triggered.connect(self.OperasiPerkalian)

        self.actionPenjumlahan_Skalar_3.triggered.connect(self.Penjumlahan_Skalar_3)
        self.actionPengurangan_Skalar_3.triggered.connect(self.Pengurangan_Skalar_3)
        self.actionPerkalian_Skalar_C.triggered.connect(self.Perkalian_Skalar_C)
        self.actionPembagian_Skalar_C.triggered.connect(self.Pembagian_Skalar_C)

    def openFile1(self):
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Image File", "", "Image Files (*.png *.jpg *.bmp *.gif);;All Files (*)", options=options)
        if filePath:
            pixmap = QtGui.QPixmap(filePath)
            pixmap = pixmap.scaled(self.label_3.size(), QtCore.Qt.KeepAspectRatio)
            self.label_3.setPixmap(pixmap)
            self.label_3.setAlignment(QtCore.Qt.AlignCenter)
            self.label_3.setPixmap(pixmap)
            self.label_3.setAlignment(QtCore.Qt.AlignCenter)
            self.pathh = filePath

    def openFile2(self):
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Image File", "", "Image Files (*.png *.jpg *.bmp *.gif);;All Files (*)", options=options)
        if filePath:
            pixmap = QtGui.QPixmap(filePath)
            pixmap = pixmap.scaled(self.label_4.size(), QtCore.Qt.KeepAspectRatio)
            self.label_4.setPixmap(pixmap)
            self.label_4.setAlignment(QtCore.Qt.AlignCenter)
            self.label_4.setPixmap(pixmap)
            self.label_4.setAlignment(QtCore.Qt.AlignCenter)
            self.pathh = filePath


    def saveFileAs(self):
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Image As", "", "Image Files (*.png *.jpg *.bmp *.gif);;All Files (*)", options=options)
        if filePath:
            pixmap = self.label_5.pixmap()
            if pixmap:
                pixmap.save(filePath)

    def LogikaAND(self):
        pixmap_3 = self.label_3.pixmap()
        pixmap_4 = self.label_4.pixmap()
        if pixmap_3 and pixmap_4:
            img_3 = pixmap_3.toImage()
            img_4 = pixmap_4.toImage()

            width = min(img_3.width(), img_4.width())
            height = min(img_3.height(), img_4.height())

            result_img = QImage(width, height, QImage.Format_RGB32)

            for x in range(width):
                for y in range(height):
                    pixel_3 = img_3.pixel(x, y)
                    pixel_4 = img_4.pixel(x, y)

                    r_3, g_3, b_3 = QtGui.qRed(pixel_3), QtGui.qGreen(pixel_3), QtGui.qBlue(pixel_3)
                    r_4, g_4, b_4 = QtGui.qRed(pixel_4), QtGui.qGreen(pixel_4), QtGui.qBlue(pixel_4)

                    # Operasi AND pada komponen warna
                    r_result = r_3 & r_4
                    g_result = g_3 & g_4
                    b_result = b_3 & b_4

                    result_img.setPixel(x, y, qRgb(r_result, g_result, b_result))

            result_pixmap = QPixmap.fromImage(result_img)
            self.label_5.setPixmap(result_pixmap)

    def LogikaOR(self):
        pixmap_3 = self.label_3.pixmap()
        pixmap_4 = self.label_4.pixmap()
        if pixmap_3 and pixmap_4:
            img_3 = pixmap_3.toImage()
            img_4 = pixmap_4.toImage()

            width = min(img_3.width(), img_4.width())
            height = min(img_3.height(), img_4.height())

            result_img = QImage(width, height, QImage.Format_RGB32)

            for x in range(width):
                for y in range(height):
                    pixel_3 = img_3.pixel(x, y)
                    pixel_4 = img_4.pixel(x, y)

                    r_3, g_3, b_3 = QtGui.qRed(pixel_3), QtGui.qGreen(pixel_3), QtGui.qBlue(pixel_3)
                    r_4, g_4, b_4 = QtGui.qRed(pixel_4), QtGui.qGreen(pixel_4), QtGui.qBlue(pixel_4)

                    # Operasi OR pada komponen warna
                    r_result = r_3 | r_4
                    g_result = g_3 | g_4
                    b_result = b_3 | b_4

                    result_img.setPixel(x, y, QtGui.qRgb(r_result, g_result, b_result))

            result_pixmap = QPixmap.fromImage(result_img)
            self.label_5.setPixmap(result_pixmap)

    def LogikaNOT(self):
            pixmap_3 = self.label_3.pixmap()
            if pixmap_3:
                img_3 = pixmap_3.toImage()

                width = img_3.width()
                height = img_3.height()

                result_img = QImage(width, height, QImage.Format_RGB32)

                for x in range(width):
                    for y in range(height):
                        pixel_3 = img_3.pixel(x, y)

                        r_3, g_3, b_3 = QtGui.qRed(pixel_3), QtGui.qGreen(pixel_3), QtGui.qBlue(pixel_3)

                        # Operasi NOT pada komponen warna
                        r_result = 255 - r_3
                        g_result = 255 - g_3
                        b_result = 255 - b_3

                        result_img.setPixel(x, y, QtGui.qRgb(r_result, g_result, b_result))

                result_pixmap = QPixmap.fromImage(result_img)
                self.label_5.setPixmap(result_pixmap)

    def OperasiPenjumlahan(self):
            pixmap_3 = self.label_3.pixmap()
            pixmap_4 = self.label_4.pixmap()

            if pixmap_3 and pixmap_4:
                img_3 = pixmap_3.toImage()
                img_4 = pixmap_4.toImage()

                width = img_3.width()
                height = img_3.height()

                result_img = QImage(width, height, QImage.Format_RGB32)

                for x in range(width):
                    for y in range(height):
                        pixel_3 = img_3.pixel(x, y)
                        pixel_4 = img_4.pixel(x, y)

                        r_3, g_3, b_3 = QtGui.qRed(pixel_3), QtGui.qGreen(pixel_3), QtGui.qBlue(pixel_3)
                        r_4, g_4, b_4 = QtGui.qRed(pixel_4), QtGui.qGreen(pixel_4), QtGui.qBlue(pixel_4)

                       #rumus
                        r_result = min(r_3 + r_4, 255)
                        g_result = min(g_3 + g_4, 255)
                        b_result = min(b_3 + b_4, 255)

                        result_img.setPixel(x, y, QtGui.qRgb(r_result, g_result, b_result))

                result_pixmap = QPixmap.fromImage(result_img)
                self.label_5.setPixmap(result_pixmap)

    def OperasiPengurangan1(self):
                pixmap_3 = self.label_3.pixmap()
                pixmap_4 = self.label_4.pixmap()

                if pixmap_3 and pixmap_4:
                    img_3 = pixmap_3.toImage()
                    img_4 = pixmap_4.toImage()

                    width = img_3.width()
                    height = img_3.height()

                    result_img = QImage(width, height, QImage.Format_RGB32)

                    for x in range(width):
                        for y in range(height):
                            pixel_3 = img_3.pixel(x, y)
                            pixel_4 = img_4.pixel(x, y)

                            r_3, g_3, b_3 = QtGui.qRed(pixel_3), QtGui.qGreen(pixel_3), QtGui.qBlue(pixel_3)
                            r_4, g_4, b_4 = QtGui.qRed(pixel_4), QtGui.qGreen(pixel_4), QtGui.qBlue(pixel_4)

                            # rumus
                            r_result = max(r_3 - r_4, 0)
                            g_result = max(g_3 - g_4, 0)
                            b_result = max(b_3 - b_4, 0)

                            result_img.setPixel(x, y, QtGui.qRgb(r_result, g_result, b_result))

                    result_pixmap = QPixmap.fromImage(result_img)
                    self.label_5.setPixmap(result_pixmap)

    def OperasiPerkalian(self):
                pixmap_3 = self.label_3.pixmap()
                pixmap_4 = self.label_4.pixmap()

                if pixmap_3 and pixmap_4:
                    img_3 = pixmap_3.toImage()
                    img_4 = pixmap_4.toImage()

                    width = img_3.width()
                    height = img_3.height()

                    result_img = QImage(width, height, QImage.Format_RGB32)

                    for x in range(width):
                        for y in range(height):
                            pixel_3 = img_3.pixel(x, y)
                            pixel_4 = img_4.pixel(x, y)

                            r_3, g_3, b_3 = QtGui.qRed(pixel_3), QtGui.qGreen(pixel_3), QtGui.qBlue(pixel_3)
                            r_4, g_4, b_4 = QtGui.qRed(pixel_4), QtGui.qGreen(pixel_4), QtGui.qBlue(pixel_4)

                            # rumus
                            r_result = (r_3 * r_4) // 255  
                            g_result = (g_3 * g_4) // 255
                            b_result = (b_3 * b_4) // 255

                            result_img.setPixel(x, y, QtGui.qRgb(r_result, g_result, b_result))

                    result_pixmap = QPixmap.fromImage(result_img)
                    self.label_5.setPixmap(result_pixmap)


    def Penjumlahan_Skalar_3(self, scalar):
                pixmap_3 = self.label_3.pixmap()
                pixmap_4 = self.label_4.pixmap()

                if pixmap_3 and pixmap_4:
                    img_3 = pixmap_3.toImage()
                    img_4 = pixmap_4.toImage()

                    width = img_3.width()
                    height = img_3.height()

                    result_img = QImage(width, height, QImage.Format_RGB32)

                    for x in range(width):
                        for y in range(height):
                            pixel_3 = img_3.pixel(x, y)
                            pixel_4 = img_4.pixel(x, y)

                            r_3, g_3, b_3 = QtGui.qRed(pixel_3), QtGui.qGreen(pixel_3), QtGui.qBlue(pixel_3)
                            r_4, g_4, b_4 = QtGui.qRed(pixel_4), QtGui.qGreen(pixel_4), QtGui.qBlue(pixel_4)

                            # rumus
                            r_result = min(r_3 + scalar, 255) 
                            g_result = min(g_3 + scalar, 255)
                            b_result = min(b_3 + scalar, 255)

                            result_img.setPixel(x, y, QtGui.qRgb(r_result, g_result, b_result))

                    result_pixmap = QPixmap.fromImage(result_img)
                    self.label_5.setPixmap(result_pixmap)

    def Pengurangan_Skalar_3(self, scalar):
                pixmap_3 = self.label_3.pixmap()
                pixmap_4 = self.label_4.pixmap()

                if pixmap_3 and pixmap_4:
                    img_3 = pixmap_3.toImage()
                    img_4 = pixmap_4.toImage()

                    width = img_3.width()
                    height = img_3.height()

                    result_img = QImage(width, height, QImage.Format_RGB32)

                    for x in range(width):
                        for y in range(height):
                            pixel_3 = img_3.pixel(x, y)
                            pixel_4 = img_4.pixel(x, y)

                            r_3, g_3, b_3 = QtGui.qRed(pixel_3), QtGui.qGreen(pixel_3), QtGui.qBlue(pixel_3)
                            r_4, g_4, b_4 = QtGui.qRed(pixel_4), QtGui.qGreen(pixel_4), QtGui.qBlue(pixel_4)

                            # rumus
                            r_result = max(r_3 - scalar, 0)
                            g_result = max(g_3 - scalar, 0)
                            b_result = max(b_3 - scalar, 0)

                            result_img.setPixel(x, y, QtGui.qRgb(r_result, g_result, b_result))

                    result_pixmap = QPixmap.fromImage(result_img)
                    self.label_5.setPixmap(result_pixmap)

    def Perkalian_Skalar_C(self, c):
                pixmap_A = self.label_3.pixmap()
                if pixmap_A:
                    img_A = pixmap_A.toImage()

                    width = img_A.width()
                    height = img_A.height()

                    result_img = QImage(width, height, QImage.Format_RGB32)

                    for x in range(width):
                        for y in range(height):
                            pixel_A = img_A.pixel(x, y)

                            r_A, g_A, b_A = QtGui.qRed(pixel_A), QtGui.qGreen(pixel_A), QtGui.qBlue(pixel_A)

                            # rumus
                            r_result = min(255, max(0, int(r_A * c)))
                            g_result = min(255, max(0, int(g_A * c)))
                            b_result = min(255, max(0, int(b_A * c)))

                            result_img.setPixel(x, y, QtGui.qRgb(r_result, g_result, b_result))

                    result_pixmap = QPixmap.fromImage(result_img)
                    self.label_5.setPixmap(result_pixmap)

    def Pembagian_Skalar_C(self, c):
        pixmap_A = self.label_3.pixmap()
        if pixmap_A:
            img_A = pixmap_A.toImage()

            width = img_A.width()
            height = img_A.height()

            result_img = QImage(width, height, QImage.Format_RGB32)

            for x in range(width):
                for y in range(height):
                    pixel_A = img_A.pixel(x, y)

                    r_A, g_A, b_A = QtGui.qRed(pixel_A), QtGui.qGreen(pixel_A), QtGui.qBlue(pixel_A)

                    # Scalar division by c, ensuring not to divide by zero
                    if c != 0:
                        r_result = min(255, max(0, int(r_A / c)))
                        g_result = min(255, max(0, int(g_A / c)))
                        b_result = min(255, max(0, int(b_A / c)))
                    else:
                        r_result, g_result, b_result = r_A, g_A, b_A  # Avoid division by zero

                    result_img.setPixel(x, y, QtGui.qRgb(r_result, g_result, b_result))

            result_pixmap = QPixmap.fromImage(result_img)
            self.label_5.setPixmap(result_pixmap)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
