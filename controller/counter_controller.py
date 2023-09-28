from PyQt5.QtWidgets import QMainWindow, QFileDialog
from mainView import Ui_mainWindow
from model.counter_model import ImageModel  # Import model yang sudah dibuat
# from ui_mainwindow import Ui_mainWindow 


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

    def open_image(self):
        # Tambahkan logika untuk membuka gambar di sini
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.bmp *.tif);;All Files (*)", options=options)
        if file_path:
            # Lakukan sesuatu dengan file_path, misalnya, menampilkan gambar di label
            pass

    def save_image(self):
        # Tambahkan logika untuk menyimpan gambar di sini
        pass

    def quit_application(self):
        # Tambahkan logika untuk keluar dari aplikasi di sini
        pass