from PyQt5.QtCore import QObject, pyqtSignal


class AppPVCModel(object):
    label_value = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.label_value = ''

    