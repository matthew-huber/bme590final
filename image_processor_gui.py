import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


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
                                             options=options)
        if fn:
            print(fn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
