import sys
from controller.App_PCV_controller import AppPCVController
from model.AppPCV_model import AppPCVModel
from view.AppPCV_view_main import AppPCVViewMain
from PyQt5.QtWidgets import QApplication

class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.main_model = AppPCVModel()
        self.main_controller = AppPCVController(self.main_model)
        self.main_view = AppPCVViewMain(self.main_model, self.main_controller)
        self.main_view.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())