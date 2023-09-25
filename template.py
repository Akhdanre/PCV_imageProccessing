import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout, QLabel

class SliderExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt Slider Example')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Slider Value: 0', self)
        layout.addWidget(self.label)

        self.slider = QSlider()
        self.slider.setOrientation(1)  # Set the slider orientation to vertical
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.sliderValueChanged)

        layout.addWidget(self.slider)
        self.setLayout(layout)

    def sliderValueChanged(self):
        value = self.slider.value()
        self.label.setText(f'Slider Value: {value}')

def main():
    app = QApplication(sys.argv)
    ex = SliderExample()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
