import sys
import random
from pathlib import Path
import pandas as pd
import qrcode
from openpyxl import *
import zxcvbn

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from openpyxl.workbook.protection import WorkbookProtection

import Epic_Pass
import LocalDB
from LocalDB import *
from SavePass_DataBase import *


# -------------------------Class SavePass------------------------------------------START
class SavePass(QWidget):

    def __init__(self, Password, dbObject1, dbObject2):
        super().__init__()

        self.secure_db_object = None
        self.dbObject = dbObject1
        self.dbObject2 = dbObject2

        self.Password = Password

        mainLayout = QVBoxLayout()

        Hlayout_browse = QHBoxLayout()
        Flayout_data = QFormLayout()
        Hlayout_RadioBtn = QHBoxLayout()

        # Create Extract action
        self.extractAction = QAction(QIcon('images/qr.jpg'), '&Extract QR', self)
        self.extractAction.setStatusTip('Extracting as QR..')
        self.extractAction.triggered.connect(self.extractQR)

        # Create Reset action
        self.resetAction = QAction('&Reset', self)
        self.resetAction.setStatusTip('Resetting the Page..')
        self.resetAction.triggered.connect(self.reset)

        # Create menu bar and add action
        menuBar = QMenuBar(None)
        menuBar.adjustSize()
        fileMenu = QMenu("&Options", self)
        fileMenu.adjustSize()
        # fileMenu.setIcon(QIcon('images/settings.png'))
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.extractAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.resetAction)


        self.username_editText = QLineEdit()
        self.username_editText.adjustSize()
        self.generated_pass_editText = QLineEdit(Password)
        self.generated_pass_editText.adjustSize()
        self.link_editText = QLineEdit()
        self.link_editText.adjustSize()
        self.notes_plain_editText = QPlainTextEdit()
        self.notes_plain_editText.adjustSize()
        # self.notes_plain_editText.setMinimumHeight(80)

        self.existing_file_radio_btn = QRadioButton("Existing File")
        self.existing_file_radio_btn.adjustSize()
        self.new_file_radio_btn = QRadioButton("New File")
        self.new_file_radio_btn.adjustSize()
        self.database_radio_btn = QRadioButton("Database")
        self.database_radio_btn.adjustSize()
        self.database_radio_btn.setChecked(True)
        self.category_combobox = QComboBox()
        self.category_combobox.adjustSize()
        self.category_combobox.addItems(['Others', 'Email addresses', 'Passwords', 'Secure Notes'])

        Hlayout_RadioBtn.addWidget(self.existing_file_radio_btn)
        Hlayout_RadioBtn.addWidget(self.new_file_radio_btn)
        Hlayout_RadioBtn.addWidget(self.database_radio_btn)

        Flayout_data.addRow("UserName: ", self.username_editText)
        Flayout_data.addRow("Password: ", self.generated_pass_editText)
        Flayout_data.addRow("URL: ", self.link_editText)
        Flayout_data.addRow("File Name: ", Hlayout_browse)
        Flayout_data.addRow("Category: ", self.category_combobox)
        Flayout_data.addRow("Save Type: ", Hlayout_RadioBtn)
        Flayout_data.addRow("Notes: ", self.notes_plain_editText)

        self.filename_edit = QLineEdit()
        self.filename_edit.adjustSize()
        Hlayout_browse.addWidget(self.filename_edit)

        file_browse = QPushButton('Browse')
        file_browse.adjustSize()
        file_browse.clicked.connect(self.open_file_dialog)
        Hlayout_browse.addWidget(file_browse)

        # button_extract = QPushButton('Extract QR', self)
        # button_extract.setFixedSize(250, 50)
        # button_extract.clicked.connect(self.extractQR)
        #
        # button_reset = QPushButton('Reset', self)
        # button_reset.setFixedSize(250, 50)
        # button_reset.clicked.connect(self.reset)

        button_save = QPushButton('Save', self)
        button_save.adjustSize()
        # button_save.setMinimumSize(250, 50)
        button_save.clicked.connect(self.save)


        buttonLayout = QHBoxLayout()
        # buttonLayout.addWidget(button_reset, 1, QtCore.Qt.AlignCenter)
        buttonLayout.addWidget(button_save, 1, QtCore.Qt.AlignCenter)

        extractLayout = QHBoxLayout()

        # Display QR Code on screen
        self.qr_img = QLabel(self)
        self.qr_img.adjustSize()
        self.qr_img.setVisible(False)
        # extractLayout.addWidget(button_extract, 1, alignment=QtCore.Qt.AlignCenter)
        extractLayout.addWidget(self.qr_img, 1, alignment=QtCore.Qt.AlignCenter)

        mainLayout.addWidget(menuBar)
        mainLayout.addLayout(Flayout_data)
        mainLayout.addLayout(extractLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    # -------------------------Functions-----------------------------------------------START

    def save_main_code(self):
        done = QMessageBox()
        done.setWindowTitle("Saved Successfully")
        done.setText("Password Saved Successfully                           ")
        done.setIcon(QMessageBox.Information)
        WindowIcon = QIcon('images/icon.png')
        done.setWindowIcon(WindowIcon)

        fileName = self.filename_edit.text()

        # new dataframe with same columns
        df = pd.DataFrame({'Username': [self.username_editText.text()], 'Pass': [self.generated_pass_editText.text()],
                           'URL': [self.link_editText.text()], 'Notes': [self.notes_plain_editText.toPlainText()], 'Category': [self.category_combobox.currentText()]})

        if(self.database_radio_btn.isChecked()):
            print("FileName: DataBase")

            path_to_db_exists = os.path.exists('./Password_Manager.db')
            table_decrypted = self.dbObject2.getFromTable_decrypted('Password_Manager')
            duplicate_found = False
            if path_to_db_exists:
                for row in table_decrypted:
                    if self.generated_pass_editText.text().strip() in row:
                        error = QMessageBox()
                        error.setWindowTitle("Error!!")
                        error.setIcon(QMessageBox.Critical)
                        error.setWindowIcon(QIcon('images/icon.png'))
                        error.setText("Password already in Database                       ")
                        error.exec()
                        duplicate_found = True
                        break
                if not duplicate_found:
                    data = [self.username_editText.text(), self.generated_pass_editText.text(),
                            self.link_editText.text(),
                            self.notes_plain_editText.toPlainText(), self.category_combobox.currentText()]
                    self.dbObject2.insertIntoTable_encrypted(tableName='Password_Manager', insertList=data)

                    self.dbObject.update_table_on_adding(self.dbObject2)

                    done.setText("Password Saved Successfully to Database               ")
                    done.exec_()
            else:
                error = QMessageBox()
                error.setWindowTitle("Error!!")
                error.setIcon(QMessageBox.Critical)
                error.setWindowIcon(QIcon('images/icon.png'))
                error.setText("Please Create your Own Database First                ")
                error.exec()

        elif (self.existing_file_radio_btn.isChecked()):
            print("FileName: ", fileName)

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
            print("FileName: ", fileName)

            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Sheet1"

            sheet["A1"] = "Username"
            sheet["B1"] = "Password"
            sheet["C1"] = "URL"
            sheet["D1"] = "Notes"
            sheet["E1"] = "Category"

            sheet["A2"] = self.username_editText.text()
            sheet["B2"] = self.generated_pass_editText.text()
            sheet["C2"] = self.link_editText.text()
            sheet["D2"] = self.notes_plain_editText.toPlainText()
            sheet["E2"] = self.category_combobox.currentText()

            # # workbook.security = WorkbookProtection(workbookPassword=self.Password, lockStructure=True)
            #
            # workbook.security.workbookPassword = self.Password
            # workbook.security.lockStructure = True
            # # workbook.security = WorkbookProtection()
            # # workbook.security.set_workbook_password(self.Password, False)

            workbook.save(fileName)
            done.exec_()

    def save(self):

        # Error Box
        error = QMessageBox()
        error.setWindowTitle("Error!!")
        error.setText("Fill All Inputs                                 ")
        error.setIcon(QMessageBox.Critical)
        WindowIcon = QIcon('images/icon.png')
        error.setWindowIcon(WindowIcon)


        if (self.username_editText.text() != "" and self.generated_pass_editText.text() != "" and self.link_editText.text() != ""):
            if (self.existing_file_radio_btn.isChecked() and self.filename_edit.text() != ""):
                if (Path(self.filename_edit.text()).is_file()):
                    self.save_main_code()
                else:
                    error.setText("Choose Correct Path                             ")
                    error.exec_()
                    # error.setText("Fill All Inputs                                 ")
                    # error.exec_()
            elif (self.new_file_radio_btn.isChecked() and self.filename_edit.text() != ""):
                if (Path(self.filename_edit.text()).is_absolute()):
                    if (Path(self.filename_edit.text()).is_dir()):
                        error.setText("Choose Correct Path                             ")
                        error.exec_()
                    else:
                        self.save_main_code()
                else:
                    error.setText("Choose Correct Path                             ")
                    error.exec_()
            elif (self.database_radio_btn.isChecked() and self.filename_edit.text() == ""):
                self.save_main_code()

            else:
                if (self.existing_file_radio_btn.isChecked() or self.new_file_radio_btn.isChecked() and self.filename_edit.text() == ""):
                    error.setText("Fill All Inputs                                 ")
                    error.exec_()
                elif (self.database_radio_btn and self.filename_edit.text() != ""):
                    error.setText("Can't Fill File Name in Database Option              ")
                    error.exec_()
                # self.save_main_code()

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

    def reset(self):
        self.username_editText.setText("")
        self.generated_pass_editText.setText("")
        self.link_editText.setText("")
        self.filename_edit.setText("")
        self.database_radio_btn.setChecked(True)
        self.notes_plain_editText.setPlainText("")
        self.category_combobox.setCurrentIndex(0)
        self.qr_img.setVisible(False)

    def extractQR(self):
        # Create QR Code
        qr = qrcode.QRCode(version=1, box_size=5, border=1)
        qr.add_data(
            f"Username: {self.username_editText.text()}\nPassword: {self.generated_pass_editText.text()}\nURL: {self.link_editText.text()}\nNotes: {self.notes_plain_editText.toPlainText()}")
        qr.make()
        img = qr.make_image(fill_color='black', back_color='white')
        img.save('Generated_QR/data_qr.png')

        # Display QR Code on screen
        self.qr_img.setPixmap(QPixmap('Generated_QR/data_qr.png').scaled(80, 80))
        self.qr_img.setVisible(True)
        self.qr_img.adjustSize()

# -------------------------Functions-----------------------------------------------END
# -------------------------Class SavePass------------------------------------------END

