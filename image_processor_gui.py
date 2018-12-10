from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtCore
import matplotlib
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
import numpy as np
import imghdr
import json
from matplotlib import pyplot as plt
# matplotlib.use("QT5Agg")


class App(QTabWidget):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        self.multiple_images = False
        self.zipped_images = False

        self.username = ""
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        # tab1
        self.entered_username = QLineEdit()
        self.user_select = QComboBox(self)
        self.user_select_error = QLabel("No user entered or selected")

        # tab2
        self.procbox = QComboBox(self)
        self.download_box = QComboBox(self)
        self.orig_next_button = QPushButton('Next Image >>')
        self.orig_prev_button = QPushButton('<< Prev Image')
        self.view_image_hist = QPushButton('View histograms for these images')
        self.download_button = QPushButton('Download', self)
        self.download_all_button = QPushButton('Download All', self)
        self.processor_button = QPushButton('Process', self)
        self.zip_download = QCheckBox("Zip together files on download")
        self.orig_image = QLabel("")
        self.proc_image = QLabel("")

        # tab3
        self.users_images = QListWidget()
        self.users_images.itemClicked.connect(self.load_image_data)
        self.image_filename = QLabel("")
        self.image_pixels = QLabel("")
        self.date_upload = QLabel("")
        self.processing_time = QLabel("")
        self.process_done = QLabel("")
        self.remove_image = QPushButton("Remove Image", self)
        self.remove_image.setEnabled(False)

        # tab4
        self.histogram_fig = QLabel("")
        self.return_to_process = QPushButton("Return to process images tab")

        self.currentChanged.connect(self.changed_tab)
        self.addTab(self.tab1, "Specify User")
        self.addTab(self.tab2, "Process Image")
        self.addTab(self.tab3, "Manage Images")
        self.addTab(self.tab4, "Color Intensity")
        self.setTabEnabled(1, False)
        self.setTabEnabled(2, False)
        self.setTabEnabled(3, False)
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()

        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Image Processor Control')

    def tab1UI(self):
        layout = QFormLayout()
        line_one_layout = QHBoxLayout()
        username_layout = QFormLayout()
        line_one_layout.addWidget(self.entered_username)
        line_one_layout.addWidget(QLabel("Or select from existing users:"))
        line_one_layout.addWidget(self.user_select)
        username_layout.addRow("Enter Username", line_one_layout)

        layout.addRow(username_layout)

        enter_button = QHBoxLayout()
        user_button = QPushButton("Enter")
        user_button.setToolTip("Enter username")
        user_button.clicked.connect(self.update_username)
        enter_button.addWidget(user_button)
        layout.addRow(enter_button)
        layout.addRow(self.user_select_error)
        self.user_select_error.hide()
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
        self.download_box.addItems(["jpg", "png", "tiff"])
        tab2layout.addWidget(self.download_box, 0, 3)

        download_buttons_layout = QHBoxLayout()
        self.download_button.setEnabled(False)
        self.download_button.setToolTip('Download image in selected format')
        self.download_button.clicked.connect(self.download_image)
        self.download_all_button.setEnabled(False)
        self.download_all_button.setToolTip('Download all in selected format')
        self.download_all_button.clicked.connect(self.download_all_images)
        download_buttons_layout.addWidget(self.download_button)
        download_buttons_layout.addWidget(self.download_all_button)
        tab2layout.addLayout(download_buttons_layout, 1, 3)

        self.zip_download.hide()
        self.zip_download.setToolTip('Zip if multiple images are downloaded')
        tab2layout.addWidget(self.zip_download, 2, 3)

        self.processor_button.setEnabled(False)
        self.processor_button.setToolTip('Send image for processing')
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

        self.view_image_hist.setEnabled(False)
        self.view_image_hist.setToolTip('View histograms for these images')
        self.view_image_hist.clicked.connect(self.make_histogram_plots)
        tab2layout.addWidget(self.view_image_hist, 5, 2, 1, 2)

        self.tab2.setLayout(tab2layout)

    def tab3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(self.users_images)

        metadata_layout = QFormLayout()
        metadata_layout.addRow("Image Filename: ", self.image_filename)
        metadata_layout.addRow("Pixel Size: ", self.image_pixels)
        metadata_layout.addRow("Latest Process Done: ", self.process_done)
        metadata_layout.addRow("Date Uploaded: ", self.date_upload)
        metadata_layout.addRow("Time to Process: ", self.processing_time)
        metadata_layout.addRow(self.remove_image)
        self.remove_image.clicked.connect(self.delete_image)

        layout.addLayout(metadata_layout)
        self.tab3.setLayout(layout)

    def tab4UI(self):
        histogram_layout = QVBoxLayout()
        histogram_layout.addWidget(self.histogram_fig)
        self.return_to_process.clicked.connect(self.switch_tab_2)
        histogram_layout.addWidget(self.return_to_process)
        self.tab4.setLayout(histogram_layout)

    def switch_tab_2(self):
        self.setCurrentIndex(1)
        self.setTabEnabled(3, False)

    def make_histogram_plots(self):
        self.setTabEnabled(3, True)
        num_cols = len(OG_HISTOGRAMS[0])
        fig, axarr = plt.subplots(num_cols, 2)
        for i in range(num_cols):
            if num_cols == 1:
                ax = axarr[0]
            else:
                ax = axarr[i, 0]
            hist_data = OG_HISTOGRAMS[0][i][0]
            bins = OG_HISTOGRAMS[0][i][1]
            ax.hist(hist_data, bins=bins)
            ax.set_title("Original, Channel " + str(i + 1))
            ax.set_ylabel("Count")
            ax.set_xlabel("Intensity")
            fig.add_axes(ax)
            if num_cols == 1:
                ax = axarr[1]
            else:
                ax = axarr[i, 1]
            hist_data = PROC_HISTOGRAMS[0][i][0]
            bins = PROC_HISTOGRAMS[0][i][1]
            ax.hist(hist_data, bins=bins)
            ax.set_title("Processed, Channel " + str(i + 1))
            ax.set_ylabel("Count")
            ax.set_xlabel("Intensity")
            fig.add_axes(ax)
        plt.tight_layout()
        plt.savefig('matplot.jpg')
        self.display_histogram()
        self.setCurrentIndex(3)

    def display_histogram(self):
        pixmap_image = QtGui.QPixmap('matplot.jpg')
        self.histogram_fig.setPixmap(pixmap_image)
        self.histogram_fig.setAlignment(QtCore.Qt.AlignCenter)
        self.histogram_fig.setScaledContents(True)
        self.histogram_fig.show()
        os.remove('matplot.jpg')

    def changed_tab(self, i):
        if i != 3:
            self.setTabEnabled(3, False)
        if i == 0:
            self.user_select.clear()
            user_list = requests.get("http://152.3.53.153:5000/user_list")
            user_list = user_list.json()
            user_list.insert(0, "Select:")
            self.user_select.addItems(user_list)
        if i == 2:
            self.update_image_list()

    def update_image_list(self):
        self.users_images.clear()
        request_url = "http://152.3.53.153:5000/get_images/" + self.username
        get_images = requests.get(request_url)
        get_users_images_list = get_images.json()
        get_users_images = []
        for item in get_users_images_list:
            get_users_images.append(item[0:(len(item)-len(self.username))])
        self.users_images.addItems(get_users_images)
        self.remove_image.setEnabled(False)

    def delete_image(self):
        filename = self.users_images.currentItem().text()
        url_end = filename + self.username
        request_url = "http://152.3.53.153:5000/delete_image/" + url_end
        delete = requests.get(request_url)
        self.update_image_list()

        self.image_filename.setText("")
        self.image_pixels.setText("")
        self.process_done.setText("")
        self.date_upload.setText("")
        self.processing_time.setText("")

    def load_image_data(self, current):
        self.remove_image.setEnabled(True)
        filename = current.text()
        url_end = filename + self.username
        request_url = "http://152.3.53.153:5000/image_data/" + url_end
        image_metadata = requests.get(request_url)
        image_metadata = image_metadata.json()

        self.image_filename.setText(str(filename))
        self.image_pixels.setText(str(image_metadata["image_pixels"]))
        self.process_done.setText(str(image_metadata["process_done"]))
        self.date_upload.setText(str(image_metadata["date_upload"]))
        self.processing_time.setText(str(image_metadata["process_times"]) +
                                     " seconds")

    def download_image(self):
        """Download image
        """
        filetype = self.download_box.currentText()
        filename = fn[0]
        filename = filename.split("/")[-1]
        url_end = filename + self.username
        processing_type = "http://152.3.53.153:5000/processing_type/" + url_end
        processing_type = requests.get(processing_type)
        processing_type = processing_type.json()
        processing_type = processing_type["process_done"]
        filename = filename.split(".")[0]
        filename = filename + "_" + processing_type + "." + filetype
        value = self.pixmap_image_scaled.save(filename, filetype, 100)
        return filename, processing_type

    def download_all_images(self):
        """Download all images
        """
        filenames = []
        nfiles = 0
        for i in range(len(fn)):
            filename, processing_type = self.download_image()
            filenames.append(filename)
            self.orig_next_image()
            nfiles = nfiles + 1
        if self.zip_download.isChecked():
            folder_name = str(nfiles) + " " + processing_type + ' images.zip'
            self.zip_downloaded_images(filenames, folder_name)

    def zip_downloaded_images(self, filenames, folder_name):
        zip_folder = zipfile.ZipFile(folder_name, "w")
        for file in filenames:
            zip_folder.write(file, compress_type=zipfile.ZIP_DEFLATED)
        for file in filenames:
            os.remove(file)

    def orig_next_image(self):
        """next image
        """
        first_image = fn.pop(0)
        fn.append(first_image)
        self.insert_orig_image(fn)
        if self.multiple_images:
            first = OG_HISTOGRAMS.pop(0)
            OG_HISTOGRAMS.append(first)
            first_proc_image = PROCESSED_IMAGE.pop(0)
            PROCESSED_IMAGE.append(first_proc_image)
            self.insert_processed_image(PROCESSED_IMAGE[0])
            first = PROC_HISTOGRAMS.pop(0)
            PROC_HISTOGRAMS.append(first)

    def orig_prev_image(self):
        """prev image
        """
        last_image = fn.pop(-1)
        fn.insert(0, last_image)
        self.insert_orig_image(fn)
        if self.multiple_images:
            last = OG_HISTOGRAMS.pop(-1)
            OG_HISTOGRAMS.insert(0, last)
            last_proc_image = PROCESSED_IMAGE.pop(-1)
            PROCESSED_IMAGE.insert(0, last_proc_image)
            self.insert_processed_image(PROCESSED_IMAGE[0])
            last = PROC_HISTOGRAMS.pop(-1)
            PROC_HISTOGRAMS.insert(0, last)

    def update_username(self):
        self.username = self.entered_username.text()
        dropdown_text = self.user_select.currentText()

        if self.username != "" or dropdown_text != "Select:":
            if self.username == "":
                self.username = dropdown_text
            self.setTabEnabled(1, True)
            self.setTabEnabled(2, True)
            self.setTabEnabled(3, False)
            self.setCurrentIndex(1)
            self.user_select_error.hide()
        else:
            self.user_select_error.show()

    @pyqtSlot()
    def file_select_button(self):
        self.openFileNamesDialog()

    def openFileNamesDialog(self):
        global TIMESTAMPS
        TIMESTAMPS = [0]
        global fn

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fn_got, _ = QFileDialog.getOpenFileNames(self, "Open Image Files", "",
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

        if fn_got:
            fn = fn_got
            self.proc_image.hide()
            self.download_all_button.setEnabled(False)
            self.download_button.setEnabled(False)
            self.view_image_hist.setEnabled(False)
            self.zip_download.hide()

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

            self.zipped_images = False
            for x in range(len(fn)):
                if zipfile.is_zipfile(fn[x]):
                    self.zipped_images = True
                    zfile = fn[x]
                    self.extractAndAppendZipFiles(zfile)
                    fn.pop(x)  # Removes zipfile name from filelist

            if self.zipped_images:
                self.orig_next_button.setEnabled(True)
                self.orig_next_button.setToolTip('View next image')
                self.orig_prev_button.setEnabled(True)
                self.orig_prev_button.setToolTip('View previous image')

            fn = validateFiles(fn)
            # Exits function in the event that there are no valid images in
            # the files selected
            if len(fn) == 0:
                return
            global PROCESSED_IMAGE
            PROCESSED_IMAGE = []
            self.insert_orig_image(fn)

    def insert_orig_image(self, fn):

        pixmap_image = QtGui.QPixmap(fn[0])
        pixmap_image_scaled = pixmap_image.scaledToHeight(240)
        self.orig_image.setPixmap(pixmap_image_scaled)
        self.orig_image.setAlignment(QtCore.Qt.AlignCenter)
        self.orig_image.setScaledContents(True)
        self.orig_image.setMinimumSize(1, 1)
        self.orig_image.show()

    def insert_processed_image(self, processed_images):
        byte_image = base64.b64decode(processed_images)
        input_image = decodeImage(byte_image)
        input_image.setflags(write=1)

        if input_image.ndim >= 3:
            input_image = compress_multidimm_image(input_image)

        pixmap_image = self.get_pixelmap_image(input_image)

        self.pixmap_image_scaled = pixmap_image.scaledToHeight(240)
        self.proc_image.setPixmap(self.pixmap_image_scaled)
        self.proc_image.setAlignment(QtCore.Qt.AlignCenter)
        self.proc_image.setScaledContents(True)
        self.proc_image.setMinimumSize(1, 1)
        self.proc_image.show()

    def getQImg(self, input_image):
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
        return qImg

    def get_pixelmap_image(self, input_image):
        qImg = self.getQImg(input_image)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        pixmap_image = QtGui.QPixmap(pixmap)
        return pixmap_image

    def process_button(self):
        self.download_button.setEnabled(True)
        self.view_image_hist.setEnabled(True)
        self.process_server()

    def process_server(self):
        images_base64 = []
        processing_type = self.procbox.currentText()
        TIMESTAMPS[0] = (str(datetime.now()))

        if len(fn) > 1:
            self.enable_process_all_button()
        else:
            self.disable_process_all_button()

        DB_filenames = makeDatabaseFileNames(fn, self.username)

        for x in range(len(fn)):
            if zipfile.is_zipfile(fn[x]):
                self.zipped_images = True
                self.extractAndAppendZipFiles(fn[x])
                # Removes zip filename from filenames list, which have been
                # replaced with file names in the zip file
                fn.pop(x)

            is_valid_header = validateImageHeader(fn[x])
            if not is_valid_header:
                fn.pop(x)

            base64_string = self.get_base64_string(fn[x])
            images_base64.append(base64_string)

        # interrupts function if no images remain after removing invalid
        #  images
        if len(fn) == 0:
            return
        r2 = requests.post("http://152.3.53.153:5000/upload", json={
            "Images": images_base64,
            "Process": processing_type,
            "User": self.username,
            "Timestamps": TIMESTAMPS,
            "FileNames": DB_filenames,
        })

        global content
        content = r2.json()
        unpack_server_info(content)

        self.insert_processed_image(PROCESSED_IMAGE[0])

    def enable_process_all_button(self):
        self.download_all_button.setEnabled(True)
        self.multiple_images = True
        self.zip_download.show()

    def disable_process_all_button(self):
        self.download_all_button.setEnabled(False)
        self.multiple_images = False
        self.zip_download.hide()

    def extractAndAppendZipFiles(self, zfile):
        z = zipfile.ZipFile(zfile, "r")

        for filename in z.namelist():
            filename = filename.split("/._")[-1]
            fn.append(filename)
            z.extractall(os.path.dirname(os.path.realpath(__file__)))

    def get_image_bytes(self, filename):
        with open(filename, "rb") as image_file:
            image_bytes = image_file.read()
        return image_bytes

    def get_base64_string(self, filename):
        image_bytes = self.get_image_bytes(filename)
        image_base64 = base64.b64encode(image_bytes)
        base64_string = image_base64.decode('ascii')
        return base64_string


def main():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())


