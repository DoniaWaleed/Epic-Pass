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
        # self.setFixedSize(900,700)
        self.setMinimumSize(900, 700)

        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(8, 50)
        self.slider.setValue(12)
        self.slider.setSingleStep(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider.setGeometry(QtCore.QRect(50, -20, 500, 160))
        self.slider.valueChanged.connect(self.update_slider_value)
        self.current_label = QLabel('', self)
        self.current_label.setText(f"Current Value: {self.slider.value()}")
        self.current_label.move(50, 20)

        self.checkbox_lower_alpha = QCheckBox("Lower Alphabet", self)
        self.checkbox_lower_alpha.move(100, 145)
        self.checkbox_lower_alpha.setChecked(True)

        self.checkbox_upper_alpha = QCheckBox("Upper Alphabet", self)
        self.checkbox_upper_alpha.move(380, 145)
        self.checkbox_upper_alpha.setChecked(True)

        self.checkbox_alpha = QCheckBox("Alphabet", self)
        self.checkbox_alpha.move(50, 100)
        self.checkbox_alpha.setChecked(True)
        self.checkbox_alpha.stateChanged.connect(self.show_chkBox)

        self.checkbox_numbers = QCheckBox("Numbers", self)
        self.checkbox_numbers.move(50, 190)
        self.checkbox_numbers.setChecked(True)

        self.checkbox_special_char = QCheckBox("Special Characters", self)
        self.checkbox_special_char.move(50, 240)
        self.checkbox_special_char.setChecked(True)

        self.button = QPushButton('Generate', self)
        self.button.resize(200, 50)
        self.button.move(50, 300)
        self.button.clicked.connect(self.btnChk)

        self.button_copy = QPushButton(' Copy to Clipboard', self)
        self.button_copy.setIcon(QIcon('images/copy_pic.png'))
        self.button_copy.resize(300, 50)
        self.button_copy.move(280, 300)
        self.button_copy.clicked.connect(self.copyToClipboard)

        self.button_extract = QPushButton('Extract QR', self)
        self.button_extract.resize(250, 50)
        self.button_extract.move(610, 300)
        self.button_extract.clicked.connect(self.extractQR)

        self.label_gen_pass = QLabel("The Generated Password:", self)
        self.label_gen_pass.move(100, 360)
        self.label_gen_pass.setVisible(True)
        label_gen_pass_font = self.label_gen_pass.font()
        label_gen_pass_font.setPointSize(9)
        self.label_gen_pass.setFont(label_gen_pass_font)
        self.label_gen_pass.adjustSize()

        self.label_strength_pass = QLabel("Password Strength:", self)
        self.label_strength_pass.move(100, 400)
        self.label_strength_pass.setVisible(True)

        # show the window
        self.show()

    # -------------------------Functions-----------------------------------------------START
    def extractQR(self):
        # Create QR Code
        qr = qrcode.QRCode(version=1, box_size=11, border=1)
        qr.add_data(self.copyPass)
        qr.make()
        img = qr.make_image(fill_color='black', back_color='white')
        img.save('Generated_QR/password_qr.png')
        # Display QR Code on screen
        qr_img = QLabel(self)
        qr_img.setPixmap(QPixmap('Generated_QR/password_qr.png'))
        qr_img.move(330, 450)
        qr_img.setVisible(True)

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

    def show_chkBox(self):
        if self.checkbox_alpha.isChecked() == True:
            self.checkbox_lower_alpha.setVisible(True)
            self.checkbox_upper_alpha.setVisible(True)
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

        if (self.checkbox_alpha.isChecked() == False and self.checkbox_numbers.isChecked() == False and self.checkbox_special_char.isChecked() == False or self.checkbox_alpha.isChecked() == True and self.checkbox_lower_alpha.isChecked() == False and self.checkbox_upper_alpha.isChecked() == False):
            self.error.exec_()
        else:
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

            newpassword = ''.join(random.sample(password, len(password)))

            while (password[0] == '?' or newpassword[0] == '?'):
                newpassword = ''.join(random.sample(password, len(password)))

            self.copyPass = newpassword
            self.strength_result = zxcvbn.zxcvbn(self.copyPass)

            print("Password:", newpassword)

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

    def update_slider_value(self, value):
        self.current_label.setText(f"Current Value: {value}")
        self.current_label.adjustSize()


# -------------------------Functions-----------------------------------------------END