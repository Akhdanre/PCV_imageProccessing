import sys
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path
# from view.AppPVC import Ui_MainWindow


class AppPVCController(object) :

    def __init__(self, model):
        super().__init__()
        self.model = model


    def onOpen(self) :
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            "/home/akeon/Pictures/", 
            "Images (*.png *.jpg)"
        )
        if filename:
            path = Path(filename)
            self.view.label.setText(path)

    def onSave(self) :
        print("onSave")

    def onSaveAs(self): 
        print("onSaveAs")

    def onExit(self):
        sys.exit()