from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap


class AppPCVModel(QObject):

    image_path_changed = pyqtSignal(str)
    image_path_changed2 = pyqtSignal(str)
    image_result_changed = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()

    @property
    def imgPath(self):
        return self.path

    def addImgPath(self, value):
        self.path = value
        self.image_path_changed.emit(value)

    @property
    def imgPath2(self):
        return self.path2

    def addImgPath2(self, value):
        self.path2 = value
        self.image_path_changed2.emit(value)

    def setHistogramBefore(self, value):
        self.histogramBefore = value

    def setHistogramAfter(self, value):
        self.histogramAfter = value

    def getHistogramBefore(self):
        return self.histogramBefore

    def getHistogramAfter(self):
        return self.histogramAfter