def unpack_server_info(content1):
    global ORIGINAL_IMAGES
    global TIMESTAMPS
    global OG_HEIGHT
    global OG_WIDTH
    global PROCESSED_IMAGE
    global PROCESSING_TIME
    global PROCESSED_HEIGHT
    global PROCESSED_WIDTH

    ORIGINAL_IMAGES = content1.get("OG Images")
    TIMESTAMPS = content1.get("Timestamps")
    OG_HEIGHT = content1.get("OG Height")
    OG_WIDTH = content1.get("OG Width")
    PROCESSED_IMAGE = content1.get("Processed Images")
    PROCESSING_TIME = content1.get("Time Spent")
    PROCESSED_HEIGHT = content1.get("Processed Height")
    PROCESSED_WIDTH = content1.get("Processed Width")

    ORIGINAL_IMAGES = ast.literal_eval(ORIGINAL_IMAGES)
    TIMESTAMPS = ast.literal_eval(TIMESTAMPS)
    OG_HEIGHT = ast.literal_eval(OG_HEIGHT)
    OG_WIDTH = ast.literal_eval(OG_WIDTH)
    PROCESSED_IMAGE = ast.literal_eval(PROCESSED_IMAGE)
    PROCESSING_TIME = ast.literal_eval(PROCESSING_TIME)
    PROCESSED_HEIGHT = ast.literal_eval(PROCESSED_HEIGHT)
    PROCESSED_WIDTH = ast.literal_eval(PROCESSED_WIDTH)

    global OG_HISTOGRAMS
    global PROC_HISTOGRAMS
    OG_HISTOGRAMS = content1.get("OG Histograms")
    PROC_HISTOGRAMS = content1.get("Processed Histograms")

    OG_HISTOGRAMS = json.loads(OG_HISTOGRAMS)
    PROC_HISTOGRAMS = json.loads(PROC_HISTOGRAMS)
    return "woo"


