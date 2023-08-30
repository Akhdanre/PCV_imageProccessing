from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot
from view.AppPVC_view_ui import PVC_view

class AppPVCViewMain(QMainWindow):
    def __init__(self, model, controller):
        super().__init__()
        self.model = model
        self.controller = controller
        self.view = PVC_view()
        self.view.setupUi(self)

        self.view.actionOpen.triggered.connect(self.controller.onOpen)
        self.view.action_save.triggered.connect(self.controller.onSave)
        self.view.actionSave_As.triggered.connect(lambda: self.controller.onSaveAs(self.view.label))
        self.view.actionExit.triggered.connect(self.controller.onExit)

        self.model.image_path_changed.connect(self.on_image_change)

    @pyqtSlot(str)
    def on_image_change(self, value):
        pixmap = QPixmap(value)
        self.view.label.setPixmap(pixmap)
        self.view.label.setScaledContents(True)


