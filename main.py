import typing
from PyQt5 import QtWidgets
from controller.App_PVC_controller import AppPVCController
from model.AppPVC_model import AppPVCModel
from view.AppPVC_view_main import AppPVCViewMain
import sys
from PyQt5.QtWidgets import QApplication

class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.main_model = AppPVCModel()
        self.main_controller = AppPVCController(self.main_model)
        self.main_view = AppPVCViewMain(self.main_model, self.main_controller)
        self.main_view.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())