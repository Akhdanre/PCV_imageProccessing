from PyQt5.QtCore import QObject, pyqtSignal


class AppPVCModel(QObject):
    
    image_path_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
    
    @property
    def imgPath(self): 
        return self.path
    
    def addImgPath(self, value):
        self.path = value
        self.image_path_changed.emit(value)

