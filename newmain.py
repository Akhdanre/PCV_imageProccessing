
from controller.counter_controller import CounterController
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = CounterController()
    sys.exit(app.exec_())
