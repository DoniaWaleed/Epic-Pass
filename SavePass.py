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

# -------------------------Class SavePass------------------------------------------START
class SavePass(QWidget):

    def __init__(self, Password):
        super().__init__()

        mainLayout = QVBoxLayout()

        Hlayout_browse = QHBoxLayout()
        Flayout_data = QFormLayout()
        Hlayout_RadioBtn = QHBoxLayout()

        self.username_editText = QLineEdit()
        self.generated_pass_editText = QLineEdit(Password)
        self.link_editText = QLineEdit()
        self.notes_plain_editText = QPlainTextEdit()
        self.notes_plain_editText.setFixedHeight(130)

        self.existing_file_radio_btn = QRadioButton("Existing File")
        self.existing_file_radio_btn.setChecked(True)
        self.new_file_radio_btn = QRadioButton("New File")

        Hlayout_RadioBtn.addWidget(self.existing_file_radio_btn)
        Hlayout_RadioBtn.addWidget(self.new_file_radio_btn)

        Flayout_data.addRow("UserName: ", self.username_editText)
        Flayout_data.addRow("Password: ", self.generated_pass_editText)
        Flayout_data.addRow("URL: ", self.link_editText)
        Flayout_data.addRow("File Name: ", Hlayout_browse)
        Flayout_data.addRow("Save Type: ", Hlayout_RadioBtn)
        Flayout_data.addRow("Notes: ", self.notes_plain_editText)

        self.filename_edit = QLineEdit()
        Hlayout_browse.addWidget(self.filename_edit)

        file_browse = QPushButton('Browse')
        file_browse.clicked.connect(self.open_file_dialog)
        Hlayout_browse.addWidget(file_browse)

        button_extract = QPushButton('Extract QR', self)
        button_extract.setFixedSize(250, 50)
        button_extract.clicked.connect(self.extractQR)

        button_save = QPushButton('Save', self)
        button_save.setFixedSize(250, 50)
        button_save.clicked.connect(self.save_to_excel)

        button_reset = QPushButton('Reset', self)
        button_reset.setFixedSize(250, 50)
        button_reset.clicked.connect(self.reset)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(button_reset, 1)
        buttonLayout.addWidget(button_save, 1)

        extractLayout = QHBoxLayout()

        # Display QR Code on screen
        self.qr_img = QLabel(self)
        self.qr_img.setVisible(False)
        extractLayout.addWidget(button_extract, 1, alignment=QtCore.Qt.AlignCenter)
        extractLayout.addWidget(self.qr_img, 1)

        mainLayout.addLayout(Flayout_data)
        mainLayout.addLayout(extractLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    # -------------------------Functions-----------------------------------------------START
    def reset(self):
        self.username_editText.setText("")
        self.generated_pass_editText.setText("")
        self.link_editText.setText("")
        self.filename_edit.setText("")
        self.existing_file_radio_btn.setChecked(True)
        self.notes_plain_editText.setPlainText("")
        self.qr_img.setVisible(False)
    def extractQR(self):
        # Create QR Code
        qr = qrcode.QRCode(version=1, box_size=5, border=1)
        qr.add_data(f"Username: {self.username_editText.text()}\nPassword: {self.generated_pass_editText.text()}\nURL: {self.link_editText.text()}\nNotes: {self.notes_plain_editText.toPlainText()}")
        qr.make()
        img = qr.make_image(fill_color='black', back_color='white')
        img.save('Generated_QR/data_qr.png')

        # Display QR Code on screen
        self.qr_img.setPixmap(QPixmap('Generated_QR/data_qr.png'))
        self.qr_img.setVisible(True)

    def save_main_code(self):
        done = QMessageBox()
        done.setWindowTitle("Saved Successfully")
        done.setText("Password Saved Successfully                           ")
        done.setIcon(QMessageBox.Information)
        WindowIcon = QIcon('images/icon.jpg')
        done.setWindowIcon(WindowIcon)

        fileName = self.filename_edit.text()
        print("FileName: ", fileName)
        # new dataframe with same columns
        df = pd.DataFrame({'Username': [self.username_editText.text()], 'Pass': [self.generated_pass_editText.text()],
                           'URL': [self.link_editText.text()], 'Notes': [self.notes_plain_editText.toPlainText()]})

        if (self.existing_file_radio_btn.isChecked()):
            # read  file content
            reader = pd.read_excel(fileName)
            # create writer object
            # used engine='openpyxl' because append operation is not supported by xlsxwriter
            writer = pd.ExcelWriter(fileName, engine='openpyxl', mode='a', if_sheet_exists="overlay")
            # append new dataframe to the Excel sheet
            df.to_excel(writer, index=False, header=False, startrow=len(reader) + 1)
            # close file
            writer.close()
            done.exec_()

        elif (self.new_file_radio_btn.isChecked()):
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Sheet1"

            sheet["A1"] = "Username"
            sheet["B1"] = "Password"
            sheet["C1"] = "URL"
            sheet["D1"] = "Notes"

            sheet["A2"] = self.username_editText.text()
            sheet["B2"] = self.generated_pass_editText.text()
            sheet["C2"] = self.link_editText.text()
            sheet["D2"] = self.notes_plain_editText.toPlainText()

            workbook.save(fileName)
            done.exec_()

    def save_to_excel(self):

        # Error Box
        error = QMessageBox()
        error.setWindowTitle("Error!!")
        error.setText("Fill All Inputs                                 ")
        error.setIcon(QMessageBox.Critical)
        WindowIcon = QIcon('images/icon.jpg')
        error.setWindowIcon(WindowIcon)

        if (self.username_editText.text() != "" and self.generated_pass_editText.text() != "" and self.link_editText.text() != "" and self.filename_edit.text() != ""):
            if (self.existing_file_radio_btn.isChecked()):
                if (Path(self.filename_edit.text()).is_file()):
                    self.save_main_code()
                else:
                    error.setText("Fill All Inputs                                 ")
                    error.exec_()
            elif (self.new_file_radio_btn.isChecked()):
                if (Path(self.filename_edit.text()).is_absolute()):
                    if (Path(self.filename_edit.text()).is_dir()):
                        error.setText("Choose Correct Path                             ")
                        error.exec_()
                    else:
                        self.save_main_code()
                else:
                    error.setText("Choose Correct Path                             ")
                    error.exec_()
            else:
                self.save_main_code()

        elif (self.username_editText.text() == "" or self.generated_pass_editText.text() == "" or self.link_editText.text() == "" or self.filename_edit.text() == ""):
            error.setText("Fill All Inputs                                 ")
            error.exec_()

    def open_file_dialog(self):
        if (self.existing_file_radio_btn.isChecked()):
            filename, ok = QFileDialog.getOpenFileName(self, "Select a File", '', 'Excel Files (*.xls *.xlsx)')

        elif (self.new_file_radio_btn.isChecked()):
            filename, ok = QFileDialog.getSaveFileName(self, "Save file", "", 'Excel Files (*.xlsx)')

        if filename:
            path = Path(filename)
            self.filename_edit.setText(str(path))


# -------------------------Functions-----------------------------------------------END
# -------------------------Class SavePass------------------------------------------END