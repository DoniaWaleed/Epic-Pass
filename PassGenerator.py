from datetime import datetime
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

import Epic_Pass

# -------------------------Password Pool-----------------------------------------------
lower_alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']

upper_alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

special_char = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '-', '/', '<', '=', '>', '?', '@', '[', ']',
                '^', '_', '{', '}', '~']
# -------------------------Password Pool-----------------------------------------------

class PassGenerator(QWidget):
    copyPass = ""

    def __init__(self):
        super().__init__()
        self.WindowIcon = QIcon('images/icon.jpg')
        self.setWindowIcon(self.WindowIcon)

        self.password_list_chk = ['']

        self.mainLayout = QVBoxLayout()
        vlayout_slider = QVBoxLayout()
        hlayout_L_U_alpha = QHBoxLayout()
        vlayout_chkBoxes = QVBoxLayout()
        hlayout_btn = QHBoxLayout()
        vlayout_genPass = QVBoxLayout()

        # Create Extract action
        self.extractAction = QAction(QIcon('images/qr.jpg'), '&Extract QR', self)
        self.extractAction.setStatusTip('Extracting as QR..')
        self.extractAction.triggered.connect(self.extractQR)

        # Create Copy action
        self.copyAction = QAction(QIcon('images/copy_pic.png'), '&Copy to Clipboard', self)
        self.copyAction.setStatusTip('Copying..')
        self.copyAction.triggered.connect(self.copyToClipboard)

        # Create Reset action
        self.resetAction = QAction('&Reset', self)
        self.resetAction.setStatusTip('Resetting the Page..')
        self.resetAction.triggered.connect(self.reset)

        # Create menu bar and add action
        self.menuBar = QMenuBar(None)
        self.menuBar.adjustSize()
        self.fileMenu = QMenu("&Options", self)
        # self.fileMenu.setIcon(QIcon('images/settings.png'))
        self.fileMenu.addAction(self.extractAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.copyAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.resetAction)
        self.menuBar.addMenu(self.fileMenu)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.adjustSize()
        self.slider.setRange(8, 50)
        self.slider.setValue(12)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider.setGeometry(QtCore.QRect(50, -20, 500, 160))
        self.slider.valueChanged.connect(self.update_slider_value)
        self.current_label = QLabel('', self)
        self.current_label.adjustSize()
        self.current_label.setText(f"Current Value: {self.slider.value()}")
        vlayout_slider.addWidget(self.menuBar)
        vlayout_slider.addWidget(self.slider)
        vlayout_slider.addWidget(self.current_label)

        self.checkbox_lower_alpha = QCheckBox("Lower Alphabet", self)
        self.checkbox_lower_alpha.adjustSize()
        self.checkbox_lower_alpha.setChecked(True)

        self.checkbox_upper_alpha = QCheckBox("Upper Alphabet", self)
        self.checkbox_upper_alpha.adjustSize()
        self.checkbox_upper_alpha.setChecked(True)

        hlayout_L_U_alpha.addWidget(self.checkbox_lower_alpha, alignment=QtCore.Qt.AlignRight)
        hlayout_L_U_alpha.addWidget(self.checkbox_upper_alpha, alignment=QtCore.Qt.AlignRight)
        hlayout_L_U_alpha.setAlignment(QtCore.Qt.AlignCenter)
        self.checkbox_alpha = QCheckBox("Alphabet", self)
        self.checkbox_alpha.adjustSize()
        self.checkbox_alpha.setChecked(True)
        self.checkbox_alpha.stateChanged.connect(self.show_chkBox)

        self.checkbox_numbers = QCheckBox("Numbers", self)
        self.checkbox_numbers.adjustSize()
        self.checkbox_numbers.setChecked(True)

        self.checkbox_special_char = QCheckBox("Special Characters", self)
        self.checkbox_special_char.adjustSize()
        self.checkbox_special_char.setChecked(True)

        vlayout_chkBoxes.addWidget(self.checkbox_alpha)
        vlayout_chkBoxes.addLayout(hlayout_L_U_alpha)
        vlayout_chkBoxes.addWidget(self.checkbox_numbers)
        vlayout_chkBoxes.addWidget(self.checkbox_special_char)

        self.button_generate = QPushButton('Generate', self)
        self.button_generate.adjustSize()
        # self.button_generate.setMinimumSize(250, 50)
        self.button_generate.clicked.connect(self.btnChk)

        # self.button_copy = QPushButton(' Copy to Clipboard', self)
        # self.button_copy.setIcon(QIcon('images/copy_pic.png'))
        # self.button_copy.resize(300, 50)
        # # self.button_copy.move(280, 300)
        # self.button_copy.clicked.connect(self.copyToClipboard)
        #
        # self.button_extract = QPushButton('Extract QR', self)
        # self.button_extract.resize(250, 50)
        # # self.button_extract.move(610, 300)
        # self.button_extract.clicked.connect(self.extractQR)

        hlayout_btn.addWidget(self.button_generate)
        # hlayout_btn.addWidget(self.button_copy)
        # hlayout_btn.addWidget(self.button_extract)

        self.label_gen_pass = QLabel("The Generated Password:", self)
        self.label_gen_pass.adjustSize()
        self.label_gen_pass.setVisible(True)
        label_gen_pass_font = self.label_gen_pass.font()
        label_gen_pass_font.setPointSize(9)
        self.label_gen_pass.setFont(label_gen_pass_font)
        self.label_gen_pass.adjustSize()

        self.label_strength_pass = QLabel("Password Strength:", self)
        self.label_strength_pass.adjustSize()
        self.label_strength_pass.setVisible(True)

        vlayout_genPass.addWidget(self.label_gen_pass)
        vlayout_genPass.addWidget(self.label_strength_pass)
        vlayout_genPass.addStretch(1)

        self.qr_img = QLabel(self)
        self.qr_img.setVisible(False)
        self.qr_img.adjustSize()

        self.mainLayout.addLayout(vlayout_slider)
        self.mainLayout.addLayout(hlayout_L_U_alpha)
        self.mainLayout.addLayout(vlayout_chkBoxes)
        self.mainLayout.addLayout(hlayout_btn)
        self.mainLayout.addLayout(vlayout_genPass)
        self.mainLayout.addWidget(self.qr_img, alignment=QtCore.Qt.AlignCenter)
        self.mainLayout.addStretch(1)

        self.setLayout(self.mainLayout)

        # show the window
        self.show()

    # -------------------------Functions-----------------------------------------------START
    def extractQR(self):
        # Create QR Code
        qr = qrcode.QRCode(version=1, box_size=4, border=1)
        qr.add_data(self.copyPass)
        qr.make()
        img = qr.make_image(fill_color='black', back_color='white')
        img.save('Generated_QR/password_qr.png')
        # Display QR Code on screen
        self.qr_img.setPixmap(QPixmap('Generated_QR/password_qr.png').scaled(70, 70))
        self.qr_img.setVisible(True)
        self.qr_img.adjustSize()

    def copyToClipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        print("Copied password:", self.copyPass)
        cb.setText(self.copyPass, mode=cb.Clipboard)
        self.clipBoardAlert = QMessageBox()
        self.clipBoardAlert.setWindowIcon(self.WindowIcon)
        self.clipBoardAlert.setWindowTitle("Copied!!")
        self.clipBoardAlert.setText(cb.text() + " Copied on Clipboard")
        self.clipBoardAlert.exec_()

    def reset(self):
        self.label_gen_pass.setText("The Generated Password:")
        self.label_strength_pass.setText("Password Strength:")
        self.qr_img.setVisible(False)

    def show_chkBox(self):
        if self.checkbox_alpha.isChecked() == True:
            self.checkbox_lower_alpha.setVisible(True)
            self.checkbox_upper_alpha.setVisible(True)

            self.checkbox_upper_alpha.adjustSize()
            self.checkbox_lower_alpha.adjustSize()
        else:
            self.checkbox_lower_alpha.setVisible(False)
            self.checkbox_upper_alpha.setVisible(False)

    def btnChk(self):

        # Error Box
        self.error = QMessageBox()
        self.error.setWindowTitle("Error!!")
        self.error.setText("You Must Choose")
        self.error.setIcon(QMessageBox.Critical)
        self.error.setWindowIcon(self.WindowIcon)

        length = self.slider.value()
        print("Length:", length)

        newPassword = ''

        if (self.checkbox_alpha.isChecked() == False and self.checkbox_numbers.isChecked() == False and self.checkbox_special_char.isChecked() == False or self.checkbox_alpha.isChecked() == True and self.checkbox_lower_alpha.isChecked() == False and self.checkbox_upper_alpha.isChecked() == False):
            self.error.exec_()
        else:
            random.seed(datetime.now())
            while newPassword in self.password_list_chk:
                password = ""
                if (self.checkbox_alpha.isChecked() == True and self.checkbox_numbers.isChecked() == True and self.checkbox_special_char.isChecked() == True):
                    if (self.checkbox_lower_alpha.isChecked() == True and self.checkbox_upper_alpha.isChecked() == True):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(upper_alpha)
                            if len(password) < length:
                                password += random.choice(numbers)
                            if len(password) < length:
                                password += random.choice(special_char)
                            if len(password) < length:
                                password += random.choice(lower_alpha)

                    elif (self.checkbox_lower_alpha.isChecked() == True and self.checkbox_upper_alpha.isChecked() == False):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(numbers)
                            if len(password) < length:
                                password += random.choice(special_char)
                            if len(password) < length:
                                password += random.choice(lower_alpha)

                    elif (self.checkbox_lower_alpha.isChecked() == False and self.checkbox_upper_alpha.isChecked() == True):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(upper_alpha)
                            if len(password) < length:
                                password += random.choice(numbers)
                            if len(password) < length:
                                password += random.choice(special_char)

                elif (self.checkbox_alpha.isChecked() == True and self.checkbox_numbers.isChecked() == True and self.checkbox_special_char.isChecked() == False):
                    if (self.checkbox_lower_alpha.isChecked() == True and self.checkbox_upper_alpha.isChecked() == True):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(upper_alpha)
                            if len(password) < length:
                                password += random.choice(numbers)
                            if len(password) < length:
                                password += random.choice(lower_alpha)

                    elif (self.checkbox_lower_alpha.isChecked() == True and self.checkbox_upper_alpha.isChecked() == False):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(numbers)
                            if len(password) < length:
                                password += random.choice(lower_alpha)

                    elif (self.checkbox_lower_alpha.isChecked() == False and self.checkbox_upper_alpha.isChecked() == True):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(upper_alpha)
                            if len(password) < length:
                                password += random.choice(numbers)

                elif (self.checkbox_alpha.isChecked() == True and self.checkbox_numbers.isChecked() == False and self.checkbox_special_char.isChecked() == True):
                    if (self.checkbox_lower_alpha.isChecked() == True and self.checkbox_upper_alpha.isChecked() == True):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(upper_alpha)
                            if len(password) < length:
                                password += random.choice(special_char)
                            if len(password) < length:
                                password += random.choice(lower_alpha)

                    elif (self.checkbox_lower_alpha.isChecked() == True and self.checkbox_upper_alpha.isChecked() == False):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(special_char)
                            if len(password) < length:
                                password += random.choice(lower_alpha)

                    elif (self.checkbox_lower_alpha.isChecked() == False and self.checkbox_upper_alpha.isChecked() == True):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(upper_alpha)
                            if len(password) < length:
                                password += random.choice(special_char)

                elif (self.checkbox_alpha.isChecked() == True and self.checkbox_numbers.isChecked() == False and self.checkbox_special_char.isChecked() == False):
                    if (self.checkbox_lower_alpha.isChecked() == True and self.checkbox_upper_alpha.isChecked() == True):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(upper_alpha)
                            if len(password) < length:
                                password += random.choice(lower_alpha)

                    elif (self.checkbox_lower_alpha.isChecked() == True and self.checkbox_upper_alpha.isChecked() == False):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(lower_alpha)

                    elif (self.checkbox_lower_alpha.isChecked() == False and self.checkbox_upper_alpha.isChecked() == True):
                        while len(password) < length:
                            if len(password) < length:
                                password += random.choice(upper_alpha)

                elif (self.checkbox_alpha.isChecked() == False and self.checkbox_numbers.isChecked() == True and self.checkbox_special_char.isChecked() == True):
                    while len(password) < length:
                        if len(password) < length:
                            password += random.choice(numbers)
                        if len(password) < length:
                            password += random.choice(special_char)


                elif (self.checkbox_alpha.isChecked() == False and self.checkbox_numbers.isChecked() == False and self.checkbox_special_char.isChecked() == True):
                    while len(password) < length:
                        if len(password) < length:
                            password += random.choice(special_char)


                elif (self.checkbox_alpha.isChecked() == False and self.checkbox_numbers.isChecked() == True and self.checkbox_special_char.isChecked() == False):
                    while len(password) < length:
                        if len(password) < length:
                            password += random.choice(numbers)

                newPassword = ''.join(random.sample(password, len(password)))

                while password[0] == '?' or newPassword[0] == '?':
                    newPassword = ''.join(random.sample(password, len(password)))

            self.password_list_chk.append(newPassword)
            self.copyPass = newPassword
            self.strength_result = zxcvbn.zxcvbn(self.copyPass)
            print("Password:", newPassword)

            if len(self.password_list_chk) > 100:
                self.password_list_chk = []

            self.gen_pass_update(self.copyPass, self.strength_result["score"])

    def gen_pass_update(self, value, value2):
        self.label_gen_pass.setText(f"The Generated Password: {value}")
        self.label_gen_pass.adjustSize()

        if value2 == 4:
            self.label_strength_pass.setText(f"Password Strength: Very Strong ({value2})")
        elif value2 == 3:
            self.label_strength_pass.setText(f"Password Strength: Strong ({value2})")
        elif value2 == 2:
            self.label_strength_pass.setText(f"Password Strength: Moderate ({value2})")
        elif value2 == 1:
            self.label_strength_pass.setText(f"Password Strength: Weak ({value2})")
        elif value2 == 0:
            self.label_strength_pass.setText(f"Password Strength: Very Weak ({value2})")
        self.label_strength_pass.adjustSize()

        if self.qr_img.isVisible():
            self.extractQR()

    def update_slider_value(self, value):
        self.current_label.setText(f"Current Value: {value}")
        self.current_label.adjustSize()


# -------------------------Functions-----------------------------------------------END