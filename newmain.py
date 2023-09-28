
import sys
from PyQt5.QtWidgets import QApplication

from controller.counter_controller import ImageController

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    controller = ImageController()
    controller.show()
    sys.exit(app.exec_())