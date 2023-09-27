from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QDesktopWidget

class CounterView(QMainWindow):
    increment_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        screen = QDesktopWidget().screenGeometry()
        width, height = screen.width(), screen.height()

        self.setWindowTitle("Counter App")
        self.setGeometry(0, 0, width, height)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("Count: 0")
        self.layout.addWidget(self.label)

        self.increment_button = QPushButton("Increment")
        self.layout.addWidget(self.increment_button)

        self.increment_button.clicked.connect(self.increment_signal.emit)

    def update_count(self, count):
        self.label.setText(f"Count: {count}")
