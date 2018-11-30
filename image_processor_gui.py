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

        self.username = ""
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.orig_image = QLabel("")
        self.proc_image = QLabel("")

        self.entered_username = QLineEdit()
        self.proc_box = QComboBox(self)
        self.download_box = QComboBox(self)

        self.addTab(self.tab1, "Specify User")
        self.addTab(self.tab2, "Process Image")
        self.setTabEnabled(1, False)
        self.tab1UI()
        self.tab2UI()

        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Image Processor Control')

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow("Username", self.entered_username)
        enter_button = QHBoxLayout()
        user_button = QPushButton("Enter")
        user_button.setToolTip("Enter username")
        user_button.clicked.connect(self.update_username)
        enter_button.addWidget(user_button)
        layout.addRow(enter_button)
        self.tab1.setLayout(layout)

    def tab2UI(self):

        tab2layout = QGridLayout()

        open_button = QPushButton('Open image', self)
        open_button.setToolTip('Choose image file(s) to process')
        open_button.clicked.connect(self.file_select_button)
        tab2layout.addWidget(open_button, 0, 0)

        self.proc_box.setEditable(True)
        self.proc_box.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.proc_box.lineEdit().setReadOnly(True)
        self.proc_box.addItems(["Histogram Equalization", "Contrast Stretching",
                      "Log Compression", "Reverse Video"])
        tab2layout.addWidget(self.proc_box, 1, 0)

        self.download_box.setEditable(True)
        self.download_box.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.download_box.lineEdit().setReadOnly(True)
        self.download_box.addItems([".JPG", ".PNG", ".TIFF"])
        tab2layout.addWidget(self.download_box, 0, 3)

        download_button = QPushButton('Download', self)
        download_button.setToolTip('Hit Button to download image in selected format')
        download_button.clicked.connect(self.download_image)
        tab2layout.addWidget(download_button, 1, 3)

        processor_button = QPushButton('Process', self)
        processor_button.setToolTip('Hit Button to Send Image to Server for Processing')
        processor_button.clicked.connect(self.process_button)
        tab2layout.addWidget(processor_button, 2, 0)

        orig_image_box = QGroupBox("Original Image")
        orig_image_layout = QHBoxLayout()
        orig_image_layout.addWidget(self.orig_image)
        orig_image_box.setLayout(orig_image_layout)
        tab2layout.addWidget(orig_image_box, 3, 0, 2, 2)

        proc_image_box = QGroupBox("Processed Image")
        proc_image_layout = QHBoxLayout()
        proc_image_layout.addWidget(self.proc_image)
        proc_image_box.setLayout(proc_image_layout)

        tab2layout.addWidget(proc_image_box, 3, 2, 2, 2)

        self.tab2.setLayout(tab2layout)

    def download_image(self):
        """Download image
        """

    def update_username(self):
        self.username = self.entered_username.text
        self.setTabEnabled(1, True)
        self.setCurrentIndex(1)

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
            self.insert_orig_image(fn)

    def insert_orig_image(self, fn):
        input_image = imread(fn[0])
        height, width, channels = input_image.shape
        bytesPerLine = channels * width
        qImg = QtGui.QImage(input_image.data, width, height,
                            bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap01 = QtGui.QPixmap.fromImage(qImg)
        pixmap_image = QtGui.QPixmap(pixmap01)
        pixmap_image_scaled = pixmap_image.scaledToHeight(240)
        self.orig_image.setPixmap(pixmap_image_scaled)
        self.orig_image.setAlignment(QtCore.Qt.AlignCenter)
        self.orig_image.setScaledContents(True)
        self.orig_image.setMinimumSize(1, 1)
        self.orig_image.show()

    def process_button(self):
        self.process_server()

    def process_server(self):
        images_base64 = []
        process = self.proc_box.currentText()
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