import sys
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot, QBuffer
from pathlib import Path
from PyQt5.QtGui import QPixmap, QImage, QColor, QImageReader
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from operasi_image.OperasiAritmatika import Ui_MainWindow


class AppPCVController(QObject):

    def __init__(self, model):
        super().__init__()
        self.model = model

    def onOpen(self, lable):
        file_filter = "Image Files (*.jpg *.png)"
        directory_path = Path.home() / "Pictures"

        response, _ = QFileDialog.getOpenFileName(
            caption="Select Image",
            directory=str(directory_path),
            filter=file_filter,
            initialFilter=file_filter
        )
        if response:
            if lable == 1:
                self.model.addImgPath(response)
            elif lable == 2:
                self.model.addImgPath2(response)

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
            image = Image.open(image_path)
            imgray = image.convert(mode='L')
            img_array = np.asarray(imgray)

            # Hitung histogram sebelum equalization
            histogram_before = np.bincount(img_array.flatten(), minlength=256)

            # Normalisasi histogram
            num_pixels = np.sum(histogram_before)
            histogram_before = histogram_before / num_pixels

            # Hitung histogram gambar sebelum perubahan
            chistogram_before = np.cumsum(histogram_before)

            # Transformasi menjadi maps
            transform_map = np.floor(255 * chistogram_before).astype(np.uint8)
            img_list = list(img_array.flatten())

            # Transformasi nilai pixel untuk disesuaikan
            eq_img_list = [transform_map[p] for p in img_list]

            # Penyesuaian gambar array pixel ke gambar penuh
            eq_img_array = np.reshape(np.asarray(eq_img_list), img_array.shape)
            # eq_img = Image.fromarray(eq_img_array, mode='L')

            # Konversi gambar PIL ke QImage dengan mode warna yang sesuai
            eq_qimage = QImage(eq_img_array.tobytes(
            ), eq_img_array.shape[1], eq_img_array.shape[0], QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(eq_qimage)

            self.model.image_result_changed.emit(pixmap)

            histogram_after = np.bincount(
                eq_img_array.flatten(), minlength=256)
            histogram_after = histogram_after / np.sum(histogram_after)

            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.bar(range(256), histogram_before, color='b', alpha=0.7)
            plt.title('Before Histogram Equalization')
            plt.xlabel('Pixel Value')
            plt.ylabel('Normalized Frequency')

            plt.subplot(1, 2, 2)
            plt.bar(range(256), histogram_after, color='r', alpha=0.7)
            plt.title('After Histogram Equalization')
            plt.xlabel('Pixel Value')
            plt.ylabel('Normalized Frequency')

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
                    """ rumus average = (R + G + B) / 3"""
                    gray[i, j] = np.uint8(
                        (0.299 * img[i, j, 0] + 0.587 * img[i, j, 1] + 0.144 * img[i, j, 2]) / 3)
        if condition == "lightness":
            for i in range(height):
                for j in range(width):
                    value = (max((0.299 * img[i, j, 0]), (0.587 * img[i, j, 1]),  (0.144 * img[i, j, 2])) +
                             min(img[i, j, 0], img[i, j, 1], img[i, j, 2])) // 2
                    if value > 255:
                        gray[i, j] = np.uint8(255)
                    elif value < 0:
                        gray[i, j] = np.uint8(0)
                    else:
                        gray[i, j] = np.uint8(value)
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

    def onAritmatikaPage(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

    def onFlipVertical(self):
        image_path = self.model.imgPath
        if image_path:
            img = mpimg.imread(image_path)
            flipped_img = QImage(
                img.shape[1], img.shape[0], QImage.Format_RGB32)

            for x in range(img.shape[1]):
                for y in range(img.shape[0]):
                    pixel = img[y, x]
                    flipped_y = img.shape[0] - 1 - y
                    flipped_img.setPixelColor(x, flipped_y, QColor(*pixel))

            flipped_pixmap = QPixmap.fromImage(flipped_img)
            self.model.image_result_changed.emit(flipped_pixmap)

    def onFlipHorizontal(self):
        image_path = self.model.imgPath
        if image_path:
            img = mpimg.imread(image_path)
            flipped_img = QImage(
                img.shape[1], img.shape[0], QImage.Format_RGB32)

            for x in range(img.shape[1]):
                for y in range(img.shape[0]):
                    # Membalikkan piksel secara horizontal
                    pixel = img[y, img.shape[1] - 1 - x]
                    flipped_img.setPixelColor(x, y, QColor(*pixel))

            flipped_pixmap = QPixmap.fromImage(flipped_img)
            self.model.image_result_changed.emit(flipped_pixmap)

    def brightnessRoute(self, route, value):
        if route == "contrast":
            self.onContrast(value)
        elif route == "brightness":
            self.onBrightness(value)

    def onBrightness(self, c):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            value = np.zeros((height, width, channels), dtype=np.uint8)

            # c = 30

            for i in range(height):
                for j in range(width):
                    red = image[i, j, 0]
                    green = image[i, j, 1]
                    blue = image[i, j, 2]

                    rValue = red + c
                    gValue = green + c
                    bValue = blue + c

                    value[i, j, 0] = rValue if rValue <= 255 and rValue >= 0 else 0 if rValue < 0 else 255
                    value[i, j, 1] = gValue if gValue <= 255 and gValue >= 0 else 0 if gValue < 0 else 255
                    value[i, j, 2] = bValue if bValue <= 255 and bValue >= 0 else 0 if bValue < 0 else 255

            height1, width1, channels1 = value.shape
            bytes_per_line = channels1 * width1
            q_img = QImage(value.data, width1, height1,
                           bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def onContrast(self, c):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            value = np.zeros((height, width, channels), dtype=np.uint8)

            # c = 70
            f = 259 * (c + 255) / (255 * (259 - c))

            for i in range(height):
                for j in range(width):
                    red = image[i, j, 0]
                    green = image[i, j, 1]
                    blue = image[i, j, 2]

                    rValue = f * (red - 128) + 128
                    gValue = f * (green - 128) + 128
                    bValue = f * (blue - 128) + 128

                    value[i, j, 0] = rValue if rValue <= 255 and rValue >= 0 else 0 if rValue < 0 else 255
                    value[i, j, 1] = gValue if gValue <= 255 and gValue >= 0 else 0 if gValue < 0 else 255
                    value[i, j, 2] = bValue if bValue <= 255 and bValue >= 0 else 0 if bValue < 0 else 255

            height1, width1, channels1 = value.shape
            bytes_per_line = channels1 * width1
            q_img = QImage(value.data, width1, height1,
                           bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)