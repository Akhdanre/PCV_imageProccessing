import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from template import FloatingLabel


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        self.floating_label = FloatingLabel(self)
        # Atur posisi awal FloatingLabel di dalam main view
        self.floating_label.move(100, 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_view = MainView()
    main_view.show()
    sys.exit(app.exec_())
