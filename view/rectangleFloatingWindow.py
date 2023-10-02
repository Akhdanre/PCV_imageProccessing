import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

class FloatingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        self.setStyleSheet("border: 2px solid black;")

        label = QLabel("Floating Widget")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("background-color: rgba(255, 255, 255, 100);")

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        self.drag_start = QPoint(0, 0)

        self.setGeometry(100, 100, 200, 100)
        self.setWindowTitle('Floating Widget')

    def mousePressEvent(self, event):
        self.drag_start = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(0, 0, 0, 0))
    app.setPalette(palette)

    widget = FloatingWidget()
    widget.show()

    sys.exit(app.exec_())