def decodeImage(byte_img):
    """Decodes a byte_image to a numpy array
    :param byte_img:
    :return:
    """

    image_buf = io.BytesIO(byte_img)

    i = mpimg.imread(image_buf, format='JPG')

    return i


def validateFiles(file_list):
    invalid_files = []

    for inx in range(len(file_list)):
        file = file_list[inx]
        is_valid_file = validateImageHeader(file)
        if not is_valid_file:
            invalid_files.append(file)

    for invalidFile in invalid_files:
        file_list.remove(invalidFile)

    return file_list


def validateImageHeader(file_path):
    header = imghdr.what(file_path)

    if header is None:
        return False
    else:
        return True


def compress_multidimm_image(input_image):

    temp = np.zeros(input_image.shape, dtype='uint8')
    temp = np.copy(input_image[:, :, 0])
    input_image[:, :, 0] = input_image[:, :, 2]
    input_image[:, :, 2] = temp
    return input_image


def makeDatabaseFileNames(fn, username):
    filenames = get_filenames_remove_full_path(fn)
    filenames = get_filenames_add_username(filenames, username)
    return filenames


def get_filenames_remove_full_path(files):
    """
    :param files: list of files with paths
    :return:
    """
    filenames = []
    for i in range(len(files)):
        filename = files[i]
        filename = filename.split("/")[-1]
        filenames.append(filename)
    return filenames


def get_filenames_add_username(files, username):
    """
    :param files: List of file names
    :param username:  Username to append
    :return:
    """

    filenames = []
    for file in files:
        filenames.append(file + username)

    return filenames


if __name__ == '__main__':
    main()
