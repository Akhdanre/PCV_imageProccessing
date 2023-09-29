from PyQt5 import QtCore, QtWidgets
import sys


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

        # self.button.clicked.connect(
        #     lambda: parent.controller.brightnessRoute(route, self.slider.value()))
