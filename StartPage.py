from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout

from SavePass import *

class StartPage(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()

        self.label_logo = QLabel()
        self.label_logo.adjustSize()
        # self.label_logo.move(100, 360)
        self.label_logo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_logo.setVisible(True)
        self.label_logo.setPixmap(QPixmap('images/icon.png').scaled(200, 200))
        # self.label_logo.resize(1000, 1000)
        # self.label_logo.adjustSize()

        self.label_title = QLabel("Epic Pass")
        self.label_title.adjustSize()
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setVisible(True)

        label_title_font = self.label_title.font()
        label_title_font.setPointSize(18)
        label_title_font.bold()

        self.label_title.setFont(label_title_font)
        self.label_title.adjustSize()

        Flayout = QFormLayout()
        Hlayout = QHBoxLayout()

        self.password_editText = QLineEdit()
        self.password_editText.setEchoMode(QLineEdit.Password)
        self.password_editText.adjustSize()

        self.checkbox_show_hide_pass = QCheckBox("Show", self)
        self.checkbox_show_hide_pass.adjustSize()
        self.checkbox_show_hide_pass.setChecked(False)
        self.checkbox_show_hide_pass.clicked.connect(self.toggleVisibility)

        Hlayout.addWidget(self.password_editText)
        Hlayout.addWidget(self.checkbox_show_hide_pass)

        Flayout.addRow("Password: ", Hlayout)

        self.label_warning = QLabel('Default Password is 12345678 Please change it as soon as possible')
        self.label_warning.adjustSize()
        self.label_warning.setVisible(True)

        self.mainLayout.addWidget(self.label_logo)
        self.mainLayout.addWidget(self.label_title)
        self.mainLayout.addLayout(Flayout)
        self.mainLayout.addWidget(self.label_warning, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.mainLayout)

    def toggleVisibility(self):
        if self.checkbox_show_hide_pass.isChecked():
            self.password_editText.setEchoMode(QLineEdit.Normal)
        else:
            self.password_editText.setEchoMode(QLineEdit.Password)

    # getter method
    def get_password_editText(self):
        return self.password_editText.text()

    def set_password_editText(self, x):
        self.password_editText.setText(x)

