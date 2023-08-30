import sys
import platform
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtCore import QObject, pyqtSlot
from pathlib import Path


class AppPVCController(QObject):

    def __init__(self, model):
        super().__init__()
        self.model = model

    def onOpen(self):
        file_filter = "Image Files (*.jpg *.png)"
        directory_path = Path.home() / "Pictures"

        response, _ = QFileDialog.getOpenFileName(
            caption="Select Image",
            directory=str(directory_path),
            filter=file_filter,
            initialFilter=file_filter
        )

        if response:
            self.model.addImgPath(response)

    def onSave(self):
        print("onSave")

    def onSaveAs(self):
        image_path = self.model.imgPath
        if image_path:
            file_filter = "JPEG Image (*.jpg);;PNG Image (*.png)"
            directory_path = Path.home() / "Pictures"

            response, _ = QFileDialog.getSaveFileName(
                caption="Save Image As",
                directory=str(directory_path),
                filter=file_filter,
                initialFilter=file_filter
            )

            if response:
                
                print("Saving the image as:", response)
        else:
            print("No image path available.")

    def onExit(self):
        sys.exit()
