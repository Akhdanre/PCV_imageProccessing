import sys
import platform
from PyQt5.QtWidgets import QFileDialog, QWidget
from pathlib import Path


class AppPVCController(QWidget):

    def __init__(self, model):
        super().__init__()
        self.model = model

    def onOpen(self):
        file_filter = "Image File (*.jpg *.png)"
        directory_path =Path.home() / "Pictures"
        
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select Image",
            directory=str(directory_path),
            filter=file_filter,
            initialFilter=file_filter
        )
        print(response[0])

    def onSave(self):
        print("onSave")

    def onSaveAs(self):
        print("onSaveAs")

    def onExit(self):
        sys.exit()
