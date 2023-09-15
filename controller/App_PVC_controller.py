import sys
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtCore import QObject, pyqtSlot, QBuffer
from pathlib import Path
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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

    def onSaveAs(self, label):
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
                new_path = f'{response}.png'
                pixmap = QPixmap(label.size())
                label.render(pixmap)
                pixmap.save(new_path)

        else:
            print("No image path available.")

    def onExit(self):
        sys.exit()


    def imageHistogram(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape

            # Mengonversi gambar ke dalam citra grayscale
            gray = np.zeros((height, width), dtype=np.uint8)
            for i in range(height):
                for j in range(width):
                    value = (0.299 * image[i, j, 0] + 0.587 * image[i, j, 1] + 0.144 * image[i, j, 2])
                    gray[i, j] = round(value)

            # Menghitung histogram citra grayscale
            histogram_gray = np.histogram(gray, bins=256, range=(0, 256))[0]

            # Menghitung histogram untuk setiap saluran warna RGB
            histogram_red = np.histogram(image[:,:,0], bins=256, range=(0, 256))[0]
            histogram_green = np.histogram(image[:,:,1], bins=256, range=(0, 256))[0]
            histogram_blue = np.histogram(image[:,:,2], bins=256, range=(0, 256))[0]

            # Menampilkan histogram dalam satu gambar
            plt.figure(figsize=(10, 5))
            plt.subplot(2, 2, 1)
            plt.bar(np.arange(256), histogram_gray, width=1.0, color='gray')
            plt.title("Histogram Grayscale")
            plt.xlabel("Nilai Piksel")
            plt.ylabel("Frekuensi")

            plt.subplot(2, 2, 2)
            plt.bar(np.arange(256), histogram_red, width=1.0, color='red')
            plt.title("Histogram Merah (R)")
            plt.xlabel("Nilai Piksel")
            plt.ylabel("Frekuensi")

            plt.subplot(2, 2, 3)
            plt.bar(np.arange(256), histogram_green, width=1.0, color='green')
            plt.title("Histogram Hijau (G)")
            plt.xlabel("Nilai Piksel")
            plt.ylabel("Frekuensi")

            plt.subplot(2, 2, 4)
            plt.bar(np.arange(256), histogram_blue, width=1.0, color='blue')
            plt.title("Histogram Biru (B)")
            plt.xlabel("Nilai Piksel")
            plt.ylabel("Frekuensi")

            plt.tight_layout()
            plt.show()

    def identify_axes(ax_dict, fontsize=48):
        kw = dict(ha="center", va="center",
        fontsize=fontsize, color="darkgrey")
        for k, ax in ax_dict.items():
            ax.text(0.5, 0.5, k,
        transform=ax.transAxes, **kw)

    def onImageProces(self, condition):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            gray = self.imageToGrayScale(image, condition)

            height, width = gray.shape
            # bytes_per_line = 1 * width
            bytes_per_line = width
            q_img = QImage(gray.data, width, height,
                           bytes_per_line, QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def imageToGrayScale(self, img, condition):
        height, width, channels = img.shape
        gray = np.zeros((height, width), dtype=np.uint8)
        if condition == "average":
            for i in range(height):
                for j in range(width):
                    gray[i, j] = np.uint8(
                        (0.299 * img[i, j, 0] + 0.587 * img[i, j, 1] + 0.144 * img[i, j, 2]) / 3)
        if condition == "lightness":
            for i in range(height):
                for j in range(width):
                    gray[i, j] = np.uint8(
                        (img[i, j, 0] + img[i, j, 1] + img[i, j, 2])/3)
        if condition == "luminance":
            for i in range(height):
                for j in range(width):
                    value = (0.299 * img[i, j, 0]) + (0.587 *
                                                      img[i, j, 1]) + (0.144 * img[i, j, 2])
                    if value > 255:
                        gray[i, j] = np.uint8(255)
                    else:
                        gray[i, j] = np.uint8(value)
        if condition == "invers":
            for i in range(height):
                for j in range(width):
                    value = (0.299 * img[i, j, 0]) + (0.587 *
                                                      img[i, j, 1]) + (0.144 * img[i, j, 2])
                    if value > 255:
                        gray[i, j] = 0
                    else:
                        gray[i, j] = 255 - value
        return gray
