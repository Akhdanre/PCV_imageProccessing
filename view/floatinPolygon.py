import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtCore import Qt

class PolygonWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.polygon = QPolygonF()
        self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the existing polygon
        if not self.polygon.isEmpty():
            painter.setPen(Qt.blue)
            painter.drawPolygon(self.polygon)

    def mousePressEvent(self, event):
        if not self.drawing:
            self.drawing = True
            self.polygon = QPolygonF()
        self.polygon.append(event.pos())
        self.update()