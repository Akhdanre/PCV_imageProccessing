# class SliderWindow(QDialog):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle('Slider Window')
#         self.setGeometry(300, 300, 300, 150)

#         layout = QVBoxLayout()

#         self.label = QLabel('Slider Value: 0')
#         layout.addWidget(self.label)

#         self.slider = QSlider()
#         self.slider.setOrientation(1)  # Vertical orientation
#         self.slider.setMinimum(0)
#         self.slider.setMaximum(100)
#         self.slider.setValue(0)
#         self.slider.valueChanged.connect(self.sliderValueChanged)

#         layout.addWidget(self.slider)

#         ok_button = QPushButton('OK')
#         ok_button.clicked.connect(self.accept)
#         layout.addWidget(ok_button)

#         self.setLayout(layout)