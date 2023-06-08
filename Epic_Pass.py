import sys
import random
from pathlib import Path
import pandas as pd
from openpyxl import *
import qrcode
import zxcvbn

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PassGenerator import *
from SavePass import *
# -------------------------Dark Theme--------------------------------------------------
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
# -------------------------Dark Theme--------------------------------------------------

# -------------------------Class MainWindow----------------------------------------START
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.WindowIcon = QIcon('images/icon.jpg')
        self.setWindowTitle("Epic Pass")
        self.setWindowIcon(self.WindowIcon)

        mainLayout = QVBoxLayout()

        # Initializing an object from StackedWidget Class to make multiple pages with shared buttons
        self.stackedWidget = QStackedWidget()

        self.passGen = PassGenerator()  # Initializing an object from PassGenerator Class
        self.PASSWORD = str(self.passGen.copyPass)

        self.savepassword = SavePass(self.PASSWORD)  # Initializing an object from SavePass Class

        self.stackedWidget.addWidget(self.passGen)  # index 0
        self.stackedWidget.addWidget(self.savepassword)  # index 1

        self.buttonPrevious = QPushButton('Previous')
        self.buttonPrevious.setVisible(False)
        self.buttonPrevious.setFixedSize(250, 50)
        self.buttonPrevious.clicked.connect(self.previousWidget)

        self.buttonNext = QPushButton('Next')
        self.buttonNext.setFixedSize(250, 50)
        self.buttonNext.clicked.connect(self.nextWidget)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.buttonPrevious)
        buttonLayout.addWidget(self.buttonNext)

        mainLayout.addWidget(self.stackedWidget)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    # -------------------------Functions-----------------------------------------------START
    def nextWidget(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() + 1) % 2)
        self.buttonNext.setVisible(False)
        self.buttonPrevious.setVisible(True)
        self.PASSWORD = str(self.passGen.copyPass)
        self.savepassword.generated_pass_editText.setText(self.PASSWORD)

    def previousWidget(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() - 1) % 2)
        self.buttonNext.setVisible(True)
        self.buttonPrevious.setVisible(False)


# -------------------------Functions-----------------------------------------------END
# -------------------------Class MainWindow----------------------------------------END

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setPalette(palette)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
