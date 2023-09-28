import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class FloatingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel("Floating Label", self)
        self.setGeometry(100, 100, 200, 200)

        self.dragging = False
        self.offset = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = self.mapToGlobal(event.pos() - self.offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.lightGray)
        painter.setBrush(Qt.white)
        painter.drawRect(self.rect())

