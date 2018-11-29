from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
from matplotlib.pyplot import imread
import base64
import sys
import requests


class App(QTabWidget):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.tab1UI()
        self.tab2UI()

        self.title = 'Image Processor Control'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow("Username", QLineEdit())
        enter_button = QHBoxLayout()
        button = QPushButton("Enter")
        button.setToolTip("Enter username")
        enter_button.addWidget(button)
        layout.addRow(enter_button)
        self.setTabText(0, "Specify User")
        self.tab1.setLayout(layout)

    def tab2UI(self):

        layout = QGridLayout()

        open_button = QPushButton('Open image', self)
        open_button.setToolTip('Choose image file(s) to process')
        open_button.clicked.connect(self.file_select_button)
        layout.addWidget(open_button, 1, 0)

        global box
        box = QComboBox(self)
        box.addItems(["Histogram Equalization", "Contrast Stretching",
                      "Log Compression", "Reverse Video"])
        layout.addWidget(box, 2, 0)

        processor_button = QPushButton('Process', self)
        processor_button.setToolTip('Hit Button to Send Image to Server for Processing')
        processor_button.clicked.connect(self.process_button)
        layout.addWidget(processor_button, 3, 0)
        self.tab2.setLayout(layout)
        self.setTabText(1, "Process Image")

    @pyqtSlot()
    def file_select_button(self):
        self.openFileNamesDialog()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global fn
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
            label_imageDisplay.move(150, 100)
            label_imageDisplay.show()

    def process_button(self):
        self.process_server()

    def process_server(self):
        images_base64 = []
        process = box.currentText()
        for x in range(len(fn)):
            input_image = imread(fn[x])
            image_base64 = base64.b64encode(input_image)
            base64_string = image_base64.decode('ascii')
            images_base64.append(base64_string)
        r2 = requests.post("http://0.0.0.0:5000/upload", json={
            "Images": images_base64,
            "Process": process,
        })
        print(r2.text)


def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()