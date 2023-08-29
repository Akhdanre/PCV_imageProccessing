
from PyQt5.QtWidgets import QMainWindow

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
        self.view.actionSave_As.triggered.connect(self.controller.onSaveAs)
        self.view.actionExit.triggered.connect(self.controller.onExit)