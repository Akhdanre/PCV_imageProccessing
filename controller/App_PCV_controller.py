import math
import sys
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSlot, QBuffer
from pathlib import Path
from PyQt5.QtGui import QPixmap, QImage, QColor, QImageReader, qRgb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from operasi_image.OperasiAritmatika import Ui_MainWindow
import cv2
import colorsys
from rembg import remove


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

            if image.mode != 'L':
                image = image.convert('L')

            width, height = image.size

            hist_before = image.histogram()

            cdf = [sum(hist_before[:i+1]) for i in range(256)]

            w, h = width, height
            normalization_factor = (w * h) - 1

            equalized_image = Image.new('L', (width, height))
            pixels = equalized_image.load()

            for x in range(width):
                for y in range(height):
                    pixel_value = image.getpixel((x, y))
                    new_pixel_value = round(
                        cdf[pixel_value] * 255 / normalization_factor)
                    pixels[x, y] = new_pixel_value

            hist_after = equalized_image.histogram()

            self.model.setHistogramBefore(hist_before)
            self.model.setHistogramAfter(hist_after)
            q_image = QImage(equalized_image.tobytes(), width,
                             height, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.model.image_result_changed.emit(pixmap)

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

            # for i in range(height):
            #     for j in range(width):
            #         red = image[i, j, 0]
            #         green = image[i, j, 1]
            #         blue = image[i, j, 2]

            #         rValue = red + c
            #         gValue = green + c
            #         bValue = blue + c

            #         value[i, j, 0] = rValue if rValue <= 255 and rValue >= 0 else 0 if rValue < 0 else 255
            #         value[i, j, 1] = gValue if gValue <= 255 and gValue >= 0 else 0 if gValue < 0 else 255
            #         value[i, j, 2] = bValue if bValue <= 255 and bValue >= 0 else 0 if bValue < 0 else 255

            imageFloat = image.astype(np.float32)
            pixel = imageFloat + c
            value = np.clip(pixel, 0, 255).astype(np.uint8)

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

            # height, width, channels = image.shape
            # result = np.zeros((height, width, channels), dtype=np.uint8)
            # result = image.copy()
            # # c = 70

            f = 259 * (c + 255) / (255 * (259 - c))

            image_float = image.astype(np.float32)
            pixel = image_float - 128
            contrasted_image = np.clip(
                f * pixel + 128, 0, 255).astype(np.uint8)

            height1, width1, channels1 = contrasted_image.shape
            bytes_per_line = channels1 * width1
            q_img = QImage(contrasted_image.data, width1, height1,
                           bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

            # for i in range(height):
            #     for j in range(width):
            # red = image[i, j, 0]
            # green = image[i, j, 1]
            # blue = image[i, j, 2]

            # rValue = f * (red - 128) + 128
            # gValue = f * (green - 128) + 128
            # bValue = f * (blue - 128) + 128

            # value[i, j, 0] = rValue if rValue <= 255 and rValue >= 0 else 0 if rValue < 0 else 255
            # value[i, j, 1] = gValue if gValue <= 255 and gValue >= 0 else 0 if gValue < 0 else 255
            # value[i, j, 2] = bValue if bValue <= 255 and bValue >= 0 else 0 if bValue < 0 else 255

            # pixel = result[i, j]
            # result[i, j, 0] = np.clip(f * (pixel[0] - 128) + 128, 0, 255)
            # result[i, j, 1] = np.clip(f * (pixel[1] - 128) + 128, 0, 255)
            # result[i, j, 2] = np.clip(f * (pixel[2] - 128) + 128, 0, 255)

            # value = np.clip(f * (image - 128) + 128, 0, 255).astype(np.uint8)

            # height1, width1, channels1 = result.shape
            # bytes_per_line = channels1 * width1
            # q_img = QImage(result.data, width1, height1,
            #                bytes_per_line, QImage.Format_RGB888)

            # pixmap = QPixmap.fromImage(q_img)
            # self.model.image_result_changed.emit(pixmap)

    # def operasiPenjumlahan(self):
    #     imageP1 = self.model.imgPath
    #     imageP2 = self.model.imgPath2

    #     if imageP1 and imageP2:
    #         image1 = mpimg.imread(imageP1)
    #         image2 = mpimg.imread(imageP2)

    #         height1, width1, channels1 = image1.shape
    #         height2, width2, channels2 = image2.shape

    #         arr1 = np.zeros((height1, width1, channels1), dtype=np.uint8)
    #         # arr2 = np.zeros((height2, width2, channels2), dtype=np.uint8)

    #         for i in range(height1):
    #             for l in range(width1):
    #                 rValue = image1[i, l, 0] + image2[i, l, 0]
    #                 gValue = image1[i, l, 1] + image2[i, l, 1]
    #                 bValue = image1[i, l, 2] + image2[i, l, 2]

    #                 arr1[i, l, 0] = rValue if rValue <= 255.0 and rValue >= 0.0 else 0.0 if rValue < 0.0 else 255.0
    #                 arr1[i, l, 1] = gValue if gValue <= 255.0 and gValue >= 0.0 else 0.0 if gValue < 0.0 else 255.0
    #                 arr1[i, l, 2] = bValue if bValue <= 255.0 and bValue >= 0.0 else 0.0 if bValue < 0.0 else 255.0

    #                 print(arr1[i, l, 0], arr1[i, l, 1], arr1[i, l, 2])

    #         heightR, widthR, channelsR = arr1.shape
    #         bytes_per_line = channelsR * width1
    #         q_img = QImage(arr1.data, widthR, heightR,
    #                        bytes_per_line, QImage.Format_RGB888)

    #         pixmap = QPixmap.fromImage(q_img)
    #         self.model.image_result_changed.emit(pixmap)

    def operasiPenjumlahan(self):
        imageP1 = self.model.imgPath
        imageP2 = self.model.imgPath2

        if imageP1 and imageP2:
            image1 = mpimg.imread(imageP1)
            image2 = mpimg.imread(imageP2)

            if image1.shape == image2.shape:
                result = np.clip(image1.astype(int) +
                                 image2.astype(int), 0, 255).astype(np.uint8)

                heightR, widthR, channelsR = result.shape
                bytes_per_line = channelsR * widthR
                q_img = QImage(result.data, widthR, heightR,
                               bytes_per_line, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(q_img)
                self.model.image_result_changed.emit(pixmap)
            else:
                print("Dimensi kedua gambar tidak cocok.")

    def operasiPengurangan(self):
        imageP1 = self.model.imgPath
        imageP2 = self.model.imgPath2

        if imageP1 and imageP2:
            image1 = mpimg.imread(imageP1)
            image2 = mpimg.imread(imageP2)

            if image1.shape == image2.shape:
                result = np.clip(image1.astype(int) -
                                 image2.astype(int), 0, 255).astype(np.uint8)

                heightR, widthR, channelsR = result.shape
                bytes_per_line = channelsR * widthR
                q_img = QImage(result.data, widthR, heightR,
                               bytes_per_line, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(q_img)
                self.model.image_result_changed.emit(pixmap)
            else:
                print("Dimensi kedua gambar tidak cocok.")

    def operasiPerkalian(self):
        imageP1 = self.model.imgPath
        imageP2 = self.model.imgPath2

        if imageP1 and imageP2:
            image1 = mpimg.imread(imageP1)
            image2 = mpimg.imread(imageP2)

            if image1.shape == image2.shape:
                result = np.clip(image1.astype(int) *
                                 image2.astype(int), 0, 255).astype(np.uint8)

                heightR, widthR, channelsR = result.shape
                bytes_per_line = channelsR * widthR
                q_img = QImage(result.data, widthR, heightR,
                               bytes_per_line, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(q_img)
                self.model.image_result_changed.emit(pixmap)
            else:
                print("Dimensi kedua gambar tidak cocok.")

    def operasiPembagian(self):
        imageP1 = self.model.imgPath
        imageP2 = self.model.imgPath2

        if imageP1 and imageP2:
            image1 = mpimg.imread(imageP1)
            image2 = mpimg.imread(imageP2)

            if image1.shape == image2.shape:
                result = np.clip(image1.astype(int) /
                                 image2.astype(int), 0, 255).astype(np.uint8)

                heightR, widthR, channelsR = result.shape
                bytes_per_line = channelsR * widthR
                q_img = QImage(result.data, widthR, heightR,
                               bytes_per_line, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(q_img)
                self.model.image_result_changed.emit(pixmap)
            else:
                print("Dimensi kedua gambar tidak cocok.")

    def operasiNot(self):
        imageP = self.model.imgPath

        if imageP:
            image = mpimg.imread(imageP)
            if len(image.shape) == 3:
                image = image[:, :, 0]

            image = (image * 255).astype(np.uint8)
            value = np.bitwise_not(image)

            heightR, widthR = value.shape
            bytes_per_line = widthR
            q_img = QImage(value.data, widthR, heightR,
                           bytes_per_line, QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def operasiAnd(self):
        imageP = self.model.imgPath
        imageP2 = self.model.imgPath2

        if imageP and imageP2:
            image = mpimg.imread(imageP)
            image2 = mpimg.imread(imageP2)

            result = np.bitwise_and(image, image2).astype(np.uint8)

            heightR, widthR, channelsR = result.shape
            bytes_per_line = channelsR * widthR
            q_img = QImage(result.data, widthR, heightR,
                           bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)
        else:
            print("tidak boleh kosong")

    def operasiXor(self):
        imageP1 = self.model.imgPath
        imageP2 = self.model.imgPath2

        if imageP1 and imageP2:
            image1 = mpimg.imread(imageP1)
            image2 = mpimg.imread(imageP2)

            if image1.shape == image2.shape:
                result = np.bitwise_xor(image1, image2).astype(np.uint8)

                heightR, widthR, channelsR = result.shape
                bytes_per_line = channelsR * widthR
                q_img = QImage(result.data, widthR, heightR,
                               bytes_per_line, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(q_img)
                self.model.image_result_changed.emit(pixmap)
            else:
                print("Ukuran kedua citra tidak sama")
        else:
            print("Path citra tidak valid")

    def bitDepth(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)

            height, width, _ = image.shape
            result = np.zeros((height, width), dtype=np.uint8)
            threshold = 127

            for i in range(height):
                for j in range(width):
                    red = image[i, j, 0]
                    green = image[i, j, 1]
                    blue = image[i, j, 2]
                    grayscale = 0.299 * red + 0.587 * green + 0.114 * blue
                    result[i, j] = 0 if grayscale < threshold else 255

            height1, width1 = result.shape
            bytes_per_line = (width1 + 7) // 8
            q_img = QImage(bytes(result.tobytes()), width1,
                           height1, bytes_per_line, QImage.Format_Mono)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def bitDepth2(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)

            height, width, _ = image.shape
            result = np.zeros((height, width), dtype=np.uint8)
            threshold1 = 85
            threshold2 = 170

            for i in range(height):
                for j in range(width):
                    red = image[i, j, 0]
                    green = image[i, j, 1]
                    blue = image[i, j, 2]
                    grayscale = 0.299 * red + 0.587 * green + 0.114 * blue
                    if grayscale < threshold1:
                        result[i, j] = 0
                    elif grayscale < threshold2:
                        result[i, j] = 1
                    else:
                        result[i, j] = 2

            height1, width1 = result.shape
            q_img = QImage(result.data, width1, height1,
                           width1, QImage.Format_Indexed8)
            color_table = [qRgb(0, 0, 0), qRgb(85, 85, 85), qRgb(
                170, 170, 170), qRgb(255, 255, 255)]
            q_img.setColorTable(color_table)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def bitDepth3(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)

            height, width, _ = image.shape
            result = np.zeros((height, width), dtype=np.uint8)
            threshold1 = 85
            threshold2 = 170
            threshold3 = 255

            for i in range(height):
                for j in range(width):
                    red = image[i, j, 0]
                    green = image[i, j, 1]
                    blue = image[i, j, 2]
                    grayscale = 0.299 * red + 0.587 * green + 0.114 * blue
                    if grayscale < threshold1:
                        result[i, j] = 0
                    elif grayscale < threshold2:
                        result[i, j] = 1
                    elif grayscale < threshold3:
                        result[i, j] = 2
                    else:
                        result[i, j] = 3

            height1, width1 = result.shape
            q_img = QImage(result.data, width1, height1,
                           width1, QImage.Format_Indexed8)

            # Buat tabel warna untuk kedalaman bit 3
            color_table = [qRgb(0, 0, 0), qRgb(85, 85, 85), qRgb(
                170, 170, 170), qRgb(255, 255, 255)]
            q_img.setColorTable(color_table)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def bitDepth4(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)

            height, width, _ = image.shape
            result = np.zeros((height, width), dtype=np.uint8)
            threshold1 = 64  # Ambang batas untuk level 1
            threshold2 = 128  # Ambang batas untuk level 2
            threshold3 = 192  # Ambang batas untuk level 3
            threshold4 = 255  # Ambang batas untuk level 4

            for i in range(height):
                for j in range(width):
                    red = image[i, j, 0]
                    green = image[i, j, 1]
                    blue = image[i, j, 2]

                    # Convert RGB to grayscale using the formula (0.299*R + 0.587*G + 0.114*B)
                    grayscale = 0.299 * red + 0.587 * green + 0.114 * blue

                    # Convert to 4-bit depth based on the thresholds
                    if grayscale < threshold1:
                        result[i, j] = 0  # Level 0
                    elif grayscale < threshold2:
                        result[i, j] = 1  # Level 1
                    elif grayscale < threshold3:
                        result[i, j] = 2  # Level 2
                    elif grayscale < threshold4:
                        result[i, j] = 3  # Level 3
                    else:
                        result[i, j] = 4  # Level 4

            height1, width1 = result.shape
            q_img = QImage(result.data, width1, height1,
                           width1, QImage.Format_Indexed8)

            # Buat tabel warna untuk kedalaman bit 4
            color_table = [qRgb(0, 0, 0), qRgb(85, 85, 85), qRgb(
                170, 170, 170), qRgb(255, 255, 255)]
            q_img.setColorTable(color_table)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    # def bitDepth4(self):
    #     image_path = self.model.imgPath
    #     if image_path:
    #         image = mpimg.imread(image_path)

    #         height, width, _ = image.shape
    #         result = np.zeros((height, width), dtype=np.uint8)
    #         threshold1 = 64  # Ambang batas untuk level 1
    #         threshold2 = 128  # Ambang batas untuk level 2
    #         threshold3 = 192  # Ambang batas untuk level 3
    #         threshold4 = 255  # Ambang batas untuk level 4

    #         for i in range(height):
    #             for j in range(width):
    #                 red = image[i, j, 0]
    #                 green = image[i, j, 1]
    #                 blue = image[i, j, 2]

    #                 # Konversi RGB ke level abu-abu dengan formula sederhana
    #                 grayscale = (red + green + blue) // 3

    #                 # Convert to 4-bit depth based on the thresholds
    #                 if grayscale < threshold1:
    #                     result[i, j] = 0  # Level 0
    #                 elif grayscale < threshold2:
    #                     result[i, j] = 1  # Level 1
    #                 elif grayscale < threshold3:
    #                     result[i, j] = 2  # Level 2
    #                 elif grayscale < threshold4:
    #                     result[i, j] = 3  # Level 3

    #         height1, width1 = result.shape
    #         q_img = QImage(result.data, width1, height1, width1, QImage.Format_Indexed8)

    #         # Buat tabel warna untuk kedalaman bit 4 dengan 16 warna RGB yang berbeda
    #         color_table = [qRgb(i * 85, i * 85, i * 85) for i in range(4)]
    #         q_img.setColorTable(color_table)

    #         pixmap = QPixmap.fromImage(q_img)
    #         self.model.image_result_changed.emit(pixmap)

    def bitDepthAll(self, n_bits):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)

            height, width, _ = image.shape
            result = np.zeros((height, width), dtype=np.uint8)

            # Define thresholds and color table based on the number of bits
            if n_bits == 5:
                thresholds = [51, 102, 153, 204, 255]
                color_table = [
                    qRgb(0, 0, 0), qRgb(51, 51, 51), qRgb(102, 102, 102),
                    qRgb(153, 153, 153), qRgb(204, 204, 204)
                ]
            elif n_bits == 6:
                thresholds = [42, 85, 128, 170, 213, 255]
                color_table = [
                    qRgb(0, 0, 0), qRgb(42, 42, 42), qRgb(85, 85, 85),
                    qRgb(128, 128, 128), qRgb(
                        170, 170, 170), qRgb(213, 213, 213)
                ]
            elif n_bits == 7:
                thresholds = [36, 73, 109, 146, 182, 219, 255]
                color_table = [
                    qRgb(0, 0, 0), qRgb(36, 36, 36), qRgb(73, 73, 73),
                    qRgb(109, 109, 109), qRgb(
                        146, 146, 146), qRgb(182, 182, 182),
                    qRgb(219, 219, 219)
                ]
            else:
                raise ValueError("Unsupported number of bits")

            for i in range(height):
                for j in range(width):
                    red = image[i, j, 0]
                    green = image[i, j, 1]
                    blue = image[i, j, 2]

                    grayscale = 0.299 * red + 0.587 * green + 0.114 * blue
                    for k in range(n_bits):
                        if grayscale < thresholds[k]:
                            result[i, j] = k
                            break

            height1, width1 = result.shape
            q_img = QImage(result.data, width1, height1,
                           width1, QImage.Format_Indexed8)

            q_img.setColorTable(color_table)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def scalingUniform(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            faktorScaling = 1.5

            w = int(width * faktorScaling)
            h = int(height * faktorScaling)

            result = np.zeros((h, w, channels), dtype=np.uint8)

            for i in range(h):
                for j in range(w):
                    xOld = i / faktorScaling
                    yOld = j / faktorScaling

                    xNearest = int(round(xOld))
                    yNearest = int(round(yOld))

                    if xNearest < height and yNearest < width:
                        result[i, j] = image[xNearest, yNearest]

            q_img = QImage(
                result.data, result.shape[1], result.shape[0], result.strides[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def scalingNonUniform(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            faktorScalingx = 1.5
            faktorScalingy = 2

            w = int(width * faktorScalingx)
            h = int(height * faktorScalingy)

            result = np.zeros((h, w, channels), dtype=np.uint8)

            for i in range(h):
                for j in range(w):
                    xOld = i / faktorScalingx
                    yOld = j / faktorScalingy

                    xNearest = int(round(xOld))
                    yNearest = int(round(yOld))

                    if xNearest < height and yNearest < width:
                        result[i, j] = image[xNearest, yNearest]

            q_img = QImage(
                result.data, result.shape[1], result.shape[0], result.strides[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def gaussianBlur(self, kernel_size):
        image_path = self.model.imgPath
        if image_path:

            image = mpimg.imread(image_path)

            kernel = np.fromfunction(
                lambda x, y: (1 / (2 * np.pi * (kernel_size**2))) *
                np.exp(- ((x - (kernel_size//2))**2 +
                       (y - (kernel_size//2))**2) / (2 * (kernel_size**2))),
                (kernel_size, kernel_size)
            )
            kernel /= np.sum(kernel)

            """
            hasil kernel untuk 3 x 3    
            121
            242
            121
            """

            blurred_image = np.zeros_like(image, dtype=np.float32)
            image_padded = np.pad(image, [(
                kernel_size//2, kernel_size//2), (kernel_size//2, kernel_size//2), (0, 0)], mode='constant')

            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    for c in range(image.shape[2]):
                        blurred_image[i, j, c] = np.sum(
                            kernel * image_padded[i:i+kernel_size, j:j+kernel_size, c])

            blurred_image = blurred_image.astype(np.uint8)

            height1, width1, _ = blurred_image.shape

            q_img = QImage(blurred_image.data, width1, height1,
                           blurred_image.strides[0], QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def translasi(self, Tx, Ty):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            Tx = int(Tx)
            Ty = int(Ty)
            height, width, _ = image.shape
            result = np.zeros((height, width, 3), dtype=np.uint8)

            for y in range(height):
                for x in range(width):
                    x_new = x + Tx
                    y_new = y + Ty

                    if 0 <= x_new < width and 0 <= y_new < height:
                        result[y_new, x_new, :] = image[y, x, :]
                    else:
                        result[y, x, :] = [0, 0, 0]
            q_img = QImage(
                result.data, result.shape[1], result.shape[0], result.strides[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def Crop(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            indices = self.model.getIndexSelected()
            xL = indices[0][0]
            xR = indices[1][0]
            yT = indices[0][1]
            yB = indices[1][1]

            # Crop the image based on the selected indices
            cropped_image = image[yT:yB, xL:xR]

            # Create a QImage from the cropped image
            height, width, channel = cropped_image.shape
            bytes_per_line = 3 * width
            q_img = QImage(
                # Menggunakan .tobytes() untuk mengambil data sebagai bytes
                cropped_image.data.tobytes(),
                width, height, bytes_per_line,
                QImage.Format_RGB888
            )

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)
            self.model.setIndexSlectedToNull()

    def rotasi(self, degree):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, _ = image.shape
            center_x, center_y = width // 2, height // 2
            result = np.zeros((height, width, 3), dtype=np.uint8)
            radians = math.radians(degree)
            for y in range(height):
                for x in range(width):
                    new_x = int((x - center_x) * math.cos(radians) -
                                (y - center_y) * math.sin(radians)) + center_x
                    new_y = int((x - center_x) * math.sin(radians) +
                                (y - center_y) * math.cos(radians)) + center_y
                    if 0 <= new_x < width and 0 <= new_y < height:
                        result[y, x] = image[new_y, new_x]

            q_img = QImage(
                result.data, result.shape[1], result.shape[0], result.strides[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def fuzzyHistogram(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            gray = np.zeros((height, width), dtype=np.uint8)
            dark = {"a": 0, "b": 63, "c": 127}
            grey = {"a": 63, "b": 127, "c": 191}
            light = {"a": 127, "b": 191, "c": 255}

            for i in range(height):
                for j in range(width):
                    value = (0.299 * image[i, j, 0]) + (0.587 *
                                                        image[i, j, 1]) + (0.144 * image[i, j, 2])
                    fuzzy1 = None
                    fuzzy2 = None
                    if 63 <= value <= 127:
                        fuzzy1 = (value - grey["a"])/(grey["b"] - grey["a"])
                        fuzzy2 = -(value - dark["a"])/(dark["a"] - dark["b"])
                        gray[i, j] = self.defuzification(
                            fuzzy1, "grey", fuzzy2, "dark")
                    elif 128 < value < 191:
                        fuzzy1 = (value - grey["b"])/(grey["c"] - grey["b"])
                        fuzzy2 = -(value - grey["c"])/(grey["c"] - light["a"])
                        gray[i, j] = self.defuzification(
                            fuzzy1, "light", fuzzy2, "grey")
                    elif value < 63:
                        fuzzy1 = value / dark["b"]
                        gray[i, j] = self.defuzification(
                            fuzzy1, "dark")
                    elif value > 191:
                        fuzzy1 = (value - light["b"]) / (255 - light["b"])
                        gray[i, j] = self.defuzification(
                            fuzzy1, "light")
                    else:
                        gray[i, j] = value

            hist_before = np.histogram(
                image.ravel(), bins=256, range=(0, 256))[0]
            hist_after = np.histogram(
                gray.ravel(), bins=256, range=(0, 256))[0]

            self.model.setHistogramBefore(hist_before)
            self.model.setHistogramAfter(hist_after)
            # # Plot histogram sebelum dan sesudah
            # plt.subplot(1, 2, 1)
            # plt.plot(hist_before)
            # plt.title("Histogram Sebelum Fuzzy")

            # plt.subplot(1, 2, 2)
            # plt.plot(hist_after)
            # plt.title("Histogram Setelah Fuzzy")

            # plt.show()

            height, width = gray.shape
            bytes_per_line = width
            q_img = QImage(gray.data, width, height,
                           bytes_per_line, QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def fuzzyHistogramRGB(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            gray = np.zeros((height, width, channels), dtype=np.uint8)
            dark = {"a": 0, "b": 63, "c": 127}
            grey = {"a": 63, "b": 127, "c": 191}
            light = {"a": 127, "b": 191, "c": 255}

            for i in range(height):
                for j in range(width):
                    for l in range(channels):
                        value = image[i, j, l]
                        fuzzy1 = None
                        fuzzy2 = None
                        if 63 <= value <= 127:
                            fuzzy1 = (value - grey["a"]) / \
                                (grey["b"] - grey["a"])
                            fuzzy2 = -(value - dark["a"]) / \
                                (dark["a"] - dark["b"])
                            gray[i, j, l] = self.defuzification(
                                fuzzy1, "grey", fuzzy2, "dark")
                        elif 128 < value < 191:
                            fuzzy1 = (value - grey["b"]) / \
                                (grey["c"] - grey["b"])
                            fuzzy2 = -(value - grey["c"]) / \
                                (grey["c"] - light["a"])
                            gray[i, j, l] = self.defuzification(
                                fuzzy1, "light", fuzzy2, "grey")
                        elif value < 63:
                            fuzzy1 = value / dark["b"]
                            gray[i, j, l] = self.defuzification(
                                fuzzy1, "dark")
                        elif value > 191:
                            fuzzy1 = (value - light["b"]) / \
                                (light["c"] - light["b"])
                            gray[i, j, l] = self.defuzification(
                                fuzzy1, "light")
                        else:
                            gray[i, j, l] = value
                    print(gray[i, j])

            hist_before = np.histogram(
                image.ravel(), bins=256, range=(0, 256))[0]
            hist_after = np.histogram(
                gray.ravel(), bins=256, range=(0, 256))[0]

            self.model.setHistogramBefore(hist_before)
            self.model.setHistogramAfter(hist_after)

            q_img = QImage(
                gray.data, gray.shape[1], gray.shape[0], gray.strides[0], QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def defuzification(self, fuzzy1, fuzzy1Role, fuzzy2=None, fuzzy2Role=None):
        role = {"dark": 0, "grey": 127, "light": 255}
        if fuzzy1Role == "dark" and fuzzy2 == None and fuzzy2Role == None:
            v0 = fuzzy1 * role[fuzzy1Role]
            return v0
        elif fuzzy1Role == "light" and fuzzy2 == None and fuzzy2Role == None:
            v0 = (fuzzy1 * role[fuzzy1Role])/fuzzy1
            return v0 if v0 <= 255 else 255.0
        v0 = (fuzzy1 * role[fuzzy1Role] + fuzzy2 *
              role[fuzzy2Role])/(fuzzy1 + fuzzy2)
        return v0

    def histogramInput(self):
        before = self.model.getHistogramBefore()

        plt.figure(figsize=(6, 4))
        plt.bar(range(len(before)), before)
        plt.title("Histogram Sebelum")

        plt.show()

    def histogramOutput(self):
        after = self.model.getHistogramAfter()

        plt.figure(figsize=(6, 4))
        plt.bar(range(len(after)), after)
        plt.title("Histogram Setelah")

        plt.show()

    def histogramInputOutput(self):
        before = self.model.getHistogramBefore()
        after = self.model.getHistogramAfter()

        plt.figure(figsize=(12, 4))

        plt.subplot(1, 2, 1)
        plt.bar(range(len(before)), before)
        plt.title("Histogram Sebelum")

        plt.subplot(1, 2, 2)
        plt.bar(range(len(after)), after)
        plt.title("Histogram Setelah")

        plt.show()

    def grayscaleValue(self, arr):
        value = (0.299 * arr[0]) + (0.587 * arr[1]) + (0.144 * arr[2])
        return value

    def lowPass(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            result = np.zeros((height, width), dtype=np.uint8)

            # kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
            kernel = np.array(
                [[1/16, 1/8, 1/16], [1/8, 1/4, 1/8], [1/16, 1/8, 1/16]])
            # kernel = np.array([[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]])
            m, n = kernel.shape
            for i in range(height):
                if i + 2 >= height:
                    break
                for j in range(width):
                    if j + 2 >= width:
                        break
                    total = 0
                    for m in range(3):
                        for n in range(3):
                            total = total + \
                                (self.grayscaleValue(
                                    image[i+m, j+n]) * kernel[m, n])
                    # np.clip(total, 0, 255)
                    result[i+1, j+1] = np.clip(total/np.sum(kernel), 0, 255)

            heightR, widthR = result.shape
            bytes_per_line = widthR
            q_img = QImage(result.data, widthR, heightR,
                           bytes_per_line, QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def highPass(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            result = np.zeros((height, width), dtype=np.uint8)

            # kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
            # kernel = np.array([[1/16, 1/8, 1/16], [1/8, 1/4, 1/8], [1/16, 1/8, 1/16]])
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            m, n = kernel.shape
            for i in range(height):
                if i + 2 >= height:
                    break
                for j in range(width):
                    if j + 2 >= width:
                        break
                    total = 0
                    for m in range(3):
                        for n in range(3):
                            total = total + \
                                (self.grayscaleValue(
                                    image[i+m, j+n]) * kernel[m, n])
                    result[i+1, j+1] = np.clip(total/np.sum(kernel), 0, 255)

            heightR, widthR = result.shape
            bytes_per_line = widthR
            q_img = QImage(result.data, widthR, heightR,
                           bytes_per_line, QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def indetityFilter(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            result = np.zeros((height, width, channels), dtype=np.uint8)

            kernel = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
            m, n = kernel.shape
            for c in range(channels):
                for i in range(height):
                    if i + 2 >= height:
                        break
                    for j in range(width):
                        if j + 2 >= width:
                            break
                        total = 0
                        for m in range(3):
                            for n in range(3):
                                total += image[i + m, j + n, c] * kernel[m, n]
                        result[i + 1, j + 1, c] = np.clip(total, 0, 255)

            heightR, widthR, channelsR = result.shape
            bytes_per_line = widthR
            q_img = QImage(result.data, widthR, heightR,
                           3 * bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def sharpenFilter(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            result = np.zeros((height, width, channels), dtype=np.uint8)

            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            m, n = kernel.shape
            for c in range(channels):
                for i in range(height):
                    if i + 2 >= height:
                        break
                    for j in range(width):
                        if j + 2 >= width:
                            break
                        total = 0
                        for m in range(3):
                            for n in range(3):
                                total += image[i + m, j + n, c] * kernel[m, n]
                        result[i + 1, j + 1, c] = np.clip(total, 0, 255)

            heightR, widthR, channelsR = result.shape
            bytes_per_line = widthR
            q_img = QImage(result.data, widthR, heightR,
                           3 * bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def unsharpMaskFilter(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            result = np.zeros((height, width, channels), dtype=np.uint8)

            kernel = np.array([[1, 4, 6, 4, 1], [4, 16, 24, 16, 4], [
                              6, 24, 36, 24, 6], [4, 16, 24, 16, 4], [1, 4, 6, 4, 1]])
            m, n = kernel.shape
            border = m // 2  # berfungsi untuk menjaga agar kernel tidak keluar
            for c in range(channels):
                for i in range(border, height - border):
                    for j in range(border, width - border):
                        total = 0
                        for x in range(m):
                            for y in range(n):
                                total += image[i - border + x,
                                               j - border + y, c] * kernel[x, y]
                        result[i, j, c] = np.clip(total // 256, 0, 255)

            heightR, widthR, channelsR = result.shape
            bytes_per_line = channelsR * widthR
            q_img = QImage(result.data, widthR, heightR,
                           bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def sobel(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            result = np.zeros((height, width), dtype=np.uint8)

            kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

            kernel = np.rot90(kernel, 2)  # Memutar kernel 180 derajat

            for i in range(height):
                if i + 2 >= height:
                    break
                for j in range(width):
                    if j + 2 >= width:
                        break
                    total = 0
                    for m_idx in range(3):
                        for n_idx in range(3):
                            total += (self.grayscaleValue(
                                image[i + m_idx, j + n_idx]) * kernel[m_idx, n_idx])
                    result[i + 1, j + 1] = np.clip(total, 0, 255)

            heightR, widthR = result.shape
            bytes_per_line = widthR
            q_img = QImage(result.data, widthR, heightR,
                           bytes_per_line, QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def prewit(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            result = np.zeros((height, width), dtype=np.uint8)

            kernel = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])

            kernel = np.rot90(kernel, 2)  # Memutar kernel 180 derajat

            for i in range(height):
                if i + 2 >= height:
                    break
                for j in range(width):
                    if j + 2 >= width:
                        break
                    total = 0
                    for m_idx in range(3):
                        for n_idx in range(3):
                            total += (self.grayscaleValue(
                                image[i + m_idx, j + n_idx]) * kernel[m_idx, n_idx])
                    result[i + 1, j + 1] = np.clip(total, 0, 255)

            heightR, widthR = result.shape
            bytes_per_line = widthR
            q_img = QImage(result.data, widthR, heightR,
                           bytes_per_line, QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    def edgeDetectionRobert(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            result = np.zeros((height, width), dtype=np.uint8)

            kernel = np.array([[-1, 0], [0, 1]])

            for i in range(height):
                if i + 1 >= height:
                    break
                for j in range(width):
                    if j + 1 >= width:
                        break
                    total = 0
                    for m in range(2):
                        for n in range(2):
                            total += (self.grayscaleValue(
                                image[i + m, j + n]) * kernel[m, n])
                    result[i, j] = np.clip(total, 0, 255)

            heightR, widthR = result.shape
            bytes_per_line = widthR
            q_img = QImage(result.data, widthR, heightR,
                           bytes_per_line, QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)
            self.model.image_result_changed.emit(pixmap)

    # def morfologiDilasi(self, kernelType):
    #     image_path = self.model.imgPath
    #     if image_path:
    #         image = mpimg.imread(image_path)
    #         height, width, channels = image.shape

    #         # Buat gambar baru untuk menyimpan hasil dilasi
    #         dilated_image = np.zeros((height, width), dtype=np.uint8)

    #         # Pilih kernel berdasarkan jenis kernel
    #         if kernelType == "cross":
    #             kernel = np.array([[0, 1, 0],
    #                             [1, 1, 1],
    #                             [0, 1, 0]], dtype=np.uint8)
    #         elif kernelType == "square3":
    #             kernel = np.array([[1, 1, 1],
    #                             [1, 1, 1],
    #                             [1, 1, 1]], dtype=np.uint8)
    #         elif kernelType == "square5":
    #             kernel = np.array([[0, 1, 1, 1, 0],
    #                             [1, 1, 1, 1, 1],
    #                             [1, 1, 1, 1, 1],
    #                             [1, 1, 1, 1, 1],
    #                             [0, 1, 1, 1, 0]], dtype=np.uint8)

    #         kernel_height, kernel_width = kernel.shape

    #         for y in range(height):
    #             for x in range(width):
    #                 max_pixel_value = 0
    #                 for ky in range(kernel_height):
    #                     for kx in range(kernel_width):
    #                         img_y = y + ky - (kernel_height // 2)
    #                         img_x = x + kx - (kernel_width // 2)

    #                         if 0 <= img_y < height and 0 <= img_x < width:
    #                             max_pixel_value = max(
    #                                 max_pixel_value, kernel[ky, kx] * image[img_y, img_x])

    #                 dilated_image[y, x] = max_pixel_value

    #         # Konversi hasil dilasi ke tipe data yang benar untuk ditampilkan
    #         dilated_image = (dilated_image * 255).astype(np.uint8)

    #         heightR, widthR = dilated_image.shape
    #         bytes_per_line = widthR
    #         q_img = QImage(dilated_image.data, widthR, heightR,
    #                     bytes_per_line, QImage.Format_Grayscale8)

    #         pixmap = QPixmap.fromImage(q_img)
    #         self.model.image_result_changed.emit(pixmap)

    def binary_threshold(self, image):
        threshold_value = 128
        thresholded_image = np.zeros_like(image)

        thresholded_image[image <= threshold_value] = 255

        return thresholded_image

    def dilasi(self, image, kernel):
        height, width = image.shape
        result = np.zeros((height, width), dtype=np.uint8)
        k_height, k_width = kernel.shape

        pad_height = k_height // 2
        pad_width = k_width // 2

        # Melakukan padding pada citra dengan nilai nol
        padded_image = np.pad(
            image, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')

        for i in range(pad_height, height + pad_height):
            for j in range(pad_width, width + pad_width):
                result[i - pad_height, j - pad_width] = np.max(
                    padded_image[i - pad_height:i + pad_height + 1, j - pad_width:j + pad_width + 1] * kernel)

        return result

    def morfologiDilasi(self, kernel_type='square3'):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape

            if kernel_type == 'square3':
                kernel = np.array([[1, 1, 1],
                                   [1, 1, 1],
                                   [1, 1, 1]], dtype=np.uint8)
            elif kernel_type == 'square5':
                kernel = np.array([[1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1]], dtype=np.uint8)
            elif kernel_type == 'cross3':
                kernel = np.array([[0, 1, 0],
                                   [1, 1, 1],
                                   [0, 1, 0]], dtype=np.uint8)
            else:
                raise ValueError("Kernel type not recognized.")

            gray_image = np.zeros((height, width), dtype=np.uint8)
            for i in range(height):
                for j in range(width):
                    gray_image[i, j] = self.grayscaleValue(image[i, j])

            result = self.binary_threshold(result)
            result = self.dilasi(gray_image, kernel)

            q_image = QImage(
                result.data, result.shape[1], result.shape[0], result.strides[0], QImage.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_image)
            self.model.image_result_changed.emit(pixmap)

    def erosi(self, image, kernel):
        height, width = image.shape
        result = np.zeros((height, width), dtype=np.uint8)
        k_height, k_width = kernel.shape

        pad_height = k_height // 2
        pad_width = k_width // 2

        padded_image = np.pad(
            image, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')

        for i in range(pad_height, height + pad_height):
            for j in range(pad_width, width + pad_width):
                result[i - pad_height, j - pad_width] = np.min(
                    padded_image[i - pad_height:i + pad_height + 1, j - pad_width:j + pad_width + 1] * kernel)

        return result

    def morfologiErosi(self, kernel_type='square3'):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape

            if kernel_type == 'square3':
                kernel = np.array([[1, 1, 1],
                                   [1, 1, 1],
                                   [1, 1, 1]], dtype=np.uint8)
            elif kernel_type == 'square5':
                kernel = np.array([[1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1]], dtype=np.uint8)
            elif kernel_type == 'cross3':
                kernel = np.array([[0, 1, 0],
                                   [1, 1, 1],
                                   [0, 1, 0]], dtype=np.uint8)
            else:
                raise ValueError("Kernel type not recognized.")

            gray_image = np.zeros((height, width), dtype=np.uint8)
            for i in range(height):
                for j in range(width):
                    gray_image[i, j] = self.grayscaleValue(image[i, j])

            result = self.binary_threshold(gray_image)
            result = self.erosi(result, kernel)

            q_image = QImage(
                result.data, result.shape[1], result.shape[0], result.strides[0], QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.model.image_result_changed.emit(pixmap)

    def opening(self, image, kernel):
        eroded_image = self.erosi(image, kernel)
        opened_image = self.dilasi(eroded_image, kernel)
        return opened_image

    def morfologiOpening(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            kernel = np.ones((9, 9), dtype=np.uint8)

            gray_image = np.zeros((height, width), dtype=np.uint8)
            for i in range(height):
                for j in range(width):
                    gray_image[i, j] = self.grayscaleValue(image[i, j])

            # Menggunakan fungsi morfologiOpening
            result = self.opening(gray_image, kernel)
            result = self.binary_threshold(result)

            q_image = QImage(
                result.data, result.shape[1], result.shape[0], result.strides[0], QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.model.image_result_changed.emit(pixmap)

    def closing(self, image, kernel):
        dilated_image = self.dilasi(image, kernel)
        closed_image = self.erosi(dilated_image, kernel)
        return closed_image

    def morfologiClosing(self):
        image_path = self.model.imgPath
        if image_path:
            image = mpimg.imread(image_path)
            height, width, channels = image.shape
            kernel = np.ones((9, 9), dtype=np.uint8)

            gray_image = np.zeros((height, width), dtype=np.uint8)
            for i in range(height):
                for j in range(width):
                    gray_image[i, j] = self.grayscaleValue(image[i, j])

            # Menggunakan fungsi morfologiOpening
            result = self.closing(gray_image, kernel)
            result = self.binary_threshold(result)

            q_image = QImage(
                result.data, result.shape[1], result.shape[0], result.strides[0], QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)
            self.model.image_result_changed.emit(pixmap)

    def segmentROI(self):
        image_path = self.model.imgPath
        if image_path:
            image = cv2.imread(image_path)
            if image is None:
                return

            # Konversi gambar ke mode warna HSV
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            self.upper_hue = 120
            self.upper_saturation = 255
            self.upper_value = 255

            self.lower_hue = 90
            self.lower_saturation = 0
            self.lower_value = 90
            lower = np.array(
                [self.lower_hue, self.lower_saturation, self.lower_value])
            upper = np.array(
                [self.upper_hue, self.upper_saturation, self.upper_value])

            mask = cv2.inRange(hsv_image, lower, upper)

            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            image_with_contours = image.copy()
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image_with_contours, (x, y),
                              (x + w, y + h), (255, 0, 0), 2)

            height, width, channel = image_with_contours.shape
            bytes_per_line = 3 * width
            q_image = QImage(image_with_contours.data, width,
                             height, bytes_per_line, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(q_image)

            self.model.image_result_changed.emit(pixmap)

    # def rgbToHsv(self):
    #     image_path = self.model.imgPath
    #     if image_path:
    #         image = mpimg.imread(image_path)
    #         image = image / 255.0

    #         # Convert RGB to HSV
    #         image_hsv = np.array([colorsys.rgb_to_hsv(
    #             pixel[0], pixel[1], pixel[2]) for pixel in image.reshape(-1, 3)])

    #         # Reshape the resulting array back to the original image shape
    #         image_hsv = image_hsv.reshape(image.shape)

    #         # Convert HSV to RGB
    #         image_rgb = np.array([colorsys.hsv_to_rgb(
    #             pixel[0], pixel[1], pixel[2]) for pixel in image_hsv.reshape(-1, 3)])

    #         # Reshape the resulting array back to the original image shape
    #         image_rgb = image_rgb.reshape(image.shape)

    #         # Convert to QImage
    #         h, w, _ = image_rgb.shape
    #         q_image = QImage(image_rgb.data, w, h, 3 * w, QImage.Format_RGB888)

    #         # Create QPixmap from QImage
    #         pixmap = QPixmap.fromImage(q_image)

    #         self.model.image_result_changed.emit(pixmap)

    def rgbToHsv(self):
        image_path = self.model.imgPath
        if image_path:
            image = cv2.imread(image_path)
            if image is None:
                return

            # Mengambil channel R, G, dan B dari gambar
            R, G, B = image[:, :, 2], image[:, :, 1], image[:, :, 0]

            # Hitung nilai V (Value)
            V = np.maximum(R, np.maximum(G, B))
            Vm = V - np.minimum(R, np.minimum(G, B))

            # Inisialisasi matriks S (Saturation)
            S = np.zeros_like(V)

            # Hitung nilai S (Saturation) hanya pada piksel dengan V > 0
            nonzero_v = V > 0
            S[nonzero_v] = Vm[nonzero_v] / V[nonzero_v]

            # Inisialisasi matriks H (Hue)
            H = np.zeros_like(V)

            # Hitung nilai H (Hue) hanya pada piksel dengan V > 0
            nonzero_v = V > 0
            R_normalized = (V - R)[nonzero_v] / Vm[nonzero_v]
            G_normalized = (V - G)[nonzero_v] / Vm[nonzero_v]
            B_normalized = (V - B)[nonzero_v] / Vm[nonzero_v]

            H[nonzero_v] = np.where(V[nonzero_v] == R[nonzero_v], 60 * (2 + B_normalized - G_normalized), H[nonzero_v])
            H[nonzero_v] = np.where(V[nonzero_v] == G[nonzero_v], 60 * (4 + R_normalized - B_normalized), H[nonzero_v])
            H[nonzero_v] = np.where(V[nonzero_v] == B[nonzero_v], 60 * (G_normalized - R_normalized), H[nonzero_v])

            # Konversi H, S, V ke rentang 0-255
            H = (H / 360.0) * 255.0
            S = S * 255.0
            V = (V / 255.0) * 255.0

            # Gabungkan H, S, V kembali menjadi gambar RGB
            result_image = cv2.merge([H, S, V]).astype(np.uint8)

            # Konversi hasil kembali ke QImage
            h, w, c = result_image.shape
            bytes_per_line = 3 * w
            qimage_result = QtGui.QImage(
                result_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(qimage_result)
            self.model.image_result_changed.emit(pixmap)

    # def rgbToYCrCb(self):
    #     image_path = self.model.imgPath
    #     if image_path:
    #         # Membaca gambar
    #         image = cv2.imread(image_path)

    #         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #         # Mengonversi RGB ke YCrCb
    #         image_ycrcb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2YCrCb)

    #         h, w, _ = image_rgb.shape
    #         bytes_per_line = 3 * w
    #         q_image = QImage(image_ycrcb.data, w, h,
    #                          bytes_per_line, QImage.Format_RGB888)
    #         pixmap = QPixmap.fromImage(q_image)
    #         self.model.image_result_changed.emit(pixmap)

    def rgbToYCrCb(self):
        image_path = self.model.imgPath
        if image_path:
            image = cv2.imread(image_path)

            ycbcr_image = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)

            # Ekstrak komponen Y, Cb, dan Cr
            Y = ycbcr_image[:, :, 0]
            Cb = ycbcr_image[:, :, 1]
            Cr = ycbcr_image[:, :, 2]

            # Konversi hasil kembali ke QImage
            h, w = Y.shape
            ycbcr_result = cv2.merge([Y, Cb, Cr])
            bytes_per_line = 3 * w
            qimage_result = QtGui.QImage(
                ycbcr_result.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
            )

            pixmap = QPixmap.fromImage(qimage_result)
            self.model.image_result_changed.emit(pixmap)

    def removeBg(self):
        image_path = self.model.imgPath
        if image_path:
            input = cv2.imread(image_path)
            output = remove(input)
            pixmap = QPixmap.fromImage(output)
            self.model.image_result_changed.emit(pixmap)

    def SegmentasiCitra(self):
        image_path = self.model.imgPath
        if image_path:
            input_image = mpimg.imread(image_path)

            # Mendapatkan lebar dan tinggi cipixmaptra
            width = input_image.width()
            height = input_image.height()

            # Buat citra segmen yang memiliki ukuran yang sama dengan citra asli
            segmented_image = QImage(width, height, QImage.Format_ARGB32)

            # Tentukan batas warna (lower_color dan upper_color) untuk segmentasi
            lower_color = QColor(100, 0, 0)
            upper_color = QColor(255, 100, 100)

            # Looping melalui setiap pixel dalam citra
            for y in range(height):
                for x in range(width):
                    pixel_color = input_image.pixelColor(x, y)
                    r, g, b = pixel_color.red(), pixel_color.green(), pixel_color.blue()

                    # Cek apakah nilai warna pixel berada dalam rentang yang ditentukan
                    if (lower_color.red() <= r <= upper_color.red() and
                        lower_color.green() <= g <= upper_color.green() and
                            lower_color.blue() <= b <= upper_color.blue()):
                        # Jika dalam rentang, set pixel menjadi merah (255, 0, 0)
                        segmented_image.setPixel(x, y, qRgb(255, 0, 0))
                    else:
                        # Jika tidak dalam rentang, set pixel menjadi hitam (0, 0, 0)
                        segmented_image.setPixel(x, y, qRgb(0, 0, 0))

            # Output citra segmen
            segmented_pixmap = QPixmap.fromImage(segmented_image)
            self.model.image_result_changed.emit(segmented_pixmap)

    def SegmentasiCitra(self):
        image_path = self.model.imgPath
        if image_path:
            input_image = QImage(image_path)

            # Mendapatkan lebar dan tinggi citra
            width = input_image.width()
            height = input_image.height()

            # Buat citra segmen yang memiliki ukuran yang sama dengan citra asli
            segmented_image = QImage(width, height, QImage.Format_ARGB32)

            # Tentukan batas warna (lower_color dan upper_color) untuk segmentasi
            lower_color = QColor(100, 0, 0)
            upper_color = QColor(255, 100, 100)

            # Looping melalui setiap pixel dalam citra
            for y in range(height):
                for x in range(width):
                    pixel_color = QColor(input_image.pixel(x, y))
                    r, g, b = pixel_color.red(), pixel_color.green(), pixel_color.blue()

                    # Cek apakah nilai warna pixel berada dalam rentang yang ditentukan
                    if (lower_color.red() <= r <= upper_color.red() and
                        lower_color.green() <= g <= upper_color.green() and
                        lower_color.blue() <= b <= upper_color.blue()):
                        # Jika dalam rentang, set pixel menjadi merah (255, 0, 0)
                        segmented_image.setPixelColor(x, y, QColor(255, 0, 0))
                    else:
                        # Jika tidak dalam rentang, set pixel menjadi hitam (0, 0, 0)
                        segmented_image.setPixelColor(x, y, QColor(0, 0, 0))

            # Output citra segmen
            segmented_pixmap = QPixmap.fromImage(segmented_image)
            self.model.image_result_changed.emit(segmented_pixmap)