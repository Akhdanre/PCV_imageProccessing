from PyQt5.QtWidgets import QMainWindow, QFileDialog
from view.mainView import Ui_mainWindow
from model.counter_model import ImageModel 
from pathlib import Path


class ImageController(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.model = ImageModel()  # Inisialisasi model

        # Hubungkan tombol-tombol atau menu dengan metode-metode controller di sini
        self.ui.actionOpen.triggered.connect(self.open_image)
        self.ui.actionSave.triggered.connect(self.save_image)
        self.ui.actionQuit.triggered.connect(self.quit_application)
        
        self.model.image_path_changed.connect(self.ui.on_image_change)

    def open_image(self):
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
            

    def save_image(self):
        # Tambahkan logika untuk menyimpan gambar di sini
        pass

    def quit_application(self):
        # Tambahkan logika untuk keluar dari aplikasi di sini
        pass