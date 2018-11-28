from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QFileDialog, QComboBox, QLabel
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
from matplotlib.pyplot import imread

import sys


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Image Processor Control'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('Open image', self)
        button.setToolTip('Choose image file(s) to process')
        button.move(0, 0)
        button.clicked.connect(self.file_select_button)

        box = QComboBox(self)
        box.addItems(["Histogram Equalization", "Contrast Stretching",
                      "Log Compression", "Reverse Video"])
        box.move(0, 30)

        self.show()

    @pyqtSlot()
    def file_select_button(self):
        self.openFileNamesDialog()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fn, _ = QFileDialog.getOpenFileNames(self, "Select Image File(s)", "",
                                             "JPEG (*.JPEG *.jpeg *.JPG "
                                             "*.jpg *.JPE *.jpe "
                                             "*JFIF *.jfif);; "
                                             "PNG (*.PNG *.png);; "
                                             "GIF (*.GIF *.gif);; "
                                             "Bitmap Files (*.BMP *.bmp"
                                             " *.DIB *.dib);;"
                                             " TIFF (*.TIF *.tif *.TIFF "
                                             "*.tiff);; ICO (*.ICO *.ico)",
                                             options=options)
        if fn:
            input_image = imread(fn[0])
            height, width, channels = input_image.shape
            bytesPerLine = channels * width
            qImg = QtGui.QImage(input_image.data, width, height,
                                bytesPerLine, QtGui.QImage.Format_RGB888)
            pixmap01 = QtGui.QPixmap.fromImage(qImg)
            pixmap_image = QtGui.QPixmap(pixmap01)
            pixmap_image_scaled = pixmap_image.scaledToHeight(240)
            label_imageDisplay = QLabel(self)
            label_imageDisplay.setPixmap(pixmap_image_scaled)
            label_imageDisplay.setAlignment(QtCore.Qt.AlignCenter)
            label_imageDisplay.setScaledContents(True)
            label_imageDisplay.setMinimumSize(1, 1)
            label_imageDisplay.move(100, 100)
            label_imageDisplay.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
