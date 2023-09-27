from PyQt5.QtCore import QObject, pyqtSlot

from model.counter_model import CounterModel
from view.counter_view import CounterView


class CounterController(QObject):
    def __init__(self):
        super().__init__()
        self.model = CounterModel()
        self.view = CounterView()
        self.view.increment_signal.connect(self.increment_count)
        self.update_view()
        self.view.show()

    @pyqtSlot()
    def increment_count(self):
        self.model.increment()
        self.update_view()

    def update_view(self):
        count = self.model.get_count()
        self.view.update_count(count)
