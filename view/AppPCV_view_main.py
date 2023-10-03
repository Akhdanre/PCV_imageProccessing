from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QSlider,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QWidget,
)
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from view import slider_windowTranslasi
from view.AppPCV_view_ui import PCV_view
from PyQt5.QtWidgets import QDesktopWidget
from view.floatingWidget import FloatingWidget
import sys

from view.slider_window import SliderWindow
from view.slider_windowTranslasi import SliderWindowTranslasi


class AppPCVViewMain(QMainWindow):
    def __init__(self, model, controller):
        super().__init__()
        self.model = model
        self.controller = controller
        self.view = PCV_view()
        self.view.setupUi(self)

        screen = QDesktopWidget().screenGeometry()
        width, height = screen.width(), screen.height()
        x = (width - self.width()) / 2
        y = (height - self.height()) / 2
        self.move(x, y)

        self.view.actionOpen.triggered.connect(
            lambda: self.controller.onOpen(1))
        self.view.actionSave_As.triggered.connect(
            lambda: self.controller.onSaveAs(self.view.label_2))
        self.view.actionExit.triggered.connect(self.controller.onExit)

        self.view.actionAverage.triggered.connect(
            lambda: self.controller.onImageProces("average"))
        self.view.actionLuminance.triggered.connect(
            lambda: self.controller.onImageProces("luminance"))
        self.view.actionLightness.triggered.connect(
            lambda: self.controller.onImageProces("lightness"))
        self.view.actionInvers.triggered.connect(
            lambda: self.controller.onImageProces("invers"))

        self.view.actionContrast.triggered.connect(
            lambda: self.sliderWindow("contrast"))
        self.view.actionBrightness.triggered.connect(
            lambda: self.sliderWindow("brightness"))

        self.view.actionHistogram_Equalization.triggered.connect(
            self.controller.imageHistogram)

        self.view.actionVertikal.triggered.connect(
            self.controller.onFlipVertical)
        self.view.actionHorizontal.triggered.connect(
            self.controller.onFlipHorizontal)

        self.view.actionScallingUni.triggered.connect(
            self.controller.scalingUniform)
        self.view.actionScallingNonUni.triggered.connect(
            self.controller.scalingNonUniform)

        self.view.actionNot.triggered.connect(self.controller.operasiNot)
        self.view.actionOr.triggered.connect(self.controller.operasiXor)
        self.view.actionAnd.triggered.connect(self.controller.operasiAnd)

        self.view.actionPenjumlahan.triggered.connect(
            self.controller.operasiPenjumlahan)
        self.view.actionPengurangan.triggered.connect(
            self.controller.operasiPengurangan)
        self.view.actionPerkalian.triggered.connect(
            self.controller.operasiPerkalian)
        self.view.actionPembagian.triggered.connect(
            self.controller.operasiPembagian)

        self.view.action1_bit.triggered.connect(
            lambda: self.controller.bitDepth(1))
        self.view.action2_bit.triggered.connect(
            lambda: self.controller.bitDepth2())
        self.view.action2_bit_2.triggered.connect(
            lambda: self.controller.bitDepth3())
        self.view.action4_bit.triggered.connect(
            lambda: self.controller.bitDepth4())
        self.view.action5_bit.triggered.connect(
            lambda: self.controller.bitDepthAll(5))
        self.view.action6_bit.triggered.connect(
            lambda: self.controller.bitDepthAll(6))
        self.view.action7_bit.triggered.connect(
            lambda: self.controller.bitDepthAll(7))

        self.view.actionGaussian_Blur_3x3.triggered.connect(
            lambda: self.controller.gaussianBlur(3))
        self.view.actionGaussian_Blur_5x5.triggered.connect(
            lambda: self.controller.gaussianBlur(5))
        self.view.actionLow_Pass_Filter.triggered.connect(
            self.controller.lowPass)
        self.view.actionHigh_Pass_Filter.triggered.connect(
            self.controller.highPass)
        self.view.actionSbbel.triggered.connect(
            self.controller.sobel)
        self.view.actionPrewitt.triggered.connect(
            self.controller.prewit)
        self.view.actionRobert.triggered.connect(
            self.controller.edgeDetectionRobert)
        self.view.actionIDENTITY.triggered.connect(
            self.controller.indetityFilter)

        self.view.actionFuzzy_Grayscale.triggered.connect(
            self.controller.fuzzyHistogram)
        self.view.actionFuzzy_HE_RGB.triggered.connect(
            self.controller.fuzzyHistogramRGB)
        self.view.actionInput.triggered.connect(self.controller.histogramInput)
        self.view.actionOutput.triggered.connect(
            self.controller.histogramOutput)
        self.view.actionInput_Output.triggered.connect(
            self.controller.histogramInputOutput)

        self.view.actionTranslasi.triggered.connect(self.sliderWindowTranslasi)
        self.view.actionRotasi.triggered.connect(self.sliderwindowrotasi)

        # self.view.actionAritmatika.triggered.connect(self.show_middle_label)
        self.view.actionSplit.triggered.connect(self.show_middle_label)
        self.view.actionArtBack.triggered.connect(self.hideMiddleLable)

        self.model.image_result_changed.connect(self.on_image_result)
        self.model.image_path_changed.connect(self.on_image_change)
        self.model.image_path_changed2.connect(self.on_image_change2)

        self.view.label_3.mousePressEvent = self.lable3Open
        self.view.label.mousePressEvent = self.lableOpen

    def lableOpen(self, event):
        if event.button() == Qt.LeftButton:
            self.controller.onOpen(1)

    def lable3Open(self, event):
        if event.button() == Qt.LeftButton:
            self.controller.onOpen(2)

    def sliderWindow(self, route):
        sliderW = SliderWindow(self)
        sliderW.show()
        sliderW.button.clicked.connect(
            lambda: self.controller.brightnessRoute(
                route, sliderW.slider.value())
        )

    def sliderwindowrotasi(self):
        sliderW = SliderWindow(self)
        sliderW.show()
        sliderW.button.clicked.connect(
            lambda: self.controller.rotasi(sliderW.slider.value())
        )

    def sliderWindowTranslasi(self):
        sliderW = SliderWindowTranslasi(self)
        sliderW.show()
        sliderW.button.clicked.connect(
            lambda: self.controller.translasi(
                sliderW.slider_x.value(), sliderW.slider_y.value())
        )

    def show_middle_label(self):
        self.resize(1425, 518)
        x_window = (QtWidgets.QDesktopWidget().width() - self.width()) / 2
        y_window = (QtWidgets.QDesktopWidget().height() - self.height()) / 2
        self.move(x_window, y_window)
        self.view.label_2.move(950, 20)
        self.view.label_3.show()

    def hideMiddleLable(self):
        self.resize(944, 518)
        x_window = (QtWidgets.QDesktopWidget().width() - self.width()) / 2
        y_window = (QtWidgets.QDesktopWidget().height() - self.height()) / 2
        self.move(x_window, y_window)
        self.view.label_2.move(480, 20)
        self.view.label_3.hide()

    @pyqtSlot(str)
    def on_image_change(self, value):
        pixmap = QPixmap(value)
        self.view.label.setPixmap(pixmap)
        self.view.label.setScaledContents(True)

    @pyqtSlot(str)
    def on_image_change2(self, value):
        pixmap = QPixmap(value)
        self.view.label_3.setPixmap(pixmap)

    @pyqtSlot(QPixmap)
    def on_image_result(self, value):
        self.view.label_2.setPixmap(value)
        self.view.label_2.setAlignment(Qt.AlignCenter)
        self.view.label_2.setScaledContents(True)
