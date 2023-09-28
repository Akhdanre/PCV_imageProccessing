from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap

class ImageModel(QObject):
    image_path_changed = pyqtSignal(str)
    image_result_changed = pyqtSignal(QPixmap)

    def __init__(self):
        super().__init__()
        self.path = ""
    
    @property
    def imgPath(self): 
        return self.path
    
    def addImgPath(self, value):
        self.path = value
        self.image_path_changed.emit(value)

