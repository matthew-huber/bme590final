from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
from matplotlib.pyplot import imread
import base64
import sys
import requests
from datetime import datetime
import zipfile
import os
import time
import ast
import matplotlib.image as mpimg
import io


class App(QTabWidget):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        self.username = ""
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.orig_image = QLabel("")
        self.proc_image = QLabel("")

        self.entered_username = QLineEdit()
        self.procbox = QComboBox(self)
        self.download_box = QComboBox(self)
        self.orig_next_button = QPushButton('Next Image >>')
        self.orig_prev_button = QPushButton('<< Prev Image')
        self.download_button = QPushButton('Download', self)
        self.processor_button = QPushButton('Process', self)

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

        self.procbox.setEditable(True)
        self.procbox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.procbox.lineEdit().setReadOnly(True)
        self.procbox.addItems(["Histogram Equalization", "Contrast Stretching",
                               "Log Compression", "Reverse Video"])
        tab2layout.addWidget(self.procbox, 1, 0)

        self.download_box.setEditable(True)
        self.download_box.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.download_box.lineEdit().setReadOnly(True)
        self.download_box.addItems([".JPG", ".PNG", ".TIFF"])
        tab2layout.addWidget(self.download_box, 0, 3)

        self.download_button.setEnabled(False)
        self.download_button.setToolTip('Download image in selected format')
        self.download_button.clicked.connect(self.download_image)
        tab2layout.addWidget(self.download_button, 1, 3)

        self.processor_button.setEnabled(False)
        self.processor_button.setToolTip('Send image to server for processing')
        self.processor_button.clicked.connect(self.process_button)
        tab2layout.addWidget(self.processor_button, 2, 0)

        orig_image_box = QGroupBox("Original Image")
        orig_image_layout = QHBoxLayout()
        orig_image_layout.addWidget(self.orig_image)
        orig_image_box.setLayout(orig_image_layout)
        tab2layout.addWidget(orig_image_box, 3, 0, 2, 2)

        self.orig_prev_button.setEnabled(False)
        self.orig_prev_button.setToolTip('No previous image to view')
        self.orig_prev_button.clicked.connect(self.orig_prev_image)
        tab2layout.addWidget(self.orig_prev_button, 5, 0)

        self.orig_next_button.setEnabled(False)
        self.orig_next_button.setToolTip('No next image to view')
        self.orig_next_button.clicked.connect(self.orig_next_image)
        tab2layout.addWidget(self.orig_next_button, 5, 1)

        proc_image_box = QGroupBox("Processed Image")
        proc_image_layout = QHBoxLayout()
        proc_image_layout.addWidget(self.proc_image)
        proc_image_box.setLayout(proc_image_layout)

        tab2layout.addWidget(proc_image_box, 3, 2, 2, 2)

        self.tab2.setLayout(tab2layout)

    def download_image(self):
        """Download image
        """

    def orig_next_image(self):
        """next image
        """
        first_image = fn.pop(0)
        fn.append(first_image)
        self.insert_orig_image(fn)

    def orig_prev_image(self):
        """prev image
        """
        last_image = fn.pop(-1)
        fn.insert(0, last_image)
        self.insert_orig_image(fn)

    def update_username(self):
        self.username = self.entered_username.text()
        if self.username != "":
            self.setTabEnabled(1, True)
            self.setCurrentIndex(1)

    @pyqtSlot()
    def file_select_button(self):
        self.openFileNamesDialog()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global fn
        global timestamps
        timestamps = [0]
        fn, _ = QFileDialog.getOpenFileNames(self, "Select Image File(s)", "",
                                             "JPEG (*.JPEG *.jpeg *.JPG "
                                             "*.jpg *.JPE *.jpe "
                                             "*JFIF *.jfif);; "
                                             "PNG (*.PNG *.png);; "
                                             "GIF (*.GIF *.gif);; "
                                             "Bitmap Files (*.BMP *.bmp"
                                             " *.DIB *.dib);;"
                                             " TIFF (*.TIF *.tif *.TIFF "
                                             "*.tiff);; ICO (*.ICO *.ico)"
                                             "ZIP (*.zip)",
                                             options=options)
        if fn:
            if len(fn) > 1:
                self.orig_next_button.setEnabled(True)
                self.orig_next_button.setToolTip('View next image')
                self.orig_prev_button.setEnabled(True)
                self.orig_prev_button.setToolTip('View previous image')
            else:
                self.orig_next_button.setEnabled(False)
                self.orig_next_button.setToolTip('No next image to view')
                self.orig_prev_button.setEnabled(False)
                self.orig_prev_button.setToolTip('No previous image to view')
            self.processor_button.setEnabled(True)
            self.insert_orig_image(fn)

    def insert_orig_image(self, fn):
            timestamps[0] = (str(datetime.now()))
            if zipfile.is_zipfile(fn[0]):
                z = zipfile.ZipFile(fn[0], "r")
                for filename in z.namelist():
                    fn[0] = filename
                    z.extractall(os.path.dirname(os.path.realpath(__file__)))
            input_image = imread(fn[0])
            print(type(input_image))
            image_shape = input_image.shape
            width = image_shape[1]
            height = image_shape[0]
            if len(image_shape) < 3:
                channels = 1
                bytesPerLine = channels * width
                qImg = QtGui.QImage(input_image.data, width, height,
                                    bytesPerLine,
                                    QtGui.QImage.Format_Grayscale8)
            else:
                channels = image_shape[2]
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

    def insert_processed_image(self, processed_images):
        byte_image = base64.b64decode(processed_images)
        input_image = decodeImage(byte_image)
        image_shape = input_image.shape
        width = image_shape[1]
        height = image_shape[0]
        if len(image_shape) < 3:
            channels = 1
            bytesPerLine = channels * width
            qImg = QtGui.QImage(input_image.data, width, height,
                                bytesPerLine,
                                QtGui.QImage.Format_Grayscale8)
        else:
            channels = image_shape[2]
            bytesPerLine = channels * width
            qImg = QtGui.QImage(input_image.data, width, height,
                                bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap01 = QtGui.QPixmap.fromImage(qImg)
        pixmap_image = QtGui.QPixmap(pixmap01)
        pixmap_image_scaled = pixmap_image.scaledToHeight(240)
        self.proc_image.setPixmap(pixmap_image_scaled)
        self.proc_image.setAlignment(QtCore.Qt.AlignCenter)
        self.proc_image.setScaledContents(True)
        self.proc_image.setMinimumSize(1, 1)
        self.proc_image.show()

    def process_button(self):
        self.download_button.setEnabled(True)
        self.process_server()

    def process_server(self):
        images_base64 = []
        process = self.procbox.currentText()
        for x in range(len(fn)):
            with open(fn[x], "rb") as image_file:
                image_bytes = image_file.read()
                print(type(image_bytes))
            image_base64 = base64.b64encode(image_bytes)
            base64_string = image_base64.decode('ascii')
            images_base64.append(base64_string)
        r2 = requests.post("http://0.0.0.0:5000/upload", json={
            "Images": images_base64,
            "Process": process,
            "User": self.username,
            "Timestamps": timestamps,
            "FileNames": fn,
        })
        time.sleep(2)
        global content
        content = requests.get("http://0.0.0.0:5000/download")
        content = content.json()
        unpack_server_info(content)
        self.insert_processed_image(s5[0])


def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())


def unpack_server_info(content1):
    global s1  # OG Images
    global s2  # TimeStamps
    global s3  # OG Height
    global s4  # OG Width
    global s5  # Processed Image
    global s6  # Time Spent
    global s7  # Processed Height
    global s8  # Processed Width
    s1 = content1.get("OG Images")
    s2 = content1.get("Timestamps")
    s3 = content1.get("OG Height")
    s4 = content1.get("OG Width")
    s5 = content1.get("Processed Images")
    s6 = content1.get("Time Spent")
    s7 = content1.get("Processed Height")
    s8 = content1.get("Processed Width")
    s1 = ast.literal_eval(s1)
    s2 = ast.literal_eval(s2)
    s3 = ast.literal_eval(s3)
    s4 = ast.literal_eval(s4)
    s5 = ast.literal_eval(s5)
    s6 = ast.literal_eval(s6)
    s7 = ast.literal_eval(s7)
    s8 = ast.literal_eval(s8)
    return "woo"


def decodeImage(byte_img):
    """Decodes a byte_image to a numpy array

    :param byte_img:
    :return:
    """
    image_buf = io.BytesIO(byte_img)

    i = mpimg.imread(image_buf, format='JPG')

    return i


if __name__ == '__main__':
    main()
