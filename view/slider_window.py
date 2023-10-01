from PyQt5 import QtCore, QtWidgets


class SliderWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SliderWindow, self).__init__(parent)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.button = QtWidgets.QPushButton("Ok")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.button)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setContentsMargins(20, 20, 20, 20)

        desktop = QtWidgets.QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        screen_width, screen_height = screen_rect.width(), screen_rect.height()

        window_width, window_height = 200, self.height()
        self.setGeometry((screen_width - window_width) // 2, (screen_height - window_height) // 2, window_width, window_height)

