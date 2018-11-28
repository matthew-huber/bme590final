import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQT5 Simple Window'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button = QPushButton('PyQT5 button', self)
        button.setToolTip('this is an example button')
        button.move(100,70)
        button.clicked.connect(self.file_select_button)

        #self.openFileNameDialog()

        #self.openFileNamesDialog()
        #self.saveFileDialog()

        self.show()

    @pyqtSlot()
    def file_select_button(self):
        self.openFileNameDialog()
        print('PyQt5 button click')

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All File (*);;Python File(*.py)", options=options)
        if fileName:
            print(fileName)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
